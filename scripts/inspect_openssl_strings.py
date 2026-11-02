import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Let's inspect strings around 0xd80a00 to 0xd80c00
chunk = data[0xd80a00:0xd80c00]
parts = chunk.split(b'\x00')
for p in parts:
    if len(p) > 2:
        print(p.decode(errors='ignore'))
