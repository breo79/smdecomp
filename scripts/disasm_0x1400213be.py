import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

target_va = 0x1400213be
rva = target_va - pe.OPTIONAL_HEADER.ImageBase
offset = text_sec.PointerToRawData + (rva - text_sec.VirtualAddress)

code = data[offset - 40 : offset + 60]
for ins in md.disasm(code, target_va - 40):
    prefix = "==> " if ins.address == target_va else "    "
    print(f"{prefix}0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
