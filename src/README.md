# Source Code Organization (`src/` and `include/`)

This directory contains the decompiled and reconstructed C source code for *Dragon Quest Monsters: Joker* (Nintendo DS, `NTR-AJRP-EUR`).

## Architectural Structure

The codebase is organized into domain-specific modules matching Nintendo DS software conventions:

```
├── include/
│   ├── types.h              Standard fixed-width integer types (u8, u16, u32, s32, fx32)
│   ├── global.h             Compiler macros, alignment directives, utility macros
│   ├── nds/
│   │   ├── memory.h         Memory map layout (ITCM, DTCM, Main RAM, Overlays, VRAM)
│   │   └── registers.h      Hardware I/O register definitions (CP_DIV, DMA, Timers)
│   └── game/
│       ├── synthesis.h      Monster breeding / synthesis structures & prototypes
│       ├── battle.h         Battle engine state, scouting formulas, damage parameters
│       ├── monster.h        Species descriptors, growth tables, and stat caps
│       ├── save.h           Save block structure and CRC16 checksum verification
│       └── script.h         Event VM bytecode opcodes (.evt) and runtime context
├── src/
│   ├── kernel/              Core systems, memory allocators, hardware math routines
│   ├── battle/              Battle calculations, scouting probability, combat AI
│   ├── synthesis/           Monster fusion solver and quadrilinear synthesis lookup
│   ├── save/                Save data serialization, slot management, and CRC16
│   ├── script/              Event script bytecode executor and cutscene drivers
│   ├── arm9/                ARM9 pseudo-C decompiler baseline (arm9.c)
│   ├── arm7/                ARM7 subsystem decompiler baseline (arm7.c)
│   └── overlays/            Overlay 0000, 0001, 0002 decompiler baselines
```

## Contributing Matching C Code

When contributing reconstructed functions:
1. Reference the verified assembly in `work/analysis/*.asm` to determine target addresses and calling conventions.
2. Ensure types and structs from `include/` are used rather than raw pointer arithmetic.
3. Test compatibility and run `python3 tools/check_progress.py` to confirm progression.
4. Consult `docs/MATCHING_GUIDE.md` for compiler flags, calling conventions, and pull request guidelines.
