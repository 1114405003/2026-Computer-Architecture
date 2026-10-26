# CLZ CP1–CP3 報告總結

本專題實作 RISC-V 的 CLZ（Count Leading Zeros，計算前導零）功能。
輸入為 32-bit `uint32_t` 位元向量，輸出為從最高位開始連續的零數量；
當輸入為 `0x00000000` 時，依規格回傳 `32`。

## CP1：C baseline

CP1 完成 C 語言參考實作與測試。演算法以 16、8、4、2、1 位元分段檢查，
若目前區段為零便累加計數並左移輸入，最後得到前導零數量。實作與測試
位於 [`src/c_baseline/`](../src/c_baseline/)。

- 函式介面：`uint32_t clz(uint32_t x)`
- 測試資料：10 組，包含最高位為 1、不同位置的 1、最低位為 1，以及全零邊界值。
- 測試向量：[test_vectors.txt](../tests/test_vectors.txt)
- 預期輸出：[expected_output.txt](../tests/expected_output.txt)
- 執行方式：

  ```text
  gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz
  ./clz
  ```

代表結果：

| 輸入 | CLZ |
|---|---:|
| `0x80000000` | 0 |
| `0x00010000` | 15 |
| `0x00000001` | 31 |
| `0x00000000` | 32 |

## CP2：RV32IM baseline

CP2 將 CP1 演算法改寫為純 RV32IM 組合語言，入口與回傳值都使用 `a0`。
實作位於 [`src/rv32im/`](../src/rv32im/)，使用 `beq`、`bnez`、`addi`、
`srli`、`slli` 與 `ret`，沒有使用 Zbb 的 `clz` 指令。

指令數以 Python 3 的 RV32I subset trace runner 逐條執行同一份組合語言
計算，未使用 Spike、Ripes 或其他模擬器。測試程式為
[`cp2_trace.py`](../tests/cp2_trace.py)，執行方式：

```text
python tests/cp2_trace.py
```

驗證結果：

| 輸入 | CLZ | 動態指令數 | 分支數 |
|---|---:|---:|---:|
| `0x80000000` | 0 | 14 | 6 |
| `0x00010000` | 15 | 21 | 6 |
| `0x00000001` | 31 | 23 | 6 |
| `0x00000000` | 32 | 3 | 1 |

baseline 靜態指令數為 25 條；完整 trace 輸出保存於
[`cp2_trace_output.txt`](../tests/cp2_trace_output.txt)。

## CP3：自訂 CLZ 指令

CP3 將 CLZ 定義為 custom-0 的 R-type 自訂指令：

```text
clz rd, rs1
rd = CLZ(rs1)
```

`rs2` 不使用並固定為 0。欄位順序符合老師指定的
`7-5-5-3-5-7`：

| `fun7/f7` | `rs2` | `rs1` | `fun3/f3` | `rd` | `opcode` |
|---:|---:|---:|---:|---:|---:|
| 7 bits | 5 bits | 5 bits | 3 bits | 5 bits | 7 bits |

指令欄位設定如下：

- `opcode = 0001011`（custom-0，`0x0B`）
- `fun3/funct3 = 101`（5）
- `fun7/funct7 = 0000000`（0）
- `rs2 = 00000`（固定為 0）

範例 `clz a0, a1`（`rd=x10`、`rs1=x11`）：

```text
0000000 00000 01011 101 01010 0001011
0x0005D50B
```

規格與 encoder 位於 [`spec/`](../spec/)。執行：

```text
python spec/clz_encoding.py
```

可驗證編碼、解碼、CLZ golden model 與指令數比較。CP3 的比較結果如下：

| 項目 | RV32IM baseline | Custom CLZ |
|---|---:|---:|
| 靜態指令數 | 25 | 1 |
| `0x80000000` 動態指令數 | 14 | 1 |
| `0x00010000` 動態指令數 | 21 | 1 |
| `0x00000001` 動態指令數 | 23 | 1 |
| `0x00000000` 動態指令數 | 3 | 1 |

本次比較採用靜態與動態指令數，不比較 cycle 或 pipeline；作業規定本階段
不要求 cycle，且尚未教授 pipeline。

若採用「每條指令 1 clock」的單週期估算，四組測試由 61 clocks 降為
4 clocks，少 57 clocks，clock reduction 為 93.4%，加速比為 15.25x。
個別輸入少 13、20、22、2 clocks，分別為 14x、21x、23x、3x 加速。
這是由已驗證的動態指令數換算，並非真實硬體 cycle 實測。

## 檔案索引

| 檔案 | 說明 |
|---|---|
| [`CP1.md`](./CP1.md) | C baseline、演算法設計與測試結果 |
| [`CP2.md`](./CP2.md) | RV32IM 組合語言、trace 測試與指令統計 |
| [`CP3.md`](./CP3.md) | 自訂指令語意、編碼與指令數比較 |
| [`figures/README.md`](./figures/README.md) | CP1 補充測試輸出 |
