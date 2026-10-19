#!/usr/bin/env python3
"""Extrait l'ensemble des regles et patterns d'Intelligence Artificielle de combat depuis les 7 tables AI_*.

Structure prouvee par desassemblage (overlay_0001, chargeur a 0x02204474, evaluateur a 0x022045d0) :
- AI_PatternTbl.bin : 31 440 octets = 131 patrons de comportement de 240 octets (40 etapes de 6 octets).
  Chaque etape : u16 action_id, u16 poids/priorite, u16 condition_flags (0x8000 = conditionnel, 0xffff = terminateur).
- AI_ActionTBL.bin : 256 octets = categorie tactique pour chacune des 256 actions (0..255).
- AI_CorrectTbl.bin : 2 048 octets = 256 entrees x 8 octets (4 x s16), ponderations de situation tactique.
- AI_IntelTBL.bin : 2 560 octets = 256 entrees x 10 octets, indicateurs booleens de tactique/intelligence.
- AI_TargetSelectAllyTbl.bin : 1 280 octets = 256 entrees x 5 octets, regles de ciblage des allies.
- AI_TargetSelectEnemyTbl.bin : 768 octets = 256 entrees x 3 octets, regles de ciblage des ennemis.
- AI_TargetSelectItemTbl.bin : 32 octets, regles de selection pour les objets de combat.
- message0.bin* (indices 600..855) : Noms officiels des 256 actions/sorts dans les 5 langues (E, F, D, I, S).
"""

import json
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")
BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire")

sys.path.insert(0, os.path.join(RACINE, "tools"))
from extract_mapping import decode  # noqa: E402

LANGUAGES = ["en", "fr", "de", "it", "es"]
LANG_SUFFIXES = {"en": "E", "fr": "F", "de": "D", "it": "I", "es": "S"}


def clean_str(s):
    import re
    s = re.sub(r"<[0-9a-f]{2}>", "", s)
    return s.strip("'").strip()


def load_action_names():
    names = {lang: {} for lang in LANGUAGES}
    for lang, sfx in LANG_SUFFIXES.items():
        p = os.path.join(DATA, f"message0.bin{sfx}")
        if os.path.exists(p):
            with open(p, "rb") as f:
                raw = f.read()
            items = [clean_str(x) for x in decode(raw).split("|")]
            for i in range(256):
                idx = 600 + i
                if idx < len(items) and items[idx]:
                    names[lang][i] = items[idx]
                else:
                    names[lang][i] = f"Action_{i}"
    return names


def main():
    action_names = load_action_names()

    # 1. AI_ActionTBL.bin
    with open(os.path.join(DATA, "AI_ActionTBL.bin"), "rb") as f:
        action_tbl = f.read()

    # 2. AI_CorrectTbl.bin
    with open(os.path.join(DATA, "AI_CorrectTbl.bin"), "rb") as f:
        correct_tbl = f.read()

    # 3. AI_IntelTBL.bin
    with open(os.path.join(DATA, "AI_IntelTBL.bin"), "rb") as f:
        intel_tbl = f.read()

    # 4. AI_TargetSelectAllyTbl.bin
    with open(os.path.join(DATA, "AI_TargetSelectAllyTbl.bin"), "rb") as f:
        target_ally = f.read()

    # 5. AI_TargetSelectEnemyTbl.bin
    with open(os.path.join(DATA, "AI_TargetSelectEnemyTbl.bin"), "rb") as f:
        target_enemy = f.read()

    # 6. AI_TargetSelectItemTbl.bin
    with open(os.path.join(DATA, "AI_TargetSelectItemTbl.bin"), "rb") as f:
        target_item = f.read()

    # 7. AI_PatternTbl.bin
    with open(os.path.join(DATA, "AI_PatternTbl.bin"), "rb") as f:
        pat_data = f.read()

    # Assembler les 256 actions
    actions = []
    for i in range(256):
        cat = action_tbl[i] if i < len(action_tbl) else 0
        corr = list(struct.unpack_from("<4h", correct_tbl, i * 8)) if (i * 8 + 8) <= len(correct_tbl) else [0, 0, 0, 0]
        intel = list(intel_tbl[i * 10 : (i + 1) * 10]) if (i + 1) * 10 <= len(intel_tbl) else [0] * 10
        ally = list(target_ally[i * 5 : (i + 1) * 5]) if (i + 1) * 5 <= len(target_ally) else [0] * 5
        enemy = list(target_enemy[i * 3 : (i + 1) * 3]) if (i + 1) * 3 <= len(target_enemy) else [0] * 3

        actions.append({
            "action_id": i,
            "names": {lang: action_names[lang].get(i, f"Action_{i}") for lang in LANGUAGES},
            "category": cat,
            "tactical_corrections": corr,
            "tactical_intel_flags": intel,
            "target_ally_rules": ally,
            "target_enemy_rules": enemy,
        })

    # Assembler les 131 patterns
    num_patterns = len(pat_data) // 240
    patterns = []
    for p_idx in range(num_patterns):
        block = pat_data[p_idx * 240 : (p_idx + 1) * 240]
        steps = []
        for s_idx in range(40):
            action_id, weight, cond = struct.unpack_from("<3H", block, s_idx * 6)
            if action_id == 0xFFFF:
                # Terminateur de sequence
                break
            if action_id == 0 and weight == 0 and cond == 0:
                continue

            name_dict = {lang: action_names[lang].get(action_id, f"Action_{action_id}") for lang in LANGUAGES}
            steps.append({
                "step_index": s_idx,
                "action_id": action_id,
                "names": name_dict,
                "weight": weight,
                "condition_raw": cond,
                "is_conditional": (cond & 0x8000) != 0,
            })
        patterns.append({
            "pattern_id": p_idx,
            "steps_count": len(steps),
            "steps": steps,
        })

    output_data = {
        "provenance": "ROM: 7 tables AI_*.bin, overlay_0001 (0x02204474, 0x022045d0) et message0.bin* via tools/extract_battle_ai.py",
        "description": "Profils decisionnels tactiques complets de l'Intelligence Artificielle de combat de DQMJ1",
        "total_actions": len(actions),
        "total_patterns": len(patterns),
        "target_item_rules": list(target_item),
        "actions": actions,
        "patterns": patterns,
    }

    out_paths = [
        os.path.join(RACINE, "assets/data/monster_ai_profiles.json"),
        os.path.join(BESTIAIRE, "assets/data/monster_ai_profiles.json"),
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Exporte avec succes : {p}")


if __name__ == "__main__":
    main()
