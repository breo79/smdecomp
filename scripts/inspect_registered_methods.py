import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

def va_to_offset(va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None

class_ptr_va = 0x14102ac78
off = va_to_offset(class_ptr_va)
# In .data, let's see what pointer or value is there
val = int.from_bytes(data[off : off + 8], 'little')
print(f"Value at 0x14102ac78: {hex(val)}")

# Let's check string references around 0x1400213b0
for start in range(0x140021350, 0x1400214a0, 0x30):
    pass

# Let's print all method name strings in that range
import capstone
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
text_sec = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
code = data[va_to_offset(0x140021350) : va_to_offset(0x1400214a0)]
for ins in md.disasm(code, 0x140021350):
    if ins.mnemonic == 'lea' and ins.op_str.startswith('r9,'):
        # get target address of lea r9, [rip + disp]
        disp = int.from_bytes(data[va_to_offset(ins.address) + 3 : va_to_offset(ins.address) + 7], 'little', signed=True)
        t_va = ins.address + 7 + disp
        t_off = va_to_offset(t_va)
        s = data[t_off : t_off + 64].split(b'\x00')[0].decode('ascii', errors='ignore')
        print(f"Method at {hex(ins.address)}: {s}")
