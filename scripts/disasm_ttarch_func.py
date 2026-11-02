import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

# .text section bounds
text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_data = data[text_sec.PointerToRawData : text_sec.PointerToRawData + text_sec.SizeOfRawData]

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# Find function start backwards from 0x14016b64e
target_va = 0x14016b64e
target_rva = target_va - pe.OPTIONAL_HEADER.ImageBase
target_offset = text_sec.PointerToRawData + (target_rva - text_sec.VirtualAddress)

# Let's search backwards for common prologues (push rbp, sub rsp, etc.)
cur = target_offset
while cur > target_offset - 0x1000:
    # check for CC CC (padding) or standard prologue
    if data[cur:cur+2] == b'\x48\x89' or data[cur:cur+1] == b'\x40' or data[cur:cur+1] == b'\x48':
        if data[cur-1] == 0xcc or data[cur-2:cur] == b'\xcc\xcc':
            func_start_offset = cur
            break
    cur -= 1

func_start_rva = text_sec.VirtualAddress + (func_start_offset - text_sec.PointerToRawData)
func_start_va = pe.OPTIONAL_HEADER.ImageBase + func_start_rva

print(f"Function start candidate: VA {hex(func_start_va)} (file offset: {hex(func_start_offset)})")

# Disassemble from func_start_va for 0x300 bytes
code = data[func_start_offset : func_start_offset + 0x400]
for ins in md.disasm(code, func_start_va):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
    if ins.address > target_va + 0x60:
        break
