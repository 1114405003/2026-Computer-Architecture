#ifndef CLZ_WRAPPER_H
#define CLZ_WRAPPER_H

#include <stdint.h>

/* RV32IM binary-search baseline implemented in clz.s. */
uint32_t clz_rv32im(uint32_t x);

/* Bit-by-bit baseline implemented in clz_loop.s (used for comparison). */
uint32_t clz_loop(uint32_t x);

/* clz rd, rs1 : rd = CLZ(rs1)
 * custom-0, R-type, funct3 = 000, funct7 = 0000000, rs2 = x0.
 */
static inline uint32_t clz_insn(uint32_t x)
{
#if defined(__riscv)
    uint32_t rd;
    __asm__ volatile(".insn r 0x0b, 0, 0, %0, %1, %2"
                     : "=r"(rd)
                     : "r"(x), "r"(0));
    return rd;
#else
    /* Host-side fallback: use the RV32IM baseline for syntax checking. */
    return clz_rv32im(x);
#endif
}

/* Non-inline wrapper used by test_clz.c and by C callers. */
uint32_t clz_via_wrapper(uint32_t x);

#endif
