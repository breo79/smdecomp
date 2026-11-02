# Confirmed Functions Catalog

This catalog contains only 100% verified functions where the name, exact virtual address, calling convention, and behavior have been proven by binary evidence, strings, RTTI, or exported symbol links. No guessed functions are included.

---

## 1. Archive & Stream Pipeline

### `TTArchive2_Load`
- **Address**: `0x14016b520`
- **Prototype**: `bool __fastcall TTArchive2_Load(TTArchive2* this, void* stream, uint64_t* out_final_offset, ...)`
- **Calling Convention**: `__fastcall` (MSVC x64)
- **Evidence**: Magic constants `0x5454434e` (`TTCN`), `0x54544345` (`TTCE`), `0x5454435a` (`TTCZ`), `0x54544365` (`TTCe`), `0x5454437a` (`TTCz`).
- **Behavior**: Parses outer archive header. For `NCTT`, reads 8-byte payload size and passes inner payload to index loader. For `ECTT`/`ZCTT`, allocates chunk offset array of `(chunk_count + 1)` 64-bit offsets and flags encryption.

### `TTArchive2_IsEncrypted`
- **Address**: `0x14016ba80`
- **Prototype**: `bool __fastcall TTArchive2_IsEncrypted(DataStream* stream)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Dynamic cast to `DataStream_Container` (`0x141050ed0`), retrieves `TTArchive2*` at `+0x30`, reads boolean byte at `+0x60`.

### `TTArchive2_InitializeIndex`
- **Address**: `0x14016c4e0`
- **Prototype**: `void __fastcall TTArchive2_InitializeIndex(TTArchive2* this, void* stream_reader, ...)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Uses `DCArray<uint64_t>` (`.?AV?$DCArray@_K@@`), parses `TTA4` index table entries (`<QQQHH`), string table (65536 bytes), and data section.

---

## 2. Cryptographic Subsystem (Blowfish)

### `Blowfish_InitDefaultMasterKey`
- **Address**: `0x1401073f0`
- **Prototype**: `void __fastcall Blowfish_InitDefaultMasterKey(void)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Direct `lea rdx, [rip + 0xb361b0]` loading the 55-byte master key at `.rdata:0x140c3d5b0`, passes to `Blowfish_GetDefaultContext` (`0x140107470`), tails into `BF_set_key` (`0x1401088b0`).

### `Blowfish_GetDefaultContext`
- **Address**: `0x140107470`
- **Prototype**: `Blowfish_Context* __fastcall Blowfish_GetDefaultContext(void)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Checks global singleton pointer `0x1410d1578`. If null, allocates `0x1050` bytes and initializes refcount.

### `Blowfish_InitContext`
- **Address**: `0x140107560`
- **Prototype**: `Blowfish_Context* __fastcall Blowfish_InitContext(Blowfish_Context* ctx, const char* key_str)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Clears context status flags; delegates to `BF_set_key` (`0x1401088b0`).

### `Blowfish_ProcessBlocks`
- **Address**: `0x140107590`
- **Prototype**: `void __fastcall Blowfish_ProcessBlocks(Blowfish_Context* ctx, uint8_t* data, size_t len)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Validates 8-byte block alignment (`test r8b, 7`), executes 16-round Feistel decryption on each 64-bit block in-place.

### `BF_set_key`
- **Address**: `0x1401088b0`
- **Prototype**: `void __fastcall BF_set_key(Blowfish_Context* ctx, int key_len, const uint8_t* key_data)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Copies standard Blowfish P-box (18 words) and S-boxes (1024 words) from `.rdata:0x140c3c560`. Performs key expansion loop and subkey generation.

---

## 3. Lua Scripting Interface & Decryption

### `luaResource_LoadWithEncryptionKey`
- **Address**: `0x1404cda20`
- **Prototype**: `int __fastcall luaResource_LoadWithEncryptionKey(lua_State* L)`
- **Calling Convention**: `__cdecl` / `__fastcall` (Lua C function)
- **Evidence**: Registered as `"LoadWithEncryptionKey"` at `0x1400213b7`. Extracts argument 2 via `lua_tolstring`. Calls `0x140107560` or defaults to `0x140107470`.

### `luaScript_ExecuteBoot`
- **Address**: `0x140150a30`
- **Prototype**: `void __fastcall luaScript_ExecuteBoot(const char* script_name, ...)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Invoked by engine entry during `GameEngine::Init` with `_boot.lua` (`0x140c1a9a0`). Jumps to `0x14004d580` passing global Lua state `0x1410b5d58`.

### `luaScript_DecryptBytecode`
- **Address**: `0x14015a480`
- **Prototype**: `bool __fastcall luaScript_DecryptBytecode(uint8_t* buffer, size_t length)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Checks encrypted header magic `\x1bLEo` (`0x6f454c1b`) / `\x1bLEn`, decrypts payload using Blowfish, and rewrites header to `\x1bLua` (`0x61754c1b`).

---

## 4. Decompression Subsystem

### `StreamDecoder_DecompressBlock`
- **Address**: `0x140425ab0`
- **Prototype**: `int __fastcall StreamDecoder_DecompressBlock(StreamDecoder* this)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Checks encryption flag (`[rbx + 0x60]`); calls `Blowfish_ProcessBlocks` at `0x140425e08`. Evaluates compression scheme `[rbx + 0x78]`: `0` -> Zlib (`0x1408f6cb0`), `1` -> Oodle (`0x1408f6d40`).

### `Oodle_DecompressChunkWrapper`
- **Address**: `0x1408f6d40`
- **Prototype**: `bool __fastcall Oodle_DecompressChunkWrapper(void* compBuf, size_t compBufSize, void* rawBuf, size_t rawLen)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Calls `OodleLZ_Decompress` exported by `oo2core_5_win64.dll`.

### `Zlib_DecompressChunkWrapper`
- **Address**: `0x1408f6cb0`
- **Prototype**: `bool __fastcall Zlib_DecompressChunkWrapper(void* compBuf, size_t compBufSize, void* rawBuf, size_t rawLen)`
- **Calling Convention**: `__fastcall`
- **Evidence**: Statically linked zlib `inflate` wrapper for legacy archives (`TTCZ`).

---

## 5. Entry Point & CRT

### `wWinMainCRTStartup`
- **Address**: `0x140b30b80`
- **Prototype**: `int __fastcall wWinMainCRTStartup(void)`
- **Evidence**: PE Optional Header AddressOfEntryPoint: `0x00b30b80`.
