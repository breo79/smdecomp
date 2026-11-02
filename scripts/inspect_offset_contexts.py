import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

def get_va(offset):
    for s in pe.sections:
        raw_start = s.PointerToRawData
        raw_end = raw_start + s.SizeOfRawData
        if raw_start <= offset < raw_end:
            rva = s.VirtualAddress + (offset - raw_start)
            return hex(pe.OPTIONAL_HEADER.ImageBase + rva)
    return "unknown"

for off in [0x16a777, 0x16aa4e, 0x16aa79, 0xc578b2, 0xc578e2, 0xc57912]:
    va = get_va(off)
    context = data[max(0, off - 32):off + 48]
    print(f"\nOffset: {hex(off)} -> VA: {va}")
    print(f"Hex: {context.hex()}")
    # print string representation if printable
    printable = "".join(chr(b) if 32 <= b < 127 else "." for b in context)
    print(f"ASCII: {printable}")
