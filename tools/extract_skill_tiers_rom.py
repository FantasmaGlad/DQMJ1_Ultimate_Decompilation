#!/usr/bin/env python3
"""Paliers de competences lus dans SkillTbl.bin -> assets/data/skill_tiers_rom.json (remplace la source wiki).

Structure d'une entree (194 x 240 octets apres l'en-tete « SKIL » + u32 nombre, prouvee par concordance avec le wiki
sur les paliers a sorts et par les noms de message0) :
  u16[1]                     points pour maitriser le palier (= dernier cumul)
  u16[2 + 2k], u16[3 + 2k]   k = 0..9 : (points ajoutes, points cumules) du deblocage k ; 0 = emplacement inutilise
  u16[22 + 6k .. 27 + 6k]    sort du deblocage k : [id d'aptitude, pre-requis 1, pre-requis 2, 0, ordre, 0] ;
                             nom = message0[600 + id], description = message0[885 + id] (Heal 632 -> 917)
  u16[82 + 2k]               effet passif du deblocage k (si pas de sort) : octet bas = id d'effet, octet haut =
                             pre-requis ; nom = message0[1912 + id] : 1..27 talents, 128..187 bonus de caracteristiques
                             (blocs de 10 : PV 128, PM 138, Attaque 148, Defense 158, Agilite 168, Sagesse 178),
                             188..214 gardes (resistances)
Valeurs des bonus : PV/PM [5,10,20,30,50,60,70,80,90,100], autres [3,5,10,20,25,30,35,40,45,50] (recoupees avec le wiki,
54 identifiants d'effet observes).
"""
import json, re, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
from extract_mapping import decode

LANGS = "EFDIS"
P = {l: [x.strip() for x in decode((D / f"message0.bin{l}").read_bytes()).split("|")] for l in LANGS}


def clean(s, l):
    s = s.replace("<ad>", "&" if l == "E" else "").replace("<8d>", " II").replace("<8e>", " III").replace("<fe>", " ")
    s = s.replace("<45>", "É").replace("<49>", "Í")
    return re.sub(r"\s+", " ", re.sub(r"<[0-9a-f]{2}>", "", s)).strip()


def msg(i, l):
    return clean(P[l][i], l) if 0 <= i < len(P[l]) else ""


def names(i):
    return {l: msg(i, l) for l in LANGS}


STATS = [("hp", 128, 2040, [5, 10, 20, 30, 50, 60, 70, 80, 90, 100]), ("mp", 138, 2050, [5, 10, 20, 30, 50, 60, 70, 80, 90, 100]),
         ("attack", 148, 2060, None), ("defense", 158, 2070, None), ("agility", 168, 2080, None), ("wisdom", 178, 2090, None)]
SMALL = [3, 5, 10, 20, 25, 30, 35, 40, 45, 50]


def effect(e):
    if 1 <= e <= 27:
        return {"kind": "trait", "effect_id": e, "name": names(1912 + e)}
    for stat, base, lab, vals in STATS:
        if base <= e < base + 10:
            n = (vals or SMALL)[e - base]
            label = {l: re.sub(r"\s*\+?\s*$", "", msg(lab, l)) for l in LANGS}
            return {"kind": "stat", "effect_id": e, "stat": stat, "bonus": n, "name": {l: f"{label[l]} +{n}" for l in LANGS}}
    if 188 <= e <= 214:
        return {"kind": "guard", "effect_id": e, "name": names(1912 + e)}
    return {"kind": "unknown", "effect_id": e, "name": {l: "" for l in LANGS}}


def main():
    b = (D / "SkillTbl.bin").read_bytes()
    assert b[:4] == b"SKIL" and struct.unpack_from("<I", b, 4)[0] == 194 and len(b) == 8 + 194 * 240
    skills_pub = json.loads((OUT / "skills.json").read_text(encoding="utf-8"))
    wiki = json.loads((OUT / "skill_tiers_wiki.json").read_text(encoding="utf-8"))
    out, cmp_ok, cmp_n, unknown = {}, 0, 0, 0
    for k, v in skills_pub.items():
        sid = v["skill_id"]
        u = struct.unpack_from("<120H", b, 8 + 240 * sid)
        unlocks = []
        for i in range(10):
            inc, cum = u[2 + 2 * i], u[3 + 2 * i]
            if inc == 0:
                continue
            grp = u[22 + 6 * i: 28 + 6 * i]
            if grp[0]:
                aid = grp[0]
                item = {"kind": "ability", "ability_id": aid, "name": names(600 + aid), "description": names(885 + aid),
                        "requires": [{"ability_id": x, "name": names(600 + x)} for x in grp[1:3] if x]}
            else:
                raw = u[82 + 2 * i]
                item = effect(raw & 0xFF)
                item["requires"] = [{"effect_id": raw >> 8, "name": names(1912 + (raw >> 8))}] if raw >> 8 else []
            unknown += item["kind"] == "unknown"
            item.update({"points": cum, "points_added": inc})
            unlocks.append(item)
        out[str(sid)] = {"skill_id": sid, "tier": v["tier"], "base_name": v["base_name"], "points_to_master": u[1], "unlocks": unlocks}
        w = wiki.get(v["base_name"]) if isinstance(wiki.get(v["base_name"]), dict) else None
        wt = [t for t in (w or {}).get("tiers", []) if t["tier"] == v["tier"]]
        if wt:
            cmp_n += 1
            cmp_ok += [(x["points"], x["name"].lower()) for x in wt[0]["unlocks"]] == [(x["points"], x["name"]["E"].lower()) for x in unlocks]
    dest = OUT / "skill_tiers_rom.json"
    dest.write_text(json.dumps({"provenance": "ROM : SkillTbl.bin + message0, voir tools/extract_skill_tiers_rom.py", "skills": out},
                               ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print("competences", len(out), "| identiques au wiki (points + noms)", cmp_ok, "/", cmp_n, "| effets inconnus", unknown)


if __name__ == "__main__":
    main()
