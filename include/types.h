#ifndef TYPES_H
#define TYPES_H

#include <stddef.h>
#include <stdint.h>

/* Standard fixed-width integer types (Nintendo DS / ARM SDK convention) */
typedef uint8_t   u8;
typedef int8_t    s8;
typedef uint16_t  u16;
typedef int16_t   s16;
typedef uint32_t  u32;
typedef int32_t   s32;
typedef uint64_t  u64;
typedef int64_t   s64;

/* Volatile types for memory-mapped I/O registers */
typedef volatile u8   vu8;
typedef volatile s8   vs8;
typedef volatile u16  vu16;
typedef volatile s16  vs16;
typedef volatile u32  vu32;
typedef volatile s32  vs32;
typedef volatile u64  vu64;
typedef volatile s64  vs64;

/* Floating point types */
typedef float  f32;
typedef double f64;

/* Fixed-point types used across DS 3D graphics and physics engines */
typedef s16 fx16;  /* Format s3.12 */
typedef s32 fx32;  /* Format s19.12 */

/* Boolean type */
typedef int BOOL;

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifndef NULL
#define NULL ((void *)0)
#endif

#endif /* TYPES_H */
