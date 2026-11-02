# Minecraft: Story Mode - Season Two — Reverse Engineering Project

A technical research and preservation project focused on understanding, documenting, and reconstructing the architecture of **Minecraft: Story Mode — Season Two** (DRM-free GOG release) and the late-generation **Telltale Tool (2017 Gen 5)** engine.

The primary objective is to document how Telltale's proprietary technology functions internally:
- Resource container formats (`.ttarch2`) and inner archive layouts (`TTA4`)
- Dual-engine compression pipelines (RAD Game Tools Oodle LZ + legacy Zlib)
- Cryptographic subsystems (Blowfish 64-bit block cipher and master key loading)
- In-memory Lua bytecode obfuscation (`\x1bLEo` / `\x1bLEn` transformation)
- Runtime object model, RTTI class hierarchies, and virtual tables
- Asset serialization formats (`.prop`, `.d3dtx`, `.d3dmesh`)

> [!NOTE]
> This repository contains reverse engineering specifications, technical findings, Ghidra analysis databases, and clean-room extraction tooling. It does **not** host or redistribute proprietary game assets.

---

## Technical Architecture

```
               [TTARCH2 Archive File]
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
   [NCTT / Raw]                  [ECTT / Chunked]
 (Uncompressed/None)         (Blowfish Encrypted + Oodle LZ)
         │                               │
         │                   ┌───────────┴───────────┐
         │                   ▼                       ▼
         │            [Blowfish Decrypt]     [Oodle Decompress]
         │            (len & ~7 blocks)     (oo2core_5_win64.dll)
         │                   │                       │
         └───────────────┬───┴───────────────────────┘
                         ▼
             [TTA4 Virtual Archive Stream]
   (Header: 12 bytes | Entries: 28 bytes | String Table: 64 KB)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
[CRC-64-ECMA Hash]  [Offset Table]  [Filenames]
(0x42F0E1EBA9EA3693) (Data Section)  (ASCII Lookup)
                         │
                         ▼
               [Extracted Resources]
      (Textures, Meshes, Scripts, Audio, Props)
                         │
                         ▼ (If .lua script)
             [Lua Bytecode Decryption]
           (\x1bLEo -> \x1bLua at 0x14015a480)
```

---

## Key Confirmed Findings

### 1. TTARCH2 Container & TTA4 Archive Specification
The engine utilizes a two-tier container architecture:
- **Outer Container (`TTARCH2`)**: Encapsulates data into 64 KB chunk blocks.
  - `0x54544345` (`ECTT`): Standard Season Two format (Blowfish encrypted + Oodle compressed).
  - `0x5454435A` (`ZCTT`): Legacy format (Zlib compressed).
  - `0x5454434E` (`NCTT`): Uncompressed raw container with an 8-byte payload size header.
  - `0x54544365` (`TTCe`) / `0x5454437A` (`TTCz`): Alternate container variants.
- **Inner Format (`TTA4` / `"4ATT"`)**:
  - Header (12 bytes): Magic `0x54544134`, 32-bit string table size (typically 65,536 bytes), 32-bit resource entry count.
  - Entries (28 bytes each, `<QQQHH`): 64-bit Symbol CRC, 64-bit data section offset, 64-bit uncompressed size, 16-bit flags, and 16-bit string table offset.
  - Filename Hashing: Standard **CRC-64-ECMA-182** (polynomial `0x42F0E1EBA9EA3693`) computed on lowercased ASCII filenames.

### 2. Cryptographic Subsystem
- **Master Archive Encryption Key**: Recovered directly from executable read-only data ([`.rdata:0x140c3d5b0`](file:///C:/Users/cxh/Projects/MCSM/project/findings/key_sources.md)):
  ```hex
  8cd29b9987de94a9e69ea5947fcec1bccc9c8eddb1a7669fb28addba9cdec29ad377627faecca7d1d8e6d9d2ab64829f92cc9498d3e4a0
  ```
- **Block Alignment Behavior**: Verified at `0x140425df3` in `StreamDecoder` that Blowfish decrypts `length & ~7` bytes, leaving trailing unaligned bytes (`length & 7`) untouched.
- **Feistel Subsystem Separation**:
  - [`Blowfish_ProcessBlocks_Encrypt`](file:///C:/Users/cxh/Projects/MCSM/project/functions/confirmed_functions.md#blowfish_processblocks_encrypt) (`0x140107590`): Rounds iterate $P[0] \to P[17]$.
  - [`Blowfish_ProcessBlocks_Decrypt`](file:///C:/Users/cxh/Projects/MCSM/project/functions/confirmed_functions.md#blowfish_processblocks_decrypt) (`0x140107a10`): Rounds iterate $P[17] \to P[0]$.

### 3. Lua Script Bytecode Transformation
- Extracted `.lua` files retain in-place obfuscation with custom magic `\x1bLEo` (`0x6f454c1b`) or `\x1bLEn` (`0x6e454c1b`).
- At runtime, [`luaScript_DecryptBytecode`](file:///C:/Users/cxh/Projects/MCSM/project/functions/confirmed_functions.md#luascript_decryptbytecode) (`0x14015a480`) skips the 4-byte header, decrypts `(len - 4) & ~7` bytes via Blowfish DECRYPT, and replaces the header with standard Lua 5.2 magic `\x1bLua` (`0x61754c1b`) before passing the buffer to `lua_load`.

---

## Extractor Tooling

A modular Python extractor is included in [`extractor/`](file:///C:/Users/cxh/Projects/MCSM/extractor):

```bash
# Analyze and display archive metadata
python extractor/main.py "C:\GOG Games\Minecraft Story Mode - Season Two\Archives\MC2_pc_PC_P2_Menu_compressed.ttarch2"

# Inspect resource contents and list filenames
python extractor/main.py "C:\GOG Games\Minecraft Story Mode - Season Two\Archives\MC2_pc_CrowdPlayLAN_Project.ttarch2" --list

# Extract all resources into extracted_assets/
python extractor/main.py "C:\GOG Games\Minecraft Story Mode - Season Two\Archives\MC2_pc_CrowdPlayLAN_Project.ttarch2" --extract
```

### Module Structure
- [`extractor/ttarch2.py`](file:///C:/Users/cxh/Projects/MCSM/extractor/ttarch2.py): Container parser, chunk offset reader, and extraction pipeline.
- [`extractor/blowfish.py`](file:///C:/Users/cxh/Projects/MCSM/extractor/blowfish.py): 55-byte master key setup and block decryption.
- [`extractor/oodle.py`](file:///C:/Users/cxh/Projects/MCSM/extractor/oodle.py): Ctypes wrapper for `oo2core_5_win64.dll`.
- [`extractor/index.py`](file:///C:/Users/cxh/Projects/MCSM/extractor/index.py): `TTA4` index table parser and Symbol CRC64 hash lookup.
- [`extractor/main.py`](file:///C:/Users/cxh/Projects/MCSM/extractor/main.py): Command-line entry point.

---

## Current Progress

| Subsystem | Status | Key Deliverables |
| :--- | :--- | :--- |
| **File Discovery** | **Completed** | [`project/findings/files.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/files.md) (453 files cataloged) |
| **Engine Identification** | **Completed** | [`project/findings/engine_version.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/engine_version.md) (`2017_03_Minecraft2`) |
| **Container Pipeline** | **Completed** | [`project/findings/ttarch_analysis.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/ttarch_analysis.md) (`ECTT`, `ZCTT`, `NCTT`, `TTA4`) |
| **Cryptography Subsystem** | **Completed** | [`project/findings/key_sources.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/key_sources.md), [`project/findings/crypto_analysis.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/crypto_analysis.md) |
| **Compression System** | **Completed** | [`project/findings/compression_system.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/compression_system.md) (Oodle LZ / Zlib) |
| **Lua Bytecode Pipeline** | **Completed** | [`project/findings/lua_crypto_analysis.md`](file:///C:/Users/cxh/Projects/MCSM/project/findings/lua_crypto_analysis.md) (`\x1bLEo` $\to$ `\x1bLua`) |
| **Resource Extraction** | **Completed** | Tested 100% extraction on `MC2_pc_CrowdPlayLAN_Project.ttarch2` |
| **Function Mapping** | **Active** | [`project/functions/confirmed_functions.md`](file:///C:/Users/cxh/Projects/MCSM/project/functions/confirmed_functions.md) (16 confirmed functions) |
| **Class & RTTI Recovery** | **Active** | [`project/structures/confirmed_structures.md`](file:///C:/Users/cxh/Projects/MCSM/project/structures/confirmed_structures.md) (3,598 RTTI classes cataloged) |

Detailed roadmap and upcoming phases are tracked in [`ROADMAP.md`](file:///C:/Users/cxh/Projects/MCSM/ROADMAP.md).

---

## Verification Methodology

This project strictly follows an evidence-based reverse engineering protocol:
1. **No Hallucinations / No Guesses**: Functions are only cataloged in [`confirmed_functions.md`](file:///C:/Users/cxh/Projects/MCSM/project/functions/confirmed_functions.md) when their virtual address, prototype, and calling convention are verified by disassembly and runtime validation.
2. **Mathematical Verification**: File layouts and offset calculations are verified down to the exact byte against total file lengths (`chunk_offsets[N] == file_size`).
3. **Reproducible Test Scripts**: Findings are codified into standalone Python test scripts in [`scripts/`](file:///C:/Users/cxh/Projects/MCSM/scripts) that execute against DRM-free game files.

---

## AI-Assisted Development Disclosure

This project utilizes AI agent tooling as an assistive research mechanism for:
- Accelerating x64 assembly pattern exploration
- Drafting experimental verification scripts
- Structuring technical markdown documentation
- Indexing binary cross-references and RTTI data

All technical claims, memory addresses, algorithm polynomials, and cryptographic keys are independently verified against the disassembled `Minecraft2.exe` binary. AI suggestions never replace binary verification.

---

## Repository Structure

```
.
├── extractor/               # Production extraction package
│   ├── ttarch2.py           # Container parser & extractor
│   ├── blowfish.py          # Blowfish Feistel cipher implementation
│   ├── oodle.py             # oo2core_5_win64.dll ctypes binding
│   ├── index.py             # TTA4 index table & CRC64 symbol hashing
│   └── main.py              # CLI extraction tool
├── scripts/                 # Standalone verification & inspection scripts
├── project/
│   ├── findings/            # In-depth technical specifications
│   │   ├── ttarch_analysis.md      # Outer TTARCH2 & inner TTA4 layouts
│   │   ├── crypto_analysis.md      # Blowfish Feistel implementation analysis
│   │   ├── key_sources.md          # 55-byte master key recovery & addresses
│   │   ├── compression_system.md   # Oodle LZ & Zlib dispatcher traces
│   │   ├── lua_crypto_analysis.md  # Script bytecode transformation traces
│   │   ├── engine_version.md       # Buildbot version & compilation flags
│   │   └── files.md                # 453-file game asset inventory
│   ├── functions/           # Function address catalog & queue
│   │   ├── confirmed_functions.md  # 100% verified functions
│   │   └── mapped_functions.md     # Cross-reference analysis catalog
│   └── structures/          # Recovered class VTables & data structures
├── CONTRIBUTING.md          # Contribution guidelines & standards
├── SECURITY.md              # Security & asset prohibition policy
├── ROADMAP.md               # Technical milestones & planned phases
└── README.md                # Project documentation overview
```

---

## Disclaimer & Legal

This repository contains only documentation, clean-room reverse engineering notes, and original analysis tools. It does not contain copyrighted game binaries, proprietary textures, 3D meshes, audio, or storyline scripts.

To test the extractor or run analysis scripts, you must possess a legitimately acquired copy of *Minecraft: Story Mode - Season Two*.

This project is conducted for educational, preservation, and interoperability purposes under fair use research standards. All trademarks and registered trademarks belong to their respective owners.
