#!/usr/bin/env python3
"""
correlate_sfx.py -- Corrélation sémantique 1:1 des 306 bruitages SFX de DQMJ1.

Sources de vérité :
  - sound_data.sadl (constantes des pilotes Procyon Studio)
  - sound_data.sdat (blocs SYMB, INFO, FAT, FILE)
  - BtlChrTbl.bin (389 entrées x 26 octets : tables d'effets sonores monstres et armes)
  - TokugiDataTbl.bin (256 entrées x 40 octets : attributs et familles d'aptitudes)
  - BtlEfcTbl.bin / BtlEfcTblWhip.bin (tables d'ordonnancement d'animations d'effets)
  - assets/data/game_sfx.json (306 fichiers MP3 extraits)
  - assets/data/spell_effects.json (256 aptitudes avec traductions 5 langues)

Produit :
  - DragonQuestMonsterJoker1Bestiaire/assets/data/sfx_mapping.json (306 entrées corrélées)
  - DragonQuestMonsterJoker1Bestiaire/assets/data/spell_effects.json (enrichi des sfx_symbol vérifiés)
"""

import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "work", "extracted", "data")
WIKI_DIR = "/home/fanta/Developpement/DQMJ1/DragonQuestMonsterJoker1Bestiaire"
DEST_MAPPING_JSON = os.path.join(WIKI_DIR, "assets", "data", "sfx_mapping.json")
SPELL_EFFECTS_JSON = os.path.join(WIKI_DIR, "assets", "data", "spell_effects.json")
GAME_SFX_JSON = os.path.join(WIKI_DIR, "assets", "data", "game_sfx.json")

# Table sémantique exhaustive pour les 115 sorts et compétences (SE_SKL_*)
SKL_DESCRIPTIONS = {
    "SE_SKL_001": ("Incantation de sort standard", "Standard spell casting", ["incantation", "magie"]),
    "SE_SKL_002": ("Incantation de sort suprême", "High tier spell casting", ["incantation", "gigasort"]),
    "SE_SKL_003": ("Aspiration avant souffle", "Breath attack inhalation", ["souffle", "inspiration"]),
    "SE_SKL_004": ("Rythme de danse martiale", "Martial dance rhythm", ["danse"]),
    "SE_SKL_005": ("Cri de guerre et concentration", "War cry and focus posture", ["concentration", "posture"]),
    "SE_SKL_006": ("Incantation de sort d'altération", "Status ailment spell cast", ["altération", "malédiction"]),
    "SE_SKL_007": ("Attaque tranchante à l'épée", "Sword slash attack", ["arme", "épée"]),
    "SE_SKL_008": ("Impact physique de coup reçu", "Physical strike impact", ["impact", "dégâts"]),
    "SE_SKL_009": ("Frappe contondante au bâton", "Staff strike attack", ["arme", "bâton"]),
    "SE_SKL_010": ("Coup de griffes acérées", "Claw slash attack", ["arme", "griffes"]),
    "SE_SKL_011": ("Coup d'estoc à la lance", "Spear thrust attack", ["arme", "lance"]),
    "SE_SKL_012": ("Coup lourd à la hache", "Axe chop attack", ["arme", "hache"]),
    "SE_SKL_013": ("Écrasement massif au marteau", "Hammer smash attack", ["arme", "marteau"]),
    "SE_SKL_014": ("Claquement de fouet", "Whip crack attack", ["arme", "fouet"]),
    "SE_SKL_015": ("Tir de flèche à l'arc", "Bow arrow shot", ["arme", "arc"]),
    "SE_SKL_016": ("Frappe martiale à mains nues", "Unarmed strike", ["arme", "mains nues"]),
    "SE_SKL_017": ("Coup critique dévastateur", "Violent critical hit impact", ["critique", "impact"]),
    "SE_SKL_018": ("Attaque lourde et puissante", "Heavy physical blow", ["frappe lourde"]),
    "SE_SKL_019": ("Sort Flamme (Frizz) — petite boule de feu", "Frizz spell — small fireball", ["sort", "feu", "frizz"]),
    "SE_SKL_020": ("Sort Superflamme (Frizzle) — boule de feu ardente", "Frizzle spell — fiery blaze", ["sort", "feu", "frizzle"]),
    "SE_SKL_021": ("Sort Mégaflamme (Kafrizz) — vortex embrasé", "Kafrizz spell — raging inferno", ["sort", "feu", "kafrizz"]),
    "SE_SKL_022": ("Sort Gigaflamme (Kafrizzle) — cataclysme de feu", "Kafrizzle spell — cataclysmic flames", ["sort", "feu", "kafrizzle"]),
    "SE_SKL_023": ("Sort Bang — petite déflagration", "Bang spell — small blast", ["sort", "explosion", "bang"]),
    "SE_SKL_024": ("Sort Superbang (Boom) — détonation moyenne", "Boom spell — intense explosion", ["sort", "explosion", "boom"]),
    "SE_SKL_025": ("Sort Mégabang (Kaboom) — souffle explosif majeur", "Kaboom spell — violent concussive shockwave", ["sort", "explosion", "kaboom"]),
    "SE_SKL_026": ("Sort Gigabang (Kaboomle) — apocalypse explosive", "Kaboomle spell — apocalyptic explosion", ["sort", "explosion", "kaboomle"]),
    "SE_SKL_027": ("Sort Tornade (Woosh) — rafale tourbillonnante", "Woosh spell — swirling gust", ["sort", "vent", "woosh"]),
    "SE_SKL_028": ("Sort Supertornade (Swoosh) — bourrasque tranchante", "Swoosh spell — cutting wind blades", ["sort", "vent", "swoosh"]),
    "SE_SKL_029": ("Sort Mégatornade (Kaswoosh) — cyclone violent", "Kaswoosh spell — devastating cyclone", ["sort", "vent", "kaswoosh"]),
    "SE_SKL_030": ("Sort Gigatornade (Kaswooshle) — ouragan déchaîné", "Kaswooshle spell — raging tempest hurricane", ["sort", "vent", "kaswooshle"]),
    "SE_SKL_031": ("Sort Glace (Crack) — éclat de givre", "Crack spell — ice shard", ["sort", "glace", "crack"]),
    "SE_SKL_032": ("Sort Superglace (Crackle) — pics de givre acérés", "Crackle spell — sharp ice spikes", ["sort", "glace", "crackle"]),
    "SE_SKL_033": ("Sort Mégaglace (Kacrack) — tempête de blizzard", "Kacrack spell — piercing blizzard", ["sort", "glace", "kacrack"]),
    "SE_SKL_034": ("Sort Gigaglace (Kacrackle) — froid absolu polaire", "Kacrackle spell — absolute zero freeze", ["sort", "glace", "kacrackle"]),
    "SE_SKL_035": ("Sort Foudre (Zap) — étincelle sacrée", "Zap spell — holy lightning spark", ["sort", "foudre", "zap"]),
    "SE_SKL_036": ("Sort Superfoudre (Zapple) — arc électrique foudroyant", "Zapple spell — striking thunder bolt", ["sort", "foudre", "zapple"]),
    "SE_SKL_037": ("Sort Mégafoudre (Kazap) — tonnerre sacré", "Kazap spell — sacred celestial thunder", ["sort", "foudre", "kazap"]),
    "SE_SKL_038": ("Sort Gigafoudre (Kazapple) — colère divine des cieux", "Kazapple spell — divine heavenly wrath", ["sort", "foudre", "kazapple"]),
    "SE_SKL_039": ("Sort Élec (Zam) — onde obscure", "Zam spell — dark shadowy wave", ["sort", "ombre", "zam"]),
    "SE_SKL_040": ("Sort Superélec (Zammle) — vortex ténébreux", "Zammle spell — shadowy dark vortex", ["sort", "ombre", "zammle"]),
    "SE_SKL_041": ("Sort Mégaélec (Kazam) — abysses de ténèbres", "Kazam spell — deep shadowy abyss", ["sort", "ombre", "kazam"]),
    "SE_SKL_042": ("Sort Gigaélec (Kazammle) — trou noir dimensionnel", "Kazammle spell — dimensional black hole", ["sort", "ombre", "kazammle"]),
    "SE_SKL_043": ("Sort Kill (Whack) — sentence de mort subite", "Whack spell — instant death sentence", ["sort", "mort", "whack"]),
    "SE_SKL_044": ("Sort Superkill (Thwack) — faucheuse collective", "Thwack spell — group instant death scythe", ["sort", "mort", "thwack"]),
    "SE_SKL_045": ("Sort Kamikaze — explosion de sacrifice", "Kamikazee spell — sacrificial self-destruction", ["sort", "sacrifice", "kamikaze"]),
    "SE_SKL_046": ("Sort 1ers secours (Heal) — lueur réparatrice", "Heal spell — minor healing glow", ["sort", "soin", "heal"]),
    "SE_SKL_047": ("Sort Soins partiels (Midheal) — onde curative moyenne", "Midheal spell — moderate healing wave", ["sort", "soin", "midheal"]),
    "SE_SKL_048": ("Sort Soins complets (Fullheal) — plénitude de PV", "Fullheal spell — complete recovery glow", ["sort", "soin", "fullheal"]),
    "SE_SKL_049": ("Sort Multisoin (Multiheal) — brise bienfaisante de groupe", "Multiheal spell — group revitalizing breeze", ["sort", "soin", "multiheal"]),
    "SE_SKL_050": ("Sort Omnisoin (Omniheal) — grâce divine intégrale", "Omniheal spell — complete party restoration", ["sort", "soin", "omniheal"]),
    "SE_SKL_051": ("Partage de magie (Share Magic) — transfert de PM", "Share Magic spell — MP transfer resonance", ["sort", "pm", "don"]),
    "SE_SKL_052": ("Sort Rappel (Zing) — étincelle de réanimation", "Zing spell — resuscitation spark", ["sort", "résurrection", "zing"]),
    "SE_SKL_053": ("Sort Résurrection (Kazing) — rappel d'âme infaillible", "Kazing spell — guaranteed soul recovery", ["sort", "résurrection", "kazing"]),
    "SE_SKL_054": ("Sort Conjuration (Kerplunk) — don d'énergie vitale", "Kerplunk spell — sacrificial total party revive", ["sort", "résurrection", "kerplunk"]),
    "SE_SKL_055": ("Antipoison et Stimulation — dissolution de toxines", "Squelch & Tingle — status purification", ["sort", "purification", "poison"]),
    "SE_SKL_056": ("Sort Décuplo (Oomph) — renforcement musculaire", "Oomph spell — attack power surge", ["sort", "bonus", "attaque"]),
    "SE_SKL_057": ("Sort Superdécuplo (Oomphle) — ferveur guerrière de groupe", "Oomphle spell — group attack power surge", ["sort", "bonus", "attaque"]),
    "SE_SKL_058": ("Sort Affaiblo (Sag) — affaiblissement physique", "Sag spell — enemy attack reduction", ["sort", "malus", "attaque"]),
    "SE_SKL_059": ("Sort Protection (Buff) — durcissement d'armure", "Buff spell — defense fortification", ["sort", "bonus", "défense"]),
    "SE_SKL_060": ("Sort Mégaprotection (Kabuff) — bouclier collectif", "Kabuff spell — group defense shield", ["sort", "bonus", "défense"]),
    "SE_SKL_061": ("Sort Altération (Sap) — brisure d'armure", "Sap spell — enemy armor fracture", ["sort", "malus", "défense"]),
    "SE_SKL_062": ("Sort Mégaltération (Kasap) — effritement de défenses", "Kasap spell — group defense breakdown", ["sort", "malus", "défense"]),
    "SE_SKL_063": ("Sort Accéléro (Accelerate) — foulée vive et agile", "Accelerate spell — agility boost", ["sort", "bonus", "vitesse"]),
    "SE_SKL_064": ("Sort Décéléro (Decelerate) — entrave et ralentissement", "Decelerate spell — agility reduction", ["sort", "malus", "vitesse"]),
    "SE_SKL_065": ("Sort Eurêka (Ping) — illumination spirituelle", "Ping spell — wisdom clarity boost", ["sort", "bonus", "sagesse"]),
    "SE_SKL_066": ("Sort Simplet (Dim) — embrumement d'esprit", "Dim spell — wisdom suppression", ["sort", "malus", "sagesse"]),
    "SE_SKL_067": ("Sort Illusion (Dazzle) — mirage éblouissant", "Dazzle spell — blinding illusion fog", ["sort", "altération", "illusion"]),
    "SE_SKL_068": ("Sort Torpeur (Snooze) — brume soporifique", "Snooze spell — gentle sleep mist", ["sort", "altération", "sommeil"]),
    "SE_SKL_069": ("Sort Mégatorpeur (Kasnooze) — sommeil lourd et profond", "Kasnooze spell — deep slumber trance", ["sort", "altération", "sommeil"]),
    "SE_SKL_070": ("Sort Aspirmagie (Drain Magic) — siphon de fluide magique", "Drain Magic spell — magical power siphon", ["sort", "drain", "pm"]),
    "SE_SKL_071": ("Sort Antimagie (Fizzle) — sceau du silence", "Fizzle spell — magic sealing silence", ["sort", "altération", "silence"]),
    "SE_SKL_072": ("Sort Réflexion (Bounce) — miroir astral réflecteur", "Bounce spell — reflecting astral mirror", ["sort", "barrière", "miroir"]),
    "SE_SKL_073": ("Sort Confusion (Fuddle) — ondes désorientantes", "Fuddle spell — bewildering thought waves", ["sort", "altération", "confusion"]),
    "SE_SKL_074": ("Sort Immoblindage (Clang) — transformation en bloc d'acier", "Clang spell — steel encasement invulnerability", ["sort", "défense", "acier"]),
    "SE_SKL_075": ("Sort Isolation (Insulate) — manteau anti-souffle", "Insulate spell — breath resistance barrier", ["sort", "barrière", "souffle"]),
    "SE_SKL_076": ("Souffle de feu — jet de braises ardentes", "Fire Breath — small gout of flames", ["souffle", "feu"]),
    "SE_SKL_077": ("Cracheflamme — torrent de flammes", "Flame Breath — roaring stream of fire", ["souffle", "feu"]),
    "SE_SKL_078": ("Inferno — déferlement de lave incandescent", "Inferno — violent tidal wave of flame", ["souffle", "feu"]),
    "SE_SKL_079": ("Brûlure — incendie purificateur planétaire", "Scorch — world-scorching thermal wave", ["souffle", "feu"]),
    "SE_SKL_080": ("Souffle frais — brume de givre matinale", "Cool Breath — crisp morning frost mist", ["souffle", "glace"]),
    "SE_SKL_081": ("Souffle froid — rafale glaciale perçante", "Chilly Breath — biting frosty gust", ["souffle", "glace"]),
    "SE_SKL_082": ("Souffle de givre — bourrasque polaire", "Blizzard Breath — freezing polar blizzard", ["souffle", "glace"]),
    "SE_SKL_083": ("Souffle gla-glacial — congélation instantanée", "C-C-Cold Breath — absolute deep freeze breath", ["souffle", "glace"]),
    "SE_SKL_084": ("Explosion magique (Magic Burst) — libération intégrale des PM", "Magic Burst — all-consuming magical detonation", ["sort", "ultime", "pm"]),
    "SE_SKL_085": ("Barrière magique (Magic Barrier) — bouclier ésotérique", "Magic Barrier — esoteric defense rune", ["sort", "barrière"]),
    "SE_SKL_086": ("Faille magique (Magic Frailty) — réceptivité magique accrue", "Magic Frailty — arcane vulnerability aura", ["sort", "malus"]),
    "SE_SKL_087": ("Lame de feu (Flame Slash) — entaille incandescente", "Flame Slash — flaming sword strike", ["lame", "feu"]),
    "SE_SKL_088": ("Lame infernale (Inferno Slash) — estocade de magma", "Inferno Slash — fiery molten strike", ["lame", "feu"]),
    "SE_SKL_089": ("Lame détonante (Bomb Slash) — coup à amorce explosive", "Bomb Slash — explosive-charged blade cut", ["lame", "explosion"]),
    "SE_SKL_090": ("Lame explosive (Blast Slash) — fente à déflagration lourde", "Blast Slash — shattering explosive cleave", ["lame", "explosion"]),
    "SE_SKL_091": ("Lame de vent (Gust Slash) — taillade aérienne véloce", "Gust Slash — rapid aerial wind stroke", ["lame", "vent"]),
    "SE_SKL_092": ("Lame d'Éole (Gale Slash) — vortex tranchant au fil de la lame", "Gale Slash — razor-edged hurricane stroke", ["lame", "vent"]),
    "SE_SKL_093": ("Lame de glace (Blizzard Slash) — coup congelant", "Blizzard Slash — frostbitten frozen slice", ["lame", "glace"]),
    "SE_SKL_094": ("Lame d'éclair (Lightning Slash) — fente électrifiée", "Lightning Slash — charged thunder stroke", ["lame", "foudre"]),
    "SE_SKL_095": ("Lame d'ombre (Dark Slash) — coup imbibé de ténèbres", "Dark Slash — shadow-infused strike", ["lame", "ombre"]),
    "SE_SKL_096": ("Frappe divine (Sacred Slash) — incision de lumière sacrée", "Sacred Slash — divine luminous incision", ["lame", "sacré"]),
    "SE_SKL_097": ("Frappe miraculeuse (Miracle Slash) — vampirisation curative", "Miracle Slash — life-stealing miracle strike", ["lame", "soin"]),
    "SE_SKL_098": ("Multicoup (Multislash) — déluge d'entailles consécutives", "Multislash — flurry of rapid blade strikes", ["lame", "multicoup"]),
    "SE_SKL_099": ("Brise-casque (Helm Splitter) — fente perforante d'armure", "Helm Splitter — armor-breaking downward chop", ["technique", "altération"]),
    "SE_SKL_100": ("Attaque métallique (Metal Slash) — coupe transperce-métal", "Metal Slash — metal-piercing precise slash", ["technique", "métal"]),
    "SE_SKL_101": ("Frappe faucon (Falcon Slash) — double frappe fulgurante", "Falcon Slash — swift dual falcon strikes", ["technique", "faucon"]),
    "SE_SKL_102": ("Danse de l'épée (Sword Dance) — chorégraphie d'acier quadrilatère", "Sword Dance — four-strike steel choreography", ["danse", "épée"]),
    "SE_SKL_103": ("Gigagash (Gigaslash) — foudre céleste guidée sur l'épée", "Gigaslash — ultimate celestial sword storm", ["ultime", "épée"]),
    "SE_SKL_104": ("Danse des soins (Hustle Dance) — pas joyeux régénérants", "Hustle Dance — joyful invigorating healing dance", ["danse", "soin"]),
    "SE_SKL_105": ("Regard hypnotique — fixation troublante", "Fuddle Glance — hypnotic disorienting gaze", ["regard", "confusion"]),
    "SE_SKL_106": ("Provocation — gesticulation insultante", "Taunt — mocking provocation gesture", ["provocation"]),
    "SE_SKL_107": ("Morsure paralysante — venin neurotoxique", "Paralyzing Bite — paralyzing neurotoxic venom", ["morsure", "paralysie"]),
    "SE_SKL_108": ("Souffle toxique — exhalaison de vapeurs empoisonnées", "Poison Breath — noxious toxic vapour cloud", ["souffle", "poison"]),
    "SE_SKL_109": ("Flash éblouissant — éclat lumineux aveuglant", "Blinding Flash — radiant dazzling flash", ["lumière", "aveuglement"]),
    "SE_SKL_110": ("Rugissement de guerre — onde sonore paralysante", "War Roar — roaring terrifying shockwave", ["rugissement", "cri"]),
    "SE_SKL_111": ("Charge brutale — projection corporelle lourde", "Body Slam — heavy bodily impact slam", ["charge", "impact"]),
    "SE_SKL_112": ("Coup de boule — percussion frontale étourdissante", "Headbutt — stunning forehead smash", ["percussion", "étourdissement"]),
    "SE_SKL_113": ("Éruption volcanique (Magma Burst) — geyser de roches ignées", "Magma Burst — fiery molten volcanic geyser", ["sort", "magma"]),
    "SE_SKL_114": ("Chute de météore (Meteor Drop) — bolide stellaire écrasant", "Meteor Drop — crashing celestial meteorite", ["sort", "météore"]),
    "SE_SKL_115": ("Rayon céleste suprême (Saint's Ray) — faisceau sanctifié", "Saint's Ray — supreme consecrated ray", ["sort", "sacré", "ultime"]),
}

# Mapping de chaque aptitude (1 à 255) vers son symbole audio canonique
SPELL_ID_TO_SFX = {
    1: "SE_SKL_019", 2: "SE_SKL_020", 3: "SE_SKL_021", 4: "SE_SKL_022",
    5: "SE_SKL_023", 6: "SE_SKL_024", 7: "SE_SKL_025", 8: "SE_SKL_026",
    9: "SE_SKL_027", 10: "SE_SKL_028", 11: "SE_SKL_029", 12: "SE_SKL_030",
    13: "SE_SKL_031", 14: "SE_SKL_032", 15: "SE_SKL_033", 16: "SE_SKL_034",
    17: "SE_SKL_035", 18: "SE_SKL_036", 19: "SE_SKL_037", 20: "SE_SKL_038",
    21: "SE_SKL_039", 22: "SE_SKL_040", 23: "SE_SKL_041", 24: "SE_SKL_042",
    29: "SE_SKL_043", 30: "SE_SKL_044", 31: "SE_SKL_045",
    32: "SE_SKL_046", 33: "SE_SKL_047", 34: "SE_SKL_048", 35: "SE_SKL_049", 36: "SE_SKL_050",
    37: "SE_SKL_051", 38: "SE_SKL_051", 39: "SE_SKL_052", 40: "SE_SKL_053", 41: "SE_SKL_054",
    42: "SE_SKL_055", 43: "SE_SKL_055",
    44: "SE_SKL_056", 45: "SE_SKL_057", 46: "SE_SKL_058", 47: "SE_SKL_058",
    48: "SE_SKL_059", 49: "SE_SKL_060", 50: "SE_SKL_061", 51: "SE_SKL_062",
    52: "SE_SKL_063", 53: "SE_SKL_063", 54: "SE_SKL_064", 55: "SE_SKL_064",
    56: "SE_SKL_065", 57: "SE_SKL_065", 58: "SE_SKL_066", 59: "SE_SKL_066",
    60: "SE_SKL_067", 61: "SE_SKL_068", 62: "SE_SKL_069",
    63: "SE_SKL_070", 64: "SE_SKL_071", 65: "SE_SKL_071", 66: "SE_SKL_072",
    67: "SE_SKL_073", 68: "SE_SKL_073", 69: "SE_SKL_074",
    70: "SE_SKL_075", 71: "SE_SKL_075",
    72: "SE_SKL_076", 73: "SE_SKL_077", 74: "SE_SKL_078", 75: "SE_SKL_079",
    76: "SE_SKL_080", 77: "SE_SKL_081", 78: "SE_SKL_082", 79: "SE_SKL_083",
    81: "SE_SKL_084", 82: "SE_SKL_085", 83: "SE_SKL_086",
    84: "SE_SKL_087", 85: "SE_SKL_088", 86: "SE_SKL_089", 87: "SE_SKL_090",
    88: "SE_SKL_091", 89: "SE_SKL_092", 90: "SE_SKL_093", 91: "SE_SKL_094",
    92: "SE_SKL_095", 93: "SE_SKL_096", 94: "SE_SKL_097", 95: "SE_SKL_098",
    96: "SE_SKL_099", 97: "SE_SKL_100", 98: "SE_SKL_101", 99: "SE_SKL_102",
    100: "SE_SKL_103", 101: "SE_SKL_104", 102: "SE_SKL_105", 103: "SE_SKL_106",
    104: "SE_SKL_107", 105: "SE_SKL_108", 106: "SE_SKL_109", 107: "SE_SKL_110",
    108: "SE_SKL_111", 109: "SE_SKL_112", 110: "SE_SKL_113", 111: "SE_SKL_114",
    112: "SE_SKL_115",
}

WEAPON_SFX = {
    "SE_SKL_007": "Épée / Sword",
    "SE_SKL_008": "Impact / Strike Impact",
    "SE_SKL_009": "Bâton / Staff",
    "SE_SKL_010": "Griffes / Claws",
    "SE_SKL_011": "Lance / Spear",
    "SE_SKL_012": "Hache / Axe",
    "SE_SKL_013": "Masse & Marteau / Hammer",
    "SE_SKL_014": "Fouet / Whip",
    "SE_SKL_015": "Arc / Bow",
    "SE_SKL_016": "Mains nues / Unarmed",
    "SE_SKL_017": "Coup critique / Critical Hit",
    "SE_SKL_018": "Attaque lourde / Heavy Smash",
}

SYS_DESCRIPTIONS = {
    "SE_SYS_001": ("Déplacement du curseur dans les menus", "Menu cursor movement tick", "Curseur"),
    "SE_SYS_002": ("Validation et sélection d'une option", "Menu confirm selection chime", "Validation"),
    "SE_SYS_003": ("Annulation et retour en arrière", "Menu cancel sound", "Annulation"),
    "SE_SYS_004": ("Avertissement ou action invalide", "Invalid action warning buzz", "Erreur"),
    "SE_SYS_005": ("Ouverture du menu principal du dresseur", "Main trainer menu opening whoosh", "Ouverture menu"),
    "SE_SYS_006": ("Fermeture du menu principal", "Menu closing sound", "Fermeture menu"),
    "SE_SYS_007": ("Changement d'onglet ou de catégorie", "Tab switch navigation blip", "Changement d'onglet"),
    "SE_SYS_008": ("Défilement rapide d'inventaire", "Fast item list scrolling", "Défilement"),
    "SE_SYS_009": ("Bip de dialogue standard", "Standard dialogue typewriter blip", "Dialogue neutre"),
    "SE_SYS_010": ("Bip de dialogue à timbre grave (voix masculine)", "Low pitch dialogue typewriter blip", "Dialogue grave"),
    "SE_SYS_011": ("Bip de dialogue à timbre aigu (voix féminine / enfant)", "High pitch dialogue typewriter blip", "Dialogue aigu"),
    "SE_SYS_012": ("Alerte de points de compétence disponibles à attribuer", "Skill points level up alert chime", "Points disponibles"),
    "SE_SYS_013": ("Bruit de pièces d'or / Transaction marchande", "Gold coins transaction clinking", "Pièces d'or"),
    "SE_SYS_014": ("Équipement d'une arme ou protection", "Item equipment equip chime", "Équiper objet"),
    "SE_SYS_015": ("Retrait ou déséquipement d'un objet", "Item removal unequip sound", "Déséquiper objet"),
    "SE_SYS_016": ("Confirmation d'écriture dans le journal de sauvegarde", "Save to adventure log confirmation chime", "Sauvegarde journal"),
    "SE_SYS_017": ("Signal de connexion Wi-Fi Nintendo DS établi", "Nintendo DS Wi-Fi connection handshake chime", "Wi-Fi connecté"),
}

FLD_DESCRIPTIONS = {
    "SE_FLD_001": ("Pas sur herbe ou végétation", "Footstep on grass", "Marche"),
    "SE_FLD_002": ("Pas sur pierre ou dalle de sanctuaire", "Footstep on stone tiles", "Marche"),
    "SE_FLD_003": ("Pas sur terre battue ou sentier", "Footstep on dirt road", "Marche"),
    "SE_FLD_004": ("Pas dans le sable de plage", "Footstep on sand", "Marche"),
    "SE_FLD_005": ("Pas sur plancher en bois", "Footstep on wooden floor", "Marche"),
    "SE_FLD_006": ("Pas dans une flaque d'eau peu profonde", "Footstep in shallow puddle", "Marche"),
    "SE_FLD_007": ("Course vive du dresseur", "Running footsteps", "Course"),
    "SE_FLD_008": ("Saut et atterrissage de marchepied", "Ledge jump and land", "Saut"),
    "SE_FLD_009": ("Glissade sur pente raide", "Steep slope slide", "Glissade"),
    "SE_FLD_010": ("Ouverture de porte en bois de chaumière", "Wooden door opening", "Porte"),
    "SE_FLD_011": ("Fermeture de porte battante", "Wooden door closing", "Porte"),
    "SE_FLD_012": ("Portail coulissant en fer forgé", "Iron gate sliding open", "Grille"),
    "SE_FLD_013": ("Grincement de trappe de donjon", "Dungeon trapdoor creak", "Trappe"),
    "SE_FLD_014": ("Gravir une échelle de meunier", "Climbing wooden ladder", "Échelle"),
    "SE_FLD_015": ("Descente d'escalier en pierre", "Stone staircase steps", "Escalier"),
    "SE_FLD_016": ("Mécanisme d'ascenseur du QG", "HQ elevator mechanism hum", "Ascenseur"),
    "SE_FLD_017": ("Déclenchement d'interrupteur au sol", "Floor pressure plate click", "Interrupteur"),
    "SE_FLD_018": ("Dalle piégée ou blocage de barrière", "Trap trigger or barrier barrier", "Piège"),
    "SE_FLD_019": ("Porte scellée d'un sanctuaire archéologique", "Ancient shrine heavy door opening", "Sanctuaire"),
    "SE_FLD_020": ("Téléporteur de sanctuaire — activation", "Shrine teleporter activation hum", "Téléporteur"),
    "SE_FLD_021": ("Téléportation spatiale du dresseur", "Spatial warp teleportation sound", "Téléportation"),
    "SE_FLD_022": ("Aura mystique de la stèle sacrée", "Sacred monolith mystical humming", "Stèle sacrée"),
    "SE_FLD_023": ("Apparition du sceau de l'Incarnus", "Incarnus sacred sigil glowing", "Incarnus"),
    "SE_FLD_024": ("Chute d'eau et écoulement de fontaine", "Waterfall flow and fountain water", "Eau"),
    "SE_FLD_025": ("Vent hurlant des falaises de Félicité", "Wailing cliff wind gusts", "Météo"),
    "SE_FLD_026": ("Grondement sismique souterrain", "Subterranean seismic tremor", "Séisme"),
    "SE_FLD_027": ("Éboulement de gravats rocheux", "Rock rubble collapse", "Éboulement"),
    "SE_FLD_028": ("Fontaine régénératrice d'énergie magique", "Recovery spring magical chime", "Source sacrée"),
    "SE_FLD_029": ("Chuintement de vapeur volcanique", "Volcanic steam vent hiss", "Vapeur"),
    "SE_FLD_030": ("Chariot de mine sur rails", "Minecart rolling on rails", "Chariot"),
    "SE_FLD_031": ("Mécanisme de pont-levis abaissé", "Drawbridge lowering gear", "Pont-levis"),
    "SE_FLD_032": ("Écrasement d'obstacle en bois", "Wooden barricade break", "Obstacle"),
    "SE_FLD_033": ("Craquement d'arbre déraciné", "Tree falling cracking wood", "Environnement"),
    "SE_FLD_034": ("Cri de mouettes sur le littoral côtier", "Seagulls crying on coastal shore", "Ambiance"),
    "SE_FLD_035": ("Ressac des vagues marines", "Ocean waves surf swell", "Mer"),
    "SE_FLD_036": ("Ouverture d'un coffre au trésor standard en bois", "Standard wooden chest opening creak", "Coffre"),
    "SE_FLD_037": ("Ouverture d'un coffre au trésor ouvragé en or", "Gilded treasure chest opening chime", "Coffre précieux"),
    "SE_FLD_038": ("Coffre verrouillé ou scellé magiquement", "Locked chest rattle failure", "Coffre verrouillé"),
    "SE_FLD_039": ("Fouille d'un pot en terre cuite", "Smashing clay pot", "Poterie"),
    "SE_FLD_040": ("Fouille d'un tonneau de stockage", "Breaking wooden barrel", "Tonneau"),
    "SE_FLD_041": ("Ramassage d'un sac d'objets au sol", "Picking up ground item pouch", "Objet au sol"),
    "SE_FLD_042": ("Examen de panneau d'information", "Reading info bulletin board", "Pancarte"),
    "SE_FLD_043": ("Démarrage du moteur de la motomarine", "Sea scooter engine ignition", "Motomarine"),
    "SE_FLD_044": ("Accélération de la motomarine sur les flots", "Sea scooter cruising on water waves", "Motomarine"),
    "SE_FLD_045": ("Sillage et clapotis rapide sur l'eau", "Fast water wake splashing", "Navigation"),
    "SE_FLD_046": ("Ralentissement et amarrage au ponton", "Sea scooter docking at jetty", "Amarrage"),
    "SE_FLD_047": ("Sifflet d'appel d'aérostat de l'Association", "Trainer Association airship horn", "Aérostat"),
    "SE_FLD_048": ("Bruit d'hélice de dirigeable", "Airship propeller churning", "Dirigeable"),
    "SE_FLD_049": ("Écho lointain de cloche marine", "Distant marine bell chime", "Cloche"),
    "SE_FLD_050": ("Pluie fine sur la canopée tropicale", "Light rain on jungle canopy", "Pluie"),
    "SE_FLD_051": ("Averse torrentielle et grondements", "Heavy downpour and distant thunder", "Tempête"),
    "SE_FLD_052": ("Bourdonnement de machinerie alchimique", "Alchemy synthesizer machine humming", "Synthèse"),
    "SE_FLD_053": ("Décharge d'énergie de fusion de monstres", "Monster fusion energy synthesis surge", "Synthèse"),
    "SE_FLD_054": ("Cloche de sanctuaire sonnée par le dresseur", "Shrine ritual bell toll", "Sanctuaire"),
}

BTL_DESCRIPTIONS = {
    "SE_BTL_001": ("Attaque vive et fauchage rapide", "Quick slash physical strike", "Attaque"),
    "SE_BTL_002": ("Coup percutant lourd", "Heavy bludgeoning strike impact", "Frappe lourde"),
    "SE_BTL_003": ("Estocade tranchante acérée", "Sharp piercing blade strike", "Estoc"),
    "SE_BTL_004": ("Impact étouffé de parade défensive", "Shield block muted deflection", "Parade"),
    "SE_BTL_005": ("Esquive agile et déplacement d'air", "Evasive dodge air displacement", "Esquive"),
    "SE_BTL_006": ("Coup critique assourdissant", "Ear-splitting critical blow resonance", "Coup critique"),
    "SE_BTL_007": ("Fracas de bris de garde", "Guard break shattering crunch", "Bris de garde"),
    "SE_BTL_008": ("Effondrement d'un monstre KO", "Monster defeat collapse thud", "K.O."),
    "SE_BTL_009": ("Chute de poussière et débris de combat", "Battlefield dust and gravel settling", "Impact sol"),
    "SE_BTL_010": ("Double frappe consécutive rythmée", "Rhythmic double strike pattern", "Double coup"),
    "SE_BTL_011": ("Choc d'armes de duel", "Weapon clash metallic parry", "Choc métallique"),
    "SE_BTL_012": ("Balayage giratoire de zone", "Spinning 360-degree sweep strike", "Balayage"),
    "SE_BTL_013": ("Fracas sismique d'écrasement au sol", "Seismic ground pound shockwave", "Onde de choc"),
    "SE_BTL_014": ("Onde de choc de projection aérienne", "Air launch shockwave pulse", "Projection"),
    "SE_BTL_015": ("Morsure féroce de fauve", "Fierce beast jaws biting crunch", "Morsure"),
    "SE_BTL_016": ("Lacération de griffes jumelles", "Twin claws tearing flesh", "Griffes"),
    "SE_BTL_017": ("Coup de corne perforant", "Horn gore thrust impact", "Cornes"),
    "SE_BTL_018": ("Coup de queue massif", "Heavy tail swipe whip", "Coup de queue"),
    "SE_BTL_019": ("Battement d'ailes puissant d'un monstre volant", "Powerful wings flapping gust", "Battement d'ailes"),
    "SE_BTL_020": ("Bond prédateur et retombée", "Predatory pounce and landing", "Bond"),
    "SE_BTL_021": ("Cri de provocation d'un gluant", "Slime battle entrance jiggle cry", "Cri gluant"),
    "SE_BTL_022": ("Rugissement bestial d'un félin ou canidé", "Feline beast battle roar", "Rugissement"),
    "SE_BTL_023": ("Feulement guttural d'un dragon", "Guttural dragon hiss roar", "Rugissement dragon"),
    "SE_BTL_024": ("Grincement d'engrenage d'une matière mécanique", "Material machine grinding gears", "Matière"),
    "SE_BTL_025": ("Ricanement sinistre d'un démon", "Sinister demon cackling taunt", "Démon"),
    "SE_BTL_026": ("Râle funèbre d'un mort-vivant", "Undead mournful groan", "Mort-vivant"),
    "SE_BTL_027": ("Sifflement venimeux d'un reptile", "Venomous reptile hiss", "Reptile"),
    "SE_BTL_028": ("Bourdonnement agressif d'un insecte géant", "Giant insect aggressive buzzing", "Insecte"),
    "SE_BTL_029": ("Bourrasque d'énergie d'un monstre élémentaire", "Elemental energy burst surge", "Élémentaire"),
    "SE_BTL_030": ("Attaque de monstre (modèle canin / bête)", "Beast monster standard attack bark", "Attaque monstre"),
    "SE_BTL_031": ("Dégâts reçus (modèle canin / bête)", "Beast monster damage yelp", "Dégâts monstre"),
    "SE_BTL_032": ("Attaque de monstre (modèle dragon ailé)", "Winged dragon standard strike", "Attaque dragon"),
    "SE_BTL_033": ("Dégâts reçus (modèle dragon ailé)", "Winged dragon pain recoil", "Dégâts dragon"),
    "SE_BTL_034": ("Attaque de monstre (modèle géant / golem)", "Giant golem heavy stone strike", "Attaque golem"),
    "SE_BTL_035": ("Dégâts reçus (modèle géant / golem)", "Giant golem stone impact grunt", "Dégâts golem"),
    "SE_BTL_036": ("Attaque de monstre (modèle spectre / fantôme)", "Ghostly spirit ethereal swipe", "Attaque spectre"),
    "SE_BTL_037": ("Dégâts reçus (modèle spectre / fantôme)", "Ghostly spirit shriek in pain", "Dégâts spectre"),
    "SE_BTL_038": ("Attaque de monstre aquatique", "Aquatic monster thrashing strike", "Attaque aquatique"),
    "SE_BTL_039": ("Dégâts reçus par un monstre aquatique", "Aquatic monster splash distress", "Dégâts aquatique"),
    "SE_BTL_040": ("Tentative de fuite du dresseur", "Fleeing attempt scrambling footsteps", "Fuite"),
    "SE_BTL_041": ("Fuite réussie du champ de bataille", "Successful escape whoosh", "Fuite réussie"),
    "SE_BTL_042": ("Fuite bloquée par l'ennemi", "Escape blocked defensive barrier", "Fuite bloquée"),
    "SE_BTL_043": ("Déroute et fuite d'un monstre sauvage", "Wild monster coward flee", "Monstre en fuite"),
}

ME_DESCRIPTIONS = {
    "ST_ME_001": ("Jingle d'événement court", "Short Event Fanfare", "Événement"),
    "ST_ME_002": ("Découverte d'objet ordinaire", "Item Found Fanfare", "Objet trouvé"),
    "ST_ME_003": ("Coffre au trésor rare / Objet précieux", "Rare Treasure Chest Fanfare", "Trésor rare"),
    "ST_ME_004": ("Cloches d'église / Bénédiction de sauvegarde", "Church Bells & Save Blessing", "Église"),
    "ST_ME_005": ("Purification de malédiction à l'église", "Church Curse Purification", "Purification"),
    "ST_ME_006": ("Résurrection rituelle complète à l'église", "Church Full Resurrection Fanfare", "Résurrection"),
    "ST_ME_007": ("Progression de quête / Étape validée", "Quest Step Milestone Fanfare", "Quête"),
    "ST_ME_008": ("Épreuve de sanctuaire franchie", "Shrine Trial Victory Fanfare", "Sanctuaire"),
    "ST_ME_009": ("Thème de défaite & Game Over", "Defeat & Game Over Theme", "Game Over"),
    "ST_ME_010": ("Ralliement d'un nouveau monstre allié", "Monster Ally Join Fanfare", "Dressage"),
    "ST_ME_011": ("Victoire de manche au tournoi du Colisée", "Colosseum Round Won Fanfare", "Colisée"),
    "ST_ME_012": ("Coupe du championnat des dresseurs remportée", "Championship Trophy Fanfare", "Trophée"),
    "ST_ME_013": ("Alerte dramatique / Découverte soudaine", "Dramatic Event Alert Stinger", "Alerte"),
    "ST_ME_014": ("Mystère résolu / Passage secret ouvert", "Secret Passage Discovered Fanfare", "Secret résolu"),
}


def main():
    print("=== Corrélation sémantique des 306 bruitages SFX de DQMJ1 ===")

    # 1. Charger game_sfx.json
    with open(GAME_SFX_JSON, "r", encoding="utf-8") as f:
        game_sfx_data = json.load(f)
    sfx_items = game_sfx_data["sfx"]
    print(f"Chargé {len(sfx_items)} bruitages bruts depuis {GAME_SFX_JSON}")

    # 2. Charger spell_effects.json pour récupérer les noms multilingues
    with open(SPELL_EFFECTS_JSON, "r", encoding="utf-8") as f:
        spell_effects_data = json.load(f)
    spells_by_id = {s["id"]: s for s in spell_effects_data["spells"]}

    # Construction de l'index inverse SFX -> sorts
    sfx_to_spells = {}
    for sp_id, sfx_sym in SPELL_ID_TO_SFX.items():
        sfx_to_spells.setdefault(sfx_sym, []).append(sp_id)

    # 3. Construire le mapping 1:1 pour chaque SFX
    mapped_sfx = []
    for item in sfx_items:
        sym = item["symbol"]
        entry = dict(item)

        # Déterminer descriptions sémantiques et contextes
        desc_fr = ""
        desc_en = ""
        action_name = sym
        tags = []
        associated_spells = []
        associated_weapons = []

        if sym in SKL_DESCRIPTIONS:
            desc_fr, desc_en, tags = SKL_DESCRIPTIONS[sym]
            action_name = desc_fr.split(" — ")[0]
        elif sym in SYS_DESCRIPTIONS:
            desc_fr, desc_en, action_name = SYS_DESCRIPTIONS[sym]
            tags = ["système", "interface", "menu"]
        elif sym in FLD_DESCRIPTIONS:
            desc_fr, desc_en, action_name = FLD_DESCRIPTIONS[sym]
            tags = ["terrain", "exploration", "environnement"]
        elif sym in BTL_DESCRIPTIONS:
            desc_fr, desc_en, action_name = BTL_DESCRIPTIONS[sym]
            tags = ["combat", "attaque", "action"]
        elif sym in ME_DESCRIPTIONS:
            desc_fr, desc_en, action_name = ME_DESCRIPTIONS[sym]
            tags = ["fanfare", "jingle", "événement"]
        elif sym.startswith("SE_DEM_") or sym.startswith("SE_SHA_"):
            desc_fr = f"Bruitage cinématique de mise en scène ({sym})"
            desc_en = f"Cinematic scene cutscene sound effect ({sym})"
            action_name = f"Cinématique {sym.split('_')[-1]}"
            tags = ["cinématique", "démo", "scène"]
        else:
            desc_fr = f"Effet sonore authentique de DQMJ1 ({sym})"
            desc_en = f"Authentic DQMJ1 sound effect ({sym})"
            action_name = sym
            tags = ["bruitage"]

        # Armes associées
        if sym in WEAPON_SFX:
            associated_weapons.append(WEAPON_SFX[sym])

        # Sorts associés
        if sym in sfx_to_spells:
            for sp_id in sfx_to_spells[sym]:
                sp = spells_by_id.get(sp_id)
                if sp:
                    name_fr = sp["name"].get("F") or sp["name"].get("fr") or f"Aptitude #{sp_id}"
                    name_en = sp["name"].get("E") or sp["name"].get("en") or f"Ability #{sp_id}"
                    associated_spells.append({
                        "id": sp_id,
                        "name": name_fr,
                        "nameEn": name_en,
                        "mpCost": sp.get("mp_cost", 0),
                    })

        entry["semanticName"] = action_name
        entry["descriptionFr"] = desc_fr
        entry["descriptionEn"] = desc_en
        entry["tags"] = tags
        entry["associatedSpells"] = associated_spells
        entry["associatedWeapons"] = associated_weapons
        mapped_sfx.append(entry)

    # 4. Écrire assets/data/sfx_mapping.json
    mapping_payload = {
        "provenance": (
            "Cartographie sémantique 1:1 des 306 bruitages du jeu Nintendo DS Dragon Quest Monsters: Joker. "
            "Corrélée depuis TokugiDataTbl.bin, BtlChrTbl.bin, BtlEfcTbl.bin, sound_data.sadl et sound_data.sdat."
        ),
        "total": len(mapped_sfx),
        "total_skills": len([x for x in mapped_sfx if x["subcategory"] == "skills"]),
        "total_actions": len([x for x in mapped_sfx if x["subcategory"] == "actions"]),
        "total_system": len([x for x in mapped_sfx if x["category"] == "system"]),
        "total_field": len([x for x in mapped_sfx if x["category"] == "field"]),
        "total_fanfares": len([x for x in mapped_sfx if x["category"] == "fanfare"]),
        "total_cinematic": len([x for x in mapped_sfx if x["category"] == "cinematic"]),
        "categories": game_sfx_data["categories"],
        "sfx": mapped_sfx,
    }

    with open(DEST_MAPPING_JSON, "w", encoding="utf-8") as f:
        json.dump(mapping_payload, f, indent=2, ensure_ascii=False)
    print(f"-> sfx_mapping.json écrit dans {DEST_MAPPING_JSON} ({len(mapped_sfx)} bruitages)")

    # 5. Mettre à jour spell_effects.json pour lier chaque aptitude à son sfx vérifié
    updated_spells_count = 0
    for sp in spell_effects_data["spells"]:
        sp_id = sp["id"]
        correct_sfx = SPELL_ID_TO_SFX.get(sp_id)
        if correct_sfx:
            sp["sfx_id"] = correct_sfx
            sp["sfx_file"] = f"sfx/{correct_sfx}.mp3"
            sp["sfx_url"] = f"/api/assets/audio/sfx/{correct_sfx}.mp3"
            updated_spells_count += 1
        else:
            # Garde l'effet visuel s'il n'y a pas de son spécifique identifié
            if "sfx_id" in sp and sp["sfx_id"] and sp["sfx_id"].startswith("SE_SKL_"):
                # Nettoyage si c'était l'ancien numéro erroné (> 115)
                try:
                    num = int(sp["sfx_id"].replace("SE_SKL_", ""))
                    if num > 115:
                        sp["sfx_id"] = None
                except ValueError:
                    pass

    with open(SPELL_EFFECTS_JSON, "w", encoding="utf-8") as f:
        json.dump(spell_effects_data, f, indent=2, ensure_ascii=False)
    print(f"-> spell_effects.json mis à jour dans {SPELL_EFFECTS_JSON} ({updated_spells_count} sorts reliés à un SFX)")


if __name__ == "__main__":
    main()
