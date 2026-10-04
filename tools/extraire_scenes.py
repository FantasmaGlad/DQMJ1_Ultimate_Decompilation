#!/usr/bin/env python3
"""Decode les fichiers .scn des cartes (eclairage et brouillard de scene) -> assets/data/map_scenes.json.

Format (164 fichiers, tous de 136 octets : « SCN\\0 » + 33 mots de 32 bits), prouve par les plages de valeurs :
  mots 0..15  4 lumieres de 4 mots : direction x, y, z (s32 virgule fixe 20.12, vecteur unitaire : longueur 1,00 +/- 0,02 sur les
              656 lumieres), puis un mot dont les octets 0..2 sont R, V, B sur 5 bits (0 a 31) et l'octet 3 = 1
              (commande LIGHT_COLOR du GPU DS)
  mot 16      couleur du brouillard : octets 0..2 R, V, B (5 bits), octet 3 = opacite (31)
  mot 17      decalage du brouillard (250 dans 124 fichiers sur 164)
  mot 18      exposant du brouillard (4, 5 ou 6)
  mot 19      256 (constant)
  mots 20..27 table de brouillard : 32 octets croissants de 0 a 127 (FOG_TABLE du GPU DS)
  mots 28..32 non decodes (conserves bruts)
Suffixe du fichier : h (90 cartes), v (33), y (41) = variantes de moment de la journee ; d'apres les couleurs (h neutre, v orange,
y bleu) h = jour, v = soir, y = nuit : INFERE, non prouve.
"""
import glob, json, math, os, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "map_scenes.json"


def s32(v):
    return v - (1 << 32) if v >= 1 << 31 else v


maps, worst, bad_colors, n_lights = {}, 0.0, 0, 0
for f in sorted(glob.glob(str(ROOT / "work/maps/*/*.scn"))):
    name = os.path.basename(f)[:-4]
    mapid, variant = name[:-1], name[-1]
    b = open(f, "rb").read()
    assert b[:4] == b"SCN\0" and len(b) == 136
    w = struct.unpack_from("<33I", b, 4)
    lights = []
    for k in range(4):
        d = [round(s32(v) / 4096, 4) for v in w[4 * k:4 * k + 3]]
        c = [w[4 * k + 3] & 0xFF, (w[4 * k + 3] >> 8) & 0xFF, (w[4 * k + 3] >> 16) & 0xFF]
        worst = max(worst, abs(math.sqrt(sum(x * x for x in d)) - 1.0))
        bad_colors += any(x > 31 for x in c) or (w[4 * k + 3] >> 24) != 1
        n_lights += 1
        lights.append({"direction": d, "color": c})
    fog_color = [w[16] & 0xFF, (w[16] >> 8) & 0xFF, (w[16] >> 16) & 0xFF]
    table = list(struct.pack("<8I", *w[20:28]))
    maps.setdefault(mapid, {})[variant] = {
        "lights": lights,
        "fog": {"color": fog_color, "opacity": w[16] >> 24, "offset": w[17], "shift": w[18], "table": table},
        "raw_words_19_28_32": [w[19], w[28], w[29], w[30], w[31], w[32]],
    }
OUT.write_text(json.dumps({"provenance": "ROM : fichiers .scn des cartes, voir docstring de tools/extraire_scenes.py",
                           "note": "Variantes h/v/y = moment de la journee, INFERE d'apres les couleurs.", "maps": maps}, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
print("cartes", len(maps), "fichiers", sum(len(v) for v in maps.values()), "| lumieres", n_lights, "ecart max a la norme 1 :", round(worst, 4), "| couleurs hors 0..31 :", bad_colors)
