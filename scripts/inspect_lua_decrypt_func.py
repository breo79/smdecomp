import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

def offset_to_va(off):
    for s in pe.sections:
        if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
            rva = s.VirtualAddress + (off - s.PointerToRawData)
            return pe.OPTIONAL_HEADER.ImageBase + rva
    return None

va_code = offset_to_va(0x159852)
va_rdata = offset_to_va(0xc49080)

print(f"Code VA: {hex(va_code)} (offset 0x159852)")
print(f"RDATA VA: {hex(va_rdata)} (offset 0xc49080)")

print("\nRDATA context:")
print("Hex:", data[0xc49070:0xc490c0].hex())
print("ASCII:", data[0xc49070:0xc490c0])

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
code = data[0x159800:0x159900]
print("\nDisassembly around 0x159852:")
for ins in md.disasm(code, offset_to_va(0x159800)):
    prefix = "==> " if ins.address == va_code else "    "
    print(f"{prefix}0x{ins.address:x}: \t{ins.mnemonic}\t{ins.op_str}")
