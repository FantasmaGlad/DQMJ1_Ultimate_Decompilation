#!/usr/bin/env python3
"""Extrait l'ensemble des 40 illustrations plein écran .d16 de la ROM en PNG haute fidélité.

Format .d16 :
- En-tête de 8 octets : 'D16\\0', largeur u16 (256), hauteur u16 (192)
- Pixels bruts BGR555 (16 bits) dilatés sur 8 bits par canal

Sorties :
- Fichiers PNG dans DragonQuestMonsterJoker1Bestiaire/assets/images/artworks/
- Catalogue structuré dans DragonQuestMonsterJoker1Bestiaire/assets/data/game_artworks.json
"""

import json
import os
import struct
import sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "work/extracted/data")
BESTIAIRE_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "DragonQuestMonsterJoker1Bestiaire")
DEST_IMG_DIR = os.path.join(BESTIAIRE_DIR, "assets/images/artworks")
DEST_JSON = os.path.join(BESTIAIRE_DIR, "assets/data/game_artworks.json")

# Audit 2026-10-02 (suite 100, dépôt Bestiaire) : cette table portait 26 titres évocateurs
# inventés de toutes pièces ("Tartarus Depths", "Celestia Ascension", "Warden Trump's Office"...),
# jamais lus dans la ROM (aucune banque mes_* ne les contient). Vérification visuelle directe de 6
# fichiers (dm_pic_00 à dm_pic_05, cf. Read du PNG) : aucun titre ne correspondait au contenu réel
# de l'image (ex. "Incarus Awakening" était en fait un carton de titre japonais "BATTLE GP - 1er
# tour"). Retirée entièrement : chaque illustration retombe sur son identifiant brut, même repli
# que pour les musiques, où aucun titre officiel n'existe non plus dans la ROM (découvert et
# documenté le 2026-09-27). Ne jamais réintroduire de titre ici sans vérification visuelle directe
# (Read du PNG) ou confirmation par une banque de texte mes_* identifiée.
TITLES: dict[str, dict[str, str]] = {}

CATEGORIES = {
    "dm_pic": "cinematic",
    "fin": "ending",
    "pirate": "character",
    "info_wall": "notice_board",
}


def decode_d16(raw_bytes):
    if len(raw_bytes) < 8 or raw_bytes[:4] != b"D16\x00":
        raise ValueError("Signature D16 invalide")
    width, height = struct.unpack_from("<HH", raw_bytes, 4)
    expected = width * height * 2 + 8
    if len(raw_bytes) < expected:
        raise ValueError(f"Fichier tronque ({len(raw_bytes)} < {expected})")

    img = Image.new("RGB", (width, height))
    pix = img.load()
    offset = 8
    for y in range(height):
        for x in range(width):
            val = struct.unpack_from("<H", raw_bytes, offset)[0]
            offset += 2
            r5 = val & 0x1F
            g5 = (val >> 5) & 0x1F
            b5 = (val >> 10) & 0x1F
            r = (r5 << 3) | (r5 >> 2)
            g = (g5 << 3) | (g5 >> 2)
            b = (b5 << 3) | (b5 >> 2)
            pix[x, y] = (r, g, b)
    return img


def main():
    os.makedirs(DEST_IMG_DIR, exist_ok=True)
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".d16")])
    artworks = []

    print(f"Extraction de {len(files)} fichiers .d16 vers {DEST_IMG_DIR}...")

    for fname in files:
        fpath = os.path.join(DATA_DIR, fname)
        base_id = fname[:-4]
        with open(fpath, "rb") as f:
            raw = f.read()

        img = decode_d16(raw)
        out_png = f"{base_id}.png"
        out_path = os.path.join(DEST_IMG_DIR, out_png)
        img.save(out_path)

        lang = "all"
        root_id = base_id
        for lcode, suffix in [("de", "_D"), ("fr", "_F"), ("it", "_I"), ("es", "_S")]:
            if base_id.endswith(suffix):
                lang = lcode
                root_id = base_id[:-2]
                break
        if lang == "all" and (base_id + "_F.d16") in files:
            lang = "en"

        cat = "cinematic"
        for prefix, c in CATEGORIES.items():
            if root_id.startswith(prefix):
                cat = c
                break

        title = TITLES.get(root_id, {"en": root_id, "fr": root_id, "de": root_id, "it": root_id, "es": root_id})

        artworks.append({
            "id": base_id,
            "root_id": root_id,
            "file": out_png,
            "category": cat,
            "lang": lang,
            "width": img.width,
            "height": img.height,
            "title": title,
            "url": f"/api/assets/images/artworks/{out_png}",
        })

    with open(DEST_JSON, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"Extraction reussie : {len(artworks)} illustrations enregistrees dans {DEST_JSON}.")


if __name__ == "__main__":
    main()
