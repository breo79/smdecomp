import os
import struct

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"
ARCH_DIR = os.path.join(GAME_DIR, "Archives")

# Take a small archive first to analyze easily
files = sorted(os.listdir(ARCH_DIR))
ttarch_files = [f for f in files if f.endswith('.ttarch2')]

# Find smallest archives
sorted_by_size = sorted(ttarch_files, key=lambda f: os.path.getsize(os.path.join(ARCH_DIR, f)))
print("5 Smallest TTARCH2 files:")
for f in sorted_by_size[:5]:
    size = os.path.getsize(os.path.join(ARCH_DIR, f))
    print(f"  {f}: {size} bytes")

sample_path = os.path.join(ARCH_DIR, sorted_by_size[0])
with open(sample_path, 'rb') as fp:
    data = fp.read(512)

magic = data[:4]
print(f"\nAnalyzing {sorted_by_size[0]}:")
print(f"Magic: {magic} ({magic.hex()})")

# Let's inspect fields
ints = struct.unpack('<16I', data[:64])
print("First 16 uint32 (little endian):")
for i, val in enumerate(ints):
    print(f"  [{i:02d}] 0x{val:08x} ({val})")

# Let's inspect 8 uint64
uint64s = struct.unpack('<8Q', data[:64])
print("\nFirst 8 uint64 (little endian):")
for i, val in enumerate(uint64s):
    print(f"  [{i:02d}] 0x{val:016x} ({val})")
