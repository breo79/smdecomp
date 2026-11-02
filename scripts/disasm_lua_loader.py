import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def offset_to_va(off):
    rva = off - text_sec.PointerToRawData
    return pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress + rva

# Disassemble from offset 0x159800 to 0x159980
code = data[0x159820 : 0x1599a0]
for ins in md.disasm(code, offset_to_va(0x159820)):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
