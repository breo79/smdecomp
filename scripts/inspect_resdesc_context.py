import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

chunk = data[0xc64b00 : 0xc65200]
pos = 0
for part in chunk.split(b'\x00'):
    if len(part) > 2:
        print(f"[{len(part)}] {part.decode(errors='ignore')}")
