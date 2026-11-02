import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

target = bytes.fromhex("1b4c456f")
pos = 0
matches = []
while True:
    idx = data.find(target, pos)
    if idx == -1: break
    matches.append(idx)
    pos = idx + 1

print(f"Occurrences of 1b4c456f in Minecraft2.exe ({len(matches)}): {[hex(m) for m in matches]}")

# Also search for "1b 4c" with cmp instruction (38 or 3c or 80 3e 1b / 80 7e 01 4c)
target_lua = b'\x1bLua'
matches_lua = []
pos = 0
while True:
    idx = data.find(target_lua, pos)
    if idx == -1: break
    matches_lua.append(idx)
    pos = idx + 1

print(f"Occurrences of '\\x1bLua' ({len(matches_lua)}): {[hex(m) for m in matches_lua]}")
