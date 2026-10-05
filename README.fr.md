# Dragon Quest Monsters: Joker — Décompilation Intégrale & Rétro-Ingénierie

<p align="center">
  <img src="https://dqmj1.wiki/api/assets/images/logo.png" alt="Dragon Quest Monsters: Joker Logo" width="460" />
</p>

[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)](LICENSE)
[![Cible Matérielle](https://img.shields.io/badge/Cible-Nintendo%20DS%20%7C%20ARMv5TE%20%2B%20ARMv4T-informational.svg)]()
[![Taux de Décompilation](https://img.shields.io/badge/D%C3%A9compilation-100%25%20%287%20140%20fonctions%29-success.svg)]()
[![Base de Code](https://img.shields.io/badge/Code%20C%20reconstruit-279k%20lignes-blue.svg)]()
[![Désassemblage & Outils](https://img.shields.io/badge/Analyse-Ghidra%20Headless%20%7C%20objdump-orange.svg)]()
[![Formats Propriétaires](https://img.shields.io/badge/D%C3%A9codeurs-SDAT%20%7C%20NSBMD%20%7C%20D16%20%7C%20FPK%20%7C%20EVT-purple.svg)]()
[![Multilingue](https://img.shields.io/badge/Localisation-5%20Langues%20%28EN%2FFR%2FDE%2FIT%2FES%29-teal.svg)]()
[![Wiki Compagnon](https://img.shields.io/badge/Wiki%20en%20ligne-dqmj1.wiki-blueviolet.svg?style=flat)](https://dqmj1.wiki/)

Projet complet de rétro-ingénierie avancée, analyse de bytecode et décompilation C pour **Dragon Quest Monsters: Joker** (Nintendo DS, version européenne `NTR-AJRP-EUR`).

Ce dépôt illustre une démarche complète de reverse engineering bas niveau : dissection de protocoles binaires propriétaires, automatisation de décompilation sur architectures asynchrones à mémoire partagée, et restitution fidèle du patrimoine logiciel.

> **English Documentation / Documentation en anglais :**
> - [Technical Overview & Getting Started (README.md)](README.md)
> - [Extracted Assets Inventory & Research Status (docs/WHAT_IS_DONE.md)](docs/WHAT_IS_DONE.md)
> - [Contributing Guidelines (CONTRIBUTING.md)](CONTRIBUTING.md)
> - [Code of Conduct (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md)


---

## Wiki 3D interactif compagnon : [dqmj1.wiki](https://dqmj1.wiki/)

Toutes les données, formules et ressources extraites dans ce dépôt alimentent directement l'encyclopédie web et le compendium 3D en production : **[https://dqmj1.wiki](https://dqmj1.wiki/)** (Page dédiée au projet sur le wiki : [dqmj1.wiki/github](https://dqmj1.wiki/github)).

Modules interactifs alimentés par la décompilation :
- **[Bestiaire 3D des monstres](https://dqmj1.wiki/)** : Rendu WebGL temps réel des 210 monstres, 6 animations officielles, plafonds et statistiques de base.
- **[Simulateur interactif de synthèse](https://dqmj1.wiki/synthese)** : Arbre React Flow et moteur de fusion 2 parents fidèle à la routine `FUN_0218bee8`.
- **[Recherche inversée de synthèse](https://dqmj1.wiki/synthese/recherche)** : Calcul de lignées optimales, recettes quadrilinéaires à 4 parents et formes d'Incarnus.
- **[Cartes 3D & minicartes](https://dqmj1.wiki/maps)** : 90 cartes 3D interactives, coordonnées réelles des coffres, collisions physiques et minicartes officielles.
- **[Calculateur de dégâts & Arène](https://dqmj1.wiki/degats)** : Formules de combat authentiques (`DamageTbl.bin`), paliers de sagesse, tension et simulateur d'arène.
- **[Studio audio & musiques](https://dqmj1.wiki/musiques)** : 25 thèmes de Koichi Sugiyama et 292 bruitages SFX resynthétisés depuis les séquences SSEQ.
- **[API REST ouverte (v1)](https://dqmj1.wiki/api)** : Accès programmatique libre, gratuit et sans clé d'API à l'ensemble du jeu de données.

> **Infrastructure & Auto-Hébergement Communautaire :**
> Le site compagnon en ligne, l'API REST publique et l'infrastructure de téléchargement des assets 3D sont intégralement auto-hébergés sur des serveurs physiques dédiés mis à disposition par **FantasmaGlad**. La bande passante très haut débit, le stockage NVMe haute capacité et la disponibilité continue sont offerts sans aucune contrepartie financière, sans publicité et sans abonnement, au bénéfice de l'ensemble de la communauté Dragon Quest et des chercheurs en rétro-ingénierie.


---

## Vue d'Ensemble du Projet

- **100 % du code décompilé** : 7 140 fonctions intégralement décompilées en 279 930 lignes de pseudo-C à travers l'ARM9, l'ARM7 et les 3 overlays dynamiques.
- **Architecture mémoire authentique** : Adresses de chargement fixes vérifiées (`0x02000000` pour l'ARM9, `0x02184b40` pour les overlays 0/1/2) avec résolution des pointeurs absolus.
- **Suite d'outillage sur mesure** :
  - Modèles 3D et squelettes d'animation (`.nsbmd`, `.nsbca`, `.nsbtx`) convertis vers glTF et scènes Blender `.blend`.
  - Synthèse et restitution des séquences audio officielles (`.sdat`, `.sseq`, `.swar`, `.sbnk`) en WAV et MP3 320 kbps.
  - Graphismes 2D (`.d16` BGR555, tuiles et palettes `.CHR`/`.SCR`/`.PAL`) décodés en PNG.
  - Scripts d'événements (`.evt` bytecode TLV) et cinématiques (`demoNNN.bin` / `.pos`).
- **Formules & Mécaniques de jeu** : Moteur de synthèse (formule canonique `FUN_0218bee8`), caractéristiques de base niveau 1 de la ROM, courbes de croissance, résistances élémentaires, équipes de dresseurs et tables de décision tactique de l'IA (`AI_*.bin`).

---

---

## Modèle 3D animé de référence : Wulfspade (No. 336 / m176)

Afin d'illustrer la fidélité de notre chaîne de conversion 3D et de réextraction squelettique sans exiger d'extraction préalable, le dépôt intègre l'actif de production complet de **Wulfspade** (*Apik*, Espèce n° 336, identifiant interne `m176`) :

- **Emplacement** : [`assets/models/wulfspade_m176/`](assets/models/wulfspade_m176/)
- **Formats inclus** :
  - `m176.glb` : Format glTF binaire autonome intégrant le maillage, le squelette 28 os, la pondération de sommet, la texture diffuse et 10 animations.
  - `m176.gltf` + `m176.bin` + `m176_1.png` : Format glTF 2.0 textuel décomposé.
- **Animations incluses** : Pose de combat, repos terrain, cycle de course, frappe physique, incantation magique, coup léger, projection lourde, défaite, cri de victoire et garde alternative.
- **Compatibilité** : Conforme au standard glTF 2.0 / GLB, immédiatement importable dans Blender, three.js, Godot ou Unity.

## Compétences Techniques & Valeur Ingénierie

Ce projet met en valeur des compétences pointues en programmation système, rétro-ingénierie logicielle et traitement de données bas niveau :

- **Analyse Binaire Statique & Assembleur ARM** :
  - Rétro-ingénierie approfondie des jeux d'instructions ARMv5TE (ARM946E-S) et ARMv4T (ARM7TDMI).
  - Traitement du basculement d'état ARM (32 bits) / Thumb (16 bits) sans artefact de désassemblage.
  - Automatisation sous Ghidra Headless (`Java`) pour la détection de structures, le pistage des références croisées (Xrefs) et l'exportation C à grande échelle.
- **Dissection de Protocoles & Formats Propriétaires** :
  - Décodage bit-à-bit d'architectures de fichiers non documentées : conteneurs FPK, matrices de caméras POS (arithmétique en virgule fixe 20.12) et interpréteurs bytecode Tag-Length-Value (TLV) `.evt`.
  - Restitution sonore matérielle : désassemblage des commandes de séquences Nitro SDAT (événements, boucles, horloges de tempo) et extraction des banques multi-échantillons ADPCM / PCM16 SWAR.
- **Architecture Embarquée & Gestion de la Mémoire** :
  - Reconstitution d'une topologie multi-overlay partageant les mêmes adresses physiques en RAM (`0x02184b40`).
  - Analyse des segments mémoire : dissociation rigoureuse des sections `.data`, `.rodata`, pools littéraux et segments non initialisés `.bss`.
- **Rigueur Industrielle & Automatisation** :
  - Chaînes de traitement déterministes en Python et Bash : pipelines d'extraction reproductibles générant des jeux de données JSON fortement typés à partir des tables binaires brutes (`EnmyKindTbl`, `ItemTbl`, `SkillTbl`).


---

## Architecture Cible : Nintendo DS

La Nintendo DS fonctionne autour de deux processeurs asynchrones avec mémoire partagée :

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
|   |  MOTEUR DU JEU : |             |  GESTION MATÉRIEL: |   |
|   |  - Rendu 3D      |             |  - Mixeur audio    |   |
|   |  - Gameplay      |             |  - Wi-Fi           |   |
|   |  - IA de combat  |             |  - Écran tactile   |   |
|   |  - Scripts monde |             |  - Horloge / RTC   |   |
|   +--------+---------+             +---------+----------+   |
|            |                                 |              |
|            +---------------+-----------------+              |
|                            |                                |
|                   +--------v--------+                       |
|                   |    4 Mo RAM     |  (Partagée)           |
|                   +-----------------+                       |
+-------------------------------------------------------------+
```

### Cartographie Mémoire (Adresses Vérifiées)

| Module Binaire | Adresse Base | Point d'Entrée | Taille | Rôle |
|---|---|---|---|---|
| `arm9.bin` | `0x02000000` | `0x02000800` | 492 576 octets | Moteur principal, physique, machines d'états, scripts |
| `arm7.bin` | `0x02380000` | `0x02380000` | 157 660 octets | Gestionnaire matériel, audio, RTC |
| `overlay_0000.bin` | `0x02184b40` | Dynamique | 378 912 octets | Menus, moteur de synthèse (`FUN_0218bee8`), inventaire |
| `overlay_0001.bin` | `0x02184b40` | Dynamique | 618 112 octets | Système de combat au tour par tour, formules, IA des monstres |
| `overlay_0002.bin` | `0x02184b40` | Dynamique | 480 736 octets | Communications sans fil, arènes |

---

## Documentation Complète

- [Guide complet de A à Z (docs/fr/GUIDE_COMPLET.md)](docs/fr/GUIDE_COMPLET.md)
- [Guide d'extraction des ressources (docs/fr/EXTRACTION_RESSOURCES.md)](docs/fr/EXTRACTION_RESSOURCES.md)
- [Guide de démarrage rapide (docs/fr/GUIDE_DEMARRAGE.md)](docs/fr/GUIDE_DEMARRAGE.md)

---

## Commandes et Outils

```bash
# Synthèse des monstres
python3 tools/extract_synthesis.py

# Statistiques de base niveau 1 et plafonds
python3 tools/extract_monster_stats.py

# Profils et arbres décisionnels d'IA de combat
python3 tools/extract_battle_ai.py

# Coffres 3D et coordonnées physiques
python3 tools/extract_chests_3d.py

# Rendu audio SSEQ vers MP3
python3 tools/render_sseq_audio.py
```

---

## Cadre Légal

Projet d'étude technique et de préservation patrimoniale mené à des fins d'interopérabilité. Dragon Quest et Dragon Quest Monsters: Joker sont des marques déposées et propriétés exclusives de Square Enix Co., Ltd. et Armor Project.
