#!/usr/bin/env python3
"""Extrait les descriptions (bestiaire in-game) depuis mes_know.binE.

Découverte de session (2026-09-24) : l'index d'un item dans mes_know.binE
correspond exactement à `monster_id` tel que défini dans mapping_monstres.json
(pas de décalage, contrairement à la table des noms qui utilise +64). Vérifié
sur les 213 entrées de mapping_monstres.json : couverture 100%, zéro
placeholder "THIS IS A BUG", correspondance sémantique cohérente pour
l'intégralité de l'échantillon (ex. monster_id=1 -> Gluant/Slime -> "soft skin
and a silly smile").

Réutilise le décodeur de texte de extract_mapping.py (encodage propriétaire
DS de ce jeu). Ce décodeur a été calibré sur des noms courts ; certains octets
de ponctuation dans les phrases longues (mes_know contient de vraies phrases,
pas juste des noms) peuvent rester imparfaitement décodés (ex. l'apostrophe
`'` sert à la fois de guillemet et, probablement, de point final scindé — non
résolu ici, affiché tel quel plutôt que deviné) : les balises `<XX>` restantes
dans la sortie sont des octets non mappés (contrôles de mise en forme /
substitutions de variable in-game), volontairement laissées visibles plutôt
que supprimées ou interprétées au hasard.
"""
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

sys.path.insert(0, os.path.join(RACINE, "tools"))
from extract_mapping import decode  # noqa: E402


def main():
    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)

    with open(os.path.join(DATA, "mes_know.binE"), "rb") as f:
        raw = f.read()
    items = [x.strip() for x in decode(raw).split("|")]

    descriptions = {}
    missing = []
    for monster_id_str, entry in mapping.items():
        monster_id = entry["monster_id"]
        if monster_id >= len(items):
            missing.append(entry["id"])
            continue
        text = items[monster_id]
        if not text or "BUG" in text:
            missing.append(entry["id"])
            continue
        descriptions[entry["id"]] = {
            "id": entry["id"],
            "monster_id": monster_id,
            "description_en": text,
        }

    out_file = os.path.join(RACINE, "tools/monster_descriptions.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=2, ensure_ascii=False)

    print(f"Descriptions saved: {len(descriptions)} / {len(mapping)} monsters.")
    if missing:
        print(f"Sans description (id absent/placeholder) : {missing}")


if __name__ == "__main__":
    main()
