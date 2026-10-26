# RV32IM baseline for CLZ(x) (input/output in a0)
# Only RV32I instructions are used.

    .text
    .globl clz
clz:
    beq   a0, zero, .Lclz_zero   # x == 0
    addi  t0, zero, 0           # count = 0

    srli  t1, a0, 16            # high 16 bits?
    bnez  t1, 1f
    addi  t0, t0, 16
    slli  a0, a0, 16
1:
    srli  t1, a0, 24            # next 8 bits?
    bnez  t1, 2f
    addi  t0, t0, 8
    slli  a0, a0, 8
2:
    srli  t1, a0, 28            # next 4 bits?
    bnez  t1, 3f
    addi  t0, t0, 4
    slli  a0, a0, 4
3:
    srli  t1, a0, 30            # next 2 bits?
    bnez  t1, 4f
    addi  t0, t0, 2
    slli  a0, a0, 2
4:
    srli  t1, a0, 31            # last bit?
    bnez  t1, 5f
    addi  t0, t0, 1
5:
    addi  a0, t0, 0            # mv a0, t0
    ret

.Lclz_zero:
    addi  a0, zero, 32
    ret
