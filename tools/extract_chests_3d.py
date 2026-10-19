#!/usr/bin/env python3
"""Extrait la géolocalisation 3D exacte de tous les coffres physiques depuis les scripts .evt de la ROM.

Preuves par le code :
  - Opcode 0x5f dans les 80 scripts .evt : instanciation d'un coffre 3D physique sur la carte.
  - Opcode 0x15 affectant les arguments avant 0x5f :
      arg 0 : Tier (0.0 = Tier C, 1.0 = Tier B, 2.0 = Tier A)
      arg 1, 2, 3 : Coordonnées 3D spatiales (X, Y, Z) en unités de carte
      arg 4 : Rotation Yaw en degrés
      arg 5 : Index / état de coffre
  - Corrélation avec les tables de butin de chests.json (Tiers A/B/C, pourcentages d'objets et monstres pièges).

Sortie : assets/data/chest_locations_3d.json
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
import evt_vm

# Charger chests.json existant
chests_db = json.loads((OUT / "chests.json").read_text(encoding="utf-8"))
tiers_data = chests_db.get("tiers", {})

TIER_LETTER = {
    0: "C",
    1: "B",
    2: "A",
}

evt_files = sorted(glob.glob(str(D / "*.evt")))

maps_chests = {}
total_chests = 0

for f in evt_files:
    map_id = Path(f).stem.lower()
    raw, seq = evt_vm.load(f)

    # Vérifier si la carte contient des coffres 0x5f
    if not any(t == 0x5f for _, t, _ in seq):
        continue

    entries = [
        struct.unpack_from("<I", raw, 4 + 4 * i)[0]
        for i in range(1024)
        if struct.unpack_from("<I", raw, 4 + 4 * i)[0] != 0xFFFFFFFF
    ]

    res, ctx, steps = evt_vm.explore(seq, entries, watch=(0x5f,), maxsteps=400_000)
    chest_list = []

    # Dédupliquer les coffres par (tier, x, y, z)
    seen_chests = set()
    for args in sorted(res[0x5f], key=lambda x: str(x)):
        if len(args) < 5 or args[0] is None or args[1] is None or args[2] is None or args[3] is None:
            continue
        raw_tier = int(round(args[0]))
        tier_letter = TIER_LETTER.get(raw_tier, "C")
        x = round(float(args[1]), 2)
        y = round(float(args[2]), 2)
        z = round(float(args[3]), 2)
        rot_y = round(float(args[4]), 1) if args[4] is not None else 0.0
        state = int(round(args[5])) if len(args) > 5 and args[5] is not None else 0

        coord_key = (tier_letter, x, y, z)
        if coord_key in seen_chests:
            continue
        seen_chests.add(coord_key)

        tier_info = tiers_data.get(tier_letter, {})
        chest_list.append({
            "map_id": map_id,
            "tier": tier_letter,
            "tier_name_en": tier_info.get("name_en", "Standard"),
            "tier_name_fr": tier_info.get("name_fr", "Standard"),
            "position": [x, y, z],
            "rot_y": rot_y,
            "state_flag": state,
            "item_chance_percent": tier_info.get("item_chance_percent", 75),
            "trap": tier_info.get("trap"),
            "possible_items": tier_info.get("items", []),
        })

    if chest_list:
        maps_chests[map_id] = chest_list
        total_chests += len(chest_list)

out = {
    "provenance": "ROM : scripts .evt, opcode 0x5f et affectations 0x15 précédant l'appel, recoupé avec chests.json",
    "total_maps": len(maps_chests),
    "total_chests": total_chests,
    "maps": maps_chests,
}

target_file = OUT / "chest_locations_3d.json"
target_file.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Écrit {target_file} : {total_chests} coffres 3D physiques extraits sur {len(maps_chests)} cartes.")
