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

# Blowfish loop typically has 16 iterations: cmp reg, 16 or 0x10 or unrolled 16 rounds.
# In OpenSSL or custom Blowfish:
# Let's search for 16-round loop or unrolled rounds
# Or search for references to 0xc3b5b0 (the S-box start VA: 0x140c3c5b0)
sbox_va = 0x140c3c5b0
print(f"Searching for references to S-box VA: {hex(sbox_va)}")

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

for i in range(text_size - 7):
    # check disp32 for 7-byte instruction
    disp = int.from_bytes(data[text_raw + i + 3 : text_raw + i + 7], byteorder='little', signed=True)
    cur_va = text_start_va + i
    if cur_va + 7 + disp == sbox_va:
        print(f"Direct reference to S-box at VA: {hex(cur_va)}")
        code = data[text_raw + i : text_raw + i + 15]
        for ins in md.disasm(code, cur_va):
            print(f"  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}")
            break
