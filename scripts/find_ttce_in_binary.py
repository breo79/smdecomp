import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Search for magic 0x54544345 or b'TTCE' or b'ECTT'
target_le = b'TTCE'
target_be = b'ECTT'

offsets_le = []
pos = 0
while True:
    idx = data.find(target_le, pos)
    if idx == -1: break
    offsets_le.append(idx)
    pos = idx + 1

offsets_be = []
pos = 0
while True:
    idx = data.find(target_be, pos)
    if idx == -1: break
    offsets_be.append(idx)
    pos = idx + 1

print(f"Occurrences of 'TTCE': {[hex(x) for x in offsets_le]}")
print(f"Occurrences of 'ECTT': {[hex(x) for x in offsets_be]}")

# Also search for "ttarch2" string
pos = 0
while True:
    idx = data.find(b'ttarch2', pos)
    if idx == -1: break
    print(f"'ttarch2' at file offset {hex(idx)}: {data[idx-10:idx+30]}")
    pos = idx + 1
