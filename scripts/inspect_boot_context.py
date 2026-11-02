import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

chunk = data[0xc19900 : 0xc19b00]
for p in chunk.split(b'\x00'):
    if len(p) > 2:
        print(p.decode(errors='ignore'))
