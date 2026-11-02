import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

target_va = 0x1408f6e5e
target_rva = target_va - pe.OPTIONAL_HEADER.ImageBase
target_offset = text_sec.PointerToRawData + (target_rva - text_sec.VirtualAddress)

# Disassemble 0x100 bytes around target_va
start_offset = target_offset - 0x60
start_va = target_va - 0x60
code = data[start_offset : start_offset + 0x120]
for ins in md.disasm(code, start_va):
    prefix = "==> " if ins.address == target_va else "    "
    print(f"{prefix}0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
