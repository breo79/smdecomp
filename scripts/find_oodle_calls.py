import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)

# Find IAT entry for OodleLZ_Decompress
oodle_decomp_iat = None
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    if b'oo2core' in entry.dll.lower():
        for imp in entry.imports:
            if imp.name == b'OodleLZ_Decompress':
                oodle_decomp_iat = imp.address
                print(f"OodleLZ_Decompress IAT: {hex(oodle_decomp_iat)}")

with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_raw = text_sec.PointerToRawData
text_size = text_sec.SizeOfRawData

# Search for calls to OodleLZ_Decompress (ff 15 / call [rip + offset])
# rip + 6 + offset = oodle_decomp_iat
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

for i in range(text_size - 6):
    b0, b1 = data[text_raw + i], data[text_raw + i + 1]
    if b0 == 0xff and b1 == 0x15: # call [rip + disp32]
        disp = int.from_bytes(data[text_raw + i + 2 : text_raw + i + 6], byteorder='little', signed=True)
        current_va = text_start_va + i
        target_va = current_va + 6 + disp
        if target_va == oodle_decomp_iat:
            print(f"Call to OodleLZ_Decompress at VA: {hex(current_va)}")
