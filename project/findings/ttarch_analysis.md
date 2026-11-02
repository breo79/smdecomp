# TTARCH2 & TTA4 Container Specification

## Confidence Levels
- **Confirmed**: Directly proven by binary analysis, disassembly, and runtime validation.
- **Likely**: Strong structural and contextual evidence matching known engine behaviors.
- **Unknown**: Requires further runtime memory tracing or key isolation.

---

## 1. Outer Container Formats (`TTARCH2`)

The game uses several container encapsulations depending on compression and encryption:

### A. Compressed / Encrypted Containers (`ECTT`, `ZCTT`, `TTCe`, `TTCz`)

**Confidence: Confirmed** (Validated at `0x14016b520` `TTArchive2_Load`)

```cpp
#pragma pack(push, 1)
struct TTArchive2_Header {
    uint32_t magic;           // 0x00: 0x54544345 ("ECTT"), 0x5454435A ("ZCTT"), etc.
    uint32_t chunk_size;      // 0x04: Uncompressed block size (typically 0x10000 = 65,536 bytes)
    uint32_t chunk_count;     // 0x08: Number of chunks N in archive
    uint64_t chunk_offsets[1];// 0x0C: Array of (N + 1) uint64_t file offsets
};
#pragma pack(pop)
```

- `chunk_offsets[0]`: Offset of first compressed chunk (`12 + (N + 1) * 8`).
- `chunk_offsets[i]`: Byte offset where chunk $i$ begins.
- `chunk_offsets[i+1] - chunk_offsets[i]`: Byte length of chunk $i$.
- `chunk_offsets[N]`: Matches total file size.
- Chunks in `ECTT` are Blowfish encrypted in 8-byte blocks, then decompressed via Oodle LZ (`oo2core_5_win64.dll`).

### B. Uncompressed Raw Containers (`NCTT`)

**Confidence: Confirmed** (Validated at `0x14016b5a3` in `TTArchive2_Load`)

```cpp
#pragma pack(push, 1)
struct TTArchive2_NCTT_Header {
    uint32_t magic;           // 0x00: 0x5454434E ("NCTT")
    uint64_t payload_size;    // 0x04: Total size of inner uncompressed payload (file_size - 12)
    // Payload starts immediately at offset 0x0C
};
#pragma pack(pop)
```

- `NCTT` archives contain NO chunk table and NO compression/encryption.
- The inner payload starts directly at offset `0x0C` (12) with the `TTA4` inner archive header.

---

## 2. Inner Archive Format (`TTA4`)

**Confidence: Confirmed** (Validated on multiple game archives and disassembly of `TTArchive2_InitializeIndex` `0x14016c4e0`)

When an `ECTT` or `ZCTT` archive's chunks are fully decompressed, or directly in an `NCTT` archive, the payload forms a `TTA4` archive stream.

### A. Header Layout (12 bytes)
```cpp
#pragma pack(push, 1)
struct TTArchive4_Header {
    uint32_t magic;             // 0x00: 0x34415454 ("4ATT" / TTA4)
    uint32_t string_table_size; // 0x04: Size of string table in bytes (typically 65,536 / 0x10000)
    uint32_t entry_count;       // 0x08: Number of resource entries in the index table
};
#pragma pack(pop)
```

### B. Entry Record Layout (28 bytes per entry)
Immediately following `TTArchive4_Header` at offset `0x0C` (relative to the inner payload) is an array of `entry_count` records:

```cpp
#pragma pack(push, 1)
struct TTArchive4_Entry {
    uint64_t symbol_hash;       // 0x00: 64-bit CRC hash of lowercased filename
    uint64_t data_offset;       // 0x08: Byte offset relative to Data Section base
    uint64_t data_size;         // 0x10: Uncompressed file size in bytes
    uint16_t flags;             // 0x18: Flags / attributes
    uint16_t name_offset;       // 0x1A: Byte offset within String Table
}; // Total size: 28 bytes (0x1C)
#pragma pack(pop)
```

### C. String Table & Data Section Layout
- **Index Table Extent**: `sizeof(TTArchive4_Header) + (entry_count * 28)` = `12 + (entry_count * 28)` bytes.
- **String Table Base**: Follows the index table immediately.
- **Data Section Base**: `12 + (entry_count * 28) + string_table_size`.
- **Resource Placement**: The data for entry $i$ is located at:
  $$\text{Resource Offset} = \text{Data Section Base} + \text{entry}[i].\text{data\_offset}$$
  $$\text{Resource Length} = \text{entry}[i].\text{data\_size}$$

---

## 3. Resource Hashing Algorithm (Symbol CRC64)

**Confidence: Confirmed** (Verified across 100% of tested archive entries)

File names are hashed into 64-bit symbols using standard **CRC-64-ECMA** (ECMA-182).

- **Polynomial**: `0x42F0E1EBA9EA3693`
- **Initial Value**: `0x0000000000000000`
- **Direction**: MSB-first (`crc ^= (byte << 56)`)
- **Pre-processing**: Filenames are converted to lowercase ASCII before hashing.
- **Sorting**: Index entries are strictly sorted in ascending order of `symbol_hash` to enable $O(\log N)$ binary searching.

### Python Reference:
```python
def crc64_telltale(name: str) -> int:
    poly = 0x42F0E1EBA9EA3693
    crc = 0
    for b in name.lower().encode('ascii'):
        crc ^= (b << 56)
        for _ in range(8):
            if crc & 0x8000000000000000:
                crc = ((crc << 1) ^ poly) & 0xFFFFFFFFFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFFFFFFFFFF
    return crc
```
