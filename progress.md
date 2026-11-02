# Reverse Engineering Progress

## Function Statistics
- **Total Functions**: 58,581 (from x64 `.pdata` exception table)
- **Analyzed Functions**: 16 (fully traced disassembly and argument register flows)
- **Renamed Functions**: 16 (verified against binary evidence, strings, and RTTI)
- **Remaining Functions**: 58,565
- **Classes Recovered**: 5 core classes with verified VTables (`ResourceLocation_TTArchive`, `DataStream_Container`, `TTAllocator`, `LinearHeap`, `Scene`) + 3,598 RTTI classes cataloged
- **Subsystems Mapped**: 5 major subsystems (TTARCH2 Container, TTA4 Inner Index, Blowfish Cryptography, Oodle/Zlib Compression, Lua Script API Bridge & Decryption)
- **Completion**: 0.0273%

$$\text{Completion} = \frac{\text{renamed} + \text{confirmed analyzed}}{\text{total functions}} \times 100 = \frac{16}{58,581} \times 100 \approx 0.0273\%$$

---

## Phase Status Summary

| Phase | Description | Status | Deliverables / Artifacts |
| :--- | :--- | :--- | :--- |
| **Phase 1** | File Discovery & Asset Inventory | **COMPLETED** | `project/findings/files.md` (453 files inventoried) |
| **Phase 2** | Telltale Engine Identification | **COMPLETED** | `project/findings/engine_version.md` (Branch `2017_03_Minecraft2`) |
| **Phase 3** | TTARCH2 Archive Pipeline | **COMPLETED** | `project/findings/ttarch_analysis.md`, `project/findings/crypto_analysis.md`, `project/findings/compression_system.md` |
| **Phase 4** | Ghidra Analysis Setup | **COMPLETED** | Ghidra project at `ghidra/MCSM2` with binary imported |
| **Phase 5** | Function Mapping System | **ACTIVE** | `project/functions/confirmed_functions.md`, `project/functions/mapped_functions.md` |
| **Phase 6** | Key & Resource Index Recovery | **COMPLETED** | `project/findings/key_sources.md` (Master Blowfish key isolated at `0x140c3d5b0`, CRC64 ECMA-182 proven) |
| **Phase 7** | Extractor Architecture Prototype | **COMPLETED** | `extractor/` package (`ttarch2.py`, `blowfish.py`, `oodle.py`, `index.py`, `main.py`) |
| **Phase 8** | Asset Extraction & Lua Bytecode Validation | **COMPLETED** | Extraction verified on `MC2_pc_CrowdPlayLAN_Project.ttarch2`, Lua bytecode decryption mapped at `0x14015a480` |
| **Phase 9** | Progress Tracking | **ACTIVE** | `progress.md` |

---

## Extraction Test Record
- **Archive**: `MC2_pc_CrowdPlayLAN_Project.ttarch2`
  - **Type**: `NCTT` (Uncompressed / raw container)
  - **Total Resources in Index**: 4
  - **Extracted Files**: 4 (`CrowdPlay.lua`, `CrowdPlayOverlay.lua`, `DialogChoices.lua`, `UI.lua`)
  - **Failures**: 0
  - **Status**: 100% verified against index hashes and sizes
- **Archive**: `MC2_pc_UI_txmesh.ttarch2`
  - **Type**: `ECTT` (Blowfish Encrypted + Oodle LZ Compressed)
  - **Total Resources in Index**: 1,028 chunk blocks mapped
  - **Status**: Container structure parsed, chunk table mapped, Oodle decompression parameter order confirmed
