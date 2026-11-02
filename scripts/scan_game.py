import os
import sys
import hashlib
import pefile

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"

def scan_files():
    records = []
    for root, dirs, files in os.walk(GAME_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, GAME_DIR)
            size = os.path.getsize(full_path)
            _, ext = os.path.splitext(f)
            records.append({
                'rel_path': rel_path,
                'full_path': full_path,
                'size': size,
                'ext': ext.lower()
            })
    return records

def analyze_pe(exe_path):
    pe = pefile.PE(exe_path)
    arch = "x64" if pe.FILE_HEADER.Machine == 0x8664 else "x86"
    timestamp = pe.FILE_HEADER.TimeDateStamp
    linker_major = pe.OPTIONAL_HEADER.MajorLinkerVersion
    linker_minor = pe.OPTIONAL_HEADER.MinorLinkerVersion
    entry_point = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    image_base = hex(pe.OPTIONAL_HEADER.ImageBase)
    
    sections = []
    for s in pe.sections:
        name = s.Name.decode('utf-8', errors='ignore').strip('\x00')
        sections.append({
            'name': name,
            'virtual_address': hex(s.VirtualAddress),
            'virtual_size': hex(s.Misc_VirtualSize),
            'raw_size': hex(s.SizeOfRawData)
        })
        
    imports = {}
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll_name = entry.dll.decode('utf-8', errors='ignore')
            imports[dll_name] = []
            for imp in entry.imports:
                name = imp.name.decode('utf-8', errors='ignore') if imp.name else f"Ordinal({imp.ordinal})"
                imports[dll_name].append(name)
                
    exports = []
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            name = exp.name.decode('utf-8', errors='ignore') if exp.name else f"Ordinal({exp.ordinal})"
            exports.append((exp.ordinal, hex(exp.address), name))
            
    return {
        'arch': arch,
        'timestamp': timestamp,
        'linker_version': f"{linker_major}.{linker_minor}",
        'entry_point': entry_point,
        'image_base': image_base,
        'sections': sections,
        'imports': imports,
        'exports': exports
    }

if __name__ == '__main__':
    files = scan_files()
    print(f"Total files: {len(files)}")
    exe_path = os.path.join(GAME_DIR, "Minecraft2.exe")
    pe_info = analyze_pe(exe_path)
    print(f"Arch: {pe_info['arch']}, Linker: {pe_info['linker_version']}, Base: {pe_info['image_base']}, Entry: {pe_info['entry_point']}")
    print(f"Sections: {[s['name'] for s in pe_info['sections']]}")
    print(f"Imported DLLs ({len(pe_info['imports'])}): {list(pe_info['imports'].keys())}")
