import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

start_va = 0x14016b640
start_rva = start_va - pe.OPTIONAL_HEADER.ImageBase
start_offset = text_sec.PointerToRawData + (start_rva - text_sec.VirtualAddress)

code = data[start_offset : start_offset + 0x300]
for ins in md.disasm(code, start_va):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
