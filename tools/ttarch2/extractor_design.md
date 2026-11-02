# TTARCH2 Extractor Architecture & Design Specification

## Overview
This document specifies the software architecture, memory model, and algorithmic flow for a clean-room extractor targeting Minecraft: Story Mode Season 2 `.ttarch2` packages (`ECTT` / `TTCE`).

---

## 1. Required Libraries & Runtime Dependencies

1. **Oodle Data Decompression Library**:
   - `oo2core_5_win64.dll` (shipped in game root).
   - Export: `OodleLZ_Decompress(const void* compBuf, size_t compBufSize, void* rawBuf, size_t rawLen, int fuzzSafe, int checkCRC, int verbosity, void* decBufBase, size_t decBufSize, void* fpCallback, void* callbackUserData, void* decoderMemory, size_t decoderMemorySize, int threadPhase)`.
2. **Blowfish 64-Bit Cipher Engine**:
   - Standard Blowfish implementation in ECB block mode.
   - 448-bit key schedule expansion matching `0x1401088b0`.
3. **CRC64 / Symbol Hash Resolver**:
   - Telltale 64-bit Symbol CRC calculation for matching filenames to hashes.

---

## 2. Core Data Structures

```cpp
#pragma pack(push, 1)

// Archive header on disk
struct ArchiveHeader {
    uint32_t magic;           // 0x54544345 ("ECTT" / TTCE)
    uint32_t chunk_size;      // 0x00010000 (65,536 bytes)
    uint32_t chunk_count;     // Total number of blocks N
};

// Virtual file table entry
struct FileEntry {
    uint64_t name_hash;       // 64-bit Symbol CRC
    uint64_t offset;          // Absolute byte offset in decompressed stream
    uint32_t size;            // Uncompressed size
    uint32_t flags;           // Resource attribute flags
};

#pragma pack(pop)
```

---

## 3. Extraction Algorithm

```mermaid
flowchart TD
    Start["Open .ttarch2 Archive"] --> ReadHdr["Read Header: magic, chunk_size, chunk_count"]
    ReadHdr --> CheckMagic{"Validate Magic"}
    CheckMagic -->|TTCE| SetEncrypted["Flag: is_encrypted = true"]
    CheckMagic -->|TTCZ| SetZlib["Flag: is_zlib = true"]
    CheckMagic -->|Other/Invalid| Abort["Abort: Unsupported Magic"]
    
    SetEncrypted --> ReadOffsets["Read (chunk_count + 1) 64-bit chunk offsets"]
    SetZlib --> ReadOffsets
    
    ReadOffsets --> LoopChunk["For each chunk i from 0 to chunk_count - 1:"]
    LoopChunk --> ReadBlock["Read slice chunk_offsets[i] .. chunk_offsets[i+1]"]
    ReadBlock --> CheckEnc{"is_encrypted?"}
    CheckEnc -->|Yes| Decrypt["Decrypt via Blowfish ECB with game key"]
    CheckEnc -->|No| Decomp["Decompress via OodleLZ_Decompress (or Zlib)"]
    Decrypt --> Decomp
    Decomp --> AppendStream["Append decompressed 64KB block to Virtual Stream"]
    AppendStream --> NextChunk{"More chunks?"}
    NextChunk -->|Yes| LoopChunk
    NextChunk -->|No| ParseIndex["Parse Virtual File Table at front of stream"]
    
    ParseIndex --> IterateEntries["For each FileEntry in Index:"]
    IterateEntries --> ExtractFile["Slice stream at FileEntry.offset for FileEntry.size"]
    ExtractFile --> SaveDisk["Write payload to output directory"]
    SaveDisk --> MoreFiles{"More files?"}
    MoreFiles -->|Yes| IterateEntries
    MoreFiles -->|No| Complete["Extraction Finished Successfully"]
```

---

## 4. Implementation Phasing
- **Phase A**: Verify Blowfish key from dynamic execution.
- **Phase B**: Build standalone parser (`parser.py` / `parser.cpp`) validating chunk extraction against `oo2core_5_win64.dll`.
- **Phase C**: Full batch extractor outputting recovered resources to `extracted_assets/`.
