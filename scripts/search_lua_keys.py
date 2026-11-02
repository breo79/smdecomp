import os

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"
ARCH_DIR = os.path.join(GAME_DIR, "Archives")

matches = []
for f in os.listdir(ARCH_DIR):
    if f.endswith('.lua'):
        path = os.path.join(ARCH_DIR, f)
        try:
            with open(path, 'rb') as fp:
                data = fp.read()
                if b'LoadWithEncryptionKey' in data or b'EncryptionKey' in data or b'Key' in data or b'Resource' in data:
                    matches.append((f, data))
        except Exception as e:
            pass

print(f"Found {len(matches)} .lua files with matches.")
for name, content in matches[:20]:
    # Look for printable strings
    import re
    strings = re.findall(rb'[ -~]{6,}', content)
    str_matches = [s.decode('ascii', errors='ignore') for s in strings if 'key' in s.lower() or 'resource' in s.lower() or 'load' in s.lower()]
    if str_matches:
        print(f"\nFile: {name}")
        for s in str_matches[:5]:
            print(f"  {s}")
