# Dragon Quest Monsters: Joker — ROM Reverse Engineering & Source Code Reconstruction

<p align="center">
  <img src="https://dqmj1.wiki/api/assets/images/logo.png" alt="Dragon Quest Monsters: Joker Logo" width="440" />
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Target-Nintendo%20DS%20%7C%20ARMv5TE%20%2B%20ARMv4T-informational.svg)]()
[![Decompilation Baseline](https://img.shields.io/badge/Ghidra%20Decompiler%20Baseline-100%25%20%287%2C140%20funcs%29-blue.svg)]()
[![Source Reconstruction](https://img.shields.io/badge/Source%20Reconstruction-In%20Progress-orange.svg)]()
[![File Formats](https://img.shields.io/badge/Custom%20Parsers-SDAT%20%7C%20NSBMD%20%7C%20D16%20%7C%20FPK%20%7C%20EVT-purple.svg)]()
[![Companion Compendium](https://img.shields.io/badge/Companion%20Compendium-dqmj1.wiki-blueviolet.svg?style=flat)](https://dqmj1.wiki/)

Reverse engineering, binary file format dissection, and progressive C source code reconstruction for **Dragon Quest Monsters: Joker** (Nintendo DS, `NTR-AJRP-EUR`).

All extracted algorithms, formulas, and 3D assets directly power the companion web encyclopedia and 3D compendium: **[https://dqmj1.wiki](https://dqmj1.wiki/)**.

> - **Documentation en français** : [Guide complet (README.fr.md)](README.fr.md)
> - **Completion Matrix** : [Progression Treemap (docs/COMPLETION_MAP.md)](docs/COMPLETION_MAP.md)
> - **Matching Guide** : [C Decompilation Standards (docs/MATCHING_GUIDE.md)](docs/MATCHING_GUIDE.md)

---

## Decompilation Completion Treemap

Proportional module weights by function volume and sub-system analysis status:

![Decompilation Treemap](docs/assets/completion_treemap.svg)

> Full technical breakdown and symbol progress: **[docs/COMPLETION_MAP.md](docs/COMPLETION_MAP.md)**

---

## Repository Structure

| Directory | Purpose |
| :--- | :--- |
| **`include/`** | Standard C types (`types.h`), hardware I/O registers (`nds/`), and game engine structures (`game/`). |
| **`src/`** | Canonical matching C modules (`src/synthesis/`, `src/battle/`, `src/kernel/`) and baseline decompiler outputs. |
| **`tools/`** | Python and shell extraction toolchain (3D models, audio SDAT/SSEQ, 2D art, scripts, and tables). |
| **`docs/`** | Technical documentation, architecture specifications, asset inventories, and completion maps. |
| **`assets/`** | Production reference datasets, verified JSON tables, and sample 3D glTF model ([Wulfspade `m176`](assets/models/wulfspade_m176/)). |
| **`work/`** | Disassembly maps, symbol cross-references, and ROM memory layout analysis. |

---

## How to Contribute

Contributions from reverse engineers, ROM hackers, and Dragon Quest enthusiasts are welcome:

1. **Symbol Recovery**: Help identify and name functions from the Ghidra baseline (`FUN_xxxxxxxx` -> semantic names).
2. **File Formats**: Refine parsers for remaining binary formats (EVT opcodes, camera trajectories, encounter tables).
3. **Build System**: Contribute to the MetroWerks CodeWarrior matching build pipeline.

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** and **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** before submitting pull requests.

---

## Acknowledgments & Attributions

- **[Apicula Project](https://github.com/scurest/apicula)**: 3D model parsing and animation decoders (`.nsbmd`, `.nsbtx`, `.nsbca`) build upon foundational Apicula research.
- **[Bubelia](https://dqmj.fandom.com/wiki/Dragon_Quest_Monsters:_Joker_Wiki)**: Founder and author of the popular Dragon Quest Monsters: Joker Wiki on Fandom; technical cross-referencing between ROM data and community wikis, decompilation architecture review, and implementation advice.
- **Bonnford**: In-depth review of game data, story lore accuracy, and Incarnus synthesis mechanics.
- **[Dragon Quest Wiki](https://dragon-quest.org/) & [Fandom Wiki](https://dragonquest.fandom.com/)**: Community editors for their long-standing preservation work.
- **[Ghidra](https://ghidra-sre.org/)**: Reverse engineering framework for binary analysis and decompilation baselines.

---

## Legal & Disclaimer

Academic reverse engineering and preservation project under applicable interoperability laws. Dragon Quest and Dragon Quest Monsters: Joker are trademarks and copyrights of Square Enix Co., Ltd. and Armor Project.
