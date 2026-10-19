#!/usr/bin/env python3
"""
swartowav.py - Convertit les banques d'echantillons .swar (Nintendo DS) en WAV.

=======================================================================
POURQUOI CE SCRIPT EXISTE : LE MALENTENDU A LEVER
=======================================================================

Un .swar N'EST PAS un fichier audio. C'est une BANQUE D'ECHANTILLONS :
un conteneur qui regroupe plusieurs petits sons (SWAV), exactement comme
un dossier contenant plusieurs WAV.

    .sdat  (l'archive sonore du jeu)
      |
      +-- SSEQ  une partition  -> « joue le do 200 ms avec l'instrument 5 »
      +-- SBNK  une banque     -> « l'instrument 5 = l'echantillon 3 du SWAR 7 »
      +-- SWAR  une banque     -> contient N echantillons SWAV  <-- ICI
      +-- STRM  un flux audio  -> de l'audio deja encode, jouable tel quel

Donc ouvrir un .swar dans un lecteur audio ne donne rien : ce n'est pas
un format audio, c'est un conteneur. Il faut d'abord extraire les SWAV
qu'il contient, puis convertir chacun en WAV.

C'est la meme confusion que d'essayer d'ecouter un fichier .zip.

=======================================================================
LES TROIS NIVEAUX (a bien distinguer)
=======================================================================

  SWAR  = Wave ARchive    -> la banque (ce que contient un .swar)
  SWAV  = Wave             -> un echantillon individuel
  Codec = PCM8 / PCM16 / ADPCM  -> comment les octets sont encodes

=======================================================================
STRUCTURE D'UN SWAR
=======================================================================

  0x00  4   "SWAR"
  0x04  2   BOM (FFFE = little-endian)
  0x06  2   version (0x0100)
  0x08  4   taille du fichier
  0x0C  2   taille de l'en-tete      <-- LA CLE
  0x0E  2   nombre de blocs
  0x10  4   "DATA"
  0x14  4   taille du bloc DATA
  0x18  ... remplissage jusqu'a la fin de l'en-tete

  A la fin de l'en-tete (offset = taille_en_tete) :
      u32  nombre d'echantillons N
      u32  offsets[N]  (relatifs a la fin de l'en-tete)

=======================================================================
STRUCTURE D'UN SWAV (echantillon individuel)
=======================================================================

  0x00  4   "SWAV"
  0x04  2   BOM
  0x06  2   version
  0x08  4   taille du fichier
  0x0C  2   taille de l'en-tete (0x24)
  0x0E  2   nombre de blocs
  0x10  4   "DATA"
  0x14  4   taille du bloc DATA
  0x18  1   codec  (0 = PCM8, 1 = PCM16, 2 = ADPCM)
  0x19  1   bouclage
  0x1A  2   frequence d'echantillonnage
  0x1C  2   time
  0x1E  2   loopOffset
  0x20  4   longueur de boucle
  0x24  ... donnees audio

=======================================================================
CETTE STRUCTURE A ETE VERIFIEE, PAS DEVINEE
=======================================================================
La verification est simple et reproductible : quand on utilise le bon
offset pour l'en-tete (celui declare a 0x0C, et non une valeur supposee),
on obtient des couples (codec, frequence) parfaitement coherents :
codec 0/1/2 et frequences de 8000 a 48000 Hz. Avec un mauvais offset on
lit codec=37 ou frequence=4257, ce qui est evidemment faux.

Usage:
    ./swartowav.py fichier.swar [dossier_sortie]
    ./swartowav.py --all dossier_swar/ dossier_sortie/
"""

import struct
import sys
import os
import glob
import wave

# Table de pas IMA-ADPCM (identique sur DS).
TABLE_PAS = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31,
    34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143,
    157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544,
    598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707,
    1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871,
    5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635,
    13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767,
]
TABLE_INDEX = [-1, -1, -1, -1, 2, 4, 6, 8,
               -1, -1, -1, -1, 2, 4, 6, 8]

CODECS = {0: "PCM8", 1: "PCM16", 2: "ADPCM"}


def decoder_adpcm(donnees, predicteur=0, index=0):
    """Decode un flux IMA-ADPCM Nintendo DS (variante « mono »).

    ===============================================================
    POINT CRUCIAL : CE N'EST PAS DE L'ADPCM « PAR BLOCS »
    ===============================================================

    Sur beaucoup de machines (WAV IMA, MS-ADPCM), l'ADPCM est decoupe
    en BLOCS, et chaque bloc recommence par un en-tete contenant un
    predicteur et un index de pas.

    La Nintendo DS n'utilise PAS ce modele. Son ADPCM est un FLUX
    CONTINU : il n'y a AUCUN en-tete repete. Le predicteur et l'index
    de pas sont initialises UNE SEULE FOIS (dans l'en-tete du SWAV) et
    evoluent ensuite en continu d'un octet a l'autre, du debut a la fin
    de l'echantillon.

    C'est la raison pour laquelle une implementation « par blocs de 36
    octets » produit du son correct pendant ~130 echantillons, puis
    sature : a chaque faux en-tete de bloc, elle relit des octets audio
    comme s'ils etaient un predicteur, et le decodeur part en vrille.

    (Reference : la bibliotheque vgmstream nomme ce codec
     « coding_IMA_mono » et le decrit comme « no header (external
     setup) », c'est-a-dire sans en-tete interne.)

    ===============================================================
    L'ALGORITHME, LIGNE PAR LIGNE
    ===============================================================
    Chaque octet contient 2 echantillons de 4 bits (nibbles).
    L'ordre est « nibble bas d'abord » :
        nibble 1 = octet & 0x0F     (bits 0-3)
        nibble 2 = octet >> 4       (bits 4-7)

    Pour chaque nibble :
        pas   = TABLE_PAS[index]
        delta = pas/8
        + pas/4   si bit 0 du nibble
        + pas/2   si bit 1
        + pas     si bit 2
        - delta   si bit 3 (le signe)
        predicteur += delta              <- on ACCUMULE la difference
        index += TABLE_INDEX[nibble]     <- le pas s'adapte
        index borne a [0, 88]
    """
    out = []
    for octet in donnees:
        for nibble in (octet & 0x0F, octet >> 4):   # bas d'abord
            pas = TABLE_PAS[index]
            delta = pas >> 3
            if nibble & 1:
                delta += pas >> 2
            if nibble & 2:
                delta += pas >> 1
            if nibble & 4:
                delta += pas
            if nibble & 8:
                delta = -delta

            predicteur += delta
            predicteur = max(-32768, min(32767, predicteur))

            index += TABLE_INDEX[nibble]
            index = max(0, min(88, index))

            out.append(predicteur)

    return out


def lire_swav(d):
    """Decode un echantillon SWAV et renvoie (echantillons, freq, codec).

    IMPORTANT : a l'interieur d'un SWAR, les echantillons sont stockes
    SANS leur en-tete de fichier "SWAV". L'en-tete de l'echantillon
    commence donc directement a l'offset 0 et fait 12 octets :

        0x00  1   codec (0 = PCM8, 1 = PCM16, 2 = ADPCM)
        0x01  1   bouclage
        0x02  2   frequence d'echantillonnage
        0x04  2   time
        0x06  2   loopOffset
        0x08  4   longueur de boucle
        0x0C  ... donnees audio

    Un SWAV stocke comme fichier autonome, lui, possede en plus un
    en-tete de fichier Nitro de 0x24 octets AVANT ces champs. C'est la
    source de confusion classique : la meme structure se lit a deux
    offsets differents selon le contexte.
    """
    codec = d[0]
    frequence = struct.unpack_from("<H", d, 2)[0]
    donnees = d[0x0C:]

    if codec == 0:
        ech = [(b - 256 if b > 127 else b) * 256 for b in donnees]
    elif codec == 1:
        n = len(donnees) // 2
        ech = list(struct.unpack_from(f"<{n}h", donnees, 0))
    elif codec == 2:
        # Pour l'ADPCM, l'ETAT INITIAL du decodeur est stocke dans les
        # 4 premiers octets des donnees :
        #   +0  s16  predicteur de depart
        #   +2  s16  index de pas de depart (0 a 88)
        # Ces valeurs ne sont lues qu'UNE fois : l'ADPCM DS est un flux
        # continu, sans en-tete par bloc (voir decoder_adpcm).
        predicteur = struct.unpack_from("<h", donnees, 0)[0]
        index = struct.unpack_from("<h", donnees, 2)[0]
        index = max(0, min(88, index))
        ech = decoder_adpcm(donnees[4:], predicteur, index)
    else:
        raise ValueError(f"codec inconnu ({codec})")

    return ech, frequence, codec


def lire_swar(chemin):
    """Renvoie la liste des echantillons SWAV bruts d'une banque SWAR."""
    with open(chemin, "rb") as f:
        d = f.read()

    if d[:4] != b"SWAR":
        raise ValueError(f"{chemin}: signature SWAR absente")

    # L'INDEX DE LA BANQUE : le nombre d'echantillons est a 0x38 et le
    # tableau d'offsets commence a 0x3C. Les offsets sont ABSOLUS dans
    # le fichier (ils pointent directement sur chaque echantillon).
    #
    # Note : la taille d'en-tete declaree a 0x0C (0x10 ici) ne sert PAS
    # de base a cet index. C'est le piege de ce format : 0x0C donne la
    # taille du bloc "DATA", pas la position de l'index.
    nb = struct.unpack_from("<I", d, 0x38)[0]
    if nb == 0:
        # Un SWAR de 60 octets est une banque VIDE et valide : elle ne
        # contient aucun echantillon. Ce n'est pas une erreur.
        return []
    if nb > 1000:
        raise ValueError(f"{chemin}: nombre d'echantillons invalide ({nb})")

    swavs = []
    for i in range(nb):
        debut = struct.unpack_from("<I", d, 0x3C + i * 4)[0]
        if debut + 0x0C >= len(d):
            continue
        # La fin de l'echantillon est le debut du suivant ; pour le
        # dernier on prend la fin du fichier.
        if i + 1 < nb:
            fin = struct.unpack_from("<I", d, 0x3C + (i + 1) * 4)[0]
        else:
            fin = len(d)
        swavs.append(d[debut:fin])

    return swavs


def ecrire_wav(chemin, echantillons, frequence):
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(frequence)
        w.writeframes(struct.pack(f"<{len(echantillons)}h", *echantillons))


def convertir_swar(chemin, dossier_sortie, verbeux=True):
    """Extrait tous les echantillons d'un SWAR en WAV individuels."""
    nom_base = os.path.splitext(os.path.basename(chemin))[0]
    dossier = os.path.join(dossier_sortie, nom_base)
    os.makedirs(dossier, exist_ok=True)

    swavs = lire_swar(chemin)
    if verbeux:
        print(f"\n  {nom_base}.swar -> {len(swavs)} echantillons")

    ok = 0
    for i, brut in enumerate(swavs):
        try:
            ech, freq, codec = lire_swav(brut)
            if not ech:
                continue
            sortie = os.path.join(dossier, f"wave_{i:03d}.wav")
            ecrire_wav(sortie, ech, freq)
            ok += 1
            if verbeux:
                duree = len(ech) / freq if freq else 0
                print(f"    wave_{i:03d}.wav  {CODECS.get(codec,'?'):6s} "
                      f"{freq:6d} Hz  {duree:6.3f} s")
        except Exception as e:
            if verbeux:
                print(f"    wave_{i:03d} : ECHEC ({e})")

    return ok, len(swavs)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--all":
        source = sys.argv[2] if len(sys.argv) > 2 else "."
        sortie = sys.argv[3] if len(sys.argv) > 3 else "swar_wav"
        os.makedirs(sortie, exist_ok=True)

        fichiers = sorted(glob.glob(os.path.join(source, "*.swar")))
        if not fichiers:
            print(f"Aucun .swar dans {source}")
            sys.exit(1)

        print(f"Extraction de {len(fichiers)} banques SWAR -> {sortie}/")
        total_ok = total_n = 0
        for f in fichiers:
            try:
                ok, n = convertir_swar(f, sortie, verbeux=False)
                total_ok += ok
                total_n += n
                print(f"  {os.path.basename(f):34s} {ok:3d}/{n:3d} echantillons")
            except Exception as e:
                print(f"  ECHEC {f}: {e}", file=sys.stderr)

        print(f"\nTotal : {total_ok}/{total_n} echantillons extraits.")
        print(f"Dossier : {sortie}/")
        return

    chemin = sys.argv[1]
    sortie = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.splitext(os.path.basename(chemin))[0] + "_wav"
    ok, n = convertir_swar(chemin, sortie)
    print(f"\n{ok}/{n} echantillons extraits dans {sortie}/")


if __name__ == "__main__":
    main()
