#!/usr/bin/env python3
"""Extrait les archives de carte .map (format FPK) vers work/maps/<carte>/.

Format FPK (verifie sur les 90 cartes) :
  0x00  "FPK\\0"
  0x04  u32 nombre d'entrees
  0x08  entrees de 40 octets : nom (32 o, ASCII, complete par des 0), u32 offset, u32 taille
Le contenu est un ensemble de fichiers Nitro : .nsbmd (modeles), .nsbtx (textures),
.nsbta/.nsbma (animations), .atr, .scn, .pos (donnees de carte).
"""
import struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work/extracted/data"
DST = ROOT / "work/maps"

def unpack(path):
    d = path.read_bytes()
    if d[:4] != b"FPK\0":
        raise ValueError(f"{path.name}: pas un FPK")
    n = struct.unpack_from("<I", d, 4)[0]
    for i in range(n):
        o = 8 + 40 * i
        name = d[o:o + 32].split(b"\0")[0].decode("latin1")
        off, size = struct.unpack_from("<II", d, o + 32)
        if off + size > len(d):
            raise ValueError(f"{path.name}:{name} depasse le fichier")
        yield name, d[off:off + size]

def main():
    total = 0
    for m in sorted(SRC.glob("*.map")):
        out = DST / m.stem
        out.mkdir(parents=True, exist_ok=True)
        for name, blob in unpack(m):
            (out / name).write_bytes(blob)
            total += 1
    print("extrait", total, "fichiers dans", DST)

if __name__ == "__main__":
    main()
