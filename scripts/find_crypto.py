import pefile
import re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"

with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Look for crypto strings
crypto_kws = [b'blowfish', b'BF_set_key', b'BF_ecb_encrypt', b'BF_cbc_encrypt', 
              b'AES_', b'EVP_', b'encryption', b'decrypt', b'cipher']

for kw in crypto_kws:
    matches = [m.start() for m in re.finditer(re.escape(kw), data, re.IGNORECASE)]
    print(f"{kw.decode()}: {len(matches)} occurrences")

# Check for Blowfish S-box constants (P-array: 0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344)
p_box_start = bytes.fromhex("886a3f24 d308a385 2e8a1913 44737003".replace(" ", ""))
idx = data.find(p_box_start)
if idx != -1:
    print(f"Found standard Blowfish P-box at offset: {hex(idx)}")
else:
    print("Standard Blowfish P-box not found directly.")
