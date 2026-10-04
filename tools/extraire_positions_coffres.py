#!/usr/bin/env python3
"""Positions des coffres (opcode 0x5f des scripts .evt) -> assets/data/chest_positions.json.

Prouve par desassemblage : le dispatcheur FUN_021c9824 envoie l'opcode 0x5f a FUN_021c4148, qui lit 6 arguments (type de coffre u8,
x, y, z, rotation, drapeau u8), convertit les flottants x, y, z et la rotation en virgule fixe 20.12 et appelle FUN_021bd0f4, qui remplit
un des 16 emplacements de coffre (position +0x70..+0x78, type +0x101, drapeau +0x100 = 1) ; le type choisit un nom de modele dans un
tableau de 3 (FUN_021acd54 : « takara », « takara_d »...). Tirage : chaque script de carte contient un aiguillage sur la variable « type de coffre » : type 0 -> sous-programme
« ランダム宝箱：A », type 1 -> « B », type 2 -> « C » (35 scripts sur 35, sans exception) : le type du coffre fixe donc le tiers de son tirage
(voir chests.json). Les scripts sont nommes comme la carte. L'explorateur evt_vm suit les deux
branches : les positions sont dedoublonnees (le drapeau 0/1 donne le meme coffre). Positions dans le repere des .pos (unites monde).
"""
import glob, json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "chest_positions.json"
sys.path.insert(0, str(ROOT / "tools"))
import evt_vm

TIER_OF_KIND = {0: "A", 1: "B", 2: "C"}
maps = {}
skipped = 0
for f in sorted(glob.glob(str(ROOT / "work/extracted/data/*.evt"))):
    name = Path(f).stem
    d, seq = evt_vm.load(f)
    if not any(t == 0x5F for _, t, _ in seq):
        continue
    entries = [e for e in (struct.unpack_from("<I", d, 4 + 4 * i)[0] for i in range(1024)) if e != 0xFFFFFFFF]
    res, _, _ = evt_vm.explore(seq, entries, watch=(0x5F,))
    seen = {}
    for a in res[0x5F]:
        if None in a[:5]:
            skipped += 1
            continue
        kind, x, y, z, rot = a[:5]
        seen[(int(kind), x, y, z, rot)] = {"kind": int(kind), "tier": TIER_OF_KIND.get(int(kind)), "pos": [x, y, z], "rotation": rot}
    if seen:
        maps[name] = sorted(seen.values(), key=lambda c: (c["kind"], c["pos"]))
OUT.write_text(json.dumps({"provenance": "ROM : opcode 0x5f des .evt, FUN_021c4148 -> FUN_021bd0f4 (voir tools/extraire_positions_coffres.py)",
                           "note": "kind = type de coffre (0 a 2), tier = tiers de tirage (0 A, 1 B, 2 C, prouve sur 35 scripts) ; positions litterales seulement.", "maps": maps}, indent=0) + "\n")
print(len(maps), "cartes,", sum(len(v) for v in maps.values()), "coffres,", skipped, "entrees a arguments variables ignorees")
