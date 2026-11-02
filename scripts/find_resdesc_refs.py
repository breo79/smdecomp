import pefile
import capstone

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
text_start_va = pe.OPTIONAL_HEADER.ImageBase + text_sec.VirtualAddress
text_raw = text_sec.PointerToRawData
text_size = text_sec.SizeOfRawData

def offset_to_va(off):
    for s in pe.sections:
        if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
            rva = s.VirtualAddress + (off - s.PointerToRawData)
            return pe.OPTIONAL_HEADER.ImageBase + rva
    return None

str_va = offset_to_va(0xc64d61)
print(f"'_resdesc_' string VA: {hex(str_va)}")

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# Find references to str_va in text_sec
for l in [5, 6, 7]:
    for i in range(text_size - l):
        disp = int.from_bytes(data[text_raw + i + (l-4) : text_raw + i + l], byteorder='little', signed=True)
        cur_va = text_start_va + i
        if cur_va + l + disp == str_va:
            print(f"Reference at VA {hex(cur_va)}")
            code = data[text_raw + i : text_raw + i + 15]
            for ins in md.disasm(code, cur_va):
                print(f"  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}")
                break
