# Guessed / Inferred Structures

These structures represent educated guesses based on RTTI symbol inspection, disassembly context, and comparison with earlier Telltale Tool reverse engineering work.

---

## 1. `ResourceEntry` (`.?AUResourceEntry@TTArchive2@@`)
- **Confidence**: 75% (Strong guess)
- **Basis**: RTTI indicates `ResourceEntry` belongs to `TTArchive2`, and `DCArray<ResourceEntry>` exists.

```cpp
struct ResourceEntry {
    uint64_t name_hash;   // 0x00: 64-bit CRC64/Symbol hash of resource filename
    uint64_t offset;      // 0x08: Relative offset inside the uncompressed stream
    uint32_t size;        // 0x10: Uncompressed file size in bytes
    uint32_t flags;       // 0x14: Compression / stream flags
};
```

---

## 2. `Symbol` (`.?AVSymbol@@`)
- **Confidence**: 85% (Strong guess)
- **Basis**: Telltale engine widespread use of 64-bit hashes for property keys, function names, and asset paths.

```cpp
struct Symbol {
    uint64_t mCRC64;      // 64-bit hashed value representing string
};
```

---

## 3. `PropertySet` (`.?AVPropertySet@@`)
- **Confidence**: 70% (Strong guess)
- **Basis**: RTTI classes `PropertySet`, `KeyInfo@PropertySet`, `PropertyValue`.

```cpp
struct PropertySet {
    void* vtable;
    uint32_t mFlags;
    uint32_t mVersion;
    // Intrusive set or map of (Symbol -> PropertyValue)
    void* mPropertyMap;
};
```
