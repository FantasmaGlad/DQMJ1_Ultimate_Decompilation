#!/usr/bin/env python3
"""
Extraction complete du CODE d'une ROM NDS.

Ce que fait ce script :
  1. Lit le conteneur .nds (non chiffre) avec ndspy.
  2. Decoupe l'ARM9 selon sa vraie structure NitroSDK :
       - section "implicite"  -> reste a ramAddress (0x02000000), c'est le jeu
       - sections annexes     -> recopiees ailleurs au boot via la "copy table"
     La copy table est decrite par 3 u32 situes a codeSettingsOffs.
  3. Extrait l'ARM7 (son/wifi/tactile) et chaque overlay ARM9.
  4. Neutralise la Secure Area (2 Ko chiffres, fonctionnellement vides).
  5. Ecrit un manifeste JSON : adresses de base + points d'entree, necessaires
     pour charger correctement les binaires dans un desassembleur.

Sortie : <outdir>/{arm9.bin, arm9_sec_*.bin, arm7.bin, overlay_NN.bin, manifest.json}
"""

import json
import os
import sys

import ndspy.rom

SECURE_AREA_SIZE = 0x800   # 2 Ko chiffres en tete de l'ARM9 (contenu inutile)


def hexa(n):
    return "0x%08X" % n if n is not None else "?"


def main(rom_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    print("Chargement de %s" % rom_path)
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)

    manifest = {
        "rom": os.path.basename(rom_path),
        "title": bytes(rom.name).decode("ascii", "replace").strip("\x00"),
        "gameCode": bytes(rom.idCode).decode("ascii", "replace").strip("\x00"),
        "developerCode": bytes(rom.developerCode).decode("ascii", "replace").strip("\x00"),
        "architecture": "ARM (little-endian) - ARM9 = ARM946E-S (ARMv5TE), ARM7 = ARM7TDMI (ARMv4T)",
        "ghidraLanguage": "ARM:LE:32:v5t",
        "binaries": [],
        "notes": [
            "Les 2 premiers Ko de arm9.bin (Secure Area) sont chiffres par la DS : "
            "une fois dechiffres ils ne contiennent que 'encryObj' + des zeros. "
            "Ils sont remplaces par des zeros ici pour ne pas polluer l'analyse.",
            "Le point d'entree reel de l'ARM9 est 0x02000800, juste apres la Secure Area.",
            "Les overlays sont charges a la MEME adresse RAM : un seul est resident "
            "a la fois. A analyser comme des binaires distincts.",
        ],
    }

    # ---------------- ARM9 ----------------
    print("\n=== ARM9 : CPU principal (logique du jeu) ===")
    mcf = rom.loadArm9()
    print("  ramAddress          : %s" % hexa(mcf.ramAddress))
    print("  codeSettingsOffs    : %s" % hexa(mcf.codeSettingsOffs))
    print("  entry point (header): %s" % hexa(rom.arm9EntryAddress))
    print("  %d section(s) :" % len(mcf.sections))

    for i, sec in enumerate(mcf.sections):
        data = bytearray(sec.data)
        implicit = bool(getattr(sec, "implicit", False))
        if i == 0:
            # Section principale : neutralise la Secure Area chiffree.
            enc = bytes(data[:SECURE_AREA_SIZE])
            was_encrypted = any(enc[16:])
            data[:SECURE_AREA_SIZE] = b"\x00" * SECURE_AREA_SIZE
            fname = "arm9.bin"
            label = "arm9 (section principale)"
            note = ("Secure Area chiffree detectee puis azeree ; point d'entree reel %s"
                    % hexa(rom.arm9EntryAddress)) if was_encrypted else ""
        else:
            fname = "arm9_sec_%08X.bin" % sec.ramAddress
            label = "arm9 section %d (annexe)" % i
            note = "recopiee a %s au boot par la copy table ; bss %d o" % (
                hexa(sec.ramAddress), sec.bssSize)
        open(os.path.join(outdir, fname), "wb").write(data)
        print("    [%d] %-28s -> %-26s %9s o  base %s  bss %d" % (
            i, label, fname, f"{len(data):,}", hexa(sec.ramAddress), sec.bssSize))
        manifest["binaries"].append({
            "name": "arm9" if i == 0 else "arm9_section%d" % i,
            "file": fname,
            "baseAddress": sec.ramAddress,
            "entryPoint": rom.arm9EntryAddress if i == 0 else None,
            "size": len(data),
            "bssSize": sec.bssSize,
            "implicit": implicit,
            "role": ("Code principal du jeu (ARM946E-S, ARMv5TE, mixte ARM/Thumb)"
                     if i == 0 else note),
        })

    # ---------------- ARM7 ----------------
    print("\n=== ARM7 : coprocesseur (son / Wi-Fi / tactile) ===")
    mcf7 = rom.loadArm7()
    print("  ramAddress          : %s" % hexa(mcf7.ramAddress))
    print("  entry point (header): %s" % hexa(rom.arm7EntryAddress))
    for i, sec in enumerate(mcf7.sections):
        data = bytes(sec.data)
        fname = "arm7.bin" if i == 0 else "arm7_sec_%08X.bin" % sec.ramAddress
        open(os.path.join(outdir, fname), "wb").write(data)
        print("    [%d] %-24s %9s o  base %s  bss %d" % (
            i, fname, f"{len(data):,}", hexa(sec.ramAddress), sec.bssSize))
        manifest["binaries"].append({
            "name": "arm7" if i == 0 else "arm7_section%d" % i, "file": fname,
            "baseAddress": sec.ramAddress,
            "entryPoint": rom.arm7EntryAddress if i == 0 else None,
            "size": len(data), "bssSize": sec.bssSize,
            "implicit": bool(getattr(sec, "implicit", False)),
            "role": "ARM7TDMI : audio, Wi-Fi, ecran tactile, horloge temps reel",
            "ghidraLanguage": "ARM:LE:32:v4t",
        })

    # ---------------- Overlays ----------------
    print("\n=== OVERLAYS ARM9 : modules charges a la demande ===")
    overlays = rom.loadArm9Overlays()
    if not overlays:
        print("  (aucun)")
    for oid in sorted(overlays):
        ov = overlays[oid]
        data = bytes(ov.data)
        fname = "overlay_%02d.bin" % oid
        open(os.path.join(outdir, fname), "wb").write(data)
        print("  overlay %-3d -> %-18s %9s o  base %s  bss %8s o  compresse=%s" % (
            oid, fname, f"{len(data):,}", hexa(ov.ramAddress),
            f"{ov.bssSize:,}", bool(ov.compressed)))
        print("             staticInit %s .. %s" % (
            hexa(ov.staticInitStart), hexa(ov.staticInitEnd)))
        manifest["binaries"].append({
            "name": "overlay_%d" % oid, "file": fname,
            "baseAddress": ov.ramAddress, "size": len(data),
            "bssSize": ov.bssSize, "wasCompressed": bool(ov.compressed),
            "staticInitStart": ov.staticInitStart, "staticInitEnd": ov.staticInitEnd,
            "role": "Overlay %d - module de code charge dynamiquement" % oid,
        })

    # ---------------- Manifeste ----------------
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n=== TERMINE ===")
    print("  Dossier   : %s" % os.path.abspath(outdir))
    total = sum(b["size"] for b in manifest["binaries"])
    print("  Binaire(s): %d, total %s octets de code" % (
        len(manifest["binaries"]), f"{total:,}"))
    print("  Manifeste : %s" % os.path.join(outdir, "manifest.json"))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: extract_code.py <rom.nds> <dossier_sortie>")
    main(sys.argv[1], sys.argv[2])
