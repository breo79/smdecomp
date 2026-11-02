# Confirmed Structures & Class Recovery Database

## 1. Priority Classes (RTTI & VTable Mappings)

### `ResourceLocation_TTArchive`
- **Class**: `ResourceLocation_TTArchive`
- **RTTI Name**: `.?AVResourceLocation_TTArchive@@`
- **TypeDescriptor VA**: `0x141070f70`
- **CompleteObjectLocator VA**: `0x140dfbec8`
- **Vtable VA**: `0x140cd3c20`
- **Related Classes**: `ResourceLocation`, `ResourceRegistry`, `TTArchive2`
- **Confidence**: 100% (Confirmed)

### `DataStream_Container`
- **Class**: `DataStream_Container`
- **RTTI Name**: `.?AVDataStream_Container@@`
- **TypeDescriptor VA**: `0x141050ed0`
- **CompleteObjectLocator VA**: `0x140dd07b0`
- **Vtable VA**: `0x140c4c140`
- **Related Classes**: `DataStream`, `StreamDecoder`, `TTArchive2`
- **Confidence**: 100% (Confirmed)

### `TTAllocator`
- **Class**: `TTAllocator`
- **RTTI Name**: `.?AVTTAllocator@@`
- **TypeDescriptor VA**: `0x141046410`
- **CompleteObjectLocator VA**: `0x140dc2ed4`
- **Vtable VA**: `0x140c18cd0`
- **Related Classes**: `TTAllocator_Default`, `TTAllocator_AsyncHeap`
- **Confidence**: 100% (Confirmed)

### `LinearHeap`
- **Class**: `LinearHeap`
- **RTTI Name**: `.?AVLinearHeap@@`
- **TypeDescriptor VA**: `0x14104bad8`
- **CompleteObjectLocator VA**: `0x140dc8bd8`
- **Vtable VA**: `0x140c31bb0`
- **Related Classes**: `TTAllocator`, `ObjWrapperBase`
- **Confidence**: 100% (Confirmed)

### `Scene`
- **Class**: `Scene`
- **RTTI Name**: `.?AVScene@@`
- **TypeDescriptor VA**: `0x14104c150`
- **CompleteObjectLocator VA**: `0x140dc9590`
- **Vtable VA**: `0x140c375d8`
- **Related Classes**: `GameEngine`, `Agent`, `MeshSceneEnlightenData`
- **Confidence**: 100% (Confirmed)

---

## 2. In-Memory Subsystem Structures

### A. Blowfish Cipher Context (`0x1050` Bytes)
Allocated at `0x1404cda7b` and initialized by `Blowfish_InitContext` (`0x140107560`):
```cpp
struct Blowfish_Context {
    uint32_t P[18];           // 0x0000..0x0047: P-box subkeys (72 bytes)
    uint32_t S[4][256];       // 0x0048..0x1047: Four S-box arrays (4,096 bytes)
    uint8_t  is_initialized;  // 0x1048: Set to 1 upon completion of BF_set_key
    uint8_t  _padding[7];     // 0x1049..0x104F: Alignment padding
};
static_assert(sizeof(Blowfish_Context) <= 0x1050, "Blowfish_Context exceeds allocation size");
```

### B. `TTArchive2_Header` (On-Disk Binary Format)
Confirmed via `0x14016b520` (`TTArchive2_Load`):
```cpp
#pragma pack(push, 1)
struct TTArchive2_Header {
    uint32_t magic;           // 0x00: 0x54544345 ("ECTT" / TTCE)
    uint32_t chunk_size;      // 0x04: Uncompressed block size (0x10000 = 65,536 bytes)
    uint32_t chunk_count;     // 0x08: Number of chunks N
    uint64_t chunk_offsets[1];// 0x0C: Array of (N + 1) uint64_t file offsets
};
#pragma pack(pop)
```

### C. `DCArray<T>` (Telltale Contiguous Array Container)
Confirmed via RTTI descriptor `.?AV?$DCArray@_K@@` and vtable at `0x140c4bfa8`:
```cpp
template <typename T>
struct DCArray {
    void*    vtable;          // 0x00: DCArray virtual table pointer
    T*       data;            // 0x08: Pointer to allocated elements
    uint64_t capacity;        // 0x10: Maximum allocated capacity
    uint64_t count;           // 0x18: Current number of elements
};
```
