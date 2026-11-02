import os, re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Find source file paths
source_files = set(re.findall(rb'[A-Za-z]:\\[^:\*\?"<>\|\r\n]+\.(?:cpp|c|h|inl)', data, re.IGNORECASE))
print(f"Total source file paths found in binary: {len(source_files)}")
sorted_sources = sorted([s.decode('utf-8', errors='ignore') for s in source_files])
for s in sorted_sources[:50]:
    print(s)

# Look for TTArchive2 strings / function names / log messages
ttarch_refs = [m.group(0).decode('utf-8', errors='ignore') 
               for m in re.finditer(rb'[ -~]{4,}', data) 
               if b'archive' in m.group(0).lower() or b'ttarch' in m.group(0).lower()]
print(f"\nArchive related strings ({len(ttarch_refs)}):")
for s in ttarch_refs[:30]:
    print(" ", s)
