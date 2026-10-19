#!/usr/bin/env python3
"""
Remonter d'une CHAINE au CODE qui l'utilise, dans un binaire ARM brut.

Pourquoi ce n'est pas trivial : sur ARM, une instruction ne peut pas contenir
une adresse 32 bits en immediat. Le compilateur pose donc l'adresse dans un
"pool litteral" (une table de mots 32 bits glissee au milieu du code), puis
emett un `ldr rX, [pc, #imm]` qui la charge par rapport au PC.

La chaine de references est donc :
    code  --ldr [pc,#imm]-->  entree du pool litteral  --valeur-->  la chaine

Cet outil remonte les trois maillons :
  1. localise toutes les occurrences de la chaine,
  2. indexe tous les mots 32 bits alignes du binaire et trouve ceux qui
     contiennent l'adresse d'une occurrence (= entrees de pool litteral),
  3. decode chaque instruction ARM/Thumb `ldr rX,[pc,#imm]` et verifie si elle
     pointe sur l'une de ces entrees.

Usage : xref_string.py <binaire> <adresse_de_base> <chaine>
"""

import struct
import sys


def find_all(data, needle):
    out = []
    start = 0
    while True:
        i = data.find(needle, start)
        if i < 0:
            return out
        out.append(i)
        start = i + 1


def build_word_index(data):
    """value -> [offsets alignes sur 4] pour tout le binaire."""
    idx = {}
    for off in range(0, len(data) - 3, 4):
        v = struct.unpack_from("<I", data, off)[0]
        idx.setdefault(v, []).append(off)
    return idx


def pc_relative_loads(data, base):
    """Genere (offset_instr, adresse_cible) pour chaque `ldr rX,[pc,#imm]`.

    ARM   : cond 0101 1001 1111 Rd imm12        -> masque 0x0FFF0000 == 0x059F0000
            cible = (PC + 8) & ~3 + imm12
    Thumb : 0100 1 Rd imm8  (mot de 16 bits)    -> masque 0xF800 == 0x4800
            cible = ((PC + 4) & ~3) + imm8*4
    """
    out = []
    for off in range(0, len(data) - 3, 2):
        half = struct.unpack_from("<H", data, off)[0]
        if (half & 0xF800) == 0x4800:                      # Thumb ldr rX,[pc,#imm8*4]
            rd = (half >> 8) & 7
            target = ((base + off + 4) & ~3) + (half & 0xFF) * 4
            out.append((off, target, "thumb", "r%d" % rd))
    for off in range(0, len(data) - 3, 4):
        w = struct.unpack_from("<I", data, off)[0]
        if (w & 0x0FFF0000) == 0x059F0000:                 # ARM ldr rX,[pc,#imm12]
            rd = (w >> 12) & 0xF
            target = ((base + off + 8) & ~3) + (w & 0xFFF)
            out.append((off, target, "arm", "r%d" % rd))
    return out


def main(binpath, base, needle):
    data = open(binpath, "rb").read()
    nb = needle.encode("utf-8")

    print("Binaire      : %s (%s octets)" % (binpath, f"{len(data):,}"))
    print("Base         : 0x%08X" % base)
    print("Chaine       : %r" % needle)

    occs = find_all(data, nb)
    if not occs:
        print("\nAucune occurrence trouvee.")
        return 1
    print("\n--- 1. Occurrences de la chaine ---")
    for o in occs:
        print("    offset 0x%06X  ->  adresse 0x%08X" % (o, base + o))

    print("\n--- 2. Entrees de pool litteral pointant sur ces occurrences ---")
    idx = build_word_index(data)
    pool_slots = {}          # adresse_du_slot -> adresse_de_la_chaine
    for o in occs:
        for slot_off in idx.get(base + o, []):
            pool_slots[base + slot_off] = base + o
    if not pool_slots:
        print("    (aucune : la chaine n'est pas referencee par une adresse absolue)")
        return 0
    for slot, target in sorted(pool_slots.items()):
        print("    slot 0x%08X (offset 0x%06X) contient 0x%08X" % (
            slot, slot - base, target))

    print("\n--- 3. Instructions qui chargent ces slots ---")
    hits = []
    for off, target, mode, reg in pc_relative_loads(data, base):
        if target in pool_slots:
            hits.append((off, target, mode, reg))
    if not hits:
        print("    (aucune instruction `ldr rX,[pc,#imm]` ne vise ces slots)")
        return 0
    for off, target, mode, reg in sorted(hits):
        print("    0x%08X  [%-5s] ldr %s, [pc, #0x%X]   -> pool 0x%08X -> \"%s\"" % (
            base + off, mode, reg, target - ((base + off + 8) & ~3) if mode == "arm"
            else target - ((base + off + 4) & ~3), target, needle))

    print("\n--- 4. Contexte a desassembler ---")
    for off, target, mode, reg in sorted(hits):
        start = max(0, off - 0x28)
        end = min(len(data), off + 0x2C)
        print("\n    autour de 0x%08X (%s) :" % (base + off, mode))
        print("      arm-none-eabi-objdump -D -b binary -m arm%s --adjust-vma=0x%08X "
              "--start-address=0x%08X --stop-address=0x%08X %s"
              % (" -M force-thumb" if mode == "thumb" else "",
                 base, base + start, base + end, binpath))
        print("      radare2 -a arm -b %d -m 0x%08X -q -c 'pd -8 @ 0x%08X; pd 14 @ 0x%08X' %s"
              % (16 if mode == "thumb" else 32, base, base + off, base + off, binpath))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], int(sys.argv[2], 0), sys.argv[3]))
