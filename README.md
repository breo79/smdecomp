# Minecraft Story Mode: Season Two — Reverse Engineering Project

A research project focused on understanding and documenting the internal architecture of **Minecraft: Story Mode — Season Two** and the late-generation **Telltale Tool engine**.

The goal of this project is to study how Telltale's technology handles:

- Resource archives (`.ttarch2`)
- Compression systems
- Encryption systems
- Lua scripting
- Engine structures
- Runtime classes and RTTI data
- Asset loading pipelines

This repository contains reverse engineering notes, analysis scripts, recovered structures, and experimental tooling created during the investigation.

> This project is for educational and preservation purposes.

---

## Project Goals

The primary objective is to understand the technical systems behind the game rather than modify or redistribute game content.

Current research areas:

### TTARCH2 Archive Format

Investigation into Telltale's archive container format:

- Archive header reconstruction
- Chunk tables
- Offset systems
- Compression detection
- Encryption handling
- Resource indexing

Supported archive types currently being investigated:

| Magic | Description |
|---|---|
| TTCE | Encrypted archive format |
| TTCZ | Compressed archive format |
| TTCN | Uncompressed archive format |

---

## Engine Research

Minecraft: Story Mode Season Two uses a late-generation version of the Telltale Tool engine.

Research includes:

- Engine subsystem identification
- Function mapping
- RTTI class recovery
- Virtual table analysis
- Resource pipeline reconstruction

Known engine components:

- Telltale Tool runtime
- RAD Oodle compression
- FMOD audio systems
- Lua scripting runtime
- DirectX rendering systems

---

## Reverse Engineering Process

The project uses several analysis tools:

- Ghidra
- Custom Python analysis scripts
- PE binary inspection
- Assembly analysis
- RTTI recovery
- Runtime tracing

The workflow generally follows:

```
Binary
  |
  v
Static Analysis
  |
  v
Function Identification
  |
  v
Hypothesis Testing
  |
  v
Documentation
  |
  v
Tool Development
```

---

# AI-Assisted Development

This project makes use of AI tools as research assistants.

AI is used for:

- Generating analysis scripts
- Helping interpret assembly patterns
- Suggesting investigation paths
- Organizing documentation
- Summarizing findings
- Reviewing hypotheses

AI does **not** replace verification.

All important discoveries are validated through:

- Binary evidence
- Disassembly
- Cross references
- Runtime behavior
- Testing against actual game files

The process is best described as:

```
Human Researcher
       |
       v
AI Assistance
       |
       v
Hypothesis
       |
       v
Binary Verification
       |
       v
Confirmed Finding
```

AI helps accelerate exploration, but conclusions are based on technical evidence.

---

## Repository Structure

```
.
├── scripts/
│   ├── Analysis and research scripts
│   └── Experimental tooling
│
├── project/
│   ├── findings/
│   │   ├── Archive research
│   │   ├── Crypto research
│   │   ├── Compression research
│   │   └── Engine notes
│   │
│   ├── functions/
│   │   └── Function mapping
│   │
│   └── structures/
│       └── Recovered classes and data structures
│
└── README.md
```

---

# Current Progress

## Completed / Confirmed

- [x] TTARCH2 header analysis
- [x] Chunk table reconstruction
- [x] Archive validation tooling
- [x] Oodle decompression investigation
- [x] Blowfish-related encryption research
- [x] Telltale Lua bytecode investigation
- [x] Initial RTTI/class recovery
- [x] Engine component identification

## In Progress

- [ ] Complete resource index reconstruction
- [ ] Recover filename/hash mapping
- [ ] Build archive extraction pipeline
- [ ] Verify encryption/decryption pipeline end-to-end
- [ ] Create reusable extraction tools

---

# Disclaimer

This repository does not include copyrighted game assets.

You must own the original game files to perform any experiments involving extracted data.

The purpose of this project is research, documentation, and preservation of software technology.

---

# Why?

Games are software history.

When studios close, tools disappear, and old technology becomes undocumented, understanding how these systems worked becomes increasingly difficult.

This project aims to document one small piece of that history: how the Telltale Tool worked internally and how its games were built.