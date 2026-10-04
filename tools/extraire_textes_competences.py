#!/usr/bin/env python3
"""Textes ROM des competences en 5 langues (E, F, D, I, S) -> assets/data/i18n/skills_texts.json.

Sources (alignees par indice, verifiees contre les noms anglais deja publies dans skills.json) :
  nom complet d'une competence   : message0[1141 + skill_id]
  description d'une competence   : message0[1398 + skill_id] ("Nom." puis phrases, sauts de ligne <fe> -> espace)
  (les paliers debloques viennent de SkillTbl.bin : voir extraire_paliers_competences_rom.py)
  talents de monstre (traits)   : message0[1913..1939]
Codes de controle : <ad> = « & » (anglais), <8d> = II, <8e> = III (tables des .evt), <fe> = saut de ligne,
<45> = E accent aigu majuscule (F « Elec », « Eclair »), <49> = I accent aigu majuscule (S « Igneo »).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from extraire_mapping import decode

LANGS = "EFDIS"
P = {l: [x.strip() for x in decode((D / f"message0.bin{l}").read_bytes()).split("|")] for l in LANGS}


def clean(s, l):
    s = s.replace("<ad>", "&" if l == "E" else "").replace("<8d>", " II").replace("<8e>", " III").replace("<fe>", " ")
    s = s.replace("<45>", "É").replace("<49>", "Í")
    s = re.sub(r"<[0-9a-f]{2}>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def get(i, l):
    return clean(P[l][i], l) if 0 <= i < len(P[l]) else ""


def by_lang(fn):
    return {l: fn(l) for l in LANGS}


skills_pub = json.loads((OUT / "skills.json").read_text(encoding="utf-8"))
skills, ok_name = {}, 0
for k, v in skills_pub.items():
    i = v["skill_id"]
    name = by_lang(lambda l: get(1141 + i, l))
    desc = by_lang(lambda l: get(1398 + i, l))
    ok_name += name["E"].replace("  ", " ") == v["name_display_en"].replace("  ", " ")
    skills[str(i)] = {"name": name, "description": desc}
print("competences", len(skills), "noms E concordants avec le wiki", ok_name)

E_clean = [get(i, "E").lower() for i in range(len(P["E"]))]

# Talents de monstre (« traits » du wiki) : noms message0[1913..1939]
tr_pub = json.loads((OUT / "monster_resistances_traits.json").read_text(encoding="utf-8"))
trait_names = sorted({t for v in tr_pub.values() if isinstance(v, dict) for t in v.get("traits", [])})
traits, trait_missing = {}, []
for n in trait_names:
    idx = [i for i in range(1913, 1940) if E_clean[i] == n.lower()]
    if idx:
        traits[n] = by_lang(lambda l: get(idx[0], l))
    else:
        trait_missing.append(n)
print("talents traduits", len(traits), "/", len(trait_names), "absents", trait_missing)

out = {
    "provenance": "ROM : message0 (E, F, D, I, S), voir docstring de tools/extraire_textes_competences.py",
    "skills": skills,
    "traits": traits,
    "not_in_rom": trait_missing,
}
(OUT / "i18n" / "skills_texts.json").write_text(json.dumps(out, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")

