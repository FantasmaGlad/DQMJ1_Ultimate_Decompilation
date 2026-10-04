#!/usr/bin/env python3
"""Extrait le catalogue d'objets/équipement (`ItemTbl.bin`) — catégorie
entièrement absente du site bestiaire avant cette session (item 19 de
docs/DATA_RESEARCH_PLAN.md du projet bestiaire).

## Provenance et niveau de confiance (session du 2026-09-25, suite 15)

Structure de fichier confirmée par arithmétique, même méthode que pour
`EnmyKindTbl.bin`/`SkillTbl.bin` : magique `"ITEM"` (offset 0-3) + `u32`
nombre d'entrées (offset 4-7) = **174**, puis 174 entrées de **92 octets**
chacune — `(16016 - 8) / 174 = 92` entier exact.

Noms : `mes_itemomitname.binE`/`.binF` (258 entrées, noms courts/singuliers,
ex. "medicinal herb"/"herbe médicinale") — index = index direct de l'entrée
dans `ItemTbl.bin` (0 = slot vide, cohérent avec les autres tables du
projet). Seules les entrées 0 à ~154 ont un nom non vide ; 155-173 sont des
slots de fin de table inutilisés (tous les octets à zéro, vérifié). Il
existe aussi `mes_itemsname.binE`/`.binF` (forme plurielle utilisée dans
l'inventaire, ex. "medicinal herbs") — non utilisée ici, `omitname` donne un
nom plus propre pour l'affichage.

**Prix d'achat/vente (offsets 12 et 16, `u16` chacun) : validés par
cohérence, pas par désassemblage** — deux preuves convergentes :
1. Le prix de vente vaut quasi systématiquement la **moitié exacte** du prix
   d'achat (règle classique de la série Dragon Quest), vérifié sur
   l'écrasante majorité du catalogue (ex. herbe médicinale 8/4, remède
   spécial 250/125, sceptre Phénix 1200/600...). Quelques exceptions
   cohérentes avec la mécanique du jeu plutôt que des erreurs : les objets
   non achetables (ex. "pépite d'or" trouvée, pas vendue en boutique) ont un
   prix d'achat à 0 mais un prix de vente non nul ; certains livres/objets de
   collection ont un ratio de revente très inférieur à 1/2 (mécanique DQ
   connue : certains objets se revendent moins bien).
2. Les valeurs absolues sont cohérentes avec les prix bien connus de la
   série Dragon Quest pour les objets communs à plusieurs titres (herbe
   médicinale = 8 pièces d'or, valeur emblématique de la série depuis DQ1).

Champ à l'offset 6 (`u16`) : regroupe des valeurs par blocs cohérents avec
les catégories visibles dans les noms (ex. les 7 "graines de stat" partagent
toutes une valeur proche 1282-1284) — **candidat sérieux pour un
type/catégorie d'objet, mais PAS assez confirmé pour être publié** (pas de
règle simple identifiée, ne pas deviner sa signification exacte).

## Limite assumée

Aucun champ "effet" (soin en HP, dégâts, attaque conférée par une arme...)
n'est publié ici — plusieurs octets candidats ont été repérés (ex. offset 5-6
de l'entrée brute, cohérent avec une valeur de soin pour les remèdes) mais ne
sont pas assez confirmés (une seule famille d'objets testée en détail) pour
être publiés sans risque de deviner. Catalogue actuel : nom + prix
uniquement.
"""
import json
import os
import re
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
sys.path.insert(0, os.path.join(RACINE, "tools"))
from extraire_mapping import decode  # noqa: E402

ENTRY_SIZE = 92
HEADER_SIZE = 8


def clean_name(name):
    # Résidus cosmétiques : quelques titres de livres gardent, dans la
    # banque française uniquement, des codes de contrôle non identifiés
    # (probablement liés à la mise en forme "italique/citation" du jeu, pas
    # au contenu du nom) et une apostrophe de citation isolée en tête/fin —
    # simple nettoyage d'affichage, jamais un changement de contenu.
    name = re.sub(r"<[0-9a-f]{2}>", "", name)
    return name.strip("'").strip()


def load_names(filename):
    with open(os.path.join(DATA, filename), "rb") as f:
        raw = f.read()
    return [clean_name(x) for x in decode(raw).split("|")]


def main():
    with open(os.path.join(DATA, "ItemTbl.bin"), "rb") as f:
        data = f.read()
    magic = data[:4]
    assert magic == b"ITEM", magic
    count = struct.unpack_from("<I", data, 4)[0]
    assert (len(data) - HEADER_SIZE) == count * ENTRY_SIZE, "taille de fichier inattendue"

    names_en = load_names("mes_itemomitname.binE")
    names_fr = load_names("mes_itemomitname.binF")

    items = {}
    for i in range(count):
        name_en = names_en[i] if i < len(names_en) else ""
        if not name_en:
            continue  # slot vide/inutilisé, ne rien publier
        entry = data[HEADER_SIZE + i * ENTRY_SIZE : HEADER_SIZE + (i + 1) * ENTRY_SIZE]
        buy_price = struct.unpack_from("<H", entry, 12)[0]
        sell_price = struct.unpack_from("<H", entry, 16)[0]
        items[str(i)] = {
            "item_id": i,
            "name_en": name_en,
            "name_fr": names_fr[i] if i < len(names_fr) else name_en,
            "buy_price": buy_price,
            "sell_price": sell_price,
        }

    out_file = os.path.join(RACINE, "tools/items.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)

    print(f"Objets publiés : {len(items)} / {count} slots de la table")


if __name__ == "__main__":
    main()
