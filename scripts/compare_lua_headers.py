import os

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"
ARCH_DIR = os.path.join(GAME_DIR, "Archives")

sample_lua = [
    "_resdesc_50_Boot.lua",
    "_resdesc_50_Chinese.lua",
    "_resdesc_50_Arabic.lua"
]

for name in sample_lua:
    p = os.path.join(ARCH_DIR, name)
    with open(p, 'rb') as fp:
        data = fp.read()
    print(f"{name} ({len(data)} bytes):")
    print("  Hex:", data[:32].hex())
    print("  ASCII:", "".join(chr(b) if 32 <= b < 127 else "." for b in data[:32]))
