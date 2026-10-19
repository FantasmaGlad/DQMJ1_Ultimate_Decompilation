#!/usr/bin/env bash
# =============================================================================
# generate_previews.sh -- Genere un PNG d'apercu pour chaque .blend de la
# bibliotheque ModelBlender.
#
# Les apercus permettent de PARCOURIR la bibliotheque sans ouvrir Blender :
# on regarde les vignettes, puis on ouvre seulement celui qui interesse.
#
# Usage :
#   tools/generate_previews.sh [nb_paralleles]
#
# =============================================================================
# ATTENTION MEMOIRE
# =============================================================================
# Chaque instance de Blender consomme 400 Mo a 1,2 Go (le moteur de rendu
# charge la scene entiere). Sur une machine de 14 Go, lancer 8 instances
# en parallele sature la RAM : 13 Go utilises sur 14, le systeme passe en
# swap et tout devient tres lent.
#
# La valeur par defaut est donc 2, et le script REFUSE d'aller au-dela de
# 3 sur une machine de moins de 24 Go, quelle que soit la valeur demandee.
#
# Le traitement se fait par VAGUES : on lance N rendus, on attend qu'ils
# soient TOUS termines, puis on continue. Ainsi aucun Blender orphelin ne
# s'accumule, et la memoire est rendue entre chaque vague.
# =============================================================================
set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MB="$RACINE/ModelBlender"
SCRIPT="$RACINE/tools/blender/render_preview.py"
PARALLELES="${1:-2}"

MEM_GO=$(free -g | awk '/^Mem:/{print $2}')

# Garde-fou memoire : plafonner le parallelisme.
PLAFOND=3
[ "$MEM_GO" -ge 24 ] && PLAFOND=6
if [ "$PARALLELES" -gt "$PLAFOND" ]; then
    echo "Machine de ${MEM_GO} Go de RAM : plafonnement de $PARALLELES a $PLAFOND instances."
    PARALLELES=$PLAFOND
fi

mkdir -p "$MB/apercus"

# Construire la liste des .blend sans apercu.
LISTE=$(mktemp)
for f in "$MB"/modeles_animes/*/*.blend "$MB"/modeles_statiques/*/*.blend; do
    [ -f "$f" ] || continue
    nom=$(basename "$f" .blend)
    [ -f "$MB/apercus/$nom.png" ] && continue
    echo "$f" >> "$LISTE"
done
TOTAL=$(wc -l < "$LISTE")
DEJA=$(ls "$MB/apercus" | wc -l)
echo "$TOTAL apercus a generer (par $PARALLELES, ${MEM_GO} Go de RAM)"

if [ "$TOTAL" -eq 0 ]; then
    echo "Tous les apercus existent deja ($DEJA)."
    rm -f "$LISTE"
    exit 0
fi

# Un rendu pour un fichier.
generer() {
    local f="$1"
    local nom sortie
    nom=$(basename "$f" .blend)
    sortie="$MB/apercus/$nom.png"
    [ -f "$sortie" ] && return 0
    blender --background "$f" --python "$SCRIPT" -- "$sortie" \
        >/dev/null 2>&1
}

# Interruption propre : tuer tous les Blender lances par ce script.
nettoyer() {
    echo
    echo "Interruption : arret des instances Blender..."
    pkill -9 -f "blender --background $MB" 2>/dev/null
    rm -f "$LISTE"
    exit 130
}
trap nettoyer INT TERM

export MB SCRIPT
export -f generer

VAGUES=0
while [ -s "$LISTE" ]; do
    # Prendre les N premiers fichiers de la liste.
    VAGUE=$(mktemp)
    head -n "$PARALLELES" "$LISTE" > "$VAGUE"
    tail -n "+$((PARALLELES + 1))" "$LISTE" > "${LISTE}.reste" 2>/dev/null \
        || : > "${LISTE}.reste"
    mv "${LISTE}.reste" "$LISTE"

    # Lancer la vague et retenir les PID.
    PIDS=()
    while IFS= read -r f; do
        generer "$f" &
        PIDS+=($!)
    done < "$VAGUE"
    rm -f "$VAGUE"

    # Attendre TOUTE la vague : aucun processus ne survit a son tour.
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null
    done

    VAGUES=$((VAGUES + 1))
    if [ $((VAGUES % 10)) -eq 0 ]; then
        DISPO=$(free -g | awk '/^Mem:/{print $7}')
        echo "  $(ls "$MB/apercus" | wc -l)/$((DEJA + TOTAL)) faits (RAM dispo : ${DISPO} Go)"
    fi
done

rm -f "$LISTE"
echo "Apercus generes : $(ls "$MB/apercus" | wc -l)"
