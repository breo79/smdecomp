import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

for s in [b'_project.lua', b'_boot.lua', b'default.prop']:
    pos = 0
    while True:
        idx = data.find(s, pos)
        if idx == -1: break
        print(f"'{s.decode()}' at file offset {hex(idx)}")
        pos = idx + 1
