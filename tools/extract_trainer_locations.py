#!/usr/bin/env python3
"""Lieux des dresseurs : instructions d'evenement 0x62 (creation d'un acteur dresseur).

Verifie par desassemblage (overlay_0000, base 0x02184b40) :
  - dispatcheur FUN_021c9824 : opcode 0x62 -> FUN_021c1f00 ;
  - FUN_021c1f00 lit 5 arguments (indice de dresseur, x, y, z, +1) puis appelle
    FUN_021caf14 qui cree l'acteur (octet +0x231 = indice, +0x230 = 1, position +0x234..).
Format d'un script .evt : magique "SCR\\0", 4096 o opaques, puis instructions TLV
(u32 type, u32 longueur totale, charge utile). Les 5 arguments sont les 5 instructions 0x15
qui precedent l'opcode ; chacune = (u32 1, f32 numero d'argument, u32 nature, f32 valeur).
Nature 2 = valeur litterale ; l'argument 0 est toujours litteral (378/378) = indice de dresseur.
Combat 0x44 de type 3 (arg 0 = 3) : l'argument 1 est l'indice de dresseur (8 dresseurs de plus : 199-205 et 226).
Le script s001.evt correspond a la carte s001.map (meme identifiant) : c'est le lieu.
Non decode : la position (arguments 1 a 4 = variables 156 a 159 calculees par le script).
"""
import json, struct, glob, os, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "work/extracted/data"
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "trainer_locations.json"

by_map = collections.OrderedDict()
by_trainer = collections.defaultdict(lambda: collections.Counter())
via = {}
for path in sorted(glob.glob(str(D / "*.evt"))):
    name = os.path.basename(path)[:-4]
    d = open(path, "rb").read()
    o = 4 + 0x1000
    seq = []
    while o + 8 <= len(d):
        t, l = struct.unpack_from("<II", d, o)
        if l < 8: break
        seq.append((t, d[o + 8:o + l])); o += l
    for i, (t, p) in enumerate(seq):
        if t == 0x44:
            # Combat type 3 : l'argument 1 est directement l'indice de dresseur (FUN_021c2530, branche 0x021c27ec).
            args = {}
            j = i - 1
            while j >= 0 and seq[j][0] == 0x15 and len(seq[j][1]) == 16:
                _, n, kind, val = struct.unpack("<IfIf", seq[j][1])
                args.setdefault(int(n), (kind, val))
                j -= 1
            if 0 in args and args[0] == (2, 3.0) and 1 in args and args[1][0] == 2:
                idx = int(args[1][1])
                by_map.setdefault(name, collections.Counter())[idx] += 1
                by_trainer[idx][name] += 1
                via.setdefault(idx, set()).add("0x44")
            continue
        if t != 0x62 or i < 5: continue
        pushes = [struct.unpack("<IfIf", x[1]) for x in seq[i - 5:i] if x[0] == 0x15 and len(x[1]) == 16]
        if len(pushes) == 5 and pushes[0][2] == 2:
            idx = int(pushes[0][3])
            by_map.setdefault(name, collections.Counter())[idx] += 1
            by_trainer[idx][name] += 1
            via.setdefault(idx, set()).add("0x62")

out = {
    "provenance": "ROM : instructions d'evenement 0x62 des scripts .evt (voir docstring de tools/extract_trainer_locations.py)",
    "note": "Le lieu est la carte du meme identifiant que le script ; la position exacte n'est pas decodee.",
    "maps": {m: sorted(c) for m, c in by_map.items()},
    "trainers": {str(i): dict(c) for i, c in sorted(by_trainer.items())},
    "via_opcode": {str(i): sorted(v) for i, v in sorted(via.items())},
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", OUT, len(by_map), "cartes,", len(by_trainer), "dresseurs distincts")
