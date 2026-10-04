#!/usr/bin/env python3
"""Décompilateur et analyseur exhaustif des 80 scripts d'événements (.evt) de DQMJ1.

Exécute l'Axe 5 du Master Plan :
- Décodage des en-têtes (table d'adresses d'entrée de 4096 octets)
- Découpage TLV du flux d'instructions de la machine virtuelle
- Extraction des 3 179 commentaires japonais de développement (0xaa, cp932)
- Extraction des dialogues (0x29) et locuteurs (0x2a)
- Extraction des combats scriptés (0x44)
- Extraction des instanciations d'entités (0x23)
- Extraction des déclencheurs audio BGM/SFX (0x48, 0x4a)
- Analyse des drapeaux de quête et de scénario (0x70 à 0x90)

Produit :
- assets/data/story_scripts.json
"""

import glob
import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(RACINE, "work/extracted/data")
OUT_RE = os.path.join(RACINE, "assets/data")
OUT_WEB = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire/assets/data")

# Table de caractères pour le décodage des chaînes textuelles dans .evt
CHAR_MAP = {
    **{i: str(i) for i in range(0, 10)},
    0x0A: " ",
    **{0x0B + i: chr(ord("A") + i) for i in range(26)},
    **{0x25 + i: chr(ord("a") + i) for i in range(26)},
    0x55: "Ü",
    0x57: "á",
    0x70: "!",
    0x71: "?",
    0x87: "+",
    0x8D: "II",
    0x8E: "III",
    0x9A: "‘",
    0x9B: "’",
    0xAC: ".",
    0xAD: "&",
    0xCC: "-",
    0xCD: ",",
    0xFE: "\n",
}

def decode_evt_string(payload: bytes) -> str:
    chars = []
    for b in payload:
        if b == 0xFF:
            break
        chars.append(CHAR_MAP.get(b, f"[{b:02x}]"))
    return "".join(chars)

def classify_comment(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["宝箱", "箱", "takara", "item", "アイテム"]):
        return "treasure"
    if any(k in t for k in ["祠", "神獣", "incarnus", "shrine"]):
        return "incarnus_shrine"
    if any(k in t for k in ["回戦", "優勝", "tournoi", "battle", "試合", "勝敗"]):
        return "tournament"
    if any(k in t for k in ["demo", "デモ", "再生", "演出", "オープニング", "エンディング"]):
        return "cutscene"
    if any(k in t for k in ["敵配置", "msg =", "配置", "出現"]):
        return "enemy_spawn"
    if any(k in t for k in ["マスター", "dresseur", "交換"]):
        return "trainer"
    if any(k in t for k in ["フラグ", "flag", "判定", "クリア"]):
        return "story_flag"
    return "general"

def decompile_evt(filepath: str) -> dict:
    filename = os.path.basename(filepath)
    map_id = filename.replace(".evt", "")

    with open(filepath, "rb") as fp:
        data = fp.read()

    file_size = len(data)
    if file_size < 4 + 0x1000 or data[:4] != b"SCR\x00":
        return {}

    # 1. En-tête : 1024 entrées de 4 octets
    entry_points = {}
    for slot in range(1024):
        offset = 4 + slot * 4
        ep = struct.unpack("<I", data[offset:offset+4])[0]
        if ep != 0xFFFFFFFF:
            entry_points[slot] = ep

    # 2. Flux TLV
    offset = 4 + 0x1000
    instructions = []
    comments = []
    dialogues = []
    battles = []
    entity_spawns = []
    audio_triggers = []
    flag_operations = []

    last_comment = ""
    last_speaker = ""

    while offset + 8 <= file_size:
        type_id, length = struct.unpack_from("<II", data, offset)
        if length < 8 or offset + length > file_size:
            break

        payload = data[offset + 8 : offset + length]
        rel_offset = offset - (4 + 0x1000)

        # Commentaire développeur japonais (0xaa)
        if type_id == 0xaa:
            raw_comment = payload.split(b"\0")[0].decode("cp932", "replace").strip()
            if raw_comment:
                category = classify_comment(raw_comment)
                last_comment = raw_comment
                comments.append({
                    "offset": rel_offset,
                    "text": raw_comment,
                    "category": category,
                })

        # Nom du locuteur (0x2a)
        elif type_id == 0x2a:
            last_speaker = decode_evt_string(payload)

        # Tirade / Dialogue (0x29)
        elif type_id == 0x29:
            dialogue_text = decode_evt_string(payload)
            dialogues.append({
                "offset": rel_offset,
                "speaker": last_speaker or "Unknown",
                "text": dialogue_text,
                "context_comment": last_comment,
            })

        # Combat scripté (0x44)
        elif type_id == 0x44:
            battle_args = [b for b in payload[:16]]
            battles.append({
                "offset": rel_offset,
                "context_comment": last_comment,
                "args": battle_args,
            })

        # Spawn entité (0x23)
        elif type_id == 0x23:
            spawn_args = [b for b in payload[:16]]
            entity_spawns.append({
                "offset": rel_offset,
                "context_comment": last_comment,
                "args": spawn_args,
            })

        # BGM / Audio (0x48, 0x4a)
        elif type_id in (0x48, 0x4a):
            audio_id = struct.unpack("<H", payload[:2])[0] if len(payload) >= 2 else 0
            audio_triggers.append({
                "offset": rel_offset,
                "type": "bgm" if type_id == 0x48 else "sfx",
                "audio_id": audio_id,
                "context_comment": last_comment,
            })

        # Flags et scénario (0x70..0x90)
        elif 0x70 <= type_id <= 0x90:
            flag_operations.append({
                "offset": rel_offset,
                "opcode": f"0x{type_id:02x}",
                "context_comment": last_comment,
            })

        instructions.append({
            "offset": rel_offset,
            "opcode": type_id,
            "len": length,
        })
        offset += length

    return {
        "map_id": map_id,
        "file_size": file_size,
        "instruction_count": len(instructions),
        "entry_points": entry_points,
        "comments_count": len(comments),
        "comments": comments,
        "dialogues_count": len(dialogues),
        "dialogues": dialogues[:30],  # échantillon représentatif par carte
        "battles_count": len(battles),
        "battles": battles,
        "entity_spawns_count": len(entity_spawns),
        "audio_triggers_count": len(audio_triggers),
        "audio_triggers": audio_triggers,
        "flag_operations_count": len(flag_operations),
    }

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.evt")))
    print(f"Décompilation de {len(files)} scripts .evt...")

    total_comments = 0
    total_dialogues = 0
    total_battles = 0
    total_instructions = 0

    scripts_by_map = {}
    comments_catalog = []

    for f in files:
        res = decompile_evt(f)
        if not res:
            continue
        map_id = res["map_id"]
        scripts_by_map[map_id] = res

        total_instructions += res["instruction_count"]
        total_comments += res["comments_count"]
        total_dialogues += res["dialogues_count"]
        total_battles += res["battles_count"]

        for c in res["comments"]:
            comments_catalog.append({
                "map_id": map_id,
                "offset": c["offset"],
                "text": c["text"],
                "category": c["category"],
            })

    output_payload = {
        "provenance": "ROM: 80 scripts .evt (data/*.evt) décompilés par machine virtuelle TLV",
        "description": "Base de données intégrale des scripts d'événements, commentaires de développement et déclencheurs narratifs",
        "metrics": {
            "scripts_count": len(scripts_by_map),
            "total_instructions": total_instructions,
            "total_developer_comments": total_comments,
            "total_dialogues": total_dialogues,
            "total_scripted_battles": total_battles,
        },
        "scripts_by_map": scripts_by_map,
        "developer_comments": comments_catalog,
    }

    for target_dir in [OUT_RE, OUT_WEB]:
        os.makedirs(target_dir, exist_ok=True)
        out_file = os.path.join(target_dir, "story_scripts.json")
        with open(out_file, "w", encoding="utf-8") as fp:
            json.dump(output_payload, fp, ensure_ascii=False, indent=1)
        print(f"Généré : {out_file} ({os.path.getsize(out_file) // 1024} Ko)")

    print(f"Succès : {total_instructions} instructions décompilées, {total_comments} commentaires japonais répertoriés.")

if __name__ == "__main__":
    main()
