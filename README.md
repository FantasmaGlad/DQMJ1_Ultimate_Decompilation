# Dragon Quest Monsters: Joker — Ultimate Decompilation & Reverse Engineering

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Target-Nintendo%20DS%20%7C%20ARMv5TE%20%2B%20ARMv4T-informational.svg)]()
[![Decompilation Rate](https://img.shields.io/badge/Decompilation-100%25%20%287%2C140%20funcs%29-success.svg)]()
[![Codebase](https://img.shields.io/badge/Reconstructed%20C-279k%20LoC-blue.svg)]()
[![Disassembly & Tooling](https://img.shields.io/badge/Analysis-Ghidra%20Headless%20%7C%20objdump-orange.svg)]()
[![File Formats](https://img.shields.io/badge/Custom%20Parsers-SDAT%20%7C%20NSBMD%20%7C%20D16%20%7C%20FPK%20%7C%20EVT-purple.svg)]()
[![Multi-language](https://img.shields.io/badge/Data%20Localization-5%20Languages%20%28EN%2FFR%2FDE%2FIT%2FES%29-teal.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Grade%20Research-brightgreen.svg)]()

Comprehensive reverse engineering, bytecode analysis, and full-stack C decompilation for **Dragon Quest Monsters: Joker** (Nintendo DS, 2006-2008, European version `NTR-AJRP-EUR`).

This repository showcases advanced systems-level reverse engineering, proprietary binary protocol dissection, custom compiler tooling, and hardware-accurate asset restoration for dual-core embedded architectures.

> **French Documentation / Documentation en français :**
> - [Guide de démarrage complet (README.fr.md)](README.fr.md)
> - [Inventaire des actifs extraits et statut R&D (docs/WHAT_IS_DONE.md)](docs/WHAT_IS_DONE.md)
> - [Documentation technique exhaustive de A à Z (docs/fr/GUIDE_COMPLET.md)](docs/fr/GUIDE_COMPLET.md)
> - [Guide d'extraction des ressources multimédias (docs/fr/EXTRACTION_RESSOURCES.md)](docs/fr/EXTRACTION_RESSOURCES.md)


---

## Project Overview

- **100% Decompiled Code**: 7,140 functions completely decompiled into 279,930 lines of pseudo-C across ARM9, ARM7, and all three runtime overlays.
- **Accurate Memory Architecture**: Fixed base mapping (`0x02000000` for ARM9, `0x02184b40` for overlays 0/1/2) with verified cross-references.
- **Custom Tooling Suite**: Production-grade decoders for DS formats:
  - 3D Models and skeleton rigs (`.nsbmd`, `.nsbca`, `.nsbtx`) converted to glTF and Blender `.blend`.
  - Audio sequence playback and resynthesis (`.sdat`, `.sseq`, `.swar`, `.sbnk`) to WAV and MP3 320 kbps.
  - 2D graphics (`.d16` BGR555, `.CHR`/`.SCR`/`.PAL` tilemaps) to PNG.
  - Event scripts (`.evt` TLV bytecode) and cutscenes (`demoNNN.bin` / `.pos`).
- **Data Tables & Game Mechanics**: Synthesis algorithms, monster species base stats, growth curves, elemental resistances, trainer teams, and battle AI logic (`AI_*.bin`).

---

## Technical Competencies & Engineering Highlights

This project demonstrates deep expertise across several systems programming, reverse engineering, and low-level software engineering domains:

- **Static Binary Analysis & Assembly**:
  - In-depth reverse engineering of ARMv5TE (ARM946E-S) and ARMv4T (ARM7TDMI) instruction sets.
  - Resolving mixed ARM (32-bit) / Thumb (16-bit) state switching without compilation artifacts.
  - Ghidra headless automation (`Java` scripts) for large-scale function detection, cross-reference tracking, and custom decompilation pipelines.
- **Binary Format Reverse Engineering**:
  - Full bit-level dissection of undocumented binary containers: FPK archive structures, POS camera matrices (20.12 fixed-point arithmetic), and EVT Tag-Length-Value (TLV) bytecode interpreters.
  - Proprietary sound synthesis decoding: reverse engineered Nitro SDAT sequence commands (events, loops, tempo timers) and parsed ADPCM / PCM16 SWAR multi-instrument soundbanks.
- **Embedded Architecture & Memory Management**:
  - Reconstructing multi-overlay memory maps sharing physical RAM addresses (`0x02184b40`).
  - Auditing memory layouts: distinguishing `.data`, `.rodata`, literals, and uninitialized `.bss` segments across game modules.
- **Data Integrity & Automation**:
  - Deterministic Python and Bash toolchains: reproducible extraction pipelines producing structured, strongly-typed JSON data from raw binary tables (`EnmyKindTbl`, `ItemTbl`, `SkillTbl`).


---

## Target Architecture: Nintendo DS

The Nintendo DS features an asynchronous dual-core architecture with shared memory:

```
+-------------------------------------------------------------+
|                        Nintendo DS                          |
|                                                             |
|   +------------------+             +--------------------+   |
|   |      ARM9        |             |       ARM7         |   |
|   |    ARM946E-S     |             |     ARM7TDMI       |   |
|   |     67 MHz       |             |      33 MHz        |   |
|   |    ARMv5TE       |             |      ARMv4T        |   |
|   |                  |             |                    |   |
|   |  GAME ENGINE:    |             |  HARDWARE SUPPORT: |   |
|   |  - 3D rendering  |             |  - Sound mixer     |   |
|   |  - Game logic    |             |  - Wi-Fi           |   |
|   |  - Battle AI     |             |  - Touchscreen     |   |
|   |  - World scripts |             |  - RTC / Power     |   |
|   +--------+---------+             +---------+----------+   |
|            |                                 |              |
|            +---------------+-----------------+              |
|                            |                                |
|                   +--------v--------+                       |
|                   |    4 MB RAM     |  (Shared)             |
|                   +-----------------+                       |
+-------------------------------------------------------------+
```

### Memory Map (Verified Offsets)

| Binary Module | Base Address | Entry Point | Size | Role |
|---|---|---|---|---|
| `arm9.bin` | `0x02000000` | `0x02000800` | 492,576 bytes | Main engine, physics, state machines, scripts |
| `arm7.bin` | `0x02380000` | `0x02380000` | 157,660 bytes | Hardware driver, audio playback, RTC |
| `overlay_0000.bin` | `0x02184b40` | Dynamic | 378,912 bytes | Menus, synthesis engine (`FUN_0218bee8`), inventory |
| `overlay_0001.bin` | `0x02184b40` | Dynamic | 618,112 bytes | Turn-based battle engine, damage formulas, monster AI |
| `overlay_0002.bin` | `0x02184b40` | Dynamic | 480,736 bytes | Wireless communications, arena battles |

---

## Repository Structure

```
DQMJ1_Ultimate_Decompilation/
|-- src/                      Decompiled C source code
|   |-- arm9/                 Core ARM9 engine code (arm9.c)
|   |-- arm7/                 Support ARM7 subsystem code (arm7.c)
|   `-- overlays/             Overlays 0, 1 and 2 decompiled code
|-- tools/                    Extraction, conversion and analysis scripts
|   |-- ghidra_scripts/       Ghidra headless automation scripts
|   |-- blender/              Blender scene setup and automation
|   |-- optimiser/            Node.js glTF processing pipelines
|   `-- extraire_*.py         Python decoders for game data and assets
|-- assets/                   Extracted game data (JSON, images)
|-- docs/                     Documentation and research notes
|   |-- en/                   Technical documentation (English)
|   |-- fr/                   Detailed guides and tutorials (French)
|   `-- architecture/         Hardware diagrams and memory specs
|-- rom/                      ROM dumps and release info (compressed)
|-- CONTRIBUTING.md           Guidelines for contributors
|-- CODE_OF_CONDUCT.md        Community standards
|-- LICENSE                   MIT License
`-- README.md                 Main project documentation
```

---

## Quick Start & Tooling

### Prerequisites

- Python 3.10+
- ndstool / devkitARM (optional, for direct ROM repacking)
- Ghidra 11+ with headless analyzer (for decompilation passes)
- Node.js 20+ (for 3D optimization tools)
- Blender 3.6+ / 4.x (for 3D rigging and animations)

### Running Extraction Tools

```bash
# Extract synthesis recipes and matrix
python3 tools/extraire_synthese.py

# Extract complete monster species base stats and limits
python3 tools/extraire_stats_especes.py

# Extract battle AI rules and decision trees
python3 tools/extraire_ia_combat.py

# Decode map layouts and 3D chest coordinates
python3 tools/extraire_coffres_3d.py

# Render SSEQ sequence music to WAV/MP3
python3 tools/rendre_sequences_sseq.py
```

---

## Contributing

Contributions from reverse engineers, ROM hackers, and Dragon Quest enthusiasts are welcome!
Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## Legal & Disclaimer

This is an academic reverse engineering and preservation project conducted under applicable interoperability laws. Dragon Quest and Dragon Quest Monsters: Joker are trademarks and copyrights of Square Enix Co., Ltd. and Armor Project.
