import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def disasm_range(start_va, count_bytes):
    rva = start_va - pe.OPTIONAL_HEADER.ImageBase
    offset = text_sec.PointerToRawData + (rva - text_sec.VirtualAddress)
    code = data[offset : offset + count_bytes]
    for ins in md.disasm(code, start_va):
        print(f"0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")

print("=== Disassembly of 0x140425ab0 around Blowfish_ProcessBlocks (0x140425e08) ===")
disasm_range(0x140425dd0, 0x90)

print("\n=== Disassembly around Blowfish_InitContext call (0x1404cda94) ===")
disasm_range(0x1404cda40, 0xb0)
