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