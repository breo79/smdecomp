# Technical Roadmap & Milestones

This document tracks the current completion status and upcoming engineering goals for the Minecraft: Story Mode - Season Two reverse engineering project.

---

## 1. Completed Milestones

### Archive & Resource Subsystems
- [x] **TTARCH2 Container Analysis**: Fully mapped outer archive layouts across `ECTT` (encrypted + Oodle), `ZCTT` (legacy Zlib), `NCTT` (uncompressed raw container), `TTCe` (alternate encrypted), and `TTCz` (alternate compressed).
- [x] **Header & Chunk Table Parsing**: Documented chunk size, chunk count, and 64-bit chunk offset tables where `chunk_offsets[N] == file_size`.
- [x] **TTA4 Inner Index Reconstruction**: Solved the inner archive index structure (12-byte header, 28-byte `<QQQHH` entry records, and 65,536-byte string table block).
- [x] **Symbol CRC64 Name Hashing**: Verified standard CRC-64-ECMA-182 (`0x42F0E1EBA9EA3693`) for lowercased ASCII filenames with $O(\log N)$ sorted index lookups.
- [x] **Modular Extractor Architecture**: Built the [`extractor/`](file:///C:/Users/cxh/Projects/MCSM/extractor) package supporting format validation, resource listing, and file unpacking.
- [x] **Resource Extraction Validation**: Successfully extracted 100% of resources from raw archives (`MC2_pc_CrowdPlayLAN_Project.ttarch2`) matching index hashes and sizes.

### Cryptography & Decompression
- [x] **Master Key Recovery**: Isolated the 55-byte static master Blowfish key stored in `.rdata:0x140c3d5b0` loaded by `0x1401073f0` (`Blowfish_InitDefaultMasterKey`).
- [x] **Feistel Subsystem Separation**: Differentiated in-engine Blowfish Feistel routines:
  - `0x140107590`: `Blowfish_ProcessBlocks_Encrypt` ($P[0] \to P[17]$)
  - `0x140107a10`: `Blowfish_ProcessBlocks_Decrypt` ($P[17] \to P[0]$)
- [x] **Cipher Block Alignment Behavior**: Documented `len & ~7` block masking at `0x140425df3`, leaving trailing `len & 7` bytes unencrypted.
- [x] **Oodle LZ Integration**: Bound `oo2core_5_win64.dll` exports (`OodleLZ_Decompress`, `OodleLZ_GetChunkCompressor`) and mapped register parameter ordering (`rawBuf`, `rawLen`, `compBuf`, `compBufSize`).
- [x] **Lua Bytecode Encryption Pipeline**: Traced in-memory script transformation at `0x14015a480` (`luaScript_DecryptBytecode`), which decrypts `\x1bLEo` / `\x1bLEn` buffers and restores standard `\x1bLua` (`0x61754c1b`) headers for execution.

---

## 2. Planned & In-Progress Milestones

### Phase 2: Tooling & Script Decompilation
- [ ] **Standalone Lua Decryptor**: Implement CLI tool to batch-convert extracted `\x1bLEo` scripts into standard Lua 5.2 bytecode ready for standard decompilers (e.g. `unluac`).
- [ ] **Full Archive Decryption/Decompression**: Finalize end-to-end multi-chunk decoding across all 183 encrypted `ECTT` archives.
- [ ] **Mass Asset Extraction**: Verify batch extraction across all 5 episodes (Episodes 201–205).

### Phase 3: Serialization & Data Formats
- [ ] **PropertySet (`.prop`) Serialization**: Reverse engineer the binary serialization format for engine property bags, symbol mappings, and meta-types.
- [ ] **Resource Type Identification**: Document format specifications for key asset types:
  - `.d3dtx`: Direct3D 11 texture format headers and mipmap layouts.
  - `.d3dmesh`: Vertex/index buffer layout, skeletal weighting, and mesh sub-chunks.
  - `.anm`: Skeletal animation tracks and quaternions.
  - `.chore`: Choreography and timeline event data.
  - `.font`: Font glyph metric structures.

### Phase 4: Runtime Engine Systems
- [ ] **Virtual File System (VFS)**: Document `ResourceLocation`, `ResourceArchive`, and archive search priority hierarchy.
- [ ] **Scene & Entity Component System**: Map the `Scene`, `Entity`, and `PropertySet` class hierarchies and component dispatch tables.
- [ ] **Memory Allocator Tracking**: Map custom linear heaps (`LinearHeap`), pool allocators, and `TTAllocator` alignment behavior.

### Phase 5: Cross-Game Engine Comparison
- [ ] **Engine Generation Comparison**: Compare Minecraft: Story Mode Season 2 (Telltale Tool 2017 Gen 5 Enlighten/D3D11) against prior generations (*The Walking Dead*, *Tales from the Borderlands*, *MCSM Season 1*) and contemporary titles (*Batman: The Telltale Series*, *Guardians of the Galaxy*).
