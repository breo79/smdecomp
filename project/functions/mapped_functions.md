# Mapped Functions Catalog

This catalog documents key functions identified through call graph traversal, RTTI cross-referencing, and binary analysis.

## 1. Archive & Resource Subsystem (`TTArchive2` / `ResourceLocation`)

### `TTArchive2_Load` (`0x14016b520`)
- **Prototype**: `bool TTArchive2_Load(TTArchive2* this, void* stream, uint64_t* out_final_offset, ...)`
- **Key Operations**:
  - Validates container magic: `0x5454434e` (`TTCN`), `0x54544345` (`TTCE`), `0x5454435a` (`TTCZ`), `0x54544365` (`TTCe`), `0x5454437a` (`TTCz`).
  - Reads 32-bit chunk size and 32-bit chunk count.
  - Dynamically allocates `0xc0` bytes for archive structure.
  - Loops over `chunk_count + 1` entries reading 64-bit chunk offsets.
  - Flags archive as encrypted (`[rbx + 0x60] = 1`) if magic is `TTCE`.

### `TTArchive2_IsEncrypted` (`0x14016ba80`)
- **Prototype**: `bool TTArchive2_IsEncrypted(DataStream* stream)`
- **Key Operations**:
  - Performs dynamic cast from `DataStream` to `DataStream_Container` (`0x141050ed0`).
  - Retrieves `TTArchive2*` handle at offset `+0x30`.
  - Returns boolean byte flag at `+0x60`.

### `TTArchive2_InitializeIndex` (`0x14016c4e0`)
- **Prototype**: `void TTArchive2_InitializeIndex(TTArchive2* this, void* stream_reader, ...)`
- **Key Operations**:
  - Initializes index tables and hash array.
  - Uses `DCArray<uint64_t>` (`.?AV?$DCArray@_K@@`) for resource hashes.

### `luaResource_LoadWithEncryptionKey` (`0x1404cda20`)
- **Prototype**: `int luaResource_LoadWithEncryptionKey(lua_State* L)`
- **Key Operations**:
  - Registered as `"LoadWithEncryptionKey"` at `0x1400213b7`.
  - Retrieves encryption key string from Lua stack argument 2 (`lua_tostring`).
  - Allocates `0x1050` bytes for `Blowfish_Context`.
  - Calls `Blowfish_InitContext` (`0x140107560`) with key buffer.

---

## 2. Cryptographic Subsystem (`Blowfish`)

### `BF_set_key` (`0x1401088b0`)
- **Prototype**: `void BF_set_key(Blowfish_Context* ctx, int key_len, const uint8_t* key_data)`
- **Key Operations**:
  - Copies initial standard P-array (18 words) and S-boxes (1024 words) from `.rdata:0x140c3c560`.
  - XORs key bytes into P-array.
  - Iteratively encrypts all-zero block and updates subkeys across all 18 P-array and 1024 S-box entries.

### `Blowfish_InitContext` (`0x140107560`)
- **Prototype**: `Blowfish_Context* Blowfish_InitContext(Blowfish_Context* ctx, const char* key_str)`
- **Key Operations**:
  - Clears context status flags.
  - Calls `BF_set_key` (`0x1401088b0`).

### `Blowfish_ProcessBlocks` (`0x140107590`)
- **Prototype**: `void Blowfish_ProcessBlocks(Blowfish_Context* ctx, uint8_t* data, size_t len)`
- **Key Operations**:
  - Validates 8-byte block alignment (`test r8b, 7`).
  - Executes 16-round Feistel decryption on each 64-bit block in-place.

---

## 3. Decompression Subsystem (`oo2core_5_win64` / `zlib`)

### `StreamDecoder_DecompressBlock` (`0x140425ab0`)
- **Prototype**: `int StreamDecoder_DecompressBlock(StreamDecoder* this)`
- **Key Operations**:
  - Checks encryption flag; invokes `Blowfish_ProcessBlocks` at `0x140425e08` if encrypted.
  - Evaluates compression scheme from `[rbx + 0x78]`:
    - `0`: routes to Zlib decompressor (`0x1408f6cb0`)
    - `1`: routes to Oodle decompressor (`0x1408f6d40`)

### `Oodle_DecompressChunkWrapper` (`0x1408f6d40`)
- **Prototype**: `bool Oodle_DecompressChunkWrapper(void* compBuf, size_t compBufSize, void* rawBuf, size_t rawLen)`
- **Key Operations**:
  - Invokes `OodleLZDecoder_MemorySizeNeeded` and `OodleLZ_GetChunkCompressor`.
  - Calls `OodleLZ_Decompress(compBuf, compBufSize, rawBuf, rawLen, fuzzSafe=1, checkCRC=0, verbosity=0, decBufBase=NULL, decBufSize=0, fpCallback=NULL, callbackUserData=NULL, decoderMemory=mem, decoderMemorySize=memSize, threadPhase=3)`.
  - Returns `true` if decompressed size matches `rawLen`.

---

## 4. Entry & Runtime Subsystem

### `wWinMainCRTStartup` (`0x140b30b80`)
- **PE Entry Point**: VA `0x140b30b80` (RVA `0xb30b80`).
- Standard MSVC CRT initialization routine.
