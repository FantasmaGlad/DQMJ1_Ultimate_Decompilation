#!/usr/bin/env python3
"""Combats a ennemis fixes des scripts d'evenements (.evt) : instruction 0x44, types 0, 1, 4 et 7.

Semantique lue dans FUN_021c2530 (overlay_0000, gestionnaire de 0x44) : l'argument 0 est le type ;
pour les types 0, 1, 4 et 7 les arguments 1 a 3 sont trois valeurs d'ennemis (0 = emplacement vide)
passees telles quelles au setter de requete de combat 0x0205438c (le meme que pour un dresseur,
qui y passe les trois especes tirees de MstrPtnTbl) ; ce sont donc des indices de BtlEnmyPrm.bin.
Les arguments 4 et 5 sont transmis (drapeaux, sens non prouve). Le type 3 prend un indice de dresseur,
le type 2 l'acteur, le type 5 un jeu d'equipes de 3 monstres copie depuis une table (non decode ici).
Les arguments sont les 6 affectations 0x15 (nature 1) qui precedent 0x44 ; seuls les litteraux sont retenus.
Sortie : assets/data/fixed_battles.json
"""
import collections, glob, json, os, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data"
D = ROOT / "work/extracted/data"
sys.path.insert(0, str(ROOT / "tools"))
import extraire_stats_combat as esc
mapping = json.loads((OUT / "monsters-mapping.json").read_text(encoding="utf-8"))
by_species = {v["monster_id"]: k for k, v in mapping.items()}
# Especes internes propres aux combats de boss scriptes (formes de combat)
BOSS_SPECIES = {
    84: "m225",   # Grand Dragon (sanctuaire)
    176: "m036",  # Orque (sanctuaire)
    177: "m180b", # As de Pique (Tartare)
    224: "m116",  # Golem (sanctuaire)
    225: "m197",  # Estark (post-game)
    275: "m211",  # Belzébik (sanctuaire)
    276: "m087",  # Encorneur (combat final)
    277: "m088",  # Sangliogre (combat final)
    278: "m188",  # Gracos (quêtes annexes)
    279: "m084b", # Bélial (île de Célesprit)
    280: "m230",  # Shivattak (sanctuaire)
    317: "m158",  # Capitaine Crow (5e combat)
    318: "m206",  # Dr Rebelote (boss final)
}
by_species.update(BOSS_SPECIES)
raw_enemies = (D / "BtlEnmyPrm.bin").read_bytes()
enemies = list(esc.read_entries(raw_enemies))

sys.path.insert(0, str(ROOT / "tools"))
from extraire_mapping import decode, format_en, format_fr
import re
_msg0 = {l: [x.strip() for x in decode((D / f"message0.bin{l}").read_bytes()).split("|")] for l in "EFDIS"}

def species_names(species_id):
    """Nom d'espece : message0[64 + id] (5 langues), utile pour les especes propres aux combats (non recrutables)."""
    def clean(s):
        s = s.replace("<45>", "\u00c9").replace("<49>", "\u00cd")
        return re.sub(r"\s+", " ", re.sub(r"<[0-9a-f]{2}>", "", s)).strip()
    def fmt(l):
        raw = clean(_msg0[l][64 + species_id]) if 64 + species_id < len(_msg0[l]) else ""
        return format_en(raw) if l == "E" else format_fr(raw) if l == "F" else raw[:1].upper() + raw[1:]
    return {l: fmt(l) for l in "EFDIS"}

def abilities(v):
    """6 emplacements d'aptitudes de combat (u16 haut de chaque u32 des octets 8-31, 0 = vide, >= 221 = « DUMMY »)."""
    e = raw_enemies[8 + 88 * v: 8 + 88 * (v + 1)]
    return [x for x in struct.unpack_from("<12H", e, 8)[1::2] if x and x < 221]

def enemy(v):
    if v == 0: return None
    if v >= len(enemies): return {"btl_enmy_prm_index": v, "unresolved": True}
    e = enemies[v]
    return {"btl_enmy_prm_index": v, "species": by_species.get(e["species_id"]), "species_id": e["species_id"], "species_names": species_names(e["species_id"]), "level": e["level"],
            "gold": e["gold"], "exp": e["exp"], "abilities": abilities(v),
            "stats": {k: e[k] for k in ("max_hp", "max_mp", "attack", "defense", "agility", "wisdom")}}

def load(f):
    d = open(f, "rb").read(); o = 0x1004; seq = []
    while o + 8 <= len(d):
        t, l = struct.unpack_from("<II", d, o)
        if l < 8: break
        seq.append((o - 0x1004, t, d[o + 8:o + l])); o += l
    return seq

# Mode de combat ecrit par FUN_021c2530 (FUN_021b932c) : types 0 -> 0x00, 4 -> 0x10, 1 et 7 -> 0x20 (le type 7 appelle en plus 0x02054de0)
MODE = {0: 0x00, 1: 0x20, 4: 0x10, 7: 0x20}
# Role d'apres les commentaires japonais des scripts (fenetre de 150 instructions autour du combat)
ROLES = [("ラスボス", "final_boss"), ("ラスダン中ボス", "last_dungeon_midboss"), ("祠", "shrine"), ("神獣", "shrine"), ("闘技場", "colosseum")]
ROLE_ORDER = ["last_dungeon_midboss", "final_boss", "shrine", "colosseum"]

def role_of(seq, i):
    text = " ".join(seq[j][2].split(b"\0")[0].decode("cp932", "replace") for j in range(max(0, i - 150), min(len(seq), i + 150)) if seq[j][1] == 0xaa)
    found = [r for k, r in ROLES if k in text]
    return next((r for r in ROLE_ORDER if r in found), None)

maps = collections.defaultdict(list)
for f in sorted(glob.glob(str(D / "*.evt"))):
    seq = load(f)
    for i, (o, t, p) in enumerate(seq):
        if t != 0x44: continue
        a = {}
        for j in range(i - 1, max(0, i - 12), -1):
            _, tt, pp = seq[j]
            if tt != 0x15 or len(pp) != 16: break
            dk, di, sk, sv = struct.unpack("<IfIf", pp)
            if dk == 1 and int(di) not in a: a[int(di)] = (sk, sv)
        if 0 not in a or a[0][0] != 2 or int(a[0][1]) not in (0, 1, 4, 7): continue
        lit = lambda k: int(a[k][1]) if k in a and a[k][0] == 2 else None
        ids = [lit(1), lit(2), lit(3)]
        if None in ids: continue
        maps[os.path.basename(f)[:-4]].append({"offset": o, "type": int(a[0][1]), "enemies": [enemy(v) for v in ids],
                                               "args_4_5_raw": [lit(4), lit(5)],
                                               "battle_mode": MODE.get(int(a[0][1])), "role": role_of(seq, i)})
out = {"provenance": "ROM : instruction 0x44 des .evt, semantique de FUN_021c2530 (voir docstring de tools/extraire_combats_fixes.py)",
       "note": "Indices lus tels quels comme indices BtlEnmyPrm ; sens des arguments 4 et 5 non prouve.", "scripts": maps}
(OUT / "fixed_battles.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
n = sum(len(v) for v in maps.values())
print("ecrit", n, "combats dans", len(maps), "scripts")
for k, v in list(maps.items())[:4]:
    for b in v[:2]: print(k, b["type"], [(e and (e.get("species"), e.get("level"))) for e in b["enemies"]])
