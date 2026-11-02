# Reverse Engineering Progress

## Function Statistics
- **Total Functions**: 58,581 (from x64 `.pdata` exception table)
- **Analyzed Functions**: 15 (fully traced disassembly and argument register flows)
- **Renamed Functions**: 15 (verified against binary evidence, strings, and RTTI)
- **Remaining Functions**: 58,566
- **Classes Recovered**: 5 core classes with verified VTables (`ResourceLocation_TTArchive`, `DataStream_Container`, `TTAllocator`, `LinearHeap`, `Scene`) + 3,598 RTTI classes cataloged
- **Subsystems Mapped**: 5 major subsystems (TTARCH2 Container, TTA4 Inner Index, Blowfish Cryptography, Oodle/Zlib Compression, Lua Script API Bridge)
- **Completion**: 0.0256%

$$\text{Completion} = \frac{\text{renamed} + \text{confirmed analyzed}}{\text{total functions}} \times 100 = \frac{15}{58,581} \times 100 \approx 0.0256\%$$

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
| **Phase 8** | Progress Tracking | **ACTIVE** | `progress.md` |
| **Phase 9** | Code Generation Rules | **PENDING** | Clean-room reconstruction strictly paused until engine mapping reaches full depth |

---

## Roadmap Milestones
- **0% – 25%**: Basic engine discovery & container mapping (**Current Phase — TTARCH2 & TTA4 pipeline solved, Extractor Milestone 1 verified**)
- **25% – 50%**: Core systems mapped (Memory manager, PropertySet, Virtual File System, Stream decoders)
- **50% – 75%**: Gameplay systems mapped (Scene, Actor, Dialogue, Lua VM)
- **75% – 90%**: Full engine behavior understood (D3D11 render pipeline, Enlighten GI, LipSync2)
- **90% – 100%**: Clean-room C++ reconstruction possible
