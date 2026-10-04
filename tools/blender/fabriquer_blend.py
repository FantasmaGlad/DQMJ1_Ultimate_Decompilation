"""
fabriquer_blend.py -- Fabrique un .blend AUTONOME et pret a l'emploi a
partir d'un glTF issu d'apicula.

Appel :
    blender --background --python fabriquer_blend.py -- <entree.gltf> <sortie.blend>

=======================================================================
CE QUI EST CORRIGE AUTOMATIQUEMENT
=======================================================================
1. TEXTURES EMBARQUEES
   Un glTF externe reference des .png a cote. On les recharge puis on les
   « pack » dans le .blend : le fichier devient autonome.

2. LES « TOURS » QUI MASQUENT LE MODELE
   Blender dessine chaque os comme une forme pleine (OCTAHEDRAL), et
   l'importateur glTF active show_in_front : les os sont donc dessines
   PAR-DESSUS le maillage. Avec des os de 8 unites dans un modele de 16,
   cela masque tout. On passe en STICK et on desactive show_in_front.

3. LES ANIMATIONS PERDUES
   Blender ne garde qu'une action active a la fois : les autres sont
   perdues a l'enregistrement. On les range TOUTES dans des pistes NLA,
   posees bout a bout (deux bandes ne peuvent pas occuper les memes
   frames sur une meme piste).

4. CONFORT
   Camera et eclairage adaptes a la taille du modele, viewport en mode
   texture, overlays desactives.
"""

import bpy
import mathutils
import os
import sys

argv = sys.argv[sys.argv.index('--') + 1:]
entree, sortie = argv[0], argv[1]

dossier_gltf = os.path.dirname(os.path.abspath(entree))


def main():
    # -----------------------------------------------------------------
    # 1. Scene vide
    # -----------------------------------------------------------------
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # -----------------------------------------------------------------
    # 2. Import
    # -----------------------------------------------------------------
    bpy.ops.import_scene.gltf(filepath=entree)

    for o in list(bpy.data.objects):
        if o.name in ('Cube', 'Icosphere', 'Camera', 'Light') \
                or o.name.startswith('Icosphere'):
            try:
                bpy.data.objects.remove(o, do_unlink=True)
            except RuntimeError:
                pass

    # -----------------------------------------------------------------
    # 3. Textures : recharger puis EMBARQUER dans le .blend
    # -----------------------------------------------------------------
    # Ne jamais toucher aux images internes de Blender : « Render Result »
    # et « Viewer Node » n'ont pas de fichier source, et tenter de les
    # packer leve une exception qui interrompt tout le script.
    for img in bpy.data.images:
        if img.name in ('Render Result', 'Viewer Node'):
            continue
        if img.source not in ('FILE', 'SEQUENCE'):
            continue

        if img.size[0] == 0 or not img.has_data:
            nom = os.path.basename(img.filepath) or (img.name + '.png')
            candidat = os.path.join(dossier_gltf, nom)
            if os.path.exists(candidat):
                img.filepath = candidat
                img.reload()

        if img.size[0] > 0:
            # Rendre l'image autonome AVANT de packer, en effacant le
            # chemin d'origine. Sans cela le .blend garde une reference
            # vers le dossier temporaire de conversion (supprime depuis),
            # ce qui declenche un avertissement « fichier introuvable » a
            # chaque ouverture, alors meme que les donnees sont bien
            # embarquees.
            img.pack()          # <- embarque l'image dans le .blend
            img.filepath = ''   # <- plus aucune reference externe
            img.filepath_raw = ''

    # -----------------------------------------------------------------
    # 4. Armatures : os discrets + toutes les animations en NLA
    # -----------------------------------------------------------------
    for arm in [o for o in bpy.data.objects if o.type == 'ARMATURE']:
        arm.data.display_type = 'STICK'     # trait fin, pas de forme pleine
        arm.show_in_front = False           # ne plus dessiner par-dessus
        arm.data.show_names = False

        if not bpy.data.actions:
            continue

        if arm.animation_data is None:
            arm.animation_data_create()

        # Premiere animation active par defaut.
        arm.animation_data.action = bpy.data.actions[0]

        # Toutes les autres rangees dans une piste NLA, bout a bout.
        piste = arm.animation_data.nla_tracks.new()
        piste.name = 'Animations'
        curseur = 0
        for a in bpy.data.actions:
            duree = max(1, int(a.frame_range[1] - a.frame_range[0]))
            try:
                bande = piste.strips.new(a.name, curseur, a)
                bande.frame_end = curseur + duree
            except RuntimeError:
                pass
            curseur += duree + 1

    # -----------------------------------------------------------------
    # 5. Cadrage : camera et lumiere adaptees a la taille du modele
    # -----------------------------------------------------------------
    maillages = [o for o in bpy.data.objects if o.type == 'MESH']
    if maillages:
        points = [o.matrix_world @ mathutils.Vector(c)
                  for o in maillages for c in o.bound_box]
        centre = mathutils.Vector((
            sum(v.x for v in points) / len(points),
            sum(v.y for v in points) / len(points),
            sum(v.z for v in points) / len(points)))
        rayon = max((v - centre).length for v in points) or 1.0

        cam_data = bpy.data.cameras.new('Camera')
        cam = bpy.data.objects.new('Camera', cam_data)
        bpy.context.scene.collection.objects.link(cam)
        cam.location = centre + mathutils.Vector(
            (rayon * 1.0, -rayon * 1.4, rayon * 0.5))
        cam.rotation_euler = (centre - cam.location).to_track_quat(
            '-Z', 'Y').to_euler()
        bpy.context.scene.camera = cam

        for rotation, energie in (((0.9, 0.2, 0.7), 3.0),
                                  ((-0.7, -0.3, -1.1), 1.5)):
            ld = bpy.data.lights.new('Lumiere', 'SUN')
            lo = bpy.data.objects.new('Lumiere', ld)
            bpy.context.scene.collection.objects.link(lo)
            lo.rotation_euler = rotation
            ld.energy = energie

        # Plage de frames sur la premiere animation.
        if bpy.data.actions:
            debut, fin = bpy.data.actions[0].frame_range
            bpy.context.scene.frame_start = int(debut)
            bpy.context.scene.frame_end = max(int(fin) + 1, int(debut) + 1)

    # -----------------------------------------------------------------
    # 6. Viewport : textures visibles, overlays discrets
    # -----------------------------------------------------------------
    for ecran in bpy.data.screens:
        for zone in ecran.areas:
            if zone.type == 'VIEW_3D':
                for espace in zone.spaces:
                    if hasattr(espace, 'shading'):
                        espace.shading.light = 'STUDIO'
                        espace.shading.color_type = 'TEXTURE'
                    if hasattr(espace, 'overlay'):
                        espace.overlay.show_overlays = False

    # -----------------------------------------------------------------
    # 7. Enregistrer (les textures packees partent avec le fichier)
    # -----------------------------------------------------------------
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=sortie, compress=True)

    verts = sum(len(o.data.vertices) for o in maillages)
    print(f"BLEND OK {os.path.basename(sortie)} "
          f"{verts} sommets {len(bpy.data.actions)} animations")


main()
