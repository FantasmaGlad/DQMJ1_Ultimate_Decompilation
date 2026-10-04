# 3D Animated Model: Wulfspade (No. 336 / m176)

This folder contains the complete, reverse-engineered 3D model and skeletal animation dataset for **Wulfspade** (Species No. 336, internal model code `m176`, known as *Apik* in French), the iconic Incarnus guardian beast of *Dragon Quest Monsters: Joker*.

---

## Technical Specifications

| Parameter | Value |
|---|---|
| Monster Name | Wulfspade (*Apik*) |
| Pokedex / Monster ID | No. 336 |
| Internal Model ID | `m176` |
| Family | Incarnus |
| Original Source | Nintendo DS ROM (`data/m176.nsbmd` + `data/m176_*.nsbca`) |
| Converted Formats | glTF 2.0 (`.gltf` + `.bin` + `.png`) and standalone Binary glTF (`.glb`) |
| Texture Format | 256x256 RGBA PNG (`m176_1.png`) |
| Vertex Count | 1,180 vertices, indexed triangle primitives |
| Skeleton Rig | 28 bones with hardware vertex weighting (skinning) |
| Animation Clips | 10 official skeletal animations decoded from ROM bytecode |

---

## Included Files

- `m176.glb`: Self-contained binary glTF file including embedded geometry, texture buffer, and all 10 skeletal animation tracks. Drag-and-drop compatible with any standard glTF viewer, Blender 3.x/4.x, Godot, Unity, or Unreal Engine.
- `m176.gltf`: Human-readable JSON descriptor specifying nodes, meshes, skins, accessors, materials, and animation channels.
- `m176.bin`: Binary buffer storing vertex positions, normals, texture coordinates, bone indices, bone weights, and animation keyframes.
- `m176_1.png`: Extracted diffuse texture map.

---

## Skeletal Animation Tracks

The following animation clips are decoded directly from Nintendo DS `.nsbca` files:

| Track Index | Clip Name | Action | Loop Behavior |
|---|---|---|---|
| 0 | `m176_00` | Battle Idle Stance | Loop |
| 1 | `m176_01` | Field Idle Stance | Loop |
| 2 | `m176_02` | Walk / Run Cycle | Loop |
| 3 | `m176_03` | Physical Attack Strike | Play Once |
| 4 | `m176_04` | Spell Cast / Special Ability | Play Once |
| 5 | `m176_05` | Hit Reaction (Light Damage) | Play Once |
| 6 | `m176_06` | Severe Knockback Damage | Play Once |
| 7 | `m176_07` | Defeat / Fainting Collapse | Play Once |
| 8 | `m176_08` | Victory Howl / Battle Cry | Play Once |
| 9 | `m176_10` | Alternate Combat Idle Stance | Loop |

---

## Usage in Blender

1. Open Blender.
2. Navigate to **File > Import > glTF 2.0 (.glb / .gltf)**.
3. Select `assets/models/wulfspade_m176/m176.glb`.
4. Switch the 3D viewport to **Material Preview** or **Rendered** shading mode.
5. In the timeline / Dope Sheet (Action Editor), select any of the 10 animation actions to preview the playback.
