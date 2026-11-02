import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

def va_to_offset(va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None

def disasm_func(va, length=64):
    off = va_to_offset(va)
    if off is None:
        print(f"Cannot resolve VA 0x{va:x}")
        return
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = data[off : off + length]
    print(f"\n--- Disassembly of 0x{va:x} ---")
    for insn in cs.disasm(code, va):
        print(f"  0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")

# 1. Disassemble 0x140107470
disasm_func(0x140107470, 0x80)

# 2. Check callers of Blowfish_InitContext (0x140107560)
print("\nSearching calls to Blowfish_InitContext (0x140107560)...")
text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
end_va = start_va + text_sec.Misc_VirtualSize
text_data = data[text_sec.PointerToRawData : text_sec.PointerToRawData + text_sec.SizeOfRawData]

target = 0x140107560
for i in range(len(text_data) - 5):
    if text_data[i] == 0xe8:
        disp = int.from_bytes(text_data[i+1:i+5], 'little', signed=True)
        cur_va = start_va + i
        if cur_va + 5 + disp == target:
            print(f"  Call from 0x{cur_va:x}")

# 3. Disassemble TTArchive2_InitializeIndex (0x14016c4e0)
disasm_func(0x14016c4e0, 0xb0)
