#!/usr/bin/env python3
"""Extrait les surnoms aléatoires attribués à un monstre recruté depuis
`mes_random_monster_name.binE`/`.binF` — item 28 de docs/DATA_RESEARCH_PLAN.md
du projet bestiaire.

## Provenance et niveau de confiance (session du 2026-09-25, suite 18)

Extraction directe (même `decode()` que les autres banques `mes_*.bin`, pas
de format binaire à percer). Structure : 4 surnoms consécutifs par espèce,
indexés par `species_id - 1` (species_id 1 = Gluant → bloc 0). Confirmé par
recoupement indépendant avec une trivia déjà connue du wiki (citée dans
docs/PLAN.md, item "Trivia" de la fiche Slime) : "The slime only has three
nicknames instead of the usual four, because the nickname 'Slimer' appears
twice, replacing 'Slimey' that should be present instead" — exactement ce
qu'on trouve au bloc 0 (`['Slimer', 'Slimer', 'Slimo', 'Mr Slim']`, le
doublon "Slimer" au lieu d'un 4e nom distinct). Coïncidence exclue vu la
précision du détail (une espèce précise, un nom précis dupliqué).
"""
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
sys.path.insert(0, os.path.join(RACINE, "tools"))
from extraire_mapping import decode  # noqa: E402

NICKNAMES_PER_SPECIES = 4


def load_names(filename):
    with open(os.path.join(DATA, filename), "rb") as f:
        raw = f.read()
    return [x.strip() for x in decode(raw).split("|")]


def main():
    names_en = load_names("mes_random_monster_name.binE")
    names_fr = load_names("mes_random_monster_name.binF")
    # Vérifié : les deux banques sont strictement identiques octet pour octet
    # (0/1405 entrées différentes) — le jeu ne traduit pas ces surnoms à
    # jeux de mots (mêmes noms en EN et FR). Un seul champ publié, pas deux
    # champs qui laisseraient croire à une traduction qui n'existe pas.
    assert names_en == names_fr, "les banques EN/FR ont divergé, à ré-investiguer"

    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    by_species_id = {e["monster_id"]: e["id"] for e in mapping.values() if e["id"].startswith("m")}

    result = {}
    max_species = len(names_en) // NICKNAMES_PER_SPECIES
    for species_id in range(1, max_species + 1):
        monster_id = by_species_id.get(species_id)
        if not monster_id:
            continue
        base = (species_id - 1) * NICKNAMES_PER_SPECIES
        names = [n for n in names_en[base : base + NICKNAMES_PER_SPECIES] if n]
        if names:
            result[monster_id] = names

    out_file = os.path.join(RACINE, "tools/monster_nicknames.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print(f"Monstres avec surnoms : {len(result)} / {max_species} slots d'espèce")


if __name__ == "__main__":
    main()
