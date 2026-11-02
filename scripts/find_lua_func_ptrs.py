import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

target1 = 0x14015a420
target2 = 0x14015a480

print(f"Searching for 64-bit pointers to {hex(target1)} and {hex(target2)}:")
for t in [target1, target2]:
    t_bytes = t.to_bytes(8, 'little')
    pos = 0
    while True:
        idx = data.find(t_bytes, pos)
        if idx == -1: break
        print(f"  Pointer to {hex(t)} at file offset {hex(idx)}")
        pos = idx + 1
