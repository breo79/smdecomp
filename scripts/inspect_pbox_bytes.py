import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Let's inspect bytes from 0xc3b550 to 0xc3b5c0
print(data[0xc3b550:0xc3b5c0].hex())

# Let's check which section this is in
for s in pe.sections:
    if s.PointerToRawData <= 0xc3b560 < s.PointerToRawData + s.SizeOfRawData:
        print(f"Section: {s.Name.decode().strip(chr(0))}")
