#!/usr/bin/env python3
"""Points d'apparition des dresseurs : execution exploratoire des scripts d'evenements (.evt).

Machine virtuelle des scripts (desassemblee dans overlay_0000, dispatcheur FUN_021cad7c) :
  operandes = (nature, valeur flottante) ; nature 0 = variable, 1 = argument, 2 = litteral, 3 = tableau ;
  0x15 affectation dest := src ; 0x16-0x1a arithmetique ; 0x0f-0x14 comparaisons (drapeau) ;
  0x0c saut ; 0x0d saut si vrai ; 0x0e saut si faux ; 0x09 appel ; 0x02 retour.
  Les cibles de saut sont des decalages depuis le debut du flux (fichier - 0x1004) : 1073/1073 valides sur s001.
  L'en-tete de 4096 o est la table des points d'entree (u32, 0xFFFFFFFF = aucun).
L'instruction 0x62 (creation d'un dresseur, FUN_021c1f00) prend 5 arguments : indice de dresseur, puis x, y, z et
un angle (variables 156 a 159). On explore le graphe de controle depuis chaque point d'entree, en suivant les deux
branches des conditions (l'etat de jeu est inconnu), et on releve pour chaque 0x62 l'indice et les variables 156-159.
Validation : la hauteur y coincide avec la hauteur du terrain du GLB de la carte (tools/optimiser).
Les variables de position ne sont pas fixes (156-159 sur s001, 177-180 sur s011) : on suit toutes les variables.
Sortie : assets/data/trainer_spawns.json
"""
import collections, glob, json, os, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "work/extracted/data"
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "trainer_spawns.json"

import sys
sys.path.insert(0, str(ROOT / "tools"))
from evt_vm import load, explore

maps = {}
for f in sorted(glob.glob(str(D / "*.evt"))):
    name = os.path.basename(f)[:-4]
    d, seq = load(f)
    if not any(t == 0x62 for _, t, _ in seq): continue
    ent = sorted({v for v in struct.unpack("<%dI" % (0x1000 // 4), d[4:4 + 0x1000]) if v != 0xFFFFFFFF})
    raw, rawctx, steps = explore(seq, ent, watch=(0x62,))
    res = collections.defaultdict(set)
    for a in raw.get(0x62, ()):
        res[a[0]].add(tuple(a[1:5]))
    ctx = {(k[1][0], tuple(k[1][1:5])): v for k, v in rawctx.items() if k[0] == 0x62}
    points = []; per = {}; contexts = {}
    for idx, sets in sorted(res.items(), key=lambda kv: (kv[0] is None, kv[0])):
        if idx is None: continue
        ids = []
        for v in sorted(sets, key=lambda x: str(x)):
            if None in v: continue
            pt = {"pos": [v[0], v[1], v[2]], "angle": v[3]}
            if pt not in points: points.append(pt)
            ids.append(points.index(pt))
            contexts.setdefault(str(int(idx)), {}).setdefault(str(points.index(pt)), sorted(ctx[(idx, tuple(v))]))
        per[str(int(idx))] = sorted(set(ids))
    maps[name] = {"spawn_points": points, "trainers": per, "context": contexts, "explored_steps": steps}
OUT.write_text(json.dumps({"provenance": "ROM : execution exploratoire des scripts .evt (voir docstring de tools/extraire_positions_dresseurs.py)",
    "note": "Chaque dresseur d'une carte peut apparaitre a l'un des points listes ; le choix depend de l'etat du jeu, non decode.",
    "maps": maps}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", OUT, {m: (len(v["spawn_points"]), len(v["trainers"])) for m, v in maps.items()})
