#!/usr/bin/env python3
"""Toutes les banques de texte mes_*.bin{E,F,D,I,S} de la ROM, alignees par indice.

Le jeu embarque 5 langues (E anglais, F francais, D allemand, I italien, S espagnol) ; chaque banque a le meme
nombre d'entrees dans chaque langue (a 1 pres pour quelques banques). Decodage : extract_mapping.decode
(caracteres inconnus laisses en <xx>). Sortie : assets/data/i18n/<banque>.json = {"E": [...], "F": [...], ...}
et assets/data/i18n/_index.json (nombre d'entrees, codes inconnus par langue).
"""
import collections, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "i18n"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from extract_mapping import decode

OUT.mkdir(parents=True, exist_ok=True)
banks = sorted({p.name.split(".bin")[0] for p in D.glob("mes_*.bin?")})
index = {}
unknown = {l: collections.Counter() for l in "EFDIS"}
for b in banks:
    langs = {}
    for l in "EFDIS":
        f = D / f"{b}.bin{l}"
        if not f.exists(): continue
        entries = decode(f.read_bytes()).split("|")
        if entries and entries[-1] == "": entries = entries[:-1]
        langs[l] = entries
        for e in entries:
            for c in re.findall(r"<([0-9a-f]{2})>", e): unknown[l][c] += 1
    (OUT / f"{b}.json").write_text(json.dumps(langs, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    index[b] = {l: len(v) for l, v in langs.items()}
(OUT / "_index.json").write_text(json.dumps({"banks": index, "unknown_codes": {l: dict(c.most_common(30)) for l, c in unknown.items()}}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(banks), "banques ;", {l: sum(unknown[l].values()) for l in unknown})
for l in "FDIS": print(l, unknown[l].most_common(12))
