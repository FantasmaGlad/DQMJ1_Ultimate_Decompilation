#!/usr/bin/env python3
"""Monstres visibles sur le terrain, par carte : opcode 0x23 des scripts .evt (FUN_021c138c) + FldEnmyPrm.bin.

FUN_021c138c (gestionnaire de l'opcode 0x23) appelle FUN_021a7e58 : cree un acteur de terrain dont l'indice
FldEnmyPrm est l'argument 0 (stocke a acteur + 0x232), puis position x, y, z (arguments 1 a 3), un angle
(argument 4), un fanion (argument 5) et un octet (argument 6). FldEnmyPrm.bin : 880 entrees de 32 o, indexees comme
BtlEnmyPrm ; le u16 a +0 est l'espece (FUN_021aabfc/FUN_021bcf10 : EnmyKindTbl[*entree]).
Au contact (FUN_021bb860), l'indice de l'acteur touche devient l'ennemi 0 du combat ; les compagnons viennent des
tables .enct/EnmyPtnTbl (tools/extraire_rencontres_sauvages.py).
Sortie : assets/data/field_monsters.json
"""
import collections, glob, json, os, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from evt_vm import load, explore
import extraire_stats_combat as esc
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}
enemies = list(esc.read_entries((D / "BtlEnmyPrm.bin").read_bytes()))
fld = (D / "FldEnmyPrm.bin").read_bytes()
def fentry(i):
    e = fld[8 + 32 * i: 8 + 32 * (i + 1)]
    return struct.unpack_from("<H", e, 0)[0]

maps = {}
mismatch = 0
for f in sorted(glob.glob(str(D / "*.evt"))):
    name = os.path.basename(f)[:-4]
    d, seq = load(f)
    if not any(t == 0x23 for _, t, _ in seq): continue
    ent = sorted({v for v in struct.unpack("<%dI" % (0x1000 // 4), d[4:4 + 0x1000]) if v != 0xFFFFFFFF})
    raw, ctx, steps = explore(seq, ent, watch=(0x23,))
    rows = []
    for a in sorted(raw.get(0x23, ()), key=lambda x: str(x)):
        if a[0] is None or a[1] is None or a[2] is None or a[3] is None: continue
        idx = int(a[0])
        if idx >= 880: continue
        sp = fentry(idx)
        if idx < len(enemies) and enemies[idx]["species_id"] != sp: mismatch += 1
        rows.append({"fld_index": idx, "species": by_species.get(sp), "species_id": sp,
                     "level": enemies[idx]["level"] if idx < len(enemies) else None,
                     "pos": [a[1], a[2], a[3]], "args_4_6_raw": [a[4], a[5], a[6]]})
    if rows: maps[name] = rows
out = {"provenance": "ROM : opcode 0x23 des .evt + FldEnmyPrm.bin (voir docstring de tools/extraire_monstres_terrain.py)",
       "note": "Positions en unites de carte ; arguments 4 a 6 non decodes.", "maps": maps}
(OUT / "field_monsters.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("cartes", len(maps), "monstres", sum(len(v) for v in maps.values()), "espece Fld != Btl:", mismatch)
