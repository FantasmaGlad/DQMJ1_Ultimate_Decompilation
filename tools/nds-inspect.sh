#!/usr/bin/env bash
# nds-inspect.sh - Decoupe une ROM Nintendo DS en ses composants analysables.
#
# Usage: nds-inspect.sh <rom.nds> [dossier_sortie]
#
# Ce script n'est qu'une enveloppe lisible autour de ndstool : il rend
# explicite ce que la ROM contient reellement, pour qu'on sache quoi
# mettre ensuite dans Ghidra ou radare2.

set -euo pipefail

ROM="${1:?Usage: nds-inspect.sh <rom.nds> [dossier_sortie]}"
OUT="${2:-$(basename "${ROM%.*}")_unpacked}"

if [[ ! -f "$ROM" ]]; then
    echo "Erreur : ROM introuvable : $ROM" >&2
    exit 1
fi

echo "=============================================="
echo " ROM      : $ROM"
echo " Sortie   : $OUT"
echo "=============================================="

mkdir -p "$OUT"
cd "$OUT"

# -9/-7     : les deux processeurs (ARM9 = principal, ARM7 = audio/wifi)
# -y9/-y7   : les tables d'overlays (code pagine, charge a la demande)
# -d data   : tous les fichiers du systeme de fichiers interne
# -t banner : la banniere affichee par le menu de la console
ndstool -x "$OLDPWD/$ROM" \
    -9 arm9.bin -7 arm7.bin \
    -y9 y9.bin  -y7 y7.bin \
    -d data -y overlay \
    -t banner.bin -v 2>&1 | tail -n 25

echo
echo "--- Contenu de la ROM (en-tete) ---"
ndstool -i "$OLDPWD/$ROM"

echo
echo "--- Fichiers extraits ---"
printf '  arm9.bin (coeur du jeu) : %s octets\n' "$(stat -c%s arm9.bin)"
printf '  arm7.bin (audio/wifi)   : %s octets\n' "$(stat -c%s arm7.bin)"
printf '  overlays (code pagine)  : %s fichiers\n' "$(ls -1 overlay 2>/dev/null | wc -l)"
printf '  data/ (assets+donnees)  : %s fichiers\n' "$(find data -type f 2>/dev/null | wc -l)"

echo
echo "Termine. Dossier : $OUT"
