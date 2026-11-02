# Lua Script Cryptographic Pipeline & Bytecode Transformation

## Summary
In *Minecraft: Story Mode - Season Two* (Telltale Tool 2017 Gen 5), Lua scripts stored inside TTARCH2 resource archives undergo a two-tier transformation:
1. **Archive Level Encapsulation**: Stored as individual resource files inside the `TTA4` index table.
2. **Bytecode Level Encryption**: Stored in a proprietary encrypted format bearing the header `\x1bLEo` (`0x6f454c1b`) or `\x1bLEn` (`0x6e454c1b`) instead of the standard Lua 5.2 header `\x1bLua` (`0x61754c1b`).

At runtime, the engine's script loader dynamically transforms the buffer in-memory right before passing it to the Lua VM bytecode reader (`lua_load`).

---

## 1. Extracted File Analysis

Examination of extracted `.lua` resources (e.g. from `MC2_pc_CrowdPlayLAN_Project.ttarch2`):
- `CrowdPlay.lua` (43,987 bytes)
- `CrowdPlayOverlay.lua` (33,661 bytes)
- `DialogChoices.lua` (56,380 bytes)
- `UI.lua` (22,120 bytes)

### Binary Header:
Every extracted file begins with:
```hex
1b 4c 45 6f 00 37 53 62 fd 6c ca 5b 3d aa 16 85 ...
```
- Bytes `0..3`: `\x1bLEo` (custom Telltale encrypted Lua bytecode magic)
- Bytes `4..`: Encrypted Lua bytecode payload

**Conclusion**: Extracted Lua files remain encrypted in-place on disk. The game engine applies a second decryption step inside the Lua subsystem during execution.

---

## 2. In-Memory Decryption Routine (`luaScript_DecryptBytecode` - `0x14015a480`)

**Confidence: Confirmed** (Validated via x64 disassembly at `0x14015a480`)

### Prototype:
```cpp
void __fastcall luaScript_DecryptBytecode(
    uint8_t* buffer,           // RCX: Pointer to loaded script buffer
    size_t length,             // EDX: Script size in bytes
    Blowfish_Context* ctx      // R8:  Blowfish cipher context
);
```

### Disassembly Analysis:
```x86asm
0x14015a480: push rbx
0x14015a482: sub  rsp, 0x20
0x14015a486: mov  r9, r8                ; r9 = Blowfish_Context
0x14015a489: mov  rbx, rcx              ; rbx = buffer pointer
0x14015a48c: mov  r8d, edx              ; r8d = buffer length
0x14015a48f: lea  rdx, [rcx + 4]        ; rdx = buffer + 4 (skip 4-byte header)
0x14015a493: add  r8d, -4               ; r8d = length - 4
0x14015a497: mov  rcx, r9               ; rcx = Blowfish_Context
0x14015a49a: mov  eax, r8d
0x14015a49d: and  eax, 7
0x14015a4a0: sub  r8d, eax              ; r8d = (length - 4) & ~7 (align to 8-byte block)
0x14015a4a3: call 0x140107a10          ; Blowfish_ProcessBlocks_Decrypt(ctx, buf + 4, aligned_len)
0x14015a4a8: mov  eax, dword ptr [rbx]  ; load original 4-byte header
0x14015a4aa: cmp  eax, dword ptr [rip + 0xaefbd8] ; cmp with \x1bLEo (0x140c49090)
0x14015a4b0: jne  0x14015a4b8
0x14015a4b2: mov  dword ptr [rbx], 0x61754c1b     ; overwrite header with \x1bLua (standard Lua 5.2)
0x14015a4b8: add  rsp, 0x20
0x14015a4bc: pop  rbx
0x14015a4bd: ret
```

### Transformation Process:
1. **Header Check**: Confirms file begins with `\x1bLEo` (`0x6f454c1b`) or `\x1bLEn` (`0x6e454c1b`).
2. **Cipher Boundary**: Skips the 4-byte magic. The payload length `(len - 4)` is aligned down to an 8-byte boundary (`len & ~7`).
3. **Decryption**: Calls `0x140107a10` (Blowfish Feistel Decryption) using the active `Blowfish_Context`.
4. **Header Rewrite**: The original magic `\x1bLEo` is replaced in-place with `\x1bLua` (`0x61754c1b`).
5. **Execution**: The restored buffer is standard Lua 5.2 compiled bytecode ready for `lua_load`.

---

## 3. Script Encryption Counterpart (`luaScript_EncryptBytecode` - `0x14015a420`)

The engine also includes the reverse encryption function used during build/packaging:
- Checks if buffer starts with standard `\x1bLua`.
- Replaces magic with `\x1bLEo` or `\x1bLEn`.
- Calls `0x140107590` (Blowfish Feistel Encryption) on `(length - 4) & ~7` bytes.

---

## 4. Key Sourcing & Context Propagation

When scripts are loaded:
1. **Default Execution**: If no custom key was supplied via `Resource_LoadWithEncryptionKey`, `0x140107470` (`Blowfish_GetDefaultContext`) provides the default context initialized with the 55-byte master key at `0x140c3d5b0`.
2. **Explicit Override**: If a script invokes `Resource_LoadWithEncryptionKey(archive_name, custom_key)` (`0x1404cda20`), a dedicated `Blowfish_Context` is allocated and bound to that archive/script namespace.
3. **Lua State Execution**: After decryption, the bytecode is passed to `0x14004d580`, which calls Lua 5.2 `lua_load` / `lua_pcall`.
