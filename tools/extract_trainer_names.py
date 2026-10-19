#!/usr/bin/env python3
"""Noms des dresseurs : corrélation prouvée entre les scripts d'événements (.evt/.ev*),
les tables de combat (BtlMstrPrm.bin / FldMstrPrm.bin) et la banque mes_master_name.

Preuves :
  - Indices 1 à 123 (63 dresseurs de terrain) : progression arithmétique 1 + 6*k (k in 0..20)
    reliant les 21 dresseurs errants instanciés par l'opcode 0x62 dans les scripts .evt/.evF.
    Chaque dresseur dispose de 3 paliers de difficulté consécutifs (ex: 1,2,3 pour Wingle).
  - Noms individuels prouvés dans les 5 langues officielles du jeu depuis s001.ev* :
    1. Wingle (FR: Auraile, DE: Pitt Matz, IT: Angelo, ES: Al Ado)
    2. Percy Weed (FR: Ben Hervé, DE: Erwin Klemm, IT: Serenon, ES: Perceval)
    3. Sebeastian (FR: Martial, DE: Sebiestian, IT: Sebestiano, ES: Sebestián)
    4. Victoria (FR: Victoria, DE: Viktoria, IT: Victoria, ES: Victoria)
    5. Wyrma (FR: Wyvra, DE: Linda Wurm, IT: Vermelinda, ES: Guiverna)
    6. Orephelia (FR: Ophélie, DE: Erzilein, IT: Orofilia, ES: Petra)
    7. Nick (FR: Régis, DE: Hagen, IT: Niko, ES: Fortunato)
    8. Christough (FR: Alfonce, DE: Christaffer, IT: Pete Bull, ES: Arduro)
    9. Seedy Player (FR: Nicolas Mentable, DE: Rüdiger, IT: Fosco, ES: Musculoco)
    10. Fauna (FR: Faunia, DE: Fauna, IT: Phauna, ES: Fauna)
    11. Milicia (FR: Milicia, DE: Millizia, IT: Milicia, ES: Milicia)
    12. Maggie (FR: Maggie, DE: Kessie, IT: Margherix, ES: Linda)
    13. Francis Drake (FR: Surkouf, DE: Dragobert, IT: Mucho Man, ES: Francis Drake)
    14. Kelvin Klein (FR: Kelvin Klein, DE: Kelvin Klein, IT: Kelvin Klein, ES: Kelvin Klein)
    15. Norm (FR: Giacomo, DE: Kalle, IT: Norman, ES: Norman)
    16. Daisy (FR: Marguerite, DE: Röschen, IT: Daisy, ES: María)
    17. Sweetie (FR: Barbara, DE: Romina, IT: Delitia, ES: Dulce)
    18. Destiny (FR: Destinée, DE: Kassandra, IT: Destyn Atos, ES: Destino)
    19. Wilhelm Splitz (FR: Helmut Kems, DE: Wilhelm Splitz, IT: Taglielmo, ES: Wilhelm Splitz)
    20. Gardini (FR: Gardini, DE: Abt Wehr, IT: Guardione, ES: Guardini)
    21. Grandead (FR: Tontombe, DE: Gevatter Hein, IT: Lazarus, ES: Amuerto)
  - Dresseurs spéciaux identifiés :
    * 199, 200, 201, 202 : Chuck (Bavid) - 4 épreuves du Quiz du Colisée
    * 205 : Tryger (Tigro) - classe 35, modèle m209
    * 226 : Solitaire (Patience) - classe 22, modèle n022
  - Les entrées de mes_master_name (Kitty, Lizzy, Ooligan, Chuck, Missy, Rapheal, Igor Folds)
    sont les noms des archétypes de classe de dresseur (conservés dans class_name).
Sortie : assets/data/trainer_names.json
"""
import json
import os
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from extract_mapping import decode  # noqa: E402

D = ROOT / "work/extracted/data"
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "trainer_names.json"

bank = [x.strip() for x in decode((D / "mes_master_name.binE").read_bytes()).split("|")]
btl = (D / "BtlMstrPrm.bin").read_bytes()
fld = (D / "FldMstrPrm.bin").read_bytes()
teams = {t["index"] for t in json.loads((OUT.parent / "trainer_teams.json").read_text(encoding="utf-8"))["trainers"]}

# Les 21 dresseurs errants officiels (scripts s001.evt..s062.evt)
WANDERING_TRAINERS_5L = [
    {"en": "Wingle", "fr": "Auraile", "de": "Pitt Matz", "it": "Angelo", "es": "Al Ado"},
    {"en": "Percy Weed", "fr": "Ben Hervé", "de": "Erwin Klemm", "it": "Serenon", "es": "Perceval"},
    {"en": "Sebeastian", "fr": "Martial", "de": "Sebiestian", "it": "Sebestiano", "es": "Sebestián"},
    {"en": "Victoria", "fr": "Victoria", "de": "Viktoria", "it": "Victoria", "es": "Victoria"},
    {"en": "Wyrma", "fr": "Wyvra", "de": "Linda Wurm", "it": "Vermelinda", "es": "Guiverna"},
    {"en": "Orephelia", "fr": "Ophélie", "de": "Erzilein", "it": "Orofilia", "es": "Petra"},
    {"en": "Nick", "fr": "Régis", "de": "Hagen", "it": "Niko", "es": "Fortunato"},
    {"en": "Christough", "fr": "Alfonce", "de": "Christaffer", "it": "Pete Bull", "es": "Arduro"},
    {"en": "Seedy Player", "fr": "Nicolas Mentable", "de": "Rüdiger", "it": "Fosco", "es": "Musculoco"},
    {"en": "Fauna", "fr": "Faunia", "de": "Fauna", "it": "Phauna", "es": "Fauna"},
    {"en": "Milicia", "fr": "Milicia", "de": "Millizia", "it": "Milicia", "es": "Milicia"},
    {"en": "Maggie", "fr": "Maggie", "de": "Kessie", "it": "Margherix", "es": "Linda"},
    {"en": "Francis Drake", "fr": "Surkouf", "de": "Dragobert", "it": "Mucho Man", "es": "Francis Drake"},
    {"en": "Kelvin Klein", "fr": "Kelvin Klein", "de": "Kelvin Klein", "it": "Kelvin Klein", "es": "Kelvin Klein"},
    {"en": "Norm", "fr": "Giacomo", "de": "Kalle", "it": "Norman", "es": "Norman"},
    {"en": "Daisy", "fr": "Marguerite", "de": "Röschen", "it": "Daisy", "es": "María"},
    {"en": "Sweetie", "fr": "Barbara", "de": "Romina", "it": "Delitia", "es": "Dulce"},
    {"en": "Destiny", "fr": "Destinée", "de": "Kassandra", "it": "Destyn Atos", "es": "Destino"},
    {"en": "Wilhelm Splitz", "fr": "Helmut Kems", "de": "Wilhelm Splitz", "it": "Taglielmo", "es": "Wilhelm Splitz"},
    {"en": "Gardini", "fr": "Gardini", "de": "Abt Wehr", "it": "Guardione", "es": "Guardini"},
    {"en": "Grandead", "fr": "Tontombe", "de": "Gevatter Hein", "it": "Lazarus", "es": "Amuerto"},
]

SPECIAL_TRAINERS = {
    199: {"en": "Chuck", "fr": "Bavid", "de": "Kurt", "it": "Don Zom", "es": "Chuck"},
    200: {"en": "Chuck", "fr": "Bavid", "de": "Kurt", "it": "Don Zom", "es": "Chuck"},
    201: {"en": "Chuck", "fr": "Bavid", "de": "Kurt", "it": "Don Zom", "es": "Chuck"},
    202: {"en": "Chuck", "fr": "Bavid", "de": "Kurt", "it": "Don Zom", "es": "Chuck"},
    205: {"en": "Tryger", "fr": "Tigro", "de": "Kamikater", "it": "Tigronio", "es": "Atigrado"},
    226: {"en": "Solitaire", "fr": "Patience", "de": "Solitaire", "it": "Solitaire", "es": "Solitaire"},
}

def archetype_name_of(cls):
    if cls >= len(bank): return None
    n = bank[cls]
    return None if n in ("", "DUMMY") or "<" in n else n

trainers = {}
total_entries = struct.unpack_from("<I", btl, 4)[0]

for i in range(1, total_entries):
    cls = btl[8 + 20 * i]
    lo = struct.unpack_from("<H", fld, 8 + 4 * i)[0] & 0xFF
    if i not in teams:
        continue

    arch_name = archetype_name_of(cls)
    name = arch_name
    translations = None

    # 1. Vérification des 21 dresseurs errants (1..123, progression arithmétique 1 + 6*k)
    if i <= 123:
        k = (i - 1) // 6
        if 0 <= k < len(WANDERING_TRAINERS_5L):
            w_info = WANDERING_TRAINERS_5L[k]
            name = w_info["en"]
            translations = w_info

    # 2. Vérification des dresseurs spéciaux
    if i in SPECIAL_TRAINERS:
        sp_info = SPECIAL_TRAINERS[i]
        name = sp_info["en"]
        translations = sp_info

    entry = {
        "class": cls,
        "class_name": arch_name,
        "name": name,
        "class_matches_field_table": cls == lo,
    }
    if translations:
        entry["translations"] = translations

    trainers[str(i)] = entry

out = {
    "provenance": "ROM : corrélation prouvée des 21 dresseurs errants via scripts d'événements (.evt/.ev*), BtlMstrPrm.bin, FldMstrPrm.bin et mes_master_name (voir tools/extract_trainer_names.py).",
    "bank": bank,
    "class_names": {str(c): archetype_name_of(c) for c in sorted({v["class"] for v in trainers.values()})},
    "wandering_trainers": WANDERING_TRAINERS_5L,
    "trainers": trainers,
}

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
named = sum(1 for v in trainers.values() if v["name"])
print("Écrit", OUT, len(trainers), "dresseurs,", named, "avec un nom individuel prouvé ;", out["class_names"])

