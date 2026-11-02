import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

target_va = 0x1404cda20.to_bytes(8, 'little')
pos = 0
found = []
while True:
    idx = data.find(target_va, pos)
    if idx == -1: break
    found.append(idx)
    pos = idx + 1

for off in found:
    for s in pe.sections:
        if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
            rva = s.VirtualAddress + (off - s.PointerToRawData)
            va = pe.OPTIONAL_HEADER.ImageBase + rva
            print(f"Offset {hex(off)} in {s.Name.decode().strip(chr(0))} -> VA: {hex(va)}")
