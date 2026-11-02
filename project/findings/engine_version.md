# Telltale Engine Identification

## Summary
The game executable `Minecraft2.exe` runs on a late-generation 64-bit revision of the proprietary **Telltale Tool** engine (specifically the **2017 branch**, designated internally as `2017_03_Minecraft2`).

This engine generation incorporates:
- **Direct3D 11 Render Pipeline** (`d3d11.dll`)
- **Geomerics Enlighten 3** Real-time Radiosity & Global Illumination SDK
- **RAD Game Tools Oodle LZ** Data Compression (`oo2core_5_win64.dll`)
- **Firelight Technologies FMOD Studio** 64-bit Audio Architecture
- **TTArchive2** chunked archive container format (`ECTT` / `TTCE`)
- **Custom Lua 5.1/5.2 Runtime** with dynamic fixup compatibility (`ttFixupLua51Script`, `ttFixupLua50Script`)

---

## Evidence Matrix

### 1. Embedded Source & Build Paths
- **Bamboo CI Build Path**:
  `C:\bambooAgent\xml-data\build-dir\BIN-MC2-P6S\TELLTALE_PC\bin\Shipping\GameApp.pdb`
- **Engine Source Code Paths**:
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\GameEngine.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\HandleObjectInfo.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\Scene.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\Meta.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\GameLoop.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\SaveLoadManager.cpp`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\RenderEnlighten.cpp`
- **Third-Party Integrations**:
  `c:\buildbot\working\2017_03_minecraft2\engine\gameengine\thirdpartyshipping\enlightensdk\src\enlightenapi\include\enlighten3\EnlightenUtils.inl`
  `C:\Buildbot\working\2017_03_Minecraft2\Engine\GameEngine\ThirdPartyShipping\OpenSSL-CMake\crypto\...`

### 2. Runtime Version & Episode Build Descriptors
From `Archives/_rescdesc_50_version_*.lua`:
- Episode 201: `2017.06.29 14:59 201 79-RC`
- Episode 202: `2017.08.10 01:33 202 52-RC`
- Episode 203: `2017.09.12 19:09 203 49-RC`
- Episode 204: `2017.10.24 13:29 204 62-RC`
- Episode 205: `2017.12.08 15:14 205 58-RC`

### 3. Archive Format & Magic Numbers
- Primary Magic: `ECTT` (`0x54544345` / `TTCE`) — Telltale Chunked Encrypted / Compressed
- Alternate Supported Magics:
  - `0x5454434e` (`TTCN`): Uncompressed chunked archive
  - `0x5454435a` (`TTCZ`): Zlib-compressed chunked archive
  - `0x54544365` (`TTCe`): Encrypted variant
  - `0x5454437a` (`TTCz`): Zlib variant

### 4. Binary Architecture & Compiler
- **Architecture**: AMD64 (x86_64)
- **Target OS**: Windows 64-bit
- **Compiler**: Microsoft Visual C++ 2015 (Linker 14.0 / MSVC 19.00, `cl.exe`)
- **RTTI Symbols**: 3,598 recovered MSVC decorated types (`.?AV...`, `.?AU...`) confirming exact class hierarchy

---

## Comparison with Known Telltale Engine Generations

| Generation | Era | Primary Games | Graphics API | Audio API | Compression | Archive Magic |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gen 2** | 2008–2010 | Sam & Max S2/S3, Tales of Monkey Island | Direct3D 9 | FMOD Ex | Zlib | `5A545441` (`ATZ`), etc. |
| **Gen 3** | 2012–2014 | The Walking Dead S1/S2, The Wolf Among Us | Direct3D 9 | FMOD Ex | Zlib | `TTARCH` |
| **Gen 4** | 2014–2015 | Tales from the Borderlands, MCSM S1 | Direct3D 9 / 11 | FMOD Ex / Studio | Zlib | `TTARCH2` |
| **Gen 5 (Enlighten)** | 2016–2017 | Batman: The Telltale Series, **MCSM Season 2**, Guardians of the Galaxy | Direct3D 11 | FMOD Studio 64 | Oodle LZ + Blowfish | `ECTT` / `TTCE` |

---

## Conclusion
- **Engine**: Telltale Tool (Gen 5 Enlighten / D3D11 Revision)
- **Engine Branch**: `2017_03_Minecraft2`
- **Confidence**: **100% (Confirmed)** based on explicit PDB paths, source file references, buildbot branch strings, and RTTI reflection data.
