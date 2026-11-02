import pefile

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)

pdata_sec = [s for s in pe.sections if s.Name.startswith(b'.pdata')][0]
entry_count = pdata_sec.SizeOfRawData // 12
print(f"Total .pdata function entries: {entry_count}")
