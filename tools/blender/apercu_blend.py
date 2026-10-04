"""
apercu_blend.py -- Genere une image PNG d'apercu pour un .blend.

Appel :
    blender --background <fichier.blend> --python apercu_blend.py -- <sortie.png>

Rend le modele de trois quarts, avec ses textures, sans les os.
"""
import bpy
import mathutils
import sys

argv = sys.argv[sys.argv.index('--') + 1:]
sortie = argv[0]

# Retirer les os de l'affichage : ils ne doivent pas apparaitre sur l'apercu.
for arm in [o for o in bpy.data.objects if o.type == 'ARMATURE']:
    arm.hide_render = True

maillages = [o for o in bpy.data.objects if o.type == 'MESH']
if not maillages:
    raise SystemExit("aucun maillage")

# Cadrer la camera sur le modele.
#
# Attention : o.bound_box donne la boite englobante dans l'espace LOCAL de
# l'objet. Pour un objet deforme par un modificateur (armature) ou tourne,
# elle ne correspond pas a ce qui est reellement dessine. On prend donc le
# maximum entre la boite locale et les dimensions reelles de l'objet.
points = [o.matrix_world @ mathutils.Vector(c)
          for o in maillages for c in o.bound_box]
centre = mathutils.Vector((
    sum(v.x for v in points) / len(points),
    sum(v.y for v in points) / len(points),
    sum(v.z for v in points) / len(points)))
rayon = max((v - centre).length for v in points) or 1.0

# Securite : si l'objet est nettement plus grand que sa boite locale
# (cas des maillages deformes), elargir le cadrage.
for o in maillages:
    r_obj = max(o.dimensions) / 2.0
    if r_obj > rayon:
        rayon = r_obj

cam = bpy.data.objects.get('Camera')
if cam is None:
    cam_data = bpy.data.cameras.new('Camera')
    cam = bpy.data.objects.new('Camera', cam_data)
    bpy.context.scene.collection.objects.link(cam)

# Choisir l'angle de vue selon la FORME de l'objet.
#
# Beaucoup d'objets de ce jeu sont des PANNEAUX presque plats : les
# panneaux indicateurs font 52 x 51 x 1.2 unites, et l000 n'est qu'un plan
# a 4 sommets de 24 x 0 x 12 portant un logo. Vus de trois quarts, ces
# objets sont vus PAR LA TRANCHE et paraissent vides.
#
# Le seuil doit rester STRICT : o_gagoil mesure 28.8 x 93.5 x 11.0, soit
# un rapport de 0.118. Avec un seuil de 0.12 il etait classe « plat » et
# photographie de dessus, alors que c'est un objet long et vertical.
# Un vrai panneau a un rapport inferieur a 0.05.
dims = [o.dimensions for o in maillages]
epaisseur_min = min(min(d) for d in dims) if dims else 0
etendue_max = max(max(d) for d in dims) if dims else 1

plat = (etendue_max > 0 and epaisseur_min / etendue_max < 0.05)

if plat:
    # Vue de face : on regarde selon l'axe le plus FIN.
    # On determine quel axe est le plus petit en moyenne.
    moy = [sum(d[i] for d in dims) / len(dims) for i in range(3)]
    axe_fin = moy.index(min(moy))
    if axe_fin == 0:
        direction = mathutils.Vector((1.0, 0.0, 0.0))
    elif axe_fin == 1:
        direction = mathutils.Vector((0.0, -1.0, 0.0))
    else:
        direction = mathutils.Vector((0.0, 0.0, 1.0))
    # Legerement decale pour garder un peu de relief.
    direction = (direction + mathutils.Vector((0.08, -0.08, 0.05))).normalized()
    cam.location = centre + direction * (rayon * 1.9)
else:
    # Vue de trois quarts classique.
    cam.location = centre + mathutils.Vector(
        (rayon * 0.9, -rayon * 1.5, rayon * 0.45))

cam.rotation_euler = (centre - cam.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Distance de la camera.
#
# On eloigne la camera d'un multiple du rayon, ce qui cadre correctement
# la grande majorite des modeles (387 sur 411 valides au premier essai).
#
# NE PAS remplacer par un calcul de projection : une version projetant
# chaque sommet sur l'axe de visee a donne de moins bons resultats sur
# TOUS les modeles (m148 est passe de 13 % a 4 % d'occupation), car la
# composante perpendiculaire sous-estime l'etendue reelle quand l'objet
# est vu de biais.
#
# La focale est en revanche ajustee : une focale courte (grand angle)
# fait entrer l'objet entier meme tres allonge.
cam.data.lens = 35.0        # grand angle : cadre large, objet entier

# Deux lumieres si le .blend n'en a pas.
if not any(o.type == 'LIGHT' for o in bpy.data.objects):
    for rotation, energie in (((0.9, 0.2, 0.7), 3.0), ((-0.7, -0.3, -1.1), 1.5)):
        ld = bpy.data.lights.new('Lumiere', 'SUN')
        lo = bpy.data.objects.new('Lumiere', ld)
        bpy.context.scene.collection.objects.link(lo)
        lo.rotation_euler = rotation
        ld.energy = energie

# Fond gris moyen : les modeles sombres restent lisibles.
monde = bpy.data.worlds.new('Apercu')
bpy.context.scene.world = monde
monde.use_nodes = True
monde.node_tree.nodes['Background'].inputs[0].default_value = (0.22, 0.23, 0.27, 1)

sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 480
sc.render.resolution_y = 480
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = sortie

# =========================================================================
# Rendre VISIBLES les objets « invisibles a la camera ».
# =========================================================================
# Certains objets du jeu portent un materiau monte ainsi :
#
#     Light Path.Is Camera Ray -> Mix Shader.Factor
#         si rayon camera : Transparent BSDF   (donc INVISIBLE au rendu)
#         sinon           : Emission
#
# C'est le montage classique d'un objet que le jeu ne veut PAS montrer
# directement : source de lumiere, volume de collision, declencheur. Leur
# texture a d'ailleurs un canal alpha entierement a 0.
# Exemples : o_guideB3 (les « guide » sont des reperes lumineux),
# o_daiLight (une source de lumiere piegee).
#
# Resultat : sur un rendu, ces objets sortent vides. C'est un comportement
# CORRECT, pas un defaut de conversion. Pour l'apercu on les rend tout de
# meme visibles, sinon on croirait que la conversion a echoue.
invisibles = []
for mat in bpy.data.materials:
    if not mat.use_nodes or mat.node_tree is None:
        continue
    noeuds = mat.node_tree.nodes
    if not any(n.type == 'LIGHT_PATH' for n in noeuds):
        continue
    image = next((n.image for n in noeuds
                  if n.type == 'TEX_IMAGE' and n.image), None)
    if image is None:
        continue

    nt = mat.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = image
    tex.location = (-400, 0)
    emi = nt.nodes.new('ShaderNodeEmission')
    emi.location = (-100, 0)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    out.location = (200, 0)
    # Replier la couleur par l'alpha : sans cela les zones transparentes
    # restent transparentes et l'objet parait encore vide.
    melange = nt.nodes.new('ShaderNodeMix')
    melange.data_type = 'RGBA'
    melange.location = (-200, -200)
    melange.inputs[0].default_value = 1.0
    melange.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)   # couleur A
    nt.links.new(melange.inputs[7], tex.outputs['Color'])     # couleur B
    nt.links.new(melange.inputs[0], tex.outputs['Alpha'])     # facteur
    nt.links.new(emi.inputs['Color'], melange.outputs[2])
    nt.links.new(out.inputs['Surface'], emi.outputs['Emission'])
    invisibles.append(mat.name)

if invisibles:
    print(f"materiaux invisibles a la camera, rendus visibles : "
          f"{len(invisibles)} ({', '.join(invisibles[:4])})")

bpy.ops.render.render(write_still=True)

print("APERCU OK", sortie)
