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

target_va = 0x14015a420
rva = target_va - pe.OPTIONAL_HEADER.ImageBase
offset = text_sec.PointerToRawData + (rva - text_sec.VirtualAddress)

code = data[offset - 80 : offset + 20]
for ins in md.disasm(code, target_va - 80):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
