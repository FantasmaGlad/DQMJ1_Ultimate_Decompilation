# Inventory of Extracted Assets and Reverse Engineering Status

This document provides a comprehensive inventory of all extracted game assets, decompiled systems, verified mechanics, and remaining research targets for *Dragon Quest Monsters: Joker* (Nintendo DS).

---

## 1. Decompiled Code and Binaries (100% Complete)

| Component | Target Architecture | Base Address | Lines of C | Status |
|---|---|---|---|---|
| `arm9.bin` | ARM946E-S (ARMv5TE) | `0x02000000` | 70,575 | Fully decompiled, clean C output (`src/arm9/arm9.c`) |
| `arm7.bin` | ARM7TDMI (ARMv4T) | `0x02380000` | 10,879 | Fully decompiled (`src/arm7/arm7.c`) |
| `overlay_0000.bin` | ARM9 Dynamic Overlay 0 | `0x02184b40` | 44,233 | Fully decompiled (`src/overlays/overlay_0000.c`) |
| `overlay_0001.bin` | ARM9 Dynamic Overlay 1 | `0x02184b40` | 89,901 | Fully decompiled (`src/overlays/overlay_0001.c`) |
| `overlay_0002.bin` | ARM9 Dynamic Overlay 2 | `0x02184b40` | 64,342 | Fully decompiled (`src/overlays/overlay_0002.c`) |
| **Total** | | | **279,930** | **7,140 functions decompiled, 0 failure** |

---

## 2. 3D Graphics and Models (100% Extracted)

| Category | Format / Source | Count | Extracted / Converted Format | Notes |
|---|---|---|---|---|
| Monster Models | `.nsbmd` + `.nsbtx` | 210 | `.gltf` + `.bin` + PNG textures / Blender `.blend` | Complete coverage of all 210 distinct monster species |
| Character Models | `.nsbmd` + `.nsbtx` | 18 | `.gltf` + `.bin` + PNG textures / Blender `.blend` | Protagonist, rivals, scouts, NPCs (`n001` to `n022`) |
| World Maps | `.map` (FPK archives) | 90 | `.glb` (3D worlds) + metadata | 90 world environments, island sub-areas, and interiors |
| Battle Arenas | `.nsbmd` / `.map` | 83 | `.glb` + metadata | Authentic 3D battle rings (`bf*`, `bd*`, `bh*`, `be*`) |
| Skeletal Animations | `.nsbca` | 1,107 | glTF animation clips | Standard battle and field animations |
| Static Model Variants | Shared mesh + texture | 28 | glTF + variant PNG mappings | Verified identical vertex topology, dynamic texture swap |

---

## 3. 2D Graphics and Artworks (100% Extracted)

| Category | Source File | Count | Format | Status |
|---|---|---|---|---|
| Monster Pixel Art Icons | `sd_*.dma` + `.pal` | 210 | PNG 24x24 / 32x32 | Complete official 2D monster icons |
| Boss Icons | `sd_*.dma` + `.pal` | 13 | PNG | Authentic boss battle interface markers |
| Full-Screen Artworks | `dm_pic_*.d16` | 40 | PNG 256x192 (RGB555) | Prologue, epilogue, and storyline illustration panels |
| Lower Screen Minimaps | `.CHR` / `.SCR` / `.PAL` | 60 | PNG 256x192 | Dual-screen DS minimaps decoded with hardware VRAM palettes |
| Interface Backgrounds | `wall_*.bin` | 7 | PNG 256x192 | Menu backdrops (Synthesis altar, Monster bank, Storage) |
| Family Crest Icons | Interface tiles | 8 | PNG 250x250 transparent | Slime, Dragon, Nature, Beast, Material, Demon, Undead, Incarnus |

---

## 4. Audio and Music (100% Extracted & Resynthesized)

| Audio Type | Source | Count | Format & Quality | Verification / Status |
|---|---|---|---|---|
| Background Music (BGM) | `sound_data.sdat` (SSEQ) | 25 | MP3 320 kbps (Studio render) | Rendered with native SWAR instrument banks; true loop points |
| Sound Effects (SFX) | `sound_data.sdat` (STRM + SSEQ) | 292 | MP3 320 kbps | Spells, physical strikes, UI alerts, field interaction sounds |
| Jingles & Fanfares (ME) | `sound_data.sdat` (STRM / SSEQ) | 19 | MP3 320 kbps | Event fanfares (Victory, Sanctuary, Quest, Level-up) |
| Raw Instrument Samples | `sound_data.sdat` (SWAR) | 404 | WAV (ADPCM / PCM16) | Individual hardware instrument samples |

---

## 5. Game Logic and Data Tables (Extracted & Verified)

- **Monster Species Stats** (`EnmyKindTbl.bin`): Level 1 base stats (HP, MP, Atk, Def, Agi, Wis) proven at ARM9 addresses `0x0203a640` and `0x0203db00`; stat caps (offsets 28..39).
- **Synthesis System** (`overlay_0000:FUN_0218bee8`): Complete 2-parent generation logic, family mixing table, and 16 quadrilinear (4-parent) recipes verified.
- **Scouting / Taming Formula** (`overlay_0001:0x92924`): Exact base rates, tension multipliers (5/20/50/100), Oomph impact, and boss immunities.
- **Battle AI Profiles** (`AI_PatternTbl.bin`, `AI_ActionTBL.bin`, etc.): 131 battle patterns, 256 tactical actions, role evaluations.
- **Wild Encounters** (`66 .enct` files): 105 wild species mapped with Day, Night, and Rain/Storm weather conditions.
- **3D Chest Coordinates** (`.evt` opcode `0x5f` + `.pos`): 76 physical 3D chests placed with exact XYZ coordinates, yaw, tiers (A/B/C), and trap rates (Cannibox/Mimic).
- **Story Cutscenes & Dialogues** (`demoNNN.bin` + `.evt`): 244 cutscene scripts, 644 camera plans (20.12 fixed-point), 4,971 spoken dialogue lines aligned across 5 official languages (EN, FR, DE, IT, ES).
- **Trainer Teams**: 158 trainer profiles decoded from `MstrPtnTbl.bin` and `FldMstrPrm.bin`, including all 21 roaming scouts.

---

## 6. What Remains Incomplete, Uncertain, or To Be Investigated

| Topic | Targeted Files / Code | Current Status | What Is Missing / Uncertainty |
|---|---|---|---|
| Skill Points per Level | `SkillPointTbl.bin` / `overlay_0001` | Non-proven | The function linking monster level progression to allocated skill points is not yet mapped in assembly. |
| Complete Battle Damage Table | `DamageTbl.bin` (2,048 B), `DamageItemTbl.bin` | Partially decoded | Loader is verified, but exact modifier matrix indexing inside `overlay_0001` needs line-by-line decompilation. |
| Battle Tension Multiplier | `overlay_0001` battle routines | Uncertain | Capture tension rates are verified (x1.4 to x2.5), but combat attack tension multipliers (reported as x1.7 to x7.5) require disassembly confirmation. |
| Boss Specific Instance Offsets | `BtlEnmyPrm.bin` (offsets `+0x00..0x07`, `+0x20..0x2F`) | Unmapped | Around 39 bytes per enemy instance in `BtlEnmyPrm` remain unassigned; boss-specific resistance overrides might be located here. |
| Binary Map Name Association | `mes_mapname.bin` | Inferred | Map names currently matched via warp triggers and sequential order; the hardcoded assembly table address is not yet confirmed. |
| Casino Dialogue Avatars | `k001.evt`, `f020.evt` (opcode `0x62`) | Unresolved | 14 casino NPCs (Alba, Announcer, Croupiers) use runtime RAM variables for spawning; static 3D model links cannot be deduced without emulator memory inspection. |
