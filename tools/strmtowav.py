#!/usr/bin/env python3
"""
strmtowav.py - Convertit les flux audio .strm (Nintendo DS) en WAV.

=======================================================================
CE QU'EST UN STRM
=======================================================================

Un STRM ("stream") est de l'audio DEJA ENCODE, pret a etre joue. C'est
l'equivalent d'un MP3/WAV dans le monde DS. Les jeux DS l'utilisent pour
les voix, les cinematiques et parfois les musiques.

Trois codecs possibles, indiques par l'octet a l'offset 0x18 :
    0 = PCM8    (8 bits non compresse, signe)
    1 = PCM16   (16 bits non compresse, signe)
    2 = ADPCM   (compresse, 4 bits par echantillon)

L'ADPCM de la DS est un IMA-ADPCM avec un pas d'echantillonnage de 8.
Chaque bloc de donnees commence par 4 octets d'en-tete contenant le
predicteur initial et l'index de table, puis 32 octets de nibbles.

=======================================================================
STRUCTURE DU FICHIER
=======================================================================

    0x00  4   "STRM"
    0x04  2   BOM (FFFE = little-endian)
    0x06  2   version
    0x08  4   taille du fichier
    0x0C  2   taille de l'en-tete
    0x0E  2   nombre de blocs
    0x10  4   "HEAD"  (signature du bloc d'en-tete)
    0x14  4   taille du bloc HEAD
    0x18  1   codec
    0x19  1   bouclage (0 = non, 1 = oui)
    0x1A  2   ?
    0x1C  2   frequence d'echantillonnage
    0x1E  2   time
    0x20  4   loopStart (en echantillons)
    0x24  4   numSamples (nombre total d'echantillons)
    0x28  4   numBlocks
    0x2C  4   blockSize (octets par bloc)
    0x30  4   samplesPerBlock
    0x34  4   lastBlockSize
    0x38  4   lastBlockSamples
    ...
    0x50  4   "DATA"
    0x54  4   taille du bloc DATA
    ...       donnees audio

Usage:
    ./strmtowav.py fichier.strm [sortie.wav]
    ./strmtowav.py --all dossier/    # convertit tous les .strm
"""

import struct
import sys
import os
import glob
import wave

# Table de pas de l'IMA-ADPCM (standard, identique sur DS).
TABLE_PAS = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31,
    34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143,
    157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544,
    598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707,
    1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871,
    5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635,
    13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767,
]

# Table d'ajustement d'index.
TABLE_INDEX = [-1, -1, -1, -1, 2, 4, 6, 8,
               -1, -1, -1, -1, 2, 4, 6, 8]


def decoder_adpcm(donnees):
    """Decode un flux IMA-ADPCM de Nintendo DS en echantillons 16 bits.

    Le format de bloc DS : 4 octets d'en-tete, puis 32 octets de donnees.
    L'en-tete contient :
        +0  (16 bits) : valeur du predicteur initial
        +2  ( 8 bits) : index dans la table de pas
        +3  ( 8 bits) : ignore
    """
    echantillons = []
    pos = 0
    n = len(donnees)

    while pos + 4 <= n:
        # En-tete du bloc
        predicteur = struct.unpack_from("<h", donnees, pos)[0]
        index = donnees[pos + 2]
        if index > 88:
            index = 88
        pos += 4

        echantillons.append(predicteur)

        # 32 octets = 64 nibbles = 64 echantillons
        fin = min(pos + 32, n)
        while pos < fin:
            octet = donnees[pos]
            pos += 1

            for nibble in (octet & 0x0F, octet >> 4):
                pas = TABLE_PAS[index]

                # Calcul de la difference
                diff = pas >> 3
                if nibble & 1:
                    diff += pas >> 2
                if nibble & 2:
                    diff += pas >> 1
                if nibble & 4:
                    diff += pas
                if nibble & 8:
                    diff = -diff

                predicteur += diff

                # Clamp sur 16 bits signes
                if predicteur > 32767:
                    predicteur = 32767
                elif predicteur < -32768:
                    predicteur = -32768

                index += TABLE_INDEX[nibble]
                if index < 0:
                    index = 0
                elif index > 88:
                    index = 88

                echantillons.append(predicteur)

    return echantillons


def lire_strm(chemin):
    """Lit un .strm et renvoie (echantillons, frequence, codec, bouclage)."""
    with open(chemin, "rb") as f:
        d = f.read()

    if d[:4] != b"STRM":
        raise ValueError(f"{chemin}: signature STRM absente")

    codec = d[0x18]
    bouclage = d[0x19]
    frequence = struct.unpack_from("<H", d, 0x1C)[0]
    num_samples = struct.unpack_from("<I", d, 0x24)[0]

    # Le bloc DATA commence par "DATA" + taille.
    i = d.find(b"DATA")
    if i < 0:
        raise ValueError(f"{chemin}: bloc DATA introuvable")
    taille_data = struct.unpack_from("<I", d, i + 4)[0]
    donnees = d[i + 8:i + 8 + taille_data]

    if codec == 0:
        # PCM8 : octets signes
        echantillons = [(b - 256 if b > 127 else b) * 256 for b in donnees]
    elif codec == 1:
        # PCM16 : mots signes little-endian
        n = len(donnees) // 2
        echantillons = list(struct.unpack_from(f"<{n}h", donnees, 0))
    elif codec == 2:
        echantillons = decoder_adpcm(donnees)
    else:
        raise ValueError(f"{chemin}: codec inconnu ({codec})")

    # On tronque a la longueur annoncee (le dernier bloc est often complete).
    if num_samples and len(echantillons) > num_samples:
        echantillons = echantillons[:num_samples]

    return echantillons, frequence, codec, bouclage


def convertir(entree, sortie=None):
    echantillons, frequence, codec, bouclage = lire_strm(entree)

    if sortie is None:
        sortie = os.path.splitext(entree)[0] + ".wav"

    with wave.open(sortie, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(frequence)
        w.writeframes(struct.pack(f"<{len(echantillons)}h", *echantillons))

    duree = len(echantillons) / frequence if frequence else 0
    noms_codec = {0: "PCM8", 1: "PCM16", 2: "ADPCM"}
    print(f"  {os.path.basename(entree):40s} "
          f"{noms_codec.get(codec, '?'):6s} {frequence:6d} Hz "
          f"{duree:6.2f} s -> {os.path.basename(sortie)}")
    return sortie


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--all":
        dossier = sys.argv[2] if len(sys.argv) > 2 else "."
        sortie_dir = sys.argv[3] if len(sys.argv) > 3 else "wav"
        os.makedirs(sortie_dir, exist_ok=True)

        fichiers = sorted(glob.glob(os.path.join(dossier, "*.strm")))
        if not fichiers:
            print(f"Aucun .strm dans {dossier}")
            sys.exit(1)

        print(f"Conversion de {len(fichiers)} flux -> {sortie_dir}/")
        ok = 0
        for f in fichiers:
            nom = os.path.splitext(os.path.basename(f))[0] + ".wav"
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
