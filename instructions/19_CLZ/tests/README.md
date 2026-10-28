# CLZ 測試資料

本資料夾包含 CP1、CP2、CP3 的測試向量、預期輸出、實際輸出與執行證據。
所有指令都從 `instructions/19_CLZ` 目錄執行。

## 檔案索引

| 檔案 | 說明 |
|---|---|
| [`test_vectors.txt`](./test_vectors.txt) | 12 組 CLZ 輸入向量 |
| [`expected_output.txt`](./expected_output.txt) | C baseline 的預期輸出 |
| [`actual_output.txt`](./actual_output.txt) | 實際編譯執行後的輸出 |
| [`cp2_trace.py`](./cp2_trace.py) | CP2 RV32I 指令層級 trace runner |
| [`cp2_trace_output.txt`](./cp2_trace_output.txt) | CP2 動態指令數與分支數輸出 |
| [`cp2_trace_detail.txt`](./cp2_trace_detail.txt) | `0x00010000` 的逐條 trace |
| [`qemu/`](./qemu/) | QEMU RV32IM 執行用的 startup、linker script 與測試程式 |
| [`qemu_output.txt`](./qemu_output.txt) | QEMU 實際執行輸出（12/12 PASS） |
| [`qemu_disassembly.txt`](./qemu_disassembly.txt) | QEMU ELF 的 RV32IM 反組譯 |
| [`qemu_size.txt`](./qemu_size.txt) | QEMU ELF 的 section 大小 |
| [`cp3_test.py`](./cp3_test.py) | CP3 語意、編碼與 `rd = x0` 測試 |
| [`cp3_test_output.txt`](./cp3_test_output.txt) | CP3 測試輸出 |
| [`cp3_encoding_output.txt`](./cp3_encoding_output.txt) | encoder / decoder / golden model 輸出 |
| [`EVIDENCE.md`](./EVIDENCE.md) | 工具版本、執行指令與限制 |

## 測試向量（12 組）

| 測試 | 輸入 | 預期 CLZ | 說明 |
|---:|---|---:|---|
| 1 | `0x80000000` | 0 | bit 31 = 1 |
| 2 | `0x40000000` | 1 | 1 個前導零 |
| 3 | `0x20000000` | 2 | 2 個前導零 |
| 4 | `0x10000000` | 3 | nibble 邊界（bit 28） |
| 5 | `0x08000000` | 4 | bit 27，4 個前導零 |
| 6 | `0x01000000` | 7 | byte 邊界（bit 24） |
| 7 | `0x00100000` | 11 | bit 20 |
| 8 | `0x00010000` | 15 | 16-bit 邊界 |
| 9 | `0x00000001` | 31 | 最低位元為 1 |
| 10 | `0x00000000` | 32 | 全零邊界 |
| 11 | `0x00F00000` | 8 | 多個相鄰位元為 1 |
| 12 | `0x0000FFFF` | 16 | 低 16 位元全為 1 |

## 執行方式

### CP1：C baseline

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
./clz.exe
```

預期最後一行：`12/12 tests passed.`

### CP2：QEMU 實際執行

```text
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -ffreestanding -fno-builtin -nostdlib -nostartfiles -T tests/qemu/link.ld -o tests/qemu/clz_qemu.elf tests/qemu/start.S src/rv32im/clz.s src/rv32im/clz_loop.s tests/qemu/test_qemu.c
qemu-system-riscv32 -machine virt -cpu rv32 -bios none -kernel tests/qemu/clz_qemu.elf -nographic -no-reboot
```

預期最後一行：`12/12 tests passed`

### CP2：指令數 trace

```text
python tests/cp2_trace.py
python tests/cp2_trace.py --detail 0x00010000
```

預期最後一行：`CP2 RV32I trace tests passed.`

### CP3：語意與編碼

```text
python tests/cp3_test.py
python spec/clz_encoding.py
```

預期最後一行：`9/9 CP3 tests passed.`

## 邊界值

- `0x80000000`：最高位元為 1，CLZ = 0。
- `0x00000001`：只有最低位元為 1，CLZ = 31。
- `0x00000000`：全零輸入，依規格 CLZ = 32。

## 注意

- 本資料夾沒有巢狀重複目錄。
- `CONTRIBUTIONS.md` 位於 `instructions/19_CLZ/CONTRIBUTIONS.md`，不在 `tests/`。

## 終端截圖

報告引用的終端機截圖放在 [`../report/figures/`](../report/figures/)；
完整索引見 [`EVIDENCE.md`](./EVIDENCE.md) 第 7 節。

