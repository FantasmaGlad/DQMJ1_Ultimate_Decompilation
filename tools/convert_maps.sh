#!/usr/bin/env bash
# Convertit chaque carte extraite (work/maps/<carte>/) en GLB + PNG avec apicula.
# Sortie brute : work/maps_raw/<carte>/ ; puis optimisation (tools/optimiser) vers
# ../DragonQuestMonsterJoker1Bestiaire/assets/models/web-gltf/maps/<carte>/ (world.glb + ciels + map.json).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/work/maps_raw"
mkdir -p "$OUT"
ok=0; ko=0
for d in "$ROOT"/work/maps/*/; do
  id="$(basename "$d")"
  rm -rf "$OUT/$id"
  if apicula convert "$d" -o "$OUT/$id" -f glb >"$ROOT/work/maps/$id.log" 2>&1; then ok=$((ok+1)); else ko=$((ko+1)); echo "echec $id"; fi
done
echo "cartes converties: $ok, echecs: $ko"

(cd "$ROOT/tools/optimiser" && [ -d node_modules ] || npm install --no-audit --no-fund) && (cd "$ROOT/tools/optimiser" && node optimize_maps.mjs 2>&1 | grep -v -e "Missing optional" -e "prune:" -e "quantize:")
