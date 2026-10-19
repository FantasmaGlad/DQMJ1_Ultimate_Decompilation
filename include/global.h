#ifndef GLOBAL_H
#define GLOBAL_H

#include "types.h"

/* Compiler attributes and memory alignment macros */
#if defined(__GNUC__)
    #define ALIGN(n)    __attribute__((aligned(n)))
    #define PACKED      __attribute__((packed))
    #define INLINE      static inline
    #define NOINLINE    __attribute__((noinline))
    #define SECTION(s)  __attribute__((section(s)))
#elif defined(__MWERKS__)
    #define ALIGN(n)    /* MWCC alignment directive */
    #define PACKED      /* MWCC packed pragma */
    #define INLINE      inline
    #define NOINLINE    __declspec(noinline)
    #define SECTION(s)  /* MWCC section pragma */
#else
    #define ALIGN(n)
    #define PACKED
    #define INLINE      static inline
    #define NOINLINE
    #define SECTION(s)
#endif

/* Array and math macros */
#define ARRAY_COUNT(arr) (sizeof(arr) / sizeof((arr)[0]))
#define MIN(a, b)        (((a) < (b)) ? (a) : (b))
#define MAX(a, b)        (((a) > (b)) ? (a) : (b))
#define CLAMP(v, min, max) (((v) < (min)) ? (min) : (((v) > (max)) ? (max) : (v)))

/* Memory mapped register accessor */
#define HW_REG(addr, type) (*(volatile type *)(addr))

#endif /* GLOBAL_H */
