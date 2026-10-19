#ifndef NDS_REGISTERS_H
#define NDS_REGISTERS_H

#include "../types.h"
#include "memory.h"

/*
 * Nintendo DS Hardware I/O Registers (ARM9)
 */

/* Math Acceleration Engine: Division (CP_DIV) */
#define REG_CP_DIVCNT           HW_REG(0x04000280, vu32)
#define REG_CP_DIV_NUMER        HW_REG(0x04000290, vu64)
#define REG_CP_DIV_DENOM        HW_REG(0x04000298, vu64)
#define REG_CP_DIV_RESULT       HW_REG(0x040002A0, vu64)
#define REG_CP_DIV_REM          HW_REG(0x040002A8, vu64)

#define CP_DIVCNT_MODE_32_32    0x00000000
#define CP_DIVCNT_MODE_64_32    0x00000001
#define CP_DIVCNT_MODE_64_64    0x00000002
#define CP_DIVCNT_BUSY          0x00008000

/* Math Acceleration Engine: Square Root (CP_SQRT) */
#define REG_CP_SQRTCNT          HW_REG(0x040002B0, vu32)
#define REG_CP_SQRT_PARAM       HW_REG(0x040002B8, vu64)
#define REG_CP_SQRT_RESULT      HW_REG(0x040002C0, vu32)

#define CP_SQRTCNT_MODE_32      0x00000000
#define CP_SQRTCNT_MODE_64      0x00000001
#define CP_SQRTCNT_BUSY         0x00008000

/* Direct Memory Access (DMA0 - DMA3) */
#define REG_DMA0SAD             HW_REG(0x040000B0, vu32)
#define REG_DMA0DAD             HW_REG(0x040000B4, vu32)
#define REG_DMA0CNT             HW_REG(0x040000B8, vu32)

#define REG_DMA3SAD             HW_REG(0x040000D4, vu32)
#define REG_DMA3DAD             HW_REG(0x040000D8, vu32)
#define REG_DMA3CNT             HW_REG(0x040000DC, vu32)

/* Interrupt Master & Masks */
#define REG_IME                 HW_REG(0x04000208, vu16)
#define REG_IE                  HW_REG(0x04000210, vu32)
#define REG_IF                  HW_REG(0x04000214, vu32)

/* Display & VRAM Status */
#define REG_DISPCNT             HW_REG(0x04000000, vu32)
#define REG_DISPSTAT            HW_REG(0x04000004, vu16)
#define REG_VCOUNT              HW_REG(0x04000006, vu16)

#endif /* NDS_REGISTERS_H */
