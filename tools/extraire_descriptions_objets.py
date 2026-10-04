#!/usr/bin/env python3
"""Descriptions d'objets en 5 langues -> assets/data/i18n/item_descriptions.json.

Source : messageEXPL.bin? (E, F, D, I, S), description de l'objet `item_id` a l'indice 8 + item_id (entrees 0 a 7 = categories
d'equipement). Verifie : pour les 126 objets nommes, la premiere phrase de la description est le nom de l'objet (98 exacts, les
28 autres sont des noms abreges de la table d'objets contre le nom complet). Les nombres inseres par le moteur (codes de controle)
ne sont pas resolus : « Restores  HP » garde un espace double reduit a un espace.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from extraire_mapping import decode

LANGS = "EFDIS"


def clean(s):
    s = s.replace("<fe>", " ").replace("<45>", "É").replace("<49>", "Í")
    return re.sub(r"\s+", " ", re.sub(r"<[0-9a-f]{2}>", "", s)).strip()


def dehyphen(s):
    """Coupures de ligne de la banque allemande (« einzel- nen », « Metall- monster ») : recolle, sauf « und » / « oder »."""
    return re.sub(r"(?<=[a-z\u00e4\u00f6\u00fc\u00df])- (?!(?:und|oder|bzw)\b)(?=[a-z\u00e4\u00f6\u00fc])", "", s)


B = {l: [(dehyphen(clean(x)) if l == "D" else clean(x)) for x in decode((D / f"messageEXPL.bin{l}").read_bytes()).split("|")] for l in LANGS}
items = json.loads((OUT / "items.json").read_text(encoding="utf-8"))
out, ok = {}, 0
for k, v in items.items():
    i = 8 + v["item_id"]
    d = {l: B[l][i] if i < len(B[l]) else "" for l in LANGS}
    if d["E"]:
        out[str(v["item_id"])] = d
        ok += d["E"].split(".")[0].strip().lower() == v["name_en"].lower()
(OUT / "i18n" / "item_descriptions.json").write_text(json.dumps({"provenance": "ROM : messageEXPL.bin? (indice 8 + item_id), voir tools/extraire_descriptions_objets.py", "items": out}, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
print("descriptions", len(out), "/", len(items), "| nom identique au nom publie", ok)
