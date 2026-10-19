#!/usr/bin/env python3
"""
d16topng.py - Convertit les images .d16 de Dragon Quest Monsters: Joker en PNG.

FORMAT .d16 (deduit par analyse, pas documente publiquement) :

    Offset  Taille  Contenu
    ------  ------  ------------------------------------------
    0x00    4       signature "D16\\0"  (44 31 36 00)
    0x04    2       largeur en pixels  (little-endian)
    0x06    2       hauteur en pixels  (little-endian)
    0x08    ...     pixels bruts

    Les pixels sont en BGR555 : 16 bits par pixel, 1 bit ignore,
    5 bits bleu, 5 bits vert, 5 bits rouge.

        16       11    10        5 4        0
    +--------+---------+----------+----------+
    | ignore |  BLEU   |   VERT   |  ROUGE   |
    +--------+---------+----------+----------+

    C'est le format natif de la Nintendo DS (et de la GBA). Chaque
    composante va de 0 a 31, il faut donc la dilater vers 0-255.

COMMENT ON A TROUVE CA :
    1. Le fichier fait 98312 octets pour une image annoncee 256x192.
       256 * 192 * 2 = 98304. La difference (8) est l'en-tete.
    2. Les 4 premiers octets sont "D16\\0" : le nom du format.
    3. Les 4 suivants, lus en little-endian : 0x0100 = 256, 0x00C0 = 192.
       Ce sont exactement les dimensions attendues. En-tete confirme.
    4. Le pixel 0 vaut 0xFBDE. En BGR555 -> R=30, G=30, B=30 : un gris
       clair. Coherent avec le coin d'une image de fond.

Usage:
    ./d16topng.py fichier.d16 [sortie.png]
    ./d16topng.py --all data/          # convertit tous les .d16 d'un dossier
"""

import struct
import sys
import os
import glob

try:
    from PIL import Image
except ImportError:
    print("Erreur : Pillow est requis.  sudo apt install python3-pil", file=sys.stderr)
    sys.exit(1)


def lire_d16(chemin):
    """Lit un .d16 et renvoie (largeur, hauteur, liste de pixels RGB)."""
    with open(chemin, "rb") as f:
        d = f.read()

    if len(d) < 8 or d[:4] != b"D16\x00":
        raise ValueError(f"{chemin}: signature D16 absente")

    largeur, hauteur = struct.unpack_from("<HH", d, 4)

    attendu = largeur * hauteur * 2
    if len(d) - 8 < attendu:
        raise ValueError(
            f"{chemin}: tronque (attendu {attendu + 8} octets, lu {len(d)})"
        )

    pixels = []
    for i in range(largeur * hauteur):
        px = struct.unpack_from("<H", d, 8 + i * 2)[0]

        # Extraction BGR555
        r5 = px & 0x1F
        g5 = (px >> 5) & 0x1F
        b5 = (px >> 10) & 0x1F

        # Dilatation 5 bits -> 8 bits. On repete les bits de poids fort
        # dans les bits de poids faible pour couvrir toute la plage :
        # 0 -> 0, 31 -> 255. Un simple *8 plafonnerait a 248.
        r = (r5 << 3) | (r5 >> 2)
        g = (g5 << 3) | (g5 >> 2)
        b = (b5 << 3) | (b5 >> 2)

        pixels.append((r, g, b))

    return largeur, hauteur, pixels


def convertir(entree, sortie=None):
    largeur, hauteur, pixels = lire_d16(entree)

    if sortie is None:
        sortie = os.path.splitext(entree)[0] + ".png"

    img = Image.new("RGB", (largeur, hauteur))
    img.putdata(pixels)
    img.save(sortie)

    print(f"  {os.path.basename(entree):28s} {largeur}x{hauteur} -> {sortie}")
    return sortie


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--all":
        dossier = sys.argv[2] if len(sys.argv) > 2 else "."
        sortie_dir = sys.argv[3] if len(sys.argv) > 3 else "png"
        os.makedirs(sortie_dir, exist_ok=True)

        fichiers = sorted(glob.glob(os.path.join(dossier, "*.d16")))
        if not fichiers:
            print(f"Aucun .d16 dans {dossier}")
            sys.exit(1)

        print(f"Conversion de {len(fichiers)} fichiers -> {sortie_dir}/")
        ok = 0
        for f in fichiers:
            nom = os.path.splitext(os.path.basename(f))[0] + ".png"
            try:
                convertir(f, os.path.join(sortie_dir, nom))
                ok += 1
            except Exception as e:
                print(f"  ECHEC {f}: {e}", file=sys.stderr)
        print(f"\n{ok}/{len(fichiers)} convertis.")
        return

    convertir(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)


if __name__ == "__main__":
    main()
