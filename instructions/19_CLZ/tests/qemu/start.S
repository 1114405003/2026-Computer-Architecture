    .section .text.start
    .globl _start

_start:
    la      sp, _stack_top
    call    main

    # a0 = number of failures.  Exit through the QEMU virt test finisher.
    li      t0, 0x100000
    beqz    a0, 1f
    li      t1, 0x3333
    slli    t2, a0, 16
    or      t1, t1, t2
    sw      t1, 0(t0)
    j       2f
1:
    li      t1, 0x5555
    sw      t1, 0(t0)
2:
    j       2b
