#!/usr/bin/env python3
"""
Explorateur du systeme de fichiers Nitro (NitroFS) d'une ROM NDS.

Le NitroFS est decrit par deux tables pointees par le header :
  - FNT (File Name Table) : un arbre de repertoires, chaque entree de
    repertoire faisant 8 octets { offset, premier_id_fichier, parent }.
  - FAT (File Allocation Table) : 8 octets par fichier { offset_debut, offset_fin }.

Les ID de fichiers sont attribues sequentiellement dans l'ordre du parcours
de l'arbre, a partir du "premier_id_fichier" du repertoire racine.
"""

import collections
import csv
import struct
import sys

# Extensions Nitro / formats Nintendo DS connus.
KINDS = {
    ".ncgr": "Graphismes 2D (tiles, comprime)",
    ".ncbr": "Graphismes 2D (bitmap brut)",
    ".nclr": "Palette de couleurs",
    ".nscr": "Disposition d'ecran (map 2D)",
    ".nftr": "Police de caracteres",
    ".nsbmd": "Modele 3D (geometrie)",
    ".nsbtx": "Textures 3D",
    ".nsbca": "Animation de squelette 3D",
    ".nsbtp": "Animation de motif (pattern)",
    ".nsbma": "Animation de materiau",
    ".nsbta": "Animation de texture (SRT)",
    ".nsbva": "Animation de visibilite",
    ".nsbmd": "Modele 3D",
    ".sdat": "Archive sonore complete (musiques + SFX)",
    ".sseq": "Sequence musicale (partition, format SMF-like)",
    ".ssbn": "Banque de sequences",
    ".swar": "Archive d'echantillons audio (WAV)",
    ".ssar": "Archive de sequences",
    ".sbnk": "Banque d'instruments",
    ".strm": "Musique streamee (PCM/ADPCM)",
    ".narc": "Archive Nitro (conteneur de fichiers)",
    ".srl": "ROM NDS imbriquee (jeu telecharge / demo)",
    ".bin": "Donnees brutes (a identifier)",
    ".dat": "Donnees brutes (a identifier)",
    ".arc": "Archive",
    ".txt": "Texte",
    ".scr": "Script",
    ".ovl": "Overlay",
}

# Magics Nintendo (stockes little-endian : "NCGR" -> b"RGCN").
MAGICS = {
    b"RGCN": "NCGR - tiles graphiques",
    b"RBCN": "NCBR - bitmap",
    b"RLCN": "NCLR - palette",
    b"RCSN": "NSCR - layout d'ecran",
    b"RTFN": "NFTR - police",
    b"J3D\x00": "modele 3D",
    b"MDL\x00": "modele 3D",
    b"TEX\x00": "texture",
    b"CRAN": "NARC - archive Nitro",
    b"STDS": "SDAT - archive sonore",
    b"QSTD": "archive",
}


def parse_fnt(fnt, root_first_file_id=0):
    """Parcourt l'arbre FNT et retourne [(file_id, "chemin/complet"), ...].

    Convention VERIFIEE sur les donnees reelles : le premier octet d'une entree
    donne la longueur du nom SEULE (il ne s'inclut pas lui-meme).
      - entree fichier    : 1 + N octets
      - entree repertoire : 1 + N + 2 (id) + 1 (parent) = N + 4 octets
    """
    files = []
    counter = [root_first_file_id]

    def dir_offset(did):
        return struct.unpack_from("<I", fnt, did * 8)[0] & 0x00FFFFFF

    def walk(off, path):
        while True:
            if off >= len(fnt):
                return
            b = fnt[off]
            if b == 0x00:                      # fin du repertoire
                return
            if b < 0x80:                       # entree de FICHIER
                name = fnt[off + 1:off + 1 + b].decode("utf-8", "replace")
                files.append((counter[0], path + name))
                counter[0] += 1
                off += b + 1
            else:                              # entree de SOUS-REPERTOIRE
                length = b & 0x7F
                name = fnt[off + 1:off + 1 + length].decode("utf-8", "replace")
                did = struct.unpack_from("<H", fnt, off + 1 + length)[0]
                walk(dir_offset(did - 0xF000), path + name + "/")
                off += length + 4              # type + nom + id(2) + parent(1)

    walk(dir_offset(0), "")
    return files


def main(rom_path, csv_out=None):
    with open(rom_path, "rb") as f:
        rom = f.read()

    header = rom[:0x200]
    fnt_off, fnt_size = struct.unpack_from("<II", header, 0x040)
    fat_off, fat_size = struct.unpack_from("<II", header, 0x048)
    arm9_off, _, _, arm9_size = struct.unpack_from("<IIII", header, 0x020)
    arm7_off, _, _, arm7_size = struct.unpack_from("<IIII", header, 0x030)
    ov9_off, ov9_size = struct.unpack_from("<II", header, 0x050)
    banner_off = struct.unpack_from("<I", header, 0x068)[0]

    fnt = rom[fnt_off:fnt_off + fnt_size]
    n_files = fat_size // 8

    # Chaque entree de table FNT fait 8 octets :
    #   u32 offset (bits 0-23 utiles) | u16 premier_id_fichier | u16 parent
    # Pour la racine, le champ "parent" contient le NOMBRE TOTAL de repertoires.
    root_first_id = struct.unpack_from("<H", fnt, 4)[0]
    n_dirs = struct.unpack_from("<H", fnt, 6)[0]

    files = parse_fnt(fnt, root_first_id)
    by_id = dict(files)

    # Table des overlays ARM9 : 32 octets par overlay.
    overlays = []
    for i in range(ov9_size // 32):
        oid, ram_addr, ram_size, bss_size, si_start, si_end, fid, _ = \
            struct.unpack_from("<8I", rom, ov9_off + i * 32)
        overlays.append({
            "id": oid, "ram_addr": ram_addr, "ram_size": ram_size,
            "bss_size": bss_size, "file_id": fid & 0xFFFFFF,
            "compressed": bool(fid & 0x01000000),
        })

    # Lecture de la FAT.
    records = []
    for fid in range(n_files):
        top, bottom = struct.unpack_from("<II", rom, fat_off + fid * 8)
        # Les bits hauts de "bottom" servent de flags sur certains jeux.
        if bottom > len(rom):
            bottom &= 0x00FFFFFF
        size = bottom - top
        name = by_id.get(fid, "<sans nom, id=%d>" % fid)
        records.append({"id": fid, "name": name, "offset": top, "size": size})

    print("=" * 78)
    print("NITROFS : %d fichiers repartis dans %d repertoires" % (len(records), n_dirs))
    print("=" * 78)

    print("\n--- A. OVERLAYS ARM9 (code charge a la demande) ---")
    if not overlays:
        print("  (aucun)")
    for o in overlays:
        name = by_id.get(o["file_id"], "?")
        print("  overlay %-3d -> RAM 0x%08X  taille %7s o  bss %6s o  fichier #%d (%s)%s" % (
            o["id"], o["ram_addr"], "{:,}".format(o["ram_size"]),
            "{:,}".format(o["bss_size"]), o["file_id"], name,
            "  [COMPRESSE]" if o["compressed"] else ""))
    print("  NB : les overlays partagent souvent la MEME adresse RAM. Un seul")
    print("      est resident a la fois ; il faut les analyser separement.")

    # ---- Repartition par type ----
    stats = collections.Counter()
    sizes = collections.Counter()
    for r in records:
        ext = "." + r["name"].rsplit(".", 1)[-1].lower() if "." in r["name"] else "(sans ext)"
        stats[ext] += 1
        sizes[ext] += r["size"]

    print("\n--- B. QUELLES DONNEES, EN QUELLE QUANTITE ? ---")
    print("%-10s %6s %14s   %s" % ("EXT", "NB", "OCTETS", "SIGNIFICATION"))
    for ext, n in stats.most_common(22):
        print("%-10s %6d %14s   %s" % (
            ext, n, "{:,}".format(sizes[ext]), KINDS.get(ext, "?")))

    # ---- Arborescence (2 premiers niveaux) ----
    print("\n--- C. ARBORESCENCE (dossiers racines) ---")
    roots = collections.Counter()
    for r in records:
        parts = r["name"].split("/")
        roots["/" + parts[0] if len(parts) > 1 else "(racine)"] += 1
    for d, n in roots.most_common(30):
        print("  %-30s %4d fichiers" % (d, n))

    # ---- Plus gros fichiers : c'est la que sont les donnees lourdes ----
    print("\n--- D. LES 20 PLUS GROS FICHIERS (ou sont les donnees lourdes) ---")
    for r in sorted(records, key=lambda x: -x["size"])[:20]:
        magic = ""
        if r["size"] >= 4:
            m = rom[r["offset"]:r["offset"] + 4]
            magic = MAGICS.get(m, "")
        print("  %-44s %10s o  @0x%08X  %s" % (
            r["name"][-44:], "{:,}".format(r["size"]), r["offset"], magic))

    # ---- Carte physique de la ROM ----
    print("\n--- E. CARTE PHYSIQUE DE LA ROM (ordre reel sur le support) ---")
    regions = [
        (0x00000000, 0x4000, "HEADER (512 o utiles + logo Nintendo)"),
        (arm9_off, arm9_off + arm9_size, "ARM9 - CODE PRINCIPAL (le jeu)"),
        (ov9_off, ov9_off + ov9_size, "Table des overlays ARM9"),
        (arm7_off, arm7_off + arm7_size, "ARM7 - CODE son/wifi/tactile"),
        (fnt_off, fnt_off + fnt_size, "FNT - arbre des noms de fichiers"),
        (fat_off, fat_off + fat_size, "FAT - table d'allocation"),
        (banner_off, banner_off + 0x840, "BANNIERE - icone + titres"),
    ]
    # Ajoute les 12 plus gros fichiers NitroFS comme regions.
    for r in sorted(records, key=lambda x: -x["size"])[:12]:
        regions.append((r["offset"], r["offset"] + r["size"], "NitroFS: " + r["name"]))
    for start, end, label in sorted(regions):
        if end <= start:
            continue
        bar_len = max(1, int((end - start) / len(rom) * 60))
        pos = int(start / len(rom) * 60)
        print("  0x%08X-0x%08X %8s o  %s" % (start, end, "{:,}".format(end - start), label))

    print("\n  Taille ROM : %s octets (%.1f MiO)" % ("{:,}".format(len(rom)), len(rom) / 1048576))
    total_fs = sum(r["size"] for r in records)
    print("  Dont NitroFS : %s octets (%.1f%%)" % ("{:,}".format(total_fs), 100 * total_fs / len(rom)))
    print("  Dont code ARM9+ARM7 : %s octets" % "{:,}".format(arm9_size + arm7_size))

    # ---- Export CSV ----
    if csv_out:
        with open(csv_out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "chemin", "offset_rom", "taille", "type_suppose"])
            for r in records:
                ext = ("." + r["name"].rsplit(".", 1)[-1].lower()) if "." in r["name"] else ""
                w.writerow([r["id"], r["name"], hex(r["offset"]), r["size"], KINDS.get(ext, "")])
        print("\n  Liste complete exportee : %s" % csv_out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: nds_fs.py <rom.nds> [sortie.csv]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
