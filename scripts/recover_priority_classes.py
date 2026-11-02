import pefile
import struct

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

def offset_to_va(off):
    for s in pe.sections:
        if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
            rva = s.VirtualAddress + (off - s.PointerToRawData)
            return pe.OPTIONAL_HEADER.ImageBase + rva
    return None

target_classes = [
    b'.?AVResourceLocation_TTArchive@@',
    b'.?AVTTArchive2@@',
    b'.?AVTTAllocator@@',
    b'.?AVLinearHeap@@',
    b'.?AVGameEngine@@',
    b'.?AVScene@@',
    b'.?AVPropertySet@@',
    b'.?AVSymbol@@',
    b'.?AVDataStream_Container@@'
]

results = {}

for mangled in target_classes:
    td_off = data.find(mangled)
    if td_off == -1:
        print(f"TypeDescriptor for {mangled.decode()} not found.")
        continue
    # In MSVC TypeDescriptor, the string starts 16 bytes into the structure
    td_struct_off = td_off - 16
    td_va = offset_to_va(td_struct_off)
    td_rva = td_va - pe.OPTIONAL_HEADER.ImageBase
    
    # In x64 MSVC RTTI, CompleteObjectLocator has:
    # signature (uint32 = 1)
    # offset (uint32 = 0)
    # cdOffset (uint32 = 0)
    # type_descriptor_rva (int32 = td_rva)
    # class_hierarchy_descriptor_rva (int32)
    # object_base_rva (int32)
    # Let's search for td_rva in .rdata
    td_rva_bytes = td_rva.to_bytes(4, 'little')
    pos = 0
    cols = []
    while True:
        idx = data.find(td_rva_bytes, pos)
        if idx == -1: break
        # check if it is part of COL: signature at idx - 12 should be 1
        if idx >= 12:
            sig = int.from_bytes(data[idx-12:idx-8], 'little')
            off_in_obj = int.from_bytes(data[idx-8:idx-4], 'little')
            if sig == 1 and off_in_obj == 0:
                col_off = idx - 12
                col_va = offset_to_va(col_off)
                cols.append(col_va)
        pos = idx + 1
        
    # Now find vtable: vtable[-1] (8 bytes before vtable) points to COL_VA
    vtables = []
    for col_va in cols:
        col_va_bytes = col_va.to_bytes(8, 'little')
        pos = 0
        while True:
            idx = data.find(col_va_bytes, pos)
            if idx == -1: break
            vtable_va = offset_to_va(idx + 8)
            vtables.append(vtable_va)
            pos = idx + 1
            
    results[mangled.decode()] = {
        'td_va': hex(td_va),
        'cols': [hex(c) for c in cols],
        'vtables': [hex(v) for v in vtables]
    }

for cls_name, info in results.items():
    print(f"\nClass: {cls_name}")
    print(f"  TypeDescriptor VA: {info['td_va']}")
    print(f"  CompleteObjectLocators: {info['cols']}")
    print(f"  Vtables: {info['vtables']}")
