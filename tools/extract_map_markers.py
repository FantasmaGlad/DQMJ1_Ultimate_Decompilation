#!/usr/bin/env python3
"""Extrait les marqueurs de carte (.pos) : warps, boutiques, points de PNJ, objets.

Format .pos (verifie sur les 76 fichiers : 21 enregistrements sur s001, tous dans la boite
englobante de l'ile) : "POS\0", u32 nombre d'enregistrements, puis des enregistrements de 72 o
(le premier est l'en-tete de la carte, ex. "SE001") :
  +0   nom (32 o, ASCII, termine par 0 ; le reste du champ est du bruit memoire)
  +32  position x, y, z : 3 x s32 en virgule fixe 20.12 (meme repere que les modeles)
  +44  rotation x, y, z : 3 x s32 20.12, en degres
  +56  echelle x, y, z : 3 x s32 20.12
  +68  4 o non decodes
Classification par prefixe du nom (convention observee, non documentee) :
  w_<carte>_...  warp vers la carte <carte> ; shop_*  boutique ; p_*  point de PNJ ; autre : objet.
Sortie : assets/data/map_markers.json
"""
import json, re, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "map_markers.json"

def kind_of(name):
    if name.startswith("w_"): return "warp"
    if name.startswith("shop_"): return "shop"
    if name.startswith("p_"): return "npc"
    return "object"

result = {}
for pos in sorted((ROOT / "work/maps").glob("*/*.pos")):
    d = pos.read_bytes()
    if d[:4] != b"POS\0": continue
    n = struct.unpack_from("<I", d, 4)[0]
    markers = []
    for k in range(1, n):  # 0 = en-tete
        r = 8 + 72 * k
        if r + 72 > len(d): break
        name = d[r:r + 32].split(b"\0")[0].decode("latin1")
        x, y, z = (v / 4096 for v in struct.unpack_from("<3i", d, r + 32))
        rot = [v / 4096 for v in struct.unpack_from("<3i", d, r + 44)]
        kind = kind_of(name)
        m = {"name": name, "kind": kind, "pos": [round(x, 3), round(y, 3), round(z, 3)], "rot_y": round(rot[1], 2)}
        if kind == "warp":
            t = re.match(r"w_([a-z]\d{3})_", name)
            if t: m["target_map"] = t.group(1)
        markers.append(m)
    result[pos.parent.name] = markers
OUT.write_text(json.dumps({"provenance": "ROM (.pos des archives .map), voir tools/extract_map_markers.py", "maps": result}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", OUT, len(result), "cartes,", sum(len(v) for v in result.values()), "marqueurs")
