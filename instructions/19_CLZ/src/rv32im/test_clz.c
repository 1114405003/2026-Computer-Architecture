#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "clz_wrapper.h"

struct test_vector {
    uint32_t input;
    uint32_t expected;
    const char *note;
};

static const struct test_vector tests[] = {
    {0x80000000u, 0u,  "bit 31 = 1"},
    {0x40000000u, 1u,  "one leading zero"},
    {0x20000000u, 2u,  "two leading zeros"},
    {0x10000000u, 3u,  "nibble boundary (bit 28)"},
    {0x08000000u, 4u,  "bit 27, four leading zeros"},
    {0x01000000u, 7u,  "byte boundary (bit 24)"},
    {0x00100000u, 11u, "bit 20"},
    {0x00010000u, 15u, "16-bit boundary"},
    {0x00000001u, 31u, "lowest bit is one"},
    {0x00000000u, 32u, "zero boundary"},
    {0x00F00000u, 8u,  "multiple adjacent ones"},
    {0x0000FFFFu, 16u, "low 16 bits are all ones"}
};

static unsigned int run_suite(const char *name, uint32_t (*fn)(uint32_t))
{
    const unsigned int n = (unsigned int)(sizeof(tests) / sizeof(tests[0]));
    unsigned int failures = 0;

    printf("[%s]\n", name);
    for (unsigned int i = 0; i < n; i++) {
        uint32_t actual = fn(tests[i].input);
        int ok = actual == tests[i].expected;

        printf("  Test %2u: CLZ(0x%08" PRIX32 ") = %" PRIu32 " (expected %" PRIu32 ") %s  %s\n",
               i + 1, tests[i].input, actual, tests[i].expected,
               ok ? "PASS" : "FAIL", tests[i].note);
        if (!ok) {
            failures++;
        }
    }
    printf("  %u/%u tests passed.\n", n - failures, n);
    return failures;
}

int main(void)
{
    unsigned int failures = 0;

    failures += run_suite("clz_rv32im (binary search)", clz_rv32im);
    failures += run_suite("clz_loop (bit by bit)", clz_loop);

    return failures == 0 ? 0 : 1;
}
