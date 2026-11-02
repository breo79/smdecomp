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

vtable_va = 0x140c4bfa8
off = va_to_offset(vtable_va)
# In MSVC x64 RTTI, vtable[-1] (8 bytes before vtable) points to CompleteObjectLocator
col_ptr_off = off - 8
col_va = int.from_bytes(data[col_ptr_off : col_ptr_off + 8], 'little')
print(f"Vtable VA: {hex(vtable_va)}, COL VA: {hex(col_va)}")

col_off = va_to_offset(col_va)
if col_off:
    # CompleteObjectLocator in x64:
    # uint32 signature (1 for 64-bit)
    # uint32 offset
    # uint32 cdOffset
    # int32 type_descriptor_rva
    # int32 class_descriptor_rva
    # int32 object_base_rva
    sig = int.from_bytes(data[col_off : col_off + 4], 'little')
    td_rva = int.from_bytes(data[col_off + 12 : col_off + 16], 'little', signed=True)
    td_va = pe.OPTIONAL_HEADER.ImageBase + td_rva
    td_off = va_to_offset(td_va)
    # TypeDescriptor has pVFTable (8 bytes), spare (8 bytes), then mangled name
    name = data[td_off + 16 : td_off + 80].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"COL TypeDescriptor VA: {hex(td_va)}, Name: {name}")
