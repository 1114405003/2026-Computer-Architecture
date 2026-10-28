#include <stdint.h>

#define UART0 ((volatile uint8_t *)0x10000000)

extern uint32_t clz_rv32im(uint32_t x);
extern uint32_t clz_loop(uint32_t x);

struct test_vector {
    uint32_t input;
    uint32_t expected;
};

static const struct test_vector tests[] = {
    {0x80000000u, 0u},
    {0x40000000u, 1u},
    {0x20000000u, 2u},
    {0x10000000u, 3u},
    {0x08000000u, 4u},
    {0x01000000u, 7u},
    {0x00100000u, 11u},
    {0x00010000u, 15u},
    {0x00000001u, 31u},
    {0x00000000u, 32u},
    {0x00F00000u, 8u},
    {0x0000FFFFu, 16u}
};

static void putc(char c)
{
    *UART0 = (uint8_t)c;
}

static void puts(const char *s)
{
    while (*s) {
        putc(*s++);
    }
}

static void print_u32(uint32_t value)
{
    char buffer[10];
    int index = 0;

    if (value == 0) {
        putc('0');
        return;
    }
    while (value != 0) {
        buffer[index++] = (char)('0' + (value % 10u));
        value /= 10u;
    }
    while (index != 0) {
        putc(buffer[--index]);
    }
}

static void print_hex32(uint32_t value)
{
    static const char digits[] = "0123456789ABCDEF";

    for (int shift = 28; shift >= 0; shift -= 4) {
        putc(digits[(value >> shift) & 0xFu]);
    }
}

int main(void)
{
    const unsigned int count = (unsigned int)(sizeof(tests) / sizeof(tests[0]));
    unsigned int failures = 0;

    puts("QEMU RV32IM CLZ execution\r\n");
    puts("input        binary  loop  expected  result\r\n");

    for (unsigned int i = 0; i < count; i++) {
        uint32_t binary = clz_rv32im(tests[i].input);
        uint32_t loop = clz_loop(tests[i].input);
        int ok = binary == tests[i].expected && loop == tests[i].expected;

        puts("0x");
        print_hex32(tests[i].input);
        puts("  ");
        print_u32(binary);
        puts("  ");
        print_u32(loop);
        puts("  ");
        print_u32(tests[i].expected);
        puts(ok ? "  PASS\r\n" : "  FAIL\r\n");

        if (!ok) {
            failures++;
        }
    }

    print_u32(count - failures);
    putc('/');
    print_u32(count);
    puts(" tests passed\r\n");

    return (int)failures;
}
