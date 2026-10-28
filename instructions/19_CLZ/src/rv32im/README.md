# CLZ RV32IM 實作（CP2）

## 1. 檔案

| 檔案 | 內容 |
|---|---|
| [`clz.s`](./clz.s) | 主要 baseline：16/8/4/2/1 分段檢查，符號 `clz_rv32im` |
| [`clz_loop.s`](./clz_loop.s) | 比較用 baseline：逐位元左移迴圈，符號 `clz_loop` |
| [`clz_wrapper.h`](./clz_wrapper.h) | `clz_insn()` inline assembly 與 C 介面 |
| [`clz_wrapper.c`](./clz_wrapper.c) | 非 inline 的 C wrapper |
| [`test_clz.c`](./test_clz.c) | 12 組測試，分別執行兩個 baseline |
| [`Makefile`](./Makefile) | `riscv64-unknown-elf-gcc` 建置規則 |

## 2. ABI 與暫存器

| 暫存器 | 用途 |
|---|---|
| `a0` | 輸入值；函式結束時存放結果 |
| `t0` | 累積的前導零數量 |
| `t1` | 右移／左移後的檢查值 |
| `ra` | 返回位址 |

兩個函式都遵循 RISC-V ELF ABI，`t0/t1` 為 caller-saved，不需要 stack。

## 3. 演算法

### 3.1 `clz.s`：16/8/4/2/1 分段檢查

1. `x == 0` 直接回傳 32。
2. 若高 16 位元全為 0，計數加 16，左移 16 位。
3. 若接下來 8 位元全為 0，計數加 8，左移 8 位。
4. 依序檢查 4、2、1 位元。
5. 最後 `a0 = t0` 並返回。

### 3.2 `clz_loop.s`：逐位元迴圈

1. `x == 0` 直接回傳 32。
2. 每回合檢查 bit 31；若為 0，計數加 1，左移 1 位，回到迴圈。
3. 找到第一個 1 時返回計數。

這個版本只用於 CP2 的「寫法比較」，不是主要 baseline。

## 4. 靜態指令數

計數方法：只計算 `clz.s` / `clz_loop.s` 中的實際 RV32I 指令，不計 label、
註解、`.section`、`.globl`、`.type`、`.size` 等指示詞。`ret` 以 1 條指令計。

| 實作 | 靜態指令數 | 靜態條件分支數 |
|---|---:|---:|
| `clz.s`（分段檢查） | 25 | 6 |
| `clz_loop.s`（逐位元迴圈） | 11 | 2 |

## 5. 動態指令數

計數方法：使用 Python 3.12.10 的 [`../../tests/cp2_trace.py`](../../tests/cp2_trace.py)
逐條執行組合語言。每執行一條指令計 1，條件分支不論是否跳轉都計 1。
這不是 Spike 或 Ripes，也不是 cycle 量測；詳細限制見
[`../../tests/EVIDENCE.md`](../../tests/EVIDENCE.md)。

| 輸入 | 結果 | `clz.s` 動態 | `clz.s` 分支 | `clz_loop.s` 動態 | `clz_loop.s` 分支 |
|---|---:|---:|---:|---:|---:|
| `0x80000000` | 0 | 14 | 6 | 6 | 2 |
| `0x40000000` | 1 | 15 | 6 | 11 | 3 |
| `0x20000000` | 2 | 16 | 6 | 16 | 4 |
| `0x10000000` | 3 | 17 | 6 | 21 | 5 |
| `0x08000000` | 4 | 16 | 6 | 26 | 6 |
| `0x01000000` | 7 | 19 | 6 | 41 | 9 |
| `0x00100000` | 11 | 19 | 6 | 61 | 13 |
| `0x00010000` | 15 | 21 | 6 | 81 | 17 |
| `0x00000001` | 31 | 23 | 6 | 161 | 33 |
| `0x00000000` | 32 | 3 | 1 | 3 | 1 |
| `0x00F00000` | 8 | 16 | 6 | 46 | 10 |
| `0x0000FFFF` | 16 | 16 | 6 | 86 | 18 |

完整輸出與逐條 trace 見
[`../../tests/cp2_trace_output.txt`](../../tests/cp2_trace_output.txt) 與
[`../../tests/cp2_trace_detail.txt`](../../tests/cp2_trace_detail.txt)。

## 6. 兩種寫法的比較

- **靜態指令數**：逐位元迴圈較短（11 條），分段檢查較長（25 條）。
- **動態指令數**：逐位元迴圈隨前導零數量線性成長；分段檢查最多 5 個階段。
- 對非零輸入，分段檢查的動態指令數可寫成：

  ```text
  dynamic = 14 + 2 × S + F
  ```

  `S` 是實際左移的區段數（0–4），`F` 是最後 1-bit 是否需要加 1（0 或 1）。
- 逐位元迴圈在 `CLZ = L` 時：

  ```text
  dynamic = 6 + 5 × L   (L = 0..31)
  ```

  零輸入例外，為 3 條。
- 因此 `CLZ` 很小（例如 `0x80000000`）時，迴圈版本較少指令；`CLZ`
  很大（例如 `0x00000001`）時，分段檢查明顯較好（23 vs 161）。

## 7. 正確性驗證

[`test_clz.c`](./test_clz.c) 對 `clz_rv32im` 與 `clz_loop` 各跑 12 組測試：
零值、最高位為 1、最低位為 1、nibble/byte/16-bit 邊界、多個相鄰 1。

Python trace runner 也會對 12 組輸入檢查結果，並斷言靜態指令數與分支數。

## 8. 建置與 QEMU 執行

以下 `make` 指令在 `src/rv32im` 目錄執行；QEMU 的組譯與執行指令則在
`instructions/19_CLZ` 目錄執行。

```text
make
# 若環境使用 riscv64-unknown-elf-gcc：
make CC=riscv64-unknown-elf-gcc
```

`Makefile` 使用 `-march=rv32im -mabi=ilp32`，預設產生
`clz.o`、`clz_loop.o`、`clz_wrapper.o`、`test_clz.o`。本組另外用
`riscv32-unknown-elf-gcc 14.2.0` 與 QEMU 11.1.2 執行 12 組測試：

```text
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -ffreestanding -fno-builtin -nostdlib -nostartfiles -T tests/qemu/link.ld -o tests/qemu/clz_qemu.elf tests/qemu/start.S src/rv32im/clz.s src/rv32im/clz_loop.s tests/qemu/test_qemu.c
qemu-system-riscv32 -machine virt -cpu rv32 -bios none -kernel tests/qemu/clz_qemu.elf -nographic -no-reboot
```

輸出在 [`../../tests/qemu_output.txt`](../../tests/qemu_output.txt)，最後
一行是 `12/12 tests passed`。

> 注意：`clz_wrapper.h` 的 `.insn` 會產生 custom-0 指令。QEMU `virt`
> 未修改 decoder 時不能執行這個 custom opcode；一般 RV32IM 驗證請使用
> `clz_rv32im` 與 `clz_loop`。

## 9. 限制

- 本組使用 QEMU `virt` 執行標準 RV32IM baseline，沒有使用 Spike/Ripes。
- QEMU 沒有實作 custom-0 `clz`，因此 custom instruction 只驗證編碼與
  golden model，不宣稱硬體執行。
- 動態指令數由自製 Python RV32I 指令層級 runner 取得，不是硬體 cycle。
- 本 CP 不比較 CPI、clock cycle 或 pipeline 行為。
