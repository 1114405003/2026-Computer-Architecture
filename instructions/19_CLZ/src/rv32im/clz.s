# uint32_t clz_rv32im(uint32_t value)
# a0: input value and return value
# t0: accumulated leading-zero count
# t1: temporary shifted value
#
# Binary-search baseline: check 16, 8, 4, 2, 1 bit groups.
    .text
    .align 2
    .globl clz_rv32im
    .type clz_rv32im, @function

clz_rv32im:
    beq     a0, zero, .Lclz_zero
    addi    t0, zero, 0

    srli    t1, a0, 16
    bnez    t1, .Lclz_8
    addi    t0, t0, 16
    slli    a0, a0, 16

.Lclz_8:
    srli    t1, a0, 24
    bnez    t1, .Lclz_4
    addi    t0, t0, 8
    slli    a0, a0, 8

.Lclz_4:
    srli    t1, a0, 28
    bnez    t1, .Lclz_2
    addi    t0, t0, 4
    slli    a0, a0, 4

.Lclz_2:
    srli    t1, a0, 30
    bnez    t1, .Lclz_1
    addi    t0, t0, 2
    slli    a0, a0, 2

.Lclz_1:
    srli    t1, a0, 31
    bnez    t1, .Lclz_done
    addi    t0, t0, 1

.Lclz_done:
    addi    a0, t0, 0
    ret

.Lclz_zero:
    addi    a0, zero, 32
    ret

    .size clz_rv32im, .-clz_rv32im
