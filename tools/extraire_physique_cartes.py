#!/usr/bin/env python3
"""Extrait les donnees physiques et attributs de surface/collision des 90 cartes (.atr).

Structure deduite de l'analyse des archives FPK :
- Format ATR : magique ATR\\0 + dimensions de grille et blocs d'attributs de cellules
- Couches :
  - *a.atr : grille de collision de terrain (marchable, obstacles, rebords franchissables, liquides)
  - *c.atr : grille de contrainte de camera
  - *e.atr : surfaces speciales / elevations
Sortie : assets/data/map_physics_attributes.json
"""

import glob
import json
import os
import struct
from collections import Counter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS_DIR = os.path.join(RACINE, "work/maps")
BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire")
OUTPUT_FILE = os.path.join(BESTIAIRE, "assets/data/map_physics_attributes.json")
SCN_FILE = os.path.join(BESTIAIRE, "assets/data/map_scenes.json")


def main():
    maps = {}
    map_dirs = sorted(os.listdir(MAPS_DIR))

    for mdir in map_dirs:
        mdir_path = os.path.join(MAPS_DIR, mdir)
        if not os.path.isdir(mdir_path):
            continue

        atr_files = glob.glob(os.path.join(mdir_path, "*.atr"))
        if not atr_files:
            continue

        a_file = next((f for f in atr_files if f.endswith("a.atr")), None)
        c_file = next((f for f in atr_files if f.endswith("c.atr")), None)
        e_file = next((f for f in atr_files if f.endswith("e.atr")), None)

        record = {
            "map_id": mdir,
            "has_terrain_collision": a_file is not None,
            "has_camera_collision": c_file is not None,
            "has_elevation_attributes": e_file is not None,
            "terrain": None,
        }

        if a_file and os.path.exists(a_file):
            with open(a_file, "rb") as f:
                d = f.read()
            if len(d) >= 20:
                magic, val1, val2, val3, val4 = struct.unpack("<4sIIII", d[:20])
                payload = d[20:]
                counts = Counter(payload)
                walkable = counts[0]
                blocked = counts[255]
                ledges = counts[254]
                special = sum(counts[v] for v in counts if v not in (0, 255, 254))
                total = len(payload)
                walk_ratio = round(walkable / total * 100, 1) if total else 0.0

                record["terrain"] = {
                    "file_name": os.path.basename(a_file),
                    "file_size": len(d),
                    "grid_width": val1,
                    "total_cells": total,
                    "walkable_cells": walkable,
                    "blocked_cells": blocked,
                    "ledge_cells": ledges,
                    "hazard_or_water_cells": special,
                    "walkable_percentage": walk_ratio,
                }

        maps[mdir] = record

    # Load SCN metadata if available
    scn_summary = {}
    if os.path.exists(SCN_FILE):
        try:
            with open(SCN_FILE) as f:
                scn_data = json.load(f)
            for mid, variants in scn_data.get("maps", {}).items():
                scn_summary[mid] = {
                    "time_variants": list(variants.keys()),
                    "has_fog": any("fog" in v for v in variants.values()),
                    "lights_count": max((len(v.get("lights", [])) for v in variants.values()), default=0),
                }
        except Exception:
            pass

    for mid, rec in maps.items():
        if mid in scn_summary:
            rec["photometry"] = scn_summary[mid]

    output_data = {
        "provenance": (
            "ROM : Fichiers .atr (attributs de collision et surfaces) et .scn "
            "(parametres photometriques et brouillard) extraits des archives FPK."
        ),
        "total_maps_with_physics": len(maps),
        "maps": maps,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Genere avec succes : {OUTPUT_FILE} ({len(maps)} cartes documentees)")


if __name__ == "__main__":
    main()
