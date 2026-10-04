#!/usr/bin/env python3
"""Génère la table d'attaque calculée par niveau (1 à 99) pour les 211 monstres de DQMJ1.

Utilisé par le calculateur de dressage (ScoutCalculator.tsx) pour permettre
de sélectionner un monstre attaquant et son niveau, et obtenir instantanément
son attaque concrète et son pourcentage de capture.

Sources ROM vérifiées :
- EnmyKindTbl.bin : plafonds de statistiques (attack_limit / bred_max)
- AbilityTbl.bin : courbes de croissance et patterns par niveau (monster_level_growth.json)
- BtlEnmyPrm.bin : stats d'encounters sauvages (monster_battle_encounters.json)
"""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RE = os.path.join(RACINE, "assets/data")
DATA_WEB = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire/assets/data")

def growth_range(lvl: int) -> tuple[int, int]:
    if lvl <= 10:
        return 0, lvl - 1
    if lvl <= 40:
        return 1, lvl - 10 - 1
    if lvl <= 50:
        return 2, lvl - 40 - 1
    return 3, lvl - 50 - 1

def main():
    mapping_path = os.path.join(DATA_WEB, "monsters-mapping.json")
    growth_path = os.path.join(DATA_WEB, "monster_level_growth.json")
    species_path = os.path.join(DATA_WEB, "monster_species_stats.json")
    encounters_path = os.path.join(DATA_WEB, "monster_battle_encounters.json")

    with open(mapping_path, encoding="utf-8") as f:
        mapping = json.load(f)
    with open(growth_path, encoding="utf-8") as f:
        gr = json.load(f)
    with open(species_path, encoding="utf-8") as f:
        sp = json.load(f)
    with open(encounters_path, encoding="utf-8") as f:
        be = json.load(f)

    patterns = gr["patterns"]
    by_monster = gr["by_monster"]

    result = {}
    for m_id, m_info in sorted(mapping.items()):
        if not m_id.startswith("m"):
            continue

        name_fr = m_info.get("nom_fr") or m_info.get("name", m_id)
        name_en = m_info.get("nom_en", name_fr)

        sp_info = sp.get(m_id, {})
        cap = sp_info.get("attack_limit", 999)

        # Recherche de la stat de base sauvage minimale
        encs = be.get(m_id, [])
        scoutable = [e for e in encs if e.get("scout_chance_raw", 0) > 0]
        if scoutable:
            base_enc = min(scoutable, key=lambda x: x.get("level", 1))
            base_lvl = base_enc.get("level", 1)
            base_atk = base_enc.get("attack", 10)
        elif encs:
            base_enc = min(encs, key=lambda x: x.get("level", 1))
            base_lvl = base_enc.get("level", 1)
            base_atk = base_enc.get("attack", 10)
        else:
            base_lvl = 1
            base_atk = 10

        gr_entry = by_monster.get(m_id)
        attack_by_lvl = []

        if gr_entry and "attack" in gr_entry["patterns"]:
            atk_pats = gr_entry["patterns"]["attack"]
            cum = 0
            cum_list = [0]  # niveau 1 = offset 0
            for lvl in range(2, 100):
                r, idx = growth_range(lvl)
                pid = atk_pats[r]
                growth = patterns[str(pid)][r][idx]
                cum += growth
                cum_list.append(cum)

            base_cum = cum_list[min(len(cum_list) - 1, max(0, base_lvl - 1))]
            for lvl in range(1, 100):
                cur_cum = cum_list[lvl - 1]
                diff = cur_cum - base_cum
                calc_atk = max(1, min(cap, base_atk + diff))
                attack_by_lvl.append(calc_atk)
        else:
            # Fallback linéaire si courbe non répertoriée
            for lvl in range(1, 100):
                calc_atk = max(1, min(cap, base_atk + int((lvl - base_lvl) * (cap - base_atk) / 98)))
                attack_by_lvl.append(calc_atk)

        result[m_id] = {
            "id": m_id,
            "name_fr": name_fr,
            "name_en": name_en,
            "cap": cap,
            "base_level": base_lvl,
            "base_attack": base_atk,
            "attack_by_level": attack_by_lvl,
        }

    for target_dir in [DATA_RE, DATA_WEB]:
        os.makedirs(target_dir, exist_ok=True)
        out_path = os.path.join(target_dir, "monster_attack_by_level.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print(f"Généré : {out_path} ({len(result)} monstres)")

if __name__ == "__main__":
    main()
