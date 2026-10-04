#!/usr/bin/env python3
"""Extrait les occurrences de combat depuis BtlEnmyPrm.bin ("special encounter
monsters" selon Data Crystal — des instances de rencontre précises, pas les
stats de base canoniques d'une espèce, voir DISCLAIMER plus bas).

## Provenance et niveau de confiance (session du 2026-09-24)

Structure reprise de `BtlEnmyPrmEntry` dans
https://github.com/ExcaliburZero/dqmj1_rom_editor
(dqmj1_rom_util/src/btl_enmy_prm.rs), un outil de modding communautaire open
source. Deux éléments sont vérifiés de façon indépendante et fiable :

1. Taille totale de la struct (88 octets) : `(len(BtlEnmyPrm.bin) - 8) / 88 = 880`
   tombe pile (entier exact) sur notre fichier réel — la struct n'est pas une
   supposition, elle est confirmée par l'arithmétique du fichier.
2. Le champ `species_id` (tout premier champ, offset 0, sans ambiguïté
   possible) correspond **exactement** à `monster_id` de mapping_monstres.json
   (vérifié sur des dizaines d'entrées distinctes, correspondance exacte).

Les champs suivants (niveau, or, exp, stats) suivent l'ORDRE donné par la
struct communautaire, mais n'ont **pas** été confirmés par désassemblage —
seulement par cohérence statistique sur les 880 entrées : les HP croissent
globalement avec le niveau pour une même espèce (~83% des espèces avec
plusieurs occurrences suivent une tendance croissante), aucune valeur
aberrante (dépassement de u16, niveau hors [0,99]). C'est une preuve solide
mais **pas une certitude absolue** — à traiter comme "vraisemblablement exact"
plutôt que "vérifié au bit près", et à corriger si une contradiction apparaît
plus tard (ex. désassemblage futur de la fonction de lecture).

## DISCLAIMER à conserver dans toute utilisation de ces données

Ce ne sont **pas** les stats de base d'une espèce (celles-ci vivraient dans
`EnmyKindTbl.bin`, non fiable à ce jour — voir docs/PLAN.md du projet
bestiaire). Ce sont des **instances de rencontre** : une espèce peut apparaître
plusieurs fois à des niveaux différents (ex. combat de mi-jeu vs. combat de
fin de jeu). Ne pas les présenter comme "les" stats du monstre sans cette
nuance.
"""
import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

FIELDS = [
    ("species_id", 2), ("unknown_a", 6), ("skills", 24), ("item_drops", 8),
    ("gold", 2), ("unknown_b", 2), ("exp", 2), ("unknown_c", 2),
    ("level", 1), ("unknown_d", 1), ("unknown_e", 1), ("scout_chance", 1),
    ("max_hp", 2), ("max_mp", 2), ("attack", 2), ("defense", 2),
    ("agility", 2), ("wisdom", 2),
    ("unknown_f", 20), ("skill_set_ids", 3), ("unknown_g", 1),
]
OFFSETS = {}
_o = 0
for _name, _size in FIELDS:
    OFFSETS[_name] = _o
    _o += _size
ENTRY_SIZE = _o
assert ENTRY_SIZE == 88, ENTRY_SIZE


def read_entries(data):
    magic, length = struct.unpack_from("<II", data, 0)
    base = 8
    for i in range(length):
        off = base + i * ENTRY_SIZE
        species_id = struct.unpack_from("<H", data, off + OFFSETS["species_id"])[0]
        gold = struct.unpack_from("<H", data, off + OFFSETS["gold"])[0]
        exp = struct.unpack_from("<H", data, off + OFFSETS["exp"])[0]
        level = data[off + OFFSETS["level"]]
        scout_chance = data[off + OFFSETS["scout_chance"]]
        hp, mp, atk, dfn, agi, wis = struct.unpack_from(
            "<6H", data, off + OFFSETS["max_hp"]
        )
        # PROUVE par desassemblage (arm9 : FUN_0203baf0 lit la base a +0x34..+0x3e, FUN_0203c45c ajoute le correctif
        # signe s16 lu a +0x44..+0x4e puis multiplie par (90..109) / 100 au hasard et borne par le plafond d'espece) :
        # les stats nominales d'un ennemi sont base + correctif (a +-10 % pres). Les champs ci-dessous sont
        # les valeurs nominales ; `stat_adjust` garde le correctif.
        adj = struct.unpack_from("<6h", data, off + 0x44)
        hp, mp, atk, dfn, agi, wis = [max(0, v + a) for v, a in zip((hp, mp, atk, dfn, agi, wis), adj)]
        yield {
            "stat_adjust": list(adj),
            "species_id": species_id,
            "level": level,
            "gold": gold,
            "exp": exp,
            "scout_chance_raw": scout_chance,
            "max_hp": hp,
            "max_mp": mp,
            "attack": atk,
            "defense": dfn,
            "agility": agi,
            "wisdom": wis,
        }


BOSS_SPECIES = {
    84: "m225",   # Grand Dragon (sanctuaire)
    176: "m036",  # Orque (sanctuaire)
    177: "m180b", # As de Pique (Tartare)
    224: "m116",  # Golem (sanctuaire)
    225: "m197",  # Estark (post-game)
    275: "m211",  # Belzébik (sanctuaire)
    276: "m087",  # Encorneur (combat final)
    277: "m088",  # Sangliogre (combat final)
    278: "m188",  # Gracos (quêtes annexes)
    279: "m084b", # Bélial (île de Célesprit)
    280: "m230",  # Shivattak (sanctuaire)
    317: "m158",  # Capitaine Crow (5e combat)
    318: "m206",  # Dr Rebelote (boss final)
}


def get_active_indices():
    import glob
    # Rencontres sauvages (EnmyPtnTbl.bin)
    p_path = os.path.join(DATA, "EnmyPtnTbl.bin")
    wild = set()
    if os.path.exists(p_path):
        p = open(p_path, "rb").read()
        cnt = struct.unpack_from("<I", p, 4)[0]
        for i in range(cnt):
            for idx in struct.unpack_from("<5H", p[8 + 32*i : 8 + 32*(i+1)], 20):
                if idx > 0: wild.add(idx)

    # Combats de dresseurs (MstrPtnTbl.bin)
    m_path = os.path.join(DATA, "MstrPtnTbl.bin")
    trainer = set()
    if os.path.exists(m_path):
        mstr = open(m_path, "rb").read()
        cnt = struct.unpack_from("<II", mstr, 0)[1]
        for i in range(cnt):
            for idx in struct.unpack_from("<3H", mstr[8 + i*26 : 8 + (i+1)*26], 14):
                if idx > 0: trainer.add(idx)

    # Combats fixes (.evt)
    fixed = set()
    for f in glob.glob(os.path.join(DATA, "*.evt")):
        d = open(f, "rb").read()
        o = 0x1004
        while o + 8 <= len(d):
            t, l = struct.unpack_from("<II", d, o)
            if l < 8: break
            if t == 0x44:
                for j in range(o - 16, max(0x1004, o - 192), -16):
                    tt, ll = struct.unpack_from("<II", d, j)
                    if tt == 0x15 and ll == 16:
                        dk, di, sk, sv = struct.unpack_from("<IfIf", d, j + 8)
                        if dk == 1 and int(di) in (1, 2, 3) and sk == 2 and int(sv) > 0:
                            fixed.add(int(sv))
            o += l
    return wild | trainer | fixed


def main():
    active_indices = get_active_indices()

    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    by_monster_id = {}
    for entry in mapping.values():
        by_monster_id.setdefault(entry["monster_id"], []).append(entry["id"])
    for sp_id, mid in BOSS_SPECIES.items():
        if mid not in by_monster_id.setdefault(sp_id, []):
            by_monster_id[sp_id].append(mid)

    with open(os.path.join(DATA, "BtlEnmyPrm.bin"), "rb") as f:
        data = f.read()

    by_id = {}
    unmatched = 0
    filtered_dummies = 0
    for i, record in enumerate(read_entries(data)):
        # Filtre les gabarits de dev inactifs (non references en jeu et HP minimes de template)
        if i not in active_indices and record["level"] <= 1 and record["max_hp"] <= 35:
            filtered_dummies += 1
            continue
        ids = by_monster_id.get(record["species_id"])
        if not ids:
            unmatched += 1
            continue
        for monster_id_str in ids:
            by_id.setdefault(monster_id_str, []).append(record)

    out_file = os.path.join(RACINE, "tools/monster_battle_encounters.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(by_id, f, indent=2, ensure_ascii=False)

    bestiaire_out = os.path.join(
        os.path.dirname(RACINE),
        "DragonQuestMonsterJoker1Bestiaire",
        "assets",
        "data",
        "monster_battle_encounters.json",
    )
    if os.path.exists(os.path.dirname(bestiaire_out)):
        with open(bestiaire_out, "w", encoding="utf-8") as f:
            json.dump(by_id, f, indent=2, ensure_ascii=False)

    total_entries = sum(len(v) for v in by_id.values())
    print(f"Encounters saved: {total_entries} across {len(by_id)} known monster ids.")
    print(f"Filtered dummy developer templates: {filtered_dummies}")
    print(f"Entries with a species_id not in mapping_monstres.json: {unmatched}")


if __name__ == "__main__":
    main()
