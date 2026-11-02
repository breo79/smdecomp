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

str_va = 0x1400213b7 + 7 + 0xc9e6f2
off = va_to_offset(str_va)
print(f"String VA: {hex(str_va)} (file offset: {hex(off)})")
chunk = data[off : off + 200]
print("Raw bytes:", chunk[:64].hex())
print("ASCII:", chunk.split(b'\x00')[0].decode('ascii', errors='ignore'))

# Also check rcx: 0x1400213c5 + 7 + 0x1104854 = 0x141125c20
rcx_va = 0x1400213c5 + 7 + 0x1104854
off2 = va_to_offset(rcx_va)
print(f"RCX VA: {hex(rcx_va)} (file offset: {hex(off2)})")
