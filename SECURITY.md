# Security Policy & Asset Guidelines

## Purpose & Scope
This repository is dedicated to technical research, documentation, and educational reverse engineering of the 2017 Telltale Tool engine and its file formats (specifically *Minecraft: Story Mode - Season Two*). 

This project does not distribute, host, or pirate copyrighted game software, binary executables, audio, textures, or scripts.

---

## 1. Responsible Disclosure

If you discover a security vulnerability in this repository, its tooling, or related automation scripts:

- **Do not open a public GitHub issue** detailing the vulnerability.
- Please submit a private report via GitHub Private Vulnerability Reporting or contact the maintainers directly.
- Include a detailed description of the vulnerability, reproduction steps, and potential impact.
- Maintainers will investigate, verify, and resolve confirmed vulnerabilities promptly.

---

## 2. Prohibition on Copyrighted Assets

To protect the project, its contributors, and intellectual property rights:

> [!CAUTION]
> **DO NOT commit, upload, or attach original game files or extracted assets to this repository.**

Specifically:
- **No Original Archives**: Do not commit `.ttarch2`, `.ttarch`, `.exe`, or `.dll` files from commercial game installations.
- **No Extracted Assets**: Do not commit extracted proprietary models (`.d3dmesh`), textures (`.d3dtx`), audio files (`.wav`, `.fsb`), or dialogues.
- **No Compiled Script Bytecode**: Do not share proprietary encrypted or compiled game scripts (`.lua`).
- **Clean Pull Requests**: Ensure all pull requests, tests, and documentation use synthetic test vectors or mock byte buffers rather than proprietary assets. Pull requests containing copyrighted material will be rejected immediately.

---

## 3. Educational & Historical Research Disclaimer

This project is conducted strictly for:
- **Interoperability**: Understanding container encapsulation and resource indexing formats for modding and user-generated content.
- **Preservation**: Documenting deprecated 32-bit and 64-bit engine architectures where official documentation and developer support no longer exist.
- **Computer Science Education**: Studying binary file structures, block ciphers, dictionary compression, and virtual machine bytecode layouts.

Contributors and users are responsible for complying with all applicable local, national, and international laws regarding reverse engineering and copyright. You must own a legitimate copy of the software to run local extraction tests against your own files.
