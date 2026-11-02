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

target_va = 0x140c3c560

# Check disp32 for instruction lengths 5, 6, 7, 8
for l in [5, 6, 7, 8]:
    for off_disp in [l - 4]: # disp32 is the last 4 bytes of instruction
        for i in range(text_size - l):
            disp = int.from_bytes(data[text_raw + i + off_disp : text_raw + i + off_disp + 4], byteorder='little', signed=True)
            cur_va = text_start_va + i
            if cur_va + l + disp == target_va:
                print(f"Match with inst len {l} at VA: {hex(cur_va)}")
                md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
                code = data[text_raw + i : text_raw + i + 15]
                for ins in md.disasm(code, cur_va):
                    print(f"  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}")
                    break
