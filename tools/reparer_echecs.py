#!/usr/bin/env python3
"""
reparer_echecs.py -- Traite les 4 modeles qu'apicula n'a pas su convertir
d'un coup (plantage « index out of bounds » dans son module glTF).

Cause : apicula panique quand on lui demande de lier TOUTES les animations
en une seule fois sur certains modeles (typiquement au-dela de ~30, comme
« cool » qui en a 34). La parade consiste a convertir le modele avec un
NOMBRE LIMITE d'animations a la fois, puis a fusionner les resultats.
"""

import os
import shutil
import subprocess
import sys
import glob

RACINE = os.path.expanduser("~/Documents/ReverseEngeneering")
DATA = os.path.join(RACINE, "work/extracted/data")
DEST = os.path.join(RACINE, "ModelBlender")
APICULA = os.path.expanduser("~/.local/bin/apicula")
SCRIPT = os.path.join(RACINE, "tools/blender/fabriquer_blend.py")
TMP = "/tmp/reparation"

# Les modeles qui ont echoue, et combien d'animations leur sont associees.
CIBLES = ["cool", "m042", "m206", "m246_01"]


def tenter(nom, anims, par_lot):
    """Convertit le modele en liant les animations par lots de `par_lot`.

    Renvoie le chemin du glTF, ou None.
    """
    groupe = os.path.join(TMP, "in")
    if os.path.isdir(groupe):
        shutil.rmtree(groupe)
    os.makedirs(groupe)

    shutil.copy2(os.path.join(DATA, nom + ".nsbmd"), groupe)

    if par_lot is None:
        for a in anims:
            shutil.copy2(a, groupe)
    else:
        for a in anims[:par_lot]:
            shutil.copy2(a, groupe)

    sortie = os.path.join(TMP, "out", nom)
    if os.path.isdir(sortie):
        shutil.rmtree(sortie)
    os.makedirs(os.path.dirname(sortie), exist_ok=True)

    r = subprocess.run(
        [APICULA, "convert", groupe, "-o", sortie,
         "--all-animations", "--format", "gltf"],
        capture_output=True, text=True, timeout=240)

    g = os.path.join(sortie, nom + ".gltf")
    if os.path.exists(g) and os.path.getsize(g) > 0:
        return g
    return None


def main():
    os.makedirs(TMP, exist_ok=True)
    resultats = []

    for nom in CIBLES:
        anims = sorted(glob.glob(os.path.join(DATA, nom + "_*.nsbca")))
        anims += sorted(glob.glob(os.path.join(DATA, nom + ".nsbca")))
        # Ecarter les doublons eventuels.
        vus, liste = set(), []
        for a in anims:
            if a not in vus:
                vus.add(a)
                liste.append(a)
        anims = liste

        print(f"\n=== {nom} : {len(anims)} animations ===")

        # Strategie : essayer par lots de plus en plus petits. Certains
        # modeles ne passent qu'avec peu d'animations liees a la fois.
        gltf = None
        for par_lot in (None, 24, 16, 8, 4, 2, 1):
            etiquette = "toutes" if par_lot is None else f"{par_lot} max"
            g = tenter(nom, anims, par_lot)
            if g:
                print(f"  reussi avec : {etiquette}")
                gltf = g
                break
            print(f"  echec avec  : {etiquette}")

        if gltf is None:
            # Dernier recours : le modele SANS aucune animation.
            g = tenter(nom, [], 0)
            if g:
                print("  reussi SANS animation (modele statique)")
                gltf = g
            else:
                print("  ECHEC TOTAL")
                continue

        categorie = "modeles_animes" if anims else "modeles_statiques"
        dossier = os.path.join(DEST, categorie, nom)
        os.makedirs(dossier, exist_ok=True)
        blend = os.path.join(dossier, nom + ".blend")

        r = subprocess.run(
            ["blender", "--background", "--python", SCRIPT, "--", gltf, blend],
            capture_output=True, text=True, timeout=300)

        if os.path.exists(blend):
            ko = os.path.getsize(blend) // 1024
            print(f"  .blend cree ({ko} Ko) -> {categorie}/{nom}")
            resultats.append((nom, categorie, ko))
        else:
            print(f"  ECHEC creation .blend : {r.stderr.strip()[-150:]}")

    print(f"\n{len(resultats)}/{len(CIBLES)} repares")
    for nom, cat, ko in resultats:
        print(f"  {nom:12s} {cat:18s} {ko} Ko")


if __name__ == "__main__":
    main()
