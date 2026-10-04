# Inventaire des Actifs Extraits et État de la Rétro-Ingénierie

Ce document dresse l'inventaire exhaustif de tous les actifs extraits de la ROM, des systèmes décompilés, des formules prouvées et des zones de recherche restant à approfondir pour *Dragon Quest Monsters: Joker* (Nintendo DS).

---

## 1. Code Décompilé et Binaires (100 % Achevés)

| Composant | Architecture Cible | Adresse de Base | Lignes de C | État |
|---|---|---|---|---|
| `arm9.bin` | ARM946E-S (ARMv5TE) | `0x02000000` | 70 575 | Décompilation C complète (`src/arm9/arm9.c`) |
| `arm7.bin` | ARM7TDMI (ARMv4T) | `0x02380000` | 10 879 | Décompilation C complète (`src/arm7/arm7.c`) |
| `overlay_0000.bin` | Overlay dynamique ARM9 (0) | `0x02184b40` | 44 233 | Décompilation C complète (`src/overlays/overlay_0000.c`) |
| `overlay_0001.bin` | Overlay dynamique ARM9 (1) | `0x02184b40` | 89 901 | Décompilation C complète (`src/overlays/overlay_0001.c`) |
| `overlay_0002.bin` | Overlay dynamique ARM9 (2) | `0x02184b40` | 64 342 | Décompilation C complète (`src/overlays/overlay_0002.c`) |
| **Total** | | | **279 930** | **7 140 fonctions décompilées, 0 échec** |

---

## 2. Ressources 3D (100 % Extraites)

| Catégorie | Format / Source | Nombre | Format Extrait & Converti | Remarques |
|---|---|---|---|---|
| Modèles de Monstres | `.nsbmd` + `.nsbtx` | 210 | `.gltf` + `.bin` + PNG / Blender `.blend` | Couverture totale des 210 espèces distinctes du bestiaire |
| Modèles de Personnages | `.nsbmd` + `.nsbtx` | 18 | `.gltf` + `.bin` + PNG / Blender `.blend` | Héros, rivaux, dresseurs et PNJ majeurs (`n001` à `n022`) |
| Cartes du Monde | `.map` (Archives FPK) | 90 | `.glb` (Mondes 3D) + métadonnées | 90 cartes complètes d'îles, grottes, sanctuaires et intérieurs |
| Arènes de Combat | `.nsbmd` / `.map` | 83 | `.glb` + métadonnées | 83 arènes de combat 3D authentiques (`bf*`, `bd*`, `bh*`, `be*`) |
| Animations Squelettiques | `.nsbca` | 1 107 | Clips d'animation glTF | Animations officielles au combat et sur le terrain |
| Variantes de Modèles | Maillage partagé + texture | 28 | glTF + substitution texture PNG | Géométrie de sommets identique vérifiée |

---

## 3. Ressources 2D et Graphismes (100 % Extraits)

| Catégorie | Fichier Source | Nombre | Format | État |
|---|---|---|---|---|
| Icônes Pixel Art Monstres | `sd_*.dma` + `.pal` | 210 | PNG 24x24 / 32x32 | 210 icônes pixel-art officielles du bestiaire |
| Icônes de Boss | `sd_*.dma` + `.pal` | 13 | PNG | Icônes d'interface des combats de boss |
| Artworks Plein Écran | `dm_pic_*.d16` | 40 | PNG 256x192 (RGB555) | Illustrations de prologue, épilogue et cinématiques |
| Minicartes Écran Inférieur | `.CHR` / `.SCR` / `.PAL` | 60 | PNG 256x192 | Minicartes 2D décodées avec palettes VRAM matérielles |
| Arrière-Plans d'Interface | `wall_*.bin` | 7 | PNG 256x192 | Décors de menus (Banque, Autel de synthèse, Enclos) |
| Icônes Officielles de Familles | Tuiles d'interface | 8 | PNG 250x250 transparents | Gluant, Dragon, Nature, Bête, Matière, Démon, Mort-vivant, Incarnus |

---

## 4. Audio et Musiques (100 % Extraits & Reconstitués)

| Type Audio | Source ROM | Nombre | Format & Qualité | État / Vérification |
|---|---|---|---|---|
| Musiques BGM | `sound_data.sdat` (SSEQ) | 25 | MP3 320 kbps (Qualité studio) | Rendues depuis les banques d'instruments SWAR ; bouclage naturel |
| Bruitages SFX | `sound_data.sdat` (STRM + SSEQ) | 292 | MP3 320 kbps | Sorts, frappes physiques, alertes système, sons de terrain |
| Jingles & Fanfares (ME) | `sound_data.sdat` (STRM / SSEQ) | 19 | MP3 320 kbps | Fanfares d'événements (Victoire, Sanctuaire, Quêtes) |
| Échantillons d'Instruments | `sound_data.sdat` (SWAR) | 404 | WAV (ADPCM / PCM16) | Échantillons bruts du synthétiseur matériel |

---

## 5. Données de Jeu et Formules Décodées (Prouvées)

- **Statistiques de Niveau 1** (`EnmyKindTbl.bin`) : Statistiques de base de niveau 1 prouvées par l'ARM9 (`0x0203a640` et `0x0203db00`) aux offsets 22..27 ; plafonds de caractéristiques aux offsets 28..39.
- **Formule de Synthèse** (`overlay_0000:FUN_0218bee8`) : Moteur de reproduction à 2 parents, matrice de mélange des familles et 16 recettes quadrilinéaires à 4 parents.
- **Formule de Dressage** (`overlay_0001:0x92924`) : Taux de capture de base, impact de la tension (5/20/50/100), sort Décuplo et immunité des boss.
- **Profils d'IA de Combat** (`AI_PatternTbl.bin`, `AI_ActionTBL.bin`, etc.) : 131 patrons comportementaux, 256 actions répertoriées, tactiques d'équipe.
- **Rencontres Sauvages & Météo** (66 fichiers `.enct`) : 105 espèces sauvages cartographiées avec indicateurs Jour, Nuit et Pluie/Tempête.
- **Coffres 3D Physiques** (opcode `.evt` `0x5f` + `.pos`) : 76 coffres situés avec coordonnées réelles X, Y, Z, yaw, tiers A/B/C et probabilités de piège Canniboîte/Imitateur.
- **Cinématiques et Dialogues** (`demoNNN.bin` + `.evt`) : 244 scripts cinématiques, 644 plans de caméras (virgule fixe 20.12), 4 971 répliques authentiques alignées en 5 langues (EN, FR, DE, IT, ES).
- **Équipes de Dresseurs** : 158 équipes décodées dans `MstrPtnTbl.bin` et `FldMstrPrm.bin`, dont les 21 dresseurs itinérants.

---

## 6. Ce qui Reste Incomplet, Non Prouvé ou en Cours de Recherche

| Sujet de Recherche | Fichiers Ciblés | Statut Actuel | Ce qui Manque / Zone d'Ombre |
|---|---|---|---|
| Points de Compétence par Niveau | `SkillPointTbl.bin` / `overlay_0001` | Non prouvé | La fonction reliant la montée en niveau d'un monstre aux points de compétence attribués n'est pas encore identifiée dans l'assembleur. |
| Matrice Complète des Dégâts | `DamageTbl.bin` (2 048 o), `DamageItemTbl.bin` | Partiel | Les chargeurs sont identifiés, mais l'indexation de la matrice dans `overlay_0001` doit être décompilée pour obtenir 100 % des formules exactes. |
| Multiplicateur de Tension au Combat | Routines de combat `overlay_0001` | Incertain | Les multiplicateurs de tension pour le dressage sont prouvés (x1.4 à x2.5), mais les ratios de combat (signalés x1.7 à x7.5) doivent être vérifiés dans le code de calcul des dégâts. |
| Octets Résiduels des Boss | `BtlEnmyPrm.bin` (offsets `+0x00..0x07`, `+0x20..0x2F`) | Non assignés | Environ 39 octets par entrée ennemie dans `BtlEnmyPrm` ne sont pas documentés ; des surcharges de résistance propres aux boss pourraient s'y trouver. |
| Rattachement Direct des Noms de Cartes | `mes_mapname.bin` | Inféré | Les noms de cartes sont déduits par les points de passage et l'ordre des fichiers ; l'adresse en mémoire où la table est indexée n'est pas confirmée. |
| Avatars des PNJ de Casino | Scripts `k001.evt`, `f020.evt` (opcode `0x62`) | Non résolu | 14 PNJ de casino (Alba, Croupiers...) utilisent des variables RAM dynamiques pour leur apparition, rendant le lien vers leur modèle 3D impossible à déduire statiquement. |
