# Minecraft: Story Mode Season 2 - File Discovery & Asset Inventory

## Overview
- **Game Release**: Minecraft: Story Mode - Season Two (GOG Release, DRM-free)
- **Game Directory**: `C:\GOG Games\Minecraft Story Mode - Season Two`
- **Total Files**: 453 files across game root and subdirectories
- **Target Platform**: Windows 64-bit (x86_64)

---

## 1. Primary Binaries & Executables

| File Name | Size (Bytes) | Architecture | Subsystem / Role |
| :--- | :--- | :--- | :--- |
| `Minecraft2.exe` | 18,766,976 | x86_64 PE32+ | Main game engine executable |
| `CrowdPlayHost.exe` | 129,536 | x86_64 PE32+ | Telltale Crowd Play local host service |
| `UninstallCrowdPlay.exe` | 28,672 | x86_64 PE32+ | Crowd Play uninstaller utility |
| `cloudflared.exe` | 37,702,280 | x86_64 PE32+ | Cloudflare Argo Tunnel helper for Crowd Play |
| `unins000.exe` | 1,334,880 | x86_32 PE32 | Inno Setup uninstaller |

### `Minecraft2.exe` Binary Characteristics
- **Machine**: `IMAGE_FILE_MACHINE_AMD64` (0x8664)
- **Image Base**: `0x140000000`
- **Address of Entry Point**: `0x140b30b80` (RVA: `0xb30b80`)
- **Linker Version**: Microsoft Visual Studio 2015 (Linker 14.0 / MSVC 19.00)
- **PDB Path**: `C:\bambooAgent\xml-data\build-dir\BIN-MC2-P6S\TELLTALE_PC\bin\Shipping\GameApp.pdb`
- **Sections**:
  - `.text` (Code): VirtualSize `0xbfa08a`, RawSize `0xbfa200`
  - `.rdata` (Read-only data, RTTI, strings): VirtualSize `0x247e62`, RawSize `0x248000`
  - `.data` (Globals/Static data): VirtualSize `0x2c640`, RawSize `0x14600`
  - `.pdata` (x64 Exception unwinding tables): VirtualSize `0x7b588`, RawSize `0x7b600`
  - `.gfids` (Control Flow Guard function identifiers): VirtualSize `0x23c`, RawSize `0x400`
  - `.tls` (Thread Local Storage): VirtualSize `0x38`, RawSize `0x200`
  - `_RDATA` (Additional read-only data): VirtualSize `0x180`, RawSize `0x200`
  - `.rsrc` (Resources: icons, version info): VirtualSize `0xd17c8`, RawSize `0xd1800`
  - `.reloc` (Base relocations): VirtualSize `0x2ea84`, RawSize `0x2ec00`

---

## 2. Dynamic Link Libraries (DLLs)

| DLL Name | Size (Bytes) | Role & Integration |
| :--- | :--- | :--- |
| `oo2core_5_win64.dll` | 913,408 | RAD Game Tools Oodle Data Compression (v5.x 64-bit). Used for decompressing chunked TTARCH2 game archives. |
| `fmod64.dll` | 1,777,152 | Firelight Technologies FMOD Low-Level Audio Engine (x64). |
| `fmodstudio64.dll` | 1,899,008 | Firelight Technologies FMOD Studio API Runtime (x64). |
| `Galaxy64.dll` | 5,757,952 | GOG Galaxy Client SDK (x64) for achievements and cloud integration. |
| `TTMediaEngine64.dll` | 16,896 | Telltale Games Media Engine (x64 video playback wrapper). |
| `dinput8.dll` | 4,608 | DirectInput wrapper / gamepad helper. |

---

## 3. Resource Archives (`Archives/*.ttarch2`)
There are **223 `.ttarch2` archives** located in the `Archives/` folder.
These archives package all game assets including textures, models (`.txmesh`), scene descriptions, sounds, dialogues, and choreographies.

### Breakdown of Archive Sets
1. **Core / Boot Archives**:
   - `MC2_pc_Boot_data.ttarch2`
   - `MC2_pc_PC_P2_Boot_data.ttarch2`
   - `MC2_pc_PC_P2_Menu_compressed.ttarch2`
   - `MC2_pc_UI_txmesh.ttarch2`
   - `MC2_pc_Project_data.ttarch2`

2. **Per-Episode Content Archives**:
   - Episode 201: `MC2_pc_Minecraft201_*.ttarch2` (e.g., `_data`, `_txmesh`, `_voice`)
   - Episode 202: `MC2_pc_Minecraft202_*.ttarch2`
   - Episode 203: `MC2_pc_Minecraft203_*.ttarch2`
   - Episode 204: `MC2_pc_Minecraft204_*.ttarch2`
   - Episode 205: `MC2_pc_Minecraft205_*.ttarch2`

3. **Localized Content Archives**:
   - Subtitles, UI text, and regional choreographies for Chinese (`Ch`/`TC`), Arabic (`Ar`), French (`Fr`), German (`De`), Spanish (`Es`), Italian (`It`), Russian (`Ru`), and Portuguese (`Pt`).

---

## 4. Lua Resource Descriptors (`Archives/_resdesc_*.lua`)
There are **198 `.lua` descriptor scripts** in `Archives/`.
These Lua files mount archives into the virtual filesystem (`logical:<...>/...`) and specify load ordering and versioning.

### Build Version Descriptors (`_rescdesc_50_version_*.lua`)
The unencrypted descriptors confirm the exact build dates and RC tags for each episode:
- **Episode 201**: `2017.06.29 14:59 201 79-RC`
- **Episode 202**: `2017.08.10 01:33 202 52-RC`
- **Episode 203**: `2017.09.12 19:09 203 49-RC`
- **Episode 204**: `2017.10.24 13:29 204 62-RC`
- **Episode 205**: `2017.12.08 15:14 205 58-RC`

---

## 5. Configuration, Manifests & Miscellaneous
- `CrowdPlay.install.xml`: Crowd Play service installation configuration.
- `CrowdPlayLAN\host-settings.xml`: Network server settings for local voting sessions.
- `goggame-1614341910.info`: GOG application configuration, game IDs, and executable launch targets.
- `goglog.ini`: GOG Galaxy launcher logging configuration.
- `webcache.zip`: Embedded web assets for Crowd Play local web interface.
