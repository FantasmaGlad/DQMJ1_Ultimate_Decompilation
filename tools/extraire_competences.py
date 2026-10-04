#!/usr/bin/env python3
"""Extrait le catalogue des compétences individuelles depuis SkillTbl.bin.

## Provenance et niveau de confiance (session du 2026-09-25)

Structure de fichier confirmée par arithmétique, même méthode que pour
`EnmyKindTbl.bin`/`BtlEnmyPrm.bin` : magique `"SKIL"` (offset 0-3) + u32
nombre d'entrées (offset 4-7) = 194, puis 194 entrées de **240 octets**
chacune — `(46568 - 8) / 194 = 240` tombe pile.

Les noms sont ceux de `mes_skillomitname.binE` (nom court/abrégé affiché en
combat, ex. "Frzz Bng"), décodés avec le même décodeur que
`extraire_descriptions.py`. Cette banque contient exactement **194 entrées**
elle aussi, et l'index 0 des deux fichiers est vide/réservé ("aucune
compétence") — correspondance 1:1 par index, pas de recoupement par nom
nécessaire.

**Ce script NE publie PAS l'interprétation des 240 octets internes de
`SkillTbl.bin`** (coût en MP, puissance, élément, cible, type d'effet...) :
aucun de ces offsets n'a été testé ni confirmé cette session. Seuls l'index
et le nom (donnée textuelle directe, pas une hypothèse) sont extraits ici,
conformément à la règle absolue n°2 (ne jamais publier de donnée devinée).

Reste à faire (voir `docs/DATA_RESEARCH_PLAN.md`) : décoder la structure des
240 octets par entrée, et surtout retrouver la table qui associe le champ
`skill_set` de chaque espèce (`EnmyKindTbl.bin`, voir
`extraire_stats_especes.py`) à un sous-ensemble de ces compétences (mécanique
d'"allocation de points de compétence" confirmée par le texte du jeu
`mes_haigou.binE`/`mes_command.binE`, mais table de correspondance non
identifiée) — sans cette table, il est impossible d'associer une compétence à
un monstre précis.

## Noms réels des compétences (session du 2026-09-25, suite 7)

`mes_skillomitname.binE` contient le nom **abrégé** ("omit name", utilisé dans
les menus de combat où la place est comptée, ex. "Frzz Bng") — confirmé par au
moins une entrée en toutes lettres dans la même banque ("Frizz Ward", index
154). Il n'existe **pas** de banque de texte séparée dans la ROM avec les noms
complets (vérifié : aucune banque `mes_*` ne contient "Frizzle"/"Kaboom" ou
toute autre orthographe complète d'un sort individuel).

Demande explicite du propriétaire (2026-09-25) : afficher le **nom réel**, pas
l'abréviation. Le nom réel de chacun des 192 panneaux de compétence a été
retrouvé en cross-référençant la liste complète de la catégorie "Dragon Quest
Monsters: Joker skill sets" du wiki communautaire dragon-quest.org (recherche
web autorisée par le propriétaire, même méthode que pour la table de fusion
famille — voir `docs/DATA_RESEARCH_PLAN.md`). Cette catégorie liste 122 pages
(certaines couvrant les 3 paliers d'un même panneau sur une seule page), pour
192 panneaux au total — nombre qui correspond exactement à celui déjà déduit
de `SkillTbl.bin`, forte corroboration croisée.

Découvertes clés de ce recoupement :

- `<8d>` / `<8e>` (octets de contrôle non mappés par le décodeur) sont des
  suffixes de **palier** : chaque panneau existe en 3 versions ("Frizz &
  Bang", "Frizz & Bang II", "Frizz & Bang III"), confirmé pour ce panneau
  précis par le wiki puis généralisé aux 33 autres triplettes de la table
  (même motif répété partout).
- `<55>` (préfixe répété sur 15 entrées) correspond au caractère **"Ü"** —
  ces 15 panneaux sont tous des "Über X" (ex. "Über Dark Dynamiter", "Über
  Blessed Blizzardier", "Über Windblast Ward") : une hypothèse antérieure de
  cette session ("Cyber X") s'est révélée fausse une fois confirmée par le
  wiki — corrigée ici.
- Les 4 panneaux "Slash" à noms opaques sont en réalité "Firewind Slashes",
  "Thunderwind Slashes", "Iceplosion Slashes" et "Darklight Slashes".
- "Cursader" (différent de "Crusader") est un panneau réel et distinct, pas
  une coquille de décodage.
- Irrégularités de nommage confirmées par le wiki (pas une déduction) :
  "Wisdom Booster" (pas "Wisdom Boost"), "Martial Artist" (pas "Martial
  Art"), "Dr. Snapped" (avec point).

Les noms ci-dessous sont donc **sourcés d'un wiki externe, pas du texte brut
du jeu** — badge de provenance affiché dans l'UI en conséquence (F6 du CDC).
Le nom abrégé original (`name_short_en`) reste conservé pour traçabilité.
"""
import json
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

sys.path.insert(0, os.path.join(RACINE, "tools"))
from extraire_mapping import decode  # noqa: E402

HEADER_SIZE = 8
ENTRY_SIZE = 240

TIER_SUFFIXES = {"<8d>": " II", "<8e>": " III"}

# Nom réel de chaque panneau (base, sans palier), retrouvé par recoupement
# avec dragon-quest.org (catégorie "Dragon Quest Monsters: Joker skill sets",
# 2026-09-25). Clé = nom abrégé brut de mes_skillomitname.binE une fois le
# suffixe de palier retiré.
REAL_NAMES = {
    "Frzz Bng": "Frizz & Bang",
    "Frzz Wsh": "Frizz & Woosh",
    "Frzz Zap": "Frizz & Zap",
    "Frzz Zam": "Frizz & Zam",
    "Bng Wsh": "Bang & Woosh",
    "Bng Crk": "Bang & Crack",
    "Bng Zap": "Bang & Zap",
    "Bng Zam": "Bang & Zam",
    "Wsh Crk": "Woosh & Crack",
    "Wsh Zap": "Woosh & Zap",
    "Wsh Zam": "Woosh & Zam",
    "Crk Zap": "Crack & Zap",
    "Crk Zam": "Crack & Zam",
    "Frwnd Slsh": "Firewind Slashes",
    "Thwnd Slsh": "Thunderwind Slashes",
    "Iceplo Slash": "Iceplosion Slashes",
    "Drkli Slash": "Darklight Slashes",
    "Wind Blowr": "Wind Blower",
    "Bnty Hunter": "Bounty Hunter",
    "Aquapthcary": "Aquapothecary",
    "Drgvn Lord": "Dragovian Lord",
    "WulfSp": "Wulfspade",
    "Rhapthrn": "Rhapthorne",
    "Dr Snapped": "Dr. Snapped",
    "Atk Boost": "Attack Boost",
    "Def Boost": "Defense Boost",
    "Agi Boost": "Agility Boost",
    "Wis Boost": "Wisdom Booster",
    "Thundr Wrd": "Thunder Ward",
    "Fire Br Wrd": "Fire Breath Ward",
    "Ice Br Wrd": "Ice Breath Ward",
    "Dazzle Wrd": "Dazzle Ward",
    "Drain M Wrd": "Drain Magic Ward",
    "AntiMgc Wrd": "Antimagic Ward",
    "Gobstop Wrd": "Gobstopper Ward",
    "BnDnce Wrd": "Ban Dance Ward",
    "Conf Ward": "Confusion Ward",
    "Inact Ward": "Inaction Ward",
    "Paral Ward": "Paralysis Ward",
    "Martial Art": "Martial Artist",
    "<55>ber Drk Dyn": "Über Dark Dynamiter",
    "<55>ber Blss Blz": "Über Blessed Blizzardier",
    "<55>ber Mage": "Über Mage",
    "<55>ber Breath": "Über Breath",
    "<55>ber Knight": "Über Knight",
    "<55>ber Healer": "Über Healer",
    "<55> Helpful": "Über Helpful",
    "<55> Charmer": "Über Charmer",
    "<55> H Boost": "Über Health Boost",
    "<55> M Boost": "Über Magic Boost",
    "<55> Atk Boost": "Über Attack Boost",
    "<55> Def Boost": "Über Defense Boost",
    "<55> Agi Boost": "Über Agility Boost",
    "<55> Wis Boost": "Über Wisdom Boost",
    "<55> Heat Wrd": "Über Heat Ward",
    "<55> Cold Wrd": "Über Cold Ward",
    "<55> WdBl Wrd": "Über Windblast Ward",
    "<55> DrkLi Wrd": "Über Darklight Ward",
}


def clean_name(raw: str) -> str:
    """Retourne le nom réel (wiki) à partir du nom abrégé brut de la ROM."""
    name = raw
    tier_suffix = ""
    for code, suffix in TIER_SUFFIXES.items():
        if name.endswith(f" {code}"):
            name = name[: -len(f" {code}")]
            tier_suffix = suffix
            break
    name = REAL_NAMES.get(name, name)
    return name + tier_suffix


def main():
    with open(os.path.join(DATA, "SkillTbl.bin"), "rb") as f:
        skill_tbl = f.read()
    magic, count = struct.unpack_from("<4sI", skill_tbl, 0)
    assert magic == b"SKIL", magic
    expected_size = HEADER_SIZE + count * ENTRY_SIZE
    assert len(skill_tbl) == expected_size, (len(skill_tbl), expected_size)

    with open(os.path.join(DATA, "mes_skillomitname.binE"), "rb") as f:
        raw_names = f.read()
    names = [x.strip() for x in decode(raw_names).split("|")]
    assert len(names) == count, (len(names), count)

    skills = {}
    skipped_empty = 0
    for i in range(count):
        name = names[i]
        if not name:
            skipped_empty += 1
            continue
        display_name = clean_name(name)
        tier = 1
        for code, ordinal in (("<8d>", 2), ("<8e>", 3)):
            if name.endswith(f" {code}"):
                tier = ordinal
                break
        base_name = display_name[:-3] if tier == 2 else display_name[:-4] if tier == 3 else display_name
        skills[str(i)] = {
            "skill_id": i,
            "name_short_en": name,
            "name_display_en": display_name,
            "base_name": base_name,
            "tier": tier,
        }

    out_file = os.path.join(RACINE, "tools/skills.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2, ensure_ascii=False)

    print(f"Skills saved: {len(skills)} named entries.")
    print(f"Empty (no name) slots skipped: {skipped_empty}")


if __name__ == "__main__":
    main()
