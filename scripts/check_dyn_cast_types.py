import pefile

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

for va in [0x141050ed0, 0x14104eb18, 0x141050eb0]:
    off = va_to_offset(va)
    if off:
        print(f"VA {hex(va)} (offset {hex(off)}):")
        # In MSVC TypeDescriptor, string starts at offset + 16 (after pVFTable and spare)
        name = data[off + 16 : off + 100].split(b'\x00')[0]
        print(f"  Mangled: {name.decode(errors='ignore')}")
