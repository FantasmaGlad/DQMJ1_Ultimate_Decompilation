#!/usr/bin/env python3
"""Extrait les equipes de dresseurs : FldMstrPrm.bin -> MstrPtnTbl.bin (+ BtlMstrPrm.bin brut).

Chaine confirmee par le code (overlay_0000, base 0x02184b40) :
  indice de dresseur i (octet +0x231 d'un acteur de terrain, FUN_021cb89c)
    -> FldMstrPrm[i] (4 o : u16 groupe/classe, u16 cle)               [FUN_021bcf60]
    -> MstrPtnTbl : entree dont le u16 a +0x18 == cle                  [FUN_021ad6bc]
    -> FUN_021ad878 / FUN_021ad7f4 : 3 especes ennemies
    -> requete de combat a 0x0216f544 : +0..+4 = 3 especes, +6 = i    [setter 0x0205438c]
    -> BtlMstrPrm[i] (20 o) copie dans l'etat de combat               [accesseur 0x021e143c]
Entree MstrPtnTbl (26 o) : [0] nombre de monstres ; [1..3] selecteur par emplacement
(>= 0 : indice fixe dans la table d'especes ; < 0 : tirage aleatoire) ; [4..8] et [9..13]
deux tableaux de 5 octets (le premier somme a 100 dans les entrees a tirage : poids en
pourcents probables, non prouve) ; [14..23] 5 x u16 especes ; [24..25] cle.
Les 5 u16 sont des INDICES DANS BtlEnmyPrm.bin (instances de combat : espece, niveau, or, exp, stats),
verifie : niveaux identiques au sein d'une equipe (5,5,5,5,5 ; 15 x5 ; 25 x5) et croissants entre dresseurs.
"""
import json, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}
p, f, b = [(D / n).read_bytes() for n in ("MstrPtnTbl.bin", "FldMstrPrm.bin", "BtlMstrPrm.bin")]

import sys
sys.path.insert(0, str(ROOT / "tools"))
import extract_combat_stats as esc
enemies = list(esc.read_entries((D / "BtlEnmyPrm.bin").read_bytes()))

raw_enemies = (D / "BtlEnmyPrm.bin").read_bytes()
def abilities(v):
    """6 emplacements d'aptitudes de combat (u16 haut de chaque u32 des octets 8-31, 0 = vide, >= 221 = « DUMMY »).
    Noms : message0[600 + id] (5 langues). Coherent avec les attaques connues des monstres (Lump Wizard : Woosh, Heal,
    Frizzle ; Black Dragon : ses trois souffles) mais NON prouve par le code."""
    e = raw_enemies[8 + 88 * v: 8 + 88 * (v + 1)]
    return [x for x in struct.unpack_from("<12H", e, 8)[1::2] if x and x < 221]

def species(v):
    if v == 0: return None
    if v >= len(enemies): return {"btl_enmy_prm_index": v, "unresolved": True}
    e = enemies[v]
    return {"btl_enmy_prm_index": v, "species": by_species.get(e["species_id"]), "species_id": e["species_id"],
            "level": e["level"], "gold": e["gold"], "exp": e["exp"],
            "abilities": abilities(v),
            "stats": {k: e[k] for k in ("max_hp", "max_mp", "attack", "defense", "agility", "wisdom")}}

patterns = {}
for i in range(struct.unpack_from("<I", p, 4)[0]):
    e = p[8 + 26 * i: 8 + 26 * (i + 1)]
    key = struct.unpack_from("<H", e, 24)[0]
    patterns[key] = {
        "count": e[0],
        "selectors": [struct.unpack("b", e[1 + k:2 + k])[0] for k in range(3)],
        "array_a": list(e[4:9]),
        "array_b": list(e[9:14]),
        "enemy_table": [species(x) for x in struct.unpack_from("<5H", e, 14)],
    }

# Modele du dresseur : FUN_021cb028 copie (octet bas du mot de groupe de FldMstrPrm) + 1 dans l'indice de personnage
# de terrain de l'acteur (+0x10e), qui indexe FldChrTbl.bin (413 entrees de 26 o ; u16 [1] = indice de ModelTbl.bin, 12 o
# par nom). Meme mecanisme que pour les monstres de terrain (FUN_021a7e58 : FldEnmyPrm[+2] + 0x3d), verifie sur 810 des
# 853 entrees de FldEnmyPrm. L'octet bas du mot de groupe est aussi la classe (mes_master_name).
fchr = (D / "FldChrTbl.bin").read_bytes()
mt = (D / "ModelTbl.bin").read_bytes()
model_names = [mt[k * 12:(k + 1) * 12].split(b"\0")[0].decode("ascii", "ignore") for k in range(len(mt) // 12)]
def trainer_model(group_word):
    ci = (group_word & 0xFF) + 1
    if ci * 26 + 26 > len(fchr): return None
    mi = struct.unpack_from("<H", fchr, ci * 26 + 2)[0]
    return model_names[mi] if mi < len(model_names) else None

trainers = []
for i in range(struct.unpack_from("<I", f, 4)[0]):
    group, key = struct.unpack_from("<HH", f, 8 + 4 * i)
    if key not in patterns or patterns[key]["count"] == 0:
        continue
    e = b[8 + 20 * i: 8 + 20 * (i + 1)]
    trainers.append({
        "index": i, "field_group_word": group, "model": trainer_model(group), "pattern_key": key,
        "battle_params_raw": {"bytes_0_3": list(e[0:4]), "bytes_4_7": list(e[4:8]),
                              "u32_8": struct.unpack_from("<I", e, 8)[0], "u32_12": struct.unpack_from("<I", e, 12)[0],
                              "bytes_16_19": list(e[16:20])},
        "team": patterns[key],
    })
out = {"provenance": "ROM (FldMstrPrm/MstrPtnTbl/BtlMstrPrm), chaine confirmee par desassemblage - voir docstring de tools/extract_trainer_teams.py",
       "note": "Sens des champs de battle_params_raw, noms et lieux des dresseurs : non prouves.",
       "trainers": trainers}
(OUT / "trainer_teams.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", len(trainers), "dresseurs avec equipe;", sum(1 for t in trainers if any(s and (s.get("unresolved") or s.get("species") is None) for s in t["team"]["enemy_table"])), "avec entrees non resolues")
