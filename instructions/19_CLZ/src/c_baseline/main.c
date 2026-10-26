#include <stdint.h>
#include <stdio.h>

uint32_t clz(uint32_t x);

int main(void)
{
    const uint32_t tests[] = {
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
    const size_t test_count = sizeof(tests) / sizeof(tests[0]);

    for (size_t i = 0; i < test_count; i++)
    {
        printf("Test %2zu: CLZ(0x%08X) = %u\n",
               i + 1, tests[i], clz(tests[i]));
    }

    return 0;
}
