import pefile
import re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

matches = [m.start() for m in re.finditer(rb'resdesc', data, re.IGNORECASE)]
print(f"Occurrences of 'resdesc': {len(matches)}")
for m in matches:
    print(f"Offset {hex(m)}: {data[max(0, m-20):m+60]}")
