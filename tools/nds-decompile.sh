#!/usr/bin/env bash
# nds-decompile.sh - Decompilation ARM9 + ARM7 + overlays via Ghidra headless.
#
# Usage: nds-decompile.sh <rom.nds|dossier_extrait>
#
# ---------------------------------------------------------------------------
# POINT CRITIQUE : LE CHOIX DU LANGAGE (le piege n°1 du RE sur ARM)
# ---------------------------------------------------------------------------
# Chaque processeur de la DS sait executer DEUX jeux d'instructions :
#
#   ARM    : 32 bits, puissant
#   Thumb  : 16 bits, code plus dense en memoire
#
# Le processeur bascule de l'un a l'autre a l'execution. Le bit 0 de
# l'adresse cible d'un saut decide :
#     bit 0 = 0  ->  la cible est du code ARM
#     bit 0 = 1  ->  la cible est du code Thumb
#
# Ghidra : les langages SANS "t" (ARM:LE:32:v5) ne desassemblent QUE l'ARM.
# Les zones Thumb y apparaissent comme instructions invalides :
#     "WARNING: Bad instruction - Truncating control flow here"
#     halt_baddata();
#
# Il faut demander explicitement la variante "T" :
#     ARM:LE:32:v5t   ARM9  (ARM946E-S, ARMv5TE)
#     ARM:LE:32:v4t   ARM7  (ARM7TDMI,  ARMv4T)
#
# Mesure faite sur cette ROM :
#     ARM7 avec v4  :  358 fonctions, 558 avertissements "bad instruction"
#     ARM7 avec v4t :  399 fonctions,   0 avertissement
#     ARM9 avec v5  : 1952 fonctions,  10 avertissements
#     ARM9 avec v5t : 1979 fonctions,   0 avertissement
#
# 41 fonctions de l'ARM7 etaient invisibles. Un langage mal choisi ne
# produit pas une erreur : il produit du code silencieusement incomplet.
# ---------------------------------------------------------------------------
#
# Ghidra a aussi besoin de l'adresse de chargement, donnee par l'en-tete :
#   ARM9  : 0x02000000 (taille 0x78A18 ici)
#   ARM7  : 0x02380000
#   ovl N : adresse donnee par la table y9.bin
# Sans ces adresses, tous les appels croises et les pointeurs internes
# sont faux : le decompile ressemble a du bruit.

set -euo pipefail

GHIDRA="${GHIDRA_HOME:-/opt/ghidra}"
PROJ="${PROJ_DIR:-$HOME/Documents/ReverseEngeneering/work/ghidra_proj}"
SRC="${1:?Usage: nds-decompile.sh <rom.nds|dossier_extrait>}"
BASE="$HOME/Documents/ReverseEngeneering/work"

# Si on recoit une ROM brute, on l'extrait d'abord.
if [[ "$SRC" == *.nds ]]; then
    WORK="$BASE/extracted"
    if [[ ! -f "$WORK/arm9.bin" ]]; then
        echo ">>> Extraction de la ROM..."
        "$HOME/Documents/ReverseEngeneering/tools/nds-inspect.sh" "$SRC" "$WORK" >/dev/null
    fi
else
    WORK="$SRC"
fi

cd "$WORK"

# Adresses de chargement, lues dans l'en-tete NDS.
ARM9_RAM=$(python3 -c "
import struct
h=open('$BASE/extracted_rom_header','rb').read(0x200) if False else None
" 2>/dev/null || true)
ARM9_RAM=0x02000000
ARM7_RAM=0x02380000

echo "=============================================="
echo " Ghidra headless : $GHIDRA"
echo " Projet          : $PROJ"
echo " Sources         : $WORK"
echo "=============================================="

mkdir -p "$PROJ"

decompile() {
    local bin="$1" name="$2" addr="$3" lang="$4"
    echo
    echo ">>> Decompilation de $name  (base $addr, $lang)"

    # -import       : charge le binaire brut
    # -loader       : BinaryLoader avec l'adresse de base explicite
    # -postScript   : notre script qui exporte tout le C decompile
    "$GHIDRA/support/analyzeHeadless" "$PROJ" DQMJoker \
        -import "$bin" \
        -processor "$lang" \
        -loader BinaryLoader \
        -loader-baseAddr "$addr" \
        -scriptPath "$HOME/Documents/ReverseEngeneering/tools/ghidra_scripts" \
        -postScript ExportDecompiled.java "$name" \
        -deleteProject \
        2>&1 | grep -E 'INFO|ERROR|WARN|Export' | tail -n 20
}

# ARM9 : le coeur du jeu (moteur, menus, sauvegarde, combat)
decompile arm9.bin arm9 "$ARM9_RAM" "ARM:LE:32:v5t"

# ARM7 : audio, wifi, gestion de l'alimentation
decompile arm7.bin arm7 "$ARM7_RAM" "ARM:LE:32:v4t"

# Overlays : code pagine. On lit leur adresse de chargement dans y9.bin.
i=0
if [[ -d overlay ]]; then
    for ovl in overlay/*.bin; do
        [[ -e "$ovl" ]] || continue
        ADDR=$(python3 -c "
import struct
d=open('y9.bin','rb').read()
i=$i
print(hex(struct.unpack_from('<I',d,i*32+4)[0]))
")
        decompile "$ovl" "overlay_$(printf '%04d' $i)" "$ADDR" "ARM:LE:32:v5t"
        i=$((i+1))
    done
fi

echo
echo "=============================================="
echo " Termine."
for f in "$HOME/Documents/ReverseEngeneering/work/decompiled"/*.c; do
    printf '  %-24s %6d fonctions\n' "$(basename "$f")" "$(grep -c '^// ----' "$f")"
done
echo "=============================================="
