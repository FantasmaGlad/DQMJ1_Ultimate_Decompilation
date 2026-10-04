#!/usr/bin/env python3
"""Anime les variantes de recoloration/forme (m160b...) qui n'ont pas de .nsbca propre.

Le jeu applique aux variantes les animations de squelette du modele de base (m160_*.nsbca pour m160b) : les
articulations sont adressees par indice. On reconvertit donc la variante avec les .nsbca de sa base (apicula) et on
garde tout resultat qui porte des animations (liaison par nom, comme le moteur du jeu).
Sortie : assets/models/web-gltf/animated/<variante>/ (gltf + bin + png).
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEST = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "models" / "web-gltf"
DATA = ROOT / "work/extracted/data"
APICULA = os.path.expanduser("~/.local/bin/apicula")
TMP = Path("/tmp/animer_variantes")

def joints(g):
    """Squelette = arbre des articulations (indice du parent de chacune) : les noms peuvent differer d'un modele a
    l'autre alors que le jeu adresse les articulations par indice."""
    if not g.get("skins"): return None
    js = g["skins"][0]["joints"]
    parent = {c: i for i, n in enumerate(g["nodes"]) for c in n.get("children", [])}
    return [js.index(parent[j]) if parent.get(j) in js else -1 for j in js]

done, skipped, differ = [], [], []
for d in sorted((BEST / "static").iterdir()):
    vid = d.name
    m = re.fullmatch(r"(m\d{3})([a-z])", vid)
    if not m or (BEST / "animated" / vid).exists(): continue
    base = m.group(1)
    anims = sorted(DATA.glob(f"{base}_*.nsbca"))
    if not (BEST / "animated" / base).exists() or not anims or not (DATA / f"{vid}.nsbmd").exists(): continue
    shutil.rmtree(TMP, ignore_errors=True); (TMP / "entree").mkdir(parents=True)
    shutil.copy2(DATA / f"{vid}.nsbmd", TMP / "entree")
    for a in anims: shutil.copy2(a, TMP / "entree")
    r = subprocess.run([APICULA, "convert", str(TMP / "entree"), "-o", str(TMP / "out"), "--all-animations", "--format", "gltf"],
                       capture_output=True, text=True, timeout=180)
    out = TMP / "out" / f"{vid}.gltf"
    if r.returncode != 0 or not out.exists():
        skipped.append((vid, "apicula")); continue
    g = json.loads(out.read_text()); b = json.loads((BEST / "animated" / base / f"{base}.gltf").read_text())
    # Le jeu lie les animations par NOM d'articulation (ViewChrTbl -> MotionTbl donne a la variante les motions de sa base,
    # meme quand le squelette differe) : on garde donc tout resultat d'apicula qui porte des animations.
    if joints(g) is None or not g.get("animations"):
        skipped.append((vid, "aucune animation")); continue
    if joints(g) != joints(b): differ.append(vid)
    shutil.copytree(TMP / "out", BEST / "animated" / vid)
    done.append(vid)
print("animees", len(done), done)
print("laissees statiques", skipped)
print("squelette different de la base (animation liee par nom, partielle possible)", differ)
