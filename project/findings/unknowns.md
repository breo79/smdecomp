# Unknowns & Open Research Questions

## 1. Archive Decryption Key
- **Item**: Master Blowfish encryption key for Season Two `.ttarch2` archives (`ECTT` / `TTCE`).
- **Status**: UNKNOWN / IN PROGRESS.
- **Evidence**:
  - Binary checks `magic == 0x54544345` and sets encryption flag `[rbx + 0x60] = 1`.
  - Standard Blowfish P-box is present at `.rdata:0x140c3c560`.
  - In earlier Telltale games, Blowfish keys were derived from string combinations (e.g., game title, build date, or specific hardcoded passphrase).
- **Next Steps**: Trace cross-references to the Blowfish initialization / `BF_set_key` equivalent function and locate key parameter in memory.

## 2. Lua Bytecode & Script Encryption
- **Item**: Format and encryption of `_resdesc_50_Boot.lua` and other compiled `.lua` scripts.
- **Status**: UNKNOWN / PARTIALLY HYPOTHESIZED.
- **Evidence**:
  - `_resdesc_50_Boot.lua` begins with non-ASCII bytes: `45 6f 76 29 97 53 ...` ("Eov)...").
  - Engine strings reference `local function ttFixupLua51Script` and `local function ttFixupLua50Script`.
  - Lua scripts in Telltale Tool post-2015 are typically compiled with modified Lua 5.1/5.2 opcodes or encrypted with Blowfish before loading.
- **Next Steps**: Locate the `luaL_loadbuffer` / `lua_load` call in `Minecraft2.exe` to see if a decryption/deserialization pass occurs prior to execution.

## 3. Save Game Format & Location
- **Item**: Save game structure and serialization format (`SaveLoadManager`).
- **Status**: UNKNOWN.
- **Evidence**: RTTI class `SaveLoadManager` present (`C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\SaveLoadManager.cpp`).
- **Next Steps**: Locate `SaveLoadManager` methods in binary, inspect serialization of `PropertySet` objects to disk.

## 4. Enlighten Radiosity Data Files
- **Item**: Storage layout of precomputed radiosity / probe volumes.
- **Status**: UNKNOWN.
- **Evidence**: Source references `RenderEnlighten.cpp` and `EnlightenUtils.inl`. RTTI classes `MeshSceneEnlightenData`, `LightmapPage@T3LightSceneInternalData`, `EnlightenAdaptiveProbeVolumeSettings`.
- **Next Steps**: Identify resource extension for Enlighten lighting packages inside the archives.
