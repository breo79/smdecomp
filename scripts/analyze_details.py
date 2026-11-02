import os
import re
import pefile
import struct

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"
EXE_PATH = os.path.join(GAME_DIR, "Minecraft2.exe")

def analyze_strings_and_rtti():
    with open(EXE_PATH, 'rb') as f:
        data = f.read()

    # Find ASCII strings
    ascii_re = re.compile(b'[ -~]{5,}')
    strings = [m.group(0).decode('ascii', errors='ignore') for m in ascii_re.finditer(data)]
    
    # RTTI class names
    rtti_classes = [s for s in strings if s.startswith('.?AV') or s.startswith('.?AU')]
    
    # Engine / build strings
    keywords = ['telltale', 'tool', 'engine', 'build', 'version', 'mc2', 'lua', 'oodle', 'fmod', 'ttarch']
    matching_strings = {}
    for kw in keywords:
        matching_strings[kw] = [s for s in strings if kw in s.lower()][:25]
        
    return rtti_classes, matching_strings

def analyze_archive(sample_path):
    with open(sample_path, 'rb') as f:
        header = f.read(128)
    return {
        'path': os.path.basename(sample_path),
        'size': os.path.getsize(sample_path),
        'magic': header[:4],
        'magic_hex': header[:4].hex(),
        'header_hex': header[:64].hex()
    }

if __name__ == '__main__':
    rtti, kw_strings = analyze_strings_and_rtti()
    print(f"Total RTTI classes found: {len(rtti)}")
    print("Sample RTTI classes (first 30):")
    for c in rtti[:30]:
        print(" ", c)
        
    print("\n--- Key String Matches ---")
    for kw, matches in kw_strings.items():
        print(f"\nKeyword: {kw} (Count sample: {len(matches)})")
        for m in matches[:10]:
            print(f"  {m}")
            
    # Sample ttarch2
    arch_dir = os.path.join(GAME_DIR, "Archives")
    samples = [f for f in os.listdir(arch_dir) if f.endswith('.ttarch2')][:5]
    print("\n--- Sample TTARCH2 Headers ---")
    for s in samples:
        info = analyze_archive(os.path.join(arch_dir, s))
        print(f"{info['path']}: magic={info['magic']} (hex: {info['magic_hex']}), size={info['size']}")
        print(f"  first 64 bytes: {info['header_hex']}")
