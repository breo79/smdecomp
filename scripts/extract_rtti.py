import os
import re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Match all .?AV and .?AU symbols
rtti_raw = set(re.findall(rb'\.\?[AU][A-Za-z0-9_@$?]+', data))
print(f"Found {len(rtti_raw)} unique decorated type descriptor symbols.")

# Let's see some samples
samples = sorted([s.decode('ascii', errors='ignore') for s in rtti_raw])
with open("project/findings/rtti_classes_raw.txt", "w", encoding="utf-8") as out:
    for s in samples:
        out.write(s + "\n")

print("Saved raw RTTI list to project/findings/rtti_classes_raw.txt")
