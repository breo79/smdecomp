import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)

for entry in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in entry.imports:
        if imp.address in [0x140c0a170, 0x140c0a178, 0x140c0a180, 0x140c0a188]:
            print(f"IAT 0x{imp.address:x}: {entry.dll.decode()} -> {imp.name.decode()}")
