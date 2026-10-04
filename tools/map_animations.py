#!/usr/bin/env python3
"""Cartographie exhaustive des 1 261 animations squelettiques (.nsbca) du jeu.

Sources prouvees par desassemblage et structures binaires :
- MotionTbl.bin (22 608 octets, 1 413 entrees de 16 octets : 12 o nom + u32 flags)
- ViewChrTbl.bin (9 152 octets, 352 entrees de 26 octets : 13 x u16, slots 2..7 associant chaque monstre a ses motions)
- BtlChrTimeTbl.bin (4 224 octets, 352 entrees de 12 octets : 3 x u32 fx16.16 pour attack/cast/flinch)
- ModelTbl.bin (3 048 octets, 254 noms de modeles 3D)
- Archives glTF converties dans assets/models/web-gltf/animated/
"""

import json
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire")
ANIM_DIR = os.path.join(BESTIAIRE, "assets/models/web-gltf/animated")
MAPPING_FILE = os.path.join(BESTIAIRE, "assets/data/monsters-mapping.json")
CONFIG_FILE = os.path.join(BESTIAIRE, "assets/data/animation_configs.json")
OUTPUT_FILE = os.path.join(BESTIAIRE, "assets/data/monster_animations.json")

ROLE_TRANSLATIONS = {
    "idle": {
        "en": "Idle",
        "fr": "Repos",
        "de": "Rast",
        "it": "Riposo",
        "es": "Reposo",
    },
    "walk": {
        "en": "Walk",
        "fr": "Marche",
        "de": "Gehen",
        "it": "Camminata",
        "es": "Caminar",
    },
    "attack": {
        "en": "Physical Attack",
        "fr": "Attaque physique",
        "de": "Physischer Angriff",
        "it": "Attacco fisico",
        "es": "Ataque físico",
    },
    "cast": {
        "en": "Spell / Skill",
        "fr": "Sort / Souffle",
        "de": "Zauber / Hauch",
        "it": "Incantesimo / Soffio",
        "es": "Conjuro / Aliento",
    },
    "flinch": {
        "en": "Damage / Flinch",
        "fr": "Dégât / Recul",
        "de": "Treffer / Rückstoß",
        "it": "Danno / Rinculo",
        "es": "Daño / Retroceso",
    },
    "battle_stance": {
        "en": "Battle Stance",
        "fr": "Posture de combat",
        "de": "Kampfhaltung",
        "it": "Guardia da combattimento",
        "es": "Guardia de combate",
    },
    "talk": {
        "en": "Talk",
        "fr": "Parler",
        "de": "Sprechen",
        "it": "Parlare",
        "es": "Hablar",
    },
    "point": {
        "en": "Point / Gesture",
        "fr": "Pointer / Geste",
        "de": "Deuten / Geste",
        "it": "Indicare / Gesto",
        "es": "Señalar / Gesto",
    },
    "surprise": {
        "en": "Alert / Surprise",
        "fr": "Alerte / Surprise",
        "de": "Alarm / Überraschung",
        "it": "Allerta / Sorpresa",
        "es": "Alerta / Sorpresa",
    },
    "nod": {
        "en": "Nod / Affirm",
        "fr": "Hochement / Accord",
        "de": "Nicken / Zustimmung",
        "it": "Cenno / Accordo",
        "es": "Asentir / Aprobación",
    },
    "action": {
        "en": "Victory / Action",
        "fr": "Victoire / Action",
        "de": "Sieg / Aktion",
        "it": "Vittoria / Azione",
        "es": "Victoria / Acción",
    },
    "run": {
        "en": "Run",
        "fr": "Course",
        "de": "Laufen",
        "it": "Corsa",
        "es": "Correr",
    },
    "jump": {
        "en": "Jump",
        "fr": "Saut",
        "de": "Sprung",
        "it": "Salto",
        "es": "Saltar",
    },
    "open": {
        "en": "Open",
        "fr": "Ouvrir",
        "de": "Öffnen",
        "it": "Aprire",
        "es": "Abrir",
    },
    "activate": {
        "en": "Activate",
        "fr": "Actionner",
        "de": "Betätigen",
        "it": "Azionare",
        "es": "Accionar",
    },
    "interact": {
        "en": "Interact",
        "fr": "Interagir",
        "de": "Interagieren",
        "it": "Interagire",
        "es": "Interactuar",
    },
    "special": {
        "en": "Special Action",
        "fr": "Action spéciale",
        "de": "Spezialaktion",
        "it": "Azione speciale",
        "es": "Acción especial",
    },
}


def get_role_and_loop(model_id: str, slot: str, flag: int):
    is_looping = (flag & 1 != 0) or (flag in (1, 9))
    if model_id.startswith("m"):
        if slot == "00":
            return "idle", True
        elif slot == "01":
            return "walk", True
        elif slot == "02":
            return "attack", False
        elif slot == "03":
            return "cast", False
        elif slot == "04":
            return "flinch", False
        elif slot == "10":
            return "battle_stance", True
        elif slot == "05":
            return "action", False
        else:
            return "special", is_looping
    elif model_id.startswith("n"):
        if slot == "00":
            return "idle", True
        elif slot == "01":
            return "walk", True
        elif slot == "02":
            return "talk", False
        elif slot == "03":
            return "point", False
        elif slot == "04":
            return "surprise", False
        elif slot == "05":
            return "nod", False
        elif slot == "10":
            return "action", False
        else:
            return "special", is_looping
    elif model_id == "cool":
        if slot == "00":
            return "idle", True
        elif slot == "01":
            return "walk", True
        elif slot == "02":
            return "run", True
        elif slot == "03":
            return "jump", False
        elif slot in ("04", "05", "06", "07", "08", "09"):
            return "interact", False
        elif slot in ("10", "11", "12"):
            return "special", False
        elif slot in ("13", "14", "15", "16"):
            return "action", False
        else:
            return "special", is_looping
    elif model_id.startswith("o_"):
        if "door" in slot or "door" in model_id:
            return "open", False
        elif "switch" in slot or "lever" in slot or "switch" in model_id or "lever" in model_id:
            return "activate", False
        elif "hashi" in slot or "hashi" in model_id:
            return "activate", False
        else:
            return "interact", is_looping
    elif model_id.startswith("takara"):
        return "open", False
    elif model_id == "taru":
        return "interact", False
    else:
        return "special", is_looping


def main():
    with open(os.path.join(DATA, "ModelTbl.bin"), "rb") as f:
        mod_bin = f.read()
    with open(os.path.join(DATA, "MotionTbl.bin"), "rb") as f:
        mot_bin = f.read()
    with open(os.path.join(DATA, "ViewChrTbl.bin"), "rb") as f:
        vct_bin = f.read()
    with open(os.path.join(DATA, "BtlChrTimeTbl.bin"), "rb") as f:
        btl_bin = f.read()

    models = [
        mod_bin[i * 12 : (i + 1) * 12].split(b"\x00")[0].decode("ascii", errors="ignore")
        for i in range(len(mod_bin) // 12)
    ]

    motions = []
    motions_by_name = {}
    for i in range(len(mot_bin) // 16):
        chunk = mot_bin[i * 16 : (i + 1) * 16]
        name = chunk[:12].split(b"\x00")[0].decode("ascii", errors="ignore")
        flag = struct.unpack("<I", chunk[12:16])[0]
        motions.append((name, flag))
        if name:
            motions_by_name[name] = (i, flag)

    with open(MAPPING_FILE) as f:
        mapping = json.load(f)

    with open(CONFIG_FILE) as f:
        anim_config = json.load(f)

    motionless_set = set(anim_config.get("motionlessAnimations", []))
    idle_overrides = anim_config.get("idleOverrides", {})

    # Read durations from glTF files
    gltf_durations = {}
    gltf_animations_by_model = {}
    if os.path.exists(ANIM_DIR):
        for mdir in sorted(os.listdir(ANIM_DIR)):
            gpath = os.path.join(ANIM_DIR, mdir, f"{mdir}.gltf")
            if os.path.exists(gpath):
                try:
                    with open(gpath) as gf:
                        g = json.load(gf)
                    anims_list = []
                    for a in g.get("animations", []):
                        aname = a.get("name")
                        max_t = 0.0
                        for s in a.get("samplers", []):
                            acc = g["accessors"][s["input"]]
                            if "max" in acc and acc["max"]:
                                max_t = max(max_t, acc["max"][0])
                        dur = round(max_t, 3)
                        gltf_durations[aname] = dur
                        anims_list.append(aname)
                    gltf_animations_by_model[mdir] = anims_list
                except Exception:
                    pass

    # Build species table
    # species_index -> (model_name, attack_time, cast_time, flinch_time, motions[6])
    species_data = {}
    for i in range(len(vct_bin) // 26):
        vrec = struct.unpack("<13H", vct_bin[i * 26 : (i + 1) * 26])
        m_idx = vrec[1]
        m_model = models[m_idx] if m_idx < len(models) else ""
        if i < len(btl_bin) // 12:
            u32s = struct.unpack("<3I", btl_bin[i * 12 : (i + 1) * 12])
            attack_t = round(u32s[0] / 65536.0, 3)
            cast_t = round(u32s[1] / 65536.0, 3)
            flinch_t = round(u32s[2] / 65536.0, 3)
        else:
            attack_t, cast_t, flinch_t = 0.0, 0.0, 0.0

        vct_motions = []
        for mot_idx in vrec[2:8]:
            if 0 < mot_idx < len(motions):
                vct_motions.append(motions[mot_idx][0])
            else:
                vct_motions.append("")

        species_data[i] = {
            "species_id": i,
            "model_name": m_model,
            "attack_seconds": attack_t,
            "cast_seconds": cast_t,
            "flinch_seconds": flinch_t,
            "vct_motions": vct_motions,
        }

    # Process all 211 monsters
    monsters_result = {}
    monsters_by_id = {}
    monsters_sorted = sorted(
        [m for m in mapping.values() if m["id"].startswith("m")],
        key=lambda x: x["monster_id"],
    )

    all_clips_index = {}

    for m in monsters_sorted:
        mid = m["monster_id"]
        model_id = m["id"]
        sp = species_data.get(mid, {})

        # Base rig
        vct_mots = sp.get("vct_motions", [])
        base_rig = ""
        for vmot in vct_mots:
            if vmot and "_" in vmot:
                base_rig = vmot.split("_")[0]
                break
        if not base_rig:
            base_rig = model_id.rstrip("abcdefghijklmnopqrstuvwxyz")

        # Available clips in glTF
        clips_in_gltf = gltf_animations_by_model.get(model_id, [])
        if not clips_in_gltf and base_rig in gltf_animations_by_model:
            clips_in_gltf = gltf_animations_by_model[base_rig]

        anim_entries = []
        for cname in clips_in_gltf:
            slot = cname.split("_")[-1] if "_" in cname else cname
            mot_info = motions_by_name.get(cname)
            flag = mot_info[1] if mot_info else 0
            role, is_loop = get_role_and_loop(model_id, slot, flag)
            dur = gltf_durations.get(cname, 0.0)
            is_motionless = cname in motionless_set

            # Timing in combat
            timing_sec = None
            if role == "attack":
                timing_sec = sp.get("attack_seconds")
            elif role == "cast":
                timing_sec = sp.get("cast_seconds")
            elif role == "flinch":
                timing_sec = sp.get("flinch_seconds")

            labels = ROLE_TRANSLATIONS.get(
                role,
                {lang: f"Animation {slot}" for lang in ("en", "fr", "de", "it", "es")},
            )

            entry = {
                "clip_name": cname,
                "slot": slot,
                "role": role,
                "flag": flag,
                "is_looping": is_loop,
                "duration_seconds": dur,
                "frame_count": round(dur * 30),
                "combat_round_seconds": timing_sec,
                "is_motionless": is_motionless,
                "labels": labels,
            }
            anim_entries.append(entry)

            if cname not in all_clips_index:
                all_clips_index[cname] = entry

        # Default idle animation
        default_idle = idle_overrides.get(model_id)
        if not default_idle:
            for a in anim_entries:
                if a["role"] == "idle" and not a["is_motionless"]:
                    default_idle = a["clip_name"]
                    break
        if not default_idle and anim_entries:
            default_idle = anim_entries[0]["clip_name"]

        monster_record = {
            "monster_id": mid,
            "model_id": model_id,
            "name_fr": m.get("nom_fr", ""),
            "name_en": m.get("nom_en", ""),
            "base_rig": base_rig,
            "default_idle": default_idle,
            "combat_timings": {
                "attack_seconds": sp.get("attack_seconds", 0.0),
                "cast_seconds": sp.get("cast_seconds", 0.0),
                "flinch_seconds": sp.get("flinch_seconds", 0.0),
            },
            "animations": anim_entries,
        }
        monsters_result[model_id] = monster_record
        monsters_by_id[str(mid)] = monster_record

    # Also build by_model_id for ALL animated models (including NPCs, Hero, objects)
    models_result = {}
    for mod_id, clips in gltf_animations_by_model.items():
        mod_entries = []
        for cname in clips:
            slot = cname.split("_")[-1] if "_" in cname else cname
            mot_info = motions_by_name.get(cname)
            flag = mot_info[1] if mot_info else 0
            role, is_loop = get_role_and_loop(mod_id, slot, flag)
            dur = gltf_durations.get(cname, 0.0)
            is_motionless = cname in motionless_set
            labels = ROLE_TRANSLATIONS.get(
                role,
                {lang: f"Animation {slot}" for lang in ("en", "fr", "de", "it", "es")},
            )
            entry = {
                "clip_name": cname,
                "slot": slot,
                "role": role,
                "flag": flag,
                "is_looping": is_loop,
                "duration_seconds": dur,
                "frame_count": round(dur * 30),
                "is_motionless": is_motionless,
                "labels": labels,
            }
            mod_entries.append(entry)
            if cname not in all_clips_index:
                all_clips_index[cname] = entry

        default_idle = idle_overrides.get(mod_id)
        if not default_idle:
            for a in mod_entries:
                if a["role"] == "idle" and not a["is_motionless"]:
                    default_idle = a["clip_name"]
                    break
        if not default_idle and mod_entries:
            default_idle = mod_entries[0]["clip_name"]

        models_result[mod_id] = {
            "model_id": mod_id,
            "default_idle": default_idle,
            "animation_count": len(mod_entries),
            "animations": mod_entries,
        }

    output_data = {
        "provenance": (
            "ROM : MotionTbl.bin (File 2834), ViewChrTbl.bin (File 3790), "
            "BtlChrTimeTbl.bin (File 97), ModelTbl.bin (File 2833) "
            "et fichiers squelettes .nsbca convertis en glTF web-ready."
        ),
        "total_monsters": len(monsters_result),
        "total_animated_models": len(models_result),
        "total_unique_clips": len(all_clips_index),
        "role_definitions": ROLE_TRANSLATIONS,
        "by_monster_slug": monsters_result,
        "by_monster_id": monsters_by_id,
        "by_model_id": models_result,
        "all_clips_index": all_clips_index,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(
        f"Genere avec succes : {OUTPUT_FILE} "
        f"({len(monsters_result)} monstres, {len(models_result)} modeles, {len(all_clips_index)} clips uniques)"
    )


if __name__ == "__main__":
    main()
