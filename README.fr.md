# Dragon Quest Monsters: Joker — Rétro-ingénierie ROM & Reconstruction du Code Source

<p align="center">
  <img src="https://dqmj1.wiki/api/assets/images/logo.png" alt="Dragon Quest Monsters: Joker Logo" width="440" />
</p>

[![Licence: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plateforme](https://img.shields.io/badge/Cible-Nintendo%20DS%20%7C%20ARMv5TE%20%2B%20ARMv4T-informational.svg)]()
[![Base de décompilation](https://img.shields.io/badge/Base%20Ghidra-100%25%20%287%2C140%20fonctions%29-blue.svg)]()
[![Reconstruction C](https://img.shields.io/badge/Reconstruction%20C-En%20cours-orange.svg)]()
[![Parsers personnalisés](https://img.shields.io/badge/Parsers-SDAT%20%7C%20NSBMD%20%7C%20D16%20%7C%20FPK%20%7C%20EVT-purple.svg)]()
[![Compendium compagnon](https://img.shields.io/badge/Compendium%20Compagnon-dqmj1.wiki-blueviolet.svg?style=flat)](https://dqmj1.wiki/)

Projet de rétro-ingénierie technique, dissection des formats binaires et reconstruction progressive du code source C pour **Dragon Quest Monsters: Joker** (Nintendo DS, version européenne `NTR-AJRP-EUR`).

L'ensemble des algorithmes, formules et modèles extraits alimente directement l'encyclopédie web et le compendium 3D : **[https://dqmj1.wiki](https://dqmj1.wiki/)**.

> - **English Documentation** : [Main Guide (README.md)](README.md)
> - **Matrice de complétion** : [Treemap d'avancement (docs/COMPLETION_MAP.md)](docs/COMPLETION_MAP.md)
> - **Guide de matching** : [Standards de décompilation C (docs/MATCHING_GUIDE.md)](docs/MATCHING_GUIDE.md)

---

## Matrice de complétion de la décompilation

Poids proportionnel des modules et avancement de l'analyse des sous-systèmes :

![Treemap de Décompilation](docs/assets/completion_treemap.svg)

> Détail technique complet des fonctions et symboles : **[docs/COMPLETION_MAP.md](docs/COMPLETION_MAP.md)**

---

## Structure du Dépôt

| Répertoire | Description |
| :--- | :--- |
| **`include/`** | Types standards C (`types.h`), registres d'E/S matériels (`nds/`) et structures du jeu (`game/`). |
| **`src/`** | Modules C matchés canoniques (`src/synthesis/`, `src/battle/`, `src/kernel/`) et bases de référence du décompilateur. |
| **`tools/`** | Chaîne d'outils d'extraction Python et Bash (modèles 3D, audio SDAT/SSEQ, graphismes 2D, scripts EVT et tables binaires). |
| **`docs/`** | Documentation technique, architecture mémoire, inventaires d'actifs et matrices d'avancement. |
| **`assets/`** | Jeux de données de référence, tables JSON vérifiées et modèle 3D glTF d'exemple ([Apik / Wulfspade `m176`](assets/models/wulfspade_m176/)). |
| **`work/`** | Cartographies de désassemblage, références croisées de symboles et analyse mémoire. |

---

## Comment Contribuer

Les contributions des rétro-ingénieurs, hackeurs de ROM et passionnés de Dragon Quest sont les bienvenues :

1. **Identification de symboles** : Aider à nommer et typer les fonctions de la base Ghidra (`FUN_xxxxxxxx` -> noms sémantiques).
2. **Formats de fichiers** : Améliorer les parsers pour les opcodes EVT résiduels, trajectoires de caméra et tables d'apparition.
3. **Chaîne de compilation** : Contribuer à la configuration de recompilation byte-matching (MetroWerks CodeWarrior DS).

Consultez **[CONTRIBUTING.md](CONTRIBUTING.md)** et **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** avant de soumettre une pull request.

---

## Remerciements & Attributions

- **[Projet Apicula](https://github.com/scurest/apicula)** : Nos décodeurs de modèles 3D (`.nsbmd`, `.nsbtx`, `.nsbca`) s'appuient sur les recherches et spécifications établies par Apicula.
- **[Bubelia](https://dqmj.fandom.com/wiki/Dragon_Quest_Monsters:_Joker_Wiki)** : Fondateur et auteur du wiki populaire Dragon Quest Monsters: Joker sur Fandom ; croisement technique entre données ROM et wikis communautaires, revue de l'architecture de décompilation et conseils d'implémentation.
- **Bonnford** : Revue approfondie des données de jeu, fidélité au scénario et mécaniques de synthèse de l'Incarnus.
- **[Dragon Quest Wiki](https://dragon-quest.org/) & [Fandom Wiki](https://dragonquest.fandom.com/)** : Éditeurs bénévoles pour leur travail d'archivage de longue date.
- **[Ghidra](https://ghidra-sre.org/)** : Framework de rétro-ingénierie pour l'analyse binaire et la génération de la base de décompilation.

---

## Cadre Légal

Projet d'étude technique et de préservation patrimoniale mené à des fins d'interopérabilité. Dragon Quest et Dragon Quest Monsters: Joker sont des marques déposées et propriétés exclusives de Square Enix Co., Ltd. et Armor Project.
