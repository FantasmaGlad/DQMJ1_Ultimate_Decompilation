#!/usr/bin/env python3
"""Extrait et rend les 60 cartes / arrière-plans 2D (.CHR + .SCR + .PAL) de la ROM en PNG haute fidélité.

Format Nintendo DS Background :
- .CHR (32 Ko) : 1 024 tuiles de 8×8 pixels en 4bpp (32 octets par tuile)
- .PAL (64 octets) : 32 couleurs BGR555 natif correspondant aux palettes hardware 14 et 15
- .SCR (8 Ko) : 4 096 entrées 16 bits (64×64 tuiles = 512×512 pixels)
  - Bits 0..9  : numéro de tuile (0x3FF = tuile vide)
  - Bit 10     : retournement horizontal
  - Bit 11     : retournement vertical
  - Bits 12..15: numéro de palette (14 ou 15)

Sorties :
- Fichiers PNG des 60 minimaps dans DragonQuestMonsterJoker1Bestiaire/assets/images/maps-2d/
- Écrans d'interface dans DragonQuestMonsterJoker1Bestiaire/assets/images/ui/
- Catalogue dans DragonQuestMonsterJoker1Bestiaire/assets/data/map_minimaps_2d.json
"""

import glob
import json
import os
import re
import struct
import sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "work/extracted/data")
BESTIAIRE_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "DragonQuestMonsterJoker1Bestiaire")
DEST_MAPS_DIR = os.path.join(BESTIAIRE_DIR, "assets/images/maps-2d")
DEST_SCREENS_DIR = os.path.join(BESTIAIRE_DIR, "assets/images/screens")
DEST_UI_DIR = os.path.join(BESTIAIRE_DIR, "assets/images/ui")
DEST_JSON = os.path.join(BESTIAIRE_DIR, "assets/data/map_minimaps_2d.json")
DEST_SCREENS_JSON = os.path.join(BESTIAIRE_DIR, "assets/data/game_screens.json")



def decode_pal(raw_pal):
    colors = []
    for i in range(0, min(len(raw_pal), 512), 2):
        val = struct.unpack("<H", raw_pal[i : i + 2])[0]
        r = (val & 0x1F) << 3
        g = ((val >> 5) & 0x1F) << 3
        b = ((val >> 10) & 0x1F) << 3
        r8 = r | (r >> 5)
        g8 = g | (g >> 5)
        b8 = b | (b >> 5)
        a = 0 if (i % 32 == 0) else 255
        colors.append((r8, g8, b8, a))
    return colors


def render_map_2d(chr_path, scr_path, pal_path):
    with open(chr_path, "rb") as f:
        chr_data = f.read()
    with open(scr_path, "rb") as f:
        scr_data = f.read()
    with open(pal_path, "rb") as f:
        pal_data = f.read()

    pal_colors = decode_pal(pal_data)
    while len(pal_colors) < 32:
        pal_colors.append((0, 0, 0, 0))

    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    pix = img.load()

    num_entries = len(scr_data) // 2
    cols = 64
    rows = min(64, num_entries // cols)

    for ty in range(rows):
        for tx in range(cols):
            idx = (ty * 64 + tx) * 2
            if idx + 2 > len(scr_data):
                continue
            entry = struct.unpack("<H", scr_data[idx : idx + 2])[0]
            tile_num = entry & 0x3FF
            if tile_num == 0x3FF:
                continue

            h_flip = (entry >> 10) & 1
            v_flip = (entry >> 11) & 1
            pal_num = (entry >> 12) & 0xF
            pal_base = 0 if pal_num == 14 else 16

            tile_offset = tile_num * 32
            if tile_offset + 32 > len(chr_data):
                continue
            tile_bytes = chr_data[tile_offset : tile_offset + 32]

            for y in range(8):
                py = 7 - y if v_flip else y
                row_bytes = tile_bytes[y * 4 : (y + 1) * 4]
                for x in range(8):
                    px = 7 - x if h_flip else x
                    byte = row_bytes[x // 2]
                    col_idx = (byte & 0xF) if (x % 2 == 0) else ((byte >> 4) & 0xF)
                    if col_idx != 0:
                        c = pal_colors[pal_base + col_idx]
                        pix[tx * 8 + px, ty * 8 + py] = c

    bbox = img.getbbox()
    if bbox:
        # Marge de 4px
        x0 = max(0, bbox[0] - 4)
        y0 = max(0, bbox[1] - 4)
        x1 = min(512, bbox[2] + 4)
        y1 = min(512, bbox[3] + 4)
        return img.crop((x0, y0, x1, y1)), bbox
    return img, None


def decode_wall(path):
    with open(path, "rb") as f:
        data = f.read()
    count = struct.unpack("<I", data[:4])[0]
    header_size = 4 + count * 8
    off0, sz0 = struct.unpack("<II", data[4:12])
    off1, sz1 = struct.unpack("<II", data[12:20])
    off2, sz2 = struct.unpack("<II", data[20:28])

    chr_data = data[header_size + off0 : header_size + off0 + sz0]
    pal_data = data[header_size + off1 : header_size + off1 + sz1]
    scr_data = data[header_size + off2 : header_size + off2 + sz2]

    pal_colors = []
    for i in range(len(pal_data) // 2):
        val = struct.unpack("<H", pal_data[i * 2 : (i + 1) * 2])[0]
        r = (val & 0x1F) << 3
        g = ((val >> 5) & 0x1F) << 3
        b = ((val >> 10) & 0x1F) << 3
        r8 = r | (r >> 5)
        g8 = g | (g >> 5)
        b8 = b | (b >> 5)
        a = 0 if i == 0 else 255
        pal_colors.append((r8, g8, b8, a))

    while len(pal_colors) < 16:
        pal_colors.append((0, 0, 0, 0))

    img = Image.new("RGBA", (256, 192), (0, 0, 0, 0))
    pix = img.load()

    for ty in range(24):
        for tx in range(32):
            idx = (ty * 32 + tx) * 2
            if idx + 2 > len(scr_data):
                continue
            entry = struct.unpack("<H", scr_data[idx : idx + 2])[0]
            tile_num = entry & 0x3FF
            h_flip = (entry >> 10) & 1
            v_flip = (entry >> 11) & 1
            tile_offset = tile_num * 32
            if tile_offset + 32 > len(chr_data):
                continue
            t_bytes = chr_data[tile_offset : tile_offset + 32]
            for y in range(8):
                py = 7 - y if v_flip else y
                row = t_bytes[y * 4 : (y + 1) * 4]
                for x in range(8):
                    px = 7 - x if h_flip else x
                    b = row[x // 2]
                    c_idx = (b & 0xF) if (x % 2 == 0) else ((b >> 4) & 0xF)
                    if c_idx != 0:
                        pix[tx * 8 + px, ty * 8 + py] = pal_colors[c_idx]

    return img


WALL_SCREENS_METADATA = {
    "wall_bank": {
        "title_fr": "Banque de prêt",
        "title_en": "Lending Bank Counter",
        "category": "services",
        "description_fr": "Comptoir de la banque de prêt de l'Arène des Dresseurs."
    },
    "wall_base": {
        "title_fr": "Base du QG",
        "title_en": "Scout Headquarters Base",
        "category": "story",
        "description_fr": "Salle principale de la base de l'Association des Dresseurs."
    },
    "wall_combi": {
        "title_fr": "Laboratoire de synthèse",
        "title_en": "Monster Synthesis Laboratory",
        "category": "synthesis",
        "description_fr": "Machine alchimique et pupitre de fusion des monstres."
    },
    "wall_gpinfo": {
        "title_fr": "Panneau du Tournoi",
        "title_en": "Tournament Information Board",
        "category": "arena",
        "description_fr": "Tableau d'affichage des scores et classements du championnat."
    },
    "wall_itemshop": {
        "title_fr": "Échoppe d'objets",
        "title_en": "Item Shop Counter",
        "category": "shops",
        "description_fr": "Comptoir de vente d'objets, armes et parchemins."
    },
    "wall_keep": {
        "title_fr": "Enclos des monstres",
        "title_en": "Monster Storage Pen",
        "category": "monsters",
        "description_fr": "Guichet de stockage et pensionnat des monstres."
    },
    "wall_skillpoint": {
        "title_fr": "Autel des compétences",
        "title_en": "Skill Point Altar",
        "category": "skills",
        "description_fr": "Autel sacré d'attribution des points de compétence."
    },
}


def main():
    os.makedirs(DEST_MAPS_DIR, exist_ok=True)
    os.makedirs(DEST_SCREENS_DIR, exist_ok=True)
    os.makedirs(DEST_UI_DIR, exist_ok=True)

    chr_files = sorted(glob.glob(os.path.join(DATA_DIR, "MAP_*.CHR")))
    print(f"Rendu de {len(chr_files)} cartes 2D vers {DEST_MAPS_DIR}...")

    manifest = []
    for chr_path in chr_files:
        base = os.path.basename(chr_path)[:-4]  # e.g. MAP_D001
        map_code = base.replace("MAP_", "").lower()  # e.g. d001
        scr_path = os.path.join(DATA_DIR, f"{base}.SCR")
        pal_path = os.path.join(DATA_DIR, f"{base}.PAL")

        if not os.path.exists(scr_path) or not os.path.exists(pal_path):
            continue

        rendered_img, bbox = render_map_2d(chr_path, scr_path, pal_path)
        out_name = f"{map_code}.png"
        out_path = os.path.join(DEST_MAPS_DIR, out_name)
        rendered_img.save(out_path)

        manifest.append({
            "map_id": map_code,
            "source": base,
            "file": out_name,
            "width": rendered_img.width,
            "height": rendered_img.height,
            "bbox": bbox,
            "url": f"/api/assets/images/maps-2d/{out_name}",
        })

    with open(DEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"60 cartes 2D rendues avec succès. Manifeste : {DEST_JSON}")

    # Rendu des écrans 2D (wall_*.bin)
    screens_manifest = []
    wall_files = sorted(glob.glob(os.path.join(DATA_DIR, "wall_*.bin")))
    print(f"Rendu de {len(wall_files)} écrans 2D vers {DEST_SCREENS_DIR}...")
    for wall_path in wall_files:
        wall_id = os.path.basename(wall_path)[:-4]
        out_name = f"{wall_id}.png"
        out_path = os.path.join(DEST_SCREENS_DIR, out_name)
        img = decode_wall(wall_path)
        img.save(out_path)

        meta = WALL_SCREENS_METADATA.get(wall_id, {
            "title_fr": wall_id,
            "title_en": wall_id,
            "category": "misc",
            "description_fr": ""
        })
        screens_manifest.append({
            "screen_id": wall_id,
            "file": out_name,
            "width": 256,
            "height": 192,
            "title_fr": meta["title_fr"],
            "title_en": meta["title_en"],
            "category": meta["category"],
            "description_fr": meta["description_fr"],
            "url": f"/api/assets/images/screens/{out_name}",
        })

    with open(DEST_SCREENS_JSON, "w", encoding="utf-8") as f:
        json.dump(screens_manifest, f, indent=2, ensure_ascii=False)

    print(f"{len(screens_manifest)} écrans 2D rendus avec succès. Manifeste : {DEST_SCREENS_JSON}")


if __name__ == "__main__":
    main()

