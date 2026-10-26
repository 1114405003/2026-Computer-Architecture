CC := riscv64-unknown-elf-gcc
CFLAGS := -march=rv32im -mabi=ilp32 -O0 -Wall -Wextra
ASFLAGS := -march=rv32im -mabi=ilp32

.PHONY: all clean

all: clz.o test_clz.o

clz.o: clz.S
	$(CC) $(ASFLAGS) -c -o $@ $<

test_clz.o: test_clz.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f clz.o test_clz.o
