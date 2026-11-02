# Contributing to MCSM Reverse Engineering

Thank you for your interest in contributing!

This project aims to document and reconstruct the internal formats, systems, and resource pipelines used by **Minecraft: Story Mode — Season Two** and the Telltale Tool engine. Contributions are welcome, whether they involve code improvements, reverse engineering research, documentation, testing, or tooling.

Because this project deals with reverse engineering, accuracy and reproducibility are extremely important. A small incorrect assumption can lead to hours of wasted investigation, so please prioritize evidence over speculation.

---

## Ways to Contribute

### Reverse Engineering Research

Useful contributions include:

- Identifying unknown functions in `Minecraft2.exe`
- Recovering additional engine structures
- Mapping classes through RTTI/vtables
- Documenting archive formats
- Investigating encryption, compression, and resource loading systems
- Comparing behavior across different Telltale games

When submitting findings, please include:

- Address/function name
- Evidence supporting the identification
- Relevant assembly snippets or references
- Confidence level

Example:

```
Function:
0x140123456

Name:
TTArchive2_ReadChunk

Confidence:
High

Evidence:
- Called from TTArchive2_Load
- Reads chunk offset table
- Passes data into StreamDecoder
```

---

## Code Contributions

Before submitting code:

1. Test your changes locally.
2. Keep changes focused.
3. Avoid introducing dependencies unless necessary.
4. Document reverse-engineered behavior clearly.

For extractor changes, please test against multiple archive types:

- ECTT (encrypted + compressed)
- ZCTT (compressed)
- NCTT (uncompressed)

Do not assume one archive represents the entire format.

---

## Reverse Engineering Guidelines

### Confirm Before Naming

Avoid marking functions as confirmed unless there is strong evidence.

Use these labels:

- **Confirmed** — Directly verified through code paths or runtime behavior.
- **High Confidence** — Strong evidence, but not fully verified.
- **Hypothesis** — A theory requiring further testing.
- **Unknown** — Not enough information yet.

---

### Document Evidence

Good:

> This function initializes a Blowfish context because it copies the standard P-array constants, expands the key schedule, and is called before block decryption.

Bad:

> This is probably encryption stuff.

---

### Do Not Remove Uncertainty

Unknown information is valuable.

If something is unclear, document it:

```
Unknown:
- Key generation source
- Whether this function handles Lua or archive encryption

Next steps:
- Trace callers
- Compare runtime behavior
```

A documented unknown is better than an incorrect answer.

---

## AI-Assisted Research

This project uses AI tools as assistants during development and analysis.

AI may be used for:

- Generating analysis scripts
- Helping interpret assembly
- Organizing documentation
- Suggesting investigation paths
- Writing boilerplate code

However:

**AI-generated conclusions must be verified.**

Reverse engineering findings should be supported by:

- Binary evidence
- Disassembly
- Runtime behavior
- Reproducible tests

AI suggestions are treated as hypotheses until confirmed.

---

## Pull Request Guidelines

A good pull request should include:

### Description

Explain:

- What was changed
- Why it was changed
- What evidence supports it

### Testing

Include:

- Commands used
- Files tested
- Expected results

Example:

```
Tested:

python extractor/main.py MC2_pc_UI_txmesh.ttarch2 --list

Result:
1028 resources detected successfully
```

### Documentation

If your change discovers new information, update the relevant documentation:

- `findings/`
- `structures/`
- `functions/`
- `progress.md`

---

## Code Style

Keep code:

- Readable
- Modular
- Documented
- Easy to debug

Prefer clear names over clever ones.

Reverse engineering code should help future researchers understand the process, not just produce a result.

---

## What Not to Submit

Please avoid:

- Unsupported guesses presented as facts
- Large unrelated rewrites
- Extracted copyrighted game assets
- Tools designed to bypass unrelated software protections
- Changes that remove attribution or documentation

---

## Final Note

Reverse engineering is a collaborative process. Every function identified, structure recovered, and format documented makes the overall picture clearer.

Whether you contribute a single byte-level observation or a complete subsystem reconstruction, your work helps preserve understanding of these systems.

Happy reversing!