# Renamed Functions Database

| Old Name | New Name | Address | Evidence | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| `FUN_14016b520` | `TTArchive2_Load` | `0x14016b520` | Checks container magic (`ECTT`, `ZCTT`, `NCTT`), parses chunk table, sets `is_encrypted` flag. | 95% (Confirmed) |
| `FUN_14016ba80` | `TTArchive2_IsEncrypted` | `0x14016ba80` | Dynamic-casts `DataStream` to `DataStream_Container`, queries `TTArchive2*` at `+0x30`, returns `[rax + 0x60]`. | 100% (Confirmed) |
| `FUN_14016c4e0` | `TTArchive2_InitializeIndex` | `0x14016c4e0` | Instantiates `DCArray<uint64_t>` (`.?AV?$DCArray@_K@@`) for 64-bit resource symbol hashes. | 90% (Confirmed) |
| `FUN_1401088b0` | `BF_set_key` | `0x1401088b0` | Copies S-boxes and P-array from `.rdata:0x140c3c560`, XORs key bytes, expands subkeys via cipher rounds. | 100% (Confirmed) |
| `FUN_140107560` | `Blowfish_InitContext` | `0x140107560` | Zeroes initialization flags and executes `BF_set_key` with input key buffer. | 100% (Confirmed) |
| `FUN_140107590` | `Blowfish_ProcessBlocks` | `0x140107590` | Enforces 8-byte block alignment (`test r8b, 7`), loops over 64-bit blocks executing 16 Feistel rounds. | 100% (Confirmed) |
| `FUN_1404cda20` | `luaResource_LoadWithEncryptionKey` | `0x1404cda20` | Registered as `"LoadWithEncryptionKey"` at `0x1400213b7`. Extracts key from Lua stack and allocates `0x1050` context. | 100% (Confirmed) |
| `FUN_1408f6d40` | `Oodle_DecompressChunkWrapper` | `0x1408f6d40` | Invokes `OodleLZ_Decompress` (`oo2core_5_win64.dll`) with `fuzzSafe=1`, `threadPhase=3`. | 98% (Confirmed) |
| `FUN_140425ab0` | `StreamDecoder_DecompressBlock` | `0x140425ab0` | Decrypts encrypted block via `Blowfish_ProcessBlocks` at `0x140425e08`, evaluates compression enum (`0`=Zlib, `1`=Oodle). | 95% (Confirmed) |
| `FUN_1408f6cb0` | `Zlib_DecompressBlockWrapper` | `0x1408f6cb0` | Companion decompression function called for compression type 0 in `StreamDecoder_DecompressBlock`. | 85% (Strong guess) |
| `FUN_140b30b80` | `wWinMainCRTStartup` | `0x140b30b80` | PE Entry point at RVA `0xb30b80` pointing to MSVC C runtime startup routine. | 100% (Confirmed) |
| `FUN_140515540` | `Stream_Read` | `0x140515540` | General stream read primitive invoked across archive loading functions. | 92% (Confirmed) |
| `FUN_140515660` | `Stream_HandleReadError` | `0x140515660` | Error trap invoked whenever `Stream_Read` fails to return the exact expected number of bytes. | 88% (Strong guess) |
