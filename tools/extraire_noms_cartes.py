#!/usr/bin/env python3
"""Noms de lieux des cartes : banque mes_map_name.binE (mes_mapname.binE), 91 entrees.

Rattachement (INFERE, non confirme par du code) :
  - donjons d* (30 cartes) : les entrees 22 a 51 dans l'ordre des identifiants (comptes egaux, et la
    structure des noms concorde : Palaish Shrine x4 = d031-d034, Temple du Soleil x3 + Temple de la Lune x3 =
    d041-d046, CELL Headquarters x4 = d051-d054, Tartarus x8 = d071-d078) ;
  - iles s* (22 cartes) : les entrees 0 a 21 sont des noms d'ile ; l'ile de chaque carte est deduite du
    graphe des warps (s -> donjon d'une ile connue) et des comptes (Infant 2, Xeroph 1, Domus 3, Palaish 5,
    Celeste 4, Fert 3, Infern 4 = 22 = nombre de cartes s*) ;
  - les autres series (e, f, h, i, k, o, t : 38 cartes, entrees 52 a 90) : ordre inconnu, sans nom.
Sortie : assets/data/map_names.json (avec le score de coherence des warps).
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from extraire_mapping import decode  # noqa: E402

OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "map_names.json"
bank = [x.strip() for x in decode((ROOT / "work/extracted/data/mes_mapname.binE").read_bytes()).split("|")]
maps = sorted(m for m in os.listdir(ROOT / "work/maps") if (ROOT / "work/maps" / m).is_dir())
D = [m for m in maps if m[0] == "d"]
assert len(D) == 30

def clean(n):
    n = n.replace(" <96> ", " - ").replace(" <02>", " 2").replace(" <03>", " 3").replace(" <04>", " 4").replace(" <96>", " -").strip()
    return re.sub(r"\s*<[0-9a-f]{2}>", "", n).strip()

names = {}
for i, m in enumerate(D):
    names[m] = {"name": clean(bank[22 + i]), "basis": "order of dungeon files vs bank entries 22-51"}

ISLAND = {"Infant": ["s001", "s091"], "Xeroph": ["s011"], "Domus": ["s021", "s022", "s023"],
          "Palaish": ["s031", "s032", "s033", "s034", "s035"], "Celeste": ["s041", "s042", "s043", "s044"],
          "Fert": ["s051", "s052", "s053"], "Infern": ["s061", "s062", "s071", "s072"]}
# comptes : chaque ile a autant de cartes que d'entrees de meme nom dans la banque (0-21)
for isl, ids in ISLAND.items():
    n = sum(1 for b in bank[:22] if b.startswith(isl))
    assert n == len(ids), (isl, n, len(ids))
    for m in ids:
        names[m] = {"name": f"{isl} Isle", "basis": "island group: bank counts and warp graph"}
assert set(m for m in maps if m[0] == "s") == set(k for k in names if k[0] == "s")

# verification : warps s -> d dont le nom de donjon designe une ile (hors Temples et CELL, ile non nommee)
marks = json.loads((OUT.parent / "map_markers.json").read_text(encoding="utf-8"))["maps"]
def island_of_dungeon(n):
    for isl in ISLAND:
        if n.startswith(isl): return isl
    return {"Temple": "Celeste"}.get(n.split(" ")[0])
ok = bad = 0
detail = []
for s, mk in marks.items():
    if s[0] != "s": continue
    for w in mk:
        t = w.get("target_map")
        if t and t[0] == "d":
            isl = island_of_dungeon(names[t]["name"])
            if isl is None: continue
            good = names[s]["name"].startswith(isl)
            ok += good; bad += not good
            if not good: detail.append((s, names[s]["name"], t, names[t]["name"]))
out = {"provenance": "mes_mapname.binE ; rattachement infere (voir docstring de tools/extraire_noms_cartes.py)",
       "bank": bank, "maps": names,
       "verification": {"warps_s_to_d_coherent": ok, "warps_s_to_d_incoherent": bad, "incoherent_details": detail}}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", OUT, len(names), "cartes nommees ; warps coherents", ok, "incoherents", bad, detail)
