#!/usr/bin/env python3
"""
create_catalog.py -- Genere le CATALOGUE.md de la bibliotheque
ModelBlender, avec l'inventaire complet des modeles et leurs noms officiels.
"""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MB = os.path.join(RACINE, "ModelBlender")
MAPPING_FILE = os.path.join(RACINE, "tools/mapping_monstres.json")

FAMILLES = [
    ("m",    "Monstres",        "Numérotation m000 → m248, identifiés par nom officiel Fandom"),
    ("o",    "Objets et décors", "Éléments interactifs : interrupteurs, miroirs, portes, panneaux"),
    ("bf",   "Décors de combat", "Battle Field : arènes et plateaux de combat"),
    ("bd",   "Bâtiments",        "Structures et architectures"),
    ("n",    "Personnages",      "PNJ et protagonistes"),
    ("bh",   "Divers (bh)",      "Éléments non classés"),
    ("be",   "Divers (be)",      "Éléments non classés"),
    ("WF",   "Divers (WF)",      "Éléments non classés"),
    ("Z_",   "Divers (Z_)",      "Éléments non classés"),
]

def charger_mapping():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def famille(nom):
    # Extraire le préfixe de base
    code_base = nom.split(" - ")[0]
    for prefixe, libelle, _ in FAMILLES:
        if code_base.startswith(prefixe):
            return prefixe, libelle
    return "?", "Non classés"

def main():
    with open(os.path.join(MB, "catalogue.json")) as f:
        data = json.load(f)

    mapping = charger_mapping()
    modeles_bruts = data["modeles"]
    
    # Normaliser les modèles
    connus = set()
    modeles = []
    
    for cat in ("modeles_animes", "modeles_statiques"):
        d = os.path.join(MB, cat)
        if not os.path.isdir(d):
            continue
        for nom in sorted(os.listdir(d)):
            if os.path.islink(os.path.join(d, nom)):
                continue  # ignorer les symlinks de compatibilité
            
            code_base = nom.split(" - ")[0]
            if code_base in connus:
                continue
            connus.add(code_base)
            
            # Trouver le .blend
            dossier_path = os.path.join(d, nom)
            blend_path = os.path.join(dossier_path, nom + ".blend")
            if not os.path.exists(blend_path):
                # Chercher un .blend quelconque dans le dossier
                for cand in os.listdir(dossier_path):
                    if cand.endswith(".blend") and not os.path.islink(os.path.join(dossier_path, cand)):
                        blend_path = os.path.join(dossier_path, cand)
                        break
            
            # Nombre d'animations d'origine
            orig_info = next((x for x in modeles_bruts if x["nom"] == code_base), None)
            anims = orig_info.get("animations", 0) if orig_info else 0
            taille = os.path.getsize(blend_path) // 1024 if os.path.exists(blend_path) else 0

            info_map = mapping.get(code_base, {})
            modeles.append({
                "code": code_base,
                "dossier": nom,
                "nom_fr": info_map.get("nom_fr", ""),
                "nom_en": info_map.get("nom_en", ""),
                "categorie": cat,
                "animations": anims,
                "taille_ko": taille,
                "statut": "ok"
            })

    # Regrouper par famille
    groupes = {}
    for m in modeles:
        code, libelle = famille(m["code"])
        groupes.setdefault((code, libelle), []).append(m)

    total_anim = sum(1 for m in modeles if m["categorie"] == "modeles_animes")
    total_stat = sum(1 for m in modeles if m["categorie"] == "modeles_statiques")
    poids = sum(m.get("taille_ko", 0) for m in modeles) // 1024

    lignes = []
    A = lignes.append

    A("# ModelBlender — bibliothèque de modèles 3D")
    A("")
    A("Tous les modèles 3D de *Dragon Quest Monsters: Joker* convertis en "
      "fichiers Blender **prêts à l'emploi**, avec leurs **noms officiels**.")
    A("")
    A("Chaque fichier `.blend` est **autonome** : les textures sont "
      "embarquées dedans, les animations sont rangées dans des pistes NLA, "
      "et les os sont en affichage discret. Il n'y a rien à configurer.")
    A("")
    A("---")
    A("")
    A("## Contenu")
    A("")
    A("| Élément | Nombre |")
    A("|---|---|")
    A(f"| Modèles **animés** | **{total_anim}** |")
    A(f"| Modèles **statiques** | **{total_stat}** |")
    A(f"| **Total** | **{len(modeles)}** |")
    # Compter les vrais aperçus (sans les symlinks)
    apercus_reels = sum(1 for f in os.listdir(os.path.join(MB, 'apercus')) if not os.path.islink(os.path.join(MB, 'apercus', f)) and f.endswith('.png'))
    A(f"| Aperçus PNG | {apercus_reels} |")
    A(f"| Poids total | ~{poids} Mo |")
    A("")
    A("## Organisation")
    A("")
    A("```")
    A("ModelBlender/")
    A("├── modeles_animes/        modèles avec squelette et animations")
    A("│   └── m148 - Mort-Vivant/m148 - Mort-Vivant.blend")
    A("├── modeles_statiques/     modèles sans animation")
    A("│   └── bd001/bd001.blend")
    A("├── apercus/               vignettes PNG avec noms officiels")
    A("│   └── m148 - Mort-Vivant.png")
    A("├── CATALOGUE.md           ce document")
    A("└── ouvrir.sh              lanceur (ouvre par nom ou par code)")
    A("```")
    A("")
    A("## Comment ouvrir un modèle")
    A("")
    A("**Depuis un terminal :**")
    A("")
    A("```bash")
    A("./ouvrir.sh Gluant          # ouvre par nom français")
    A("./ouvrir.sh Slime           # ouvre par nom Fandom anglais")
    A("./ouvrir.sh m000            # ouvre par code ROM d'origine")
    A("./ouvrir.sh --liste         # liste tout ce qui est disponible")
    A("./ouvrir.sh --liste Gluant  # filtre les modèles contenant 'Gluant'")
    A("./ouvrir.sh --apercu Joker  # montre la vignette du Joker")
    A("```")
    A("")
    A("**À la main :** ouvrir le `.blend` dans Blender (double-clic).")
    A("")
    A("---")
    A("")
    A("## Les familles de modèles")
    A("")
    A("| Préfixe | Famille | Nombre | Signification |")
    A("|---|---|---|---|")
    for (code, libelle), liste in sorted(groupes.items(), key=lambda kv: -len(kv[1])):
        sens = next((s for p, l, s in FAMILLES if l == libelle), "—")
        A(f"| `{code}` | **{libelle}** | {len(liste)} | {sens} |")
    A("")
    A("---")
    A("")

    # Détail par famille
    A("## Inventaire détaillé")
    A("")
    for (code, libelle), liste in sorted(groupes.items(), key=lambda kv: -len(kv[1])):
        liste_triee = sorted(liste, key=lambda x: x["code"])
        A(f"### {libelle} (`{code}`) — {len(liste)} modèles")
        A("")
        if code == "m":
            A("| Code | Nom Officiel (FR) | Nom Fandom (EN) | Anim. | Poids | Fichier |")
            A("|---|---|---|---|---|---|")
            for m in liste_triee:
                cat = m["categorie"]
                n = m.get("animations", 0)
                anim = f"**{n}**" if n else "—"
                nom_fr = m["nom_fr"] or "—"
                nom_en = m["nom_en"] or "—"
                A(f"| `{m['code']}` | **{nom_fr}** | *{nom_en}* | {anim} | {m.get('taille_ko', '?')} Ko | `{cat}/{m['dossier']}/` |")
        else:
            A("| Modèle | Animations | Poids | Fichier |")
            A("|---|---|---|---|")
            for m in liste_triee:
                cat = m["categorie"]
                n = m.get("animations", 0)
                anim = f"**{n}**" if n else "—"
                label = f"`{m['dossier']}`"
                A(f"| {label} | {anim} | {m.get('taille_ko', '?')} Ko | `{cat}/{m['dossier']}/` |")
        A("")

    A("---")
    A("")
    A("## Les monstres les plus animés")
    A("")
    A("| Code | Nom Officiel (FR) | Nom Fandom (EN) | Animations |")
    A("|---|---|---|---|")
    for m in sorted([x for x in modeles if x["code"].startswith("m")], key=lambda x: -x.get("animations", 0))[:20]:
        A(f"| `{m['code']}` | **{m['nom_fr']}** | *{m['nom_en']}* | **{m.get('animations', 0)}** |")
    A("")
    A("---")
    A("")
    A("## Identification des monstres")
    A("")
    A("La correspondance entre les modèles 3D (`m000` → `m248`) et les monstres réels a été "
      "établie avec certitude mathématique en croisant les tables internes de la ROM :")
    A("- `ModelTbl.bin` : liste séquentielle des modèles 3D")
    A("- `ViewChrTbl.bin` : table d'affichage associant chaque ID monstre à son modèle 3D")
    A("- `message0.binE` & `message0.binF` : dictionnaires des noms officiels singuliers (FR & EN)")
    A("")
    A("## Cadre légal")
    A("")
    A("Ces fichiers sont issus de l'analyse d'une ROM commerciale, à des fins d'étude et de "
      "préservation (directive 2009/24/CE art. 5 et 6 ; CPI art. L.122-6-1).")
    A("")
    A("**Usage personnel uniquement. Ne pas redistribuer** : les modèles, textures et animations "
      "sont la propriété de Square Enix.")

    with open(os.path.join(MB, "CATALOGUE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print(f"Catalogue écrit : {len(modeles)} modèles, {len(groupes)} familles.")

if __name__ == "__main__":
    main()
