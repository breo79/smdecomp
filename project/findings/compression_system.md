# Telltale Tool Compression Subsystem Analysis

## Overview
Minecraft: Story Mode Season 2 utilizes a dual-engine compression architecture within its stream decoding pipeline (`StreamDecoder`). While previous engine generations relied solely on Deflate/Zlib, the 2017 generation introduces **RAD Game Tools Oodle LZ** as the default high-performance decompressor, while retaining legacy Zlib decoding for backwards compatibility.

---

## 1. Compression Dispatcher (`StreamDecoder_DecompressBlock` - `0x140425ab0`)

The primary dispatcher function is located at virtual address `0x140425ab0`.

### Compression Scheme Enum (`[rbx + 0x78]`):
The engine evaluates the 32-bit integer at offset `+0x78` in the `StreamDecoder` structure:

| Enum Value | Compression Method | Handler Function | Library Source |
| :---: | :--- | :--- | :--- |
| `0` | **ZLIB / Deflate** | `0x1408f6cb0` (`Zlib_DecompressBlockWrapper`) | In-engine static Zlib |
| `1` | **Oodle LZ** | `0x1408f6d40` (`Oodle_DecompressChunkWrapper`) | `oo2core_5_win64.dll` |

### Assembly Trace (`0x140425ba6`):
```assembly
0x140425ba6: mov  ecx, dword ptr [rbx + 0x78]  ; Load compression scheme enum
0x140425ba9: xor  dl, dl
0x140425bab: mov  r8, qword ptr [rbx + 0xa8]   ; Output raw buffer
0x140425bb2: test ecx, ecx                     ; Check if scheme == 0 (ZLIB)
0x140425bb4: je   0x140425bcb                  ; Route to ZLIB
0x140425bb6: cmp  ecx, 1                       ; Check if scheme == 1 (Oodle)
0x140425bb9: jne  0x140425bdc
0x140425bbb: mov  edx, dword ptr [r14]         ; Compressed buffer size
0x140425bbe: mov  r9d, r15d                    ; Expected uncompressed length
0x140425bc1: mov  rcx, rdi                     ; Compressed data pointer
0x140425bc4: call 0x1408f6d40                  ; Call Oodle decompressor
0x140425bc9: jmp  0x140425bd9
0x140425bcb: mov  r9d, r15d                    ; Parameters for ZLIB
0x140425bce: mov  rdx, r14
0x140425bd1: mov  rcx, rdi
0x140425bd4: call 0x1408f6cb0                  ; Call ZLIB decompressor
```

---

## 2. Oodle Decompression Wrapper (`0x1408f6d40`)

The wrapper routine bridges the engine's memory buffers to the external `oo2core_5_win64.dll` C-API.

### Function Signature:
```cpp
bool Oodle_DecompressChunkWrapper(
    const void* compBuf,       // RCX: Pointer to compressed block data
    size_t      compBufSize,   // RDX: Byte size of compressed block
    void*       rawBuf,        // R8:  Pointer to destination buffer (64 KB)
    size_t      rawLen         // R9:  Expected uncompressed length
);
```

### Oodle API Calls & Parameter Configuration:
Inside `0x1408f6d40`:
1. **Decoder Memory Query**:
   ```assembly
   0x1408f6da1: call [OodleLZ_GetChunkCompressor]      ; Determines compressor format
   0x1408f6dab: call [OodleLZDecoder_MemorySizeNeeded] ; Computes scratchpad size
   ```
2. **Scratchpad Allocation**:
   Allocates scratchpad memory buffer via engine linear heap allocator (`0x1400401b0`).
3. **Execution (`0x1408f6e5e: call [OodleLZ_Decompress]`)**:
   Passes exact execution parameters:
   - `fuzzSafe`: `1` (defensive bounds validation)
   - `checkCRC`: `0`
   - `verbosity`: `0`
   - `decBufBase`: `NULL`
   - `decBufSize`: `0`
   - `fpCallback`: `NULL`
   - `callbackUserData`: `NULL`
   - `threadPhase`: `3`
4. **Validation & Return Value**:
   ```assembly
   0x1408f6e64: mov rsi, rax        ; RAX = returned decompressed bytes
   ...
   0x1408f6e8c: cmp rsi, rbx        ; Compare returned size with rawLen
   0x1408f6e8f: sete bl             ; Returns true only if bytes match exactly
   ```

---

## 3. Buffer Allocation & Memory Management
- **Chunk Size Standard**: Default uncompressed chunk size across all Season 2 `.ttarch2` archives is **65,536 bytes (64 KB)** (`0x00010000`).
- **Decoder Output Buffer**: Reused across consecutive chunk reads to minimize heap fragmentation.
- **Error Recovery**: If decompression fails (`OodleLZ_Decompress` returns fewer bytes than expected), the engine sets error status at `[rdi + 0x10]` and aborts stream loading.
