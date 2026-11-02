import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Search for 64-bit pointer or 32-bit RVA to 0x140c3c560 or 0xc3c560
target_va = 0x140c3c560.to_bytes(8, 'little')
target_rva = 0xc3c560.to_bytes(4, 'little')

print("Occurrences of target_va in entire binary:")
pos = 0
while True:
    idx = data.find(target_va, pos)
    if idx == -1: break
    print(f"  VA pointer at file offset: {hex(idx)}")
    pos = idx + 1

print("Occurrences of target_rva in entire binary:")
pos = 0
while True:
    idx = data.find(target_rva, pos)
    if idx == -1: break
    print(f"  RVA pointer at file offset: {hex(idx)}")
    pos = idx + 1
