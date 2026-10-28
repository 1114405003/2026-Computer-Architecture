# 執行證據（EVIDENCE）

本文件記錄本次繳交使用的工具、版本、指令與實際輸出。所有輸出檔都在
`tests/` 目錄。

## 1. 執行環境

| 項目 | 內容 |
|---|---|
| 作業系統 | Windows 10/11 |
| Python | 3.12.10 |
| C 編譯器（CP1） | MSYS2 UCRT64 `gcc` 16.2.0 |
| RISC-V 工具鏈 | `riscv32-unknown-elf-gcc` 14.2.0 |
| RISC-V 模擬器 | QEMU `qemu-system-riscv32` 11.1.2（`virt` 機器） |
| 執行日期 | 2026-10-28 |

## 2. CP1：C baseline

指令：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
./clz.exe
```

輸出檔：[`actual_output.txt`](./actual_output.txt)

最後一行：

```text
12/12 tests passed.
```

## 3. CP2：QEMU RV32IM 實際執行

這一節是真正的 RV32IM 機器碼執行，不是 Python 模擬。`clz.s` 與
`clz_loop.s` 由 `riscv32-unknown-elf-gcc` 組譯，放進 QEMU 的 `virt`
機器執行。

建置：

```text
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -ffreestanding -fno-builtin -nostdlib -nostartfiles -T tests/qemu/link.ld -o tests/qemu/clz_qemu.elf tests/qemu/start.S src/rv32im/clz.s src/rv32im/clz_loop.s tests/qemu/test_qemu.c
```

執行：

```text
qemu-system-riscv32 -machine virt -cpu rv32 -bios none -kernel tests/qemu/clz_qemu.elf -nographic -no-reboot
```

輸出檔：

- [`qemu_output.txt`](./qemu_output.txt)
- [`qemu_disassembly.txt`](./qemu_disassembly.txt)：`riscv32-unknown-elf-objdump -d` 的實際指令。
- [`qemu_size.txt`](./qemu_size.txt)：ELF section 大小。

`qemu_output.txt` 最後一行：

```text
12/12 tests passed
```

> QEMU `virt` 沒有實作本組的 custom-0 `clz` opcode，因此 QEMU 只執行
> `clz_rv32im` 與 `clz_loop` 兩個標準 RV32IM baseline；`.insn` wrapper
> 沒有在 QEMU 中執行。

## 4. CP2：Python trace runner（動態指令數）

QEMU 可以驗證結果，但沒有直接提供「這一趟執行了幾條指令」的計數。
因此動態指令數另外由 [`cp2_trace.py`](./cp2_trace.py) 逐條執行同一份
組合語言取得。

指令：

```text
python tests/cp2_trace.py
python tests/cp2_trace.py --detail 0x00010000
```

輸出檔：

- [`cp2_trace_output.txt`](./cp2_trace_output.txt)
- [`cp2_trace_detail.txt`](./cp2_trace_detail.txt)

`cp2_trace.py` 會：

1. 解析 `src/rv32im/clz.s` 與 `src/rv32im/clz_loop.s`。
2. 逐條執行實際的 RV32I 指令。
3. 對 12 組輸入比對 golden result。
4. 計算動態指令數與條件分支數。
5. 斷言靜態指令數（25 / 11）與靜態分支數（6 / 2）。

最後一行：

```text
CP2 RV32I trace tests passed.
```

> 這不是 cycle 量測。QEMU 負責「真的跑得動、結果正確」；Python runner
> 負責「逐條計數」。兩者用途不同，報告中沒有把指令數換算成 clock。

## 5. CP3：語意與編碼

指令：

```text
python tests/cp3_test.py
python spec/clz_encoding.py
```

輸出檔：

- [`cp3_test_output.txt`](./cp3_test_output.txt)
- [`cp3_encoding_output.txt`](./cp3_encoding_output.txt)

最後一行：

```text
9/9 CP3 tests passed.
```

## 6. Git 標籤證據

以 `git ls-remote --tags origin` 取得的遠端標籤：

```text
b72b111721ecb081c392eec7841cc2d15175a621  refs/tags/cp1-submit
5985985017b7a013bc286c30ca7658af9aa490d8  refs/tags/cp2-submit
4f518f5db99a429a6baed616a57905a563e5c97e  refs/tags/cp3-submit
```

三個 tag 都存在於遠端。若課程平台要求以 tag 推送時間判定，請以平台顯示
的時間為準。

## 7. 終端截圖

| 圖 | 檔案 | 內容 |
|---|---|---|
| CP1 | [`../report/figures/cp1_c_baseline.png`](../report/figures/cp1_c_baseline.png) | C baseline 編譯與 12/12 輸出 |
| CP2 QEMU | [`../report/figures/cp2_qemu.png`](../report/figures/cp2_qemu.png) | QEMU RV32IM 執行與 12/12 輸出 |
| CP2 trace | [`../report/figures/cp2_trace.png`](../report/figures/cp2_trace.png) | Python trace 的動態指令數與分支數 |
| CP3 tests | [`../report/figures/cp3_tests.png`](../report/figures/cp3_tests.png) | CP3 語意與編碼測試 9/9 |
| CP3 encoding | [`../report/figures/cp3_encoding.png`](../report/figures/cp3_encoding.png) | 三個機器碼範例與 golden model |

截圖只作為輔助；數據仍以本文件前面列出的文字輸出檔為準。

