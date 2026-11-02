import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

def offset_to_va(offset):
    for s in pe.sections:
        raw_start = s.PointerToRawData
        raw_end = raw_start + s.SizeOfRawData
        if raw_start <= offset < raw_end:
            rva = s.VirtualAddress + (offset - raw_start)
            return pe.OPTIONAL_HEADER.ImageBase + rva
    return None

p_box_va = offset_to_va(0xc3b560)
print(f"Blowfish P-box VA: {hex(p_box_va)}")

# Search for references in .text
text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_raw = text_sec.PointerToRawData
text_size = text_sec.SizeOfRawData

# Search for lea rxx, [rip + disp32] or mov rxx, [rip + disp32]
# rip + len + disp32 = p_box_va
refs = []
for i in range(text_size - 7):
    # check 7-byte instruction with disp32 at offset 3
    # 48 8d xx xx xx xx xx (lea reg, [rip + disp])
    b0 = data[text_raw + i]
    if b0 in [0x48, 0x4c]:
        b1 = data[text_raw + i + 1]
        if b1 == 0x8d: # lea
            disp = int.from_bytes(data[text_raw + i + 3 : text_raw + i + 7], byteorder='little', signed=True)
            cur_va = text_start_va + i
            if cur_va + 7 + disp == p_box_va:
                refs.append(cur_va)

print(f"References to Blowfish P-box ({len(refs)}): {[hex(r) for r in refs]}")
