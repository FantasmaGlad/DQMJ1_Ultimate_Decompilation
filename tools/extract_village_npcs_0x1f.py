#!/usr/bin/env python3
"""Extrait exhaustivement les villageois et PNJ de terrain instanciés via l'opcode 0x1f
depuis les 80 scripts .evt de la ROM de DQMJ1.

Chaque spawn 0x1f reçoit ses paramètres par les opcodes 0x15 précédents :
- arg0 : indice de personnage (chr_id = arg0 + 1)
- arg1 : coordonnée X (float)
- arg2 : coordonnée Y (float)
- arg3 : coordonnée Z (float)
- arg4 : rotation / orientation (float)

L'indice chr_id indexe FldChrTbl.bin (stride 26 octets), dont le mot u16[1]
désigne le modèle 3D dans ModelTbl.bin (n000..n028, m000..m248).
"""

import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(RACINE, "work/extracted/data")
OUT_RE = os.path.join(RACINE, "assets/data")
OUT_BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire/assets/data")

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
    return "".join(chars).strip()

def load_tables():
    with open(os.path.join(DATA_DIR, "FldChrTbl.bin"), "rb") as f:
        fldchr = f.read()
    with open(os.path.join(DATA_DIR, "ModelTbl.bin"), "rb") as f:
        modeltbl = f.read()

    models = [
        modeltbl[i * 12 : (i + 1) * 12].split(b"\0")[0].decode("ascii", "replace")
        for i in range(len(modeltbl) // 12)
    ]
    return fldchr, models

def get_model_for_chr_id(fldchr: bytes, models: list, chr_id: int):
    if chr_id < 0 or chr_id >= len(fldchr) // 26:
        return None, None
    entry = fldchr[chr_id * 26 : (chr_id + 1) * 26]
    model_idx = struct.unpack_from("<H", entry, 2)[0]
    model_name = models[model_idx] if model_idx < len(models) else None
    return model_idx, model_name

def extract_all():
    fldchr, models = load_tables()
    evt_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".evt"))

    results_by_map = {}
    total_spawns = 0
    all_models_found = set()

    for filename in evt_files:
        path = os.path.join(DATA_DIR, filename)
        map_id = filename[:-4]

        with open(path, "rb") as fp:
            data = fp.read()

        if len(data) < 4 + 0x1000 or data[:4] != b"SCR\0":
            continue

        # En-têtes : 1024 slots
        entry_points = {}
        for slot in range(1024):
            ep = struct.unpack_from("<I", data, 4 + slot * 4)[0]
            if ep != 0xFFFFFFFF:
                entry_points[slot] = ep

        # Flux TLV
        offset = 4 + 0x1000
        n = len(data)
        args = {}
        last_comment = ""
        current_speaker = None
        map_spawns = []
        map_dialogues = []

        while offset + 8 <= n:
            tid, length = struct.unpack_from("<II", data, offset)
            if length < 8 or offset + length > n:
                break
            payload = data[offset + 8 : offset + length]

            if tid == 0x15:  # Argument setter
                if len(payload) >= 16:
                    u1, arg_num, nature, val = struct.unpack("<IffI", payload[:16])
                    val_float = struct.unpack("<f", payload[12:16])[0]
                    val_int = struct.unpack("<i", payload[12:16])[0]
                    args[int(round(arg_num))] = (nature, val_int, val_float)

            elif tid == 0xaa:  # Commentaire japonais
                last_comment = payload.split(b"\0")[0].decode("cp932", "replace").strip()

            elif tid == 0x2a:  # SpeakerName
                current_speaker = decode_evt_string(payload)

            elif tid == 0x29:  # SetDialog
                text = decode_evt_string(payload)
                if text and current_speaker:
                    map_dialogues.append({
                        "offset": offset,
                        "speaker": current_speaker,
                        "text": text,
                        "comment": last_comment,
                    })

            elif tid == 0x1f:  # Spawn acteur terrain (PNJ / Villageois)
                arg0_info = args.get(0)
                if arg0_info is not None:
                    chr_id = int(round(arg0_info[2])) + 1
                    model_idx, model_name = get_model_for_chr_id(fldchr, models, chr_id)
                    x = args.get(1, (0, 0, 0.0))[2]
                    y = args.get(2, (0, 0, 0.0))[2]
                    z = args.get(3, (0, 0, 0.0))[2]
                    rot = args.get(4, (0, 0, 0.0))[2]

                    if model_name:
                        all_models_found.add(model_name)

                    spawn_entry = {
                        "offset": offset,
                        "chr_id": chr_id,
                        "model_index": model_idx,
                        "model": model_name,
                        "x": round(x, 2),
                        "y": round(y, 2),
                        "z": round(z, 2),
                        "rotation": round(rot, 1),
                        "context_comment": last_comment,
                        "associated_speaker": current_speaker,
                    }
                    map_spawns.append(spawn_entry)
                    total_spawns += 1
                args = {}

            elif tid in (0x02, 0x0C):  # Return / Jump : réinitialisation de contexte
                current_speaker = None
                args = {}

            offset += length

        if map_spawns or map_dialogues:
            results_by_map[map_id] = {
                "spawns_count": len(map_spawns),
                "dialogues_count": len(map_dialogues),
                "spawns": map_spawns,
                "dialogues": map_dialogues,
            }

    output_data = {
        "metadata": {
            "source": "Nintendo DS ROM NTR-AJRP-EUR - overlay_0000.c:021c0f58 / 021b9444 / FldChrTbl.bin / ModelTbl.bin",
            "total_spawns": total_spawns,
            "total_maps": len(results_by_map),
            "distinct_models": sorted(list(all_models_found)),
        },
        "maps": results_by_map,
    }

    os.makedirs(OUT_RE, exist_ok=True)
    out_file_re = os.path.join(OUT_RE, "field_npcs_0x1f.json")
    with open(out_file_re, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    os.makedirs(OUT_BESTIAIRE, exist_ok=True)
    out_file_wiki = os.path.join(OUT_BESTIAIRE, "field_npcs_0x1f.json")
    with open(out_file_wiki, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Extraction terminée avec succès :")
    print(f"- Total spawns 0x1f : {total_spawns}")
    print(f"- Cartes concernées : {len(results_by_map)}")
    print(f"- Modèles 3D distincts ({len(all_models_found)}) : {sorted(list(all_models_found))}")
    print(f"- Données écrites dans : {out_file_wiki}")

if __name__ == "__main__":
    extract_all()
