#ifndef GAME_MONSTER_H
#define GAME_MONSTER_H

#include "../types.h"
#include "synthesis.h"

/*
 * Monster species descriptor structure
 * Layout corresponds to EnmyKindTbl.bin verified at ARM9 0x0203a640
 */
typedef struct {
    u16 species_id;             /* 0 to 209 */
    u8  family_id;              /* 0 = Slime, 7 = Incarnus */
    u8  rank_id;                /* 0 = F, 7 = X */
    u16 max_hp_cap;             /* Hard ceiling for HP stat */
    u16 max_mp_cap;             /* Hard ceiling for MP stat */
    u16 max_atk_cap;            /* Hard ceiling for Attack stat */
    u16 max_def_cap;            /* Hard ceiling for Defense stat */
    u16 max_agi_cap;            /* Hard ceiling for Agility stat */
    u16 max_wis_cap;            /* Hard ceiling for Wisdom stat */
    u8  growth_curve_id;        /* Index into level-up growth rate table */
    u8  exp_curve_id;           /* Experience progression tier */
    u8  default_skill_ids[3];   /* Starting skill sets */
    u8  trait_ids[2];           /* Inherent species traits */
    u8  equipment_flags;        /* Allowed weapon classes */
} ALIGN(4) MonsterSpeciesEntry;

#endif /* GAME_MONSTER_H */
