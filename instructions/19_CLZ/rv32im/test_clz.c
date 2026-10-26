#include <stdint.h>
#include <stdio.h>

extern uint32_t clz_rv32im(uint32_t value);

struct test_vector {
    uint32_t input;
    uint32_t expected;
};

static const struct test_vector tests[] = {
    {0x00000000u, 32u},
    {0x00000001u, 31u},
    {0x00000002u, 30u},
    {0x00010000u, 15u},
    {0x0000ffffu, 16u},
    {0x007fffffu, 9u},
    {0x01000000u, 7u},
    {0x40000000u, 1u},
    {0x7fffffffu, 1u},
    {0x80000000u, 0u},
    {0xffffffffu, 0u},
};

int main(void) {
    unsigned int failures = 0;

    for (unsigned int i = 0; i < sizeof(tests) / sizeof(tests[0]); ++i) {
        uint32_t actual = clz_rv32im(tests[i].input);
        printf("0x%08lx -> %lu (expected %lu)%s\n",
               (unsigned long)tests[i].input,
               (unsigned long)actual,
               (unsigned long)tests[i].expected,
               actual == tests[i].expected ? "" : " FAIL");
        if (actual != tests[i].expected) {
            ++failures;
        }
    }

    printf("%u/%u tests passed\n",
           (unsigned int)(sizeof(tests) / sizeof(tests[0])) - failures,
           (unsigned int)(sizeof(tests) / sizeof(tests[0])));
    return failures != 0;
}
