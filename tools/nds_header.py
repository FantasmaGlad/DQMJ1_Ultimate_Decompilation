#!/usr/bin/env python3
"""
Parseur d'en-tête NDS (Nintendo DS ROM image) - outil pédagogique.

Reference du format : gbatek "DS Cartridge Header" / "DS Cartridge File System".
Un .nds est un conteneur plat : le header de 512 octets decrit OU se trouvent
les deux binaires ARM, l'arbre de noms de fichiers (FNT), la table d'allocation
(FAT), les overlays et la banniere.
"""

import hashlib
import struct
import sys

U32 = "<I"
U16 = "<H"


def u32(data, off):
    return struct.unpack_from(U32, data, off)[0]


def u16(data, off):
    return struct.unpack_from(U16, data, off)[0]


def ascii_field(data, off, size):
    return data[off:off + size].split(b"\x00")[0].decode("ascii", "replace")


def hexs(data, off, size):
    return data[off:off + size].hex()


def main(path):
    with open(path, "rb") as f:
        head = f.read(0x200)
        f.seek(0)
        full_sha1 = hashlib.sha1(f.read()).hexdigest()

    if len(head) < 0x200:
        sys.exit("Fichier trop petit pour etre un .nds")

    h = {}
    h["game_title"] = ascii_field(head, 0x000, 12)
    h["game_code"] = ascii_field(head, 0x00C, 4)
    h["maker_code"] = ascii_field(head, 0x010, 2)
    h["unit_code"] = head[0x012]
    h["encryption_seed_select"] = head[0x013]
    cap_exp = head[0x014]
    h["device_capacity"] = cap_exp
    h["device_capacity_bytes"] = (128 * 1024) << cap_exp if cap_exp else 0
    h["dsi_flags"] = u16(head, 0x018)
    h["rom_version"] = head[0x01E]
    h["internal_flag"] = head[0x01F]

    h["arm9_rom_offset"] = u32(head, 0x020)
    h["arm9_entry_address"] = u32(head, 0x024)
    h["arm9_ram_address"] = u32(head, 0x028)
    h["arm9_size"] = u32(head, 0x02C)

    h["arm7_rom_offset"] = u32(head, 0x030)
    h["arm7_entry_address"] = u32(head, 0x034)
    h["arm7_ram_address"] = u32(head, 0x038)
    h["arm7_size"] = u32(head, 0x03C)

    h["fnt_offset"] = u32(head, 0x040)
    h["fnt_size"] = u32(head, 0x044)
    h["fat_offset"] = u32(head, 0x048)
    h["fat_size"] = u32(head, 0x04C)

    h["arm9_overlay_offset"] = u32(head, 0x050)
    h["arm9_overlay_size"] = u32(head, 0x054)
    h["arm7_overlay_offset"] = u32(head, 0x058)
    h["arm7_overlay_size"] = u32(head, 0x05C)

    h["normal_card_control"] = u32(head, 0x060)
    h["secure_card_control"] = u32(head, 0x064)
    h["banner_offset"] = u32(head, 0x068)
    h["secure_area_crc"] = u16(head, 0x06C)
    h["secure_transfer_timeout"] = u16(head, 0x06E)
    h["arm9_autoload"] = u32(head, 0x074)
    h["arm7_autoload"] = u32(head, 0x078)
    h["secure_area_disable"] = u32(head, 0x07C)
    h["total_used_rom_size"] = u32(head, 0x080)
    h["rom_header_size"] = u32(head, 0x084)

    h["logo_crc"] = u16(head, 0x15C)
    h["header_crc"] = u16(head, 0x15E)

    print("=" * 68)
    print("EN-TETE NDS : %s" % path)
    print("=" * 68)

    print("\n--- IDENTITE ---")
    print("  Titre                : %r" % h["game_title"])
    print("  Game code            : %s   (lettre 1 = plateforme, lettre 4 = region)"
          % h["game_code"])
    print("  Maker code           : %s" % h["maker_code"])
    print("  Version ROM          : %d" % h["rom_version"])
    print("  Flags DSi            : 0x%04x" % h["dsi_flags"])
    print("  Capacite declaree    : 2^%d * 128Ko = %d MiO"
          % (h["device_capacity"], h["device_capacity_bytes"] // (1024 * 1024)))
    print("  SHA1 complet         : %s" % full_sha1)

    print("\n--- PROCESSEURS (le coeur du reverse) ---")
    print("  ARM9 (CPU principal, le jeu)")
    print("    offset ROM         : 0x%08X" % h["arm9_rom_offset"])
    print("    adresse d'entree   : 0x%08X" % h["arm9_entry_address"])
    print("    adresse RAM        : 0x%08X  <-- base a donner au desassembleur"
          % h["arm9_ram_address"])
    print("    taille             : %d octets (%.1f KiO)"
          % (h["arm9_size"], h["arm9_size"] / 1024))
    print("  ARM7 (coprocesseur : son, wifi, tactile)")
    print("    offset ROM         : 0x%08X" % h["arm7_rom_offset"])
    print("    adresse d'entree   : 0x%08X" % h["arm7_entry_address"])
    print("    adresse RAM        : 0x%08X" % h["arm7_ram_address"])
    print("    taille             : %d octets (%.1f KiO)"
          % (h["arm7_size"], h["arm7_size"] / 1024))

    print("\n--- SYSTEME DE FICHIERS ---")
    print("  FNT (arbre des noms) : offset 0x%08X  taille %d" % (h["fnt_offset"], h["fnt_size"]))
    print("  FAT (table fichiers) : offset 0x%08X  taille %d  => %d fichiers"
          % (h["fat_offset"], h["fat_size"], h["fat_size"] // 16))

    print("\n--- OVERLAYS (blocs de code charges a la volee) ---")
    print("  ARM9 overlays        : offset 0x%08X  taille %d  => %d overlay(s)"
          % (h["arm9_overlay_offset"], h["arm9_overlay_size"],
             h["arm9_overlay_size"] // 32))
    print("  ARM7 overlays        : offset 0x%08X  taille %d"
          % (h["arm7_overlay_offset"], h["arm7_overlay_size"]))

    print("\n--- AUTRES ---")
    print("  Banniere             : offset 0x%08X" % h["banner_offset"])
    print("  Taille ROM utilisee  : %d octets (%.1f MiO)"
          % (h["total_used_rom_size"], h["total_used_rom_size"] / 1048576))
    print("  CRC logo Nintendo    : 0x%04X  (attendu 0xCF56 -> %s)"
          % (h["logo_crc"], "OK" if h["logo_crc"] == 0xCF56 else "INVALIDE"))
    print("  CRC header (0x000-0x15D) : 0x%04X -> %s"
          % (h["header_crc"],
             "OK" if h["header_crc"] == crc16(head[:0x15E]) else "INVALIDE"))

    # Verifie si l'ARM9 est compresse : la compression Nitro ajoute une en-tete
    # de 8 octets en fin de bloc (4 octets de taille + marqueur "DEC0"/"BLZ_").
    with open(path, "rb") as f:
        f.seek(h["arm9_rom_offset"])
        arm9_start = f.read(32)
        f.seek(h["arm9_rom_offset"] + h["arm9_size"] - 12)
        arm9_tail = f.read(12)
    print("\n--- ARM9 : 32 premiers octets ---")
    print("  " + arm9_start.hex(" "))
    print("--- ARM9 : 12 derniers octets ---")
    print("  " + arm9_tail.hex(" "))
    marker = arm9_tail[4:8]
    if marker in (b"DEC0", b"DEC1", b"BLZ_", b"\x21\x06\xc0\xde"):
        print("  => Compression Nitro detectee (marqueur %r) : l'ARM9 DOIT etre"
              " decompresse avant analyse." % marker)
    elif arm9_start[:4] == b"\x21\x06\xc0\xde":
        print("  => Compression Nitro (marqueur de debut C0DE0621).")
    else:
        print("  => Aucun marqueur de compression evident : verifier quand meme"
              " avec ndspy.")

    if h["banner_offset"]:
        dump_banner(path, h["banner_offset"])


NDS_BANNER_LANGS = ["japonais", "anglais", "francais", "allemand", "italien", "espagnol"]


def dump_banner(path, off):
    with open(path, "rb") as f:
        f.seek(off)
        b = f.read(0x840)
    print("\n--- BANNIERE (icone + titres localises) ---")
    print("  version : %d" % u16(b, 0))
    print("  CRC16   : %s" % " ".join("0x%04X" % u16(b, 2 + 2 * i) for i in range(4)))
    for i, lang in enumerate(NDS_BANNER_LANGS):
        raw = b[0x220 + i * 0x200: 0x220 + (i + 1) * 0x200]
        title = raw.decode("utf-16-le", "replace").replace("\x00", "").strip()
        if title:
            print("  %-9s : %s" % (lang, " / ".join(title.split("\n"))))


def crc16(data):
    """CRC-16/CCITT modbus inverse utilise par Nintendo (poly 0xA001)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: nds_header.py <rom.nds>")
    main(sys.argv[1])
