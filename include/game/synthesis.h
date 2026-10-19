#ifndef GAME_SYNTHESIS_H
#define GAME_SYNTHESIS_H

#include "../types.h"

/*
 * Monster Families (8 core families in DQMJ1)
 */
typedef enum {
    FAMILY_SLIME    = 0,
    FAMILY_DRAGON   = 1,
    FAMILY_NATURE   = 2,
    FAMILY_BEAST    = 3,
    FAMILY_MATERIAL = 4,
    FAMILY_DEMON    = 5,
    FAMILY_UNDEAD   = 6,
    FAMILY_INCARNUS = 7
} MonsterFamily;

/*
 * Monster Ranks (F through X)
 */
typedef enum {
    RANK_F = 0,
    RANK_E = 1,
    RANK_D = 2,
    RANK_C = 3,
    RANK_B = 4,
    RANK_A = 5,
    RANK_S = 6,
    RANK_X = 7
} MonsterRank;

/*
 * Synthesis candidate produced by evaluation
 */
typedef struct {
    u16 species_id;
    u8  formula_type;   /* 0: Generic family/rank, 1: Specific monster pair, 2: Special recipe */
    u8  flags;          /* Trait inheritance / special status */
} SynthesisCandidate;

/*
 * Output candidate structure (up to 3 offerings shown to player)
 */
typedef struct {
    u8 count;
    SynthesisCandidate candidates[3];
} SynthesisResult;

/*
 * Evaluates synthesis options between two parent monsters.
 * Reverse-engineered from overlay_0000:FUN_0218bee8.
 *
 * @param parent_a_id Species ID of the first parent (positive / charge)
 * @param parent_b_id Species ID of the second parent (negative / charge)
 * @param out_result  Pointer to receive the generated offspring candidates
 * @return TRUE if valid synthesis choices were found, FALSE otherwise.
 */
BOOL synthesis_evaluate(u16 parent_a_id, u16 parent_b_id, SynthesisResult *out_result);

/*
 * Evaluates 4-parent quadrilinear synthesis combinations.
 * Reverse-engineered from overlay_0000:FUN_0218c150.
 *
 * @param gp_a1 Grandparent A1 species ID
 * @param gp_a2 Grandparent A2 species ID
 * @param gp_b1 Grandparent B1 species ID
 * @param gp_b2 Grandparent B2 species ID
 * @return Offspring species ID, or 0 if no 4-parent recipe matches.
 */
u16 synthesis_resolve_quadrilinear(u16 gp_a1, u16 gp_a2, u16 gp_b1, u16 gp_b2);

#endif /* GAME_SYNTHESIS_H */
