#!/usr/bin/env python3
"""Extrait les rencontres sauvages exhaustives avec météo, jour/nuit et sous-zones depuis les 66 fichiers .enct.

Sources de vérité :
  - 66 fichiers .enct dans work/extracted/data/*.enct
  - EnmyPtnTbl.bin (216 patterns de composition de groupe)
  - BtlEnmyPrm.bin (880 gabarits d'ennemis de combat)
  - FldEnmyPrm.bin et opcode 0x23 (monstres visibles sur le terrain)
  - monsters-mapping.json (association interne -> identifiant canonique)

Sortie : assets/data/wild_encounters_complete.json
"""
import glob
import json
import os
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
import extraire_stats_combat as esc

# Chargement des tables de base
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}
enemies = list(esc.read_entries((D / "BtlEnmyPrm.bin").read_bytes()))

# Lecture des monstres de terrain existants
field_data = json.loads((OUT / "field_monsters.json").read_text(encoding="utf-8"))
field_by_map = field_data.get("maps", {})

# Lecture des patterns de EnmyPtnTbl.bin
p = (D / "EnmyPtnTbl.bin").read_bytes()
num_patterns = struct.unpack_from("<I", p, 4)[0]
patterns = {}

def get_enemy_info(idx):
    if idx == 0 or idx >= len(enemies):
        return None
    e = enemies[idx]
    sp = e["species_id"]
    m_id = by_species.get(sp)
    return {
        "btl_index": idx,
        "species_id": sp,
        "monster_id": m_id,
        "level": e["level"],
    }

for i in range(num_patterns):
    e = p[8 + 32 * i: 8 + 32 * (i + 1)]
    key = struct.unpack_from("<H", e, 0)[0]
    byte2 = e[2]
    pct_a = e[4]
    sel_a = [x - 256 if x > 127 else x for x in e[5:8]]
    pct_b = e[8]
    sel_b = [x - 256 if x > 127 else x for x in e[9:12]]
    pct_c = max(0, 100 - pct_a - pct_b)
    min_c = e[12]
    max_c = e[13]
    weights_c = list(e[14:19])
    enemy_indices = struct.unpack_from("<5H", e, 20)
    enemy_list = [get_enemy_info(x) for x in enemy_indices]

    patterns[key] = {
        "pattern_key": key,
        "byte2": byte2,
        "group_a": {"percent": pct_a, "selectors": sel_a},
        "group_b": {"percent": pct_b, "selectors": sel_b},
        "group_c": {"percent": pct_c, "min": min_c, "max": max_c, "weights": weights_c},
        "enemies": enemy_list,
    }

# Mapping du flag temporel / météo
# 0 = Jour, 1 = Nuit, 2 = Pluie / Tempête (ex: Fert)
WEATHER_LABELS = {
    0: "day",
    1: "night",
    2: "rain_storm",
}

maps_result = {}
monsters_locations = {}

enct_files = sorted(glob.glob(str(D / "*.enct")))

for f in enct_files:
    map_id = os.path.basename(f)[:-5].lower()
    raw = open(f, "rb").read()
    if len(raw) < 8:
        continue
    n = struct.unpack_from("<I", raw, 4)[0]
    encounters = []
    zones = set()
    map_monsters = {}

    for i in range(n):
        entry = raw[8 + 16 * i: 8 + 16 * (i + 1)]
        if len(entry) < 16:
            continue
        bg = entry[:8].split(b"\0")[0].decode("ascii", errors="ignore").upper()
        zone = entry[8]
        weather_flag = entry[9]
        attr_high = struct.unpack_from("<H", entry, 10)[0]
        key = struct.unpack_from("<H", entry, 12)[0]
        attr_low = entry[14]

        zones.add(zone)
        weather_label = WEATHER_LABELS.get(weather_flag, f"weather_{weather_flag}")

        pat = patterns.get(key)
        companions = []
        if pat:
            for em in pat["enemies"]:
                if em and em["monster_id"]:
                    companions.append(em)
                    m_id = em["monster_id"]
                    if m_id not in map_monsters:
                        map_monsters[m_id] = {
                            "monster_id": m_id,
                            "species_id": em["species_id"],
                            "roles": set(),
                            "time_weather": set(),
                            "levels": set(),
                            "battle_backgrounds": set(),
                        }
                    map_monsters[m_id]["roles"].add("companion")
                    map_monsters[m_id]["time_weather"].add(weather_label)
                    map_monsters[m_id]["levels"].add(em["level"])
                    if bg:
                        map_monsters[m_id]["battle_backgrounds"].add(bg)

        encounters.append({
            "zone": zone,
            "weather_flag": weather_flag,
            "time_weather": weather_label,
            "battle_background": bg,
            "attr_high": attr_high,
            "attr_low": attr_low,
            "pattern_key": key,
            "companions": companions,
        })

    # Monstres de terrain pour cette carte
    field_list = field_by_map.get(map_id, [])
    for fm in field_list:
        m_id = fm.get("species")
        if m_id:
            if m_id not in map_monsters:
                map_monsters[m_id] = {
                    "monster_id": m_id,
                    "species_id": fm.get("species_id"),
                    "roles": set(),
                    "time_weather": set(),
                    "levels": set(),
                    "battle_backgrounds": set(),
                }
            map_monsters[m_id]["roles"].add("field")
            if fm.get("level"):
                map_monsters[m_id]["levels"].add(fm["level"])

    # Enregistrer dans l'index par monstre
    for m_id, m_data in map_monsters.items():
        if m_id not in monsters_locations:
            monsters_locations[m_id] = []
        monsters_locations[m_id].append({
            "map_id": map_id,
            "roles": sorted(m_data["roles"]),
            "time_weather": sorted(m_data["time_weather"]) if m_data["time_weather"] else ["any"],
            "levels": sorted(m_data["levels"]),
            "battle_backgrounds": sorted(m_data["battle_backgrounds"]),
        })

    maps_result[map_id] = {
        "map_id": map_id,
        "zones": sorted(zones),
        "encounters_count": len(encounters),
        "encounters": encounters,
        "monsters": [
            {
                "monster_id": m_id,
                "species_id": v["species_id"],
                "roles": sorted(v["roles"]),
                "time_weather": sorted(v["time_weather"]) if v["time_weather"] else ["any"],
                "levels": sorted(v["levels"]),
                "battle_backgrounds": sorted(v["battle_backgrounds"]),
            }
            for m_id, v in sorted(map_monsters.items())
        ],
    }

out_data = {
    "provenance": "ROM : 66 fichiers .enct + EnmyPtnTbl.bin + BtlEnmyPrm.bin + FldEnmyPrm.bin / opcode 0x23",
    "weather_mapping": WEATHER_LABELS,
    "total_maps": len(maps_result),
    "total_monsters_with_wild": len(monsters_locations),
    "maps": maps_result,
    "monsters": {k: sorted(v, key=lambda x: x["map_id"]) for k, v in sorted(monsters_locations.items())},
}

target_file = OUT / "wild_encounters_complete.json"
target_file.write_text(json.dumps(out_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Écrit {target_file} : {len(maps_result)} cartes, {len(monsters_locations)} monstres cartographiés.")
