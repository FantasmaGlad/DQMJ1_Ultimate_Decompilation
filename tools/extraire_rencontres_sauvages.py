#!/usr/bin/env python3
"""Rencontres sauvages : <carte>.enct -> EnmyPtnTbl.bin -> BtlEnmyPrm.bin.

Chaine lue dans le code (overlay_0000, base 0x02184b40) :
  FUN_021bb860 (combat sauvage) : FUN_021ad1dc(zone, nuit, attribut haut, attribut bas) cherche dans la table
  `.enct` de la carte (chargee sous "%c%03d.enct") l'entree dont l'octet +8 = zone, +9 = nuit(1)/jour(0),
  u16 +10 = quartet haut de l'attribut de case, octet +14 = quartet bas (second passage sans ce dernier) ;
  elle renvoie le u16 +12 = cle EnmyPtnTbl. Entree .enct : 16 o = nom du fond de combat (8 o, "BF001B"), zone,
  nuit, attribut haut (u16), cle (u16), attribut bas.
  FUN_021ad3cc : recherche dichotomique de la cle (u16 +0) dans EnmyPtnTbl (216 entrees de 32 o).
  FUN_021ad4ec : tirage r dans [0,100) : r < +4 -> groupe A (+4) ; sinon r < +4 + +8 -> groupe B (+8) ; sinon groupe C (+0xc).
  Groupes A/B (4 o) : [0] pourcentage, [1..3] selecteur signe des emplacements 0 a 2 = indice dans le tableau
  de 5 u16 (+0x14, indices BtlEnmyPrm) ; -1 : emplacement 0 = le monstre touche sur le terrain (inchange),
  emplacements 1-2 = vide. Groupe C (FUN_021ad438) : [0] min, [1] max (nombre de monstres tire), [2..6] poids
  des 5 monstres ; l'emplacement 0 reste le monstre touche.
  L'octet +2 de l'entree est transmis au combat (sens non prouve).
Sortie : assets/data/wild_encounters.json
"""
import glob, json, os, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
import extraire_stats_combat as esc
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}
enemies = list(esc.read_entries((D / "BtlEnmyPrm.bin").read_bytes()))

def enemy(v):
    if v == 0 or v >= len(enemies): return None
    e = enemies[v]
    return {"btl_enmy_prm_index": v, "species": by_species.get(e["species_id"]), "level": e["level"]}

p = (D / "EnmyPtnTbl.bin").read_bytes()
patterns = {}
for i in range(struct.unpack_from("<I", p, 4)[0]):
    e = p[8 + 32 * i: 8 + 32 * (i + 1)]
    key = struct.unpack_from("<H", e, 0)[0]
    sg = lambda b: b - 256 if b > 127 else b
    patterns[key] = {
        "byte2_raw": e[2],
        "group_a": {"percent": e[4], "selectors": [sg(x) for x in e[5:8]]},
        "group_b": {"percent": e[8], "selectors": [sg(x) for x in e[9:12]]},
        "group_c": {"percent": max(0, 100 - e[4] - e[8]), "min": e[12], "max": e[13], "weights": list(e[14:19])},
        "enemies": [enemy(x) for x in struct.unpack_from("<5H", e, 20)],
    }

maps = {}
for f in sorted(glob.glob(str(D / "*.enct"))):
    d = open(f, "rb").read()
    n = struct.unpack_from("<I", d, 4)[0]
    rows = []
    for i in range(n):
        e = d[8 + 16 * i: 8 + 16 * (i + 1)]
        key = struct.unpack_from("<H", e, 12)[0]
        rows.append({"battle_background": e[:8].split(b"\0")[0].decode("ascii"), "zone": e[8], "night": e[9],
                     "attr_high": struct.unpack_from("<H", e, 10)[0], "attr_low": e[14], "pattern_key": key,
                     "known_pattern": key in patterns})
    maps[os.path.basename(f)[:-5].lower()] = rows
out = {"provenance": "ROM : .enct + EnmyPtnTbl + BtlEnmyPrm, chaine lue dans le code (voir docstring de tools/extraire_rencontres_sauvages.py)",
       "note": "Le monstre touche sur le terrain (emplacement 0) n'est pas dans ces tables ; elles donnent les compagnons.",
       "patterns": {str(k): v for k, v in patterns.items()}, "maps": maps}
(OUT / "wild_encounters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
allkeys = {r["pattern_key"] for rows in maps.values() for r in rows}
print("cartes", len(maps), "lignes", sum(len(v) for v in maps.values()), "cles distinctes", len(allkeys), "inconnues", len(allkeys - set(patterns)), "patterns", len(patterns))
