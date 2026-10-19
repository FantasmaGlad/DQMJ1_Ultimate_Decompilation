#include "game/battle.h"

/*
 * Scouting / Taming Formula Calculation
 * Reverse-engineered from overlay_0001:0x92924
 *
 * The scouting success rate is determined by comparing the effective attack
 * dealt by the active team against the wild monster's defense and max HP,
 * multiplied by tension tier modifiers and prior failure penalties.
 */

static const u16 sTensionMultipliers[5] = {
    100,  /* Normal: 1.00x */
    120,  /* 5:      1.20x */
    170,  /* 20:     1.70x */
    250,  /* 50:     2.50x */
    350   /* 100:    3.50x */
};

u32 scout_rate_calculate(const ScoutParameters *params) {
    u32 effective_attack;
    u32 rate;
    u16 tension_mult;

    if (params == NULL || params->target_defense == 0 || params->target_max_hp == 0) {
        return 0;
    }

    effective_attack = (u32)params->team_attack_total;

    /* Oomph increases effective attack by 25% */
    if (params->oomph_active) {
        effective_attack = (effective_attack * 125) / 100;
    }

    /* Tension multiplier */
    tension_mult = (params->tension_tier < 5) ? sTensionMultipliers[params->tension_tier] : 100;
    effective_attack = (effective_attack * tension_mult) / 100;

    /* Base ratio: (effective_attack * 1000) / (defense + max_hp / 2) */
    rate = (effective_attack * 1000) / ((u32)params->target_defense + (params->target_max_hp / 2));

    /* Repeat attempt penalty: rate drops with successive attempts in same encounter */
    if (params->prior_scout_attempts > 0) {
        u32 penalty = params->prior_scout_attempts * 15;
        if (penalty >= 90) {
            penalty = 90;
        }
        rate = (rate * (100 - penalty)) / 100;
    }

    /* Cap at 100.00% (10000 basis points) */
    if (rate > 10000) {
        rate = 10000;
    }

    return rate;
}
