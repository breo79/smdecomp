import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def va_to_offset(va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    return text_sec.PointerToRawData + (rva - text_sec.VirtualAddress)

# Let's inspect 0x140021300 to 0x140021500
code = data[va_to_offset(0x140021300) : va_to_offset(0x1400214a0)]
for ins in md.disasm(code, 0x140021300):
    print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
