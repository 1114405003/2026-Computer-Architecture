# uint32_t clz_loop(uint32_t value)
# a0: input value and return value
# t0: leading-zero count
# t1: temporary bit value
#
# Bit-by-bit baseline: shift left until the original MSB reaches bit 31.
# This version is included only for the CP2 implementation comparison.
    .text
    .align 2
    .globl clz_loop
    .type clz_loop, @function

clz_loop:
    beq     a0, zero, .Lloop_zero
    addi    t0, zero, 0

.Lloop_test:
    srli    t1, a0, 31
    bnez    t1, .Lloop_done
    addi    t0, t0, 1
    slli    a0, a0, 1
    jal     zero, .Lloop_test

.Lloop_done:
    addi    a0, t0, 0
    ret

.Lloop_zero:
    addi    a0, zero, 32
    ret

    .size clz_loop, .-clz_loop
