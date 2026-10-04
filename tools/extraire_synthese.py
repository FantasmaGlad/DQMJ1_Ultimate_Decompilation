#!/usr/bin/env python3
"""Extrait les tables de synthese (fusion) de la ROM : overlay_0000.bin + EnmyKindTbl.bin.

Logique retrouvee par desassemblage (Ghidra, overlay_0000, base 0x02184b40) :
  FUN_0218bee8  point d'entree (parent A, parent B, indice de candidat 0/1/2)
  FUN_0218c644  recettes a 4 parents (table de 5 s16 : resultat + 4 parents, fin = 0)
  FUN_0218c430  recettes monstre+monstre (table de 3 s16 : A, B, resultat, fin = -1)
  FUN_0218c3d0  recettes monstre+famille (table de 3 s16 : espece, famille, resultat)
  FUN_0218c0a8  formule generique (valeur = octet 0 de EnmyKindTbl, plafond par famille)
  FUN_0218c344  melange de familles (table de 3 s16 : famA, famB, resultat, defaut 1)
  FUN_0218c4b8  formes Incarnus (dependent de l'avancement de l'histoire)
Sortie : ../DragonQuestMonsterJoker1Bestiaire/assets/data/synthesis_rom.json
"""
import json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
BASE = 0x2184B40
ov = (ROOT / "work/code/overlay_00.bin").read_bytes()
ekt = (ROOT / "work/extracted/data/EnmyKindTbl.bin").read_bytes()
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}

def s16(a): return struct.unpack_from("<h", ov, a - BASE)[0]
def u32(a): return struct.unpack_from("<I", ov, a - BASE)[0]

def table(start, width, stop):
    out, a = [], start
    while s16(a) != stop and len(out) < 1000:
        out.append([s16(a + 2 * i) for i in range(width)])
        a += 2 * width
    return out

# Pointeurs lus dans les pools litteraux des fonctions decompilees.
P_CAP, P_BLACK = u32(0x218C300), u32(0x218C304)
P_MF, P_MM = u32(0x218C42C), u32(0x218C4B4)
P_QUAD, P_MIX = u32(0x218C704), u32(0x218C3CC)

n = struct.unpack_from("<I", ekt, 4)[0]
E = lambda i: ekt[8 + 136 * i: 8 + 136 * (i + 1)]
species = {}
for i in range(n):
    e = E(i)
    if i in by_species:
        species[by_species[i]] = {"species_id": i, "value": e[0], "family_id": e[4] >> 4}

def ref(sid): return by_species.get(sid)

black, a = [], P_BLACK
while s16(a) != -1:
    black.append(s16(a)); a += 2

data = {
    "provenance": "ROM (overlay_0000.bin, desassemblage) - voir tools/extraire_synthese.py",
    "family_names": {"1": "Slime", "2": "Dragon", "3": "Nature", "4": "Beast",
                     "5": "Material", "6": "Demon", "7": "Undead", "8": "Wildcard"},
    "family_mix": [{"a": x, "b": y, "result": z} for x, y, z in table(P_MIX, 3, -1)],
    "family_mix_default": 1,
    "family_cap_species": {str(f): ref(s16(P_CAP + 2 * f)) for f in range(1, 8)},
    "excluded_from_generic": [ref(x) for x in black],
    "special_monster_family": [{"monster": ref(x), "family_id": f, "result": ref(r), "raw": [x, f, r]} for x, f, r in table(P_MF, 3, -1)],
    "special_monster_monster": [{"a": ref(x), "b": ref(y), "result": ref(r), "raw": [x, y, r]} for x, y, r in table(P_MM, 3, -1)],
    "quadrilinear": [{"result": ref(r[0]), "parents": [ref(p) for p in r[1:]], "raw": r} for r in table(P_QUAD, 5, 0)],
    "incarnus": {
        "note": "FUN_0218c4b8 : parent famille 8 (Wildcard). Forme selon la famille du partenaire ; variante Ace si valeur du partenaire >= 0x8a et avancement histoire > 5.",
        "by_partner_family": {"3": ["m176", "m180"], "4": ["m179", "m183"], "5": ["m178", "m182"], "6": ["m177", "m181"]},
        "ace_partner_min_value": 0x8A,
        "wulfspade_ace_plus": {"m043": "m180b", "m044": "m180c"},
    },
    "species": species,
    # Table complete (352 especes) telle que lue par le code : [valeur (octet 0), id de famille (nibble haut de l'octet 4)].
    # Necessaire a la formule generique (recherche de l'espece de valeur v).
    "all_species_value_family": [[E(i)[0], E(i)[4] >> 4] for i in range(n)],
}
bad = [k for k in ("family_cap_species", "excluded_from_generic") for v in (data[k].values() if isinstance(data[k], dict) else data[k]) if v is None]
(OUT / "synthesis_rom.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ecrit", OUT / "synthesis_rom.json", {k: len(v) for k, v in data.items() if isinstance(v, (list, dict))}, "non resolus:", bad)
