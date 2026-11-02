# Hypothesis Log

## Hypothesis 001
- **Date**: 2026-11-01
- **Function / Target**: `0x14016b520`
- **Guess**: `TTArchive2::Load` / `TTArchive2::Open`
- **Evidence**:
  - Validates archive magic numbers (`TTCN`, `TTCE`, `TTCZ`, `TTCe`, `TTCz`).
  - Reads chunk size (uint32) and chunk count (uint32).
  - Allocates 0xC0 bytes for archive context and reads array of 64-bit chunk offsets.
- **Confidence**: 95%
- **Status**: Confirmed

---

## Hypothesis 002
- **Date**: 2026-11-01
- **Function / Target**: `0x1408f6d40`
- **Guess**: `Oodle_DecompressChunkWrapper`
- **Evidence**:
  - Direct caller of `OodleLZ_Decompress` (`oo2core_5_win64.dll`).
  - Sets up Oodle decoding parameters (`threadPhase = 3`, `fuzzSafe = 1`, `checkCRC = 0`).
  - Returns boolean success flag comparing decompressed byte count to expected uncompressed size.
- **Confidence**: 98%
- **Status**: Confirmed

---

## Hypothesis 003
- **Date**: 2026-11-01
- **Function / Target**: `0x140425ab0`
- **Guess**: `StreamDecoder::DecompressBlock`
- **Evidence**:
  - Decrypts encrypted block via `Blowfish_ProcessBlocks` at `0x140425e08`.
  - Inspects `[rbx + 0x78]` as compression type enum:
    - If `0`: calls `0x1408f6cb0` (Zlib decompress)
    - If `1`: calls `0x1408f6d40` (Oodle decompress)
- **Confidence**: 95%
- **Status**: Confirmed

---

## Hypothesis 004
- **Date**: 2026-11-01
- **Function / Target**: `0x14016c4e0`
- **Guess**: `TTArchive2::InitializeIndex`
- **Evidence**:
  - Called directly from `TTArchive2::Load` at `0x14016b622` and `0x14016b757`.
  - Instantiates `DCArray<uint64_t>` (RTTI vtable at `0x140c4bfa8`) to hold 64-bit resource symbol hashes.
- **Confidence**: 90%
- **Status**: Confirmed

---

## Hypothesis 005
- **Date**: 2026-11-01
- **Function / Target**: `0x140c3c560`
- **Guess**: Standard Blowfish P-Box S-Box Constant Table
- **Evidence**:
  - Exact hex match with fractional digits of $\pi$ used by Bruce Schneier's Blowfish cipher:
    `0x243F6A88`, `0x85A308D3`, `0x13198A2E`, `0x03707344`.
- **Confidence**: 100%
- **Status**: Confirmed

---

## Hypothesis 006
- **Date**: 2026-11-01
- **Function / Target**: `0x1401088b0`
- **Guess**: `BF_set_key`
- **Evidence**:
  - Copies initial P-box and S-boxes from `.rdata:0x140c3c560`.
  - XORs key bytes into P-array and expands subkeys across 18 P-array and 1024 S-box entries.
- **Confidence**: 100%
- **Status**: Confirmed

---

## Hypothesis 007
- **Date**: 2026-11-01
- **Function / Target**: `0x140107560`
- **Guess**: `Blowfish_InitContext`
- **Evidence**:
  - Clears context status flags and invokes `BF_set_key` with key buffer.
- **Confidence**: 100%
- **Status**: Confirmed

---

## Hypothesis 008
- **Date**: 2026-11-01
- **Function / Target**: `0x140107590`
- **Guess**: `Blowfish_ProcessBlocks`
- **Evidence**:
  - Validates 8-byte block alignment (`test r8b, 7`).
  - Executes 16-round Feistel decryption on 64-bit blocks in-place.
- **Confidence**: 100%
- **Status**: Confirmed

---

## Hypothesis 009
- **Date**: 2026-11-01
- **Function / Target**: `0x1404cda20`
- **Guess**: `luaResource_LoadWithEncryptionKey`
- **Evidence**:
  - Registered as `"LoadWithEncryptionKey"` at `0x1400213b7`.
  - Retrieves encryption key string from Lua stack argument 2 (`lua_tostring`) and allocates `0x1050` bytes context.
- **Confidence**: 100%
- **Status**: Confirmed
