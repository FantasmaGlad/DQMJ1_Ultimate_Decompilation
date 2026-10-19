#!/usr/bin/env python3
"""Extrait et correle les 216 effets speciaux visuels (.efc) et les 256 aptitudes/sorts (TokugiDataTbl.bin & BtlEfcTbl.bin).

Structure decodée :
- 216 fichiers .efc (archives FPK Nitro) :
  - EFC_xxx.nsbmd (maillage 3D / particules)
  - EFC_xxx.nsbca (squelette d'animation)
  - EFC_xxx.nsbta (animation de texture UV)
  - EFC_xxx.nsbma (animation de matériau/couleur)
- TokugiDataTbl.bin (256 aptitudes x 40 octets) :
  - Coût en PM, dégâts de base min/max, plafond de dégâts, seuils de sagesse min/max, identifiant SE sonore
- BtlEfcTbl.bin (256 aptitudes x 126 octets) :
  - 18 sous-étapes d'animation/keyframes de 7 octets

Sortie :
- DragonQuestMonsterJoker1Bestiaire/assets/data/spell_effects.json
"""

import glob
import json
import os
import struct
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA_DIR = ROOT / "work/extracted/data"
BESTIAIRE_DIR = ROOT.parent / "DragonQuestMonsterJoker1Bestiaire"
DEST_JSON = BESTIAIRE_DIR / "assets/data/spell_effects.json"
SKILL_TIERS_PATH = BESTIAIRE_DIR / "assets/data/skill_tiers_rom.json"


def unpack_fpk(blob):
    if blob[:4] != b"FPK\0":
        return []
    n = struct.unpack_from("<I", blob, 4)[0]
    subfiles = []
    for i in range(n):
        o = 8 + 40 * i
        name = blob[o : o + 32].split(b"\0")[0].decode("latin1")
        off, size = struct.unpack_from("<II", blob, o + 32)
        subfiles.append({"name": name, "size": size})
    return subfiles


def load_ability_names():
    names_by_id = {}
    if SKILL_TIERS_PATH.exists():
        with open(SKILL_TIERS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for skill in data.get("skills", {}).values():
            for unlock in skill.get("unlocks", []):
                aid = unlock.get("ability_id")
                if aid is not None and aid not in names_by_id:
                    names_by_id[aid] = {
                        "name": unlock.get("name", {}),
                        "description": unlock.get("description", {}),
                    }
    return names_by_id


def main():
    ability_texts = load_ability_names()

    # 1. Scanner les 216 .efc
    efc_catalog = {}
    for p in sorted(DATA_DIR.glob("*.efc")):
        d = p.read_bytes()
        subfiles = unpack_fpk(d)
        efc_id = p.stem.replace("EFC_", "")
        efc_catalog[efc_id] = {
            "id": efc_id,
            "filename": p.name,
            "size": len(d),
            "subfiles": subfiles,
            "has_model": any(s["name"].endswith(".nsbmd") for s in subfiles),
            "has_skeleton": any(s["name"].endswith(".nsbca") for s in subfiles),
            "has_texture_anim": any(s["name"].endswith(".nsbta") for s in subfiles),
            "has_material_anim": any(s["name"].endswith(".nsbma") for s in subfiles),
        }

    # 2. TokugiDataTbl.bin
    tokugi_data = (DATA_DIR / "TokugiDataTbl.bin").read_bytes()
    num_tokugi = len(tokugi_data) // 40

    # 3. BtlEfcTbl.bin
    btl_efc_data = (DATA_DIR / "BtlEfcTbl.bin").read_bytes()

    spells = []
    for i in range(num_tokugi):
        t_entry = tokugi_data[i * 40 : (i + 1) * 40]
        mp = struct.unpack_from("<H", t_entry, 2)[0]
        min_dmg = struct.unpack_from("<H", t_entry, 8)[0]
        max_dmg = struct.unpack_from("<H", t_entry, 10)[0]
        cap_dmg = struct.unpack_from("<H", t_entry, 14)[0]
        min_wis = struct.unpack_from("<H", t_entry, 16)[0]
        max_wis = struct.unpack_from("<H", t_entry, 18)[0]
        se_id = struct.unpack_from("<H", t_entry, 32)[0]
        if se_id == 65535:
            se_id = None

        # BtlEfcTbl 18 steps de 7 octets
        efc_steps = []
        if i * 126 + 126 <= len(btl_efc_data):
            b_entry = btl_efc_data[i * 126 : (i + 1) * 126]
            for s in range(18):
                c = b_entry[s * 7 : (s + 1) * 7]
                u0 = struct.unpack("<H", c[:2])[0]
                u1 = struct.unpack("<H", c[2:4])[0]
                u2 = struct.unpack("<H", c[4:6])[0]
                u8 = c[6]
                if u0 != 0 or u1 != 0 or u2 != 0 or u8 != 0:
                    efc_steps.append({"step": s, "type": u0, "target_val": u1, "param": u2, "flag": u8})

        info = ability_texts.get(i, {})
        name = info.get("name", {"en": f"Ability {i}", "fr": f"Aptitude {i}", "de": f"Fähigkeit {i}", "it": f"Abilità {i}", "es": f"Habilidad {i}"})
        desc = info.get("description", {})

        spells.append({
            "id": i,
            "name": name,
            "description": desc,
            "mp_cost": mp,
            "min_damage": min_dmg if min_dmg > 0 else None,
            "max_damage": max_dmg if max_dmg > 0 else None,
            "cap_damage": cap_dmg if cap_dmg > 0 else None,
            "wisdom_threshold_min": min_wis if min_wis > 0 else None,
            "wisdom_threshold_cap": max_wis if max_wis > 0 else None,
            "sfx_id": f"SE_SKL_{se_id:03d}" if se_id is not None else None,
            "animation_steps_count": len(efc_steps),
            "animation_steps": efc_steps,
        })

    payload = {
        "provenance": "ROM : TokugiDataTbl.bin (File ID 3784), BtlEfcTbl.bin (File ID 98) et 216 archives EFC_*.efc",
        "total_effects": len(efc_catalog),
        "total_spells": len(spells),
        "effects": efc_catalog,
        "spells": spells,
    }

    with open(DEST_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Extraction terminee : {len(efc_catalog)} effets et {len(spells)} aptitudes enregistres dans {DEST_JSON}")


if __name__ == "__main__":
    main()
