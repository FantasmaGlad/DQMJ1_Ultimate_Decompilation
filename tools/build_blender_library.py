#!/usr/bin/env python3
"""
build_blender_library.py -- Construit la bibliotheque « ModelBlender ».

=======================================================================
CE QUE FAIT CE SCRIPT
=======================================================================
Il prepare TOUS les modeles 3D de la ROM dans un dossier pret a l'emploi :

    ModelBlender/
      modeles_animes/m148/m148.blend     <- ouvrir directement
      modeles_statiques/bf001a/...blend
      apercus/m148.png                   <- voir sans ouvrir Blender
      CATALOGUE.md                       <- index complet
      ouvrir.sh                          <- lanceur

Chaque fichier .blend contient deja :
  - le maillage avec ses TEXTURES EMBARQUEES (rien a retrouver)
  - l'armature avec TOUTES les animations dans des pistes NLA
  - les os en affichage discret (plus de « tours » qui masquent le modele)
  - viewport en mode texture, overlays desactives
  - une camera et un eclairage prets a rendre

=======================================================================
POURQUOI DES .blend ET NON DES .gltf
=======================================================================
Un .gltf est un PLAN : il reference des .bin et des .png externes. Si on
deplace le .gltf seul, Blender n'affiche qu'un maillage gris (l'image
devient vide, taille 0x0).

Un .blend, lui, est AUTONOME : tout est dedans, textures comprises
(« packed »). Un seul fichier a copier, ouvrir, archiver.

=======================================================================
ARCHITECTURE
=======================================================================
Deux etapes, volontairement separees :

  1. apicula convertit chaque .nsbmd (+ ses .nsbca) en glTF.
     C'est la seule partie qui comprend le format Nintendo.

  2. Blender ouvre ce glTF, corrige ce qui doit l'etre, et enregistre
     un .blend autonome.
     C'est la seule partie qui comprend Blender.
"""

import json
import os
import shutil
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
DEST = os.path.join(RACINE, "ModelBlender")
APICULA = os.path.expanduser("~/.local/bin/apicula")

# Le script Blender qui fabrique un .blend propre a partir d'un glTF.
SCRIPT_BLEND = os.path.join(RACINE, "tools/blender/build_blend.py")


def lister_modeles():
    """Renvoie [(nom, chemin_nsbmd, [chemins_nsbca])] pour les 411 modeles."""
    modeles = []
    for f in sorted(os.listdir(DATA)):
        if not f.lower().endswith(".nsbmd"):
            continue
        nom = f[:-len(".nsbmd")]
        nsbmd = os.path.join(DATA, f)

        # Animations associees : m148.nsbca et m148_00.nsbca, etc.
        anims = []
        for a in sorted(os.listdir(DATA)):
            if not a.lower().endswith(".nsbca"):
                continue
            base = a[:-len(".nsbca")]
            if base == nom or base.startswith(nom + "_"):
                anims.append(os.path.join(DATA, a))

        modeles.append((nom, nsbmd, anims))
    return modeles


def convertir(nom, nsbmd, anims, temporaire):
    """Convertit un modele (et ses animations) en glTF via apicula."""
    groupe = os.path.join(temporaire, "entree")
    if os.path.isdir(groupe):
        shutil.rmtree(groupe)
    os.makedirs(groupe)

    shutil.copy2(nsbmd, groupe)
    for a in anims:
        shutil.copy2(a, groupe)

    sortie = os.path.join(temporaire, "gltf", nom)
    if os.path.isdir(sortie):
        shutil.rmtree(sortie)

    # apicula exige que le DOSSIER PARENT de la sortie existe : sinon il
    # echoue avec « No such file or directory (os error 2) ». Il refuse
    # aussi de creer lui-meme le dossier final s'il existe deja.
    os.makedirs(os.path.dirname(sortie), exist_ok=True)

    r = subprocess.run(
        [APICULA, "convert", groupe, "-o", sortie,
         "--all-animations", "--format", "gltf"],
        capture_output=True, text=True, timeout=180)

    if r.returncode != 0 or not os.path.exists(os.path.join(sortie, nom + ".gltf")):
        return None, (r.stderr.strip() or r.stdout.strip())[:200]

    return os.path.join(sortie, nom + ".gltf"), None


def main():
    seulement = sys.argv[1] if len(sys.argv) > 1 else None

    os.makedirs(DEST, exist_ok=True)
    os.makedirs(os.path.join(DEST, "apercus"), exist_ok=True)
    temporaire = "/tmp/modelblender_travail"
    os.makedirs(temporaire, exist_ok=True)

    modeles = lister_modeles()
    print(f"{len(modeles)} modeles a traiter")

    catalogue = []
    echecs = []

    for i, (nom, nsbmd, anims) in enumerate(modeles, 1):
        # Classement : animé s'il a des .nsbca, statique sinon.
        categorie = "modeles_animes" if anims else "modeles_statiques"
        dossier = os.path.join(DEST, categorie, nom)

        if seulement and seulement not in nom:
            continue

        deja = os.path.exists(os.path.join(dossier, nom + ".blend"))
        if deja:
            catalogue.append({"nom": nom, "categorie": categorie,
                              "animations": len(anims), "statut": "deja fait"})
            continue

        gltf, err = convertir(nom, nsbmd, anims, temporaire)
        if gltf is None:
            echecs.append((nom, err))
            print(f"  [{i}/{len(modeles)}] {nom:16s} ECHEC conversion apicula")
            continue

        # Fabriquer le .blend autonome.
        os.makedirs(dossier, exist_ok=True)
        blend = os.path.join(dossier, nom + ".blend")
        r = subprocess.run(
            ["blender", "--background", "--python", SCRIPT_BLEND, "--",
             gltf, blend],
            capture_output=True, text=True, timeout=300)

        if not os.path.exists(blend):
            echecs.append((nom, r.stderr.strip()[-200:]))
            print(f"  [{i}/{len(modeles)}] {nom:16s} ECHEC creation .blend")
            continue

        taille = os.path.getsize(blend) // 1024
        print(f"  [{i}/{len(modeles)}] {nom:16s} OK  {categorie:18s} "
              f"{len(anims):3d} anim  {taille:5d} Ko")

        catalogue.append({"nom": nom, "categorie": categorie,
                          "animations": len(anims), "taille_ko": taille,
                          "statut": "ok"})

    # Sauvegarder le catalogue.
    with open(os.path.join(DEST, "catalogue.json"), "w") as f:
        json.dump({"modeles": catalogue, "echecs": echecs}, f, indent=1)

    print(f"\n{catalogue} -> {len(catalogue)} modeles")
    print(f"{len(echecs)} echecs")


if __name__ == "__main__":
    main()
