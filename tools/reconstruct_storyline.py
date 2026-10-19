#!/usr/bin/env python3
"""Génère la chronologie scénaristique, les quêtes et les secrets narratifs de DQMJ1.

Exécute l'Axe 5.2 du Master Plan :
- Reconstitution en 5 actes de la trame narrative
- Liaison avec les cartes (map_names.json), les boss (fixed_battles.json),
  les personnages et les commentaires des développeurs de la ROM.

Produit :
- assets/data/story_timeline.json
"""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_RE = os.path.join(RACINE, "assets/data")
OUT_WEB = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire/assets/data")

ACTS = [
    {
        "id": "act_1",
        "act_number": 1,
        "title": {
            "fr": "Prologue : L'Infiltration de l'Albatros",
            "en": "Prologue: Infiltration of the Albatross",
            "de": "Prolog: Infiltration der Albatross",
            "it": "Prologo: L'infiltrazione dell'Albatross",
            "es": "Prólogo: La infiltración del Albatros",
        },
        "period": "Intro",
        "icon": "scroll",
        "summary": {
            "fr": "Emprisonné dans les cales de la prison flottante de l'Albatros, le jeune héros est convoqué par le Directeur Craps, chef suprême de l'organisation secrète de la Commission. Chargé d'une mission d'espionnage sous couverture au Tournoi des Dresseurs des Sept-Îles, il débarque sur l'Île des Apprentis pour choisir son premier monstre et recevoir sa bague de dresseur.",
            "en": "Imprisoned in the hold of the floating prison Albatross, the young hero is summoned by Warden Craps, supreme head of the secret Commission. Tasked with an undercover espionage mission at the Monster Scout Tournament in the Green Bays archipelago, he arrives on Infant Isle to choose his first monster and receive his scout ring.",
            "de": "Eingekerkert im Rumpf des Gefängnisschiffs Albatross wird der junge Held von Direktor Craps vorgeladen. Beauftragt mit einer verdeckten Spionagemission beim Monster-Scout-Turnier, landet er auf der Insel der Lehrlinge, um sein erstes Monster zu wählen.",
            "it": "Imprigionato nella stiva dell'Albatross, il giovane eroe viene convocato dal Direttore Craps. Incaricato di una missione segreta di spionaggio al Torneo, sbarca sull'Isola degli Apprendisti per scegliere il suo primo mostro.",
            "es": "Encarcelado en la bodega del Albatros, el joven héroe es convocado por el Director Craps. Encargado de una misión secreta de espionaje en el Torneo, desembarca en la Isla del Aprendiz para elegir a su primer monstruo.",
        },
        "chapters": [
            {
                "id": "ch_1_1",
                "title": {
                    "fr": "La Cellule et l'Ordre de Mission",
                    "en": "The Cell and the Mission Order",
                    "de": "Die Zelle und der Einsatzbefehl",
                    "it": "La cella e l'ordine di missione",
                    "es": "La celda y la orden de misión",
                },
                "synopsis": {
                    "fr": "Le héros démarre sa détention dans la cellule w000. Le garde annonce la convocation de Craps. Dans le bureau w001, Craps ordonne au héros de s'inscrire au championnat comme agent secret afin de surveiller les activités suspectes du Dr Rebelote.",
                    "en": "The hero starts in cell w000. The guard escorts him to Warden Craps in w001. Craps orders him to enter the championship under cover to investigate suspicious activities.",
                    "de": "Der Held beginnt in Zelle w000 und erhält in Büro w001 von Craps den Befehl, verdeckt am Turnier teilzunehmen.",
                    "it": "L'eroe inizia nella cella w000 e riceve nel bureau w001 l'ordine di partecipare sotto copertura al torneo.",
                    "es": "El héroe comienza en la celda w000 y recibe de Craps la orden de infiltrarse en el torneo.",
                },
                "maps": ["w000", "w001"],
                "characters": ["Craps (Directeur)", "Garde de la prison"],
                "dev_notes": ["アイテム取得メッセージを表示 (Affichage du message d'acquisition d'objet)", "優勝DEMOを再生 (Lecture cinématique champion)"],
                "unlocks": ["Anneau de dresseur", "Journal de quête"],
            },
            {
                "id": "ch_1_2",
                "title": {
                    "fr": "L'Arrivée sur l'Île des Apprentis",
                    "en": "Arrival on Infant Isle",
                    "de": "Ankunft auf der Insel der Lehrlinge",
                    "it": "Arrivo sull'Isola degli Apprendisti",
                    "es": "Llegada a la Isla del Aprendiz",
                },
                "synopsis": {
                    "fr": "Débarquement en radeau sur l'Île des Apprentis (f000). Au sommet de la colline, le héros rencontre le Dr Belote et choisit son monstre de départ parmi Smilodon, Vampivol ou Tronc-binocle, avant de passer l'épreuve de qualification.",
                    "en": "Landing on Infant Isle (f000). At the hilltop, the hero meets Dr Snap and chooses his starter monster among Mischievous Mole, Platypunk, or Capsichum before the qualification trial.",
                    "de": "Landung auf der Insel der Lehrlinge (f000). Auswahl des Startermonsters und Ablegen der Qualifikationsprüfung.",
                    "it": "Sbarco sull'Isola degli Apprendisti (f000), scelta del mostro iniziale e superamento della prova.",
                    "es": "Llegada a la Isla del Aprendiz (f000), elección del monstruo inicial y superación de la prueba.",
                },
                "maps": ["f000"],
                "characters": ["Dr Belote", "Locataires de l'île"],
                "dev_notes": ["msg = 0 の敵配置 (Placement des monstres sauvages introductifs)"],
                "unlocks": ["Premier monstre de combat", "Accès à l'hydravion vers Apprenti et Fert"],
            },
        ],
    },
    {
        "id": "act_2",
        "act_number": 2,
        "title": {
            "fr": "L'Éveil de l'Incarnus et les Sanctuaires Sacrés",
            "en": "Awakening of the Incarnus & Sacred Shrines",
            "de": "Erwachen des Inkarnus & Die Heiligen Schreine",
            "it": "Il Risveglio dell'Incarnus e i Santuari Sacri",
            "es": "El Despertar del Incarnus y los Santuarios Sagrados",
        },
        "period": "Chapitre 1",
        "icon": "shield",
        "summary": {
            "fr": "Au cœur du temple scellé de l'Île des Apprentis, le héros découvre une créature mystique blessée : l'Incarnus. Lié par le destin, l'animal sacré s'éveille sous la forme d'un jeune Wulfspade (Apik). Pour accomplir sa destinée et purifier les îles des ténèbres naissantes, l'Incarnus doit voyager à travers les sanctuaires de Fert, Pandémonia, Xéroph et Célestia afin d'acquérir ses formes sacrées (Diamagon, Cluboon, Hawkhart).",
            "en": "Deep inside the sealed shrine of Infant Isle, the hero discovers a wounded mystical creature: the Incarnus. Bound by destiny, the sacred beast awakens as young Wulfspade. To fulfill its divine purpose, it must journey to the elemental shrines across Xeroph, Palaish, Celeste and Infern to unlock its forms: Hawkhart, Cluboon, and Diamagon.",
            "de": "Im Schrein der Lehrlingsinsel erwacht das heilige Tier: der Inkarnus in Gestalt des Wulfspade. Durch das Durchqueren der Schreine erlangt er seine göttlichen Verwandlungen.",
            "it": "Nel santuario dell'Isola degli Apprendisti si risveglia l'Incarnus. Attraverso i quattro santuari dell'arcipelago acquisisce le sue quattro forme elementali.",
            "es": "En el santuario de la Isla del Aprendiz despierta el Incarnus. Al superar los santuariossagrados, adquiere sus cuatro formas sagradas.",
        },
        "chapters": [
            {
                "id": "ch_2_1",
                "title": {
                    "fr": "Le Miroir de l'Autel et la Première Métamorphose",
                    "en": "The Altar Mirror and First Metamorphosis",
                    "de": "Der Altarspiegel und die Erste Metamorphose",
                    "it": "Lo Specchio dell'Altare e la Prima Metamorfosi",
                    "es": "El Espejo del Altar y la Primera Metamorfosis",
                },
                "synopsis": {
                    "fr": "Exploration du premier sanctuaire d011 et de la chambre du miroir s001. L'Incarnus se regarde dans le miroir sacré et acquiert sa première évolution majeure. Réception de la plaque sacrée.",
                    "en": "Exploring shrine d011 and mirror room s001. The Incarnus looks into the sacred mirror and gains its first major evolution, receiving the sacred tablet.",
                    "de": "Erkundung von Schrein d011 und Spiegelkammer s001. Erste Verwandlung des Inkarnus.",
                    "it": "Esplorazione del santuario d011 e prima metamorfosi dell'Incarnus.",
                    "es": "Exploración del santuario d011 y primera metamorfosis del Incarnus.",
                },
                "maps": ["s001", "d011", "d012", "h001"],
                "characters": ["Incarnus (Apik)", "Gardien du Temple"],
                "dev_notes": ["祠クリア判定：1stクリア (Contrôle validation premier sanctuaire)", "神獣タイプ：子供 (Type Incarnus enfant)"],
                "unlocks": ["Forme Apik avancée", "Plaque sacrée de Fert"],
            },
            {
                "id": "ch_2_2",
                "title": {
                    "fr": "Les Épreuves des Quatre Éléments",
                    "en": "The Four Elemental Trials",
                    "de": "Die Prüfungen der Vier Elemente",
                    "it": "Le Prove dei Quattro Elementi",
                    "es": "Las Pruebas de los Cuatro Elementos",
                },
                "synopsis": {
                    "fr": "Voyage à travers les sanctuaires de Pandémonia (d021-d022), Xéroph (d031-d034) et Célestia (d041-d046). L'Incarnus débloque successivement Diamagon (eau/soins), Cluboon (terre/force) et Hawkhart (vent/foudre).",
                    "en": "Traveling through shrines on Palaish, Xeroph and Celeste. Incarnus unlocks Diamagon, Cluboon and Hawkhart forms.",
                    "de": "Reise durch die Schreine von Palaish, Xeroph und Celeste. Der Inkarnus meistert alle vier Formen.",
                    "it": "Viaggio attraverso i santuari di Palaish, Xeroph e Celeste.",
                    "es": "Viaje por los santuarios de las islas intermedias y obtención de todas las formas.",
                },
                "maps": ["d021", "d022", "d031", "d032", "d041", "d042", "s011", "s021", "s031"],
                "characters": ["Incarnus (4 formes)", "Solitaire", "Shuffles"],
                "dev_notes": ["祠クリア判定：2ndクリア", "祠クリア判定：3rdクリア", "祠クリア判定：4thクリア"],
                "unlocks": ["Synthèse de l'Incarnus", "Accès à toutes les îles de l'archipel"],
            },
        ],
    },
    {
        "id": "act_3",
        "act_number": 3,
        "title": {
            "fr": "Le Championnat des Dresseurs et les Rivaux",
            "en": "Monster Scout Tournament & The Rivals",
            "de": "Das Monster-Scout-Turnier und die Rivalen",
            "it": "Il Torneo dei Dresseur e i Rivali",
            "es": "El Torneo de Reclutadores y los Rivales",
        },
        "period": "Chapitre 2",
        "icon": "trophy",
        "summary": {
            "fr": "Parallèlement à la quête divine, le héros gravit les échelons du tournoi officiel. Sur chaque île, il affronte les dresseurs itinérants et croise le fer avec ses rivaux : Solitaire, l'arrogante dresseuse au grand cœur, Shuffles l'illusionniste et Bob A' Job l'opportuniste. Réunissant les 10 marques des sanctuaires, il se qualifie pour les phases finales au Colisée de Palatopia.",
            "en": "Alongside the divine quest, the hero climbs tournament ranks. Across each island, he clashes with wandering scouts and iconic rivals: Solitaire, Shuffles, and Bob A' Job. Collecting 10 shrine marks, he qualifies for the finals at the Palaish Coliseum.",
            "de": "Parallel zur Schreinqueste steigt der Held im Turnier auf, bezwingt rivalisierende Dresseure wie Solitaire und qualifiziert sich für die Finalrunden.",
            "it": "Il giovane eroe scala le classifiche del torneo affrontando i rivali Solitaire, Shuffles e Bob A' Job.",
            "es": "El héroe compite en el campeonato enfrentando a sus rivales y clasificándose para la gran final.",
        },
        "chapters": [
            {
                "id": "ch_3_1",
                "title": {
                    "fr": "Les Épreuves des Îles et les Rencontres de Rivaux",
                    "en": "Island Trials & Rival Encounters",
                    "de": "Inselprüfungen & Rivalen-Begegnungen",
                    "it": "Prove delle Isole e Incontri dei Rivali",
                    "es": "Pruebas de las Islas y Encuentros con Rivales",
                },
                "synopsis": {
                    "fr": "Exploration des terres sauvages de Fert (f010), des cratères volcaniques de Pandémonia (f020), du désert de Xéroph (f030) et des hauteurs jumelles de Célestia (f040). Duels contre Solitaire et son fidèle Golem.",
                    "en": "Exploration of Fert, Palaish, Xeroph and Celeste. Scouting powerful monsters and confronting Solitaire and her Golem.",
                    "de": "Erkundung der Inseln und Duelle gegen Solitaire und andere Dresseure.",
                    "it": "Esplorazione delle isole e sfide contro Solitaire.",
                    "es": "Exploración de las islas y combates contra Solitaire.",
                },
                "maps": ["f010", "f020", "f030", "f040", "f050"],
                "characters": ["Solitaire", "Shuffles", "Bob A' Job", "Croupier"],
                "dev_notes": ["交換マスター配置判定 (Vérification des maîtres de troc)", "ランダム宝箱：A, B, C"],
                "unlocks": ["Boutiques avancées", "Synthèse sans restriction"],
            },
            {
                "id": "ch_3_2",
                "title": {
                    "fr": "Les Phases Finales du Colisée de Palatopia",
                    "en": "The Finals at Palaish Coliseum",
                    "de": "Die Finalrunden im Kolosseum von Palatopia",
                    "it": "Le Fasi Finali al Colosseo di Palatopia",
                    "es": "Las Fases Finales en el Coliseo de Palatopia",
                },
                "synopsis": {
                    "fr": "Dans l'arène w002 et le colisée w003, le héros triomphe tour après tour des 5 rondes éliminatoires. Il bat son ultime rival en finale et est sacré Grand Champion des Dresseurs.",
                    "en": "In arena w002 and coliseum w003, the hero overcomes all 5 tournament rounds, defeating his final rival to be crowned Champion.",
                    "de": "Im Kolosseum w003 gewinnt der Held alle 5 Runden und wird zum Champion gekrönt.",
                    "it": "Nel Colosseo w003 il protagonista supera i 5 turni e conquista il titolo di Campione.",
                    "es": "En el coliseo w003, el protagonista vence en las 5 rondas y se proclama Campeón.",
                },
                "maps": ["w002", "w003"],
                "characters": ["Directeur Craps", "Solitaire", "Arbitre du Colisée"],
                "dev_notes": [
                    "1回戦基本処理を読み込み (Chargement Round 1)",
                    "2回戦基本処理を読み込み (Chargement Round 2)",
                    "3回戦基本処理を読み込み (Chargement Round 3)",
                    "4回戦基本処理を読み込み (Chargement Round 4)",
                    "5回戦基本処理を読み込み (Chargement Round 5)",
                    "優勝DEMOを再生 (Lecture cinématique victoire)"
                ],
                "unlocks": ["Titre de Champion", "Accès à la cérémonie officielle"],
            },
        ],
    },
    {
        "id": "act_4",
        "act_number": 4,
        "title": {
            "fr": "La Conspiration de la Commission et le Dr Rebelote",
            "en": "Conspiracy of the Commission & Dr Snap",
            "de": "Die Verschwörung der Kommission & Dr. Snapped",
            "it": "La Cospirazione della Commissione e il Dr. Rebelote",
            "es": "La Conspiración de la Comisión y el Dr. Snap",
        },
        "period": "Climax",
        "icon": "skull",
        "summary": {
            "fr": "La cérémonie de remise des prix vire au cauchemar. Le Dr Rebelote révèle son plan diabolique : utiliser les pouvoirs de purification de l'Incarnus pour briser le sceau des Enfers et dominer le monde. Par une injection de matière ténébreuse, il corrompt l'Incarnus, le transformant en l'As de Pique, serviteur du néant. Le héros doit infiltrer le laboratoire secret k001 et les abysses de Tartare pour libérer son compagnon et affronter le Dr Rebelote fusionné.",
            "en": "The victory ceremony turns to tragedy. Dr Snap reveals his plot to corrupt the Incarnus into the Ace of Spades using dark matter. The hero pursues him into secret lab k001 and the depths of Infern Isle to purge the corruption and defeat Dr Snapped.",
            "de": "Dr. Snapped korrumpiert den Inkarnus zum Pik-As. Der Held dringt in das geheime Labor k001 vor und stellt Snapped im Tartarus zum Endkampf.",
            "it": "Il Dr. Rebelote corrompe l'Incarnus nell'Asso di Picche. L'eroe lo affronta nel laboratorio segreto e negli abissi di Infern Isle.",
            "es": "El Dr. Snap corrompe al Incarnus convirtiéndolo en el As de Picas. El héroe viaja al laboratorio secreto para derrotar al Dr. Snap fusionado.",
        },
        "chapters": [
            {
                "id": "ch_4_1",
                "title": {
                    "fr": "La Chute dans les Ténèbres : L'As de Pique",
                    "en": "Fall into Darkness: The Ace of Spades",
                    "de": "Absturz in die Finsternis: Pik-As",
                    "it": "Caduta nelle Tenebre: L'Asso di Picche",
                    "es": "Caída en las Tinieblas: El As de Picas",
                },
                "synopsis": {
                    "fr": "Le Dr Rebelote injecte les miasmes du Tartare dans l'Incarnus. Devenu l'As de Pique (m180b), l'animal sacré se retourne contre son maître. Solitaire et Craps prêtent main forte au héros pour pénétrer dans les installations secrètes de l'Île d'Inaccess.",
                    "en": "Dr Snap corrupts the Incarnus into Ace of Spades (m180b). Solitaire and Craps assist the hero to breach the secret laboratory.",
                    "de": "Verwandlung des Inkarnus in das bösartige Pik-As (m180b) und Infiltration des Geheimbunkers.",
                    "it": "L'Incarnus si trasforma nell'Asso di Picche (m180b). Infiltrazione del laboratorio segreto.",
                    "es": "Corrupción del Incarnus en As de Picas (m180b) e infiltración del búnker.",
                },
                "maps": ["k001", "k002", "k003", "f070"],
                "characters": ["Dr Rebelote", "As de Pique (m180b)", "Solitaire", "Directeur Craps"],
                "dev_notes": ["msg値 再セット (Réinitialisation des variables d'événement)", "ボス演出フラグ (Flag de mise en scène boss)"],
                "unlocks": ["Combat d'éveil de l'As de Pique", "Accès à l'île finale de Pandémonia Inférieure"],
            },
            {
                "id": "ch_4_2",
                "title": {
                    "fr": "L'Affrontement Final contre le Dr Rebelote Fusionné",
                    "en": "Final Confrontation with Dr Snapped",
                    "de": "Die Letzte Schlacht gegen Dr. Snapped",
                    "it": "Lo Scontro Finale con il Dr. Snapped",
                    "es": "El Enfrentamiento Final contra el Dr. Snapped",
                },
                "synopsis": {
                    "fr": "Dans le sanctuaire brisé f100, le Dr Rebelote absorbe la matière noire et mute en une abomination titanesque (Dr Rebelote Fusionné, PV 4065, niveau 40). Après un combat apocalyptique, l'Incarnus est purifié et rétablit l'équilibre de l'archipel.",
                    "en": "In ruined shrine f100, Dr Snap mutates into Dr Snapped (HP 4065, level 40). After an epic battle, Incarnus is purified, saving the world.",
                    "de": "Finaler Showdown gegen Dr. Snapped (LP 4065, Stufe 40). Reinigung des Inkarnus und Rettung der Welt.",
                    "it": "Scontro finale contro il Dr. Rebelote Fuso (PV 4065, livello 40). Purificazione dell'Incarnus.",
                    "es": "Batalla final contra el Dr. Snap Fusionado (PV 4065, nivel 40) y purificación del Incarnus.",
                },
                "maps": ["f100"],
                "characters": ["Dr Rebelote Fusionné (m210)", "Incarnus Céleste", "Solitaire"],
                "dev_notes": ["エンディングDEMOを再生 (Lecture cinématique de fin)", "祠クリア判定：全てクリア (Validation totale)"],
                "unlocks": ["Générique de fin", "Sauvegarde Post-Game"],
            },
        ],
    },
    {
        "id": "act_5",
        "act_number": 5,
        "title": {
            "fr": "L'Incarnus Céleste et les Secrets du Post-Game",
            "en": "The Celestial Incarnus & Post-Game Mysteries",
            "de": "Der Himmlische Inkarnus & Post-Game-Geheimnisse",
            "it": "L'Incarnus Celeste e i Misteri del Post-Game",
            "es": "El Incarnus Celestial y los Secretos del Post-Game",
        },
        "period": "Post-Game",
        "icon": "star",
        "summary": {
            "fr": "La paix revenue sur l'archipel ouvre l'accès aux plus grands défis du monde des monstres. L'Incarnus renaît dans sa forme ultime : Joker (m181b), le seigneur des bêtes sacrées. Les sanctuaires scellés de Pandémonia s'ouvrent, révélant la crypte d'Estark, le dieu de la destruction endormi. Sur l'océan, le légendaire Navire Fantôme du Capitaine Crow apparaît par temps de brume, tandis que l'Arène de Palatopia ouvre ses tournois secrets de rang S et X.",
            "en": "Peace restored, the greatest challenges await. The Incarnus is reborn as Joker (m181b), the divine sovereign. Sealed crypts on Infern Isle open to reveal sleeping giant Estark. Across the foggy seas, Captain Crow's Ghost Ship appears, while the Coliseum unveils secret Rank S & X tournaments.",
            "de": "Wiedergeburt des Inkarnus als Joker (m181b). Öffnung der versiegelten Grüfte für Estark, das Geisterschiff von Kapitän Crow und Rang-S/X-Turniere.",
            "it": "Rinascita dell'Incarnus come Joker (m181b). Sfida a Estark, apparizione della Nave Fantasma di Capitan Crow e tornei di Rango S/X.",
            "es": "Renacimiento del Incarnus como Joker (m181b). Desafío de Estark, el barco fantasma del Capitán Cuervo y torneos de Rango S/X.",
        },
        "chapters": [
            {
                "id": "ch_5_1",
                "title": {
                    "fr": "Le Réveil d'Estark dans les Abysses de Tartare",
                    "en": "Awakening of Estark in the Abyss",
                    "de": "Erwachen von Estark in den Abgründen",
                    "it": "Il Risveglio di Estark negli Abissi",
                    "es": "El Despertar de Estark en los Abismos",
                },
                "synopsis": {
                    "fr": "Dans les profondeurs scellées du temple d078, le titan Estark (PV 2560, niveau 30) sommeille depuis des millénaires. Si le héros parvient à le vaincre en moins de 10 tours, Estark reconnaît sa bravoure et rejoint son équipe.",
                    "en": "Deep in sealed dungeon d078, ancient lord Estark (HP 2560, level 30) sleeps. Defeating him in under 10 turns earns his respect and allegiance.",
                    "de": "In den Tiefen von Schrein d078 schläft Estark (LP 2560). Ein Sieg in unter 10 Runden gewinnt ihn für das eigene Team.",
                    "it": "Nelle profondità del tempio d078 dorme Estark (PV 2560). Sconfitto in meno di 10 turni si unisce alla squadra.",
                    "es": "En las profundidades del templo d078 duerme Estark (PV 2560). Al derrotarlo en menos de 10 turnos, se une al equipo.",
                },
                "maps": ["d077", "d078", "f121"],
                "characters": ["Estark (m158)", "Incarnus Forme Joker"],
                "dev_notes": ["エスターク撃破判定 (Contrôle défaite d'Estark)", "ターン数カウント (Décompte des tours de combat)"],
                "unlocks": ["Recrutement d'Estark", "Titre de Maître Suprême"],
            },
            {
                "id": "ch_5_2",
                "title": {
                    "fr": "Le Navire Fantôme du Capitaine Crow",
                    "en": "Captain Crow's Ghost Ship",
                    "de": "Das Geisterschiff von Kapitän Crow",
                    "it": "La Nave Fantasma di Capitan Crow",
                    "es": "El Barco Fantasma del Capitán Cuervo",
                },
                "synopsis": {
                    "fr": "Par nuit brumeuse sur les quais de Fert, Xéroph ou Célestia, le navire pirate d071 émerge des flots. Le Capitaine Crow défie le héros à 5 reprises successives, devenant plus redoutable à chaque assaut avant de capituler et d'offrir son pacte de dresseur.",
                    "en": "On foggy nights, pirate galleon d071 appears. Captain Crow challenges the player 5 successive times before surrendering and joining the scout team.",
                    "de": "In nebligen Nächten erscheint das Geisterschiff d071. Kapitän Crow fordert den Spieler fünfmal heraus.",
                    "it": "Nelle notti di nebbia appare il vascello pirata d071 di Capitan Crow per 5 battaglie consecutive.",
                    "es": "En noches de niebla, el barco pirata d071 desafía al jugador 5 veces sucesivas.",
                },
                "maps": ["d071", "d072", "d073", "d074", "d075", "d076"],
                "characters": ["Capitaine Crow (m152)", "Équipage squelette"],
                "dev_notes": ["海賊船出現判定 (Contrôle d'apparition du vaisseau pirate)", "撃破回数カウント (Décompte des 5 victoires)"],
                "unlocks": ["Recrutement du Capitaine Crow", "Clé des pirates"],
            },
            {
                "id": "ch_5_3",
                "title": {
                    "fr": "La Métamorphose Finale : Joker et l'As de Pique Purifié",
                    "en": "Final Metamorphosis: Joker & Purified Ace of Spades",
                    "de": "Finale Metamorphose: Joker & Geläutertes Pik-As",
                    "it": "Metamorfosi Finale: Joker e l'Asso di Picche Purificato",
                    "es": "Metamorfosis Final: Joker y el As de Picas Purificado",
                },
                "synopsis": {
                    "fr": "Au sanctuaire secret de Pandémonia f111, l'Incarnus débloque la synthèse ultime pour alterner librement entre toutes ses formes : Apik, Diamagon, Cluboon, Hawkhart, As de Pique purifié et la forme souveraine Joker.",
                    "en": "At secret shrine f111, the Incarnus unlocks sovereign synthesis to alternate freely between all forms including Joker and purified Ace of Spades.",
                    "de": "Am Schrein f111 meistert der Inkarnus den freien Wechsel zwischen allen göttlichen Formen.",
                    "it": "Al santuario f111 l'Incarnus padroneggia la fusione finale per passare a tutte le forme.",
                    "es": "En el santuario f111, el Incarnus adquiere la síntesis definitiva para cambiar entre todas sus formas.",
                },
                "maps": ["f111", "s071", "s072"],
                "characters": ["Incarnus (Joker, m181b)", "Solitaire"],
                "dev_notes": ["ジョーカー合成フラグ (Flag de synthèse Joker)", "全神獣解放 (Libération de toutes les formes sacrées)"],
                "unlocks": ["Synthèse du Joker", "Achèvement 100% de la Bibliothèque des Monstres"],
            },
        ],
    },
]

def main():
    payload = {
        "provenance": "ROM: 80 scripts .evt, 172 combats fixes (BtlEnmyPrm.bin), cartes 3D (.map) et 3179 commentaires japonais (0xaa)",
        "description": "Chronologie narrative intégrale de Dragon Quest Monsters: Joker découpée en 5 actes, quêtes principales et post-game avec commentaires de développement",
        "acts_count": len(ACTS),
        "acts": ACTS,
    }

    for target_dir in [OUT_RE, OUT_WEB]:
        os.makedirs(target_dir, exist_ok=True)
        out_file = os.path.join(target_dir, "story_timeline.json")
        with open(out_file, "w", encoding="utf-8") as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=1)
        print(f"Généré : {out_file} ({os.path.getsize(out_file) // 1024} Ko)")

if __name__ == "__main__":
    main()
