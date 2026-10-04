#!/usr/bin/env python3
"""Traductions ROM (E, F, D, I, S) des jeux de donnees du site, alignees par indice de banque.

Sources (indices verifies contre les champs anglais deja publies, nombre de concordances affiche) :
  monstres : nom = message0[64 + monster_id] ; description = mes_know[monster_id]
  objets   : nom = message0[1654 + item_id]
  competences : nom court = mes_skillomitname[skill_id]
  surnoms  : mes_random_monster_name (4 par espece)
  cartes   : entrees de mes_mapname retrouvees par egalite avec le nom anglais publie
  dresseurs : mes_master_name[classe]
  resistances : mes_taisei, 8 libelles par categorie
  indices / rumeurs : mes_hint, mes_bbs (banques entieres)
Nettoyage : codes de controle <xx> retires des noms ; noms de monstres en casse titre (F par format_fr, E par format_en,
autres langues : premiere lettre en majuscule).
Sortie : assets/data/i18n/entities.json
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from extraire_mapping import decode, format_en, format_fr

LANGS = "EFDIS"
def bank(name):
    out = {}
    for l in LANGS:
        f = D / f"{name}.bin{l}"
        t = [x.strip() for x in decode(f.read_bytes()).split("|")]
        out[l] = t
    return out

def strip_codes(s):
    s = s.replace("<8d>", " II").replace("<8e>", " III")  # chiffres romains (table des .evt : 0x8D = II, 0x8E = III)
    s = s.replace("<fe>", " ")  # saut de ligne
    s = s.replace("<45>", "\u00c9").replace("<49>", "\u00cd")  # E / I accent aigu majuscules (F « Elec », S « Igneo »), suite 57
    return re.sub(r"\s*<[0-9a-f]{2}>", "", s).strip()
def cap(s): return s[:1].upper() + s[1:]
def get(b, i, l): return b[l][i] if 0 <= i < len(b[l]) else ""
def by_lang(fn): return {l: fn(l) for l in LANGS}

msg0 = bank("message0")
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
know = bank("mes_know")
def mname(mid, l):
    raw = strip_codes(get(msg0, 64 + mid, l))
    return format_en(raw) if l == "E" else format_fr(raw) if l == "F" else cap(raw)
monsters, ok_name = {}, 0
for k, v in mapping.items():
    mid = v["monster_id"]
    if mid <= 0: continue
    names = by_lang(lambda l: mname(mid, l))
    ok_name += names["E"] == v["nom_en"]
    monsters[k] = {"name": names, "description": by_lang(lambda l: strip_codes(get(know, mid, l)).replace("�", ""))}
print("monstres", len(monsters), "noms E concordants", ok_name, "/", len(monsters))

items_pub = json.loads((OUT / "items.json").read_text(encoding="utf-8"))
items, ok = {}, 0
for k, v in items_pub.items():
    n = by_lang(lambda l: strip_codes(get(msg0, 1654 + v["item_id"], l)))
    ok += n["E"].lower() == v["name_en"].lower()
    items[k] = {"name": n}
print("objets", len(items), "concordants", ok)

sk_pub = json.loads((OUT / "skills.json").read_text(encoding="utf-8"))
sko = bank("mes_skillomitname")
skills, ok = {}, 0
for k, v in sk_pub.items():
    n = by_lang(lambda l: strip_codes(get(sko, v["skill_id"], l)))
    ok += n["E"] == strip_codes(v["name_short_en"])
    skills[k] = {"short_name": n}
print("competences", len(skills), "concordantes", ok)

nick = bank("mes_random_monster_name")
nick_pub = json.loads((OUT / "monster_nicknames.json").read_text(encoding="utf-8"))
E_list = nick["E"]; nicknames, ok = {}, 0
for k, names in nick_pub.items():
    mid = mapping[k]["monster_id"] if k in mapping else None
    if not mid: continue
    idx = [i for i in range(len(E_list)) if E_list[i] == names[0] and E_list[i:i + 4] == names]
    if idx and idx[0] % 4 == 0 and idx[0] // 4 in (mid, mid - 1):
        ok += 1
    if idx: nicknames[k] = by_lang(lambda l: [strip_codes(x) for x in nick[l][idx[0]: idx[0] + 4]])
print("surnoms", len(nicknames), "/", len(nick_pub), "alignes sur l'indice espece", ok)

mm = bank("mes_mapname")
def clean_map(n):
    n = n.replace(" <96> ", " - ").replace(" <02>", " 2").replace(" <03>", " 3").replace(" <04>", " 4").replace(" <96>", " -")
    return strip_codes(n)
maps_pub = json.loads((OUT / "map_names.json").read_text(encoding="utf-8"))["maps"]
E_clean = [clean_map(x) for x in mm["E"]]
maps, miss = {}, 0
for k, v in maps_pub.items():
    if v["name"] in E_clean:
        i = E_clean.index(v["name"])
        maps[k] = by_lang(lambda l: clean_map(get(mm, i, l)))
    else: miss += 1
print("cartes", len(maps), "sans correspondance", miss)

mmn = bank("mes_master_name")
trainer_classes = by_lang(lambda l: [strip_codes(x) for x in mmn[l]])
taisei = bank("mes_taisei")
resist = {i: by_lang(lambda l: re.sub(r"^(Vulnerable to|Vulnérable|Verletzlich|Debole|Vulnerable) ", "", strip_codes(taisei["E"][8 * i])) if l == "E" else strip_codes(taisei[l][8 * i])) for i in range(27)}
abilities = {str(i): by_lang(lambda l: strip_codes(get(msg0, 600 + i, l))) for i in range(1, 221)}
hints = bank("mes_hint"); bbs = bank("mes_bbs")
out = {"provenance": "ROM : banques message0/mes_* dans 5 langues, voir docstring de tools/extraire_traductions.py",
       "languages": {"E": "en", "F": "fr", "D": "de", "I": "it", "S": "es"},
       "monsters": monsters, "items": items, "skills": skills, "nicknames": nicknames, "maps": maps,
       "trainer_classes": trainer_classes, "resistance_categories": resist, "abilities": abilities, "resistance_labels": {l: [strip_codes(x) for x in taisei[l]] for l in LANGS},
       "hints": {l: [strip_codes(x)for x in hints[l]] for l in LANGS}, "rumors": {l: [strip_codes(x) for x in bbs[l]] for l in LANGS}}
(OUT / "i18n" / "entities.json").write_text(json.dumps(out, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
