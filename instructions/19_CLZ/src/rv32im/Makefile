CC := riscv32-unknown-elf-gcc
CFLAGS ?= -march=rv32im -mabi=ilp32 -O2 -Wall -Wextra
ASFLAGS ?= -march=rv32im -mabi=ilp32

.PHONY: all clean

all: clz.o clz_loop.o clz_wrapper.o test_clz.o

clz.o: clz.s
	$(CC) $(ASFLAGS) -c -o $@ $<

clz_loop.o: clz_loop.s
	$(CC) $(ASFLAGS) -c -o $@ $<

clz_wrapper.o: clz_wrapper.c clz_wrapper.h
	$(CC) $(CFLAGS) -c -o $@ $<

test_clz.o: test_clz.c clz_wrapper.h
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f *.o
