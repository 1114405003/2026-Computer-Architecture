.section .text
.align 2
.globl clz_rv32im
.type clz_rv32im, @function

# uint32_t clz_rv32im(uint32_t value)
# a0: input value and return value
# t0: accumulated leading-zero count
# t1: temporary shifted value
clz_rv32im:
    beq     a0, zero, .Lzero
    addi    t0, zero, 0

    # If the upper 16 bits are zero, move the lower half upward.
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

.size clz_rv32im, .-clz_rv32im
