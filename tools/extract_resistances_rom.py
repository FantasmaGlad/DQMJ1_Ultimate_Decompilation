#!/usr/bin/env python3
"""Resistances par espece lues dans EnmyKindTbl.bin (ROM), noms de categories recoupes avec le wiki.

Lecture prouvee par le code (FUN_021c4f98, overlay_0000) : les u32 aux offsets 0x44, 0x48, 0x4c, 0x50 de
l'entree sont decoupes en quartets (8 par u32, poids faible d'abord) et copies dans l'instance (+0x32...) :
32 quartets, dont 27 utilises (les 5 derniers valent 0). Valeurs observees : 0, 1, 5, 7.
Noms et sens des valeurs : ordre de mes_taisei.binE (27 blocs de 8 libelles), CONFIRME par recoupement avec le
wiki (monster_resistances_traits.json) : accord affiche a l'execution ; 5 = immunise, 7 = soigne, 0 = vulnerable.
Les octets 0x28-0x3f (six groupes de 4 octets) sont les motifs de croissance de stats, identiques au wiki
pour 208 especes sur 209 (m097 differe) : confirmation ROM independante de monster_level_growth.json.
Sortie : assets/data/monster_resistances_rom.json
"""
import json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
wiki = json.loads((OUT / "monster_resistances_traits.json").read_text(encoding="utf-8"))
data = (D / "EnmyKindTbl.bin").read_bytes()

def nibbles(sid):
    e = data[8 + 136 * sid: 8 + 136 * (sid + 1)]
    out = []
    for off in (0x44, 0x48, 0x4C, 0x50):
        w = struct.unpack_from("<I", e, off)[0]
        out += [(w >> (4 * j)) & 15 for j in range(8)]
    return out[:27]

rows = {k: nibbles(v["monster_id"]) for k, v in mapping.items() if k in wiki and v["monster_id"] > 0}
cats = set()
for v in wiki.values():
    for s in v["resistances"]:
        for pre in ("Vulnerable to ", "Healed by "):
            if s.startswith(pre): cats.add(s[len(pre):])
        if s.endswith("proof"): cats.add(s[:-5])

def flags(k, c):
    s = wiki[k]["resistances"]
    return (f"{c}proof" in s, f"Healed by {c}" in s, f"Vulnerable to {c}" in s)

# Ordre des 27 categories : banque de texte mes_taisei.binE, 8 libelles par categorie (Vulnerable to X, vide,
# 3 degres de degats reduits, Xproof, Reflects X, Healed by X) -> la valeur du quartet 0..7 indexe ce bloc.
sys.path.insert(0, str(ROOT / "tools"))
from extract_mapping import decode  # noqa: E402
bank = [x.strip() for x in decode((D / "mes_taisei.binE").read_bytes()).split("|")]
names = {i: {"name": bank[8 * i].replace("Vulnerable to ", "")} for i in range(27)}
agree_tot = agree_ok = 0
for i, c in names.items():
    for k, n in rows.items():
        for flag, val in zip(flags(k, c["name"]), (5, 7, 0)):
            if flag: agree_tot += 1; agree_ok += n[i] == val
monsters = {k: nibbles(v["monster_id"]) for k, v in mapping.items() if v["monster_id"] > 0}
res = {"provenance": "ROM (EnmyKindTbl, u32 0x44-0x50 en quartets) ; noms de categories recoupes avec le wiki, voir docstring de tools/extract_resistances_rom.py",
       "value_meaning": {"0": "vulnerable", "1": "normal", "2": "reduced damage (level 1)", "3": "reduced damage (level 2)", "4": "reduced damage (level 3)", "5": "immune", "6": "reflects", "7": "heals"},
       "value_note": "Libelles par bloc de 8 dans mes_taisei.binE ; seules les valeurs 0, 1, 5, 7 sont observees.",
       "categories": {str(i): names[i] for i in range(27)},
       "monsters": monsters}
(OUT / "monster_resistances_rom.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("categories", len(names), "(noms lus dans mes_taisei) ; accord avec le wiki", agree_ok, "/", agree_tot)
