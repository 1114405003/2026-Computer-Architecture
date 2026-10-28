# QEMU RV32IM 執行證據

本資料夾用真正的 RISC-V 工具鏈組譯 `src/rv32im/clz.s` 與
`src/rv32im/clz_loop.s`，再放進 QEMU 的 `virt` 機器執行。這不是 Python
runner，而是實際的 RV32IM 機器碼。

## 工具

| 項目 | 版本 |
|---|---|
| `riscv32-unknown-elf-gcc` | 14.2.0 |
| `qemu-system-riscv32` | 11.1.2 |

## 建置

從 `instructions/19_CLZ` 執行：

```text
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -ffreestanding -fno-builtin -nostdlib -nostartfiles -T tests/qemu/link.ld -o tests/qemu/clz_qemu.elf tests/qemu/start.S src/rv32im/clz.s src/rv32im/clz_loop.s tests/qemu/test_qemu.c
```

## 執行

```text
qemu-system-riscv32 -machine virt -cpu rv32 -bios none -kernel tests/qemu/clz_qemu.elf -nographic -no-reboot
```

程式透過 UART（`0x10000000`）輸出，最後用 QEMU `virt` 的 test finisher
（`0x100000`）結束。

## 輸出

- [`../qemu_output.txt`](../qemu_output.txt)：QEMU 執行結果。
- [`../qemu_disassembly.txt`](../qemu_disassembly.txt)：`objdump -d` 反組譯。
- [`../qemu_size.txt`](../qemu_size.txt)：ELF section 大小。

> `clz_wrapper.h` 的 `.insn` custom-0 指令沒有在這個 QEMU 模型中實作，
> 因此 QEMU 測試只執行兩個標準 RV32IM baseline，不執行 custom opcode。
