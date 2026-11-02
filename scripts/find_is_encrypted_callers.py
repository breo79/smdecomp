import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_raw = text_sec.PointerToRawData
text_size = text_sec.SizeOfRawData

target_va = 0x14016ba80

# Near call (e8 rel32)
callers = []
for i in range(text_size - 5):
    if data[text_raw + i] == 0xe8:
        rel = int.from_bytes(data[text_raw + i + 1 : text_raw + i + 5], byteorder='little', signed=True)
        cur_va = text_start_va + i
        if cur_va + 5 + rel == target_va:
            callers.append(cur_va)

print(f"Callers of IsEncrypted ({len(callers)}): {[hex(c) for c in callers]}")
