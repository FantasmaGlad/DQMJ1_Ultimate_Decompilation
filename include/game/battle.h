#ifndef GAME_BATTLE_H
#define GAME_BATTLE_H

#include "../types.h"

/*
 * Scouting / Taming calculation parameters
 * Reverse-engineered from overlay_0001:0x92924
 */
typedef struct {
    u16 team_attack_total;      /* Total effective attack power of the scout attempt */
    u16 target_defense;         /* Defense stat of the target wild monster */
    u8  tension_tier;           /* 0: Normal, 1: 5, 2: 20, 3: 50, 4: 100 */
    u8  oomph_active;           /* 1 if Oomph buff applied, 0 otherwise */
    u16 target_max_hp;          /* Maximum HP of the wild monster */
    u8  target_rank;            /* Rank tier (0 = F, ..., 7 = X) */
    u8  target_family;          /* Family ID */
    u8  prior_scout_attempts;   /* Number of prior scouts in current encounter */
} ScoutParameters;

/*
 * Calculates scouting success probability percentage (0 to 100%).
 *
 * @param params Input combat state and monster attributes
 * @return Probability in basis points (0 to 10000, representing 0.00% to 100.00%)
 */
u32 scout_rate_calculate(const ScoutParameters *params);

/*
 * Damage calculation parameters
 */
typedef struct {
    u16 attacker_stat;          /* Attack (physical) or Wisdom (spell) */
    u16 defender_defense;       /* Defense stat or Spell resistance */
    u8  tension_multiplier;     /* Tension damage multiplier */
    u8  element_affinity;       /* 0: Weak (+25%), 1: Normal, 2: Resistant (-50%), 3: Immune, 4: Absorb */
    u16 base_power;             /* Ability / spell base power coefficient */
} DamageParameters;

/*
 * Calculates final combat damage dealt.
 */
s32 battle_damage_calculate(const DamageParameters *params);

#endif /* GAME_BATTLE_H */
