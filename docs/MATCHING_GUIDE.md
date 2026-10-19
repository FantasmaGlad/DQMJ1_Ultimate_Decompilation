# Dragon Quest Monsters: Joker — C Matching Decompilation Engineering Guide

This guide establishes the technical specification, compiler configuration, clean-room standards, and verification workflow required to achieve 1:1 byte-matching decompilation for *Dragon Quest Monsters: Joker* (Nintendo DS, `NTR-AJRP-EUR`).

---

## 1. Target Hardware & Compiler Environment

### 1.1 Hardware Specifications
- **Main Processor (ARM9)**: ARM946E-S core (ARMv5TE instruction set) clocked at 67.028 MHz. Contains 8 KB Instruction Cache, 4 KB Data Cache, 32 KB ITCM (`0x01FF8000`), 16 KB DTCM (`0x027E0000`).
- **Co-Processor (ARM7)**: ARM7TDMI core (ARMv4T instruction set) clocked at 33.514 MHz. Manages real-time audio synthesis (SDAT), IPC FIFO queues, and SPI touch digitizer.
- **Hardware Math Engine**: Memory-mapped coprocessors `CP_DIV` (64/32 and 32/32 division, 36 cycles) and `CP_SQRT` (64-bit/32-bit square root, 26 cycles).

### 1.2 Target Compiler
*Dragon Quest Monsters: Joker* (released late 2006 in Japan, early 2008 in Europe) was authored using the official Nintendo Nitro SDK and built using **Metrowerks CodeWarrior for ARM (MWCCARM)**.

- **Compiler Version**: MWCCARM 2.0 SP2 (build 82) / MWCCARM 3.0.
- **Instruction Modes**:
  - **ARM (32-bit)**: Used for time-critical kernel loops, 3D geometry transformation, interrupt handlers, and hardware math routines.
  - **THUMB (16-bit)**: Used across the majority of gameplay logic, battle engine, synthesis calculations, and menu overlays to optimize code density.

### 1.3 Exact CodeWarrior Compiler Flags

```text
# General C Flags
-O4,p               # Optimization level 4, favor code speed
-proc arm946e-s     # Target core architecture
-enum int           # Force enums to 32-bit signed integers
-char signed        # char defaults to signed
-inline on          # Enable aggressive inlining
-Cpp_exceptions off # Disable C++ exception runtime
-ipa file           # Inter-procedural analysis scoped to single file

# Architecture Mode Selection
-thumb              # Emit 16-bit THUMB bytecode (default for game logic)
# (Omit -thumb for ARM 32-bit mode files, e.g. src/kernel/math.c)
```

---

## 2. ABI & Calling Conventions (ATPCS)

The codebase strictly follows the **ARM-Thumb Procedure Call Standard (ATPCS)**:

- **Argument Registers**:
  - `r0` – `r3`: First 4 word-sized parameters (or 64-bit pairs in `r0:r1`, `r2:r3`).
  - Stack (`sp`): Parameters beyond 4 words are pushed right-to-left onto the stack.
- **Return Value**:
  - `r0`: 32-bit return value or pointer.
  - `r0:r1`: 64-bit integer return value.
- **Register Scratch vs Preserved**:
  - Scratch (caller-saved): `r0`, `r1`, `r2`, `r3`, `r12` (`ip`).
  - Preserved (callee-saved): `r4`, `r5`, `r6`, `r7`, `r8`, `r9`, `r10`, `r11` (`v1`–`v8`). Must be pushed/popped if modified.
  - Special: `r13` (`sp`, stack pointer, must remain 8-byte aligned at external call boundaries), `r14` (`lr`, link register), `r15` (`pc`, program counter).

---

## 3. Clean-Room Engineering Policy

1. **Zero Proprietary SDK Code**: Do NOT copy headers, macros, or source files from official Nintendo SDKs or leaked repositories. All type definitions, memory offsets, and structure layouts in `include/` must be clean-room reconstructions derived exclusively from binary analysis of the retail European ROM (`NTR-AJRP-EUR`).
2. **Explicit Type Typing**: Use fixed-width types from `include/types.h` (`u8`, `u16`, `u32`, `s8`, `s16`, `s32`, `fx32`, `BOOL`). Avoid raw compiler primitives (`int`, `short`, `long`) to prevent 32/64-bit host architecture divergence.
3. **Hardware Registers**: Always access hardware memory-mapped I/O via the verified macros defined in `include/nds/registers.h` (`REG_CP_DIVCNT`, `REG_DMA0SAD`, etc.).

---

## 4. Function Matching Methodology

Matching a function requires making the compiler output byte-for-byte identical machine code (`.text` section) to the retail ROM slice.

```
       Retail ROM Binary (NTR-AJRP-EUR)
                     │
                     ▼
             Ghidra Baseline
         (src/overlays, src/arm9)
                     │
                     ▼ (Decompiler analysis)
             Reconstructed C
        (src/<domain>/<module>.c)
                     │
                     ▼ (MWCCARM compiler)
             Compiled Object (.o)
                     │
                     ▼ (diff.py / objdump)
             Byte-Matching Audit
          ┌──────────┴──────────┐
      [Mismatch]            [100% Match]
          │                      │
   Adjust C syntax /       Integrate into
   variable lifetimes      src/ + update
   & loop constructs       check_progress.py
```

### 4.1 Step-by-Step Workflow

1. **Identify Target Slice**: Locate function address and length in `work/analysis/` (e.g., `overlay_0000.asm:0x0218bee8`).
2. **Setup Matching Scaffold**: Place the reconstructed function in the appropriate domain folder:
   - `src/kernel/`: Memory management, task schedulers, math coprocessor drivers.
   - `src/battle/`: Battle loop, damage formulas, AI decision trees, scouting rate.
   - `src/synthesis/`: Monster breeding solver, quadrilinear fusion lookup tables.
   - `src/save/`: EEPROM serialization, block validation, CCITT CRC16.
   - `src/script/`: Event VM bytecode executor (`.evt`), cutscene cameras.
3. **Guarding In-Progress Work**: Use `#ifdef NON_MATCHING` macros when a function is functionally equivalent but not yet byte-identical:

```c
#ifdef NON_MATCHING
/* Functionally accurate C implementation undergoing register-matching */
u32 scout_rate_calculate(const ScoutParameters *params) {
    /* ... */
}
#else
/* Assembly fallback matching exact binary slice */
#endif
```

4. **Literal Pool Optimization**: CodeWarrior groups literal pool constants (`.pool` / `LDR rX, =const`) at the end of functions or after unconditional branches (`B`, `BX`). If literals appear in the wrong order, reordering local variable declarations or modifying sub-expression evaluation order will adjust pool placement.
5. **Induction Variables & Register Allocation**: If CodeWarrior assigns variables to the wrong registers (`r4` instead of `r5`), inspect variable lifetimes:
   - Declaring variables in inner blocks reduces register pressure.
   - Using `register` keyword or `volatile` casts helps guide register selection without altering semantics.

---

## 5. Progress Tracking & Tooling

Contributors must verify their progress with the automated tracker:

```bash
# Run progress check across all 7,140 functions
python3 tools/check_progress.py
```

### Progress Output Format

```text
====================================================================
  DQMJ1 (NTR-AJRP-EUR) - Decompilation Progression Status
====================================================================
Module               | Weight   | Total Funcs  | Matched  | Coverage
--------------------------------------------------------------------
arm9.bin             |    36%  |       2541   |       1  |   0.04%
overlay_0001.bin     |    29%  |       2105   |       1  |   0.05%
overlay_0000.bin     |    16%  |       1120   |       2  |   0.18%
overlay_0002.bin     |    15%  |       1062   |       2  |   0.19%
arm7.bin             |     4%  |        312   |       0  |   0.00%
--------------------------------------------------------------------
TOTAL                | 100%     |       7140   |       6  |   0.08%
====================================================================
Baseline: 100% cataloged (7,140 functions). Clean-room matching in progress.
```

---

## 6. Pull Request Checklist

Before submitting a matching pull request:

- [ ] Function builds cleanly without compiler warnings.
- [ ] No proprietary SDK headers or copyright infringements are included.
- [ ] Verified assembly comparison confirms 1:1 opcode match against retail ROM.
- [ ] Variable and parameter names are clear, descriptive, and adhere to `include/` conventions.
- [ ] Conventional Commit message used: `feat(battle): match scout_rate_calculate (0x92924)`.
- [ ] Zero emojis in commit message, code comments, or documentation.
