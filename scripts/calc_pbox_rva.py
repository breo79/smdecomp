import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)

for s in pe.sections:
    name = s.Name.decode().strip(chr(0))
    if s.PointerToRawData <= 0xc3b560 < s.PointerToRawData + s.SizeOfRawData:
        rva = s.VirtualAddress + (0xc3b560 - s.PointerToRawData)
        va = pe.OPTIONAL_HEADER.ImageBase + rva
        print(f"Section {name}: PointerToRawData={hex(s.PointerToRawData)}, VirtualAddress={hex(s.VirtualAddress)}")
        print(f"File offset 0xc3b560 -> RVA: {hex(rva)} -> VA: {hex(va)}")
