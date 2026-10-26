#include <stdint.h>
#include <stdio.h>

#include "clz_wrapper.h"

uint32_t clz_rv32im(uint32_t x)
{
    /* Reference to the assembly implementation in clz.s. */
    extern uint32_t clz(uint32_t x);
    return clz(x);
}

int main(void)
{
    const uint32_t tests[] = {
        0x80000000u, 0x40000000u, 0x20000000u, 0x10000000u,
        0x08000000u, 0x01000000u, 0x00100000u, 0x00010000u,
        0x00000001u, 0x00000000u
    };

    for (size_t i = 0; i < sizeof(tests) / sizeof(tests[0]); i++)
    {
        printf("Test %2zu: CLZ(0x%08X) = %u (custom = %u)\n",
               i + 1, tests[i],
               clz_rv32im(tests[i]),
               clz_insn(tests[i]));
    }
    return 0;
}
