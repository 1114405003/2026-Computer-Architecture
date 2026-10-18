# CP2: RV32IM CLZ implementation
# Input:  a0 = 32-bit value
# Output: a0 = number of leading zero bits

    .text
    .globl clz
    .type clz, @function

clz:
    beq     a0, zero, .Lzero
    addi    t0, zero, 0

    srli    t1, a0, 16
    bne     t1, zero, .Lcheck8
    addi    t0, t0, 16
    slli    a0, a0, 16

.Lcheck8:
    srli    t1, a0, 24
    bne     t1, zero, .Lcheck4
    addi    t0, t0, 8
    slli    a0, a0, 8

.Lcheck4:
    srli    t1, a0, 28
    bne     t1, zero, .Lcheck2
    addi    t0, t0, 4
    slli    a0, a0, 4

.Lcheck2:
    srli    t1, a0, 30
    bne     t1, zero, .Lcheck1
    addi    t0, t0, 2
    slli    a0, a0, 2

.Lcheck1:
    srli    t1, a0, 31
    bne     t1, zero, .Ldone
    addi    t0, t0, 1

.Ldone:
    addi    a0, t0, 0
    jalr    zero, 0(ra)

.Lzero:
    addi    a0, zero, 32
    jalr    zero, 0(ra)

    .size clz, .-clz
