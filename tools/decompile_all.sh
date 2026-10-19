#!/usr/bin/env bash
# =============================================================================
# Exporte le pseudo-code C de tous les binaires d'un projet Ghidra.
#
#   decompile_all.sh [dossier_projet] [nom_projet] [dossier_sortie]
#
# Chaque binaire du projet est traité par le script Ghidra DecompileAll.java,
# qui décompile toutes les fonctions reconnues par l'auto-analyse.
# =============================================================================
set -uo pipefail

PROJ_DIR="${1:-$HOME/Documents/DS/ghidra}"
PROJ="${2:-DQMJoker}"
OUT="${3:-$HOME/Documents/DS/work/decompiled}"
CODE="${4:-$HOME/Documents/DS/work/code}"
SCRIPTS="$HOME/Documents/DS/tools/ghidra_scripts"
HEADLESS="/opt/ghidra/support/analyzeHeadless"

[ -x "$HEADLESS" ] || { echo "analyzeHeadless introuvable : $HEADLESS"; exit 1; }
[ -d "$PROJ_DIR/$PROJ.rep" ] || { echo "projet Ghidra introuvable : $PROJ_DIR/$PROJ"; exit 1; }
mkdir -p "$OUT"

shopt -s nullglob
BINS=("$CODE"/*.bin)
if [ ${#BINS[@]} -eq 0 ]; then
    echo "Aucun .bin dans $CODE — lancer d'abord extract_code.py"
    exit 1
fi

echo "Projet Ghidra : $PROJ_DIR/$PROJ"
echo "Binaires      : ${#BINS[@]}"
echo "Sortie        : $OUT"
echo

for path in "${BINS[@]}"; do
    name="$(basename "$path")"
    cfile="$OUT/${name%.bin}.c"
    echo "=============================================================="
    echo " $name -> $(basename "$cfile")"
    echo "=============================================================="
    "$HEADLESS" "$PROJ_DIR" "$PROJ" -process "$name" -noanalysis -readOnly \
        -scriptPath "$SCRIPTS" -postScript DecompileAll.java "$cfile" \
        2>&1 | grep -E "DecompileAll.java>|TERMINE|fonctions|decompilees|echec|sortie|ERROR" \
        | sed 's/^INFO  DecompileAll.java> //'
    echo
done

echo "=============================================================="
echo " SYNTHÈSE"
echo "=============================================================="
printf '%-28s %10s %12s\n' "FICHIER" "LIGNES" "OCTETS"
TOTAL_LINES=0
for f in "$OUT"/*.c; do
    [ -f "$f" ] || continue
    lines=$(wc -l < "$f")
    TOTAL_LINES=$((TOTAL_LINES + lines))
    printf '%-28s %10s %12s\n' "$(basename "$f")" "$lines" "$(stat -c%s "$f")"
done
echo
echo "Total : $TOTAL_LINES lignes de pseudo-C dans $OUT"
echo "Fonctions décompilées : $(grep -hc '^/\* ==== ' "$OUT"/*.c 2>/dev/null | paste -sd+ | bc)"
