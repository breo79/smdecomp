import pefile
import capstone
import re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_raw = text_sec.PointerToRawData
text_size = text_sec.SizeOfRawData

def va_to_offset(va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    return text_raw + (rva - text_sec.VirtualAddress)

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# Disassemble all functions in 0x14016b000 to 0x14016e000
# Look for 0x60 offset references: cmp/mov/test byte ptr [reg + 0x60]
start_va = 0x14016b000
end_va = 0x14016f000
code = data[va_to_offset(start_va) : va_to_offset(end_va)]

print(f"Scanning disassembly between {hex(start_va)} and {hex(end_va)} for +0x60 and calls...")
for ins in md.disasm(code, start_va):
    op = ins.op_str
    if '+ 0x60]' in op or '+ 0x60' in op:
        print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
