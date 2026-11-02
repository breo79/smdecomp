import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

target_va = 0x1408f6da1
rva = target_va - pe.OPTIONAL_HEADER.ImageBase
offset = text_sec.PointerToRawData + (rva - text_sec.VirtualAddress)

# Let's search back for int3 padding (0xcc 0xcc)
cur = offset
while cur > offset - 0x500:
    if data[cur-2:cur] == b'\xcc\xcc':
        func_start_offset = cur
        break
    cur -= 1

func_start_rva = text_sec.VirtualAddress + (func_start_offset - text_sec.PointerToRawData)
func_start_va = pe.OPTIONAL_HEADER.ImageBase + func_start_rva
print(f"Function start: {hex(func_start_va)}")

code = data[func_start_offset : offset + 20]
for ins in md.disasm(code, func_start_va):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
    if ins.address >= 0x1408f6da5:
        break
