#!/usr/bin/env python3
"""Extrait résistances élémentaires/altérations de statut et traits passifs
par monstre depuis l'infobox du wiki communautaire DQMJ (Fandom).

## Provenance et niveau de confiance (session du 2026-09-25, suite 15)

Source : les mêmes 210 pages en cache (`work/extracted/data/wiki_cache/pages/`,
téléchargées pour `extract_growth_curves.py`, `action=parse&prop=wikitext`,
aucune nouvelle requête réseau pour ce script). Champs `res1`-`res5` et
`trait1`-`trait2` de `{{Infobox monster}}`.

**Pourquoi publier une donnée non désassemblée, non confirmée par la ROM** :
demandé par le propriétaire (2026-09-25, "Liste 100% des types de données...
qui mériteraient d'être dans le wiki" puis "Go" sur l'item "Éléments/altérations
de statut : 27 libellés textuels connus, valeurs par monstre introuvables").
Aucune table de résistances par monstre n'a été localisée dans la ROM à ce
jour (voir item 4 de docs/DATA_RESEARCH_PLAN.md) — seuls les 27 LIBELLÉS
existent dans `mes_taisei.binE`, pas les valeurs. Élément de corroboration
fort (pas une confirmation par désassemblage, mais pas une simple confiance
aveugle envers le wiki non plus) : les valeurs de résistance de ce wiki
utilisent EXACTEMENT les gabarits de phrase trouvés indépendamment dans
`mes_taisei.binE` ("Xproof", "Vulnerable to X", "Healed by X") — cohérence
interne avec la ROM, sans être une preuve absolue.

**Traits** : mécanique de jeu (capacité passive, 0 à 2 par monstre) qui
n'existait dans AUCUNE donnée publiée par ce projet avant cette session — pas
de piste ROM identifiée du tout pour cette donnée, uniquement sourcée wiki.

Champs vides (`''`) traités comme "aucune résistance"/"aucun second trait" —
jamais remplacés par une valeur inventée.
"""
import json
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_CACHE = os.path.join(RACINE, "work/extracted/data/wiki_cache/pages")

NAME_FIXES = {
    "dr snapped": "dr. snapped",
}


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9_-]", "_", name) + ".json"


def parse_infobox_list_field(wikitext, prefix, count):
    values = []
    for i in range(1, count + 1):
        m = re.search(prefix + str(i) + r"\s*=\s*([^\n|]*)", wikitext)
        value = m.group(1).strip() if m else ""
        if value:
            values.append(value)
    return values


def main():
    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    by_name_en = {}
    for e in mapping.values():
        if e["id"].startswith("m"):
            by_name_en[e["nom_en"].strip().lower()] = e["id"]

    # Même liste de noms wiki que extract_growth_curves.py (Module:Growth/monster growth)
    with open(
        os.path.join(RACINE, "work/extracted/data/wiki_cache/Module_Growth_monster_growth.json"),
        encoding="utf-8",
    ) as f:
        growth_cache = json.load(f)
    lua = list(growth_cache["query"]["pages"].values())[0]["revisions"][0]["*"]
    names = re.findall(r'monsters\["([^"]+)"\]', lua)

    result = {}
    unmatched = []
    no_page = []
    for name in names:
        key = NAME_FIXES.get(name.strip().lower(), name.strip().lower())
        monster_id = by_name_en.get(key)
        if not monster_id:
            unmatched.append(name)
            continue
        path = os.path.join(PAGES_CACHE, safe_filename(name))
        if not os.path.exists(path):
            no_page.append(name)
            continue
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        if "parse" not in payload:
            no_page.append(name)
            continue
        wikitext = payload["parse"]["wikitext"]["*"]
        resistances = parse_infobox_list_field(wikitext, r"\|res", 5)
        traits = parse_infobox_list_field(wikitext, r"\|trait", 2)
        result[monster_id] = {"resistances": resistances, "traits": traits}

    out_file = os.path.join(RACINE, "tools/monster_resistances_traits.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    with_res = sum(1 for v in result.values() if v["resistances"])
    with_traits = sum(1 for v in result.values() if v["traits"])
    print(f"Monstres traités : {len(result)}")
    print(f"Avec au moins 1 résistance : {with_res}")
    print(f"Avec au moins 1 trait : {with_traits}")
    print(f"Non appariés à un id : {unmatched}")
    print(f"Sans page en cache : {no_page}")


if __name__ == "__main__":
    main()
