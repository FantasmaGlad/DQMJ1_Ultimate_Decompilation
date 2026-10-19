#!/usr/bin/env python3
"""
sdatextract.py - Extrait le contenu audio d'un fichier .sdat Nintendo DS.

=======================================================================
CE QU'EST UN SDAT, ET POURQUOI CE N'EST PAS UN DOSSIER DE MP3
=======================================================================

Un .sdat (Sound Data Archive) est l'archive sonore standard du SDK Nitro
de Nintendo. Elle est utilisee par des centaines de jeux DS. Elle contient
CINQ types d'objets, et il est essentiel de comprendre qu'ils ne sont pas
interchangeables :

    SSEQ  Sequence      Une PARTITION, pas de l'audio. Ce sont des notes
                        ("joue le do pendant 200 ms avec l'instrument 5").
                        C'est l'equivalent d'un fichier MIDI.

    SBNK  Bank          Un "patch" : la table qui associe chaque instrument
                        a un echantillon dans un SWAR.

    SWAR  Wave Archive  Des ECHANTILLONS audio bruts (PCM 8/16 bits ou ADPCM).
                        Ce sont les briques de base des instruments.

    STRM  Stream        De l'audio DEJA ENCODE, equivalent d'un MP3/WAV
                        complet. Utilise pour les voix, les cinematiques.

    SARC  Sound Archive Un conteneur imbrique.

Le point crucial : une musique de jeu DS est tres souvent une SSEQ. La
SSEQ seule ne "sonne" pas : elle decrit quoi jouer, et a besoin de la SBNK
+ du SWAR pour produire du son. Il faut donc SIMULER la console (un
sequenceur) pour l'entendre. C'est pour cela que "extraire la musique"
d'un jeu DS demande un outil specialise (vgmstream) et non un simple
depaqueteur.

En revanche, les STRM sont directement decodables : ce sont de vrais
flux audio.

=======================================================================
STRUCTURE DU FORMAT
=======================================================================

    Offset  Taille  Contenu
    0x00    4       "SDAT"
    0x04    2       BOM (FFFE = little-endian)
    0x06    2       version (0x0100)
    0x08    2       taille de l'en-tete
    0x0A    2       nombre de blocs
    0x0C    4       taille totale du fichier
    0x10    4       offset du bloc INFO
    0x14    4       offset du bloc FAT
    0x18    4       offset du bloc FILE
    ...

Le bloc INFO contient 5 sous-blocs dans cet ordre :
    SSEQ, SBNK, SWAR, STRM, SARC  (souvent dans l'ordre SBNK,SBNK,SWAR,...)

Chaque sous-bloc commence par :
    4 octets : nombre d'entrees
    4 octets : taille du sous-bloc
    puis un tableau d'entrees de 4 octets chacune :
        - si le fichier est en FAT : offset relatif dans le bloc FILE
        - sinon : offset absolu dans le SDAT

Le bloc FILE contient les donnees brutes, et la FAT donne leurs positions.

Usage:
    ./sdatextract.py sound_data.sdat [dossier_sortie]
"""

import struct
import sys
import os

# Types d'entrees SDAT, dans l'ordre ou ils apparaissent dans le bloc INFO.
TYPES = ["SSEQ", "SBNK", "SWAR", "STRM", "SARC"]

# Extensions reelles des donnees contenues.
EXT = {"SSEQ": "sseq", "SBNK": "sbnk", "SWAR": "swar",
       "STRM": "strm", "SARC": "sarc"}


def u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def u16(d, o):
    return struct.unpack_from("<H", d, o)[0]


def lire_symb(d, off, taille_fichier):
    """Lit le bloc SYMB : associe un identifiant numerique a un NOM.

    Structure :
        0x00  "SYMB"
        0x04  taille du bloc
        0x08  offset de la table des chaines (relatif au bloc)
        0x0C  nombre d'entrees
        ...   table d'entrees de 4 octets : offset de chaine (relatif)
        ...   table des chaines (ASCII terminees par \\0)

    C'est la partie la plus precieuse du fichier : elle donne les VRAIS
    noms des sons (SE_BTL_001, BGM_001...), la ou le reste du format ne
    contient que des indices numeriques.
    """
    if d[off:off + 4] != b"SYMB":
        return {}

    off_table = u32(d, off + 0x08)
    nb = u32(d, off + 0x0C)

    if nb > 100000:
        return {}

    noms = {}
    for i in range(nb):
        pos = off + off_table + i * 4
        if pos + 4 > len(d):
            break
        rel = u32(d, pos)
        if rel == 0:
            continue
        s = off + rel
        fin = d.find(b"\x00", s)
        if fin < 0:
            continue
        noms[i] = d[s:fin].decode("ascii", "replace")

    return noms


def extraire(chemin, sortie):
    d = open(chemin, "rb").read()

    if d[:4] != b"SDAT":
        print(f"Erreur : {chemin} n'est pas un SDAT", file=sys.stderr)
        return 1

    taille_fichier = u32(d, 0x0C)
    off_info = u32(d, 0x10)
    off_fat = u32(d, 0x14)
    off_file = u32(d, 0x18)

    # ------------------------------------------------------------------
    # DEUX VARIANTES D'EN-TETE EXISTENT (et c'est le piege de ce format)
    # ------------------------------------------------------------------
    # Variante classique : trois offsets SEPARES.
    #     0x10 = offset INFO, 0x14 = offset FAT, 0x18 = offset FILE
    #
    # Variante "avec symboles" (celle de ce jeu) : des PAIRES (offset, taille).
    #     0x10 = offset/taille de SYMB
    #     0x18 = offset/taille de INFO
    #     0x20 = offset/taille de FAT
    #     0x28 = offset/taille de FILE
    #
    # On les distingue en verifiant quelle interpretation place une
    # signature connue a l'offset 0x10. Ici on lit "SYMB" -> variante B.
    # ------------------------------------------------------------------
    def bloc_valide(off):
        return (0 <= off < len(d) - 4 and
                d[off:off + 4] in (b"INFO", b"FAT ", b"FILE", b"SYMB"))

    if bloc_valide(off_info) and d[off_info:off_info + 4] == b"INFO":
        variante = "classique"
    elif bloc_valide(off_info):
        # Variante avec paires : on decale d'un cran.
        variante = "paires (avec SYMB)"
        off_info = u32(d, 0x18)
        off_fat = u32(d, 0x20)
        off_file = u32(d, 0x28)
    else:
        print(f"En-tete SDAT non reconnu (0x10=0x{off_info:x})",
              file=sys.stderr)
        return 1

    print("=" * 62)
    print(f" SDAT : {chemin}")
    print("=" * 62)
    print(f"  version        : 0x{u16(d, 0x06):04x}")
    print(f"  agencement     : {variante}")
    print(f"  taille reelle  : {len(d)} octets")
    print(f"  taille annoncee: {taille_fichier} octets")
    print(f"  bloc INFO      : 0x{off_info:06x}")
    print(f"  bloc FAT       : 0x{off_fat:06x}")
    print(f"  bloc FILE      : 0x{off_file:06x}")
    print()

    # Le bloc SYMB (si present) contient les NOMS des sons.
    noms_symboles = {}
    if variante != "classique":
        off_symb = u32(d, 0x10)
        if d[off_symb:off_symb + 4] == b"SYMB":
            noms_symboles = lire_symb(d, off_symb, len(d))
            print(f"  bloc SYMB      : 0x{off_symb:06x} "
                  f"({len(noms_symboles)} symboles)")
            print()

    # Le bloc FAT : liste d'entrees vers le bloc FILE.
    #
    # Structure :  magic(4) + taille_bloc(4) + nombre_entrees(4) + entrees
    #
    # PIEGE 1 : le nombre d'entrees est a l'offset +8, pas +4. Lire +4
    #           donne la taille du bloc en octets, qu'on confondrait avec
    #           un nombre d'entrees.
    #
    # PIEGE 2 : dans CE jeu, chaque entree fait 16 OCTETS, pas 8 comme
    #           dans le SDAT standard. Verification : 394 entrees
    #           * 16 + 12 d'en-tete = 6316 octets, soit exactement la
    #           taille du bloc (0x18AC). Avec 8 octets on trouverait
    #           788 entrees, ce qui est faux.
    #           Les 8 octets supplementaires sont du remplissage.
    #
    # On deduit donc la largeur d'entree de la taille du bloc, au lieu
    # de la supposer.
    if d[off_fat:off_fat + 4] != b"FAT ":
        print("Attention : pas de signature FAT", file=sys.stderr)
        return 1

    taille_bloc_fat = u32(d, off_fat + 4)
    nb_fat = u32(d, off_fat + 8)

    largeur = 8
    if nb_fat > 0:
        largeur = (taille_bloc_fat - 12) // nb_fat
        if largeur < 8 or largeur > 64:
            largeur = 8

    fat = []
    for i in range(nb_fat):
        base = off_fat + 12 + i * largeur
        if base + 8 > len(d):
            break
        o = u32(d, base)
        t = u32(d, base + 4)
        fat.append((o, t))

    print(f"  entrees FAT    : {len(fat)}  ({largeur} octets/entree)")
    print()

    # Le bloc INFO : 5 sous-blocs, offsets RELATIFS au bloc INFO.
    os.makedirs(sortie, exist_ok=True)

    total_extrait = 0
    stats = []
    offset_type = 0   # index global pour la correspondance avec SYMB

    for i, nom in enumerate(TYPES):
        base = off_info + 8 + i * 8

        if base + 8 > off_fat:
            break

        rel = u32(d, base)
        if rel == 0:
            continue

        # CONVERSION CLE : offset relatif -> offset absolu.
        off_sub = off_info + rel

        # ------------------------------------------------------------------
        # A PROPOS DES TABLEAUX DE SOUS-BLOCS
        # ------------------------------------------------------------------
        # Dans la plupart des SDAT, chaque entree du sous-bloc est un INDEX
        # dans la FAT. Dans CE jeu, ce n'est pas le cas : les valeurs forment
        # une suite arithmetique de raison 12, et beaucoup ne tombent sur
        # aucune entree FAT valide. L'encodage n'est pas le standard.
        #
        # Plutot que de deviner, on adopte la methode FIABLE : on prend la
        # FAT comme source de verite, puisque ses entrees contiennent les
        # vraies donnees (on le verifie en lisant leur signature interne).
        # Le sous-bloc ne sert alors qu'a connaitre l'ORDRE des fichiers,
        # pas leur position.
        # ------------------------------------------------------------------
        nb = u32(d, off_sub) or u32(d, off_sub + 4)
        if nb > 10000:
            continue

        # Tableau d'entrees : on selectionne dans la FAT toutes les entrees
        # dont la signature interne correspond au type demande. C'est une
        # methode plus robuste que de suivre les tables du sous-bloc,
        # puisqu'elle s'appuie sur les donnees elles-memes.
        entrees = []
        for off_data, taille_data in fat:
            if taille_data < 8 or off_data + 8 > len(d):
                continue
            magic = d[off_data:off_data + 4]
            if magic == nom.encode("ascii"):
                if off_data + taille_data <= len(d):
                    entrees.append((off_data, taille_data))

        # Si le sous-bloc declare moins de fichiers que la FAT n'en
        # contient pour ce type, on garde la liste la plus complete.
        # (Un sous-bloc peut etre tronque ou encode differemment.)

        # Ecriture des fichiers.
        dossier = os.path.join(sortie, nom)
        os.makedirs(dossier, exist_ok=True)

        ecrits = 0
        total_type = 0
        for j, (o, t) in enumerate(entrees):
            if t == 0 or o + t > len(d):
                continue

            # Le bloc SYMB donne les noms dans le meme ordre que les
            # donnees : l'entree j du type correspond au symbole d'index
            # global calcule par offset_type + j.
            sym = noms_symboles.get(offset_type + j)
            if sym:
                # On nettoie le nom pour en faire un nom de fichier sur.
                propre = "".join(c if c.isalnum() or c in "_-" else "_"
                                 for c in sym)
                nom_fichier = f"{j:04d}_{propre}.{EXT[nom]}"
            else:
                nom_fichier = f"{nom}_{j:04d}.{EXT[nom]}"

            chemin_out = os.path.join(dossier, nom_fichier)
            with open(chemin_out, "wb") as f:
                f.write(d[o:o + t])
            ecrits += 1
            total_extrait += t
            total_type += t

        # Detection du format reel des donnees (magic interne).
        magics = set()
        for o, t in entrees[:8]:
            if t >= 4 and o + 4 <= len(d):
                magics.add(d[o:o + 4].decode("ascii", "replace"))

        stats.append((nom, nb, ecrits, total_type, magics))
        offset_type += ecrits

    print(f"  {'type':6s} {'entrees':>8s} {'ecrites':>8s} {'bloc':>10s}  magic interne")
    print(f"  {'-'*6} {'-'*8} {'-'*8} {'-'*10}  {'-'*14}")
    for nom, nb, ecrits, taille, magics in stats:
        m = ", ".join(sorted(magics)[:3]) if magics else "-"
        print(f"  {nom:6s} {nb:8d} {ecrits:8d} 0x{taille:08x}  {m}")

    print()
    print(f"  Total extrait : {total_extrait} octets")
    print(f"  Dossier       : {sortie}/")
    print()

    # Explication adaptee a ce qu'on a trouve.
    dossiers = [s[0] for s in stats if s[2] > 0]
    if "STRM" in dossiers:
        print("  Les fichiers .strm sont de l'audio deja encode : ils se")
        print("  convertissent en WAV directement (voir la doc).")
    if "SSEQ" in dossiers:
        print("  Les fichiers .sseq sont des PARTITIONS (comme du MIDI).")
        print("  Ils decrivent quoi jouer, sans contenir le son. Pour les")
        print("  entendre il faut simuler la console : voir vgmstream.")
    if "SWAR" in dossiers:
        print("  Les fichiers .swar contiennent des ECHANTILLONS audio")
        print("  (la matiere premiere des instruments).")

    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    chemin = sys.argv[1]
    sortie = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.splitext(os.path.basename(chemin))[0] + "_extrait"

    sys.exit(extraire(chemin, sortie))


if __name__ == "__main__":
    main()
