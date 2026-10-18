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
    const uint32_t expected[] = {
        0, 1, 2, 3, 4, 7, 11, 15, 31, 32
    };
    const size_t test_count = sizeof(tests) / sizeof(tests[0]);
    size_t passed = 0;

    for (size_t i = 0; i < test_count; i++)
    {
        const uint32_t actual = clz(tests[i]);
        const int is_pass = actual == expected[i];

        printf("Test %2zu: CLZ(0x%08X) = %u (expected %u) %s\n",
               i + 1, tests[i], actual, expected[i],
               is_pass ? "PASS" : "FAIL");
        if (is_pass)
            passed++;
    }

    printf("%zu/%zu tests passed.\n", passed, test_count);
    return passed == test_count ? 0 : 1;
}
