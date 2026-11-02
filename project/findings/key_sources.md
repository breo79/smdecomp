# Cryptographic Key Sources Analysis

## Summary
Minecraft: Story Mode - Season Two (Telltale Tool 2017 Gen 5) utilizes a 55-byte master Blowfish key stored in the executable's read-only data section (`.rdata`). This document details the key representation, memory location, caller mechanisms, and how encryption keys are sourced throughout the game engine.

---

## 1. Master Archive Encryption Key

- **Status**: **Confirmed**
- **Algorithm**: Blowfish (16 rounds, 448-bit / 55-byte key)
- **Virtual Address**: `0x140c3d5b0`
- **File Offset**: `0x00c3c5b0` (`.rdata` section)
- **Length**: 55 bytes (`0x37`), null-terminated byte sequence
- **Hex Representation**:
  ```
  8cd29b9987de94a9e69ea5947fcec1bccc9c8eddb1a7669fb28addba9cdec29ad377627faecca7d1d8e6d9d2ab64829f92cc9498d3e4a0
  ```
- **Byte Stream (55 bytes)**:
  `\x8c\xd2\x9b\x99\x87\xde\x94\xa9\xe6\x9e\xa5\x94\x7f\xce\xc1\xbc\xcc\x9c\x8e\xdd\xb1\xa7\x66\x9f\xb2\x8a\xdd\xba\x9c\xde\xc2\x9a\xd3\x77\x62\x7f\xae\xcc\xa7\xd1\xd8\xe6\xd9\xd2\xab\x64\x82\x9f\x92\xcc\x94\x98\xd3\xe4\xa0`

---

## 2. Key Scope & Sourcing Architecture

Analysis of binary callers and archive formats confirms the following key hierarchy:

1. **Master Static Archive Key**:
   - The master key at `0x140c3d5b0` is hardcoded directly into `Minecraft2.exe`.
   - It is shared across all episodes (Episodes 201 to 205) for all encrypted `ECTT` archives.
   - It is NOT dynamically generated via user credentials or machine-specific hardware IDs.

2. **Default Blowfish Context (`0x140107470`)**:
   - Manages a singleton `Blowfish_Context` allocated on the heap (0x1050 bytes).
   - Stored in global pointer `0x1410d1578`.
   - Automatically loaded when archive decompression routines encounter `ECTT` (`0x54544345`) chunks without an explicit per-archive key override.

3. **Script API Override (`Resource_LoadWithEncryptionKey` at `0x1404cda20`)**:
   - Registered in Lua engine as `Resource_LoadWithEncryptionKey(archive_name, [key_string])`.
   - Inspects Lua argument 2 (`lua_tolstring(L, 2, NULL)`):
     - If non-null: dynamically allocates a new 0x1050-byte `Blowfish_Context` and calls `Blowfish_InitContext` (`0x140107560`) with the custom string.
     - If null or omitted: invokes `0x140107470` to fetch the default master context.

4. **Script Bytecode Encryption (`\x1bLEo` / `\x1bLEn`)**:
   - Compiled Lua scripts packed into archives or external directories begin with custom magic `\x1bLEo` or `\x1bLEn`.
   - At runtime, `0x14015a480` / `0x14015a420` decrypts the payload in-place using Blowfish and restores the standard Lua 5.2 bytecode header `\x1bLua` (`0x61754c1b`).
