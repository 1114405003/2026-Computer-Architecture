#ifndef CLZ_WRAPPER_H
#define CLZ_WRAPPER_H

#include <stdint.h>

uint32_t clz_rv32im(uint32_t x);

/* clz rd, rs1 : rd = CLZ(rs1) (custom-0, R-type, funct3=5, funct7=0, rs2=0) */
static inline uint32_t clz_insn(uint32_t x)
{
#if defined(__riscv)
    uint32_t rd;
    __asm__ volatile(".insn r 0x0b, 5, 0, %0, %1, %2"
                     : "=r"(rd)
                     : "r"(x), "r"(0));
    return rd;
#else
    return clz_rv32im(x);
#endif
}

#endif
