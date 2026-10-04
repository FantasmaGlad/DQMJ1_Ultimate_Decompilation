#!/usr/bin/env python3
"""Extrait rang/famille/stats de base/skill_set depuis EnmyKindTbl.bin.

## Provenance et niveau de confiance (session du 2026-09-25)

Structure de fichier confirmée par arithmétique : magique "EKT\\0" (offset 0-3)
+ u32 nombre d'entrées (offset 4-7) = 352, puis 352 entrées de **136 octets**
chacune — `(len(EnmyKindTbl.bin) - 8) / 352 = 136` tombe pile.

Les offsets ci-dessous reprennent l'ORDRE de champs transcrit depuis Data
Crystal (ROM map DQMJ1), mais **PAS sa taille totale** (148 o, fausse — on
utilise 136 o, confirmée par le fichier réel). L'erreur de Data Crystal ne
semble affecter que le dernier champ ("unknown" de fin, 63 o réels au lieu de
75 annoncés) : tous les offsets AVANT ce champ de fin restent donc plausibles
et ont été validés statistiquement sur l'ensemble des 352 entrées :

- `rank_and_family` (offset 4, un octet) : nibble haut = famille, nibble bas
  = rang. Vérifié : 210 des 213 monstres nommés dans mapping_monstres.json
  ont une valeur non nulle ; 102 des 103 entrées à 0 correspondent à des ids
  SANS nom connu (emplacements vides/non utilisés) — signal net et cohérent
  sur l'ensemble du fichier, pas un cas isolé.
- Familles observées : 9 valeurs distinctes (dont 0 = vide/inutilisé), donc 8
  familles réelles. Rangs observés : 10 valeurs distinctes (dont 0 = vide),
  donc 9 rangs réels — PAS encore fait le lien avec les lettres F à X
  utilisées par la communauté DQM, ce lien reste à établir (ne pas deviner
  quel nombre correspond à quelle lettre sans confirmation).
- CORRECTION 2026-09-26 : les six stats aux offsets 28-39 sont des PLAFONDS (six u16), prouves par
  desassemblage (FUN_021c4f98) ; il n'y a aucune stat de base dans cette table.
- `skill_set` (offset 72, un octet) : cohérent avec le regroupement par
  famille (les Gluants "métal" partagent une valeur différente des Gluants
  normaux).

**Validation statistique forte, pas de désassemblage confirmé.** Champs
"traits", "weapon_compatibility" et autres du reste de la struct Data Crystal
(avant l'offset 28) ne sont PAS extraits ici : leurs offsets n'ont pas été
testés/validés cette session, ne pas les deviner.

## Lettres de rang (session du 2026-09-25, suite)

Les lettres de rang F/E/D/C/B/A/S/X (dans cet ordre croissant de puissance)
ont été retrouvées **littéralement dans le texte du jeu**, à deux endroits
indépendants qui donnent la même séquence dans le même ordre :
`mes_command.binE` (indices 20-27) et `mes_gparts.binE` (indices 24-31, écran
d'affichage compact de fiche monstre — juste après le libellé `"Rank"` à
l'indice 14). Ce n'est donc pas une supposition externe (wiki communautaire)
mais une lecture directe du texte embarqué dans la ROM.

Seulement **8 lettres** existent dans ces deux banques, alors que le champ
`rank` de `EnmyKindTbl.bin` prend **9 valeurs non nulles** (1 à 9). La
correspondance 1→F, 2→E, ..., 8→X (ordre croissant, cohérent avec Gluant/m000
en rang 1 = F, le rang de départ le plus bas de la série) est publiée
ci-dessous. Le rang **9** (10 monstres seulement, le groupe le plus rare, et
qui contient Trode d'après `docs/PLAN.md`) n'a **aucune lettre confirmée** :
hypothèse non publiée comme un fait — probablement une valeur sentinelle
réservée aux monstres uniques/scénaristiques plutôt qu'un 9e rang réel au-delà
de X, mais ceci reste une hypothèse, affichée comme telle dans l'UI (rang 9 =
badge "non mappé", jamais une lettre inventée).
"""

RANK_LETTERS = {
    1: "F",
    2: "E",
    3: "D",
    4: "C",
    5: "B",
    6: "A",
    7: "S",
    8: "X",
}

## Noms de famille (session du 2026-09-25, suite 7)
#
# Aucun nom de famille n'existe comme texte dans la ROM (recherche exhaustive
# par mots-clés sur toutes les banques `mes_*` anglaises, sans résultat) —
# affichage par icône uniquement dans le jeu d'origine, icônes non localisées.
# Les 8 noms ci-dessous viennent d'un TRIPLE recoupement, pas d'un texte lu
# directement :
#   1. Wiki externe (rebjorn-wiki.com/dqmj/synthesis, recherche autorisée) :
#      table de mélange des familles avec 7 noms (Slime/Dragon/Nature/
#      Material/Demon/Undead/Beast) + "???" pour une 8e famille.
#   2. mes_monstersname.binE (noms de groupes de monstres au pluriel, 346
#      entrées) organisé en 8 blocs consécutifs dans cet ordre exact.
#   3. Corrélation par mot-clé de noms anglais connus (monsters-mapping.json)
#      contre le champ `family` déjà extrait : vote statistique quasi
#      unanime pour chaque bloc (ex. 27/27 "slime" -> famille 1).
# La 8e famille ("???" côté wiki) est confirmée être "Wildcard" : ses 10
# membres (famille 8) sont EXACTEMENT les 10 monstres de rang 9 non mappé
# (voir RANK_LETTERS ci-dessus) — identité totale, pas juste une similarité.
FAMILY_NAMES = {
    1: "Slime",
    2: "Dragon",
    3: "Nature",
    4: "Beast",
    5: "Material",
    6: "Demon",
    7: "Undead",
    8: "Wildcard",
}
import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

ENTRY_SIZE = 136
HEADER_SIZE = 8


def read_entries(data: bytes):
    magic, count = struct.unpack_from("<4sI", data, 0)
    assert magic == b"EKT\x00", magic
    for i in range(count):
        off = HEADER_SIZE + i * ENTRY_SIZE
        raf = data[off + 4]
        rank = raf & 0x0F
        family = (raf & 0xF0) >> 4
        # Stats de base niveau 1 : six u8 aux offsets 0x16 a 0x1b (PV, PM, attaque, defense, agilite, sagesse),
        # PROUVE par desassemblage ARM9 aux adresses 0x0203a640 et 0x0203db00.
        (
            base_hp,
            base_mp,
            base_attack,
            base_defense,
            base_agility,
            base_wisdom,
        ) = struct.unpack_from("<6B", data, off + 22)
        # Plafonds de stats : six u16 little-endian aux offsets 0x1c a 0x26 (PV, PM, attaque, defense, agilite,
        # sagesse), PROUVE par desassemblage (FUN_021c4f98 : stat = min(plafond, stat + gain)).
        (
            max_hp_limit,
            max_mp_limit,
            attack_limit,
            defense_limit,
            agility_limit,
            wisdom_limit,
        ) = struct.unpack_from("<6H", data, off + 28)
        skill_set = data[off + 72]
        yield {
            "species_id": i,
            "rank": rank,
            "rank_letter": RANK_LETTERS.get(rank),
            "family": family,
            "family_name": FAMILY_NAMES.get(family),
            "base_hp": base_hp,
            "base_mp": base_mp,
            "base_attack": base_attack,
            "base_defense": base_defense,
            "base_agility": base_agility,
            "base_wisdom": base_wisdom,
            "max_hp_limit": max_hp_limit,
            "max_mp_limit": max_mp_limit,
            "attack_limit": attack_limit,
            "defense_limit": defense_limit,
            "agility_limit": agility_limit,
            "wisdom_limit": wisdom_limit,
            "skill_set": skill_set,
        }


def main():
    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    by_monster_id: dict[int, list[str]] = {}
    for entry in mapping.values():
        by_monster_id.setdefault(entry["monster_id"], []).append(entry["id"])

    with open(os.path.join(DATA, "EnmyKindTbl.bin"), "rb") as f:
        data = f.read()

    result: dict[str, dict] = {}
    skipped_empty = 0
    for record in read_entries(data):
        if record["rank"] == 0 and record["family"] == 0:
            skipped_empty += 1
            continue
        for monster_id_str in by_monster_id.get(record["species_id"], []):
            result[monster_id_str] = record

    out_file = os.path.join(RACINE, "tools/monster_species_stats.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Species stats saved: {len(result)} known monster ids matched.")
    print(f"Empty (rank=0, family=0) slots skipped: {skipped_empty}")


if __name__ == "__main__":
    main()
