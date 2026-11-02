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

target_va = 0x1404cda20

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

for l in [5, 6, 7]:
    for i in range(text_size - l):
        disp = int.from_bytes(data[text_raw + i + (l-4) : text_raw + i + l], byteorder='little', signed=True)
        cur_va = text_start_va + i
        if cur_va + l + disp == target_va:
            print(f"Reference with length {l} at VA {hex(cur_va)}")
            code = data[text_raw + i : text_raw + i + 15]
            for ins in md.disasm(code, cur_va):
                print(f"  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}")
                break
