#!/usr/bin/env python3
"""Catalogue les 83 arènes de combat 3D (bd*, bf*, bh*, be*) et les relie aux cartes et monstres.

Sources de vérité :
  - Modèles GLB dans assets/models/web-gltf/glb/
  - Rencontres sauvages dans assets/data/wild_encounters_complete.json

Sortie : assets/data/battle_arenas.json
"""
import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"

glbs = glob.glob(str(OUT.parent / "models" / "web-gltf" / "glb" / "*" / "*.glb"))

wild_enc_path = OUT / "wild_encounters_complete.json"
wild_data = json.loads(wild_enc_path.read_text(encoding="utf-8")) if wild_enc_path.exists() else {}

bg_maps = {}
bg_monsters = {}
if "maps" in wild_data:
    for map_id, m_info in wild_data["maps"].items():
        for enc in m_info.get("encounters", []):
            bg = enc.get("battle_background", "").lower()
            if bg:
                if bg not in bg_maps:
                    bg_maps[bg] = set()
                bg_maps[bg].add(map_id)

if "monsters" in wild_data:
    for m_id, locs in wild_data["monsters"].items():
        for loc in locs:
            for bg in loc.get("battle_backgrounds", []):
                bg_low = bg.lower()
                if bg_low not in bg_monsters:
                    bg_monsters[bg_low] = set()
                bg_monsters[bg_low].add(m_id)

arenas = []
for g in sorted(glbs):
    name = os.path.basename(g)[:-4]
    p = name[:2].lower()
    if p in ("bd", "bf", "bh", "be"):
        category = "sanctuary" if p == "bd" else ("field" if p == "bf" else ("arena" if p == "bh" else "special"))
        arenas.append({
            "id": name,
            "category": category,
            "maps": sorted(bg_maps.get(name.lower(), set())),
            "monsters": sorted(bg_monsters.get(name.lower(), set())),
            "glb_path": f"models/web-gltf/glb/{name}/{name}.glb",
            "url": f"/api/assets/models/web-gltf/glb/{name}/{name}.glb",
        })

out = {
    "provenance": "ROM : 83 modèles géométriques d'arènes de combat GLB (.nsbmd) corrélés avec les tables .enct",
    "total_arenas": len(arenas),
    "arenas": arenas,
}

target = OUT / "battle_arenas.json"
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Écrit {target} : {len(arenas)} arènes de combat 3D répertoriées.")
