#!/usr/bin/env python3
"""Combats de dresseurs des scripts (opcode 0x44 de types 2, 3, 6, 8) -> assets/data/trainer_battles.json.

Semantique (desassemblage de FUN_021c2530, overlay_0000) : types 3, 6 et 8 lisent l'argument 1 comme indice de dresseur et appellent
FUN_021ad878 (equipe de MstrPtnTbl) ; modes de combat ecrits : type 3 -> 0x11 (scenarise), 6 -> 0x01 (standard), 8 -> 0x21 (boss).
Le type 2 prend l'acteur de terrain (+0x231) et n'a pas d'indice litteral : ignore ici.
"""
import glob, json, os, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "work/extracted/data"
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "trainer_battles.json"
MODE = {3: 0x11, 6: 0x01, 8: 0x21}
res = {}
for path in sorted(glob.glob(str(D / "*.evt"))):
    name = os.path.basename(path)[:-4]
    d = open(path, "rb").read()
    o, seq = 4 + 0x1000, []
    while o + 8 <= len(d):
        t, l = struct.unpack_from("<II", d, o)
        if l < 8:
            break
        seq.append((o - 0x1004, t, d[o + 8:o + l]))
        o += l
    for i, (off, t, p) in enumerate(seq):
        if t != 0x44:
            continue
        args, j = {}, i - 1
        while j >= 0 and seq[j][1] == 0x15 and len(seq[j][2]) == 16:
            _, n, kind, val = struct.unpack("<IfIf", seq[j][2])
            args.setdefault(int(n), (kind, val))
            j -= 1
        if 0 in args and args[0][0] == 2 and int(args[0][1]) in MODE and 1 in args and args[1][0] == 2:
            res.setdefault(name, []).append({"offset": off, "type": int(args[0][1]), "battle_mode": MODE[int(args[0][1])], "trainer_index": int(args[1][1])})
OUT.write_text(json.dumps({"provenance": "ROM : instruction 0x44 des .evt, types 3, 6, 8 (voir docstring de tools/extraire_combats_dresseurs.py)", "scripts": res}, indent=0) + "\n")
n = sum(len(v) for v in res.values())
print(n, "combats dans", len(res), "scripts")
import collections
c = collections.Counter((b["type"]) for v in res.values() for b in v); print(dict(c))
for s, v in res.items():
    for b in v:
        if b["type"] == 8: print(s, b)
