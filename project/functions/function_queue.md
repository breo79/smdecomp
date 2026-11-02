# Function Queue (Priority Analysis Backlog)

Follow the call graph priority outlined in Phase 8:

## 1. Engine Initialization & WinMain Entry
- [ ] `0x140b30b80` (`wWinMainCRTStartup` -> find target `WinMain`)
- [ ] `WinMain` -> locate `GameEngine::Init` and command line argument parsing.
- [ ] Engine configuration loading (`tool.prop`, default resolution, display mode).

## 2. Blowfish Decryption Subroutine
- [ ] Cross-reference callers of Blowfish P-box (`.rdata:0x140c3c560`).
- [ ] Find function that sets Blowfish key (`BF_set_key` equivalent).
- [ ] Isolate key buffer location and key derivation logic for `ECTT` archives.

## 3. Archive & File System Traversal
- [ ] `0x14016b8e3` (called from `TTArchive2_Load` to finish mounting).
- [ ] `0x14016ca20` (resource index reader and hash search function).
- [ ] `ResourceCreateConcreteArchiveLocation` (LUA binding / engine mount logic).
- [ ] `ResourceResolveAddressToConcreteLocationID` (URI router: `logical:<...>/...`).

## 4. Scripting & Lua Virtual Machine
- [ ] Locate `luaL_loadbuffer` / `lua_pcall` calls.
- [ ] Identify custom Telltale Lua opcodes and bytecode verification.
- [ ] Trace `GameEngine_AddBuildVersionInfo` registration.

## 5. Direct3D 11 Renderer Initialization
- [ ] Locate calls to `D3D11CreateDeviceAndSwapChain`.
- [ ] Trace `T3Texture_DX11` initialization and shader loading.
- [ ] Enlighten Radiosity SDK hookups (`RenderEnlighten.cpp`).

## 6. FMOD Studio Audio Engine
- [ ] Locate calls to `fmodstudio64.dll` (`FMOD::Studio::System::create`).
- [ ] Trace sound bank loading and sound event emitters (`SoundSystem`).
