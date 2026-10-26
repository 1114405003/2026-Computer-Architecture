# RV32IM CLZ baseline (CP2)

本資料夾是 CP2 的唯一 RV32IM 實作位置。CP2 將 CP1 的 CLZ 分段檢查
演算法改寫成 RISC-V RV32I 組合語言，並提供 C wrapper 與 custom CLZ
inline assembly 範例。

## 檔案說明

| 檔案 | 用途 |
|---|---|
| [`clz.s`](./clz.s) | RV32IM baseline 的 `clz` 函式 |
| [`clz_wrapper.c`](./clz_wrapper.c) | baseline 與 custom wrapper 的測試程式 |
| [`clz_wrapper.h`](./clz_wrapper.h) | `clz_rv32im()` 與 `clz_insn()` 宣告/實作 |
| [`../../tests/cp2_trace.py`](../../tests/cp2_trace.py) | RV32I subset trace runner |
| [`../../report/CP2.md`](../../report/CP2.md) | CP2 報告與指令統計 |

## 函式介面

```c
uint32_t clz_rv32im(uint32_t x);
uint32_t clz_insn(uint32_t x);
```

兩個函式的輸入都是 32-bit `uint32_t`：

- `clz_rv32im(x)`：呼叫 `clz.s` 的 RV32IM baseline。
- `clz_insn(x)`：在 RISC-V 編譯器下產生 custom-0 的 CLZ 指令。
- 非 RISC-V 主機上的 `clz_insn(x)` 會 fallback 到 baseline，不能代表
  x86 Windows 實際執行 custom opcode。

## RV32IM assembly 演算法

`clz.s` 使用 `a0` 作為輸入與回傳值，`t0` 保存累計的前導零數量，
`t1` 保存各階段的右移檢查結果：

1. `a0 == 0` 時直接回傳 `32`。
2. 右移 16 位檢查高 16 位；若為零，累加 16 並左移。
3. 右移 24 位檢查接下來的 8 位；必要時累加 8 並左移。
4. 右移 28 位檢查 4 位；必要時累加 4 並左移。
5. 右移 30 位檢查 2 位；必要時累加 2 並左移。
6. 右移 31 位檢查最後 1 位；必要時累加 1。
7. 將計數寫回 `a0` 後以 `ret` 返回。

使用的指令都是 RV32I 基礎指令：

```text
beq, bnez, addi, srli, slli, ret
```

沒有使用 Zbb 的原生 `clz`，因此可作為 custom instruction 的 baseline。

## Custom CLZ wrapper

`clz_wrapper.h` 使用 GNU assembler 的 `.insn` 格式：

```c
.insn r 0x0b, 5, 0, rd, rs1, rs2
```

欄位意義為：

```text
opcode = 0x0b       // custom-0，7 bits
funct3 = 5          // 101，3 bits
funct7 = 0          // 0000000，7 bits
rs2    = x0         // 不使用
```

這與 CP3 的 R-type 欄位順序 `7-5-5-3-5-7` 一致。範例
`clz a0, a1` 的 machine code 為 `0x0005D50B`。完整規格請參考
[`../../spec/README.md`](../../spec/README.md)。

## 指令統計

CP2 baseline 的靜態指令數為 25 條，custom CLZ 為 1 條。使用 trace
runner 得到以下動態結果：

| 輸入 | CLZ 結果 | 動態指令數 | 分支數 |
|---|---:|---:|---:|
| `0x80000000` | 0 | 14 | 6 |
| `0x00010000` | 15 | 21 | 6 |
| `0x00000001` | 31 | 23 | 6 |
| `0x00000000` | 32 | 3 | 1 |

## 測試方式

### Python trace runner

在專案根目錄執行：

```powershell
Set-Location 'D:\10.13\2026-Computer-Architecture\instructions\19_CLZ'
python .\tests\cp2_trace.py
```

成功時會顯示：

```text
CP2 RV32I trace tests passed.
```

此 runner 逐條執行 `clz.s` 中使用的 RV32I 指令，驗證 CLZ 結果、25
條靜態指令、動態指令數與分支數；不需要 Spike、Ripes 或 GCC。

### RISC-V toolchain 組譯

若已安裝 RISC-V GNU toolchain，可檢查 assembly 是否能組譯：

```powershell
Set-Location 'D:\10.13\2026-Computer-Architecture\instructions\19_CLZ\src\rv32im'
riscv64-unknown-elf-as -march=rv32im -mabi=ilp32 .\clz.s -o .\clz.o
```

檢查工具是否存在：

```powershell
Get-Command riscv64-unknown-elf-as
```

一般 x86 GCC 不能把 `clz.s` 當成 x86 程式執行；它只能編譯 CP1
C baseline。CP2 assembly 必須使用 RISC-V toolchain 或本專案的 Python
trace runner。

## Ripes 注意事項

Ripes 可以用來觀察 RV32I baseline 的 pipeline cycles、retired
instructions 與 CPI，但預設 processor 不一定支援本組的 custom-0
`clz` opcode。未修改 Ripes decoder 前，不應宣稱已在 Ripes 執行 custom
CLZ；custom instruction 的機器碼與 golden model 請使用
[`../../spec/clz_encoding.py`](../../spec/clz_encoding.py) 驗證。
