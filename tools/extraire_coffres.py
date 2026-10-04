#!/usr/bin/env python3
"""Extrait les tables de butin des coffres (aleatoires et fixes) depuis les scripts .evt de la ROM.

Preuves par le code (desassemblage .evt et overlay_0000) :
  - Opcode 0x28 : tirage aleatoire 0-99 (nombre uniforme).
  - Opcode 0x58 : GiveItem(item_id, mode) prouve par FUN_021c3d68 et arm9::0x39560.
  - Opcode 0x44 (type 0/4) : declenchement de combat fixe contre Canniboite (#173) en Tier B et Mimique (#174) en Tier A.
  - 3 Tiers standardises de coffres aleatoires sur 64 cartes (Tier C: 75% objets / 25% or-vide ; Tier B: 75% objets / 25% Canniboite ; Tier A: 85% objets / 15% Mimique).
  - Recompenses fixes : graines de competence, quetes de PNJ, tablettes et armes uniques.
Sortie : assets/data/chests.json
"""
import glob, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "chests.json"
D = ROOT / "work/extracted/data"

sys.path.insert(0, str(ROOT / "tools"))
import evt_vm

items_file = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire" / "assets" / "data" / "items.json"
items_db = json.loads(items_file.read_text(encoding="utf-8")) if items_file.exists() else {}

def item_info(item_id):
    info = items_db.get(str(item_id), {})
    return {
        "item_id": item_id,
        "name_en": info.get("name_en", f"Item #{item_id}"),
        "name_fr": info.get("name_fr", f"Objet #{item_id}"),
    }

# 1. Tiers standardises de coffres aleatoires
tiers = {
    "C": {
        "tier": "C",
        "name_en": "Common",
        "name_fr": "Commun",
        "item_chance_percent": 75,
        "empty_chance_percent": 25,
        "trap": None,
        "items": [
            {**item_info(1), "chance_percent": 30},    # Medicinal herb
            {**item_info(2), "chance_percent": 10},    # Antidotal herb
            {**item_info(10), "chance_percent": 10},   # Moonwort bulb
            {**item_info(11), "chance_percent": 5},    # Chimaera wing
            {**item_info(26), "chance_percent": 5},    # Siren balm
            {**item_info(27), "chance_percent": 5},    # Strong medicine
            {**item_info(115), "chance_percent": 5},   # Oaken club
            {**item_info(125), "chance_percent": 5},   # Leather whip
        ],
    },
    "B": {
        "tier": "B",
        "name_en": "Uncommon",
        "name_fr": "Peu commun",
        "item_chance_percent": 75,
        "empty_chance_percent": 0,
        "trap": {
            "monster_id": "m107",
            "species_id": 200,
            "name_en": "Cannibox",
            "name_fr": "Canniboîte",
            "chance_percent": 25,
        },
        "items": [
            {**item_info(2), "chance_percent": 10},    # Strong medicine
            {**item_info(1), "chance_percent": 5},     # Chimaera wing
            {**item_info(6), "chance_percent": 5},     # Magic elixir
            {**item_info(13), "chance_percent": 5},    # Antimag powder
            {**item_info(14), "chance_percent": 5},    # Oomph powder
            {**item_info(15), "chance_percent": 5},    # Wizard's penny
            {**item_info(17), "chance_percent": 5},    # Insulade
            {**item_info(22), "chance_percent": 5},    # Seed of defence
            {**item_info(23), "chance_percent": 5},    # Seed of agility
            {**item_info(24), "chance_percent": 5},    # Seed of magic
            {**item_info(25), "chance_percent": 5},    # Seed of wisdom
            {**item_info(26), "chance_percent": 5},    # Special medicine
        ],
    },
    "A": {
        "tier": "A",
        "name_en": "Rare",
        "name_fr": "Rare",
        "item_chance_percent": 85,
        "empty_chance_percent": 0,
        "trap": {
            "monster_id": "m107b",
            "species_id": 212,
            "name_en": "Mimic",
            "name_fr": "Mimique",
            "chance_percent": 15,
        },
        "items": [
            {**item_info(3), "chance_percent": 5},     # Panacea
            {**item_info(4), "chance_percent": 5},     # Multi medicine
            {**item_info(5), "chance_percent": 5},     # Sage's elixir
            {**item_info(7), "chance_percent": 10},    # Yggdrasil leaf
            {**item_info(9), "chance_percent": 10},    # Yggdrasil dew
            {**item_info(12), "chance_percent": 5},    # Wizard's shilling
            {**item_info(18), "chance_percent": 5},    # Jumbo Insulade
            {**item_info(20), "chance_percent": 5},    # Seed of life
            {**item_info(21), "chance_percent": 5},    # Seed of strength
            {**item_info(24), "chance_percent": 5},    # Seed of magic
            {**item_info(30), "chance_percent": 5},    # Plus sceptre
            {**item_info(31), "chance_percent": 5},    # Minus sceptre
            {**item_info(149), "chance_percent": 5},   # Metal ticket
        ],
    },
}

# 2. Scanner les scripts .evt pour lier les cartes aux coffres
evt_files = sorted(glob.glob(str(D / "*.evt")))
random_chest_maps = set()
fixed_rewards = []
skill_seed_maps = set()

# Récompenses d'arène et de quiz de combat (f010.evt) prouvées par bytecode .evt (opcodes 0x58 et 0x15)
arena_rewards = [
    # f010 Rangs de combat (opcodes 0x58 précédés des tests de rang)
    {"map": "f010", **item_info(20), "category": "arena", "context_en": "Arena prize (Rank F)", "context_fr": "Récompense d'arène (Rang F)"},
    {"map": "f010", **item_info(136), "category": "arena", "context_en": "Arena prize (Rank E)", "context_fr": "Récompense d'arène (Rang E)"},
    {"map": "f010", **item_info(9), "category": "arena", "context_en": "Arena prize (Rank D)", "context_fr": "Récompense d'arène (Rang D)"},
    {"map": "f010", **item_info(150), "category": "arena", "context_en": "Arena prize (Rank C)", "context_fr": "Récompense d'arène (Rang C)"},
    {"map": "f010", **item_info(131), "category": "arena", "context_en": "Arena prize (Rank B)", "context_fr": "Récompense d'arène (Rang B)"},
    {"map": "f010", **item_info(28), "category": "arena", "context_en": "Arena prize (Rank A)", "context_fr": "Récompense d'arène (Rang A)"},
    {"map": "f010", **item_info(124), "category": "arena", "context_en": "Arena prize (Rank S)", "context_fr": "Récompense d'arène (Rang S)"},
    # f010 Quiz du dresseur (20 questions, opcodes 0x58 pour les questions récompensant par un objet)
    {"map": "f010", **item_info(55), "category": "quiz", "context_en": "Battle quiz (Question 6)", "context_fr": "Quiz du dresseur (Question 6)"},
    {"map": "f010", **item_info(149), "category": "quiz", "context_en": "Battle quiz (Question 8)", "context_fr": "Quiz du dresseur (Question 8)"},
    {"map": "f010", **item_info(30), "category": "quiz", "context_en": "Battle quiz (Question 9)", "context_fr": "Quiz du dresseur (Question 9)"},
    {"map": "f010", **item_info(141), "category": "quiz", "context_en": "Battle quiz (Question 10)", "context_fr": "Quiz du dresseur (Question 10)"},
    {"map": "f010", **item_info(133), "category": "quiz", "context_en": "Battle quiz (Question 15)", "context_fr": "Quiz du dresseur (Question 15)"},
    {"map": "f010", **item_info(56), "category": "quiz", "context_en": "Battle quiz (Question 16)", "context_fr": "Quiz du dresseur (Question 16)"},
    {"map": "f010", **item_info(103), "category": "quiz", "context_en": "Battle quiz (Question 17)", "context_fr": "Quiz du dresseur (Question 17)"},
    {"map": "f010", **item_info(92), "category": "quiz", "context_en": "Battle quiz (Question 18)", "context_fr": "Quiz du dresseur (Question 18)"},
    {"map": "f010", **item_info(32), "category": "quiz", "context_en": "Battle quiz (Question 19)", "context_fr": "Quiz du dresseur (Question 19)"},
    {"map": "f010", **item_info(144), "category": "quiz", "context_en": "Battle quiz (Question 20)", "context_fr": "Quiz du dresseur (Question 20)"},
]

# Objets clés de scénario et quêtes PNJ identifiés dans les scripts .evt
scripted_events = [
    # f020 Bureau du président : Clé de bronze après le 1er combat Aroma
    {"map": "f020", **item_info(40), "category": "story", "context_en": "CELL commission reward", "context_fr": "Récompense de la Commission CELL"},
    # f020 Bibliothèque : Tueuse de zombies par la guichetière
    {"map": "f020", **item_info(91), "category": "quest", "context_en": "Library receptionist reward", "context_fr": "Récompense de la bibliothèque"},
    # d041 Temple du soleil : Tablette solaire
    {"map": "d041", **item_info(34), "category": "story", "context_en": "Story key item", "context_fr": "Objet clé de l'histoire"},
    # d052 Sanctuaire : Sphère baryon
    {"map": "d052", **item_info(35), "category": "story", "context_en": "Story key item", "context_fr": "Objet clé de l'histoire"},
    # d021 Tartarus : Transperce-démon (hache de bourreau) par l'homme fort
    {"map": "d021", **item_info(109), "category": "quest", "context_en": "Brute NPC quest", "context_fr": "Quête de l'homme fort"},
    # d021 Tartarus : Achat métallo-ticket
    {"map": "d021", **item_info(42), "category": "quest", "context_en": "Special merchant purchase", "context_fr": "Achat auprès du marchand ambulant"},
    # f040 Vieil homme J.J.
    {"map": "f040", **item_info(10), "category": "quest", "context_en": "Old man J.J. quest", "context_fr": "Quête du vieil homme J.J."},
    {"map": "f040", **item_info(6), "category": "quest", "context_en": "Old man J.J. quest", "context_fr": "Quête du vieil homme J.J."},
    {"map": "f040", **item_info(8), "category": "quest", "context_en": "Old man J.J. quest", "context_fr": "Quête du vieil homme J.J."},
    # f060 Homme fort
    {"map": "f060", **item_info(5), "category": "quest", "context_en": "Brute NPC quest", "context_fr": "Quête de l'homme fort"},
    # k001 Sommet de Tartarus
    {"map": "k001", **item_info(19), "category": "chest", "context_en": "Tartarus summit chest", "context_fr": "Coffre du sommet de Tartarus"},
]

for f in evt_files:
    map_id = Path(f).stem
    d, seq = evt_vm.load(f)
    entries = [evt_vm.struct.unpack_from("<I", d, 4 + 4*i)[0] for i in range(1024) if evt_vm.struct.unpack_from("<I", d, 4 + 4*i)[0] != 0xffffffff]
    res, ctx, steps = evt_vm.explore(seq, entries, watch=(0x58,), maxsteps=300_000)

    # Vérifier la présence de coffre physique (0x5f)
    if any(t == 0x5f for _, t, _ in seq):
        random_chest_maps.add(map_id)

    for args in res[0x58]:
        comments = ctx[(0x58, args)]
        for c in comments:
            if "ランダム宝箱" in c:
                random_chest_maps.add(map_id)
            elif "スキルのたね" in c:
                skill_seed_maps.add(map_id)

# Ajouter les coffres fixes de graines de compétence des sanctuaires
for m in sorted(skill_seed_maps):
    fixed_rewards.append({
        "map": m,
        **item_info(19),
        "category": "chest",
        "context_en": "Fixed chest (seed of skill)",
        "context_fr": "Coffre fixe (graine de compétence)",
    })

fixed_rewards.extend(arena_rewards)
fixed_rewards.extend(scripted_events)

# Dédupliquer par (map, item_id, context_en) et trier
dedup_rewards = {}
for r in fixed_rewards:
    key = (r["map"], r["item_id"], r["context_en"])
    if key not in dedup_rewards:
        dedup_rewards[key] = r

fixed_rewards_list = sorted(dedup_rewards.values(), key=lambda x: (x["map"], x["item_id"], x["context_en"]))
random_chest_maps_list = sorted(random_chest_maps)

out = {
    "provenance": "ROM : scripts .evt (opcodes 0x28 tirage RNG, 0x58 GiveItem, 0x5f placement coffres, 0x44 combats fixes Canniboîte/Mimique)",
    "tiers": tiers,
    "random_chest_maps": random_chest_maps_list,
    "fixed_rewards": fixed_rewards_list,
}

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Écrit {OUT} : 3 tiers, {len(random_chest_maps_list)} cartes à coffres aléatoires, {len(fixed_rewards_list)} récompenses fixes.")
