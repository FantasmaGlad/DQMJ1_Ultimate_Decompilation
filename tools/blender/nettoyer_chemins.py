"""
nettoyer_chemins.py -- Supprime les references exterieures mortes des
.blend de la bibliotheque ModelBlender.

Les .blend ont ete fabriques a partir de glTF places dans un dossier
temporaire (/tmp/modelblender_travail), supprime depuis. Chaque texture
est bien EMBARQUEE (« packed »), mais le .blend garde le chemin d'origine
en memoire, ce qui provoque un avertissement « fichier introuvable » a
chaque ouverture.

Ce script ouvre chaque .blend, vide ce chemin, et reenregistre. Apres
passage, les fichiers sont totalement autonomes.

Appel :
    blender --background <fichier.blend> --python nettoyer_chemins.py
"""

import bpy
import sys

corrigees = 0
for img in bpy.data.images:
    # Ne jamais toucher aux images internes de Blender : elles n'ont pas
    # de fichier source et n'ont donc rien a nettoyer.
    if img.name in ('Render Result', 'Viewer Node'):
        continue
    if img.packed_file is None:
        continue
    if img.filepath or img.filepath_raw:
        img.filepath = ''
        img.filepath_raw = ''
        corrigees += 1

if corrigees:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, compress=True)

print(f"NETTOYE {corrigees} chemin(s) : {bpy.data.filepath}")
