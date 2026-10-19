#!/usr/bin/env python3
"""Zone (code d'ile) de chaque carte, lue dans la table par carte de overlay_0000 -> assets/data/map_areas.json.

Table de 100 entrees de 16 octets a 0x021de4d2 - 2 (pointeur en 0x021ac8e8, lecteur FUN_021ac8dc = octet 2 de l'entree) :
octet 0 serie (0 s, 1 d, 2 f, 3 k, 5 h, 6 e, 7 i, 8 t, 9 w, 10 o), octet 1 numero (nom de fichier %c%03d), octet 2 code de zone.
Codes : 1 Infant Isle (s001 s002 d001), 2 Domus (s021..), 3 Xeroph (s011, d011..), 4 Celeste (s041..), 5 Palaish (s031..), 6 Fert (s051..),
7 Infern (s061..), 8 serie i, 0 sans zone (f, k, h, e...). Le code est celui ecrit dans l'octet d'etat 0x0216f440 en entrant sur une
carte (fonction 0x021b0bb8). Rattachement code -> nom d'ile : par les noms de cartes (mes_mapname), inferre.
"""
import json, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "map_areas.json"
BASE = 0x02184B40
LETTERS = {0: "s", 1: "d", 2: "f", 3: "k", 5: "h", 6: "e", 7: "i", 8: "t", 9: "w", 10: "o"}

b = (ROOT / "work/extracted/overlay/overlay_0000.bin").read_bytes()
q = 0x021DE4D2 - 2 - BASE
maps, areas = {}, {}
for i in range(100):
    ser, num, area = b[q + 16 * i], b[q + 16 * i + 1], b[q + 16 * i + 2]
    if ser not in LETTERS:
        continue
    mid = f"{LETTERS[ser]}{num:03d}"
    maps[mid] = area
    areas.setdefault(str(area), []).append(mid)
OUT.write_text(json.dumps({"provenance": "ROM : overlay_0000, table par carte (FUN_021ac8dc), voir tools/extract_map_areas.py", "maps": maps, "areas": areas}, indent=0) + "\n")
print(len(maps), "cartes,", {k: len(v) for k, v in sorted(areas.items())})
