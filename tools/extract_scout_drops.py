#!/usr/bin/env python3
"""Extrait les taux de capture (scout) et les tables de butin (drops) de BtlEnmyPrm.bin (File ID 100).

Structure prouvee par desassemblage (overlay_0001, FUN_021e0c00) :
- En-tete : 8 octets ("BEPT", u32 nombre d'entrees = 880)
- Entrees : 88 octets chacune
  - Offset 0  : species_id (u16)
  - Offset 32 : item1_id (u16)
  - Offset 34 : item1_rate_idx (u8, 0=100%, 1=50%, 2=25%, 3=12.5%, 4=6.25%, 5=3.125%, 6=1.5625%)
  - Offset 36 : item2_id (u16)
  - Offset 38 : item2_rate_idx (u8)
  - Offset 44 : exp (u16)
  - Offset 46 : gold (u16)
  - Offset 48 : level (u8)
  - Offset 51 : scout_rate_base (u8 : 0=indressable, 1, 10, 25, 35, 40, 45, 50, 55, 65, 70, 75, 80, 85, 90, 100)
  - Offsets 52..63 : Stats de base (HP, MP, Att, Def, Agi, Wis en u16)
  - Offsets 68..79 : Modificateurs de stats (6 x u16)
  - Offsets 84..86 : 3 competences innees (u8)
"""

import json
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire")

sys.path.insert(0, os.path.join(RACINE, "tools"))
from extract_mapping import decode  # noqa: E402

RATE_FRACTIONS = {
    0: "1/1",
    1: "1/2",
    2: "1/4",
    3: "1/8",
    4: "1/16",
    5: "1/32",
    6: "1/64",
}

RATE_PERCENTS = {
    0: 100.0,
    1: 50.0,
    2: 25.0,
    3: 12.5,
    4: 6.25,
    5: 3.125,
    6: 1.5625,
}

LANGUAGES = ["en", "fr", "de", "it", "es"]
LANG_SUFFIXES = {"en": "E", "fr": "F", "de": "D", "it": "I", "es": "S"}


def clean_name(name):
    import re
    name = re.sub(r"<[0-9a-f]{2}>", "", name)
    return name.strip("'").strip()


def load_item_names():
    names = {lang: {} for lang in LANGUAGES}
    for lang, sfx in LANG_SUFFIXES.items():
        p = os.path.join(DATA, f"mes_itemomitname.bin{sfx}")
        if os.path.exists(p):
            with open(p, "rb") as f:
                raw = f.read()
            parts = [clean_name(x) for x in decode(raw).split("|")]
            for idx, n in enumerate(parts):
                if n:
                    names[lang][idx] = n
    return names


def main():
    prm_path = os.path.join(DATA, "BtlEnmyPrm.bin")
    with open(prm_path, "rb") as f:
        data = f.read()

    magic = data[:4]
    assert magic == b"BEPT", f"Mauvais magic : {magic}"
    count = struct.unpack_from("<I", data, 4)[0]
    entry_size = 88
    assert len(data) == 8 + count * entry_size

    item_names = load_item_names()

    # Charger le mapping monstre (id numerique -> slug m###)
    mapping_path = os.path.join(BESTIAIRE, "assets/data/monsters-mapping.json")
    species_slug_map = {}
    if os.path.exists(mapping_path):
        with open(mapping_path, "r", encoding="utf-8") as f:
            m = json.load(f)
            for slug, info in m.items():
                species_slug_map[info["monster_id"]] = slug

    by_encounter = []
    by_species = {}

    for i in range(count):
        entry = data[8 + i * entry_size : 8 + (i + 1) * entry_size]
        species_id = struct.unpack_from("<H", entry, 0)[0]
        item1_id, item1_rate = struct.unpack_from("<HB", entry, 32)
        item2_id, item2_rate = struct.unpack_from("<HB", entry, 36)
        exp, gold = struct.unpack_from("<HH", entry, 44)
        level = entry[48]
        scout_rate = entry[51]

        drops = []
        for i_id, i_rate in [(item1_id, item1_rate), (item2_id, item2_rate)]:
            if i_id > 0:
                d = {
                    "item_id": i_id,
                    "names": {lang: item_names[lang].get(i_id, "") for lang in LANGUAGES},
                    "rate_index": i_rate,
                    "rate_fraction": RATE_FRACTIONS.get(i_rate, f"1/{2**i_rate}"),
                    "rate_percent": RATE_PERCENTS.get(i_rate, 100.0 / (2**i_rate)),
                }
                drops.append(d)

        enc_info = {
            "encounter_index": i,
            "species_id": species_id,
            "species_slug": species_slug_map.get(species_id, f"m{species_id:03d}"),
            "level": level,
            "exp": exp,
            "gold": gold,
            "scout_rate_base": scout_rate,
            "is_scoutable": scout_rate > 0,
            "drops": drops,
        }
        by_encounter.append(enc_info)

        # Agreger par espece
        if species_id not in by_species:
            by_species[species_id] = {
                "species_id": species_id,
                "species_slug": species_slug_map.get(species_id, f"m{species_id:03d}"),
                "wild_scout_rates": set(),
                "all_scout_rates": set(),
                "encounters_count": 0,
                "drops_dict": {},
            }

        sp = by_species[species_id]
        sp["encounters_count"] += 1
        sp["all_scout_rates"].add(scout_rate)
        if scout_rate > 0:
            sp["wild_scout_rates"].add(scout_rate)

        for d in drops:
            key = (d["item_id"], d["rate_index"])
            if key not in sp["drops_dict"]:
                sp["drops_dict"][key] = d

    # Finaliser les dictionnaires d'especes
    species_out = {}
    for sid, sp in sorted(by_species.items()):
        slug = sp["species_slug"]
        wild_rates = sorted(sp["wild_scout_rates"])
        drops_list = sorted(sp["drops_dict"].values(), key=lambda x: x["item_id"])
        species_out[slug] = {
            "species_id": sid,
            "species_slug": slug,
            "is_scoutable": len(wild_rates) > 0,
            "scout_rate_base": wild_rates[0] if len(wild_rates) == 1 else (wild_rates if wild_rates else 0),
            "scout_rate_min": min(wild_rates) if wild_rates else 0,
            "scout_rate_max": max(wild_rates) if wild_rates else 0,
            "drops": drops_list,
        }

    output_data = {
        "provenance": "ROM: BtlEnmyPrm.bin (File ID 100), overlay_0001 (0x5c1c8, 0x92924) via tools/extract_scout_drops.py",
        "description": "Taux de dressage de base et tables de butin d'apres-combat 100% extraits de la ROM",
        "scout_formula": {
            "description": "Chances de capture par coup = (Degats_Physiques / PV_Max_Ennemi) * Scout_Rate_Base / (1 + Nb_Monstres_Possedes)",
            "tension_multipliers": {"0": 1.0, "5": 1.4, "20": 1.7, "50": 2.0, "100": 2.5},
            "provenance_code": "overlay_0001:0x92924",
        },
        "drop_rates_table": {
            str(k): {"fraction": frac, "percent": pct} for k, (frac, pct) in sorted(
                [(k, (RATE_FRACTIONS[k], RATE_PERCENTS[k])) for k in RATE_FRACTIONS]
            )
        },
        "by_species": species_out,
        "by_encounter": by_encounter,
    }

    # Sauvegarder dans les deux depots
    out_paths = [
        os.path.join(RACINE, "assets/data/monster_drops_scout.json"),
        os.path.join(BESTIAIRE, "assets/data/monster_drops_scout.json"),
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Exporte avec succes : {p}")


if __name__ == "__main__":
    main()
