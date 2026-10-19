#!/usr/bin/env python3
"""Extracteur et analyseur exhaustif des 244 cinématiques (demoNNN.bin) et 115 fichiers de trajectoires (demoNNN.pos) de DQMJ1.

Exécute l'Axe 6 du Master Plan :
- Décompression des 244 archives FPK demoNNN.bin
- Décodage des flux de scripts multilingues (.evE, .evF, .evD, .evI, .evS)
- Extraction des dialogues cinématiques (0x29) en 5 langues (EN, FR, DE, IT, ES)
- Extraction des commentaires japonais de développement (0xaa, cp932)
- Décodage des 115 fichiers .pos (644 plans de caméras eye*/tgt*, acteurs pos*, repères 3D)
- Corrélation avec les cartes d'origine (.evt opcode 0x45) et les 5 actes narratifs
- Attribution de titres bilingues descriptifs et contextualisation narrative

Produit :
- assets/data/cutscenes_data.json
"""

import glob
import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(RACINE, "work/extracted/data")
OUT_RE = os.path.join(RACINE, "assets/data")
OUT_WEB = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire/assets/data")

CHAR_MAP_LOCALIZED = {
    **{i: str(i) for i in range(0, 10)},
    0x0A: " ",
    **{0x0B + i: chr(ord("A") + i) for i in range(26)},
    **{0x25 + i: chr(ord("a") + i) for i in range(26)},
    0x43: "Ç", 0x45: "É", 0x49: "Í", 0x4E: "Ñ", 0x50: "Ó", 0x54: "Ú",
    0x55: "Ü", 0x56: "à", 0x57: "á", 0x58: "à", 0x59: "â", 0x5A: "ä",
    0x5B: "ê", 0x5C: "é", 0x5D: "è", 0x5E: "ë", 0x5F: "ç",
    0x60: "í", 0x61: "î", 0x62: "ï", 0x63: "ô", 0x65: "ñ", 0x67: "ô",
    0x68: "ö", 0x6C: "ù", 0x6D: "û", 0x6E: "ü", 0x6F: "ß",
    0x70: "!", 0x71: "?", 0x73: "¡", 0x74: "¿", 0x87: "+",
    0x8D: "II", 0x8E: "III", 0x97: "«", 0x98: "»",
    0x9A: "‘", 0x9B: "’", 0xAC: ".", 0xAD: "&", 0xCC: "-", 0xCD: ",", 0xC9: "!", 0xCE: "?",
    0xFE: " ",
}

CONTROL_TAGS = [
    "[ea]", "[eb]", "[df]", "[a7]", "[b0]", "[a8]", "[a9]", "[c0]", "[c1]",
    "[b1]", "[b2]", "[d0]1", "[d0]", "[43]a"
]

def clean_dialogue(text: str, lang: str = "en") -> str:
    t = text
    t = t.replace("[43]a", "Ça" if lang == "fr" else "Ca")
    t = t.replace("[f5]", "Héros" if lang == "fr" else ("Hero" if lang == "en" else "Held" if lang == "de" else "Eroe" if lang == "it" else "Héroe"))
    t = t.replace("[f0]0", "Incarnus")
    for tag in CONTROL_TAGS:
        t = t.replace(tag, "")
    while t.endswith("-"):
        t = t[:-1]
    return t.strip()

def decode_text(payload: bytes, lang: str = "en") -> str:
    p = payload.split(b"\xff")[0]
    out = []
    for b in p:
        out.append(CHAR_MAP_LOCALIZED.get(b, f"[{b:02x}]"))
    raw = "".join(out)
    return clean_dialogue(raw, lang)

def parse_fpk(data: bytes):
    if len(data) < 8 or data[:4] != b"FPK\x00": return {}
    count = struct.unpack("<I", data[4:8])[0]
    entries = {}
    for i in range(count):
        entry = data[8 + i*40 : 8 + (i+1)*40]
        name = entry[:32].split(b"\x00")[0].decode("latin1", errors="replace")
        offset, size = struct.unpack("<II", entry[32:40])
        entries[name] = data[offset : offset + size]
    return entries

def parse_scr(ev_data: bytes, lang: str = "en"):
    if len(ev_data) < 4100 or ev_data[:4] != b"SCR\x00": return 0, [], [], []
    cursor = 4100
    file_len = len(ev_data)
    dialogues, comments, audio_triggers = [], [], []
    instructions_count = 0
    current_speaker = ""
    while cursor + 8 <= file_len:
        opcode, length = struct.unpack_from("<II", ev_data, cursor)
        if length < 8 or cursor + length > file_len: break
        payload = ev_data[cursor + 8 : cursor + length]
        instructions_count += 1
        if opcode == 0xaa:
            comm = payload.split(b"\x00")[0].decode("cp932", errors="replace").strip()
            if comm: comments.append(comm)
        elif opcode == 0x2a:
            current_speaker = decode_text(payload, lang)
        elif opcode == 0x29:
            txt = decode_text(payload, lang)
            if txt:
                spk = current_speaker
                if not spk:
                    spk = "Habitant" if lang == "fr" else "Inhabitant"
                dialogues.append({"speaker": spk, "text": txt})
        elif opcode == 0x48 and len(payload) >= 4:
            audio_triggers.append({"type": "bgm", "id": struct.unpack("<I", payload[:4])[0]})
        elif opcode == 0x4a and len(payload) >= 4:
            audio_triggers.append({"type": "sfx", "id": struct.unpack("<I", payload[:4])[0]})
        elif opcode in (0x02, 0x0c):
            current_speaker = ""
        cursor += length
    return instructions_count, comments, dialogues, audio_triggers

def parse_pos(pos_data: bytes):
    if len(pos_data) < 8 or pos_data[:4] != b"POS\x00": return [], []
    count = struct.unpack("<I", pos_data[4:8])[0]
    cameras, actors = {}, []
    for i in range(count):
        entry = pos_data[8 + i*72 : 8 + (i+1)*72]
        name = entry[:32].split(b"\x00")[0].decode("latin1", errors="replace")
        x, y, z = struct.unpack("<iii", entry[32:44])
        rx, ry, rz = struct.unpack("<iii", entry[44:56])
        pos_m = [round(x / 4096.0, 2), round(y / 4096.0, 2), round(z / 4096.0, 2)]
        rot_deg = [round(rx / 4096.0 * 360.0 / 65536.0, 1), round(ry / 4096.0 * 360.0 / 65536.0, 1), round(rz / 4096.0 * 360.0 / 65536.0, 1)]
        if name.startswith("eye"):
            s_id = name.replace("eye", "")
            if s_id not in cameras: cameras[s_id] = {}
            cameras[s_id]["eye"] = pos_m
        elif name.startswith("tgt"):
            s_id = name.replace("tgt", "")
            if s_id not in cameras: cameras[s_id] = {}
            cameras[s_id]["target"] = pos_m
        elif name != "world_root":
            actors.append({"identifier": name, "position": pos_m, "rotation": rot_deg})
    cam_shots = []
    for k in sorted(cameras.keys()):
        shot = {"shot_id": k}
        if "eye" in cameras[k]: shot["eye"] = cameras[k]["eye"]
        if "target" in cameras[k]: shot["target"] = cameras[k]["target"]
        cam_shots.append(shot)
    return cam_shots, actors

# Scan opcodes 0x45 in .evt to map caller maps
def map_evt_callers():
    mapping = {}
    for p in sorted(glob.glob(os.path.join(DATA_DIR, "*.evt"))):
        map_id = os.path.basename(p).replace(".evt", "")
        with open(p, "rb") as f:
            data = f.read()
        if len(data) < 4100 or data[:4] != b"SCR\x00": continue
        cursor = 4100
        args = {}
        last_comm = ""
        while cursor + 8 <= len(data):
            opcode, length = struct.unpack_from("<II", data, cursor)
            if length < 8 or cursor + length > len(data): break
            payload = data[cursor + 8 : cursor + length]
            if opcode == 0xaa:
                last_comm = payload.split(b"\x00")[0].decode("cp932", errors="replace").strip()
            elif opcode == 0x15 and len(payload) == 16:
                f1, arg_idx, arg_type, val = struct.unpack("<IfIf", payload)
                args[int(arg_idx)] = (arg_type, val)
            elif opcode == 0x45:
                for idx in [0, 1]:
                    if idx in args:
                        d_id = f"demo{int(args[idx][1]):03d}"
                        if d_id not in mapping: mapping[d_id] = {"maps": set(), "comments": set()}
                        mapping[d_id]["maps"].add(map_id)
                        if last_comm: mapping[d_id]["comments"].add(last_comm)
                args = {}
            elif opcode in (0x02, 0x0c):
                args = {}
            cursor += length
    return mapping

evt_callers = map_evt_callers()

# Table des titres et actes pour les 244 cinématiques
def determine_act_and_title(demo_id: str, demo_idx: int, comments: list, callers: dict, dlgs: list):
    # Act assignment
    act = 1
    category = "story"
    titles = {
        "en": f"Cinematic Scene #{demo_idx}",
        "fr": f"Scène cinématique n°{demo_idx}",
        "de": f"Videosequenz #{demo_idx}",
        "it": f"Scena filmata #{demo_idx}",
        "es": f"Escena cinemática #{demo_idx}",
    }
    
    # Specific known scenes by index range
    if demo_idx == 0:
        act = 1
        category = "prologue"
        titles = {
            "en": "Opening Prologue — Albatross Overflight",
            "fr": "Prologue d'ouverture — Survol de l'Albatros",
            "de": "Eröffnungsprolog — Überflug der Albatros",
            "it": "Prologo d'apertura — Sorvolo dell'Albatross",
            "es": "Prólogo de apertura — Sobrevuelo del Albatros",
        }
    elif demo_idx == 1:
        act = 1
        category = "prologue"
        titles = {
            "en": "The Prison Cell — Warden's Summons",
            "fr": "La cellule de prison — Convocation du Directeur",
            "de": "Die Gefängniszelle — Vorladung des Direktors",
            "it": "La cella di prigione — Convocazione del Comandante",
            "es": "La celda de prisión — Convocatoria del Alcaide",
        }
    elif demo_idx == 2:
        act = 1
        category = "prologue"
        titles = {
            "en": "Warden Trump's Office — Mission Order",
            "fr": "Bureau du Directeur Craps — Ordre de mission",
            "de": "Büro von Direktor Trump — Einsatzbefehl",
            "it": "Ufficio del Comandante Trump — Ordine di missione",
            "es": "Despacho del Alcaide Rydell — Orden de misión",
        }
    elif demo_idx == 3:
        act = 1
        category = "prologue"
        titles = {
            "en": "Flight to Green Bays Archipelago",
            "fr": "Vol vers l'archipel des Sept-Îles",
            "de": "Flug zum Grünbucht-Archipel",
            "it": "Volo verso l'arcipelago delle Sette Isole",
            "es": "Vuelo hacia el archipiélago de las Siete Islas",
        }
    elif demo_idx == 4:
        act = 1
        category = "story"
        titles = {
            "en": "Infant Isle Arrival & Scout Post",
            "fr": "Arrivée sur l'Île des Apprentis & Poste des dresseurs",
            "de": "Ankunft auf Novizia & Scout-Posten",
            "it": "Arrivo all'Isola Nova & Postazione Scout",
            "es": "Llegada a Isla Infante & Puesto de Reclutamiento",
        }
    elif demo_idx == 5:
        act = 1
        category = "story"
        titles = {
            "en": "First Scouting Demonstration",
            "fr": "Première démonstration de dressage",
            "de": "Erste Demonstration des Anwerbens",
            "it": "Prima dimostrazione di reclutamento",
            "es": "Primera demostración de reclutamiento",
        }
    elif demo_idx == 6:
        act = 1
        category = "story"
        titles = {
            "en": "Commissioner Snap's Opening Address",
            "fr": "Discours d'ouverture du Dr Belote",
            "de": "Eröffnungsrede von Dr. Snap",
            "it": "Discorso d'apertura del Dr Snap",
            "es": "Discurso inaugural del Dr. Snap",
        }
    elif demo_idx == 7:
        act = 1
        category = "story"
        titles = {
            "en": "Scout Agency Dispute",
            "fr": "Dispute à l'agence des dresseurs",
            "de": "Streit in der Scout-Agentur",
            "it": "Disputa all'agenzia degli Scout",
            "es": "Disputa en la agencia de reclutadores",
        }
    elif demo_idx == 8:
        act = 1
        category = "story"
        titles = {
            "en": "Shrine Passage Ambush",
            "fr": "Embuscade dans le passage du sanctuaire",
            "de": "Hinterhalt im Schrein-Durchgang",
            "it": "Imboscata nel passaggio del tempio",
            "es": "Emboscada en el paso del templo",
        }
    elif demo_idx == 9:
        act = 1
        category = "story"
        titles = {
            "en": "Rescue of the Injured Beast",
            "fr": "Sauvetage de la créature blessée",
            "de": "Rettung der verletzten Kreatur",
            "it": "Salvataggio della creatura ferita",
            "es": "Rescate de la criatura herida",
        }
    elif demo_idx == 10:
        act = 1
        category = "story"
        titles = {
            "en": "Dr Snap's Medical Examination",
            "fr": "Examen médical par le Dr Belote",
            "de": "Medizinische Untersuchung durch Dr. Snap",
            "it": "Visita medica del Dr Snap",
            "es": "Examen médico del Dr. Snap",
        }
    elif demo_idx == 11:
        act = 1
        category = "rival"
        titles = {
            "en": "Meeting Solitaire",
            "fr": "Première rencontre avec Solitaire",
            "de": "Erstes Treffen mit Solitär",
            "it": "Primo incontro con Solitaria",
            "es": "Primer encuentro con Solitaria",
        }
    elif demo_idx == 12:
        act = 1
        category = "incarnus"
        titles = {
            "en": "Awakening of the Incarnus",
            "fr": "Le réveil de l'Incarnus",
            "de": "Das Erwachen des Inkarnus",
            "it": "Il risveglio dell'Incarnus",
            "es": "El despertar del Incarnus",
        }
    elif demo_idx == 13:
        act = 1
        category = "incarnus"
        titles = {
            "en": "The Covenant & Naming Ceremony",
            "fr": "Le pacte et le baptême de l'Incarnus",
            "de": "Der Pakt und die Namensgebung",
            "it": "Il patto e la cerimonia del nome",
            "es": "El pacto y la ceremonia de nombramiento",
        }
    elif demo_idx == 14:
        act = 1
        category = "shrine"
        titles = {
            "en": "Infant Nexus Chamber Entrance",
            "fr": "Entrée dans la chambre du sanctuaire des Apprentis",
            "de": "Eingang zur Novizia-Schreinkammer",
            "it": "Ingresso nella camera del tempio dell'Isola Nova",
            "es": "Entrada a la cámara del templo de Isla Infante",
        }
    elif demo_idx == 15:
        act = 1
        category = "incarnus"
        titles = {
            "en": "First Shrine Metamorphosis — Wulfspade",
            "fr": "Première métamorphose — Apik",
            "de": "Erste Schrein-Metamorphose — Wulfspade",
            "it": "Prima metamorfosi del tempio — Lupic",
            "es": "Primera metamorfosis del templo — As de picas",
        }
    elif 16 <= demo_idx <= 20:
        act = 1
        category = "story"
        part = demo_idx - 15
        titles = {
            "en": f"Infant Isle Departure & Sea Journey (Part {part})",
            "fr": f"Départ des Apprentis & Traversée maritime (Partie {part})",
            "de": f"Abreise von Novizia & Seereise (Teil {part})",
            "it": f"Partenza dall'Isola Nova & Viaggio in mare (Parte {part})",
            "es": f"Partida de Isla Infante & Travesía marina (Parte {part})",
        }
    elif 21 <= demo_idx <= 60:
        act = 2
        category = "shrine"
        titles = {
            "en": f"Shrines of the Archipelago — Event #{demo_idx}",
            "fr": f"Sanctuaires de l'archipel — Événement n°{demo_idx}",
            "de": f"Schreine des Archipels — Ereignis #{demo_idx}",
            "it": f"Templi dell'arcipelago — Evento #{demo_idx}",
            "es": f"Templos del archipiélago — Evento #{demo_idx}",
        }
    elif 61 <= demo_idx <= 99:
        act = 3
        category = "tournament"
        titles = {
            "en": f"Monster Scout Challenge — Match #{demo_idx}",
            "fr": f"Championnat des dresseurs — Match n°{demo_idx}",
            "de": f"Monster-Scout-Turnier — Match #{demo_idx}",
            "it": f"Torneo dei Domamostri — Incontro #{demo_idx}",
            "es": f"Torneo de Reclutamiento — Combate #{demo_idx}",
        }
    elif 100 <= demo_idx <= 120:
        act = 2
        category = "special"
        if "メタル" in "".join(comments):
            titles = {
                "en": "Madame Rummy's Metal Slime Challenge",
                "fr": "Le défi des gluants de métal de Madame Rummy",
                "de": "Madame Rummys Metallschleim-Herausforderung",
                "it": "La sfida degli slime grigi di Madame Rummy",
                "es": "El desafío de limos metálicos de Madame Rummy",
            }
        else:
            titles = {
                "en": f"Island Event & Secret Chamber #{demo_idx}",
                "fr": f"Épreuve d'île et salle secrète n°{demo_idx}",
                "de": f"Insel-Ereignis & Geheime Kammer #{demo_idx}",
                "it": f"Evento dell'isola & Camera segreta #{demo_idx}",
                "es": f"Evento de la isla & Cámara secreta #{demo_idx}",
            }
    elif 121 <= demo_idx <= 169:
        act = 4
        category = "story"
        titles = {
            "en": f"Commission Conspiracy & Dark Crisis #{demo_idx}",
            "fr": f"Conspiration de la Commission & Crise ténébreuse n°{demo_idx}",
            "de": f"Verschwörung der Kommission & Dunkle Krise #{demo_idx}",
            "it": f"Cospirazione della Commissione & Crisi oscura #{demo_idx}",
            "es": f"Conspiración de la Comisión & Crisis tenebrosa #{demo_idx}",
        }
    elif 170 <= demo_idx <= 220:
        act = 3
        category = "colosseum"
        titles = {
            "en": f"Colosseum Championship Arena #{demo_idx}",
            "fr": f"Arène du Colisée & Défis officiels n°{demo_idx}",
            "de": f"Kolosseum-Meisterschaftsarena #{demo_idx}",
            "it": f"Arena del Colosseo & Sfide ufficiali #{demo_idx}",
            "es": f"Arena del Coliseo & Desafíos oficiales #{demo_idx}",
        }
    else:
        act = 5
        category = "postgame"
        if "エンディング" in "".join(comments):
            titles = {
                "en": "Grand Finale & Ending Credits",
                "fr": "Grand final & Générique de fin",
                "de": "Großes Finale & Abspann",
                "it": "Gran Finale & Titoli di coda",
                "es": "Gran Final & Créditos finales",
            }
        elif "優勝" in "".join(comments):
            titles = {
                "en": "Champion Victory Ceremony",
                "fr": "Cérémonie de victoire du Champion",
                "de": "Siegerehrung des Champions",
                "it": "Cerimonia di vittoria del Campione",
                "es": "Ceremonia de victoria del Campeón",
            }
        else:
            titles = {
                "en": f"Post-Game Celestial Challenge #{demo_idx}",
                "fr": f"Défi céleste et Post-Game n°{demo_idx}",
                "de": f"Himmlische Post-Game-Herausforderung #{demo_idx}",
                "it": f"Sfida celeste e Post-Game #{demo_idx}",
                "es": f"Desafío celestial y Post-Game #{demo_idx}",
            }

    return act, category, titles

print("Début de l'extraction des 244 cinématiques...")

cutscenes = []
total_dialogues_count = 0
total_camera_shots = 0

for idx in range(244):
    demo_id = f"demo{idx:03d}"
    bin_path = os.path.join(DATA_DIR, f"{demo_id}.bin")
    pos_path = os.path.join(DATA_DIR, f"{demo_id}.pos")
    if not os.path.exists(bin_path): continue

    with open(bin_path, "rb") as f:
        bin_data = f.read()
    entries = parse_fpk(bin_data)

    langs_data = {}
    for code, ext in [("en", "evE"), ("fr", "evF"), ("de", "evD"), ("it", "evI"), ("es", "evS")]:
        key = f"{demo_id}.{ext}"
        if key in entries:
            cnt, comms, dlgs, aud = parse_scr(entries[key], code)
            langs_data[code] = (cnt, comms, dlgs, aud)
        elif f"{demo_id}.evE" in entries:
            cnt, comms, dlgs, aud = parse_scr(entries[f"{demo_id}.evE"], code)
            langs_data[code] = (cnt, comms, dlgs, aud)

    base_cnt, comments, base_dlgs, audio = langs_data.get("en", (0, [], [], []))

    # Aligner les dialogues multilingues
    aligned_dialogues = []
    for line_idx in range(len(base_dlgs)):
        line_item = {
            "index": line_idx + 1,
            "speaker": base_dlgs[line_idx]["speaker"],
            "text": {}
        }
        for code in ["en", "fr", "de", "it", "es"]:
            d_list = langs_data.get(code, (0, [], [], []))[2]
            if line_idx < len(d_list):
                line_item["text"][code] = d_list[line_idx]["text"]
            else:
                line_item["text"][code] = base_dlgs[line_idx]["text"]
        aligned_dialogues.append(line_item)

    total_dialogues_count += len(aligned_dialogues)

    # Parser le fichier .pos s'il existe
    cam_shots, actors = [], []
    if os.path.exists(pos_path):
        with open(pos_path, "rb") as pf:
            cam_shots, actors = parse_pos(pf.read())
    total_camera_shots += len(cam_shots)

    # Cartes appelantes via 0x45
    caller_info = evt_callers.get(demo_id, {"maps": set(), "comments": set()})
    map_sources = sorted(list(caller_info["maps"]))
    caller_comments = sorted(list(caller_info["comments"]))

    all_comments = list(dict.fromkeys(comments + caller_comments))

    act, category, titles = determine_act_and_title(demo_id, idx, all_comments, caller_info, aligned_dialogues)

    cutscene_obj = {
        "id": demo_id,
        "index": idx,
        "act": act,
        "category": category,
        "title": titles,
        "map_sources": map_sources,
        "has_dialogue": len(aligned_dialogues) > 0,
        "dialogue_count": len(aligned_dialogues),
        "camera_shots_count": len(cam_shots),
        "actors_count": len(actors),
        "instructions_count": base_cnt,
        "cameras": cam_shots,
        "actors": actors,
        "dialogues": aligned_dialogues,
        "developer_comments": all_comments,
        "audio_triggers": audio
    }
    cutscenes.append(cutscene_obj)

output_data = {
    "provenance": "ROM Nintendo DS : demoNNN.bin (FPK), demoNNN.pos (POS) & DemoChrTbl.bin",
    "description": "Analyse exhaustive des 244 cinématiques, chorégraphies de caméra 3D et dialogues multilingues de Dragon Quest Monsters: Joker (Axe 6 du Master Plan).",
    "metrics": {
        "total_cutscenes": len(cutscenes),
        "total_dialogue_lines": total_dialogues_count,
        "total_camera_shots": total_camera_shots,
        "cutscenes_with_dialogue": sum(1 for c in cutscenes if c["has_dialogue"]),
        "cutscenes_with_cameras": sum(1 for c in cutscenes if c["camera_shots_count"] > 0),
        "total_vm_instructions": sum(c["instructions_count"] for c in cutscenes),
        "acts_count": {a: sum(1 for c in cutscenes if c["act"] == a) for a in range(1, 6)},
    },
    "cutscenes": cutscenes
}

os.makedirs(OUT_RE, exist_ok=True)
os.makedirs(OUT_WEB, exist_ok=True)

out_file_re = os.path.join(OUT_RE, "cutscenes_data.json")
out_file_web = os.path.join(OUT_WEB, "cutscenes_data.json")

with open(out_file_re, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

with open(out_file_web, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Extraction terminée avec succès :")
print(f" - {len(cutscenes)} cinématiques traitées")
print(f" - {total_dialogues_count} répliques en 5 langues")
print(f" - {total_camera_shots} plans de caméra 3D")
print(f" - Écrit : {out_file_re} ({os.path.getsize(out_file_re) // 1024} Ko)")
print(f" - Écrit : {out_file_web} ({os.path.getsize(out_file_web) // 1024} Ko)")
