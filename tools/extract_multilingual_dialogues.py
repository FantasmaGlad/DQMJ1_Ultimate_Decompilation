#!/usr/bin/env python3
"""Dialogues des scripts .evt dans les 5 langues (.evt = anglais, .evF/.evD/.evI/.evS), alignes par instruction.

Les scripts de chaque langue ont le meme flux d'instructions (memes opcodes, memes positions) : la n-ieme
instruction 0x29 (SetDialog) d'un script est la meme replique dans toutes les langues ; le locuteur est le dernier
0x2A (SpeakerName) qui la precede. On garde les repliques que l'anglais publie deja (locuteur et texte non vides) et
on ajoute les autres langues au meme indice. Decodage : table des .evt (chiffres 0x00-0x09) + accents de
extract_mapping.decode ; codes inconnus laisses en [xx] (codes de controle du moteur de texte).
Sortie : assets/data/i18n/dialogues.json = {script: [{"E": {"speaker","text"}, "F": ..., "D": ..., "I": ..., "S": ...}]}
"""
import json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "work/extracted/data"
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "i18n" / "dialogues.json"
sys.path.insert(0, str(ROOT / "tools"))
import extract_dialogues as ed
from extract_mapping import decode

EXT = {"E": ".evt", "F": ".evF", "D": ".evD", "I": ".evI", "S": ".evS"}

# Signes propres a une langue, deduits par alignement avec l'anglais (dernier caractere de la replique) et par
# contexte : F 0xc9 = "!" (1093/1093 quand l'anglais finit par "!"), 0xce = "?" (656/674), 0x43 = "C cedille" ("[43]a" = Ca),
# 0x97/0x98 = guillemets ouvrant/fermant (« »), D 0xaa = apostrophe fermante, D 0x42 = "A trema", I 0x44 = "E accent grave".
LANG = {
    "F": {0xC9: "!", 0xCE: "?", 0x43: "Ç", 0x97: "«", 0x98: "»"},
    "D": {0xAA: "’", 0x42: "Ä"},
    "I": {0x97: "«", 0x98: "»", 0x44: "È"},
    "S": {0x97: "«", 0x98: "»"},
}

def dec(payload, lang="E"):
    p = payload.split(b"\xff")[0]
    out = []
    for b in p:
        if b in LANG.get(lang, {}): out.append(LANG[lang][b])
        elif b in ed.CHAR_MAP and not (0x56 <= b <= 0x6f or b == 0x55): out.append(ed.CHAR_MAP[b])
        else:
            c = decode(bytes([b]))
            out.append(c.replace("<", "[").replace(">", "]") if c.startswith("<") else c)
    return "".join(out).replace("\n", "\n")

def events(path, lang):
    if not path.exists(): return []
    data = path.read_bytes()
    if data[:4] != b"SCR\x00": return []
    ev, speaker = [], None
    for t, payload in ed.read_instructions(data):
        if t == 0x2A: speaker = dec(payload, lang).strip()
        elif t == 0x29:
            txt = dec(payload, lang).strip()
            if speaker and txt:
                ev.append((speaker, txt))
    return ev

result, misaligned = {}, []
for f in sorted(D.glob("*.evt")):
    sid = f.stem
    per = {l: events(D / f"{sid}{e}", l) for l, e in EXT.items()}
    n = len(per["E"])
    if any(len(v) != n for v in per.values()): misaligned.append(sid)
    rows = []
    for i, (sp, tx) in enumerate(per["E"]):
        if not (sp and tx): continue
        row = {}
        for l, v in per.items():
            if i < len(v) and v[i][1]: row[l] = {"speaker": v[i][0] or sp, "text": v[i][1]}
        rows.append(row)
    if rows: result[sid] = rows
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
print("scripts", len(result), "repliques", sum(len(v) for v in result.values()), "desalignes", misaligned)
