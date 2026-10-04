#!/usr/bin/env python3
"""
renommer_modeles.py -- Renomme les modeles 3D et les apercus PNG
avec les noms officiels du Fandom Dragon Quest Monsters: Joker.
"""

import json
import os
import shutil
import sys

RACINE = os.path.expanduser("~/Documents/ReverseEngeneering")
MB = os.path.join(RACINE, "ModelBlender")
APERCUS = os.path.join(MB, "apercus")
ANIMES = os.path.join(MB, "modeles_animes")
STATIQUES = os.path.join(MB, "modeles_statiques")
OUT_MODELS = os.path.join(RACINE, "out/models")
MAPPING_FILE = os.path.join(RACINE, "tools/mapping_monstres.json")

def charger_mapping():
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def renommer(dry_run=False):
    mapping = charger_mapping()
    renommes_png = 0
    renommes_blend = 0
    renommes_out = 0

    print("=== Renommage des aperçus PNG ===")
    for model_id, info in sorted(mapping.items()):
        nom_fr = info["nom_fr"]
        ancien_png = os.path.join(APERCUS, f"{model_id}.png")
        nouveau_nom = f"{model_id} - {nom_fr}.png"
        nouveau_png = os.path.join(APERCUS, nouveau_nom)

        if os.path.isfile(ancien_png) and not os.path.islink(ancien_png):
            if dry_run:
                print(f"[DRY-RUN] {model_id}.png -> {nouveau_nom}")
            else:
                os.rename(ancien_png, nouveau_png)
                # Créer un lien symbolique pour la rétrocompatibilité
                os.symlink(nouveau_nom, ancien_png)
            renommes_png += 1
        elif os.path.exists(nouveau_png):
            renommes_png += 1

    print(f"Aperçus traités : {renommes_png}")

    print("\n=== Renommage des modèles Blender (dossiers et .blend) ===")
    for cat_dir in (ANIMES, STATIQUES):
        if not os.path.isdir(cat_dir):
            continue
        for model_id, info in sorted(mapping.items()):
            nom_fr = info["nom_fr"]
            ancien_dossier = os.path.join(cat_dir, model_id)
            nouveau_nom_dossier = f"{model_id} - {nom_fr}"
            nouveau_dossier = os.path.join(cat_dir, nouveau_nom_dossier)

            if os.path.isdir(ancien_dossier) and not os.path.islink(ancien_dossier):
                ancien_blend = os.path.join(ancien_dossier, f"{model_id}.blend")
                nouveau_blend = os.path.join(ancien_dossier, f"{model_id} - {nom_fr}.blend")
                if dry_run:
                    print(f"[DRY-RUN] Dossier: {model_id} -> {nouveau_nom_dossier}")
                    if os.path.exists(ancien_blend):
                        print(f"          Fichier: {model_id}.blend -> {model_id} - {nom_fr}.blend")
                else:
                    if os.path.exists(ancien_blend):
                        os.rename(ancien_blend, nouveau_blend)
                        # Symlink pour l'ancien .blend
                        os.symlink(f"{model_id} - {nom_fr}.blend", ancien_blend)
                    os.rename(ancien_dossier, nouveau_dossier)
                    # Symlink pour l'ancien dossier
                    os.symlink(nouveau_nom_dossier, ancien_dossier)
                renommes_blend += 1
            elif os.path.isdir(nouveau_dossier):
                renommes_blend += 1

    print(f"Modèles Blender traités : {renommes_blend}")

    print("\n=== Renommage out/models/ (dossiers glTF/bin/textures) ===")
    if os.path.isdir(OUT_MODELS):
        for model_id, info in sorted(mapping.items()):
            nom_fr = info["nom_fr"]
            ancien_out = os.path.join(OUT_MODELS, model_id)
            nouveau_out_nom = f"{model_id} - {nom_fr}"
            nouveau_out = os.path.join(OUT_MODELS, nouveau_out_nom)
            if os.path.isdir(ancien_out) and not os.path.islink(ancien_out):
                if dry_run:
                    print(f"[DRY-RUN] out/models: {model_id} -> {nouveau_out_nom}")
                else:
                    os.rename(ancien_out, nouveau_out)
                    os.symlink(nouveau_out_nom, ancien_out)
                renommes_out += 1
            elif os.path.isdir(nouveau_out):
                renommes_out += 1
    print(f"Modèles out/models traités : {renommes_out}")

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    renommer(dry_run=dry)
