<<<<<<< Updated upstream:src/clz.c
#include <stdio.h>
#include <stdint.h>

uint32_t clz(uint32_t x)
{
    uint32_t count = 0;

    if (x == 0)
        return 32;

    if ((x & 0xFFFF0000) == 0)
    {
        count += 16;
        x <<= 16;
    }

    if ((x & 0xFF000000) == 0)
    {
        count += 8;
        x <<= 8;
    }

    if ((x & 0xF0000000) == 0)
    {
        count += 4;
        x <<= 4;
    }

    if ((x & 0xC0000000) == 0)
    {
        count += 2;
        x <<= 2;
    }

    if ((x & 0x80000000) == 0)
    {
        count += 1;
    }

    return count;
}

int main(void)
{
    uint32_t tests[10] = {
        0x80000000,
        0x40000000,
        0x20000000,
        0x10000000,
        0x08000000,
        0x01000000,
        0x00100000,
        0x00010000,
        0x00000001,
        0x00000000
    };

    for (int i = 0; i < 10; i++)
    {
        printf("Test %2d: CLZ(0x%08X) = %u\n",
               i + 1, tests[i], clz(tests[i]));
    }

    return 0;
}
=======
#include <stdio.h>
#include <stdint.h>

uint32_t clz(uint32_t x)
{
    uint32_t count = 0;

    if (x == 0)
        return 32;

    if ((x & 0xFFFF0000) == 0)
    {
        count += 16;
        x <<= 16;
    }

    if ((x & 0xFF000000) == 0)
    {
        count += 8;
        x <<= 8;
    }

    if ((x & 0xF0000000) == 0)
    {
        count += 4;
        x <<= 4;
    }

    if ((x & 0xC0000000) == 0)
    {
        count += 2;
        x <<= 2;
    }

    if ((x & 0x80000000) == 0)
    {
        count += 1;
    }

    return count;
}

int main(void)
{
    uint32_t tests[10] = {
        0x80000000,
        0x40000000,
        0x20000000,
        0x10000000,
        0x08000000,
        0x01000000,
        0x00100000,
        0x00010000,
        0x00000001,
        0x00000000
    };

    for (int i = 0; i < 10; i++)
    {
        printf("Test %2d: CLZ(0x%08X) = %u\n",
               i + 1, tests[i], clz(tests[i]));
    }

    return 0;
}
>>>>>>> Stashed changes:src/c_baseline/clz.c
