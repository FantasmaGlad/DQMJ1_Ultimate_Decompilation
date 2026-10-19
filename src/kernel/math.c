#include "global.h"
#include "nds/registers.h"

/*
 * Hardware Division Routine (CP_DIV Coprocessor)
 * Configures the ARM9 mathematical hardware engine for 64-bit / 32-bit division
 */
s64 math_div_hardware(s64 numerator, s32 denominator) {
    if (denominator == 0) {
        return 0;
    }

    /* Set mode to 64-bit / 32-bit signed division */
    REG_CP_DIVCNT = CP_DIVCNT_MODE_64_32;
    REG_CP_DIV_NUMER = (u64)numerator;
    REG_CP_DIV_DENOM = (u64)(u32)denominator;

    /* Poll busy flag until hardware division finishes (typically 36 cycles) */
    while (REG_CP_DIVCNT & CP_DIVCNT_BUSY) {
        /* Wait */
    }

    return (s64)REG_CP_DIV_RESULT;
}
