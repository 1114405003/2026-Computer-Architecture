 CLZ 自訂指令規格與驗證工具

本資料夾對應 CP3，內容包含 CLZ 自訂指令的正式語意、R-type 編碼、
機器碼範例、golden model，以及 RV32IM baseline 與 custom instruction
的指令數比較。

## 1. 指令語意

指令語法：

```text
clz rd, rs1
```

指令執行：

```text
rd = CLZ(rs1)
```

`rs1` 是 32-bit 位元向量，結果 `rd` 的範圍為 `0..32`。當 `rs1` 為
`0x00000000` 時，沒有任何 `1` 可以作為最高位，因此規定回傳 `32`。
`rs2` 不參與運算，固定填入 `x0`。

等價公式：

```text
CLZ(rs1) = 32 - bit_length(rs1)
bit_length(0) = 0
```

虛擬碼：

```text
CLZ(rs1):
    if rs1 == 0:
        return 32
    count = 0
    for i = 31 down to 0:
        if bit(rs1, i) == 1:
            return count
        count = count + 1
```

完整規格請參考 [`clz_spec.md`](./clz_spec.md)。

## 2. R-type 欄位配置

本組依照老師指定的欄位順序 `7-5-5-3-5-7`：

```text
31      25 24   20 19   15 14  12 11    7 6       0
| funct7 |  rs2  |  rs1  |funct3|  rd   |  opcode |
|   7    |   5    |   5    |  3   |   5   |    7    |
```

欄位設定：

| 欄位 | 值 | 寬度 | 說明 |
|---|---|---:|---|
| `opcode` | `0001011` (`0x0B`) | 7 bits | RISC-V custom-0 |
| `funct3/fun3/f3` | `101` (`5`) | 3 bits | CLZ operation |
| `funct7/fun7/f7` | `0000000` (`0`) | 7 bits | CLZ operation |
| `rs1` | 輸入暫存器 | 5 bits | 32-bit input |
| `rs2` | `00000` (`x0`) | 5 bits | 不使用，固定為 0 |
| `rd` | 輸出暫存器 | 5 bits | CLZ result |

## 3. 完整機器碼範例

以 `clz a0, a1` 為例：

```text
rd  = x10 = 01010
rs1 = x11 = 01011
rs2 = x0  = 00000
```

欄位組合：

```text
funct7  rs2   rs1   funct3 rd    opcode
0000000 00000 01011 101    01010 0001011
```

32-bit machine code：

```text
0x0005D50B
```

## 4. Python encoder 與 golden model

[`clz_encoding.py`](./clz_encoding.py) 提供：

- `clz_golden(x)`：32-bit CLZ 參考結果。
- `encode_clz(rd, rs1, rs2=0)`：將欄位編碼成 32-bit instruction。
- `decode_clz(word)`：解析 opcode、funct3、funct7 與暫存器欄位。
- `apply_clz(regs, rd, rs1)`：模擬暫存器寫回行為。
- `instruction_count_comparison()`：回傳 baseline/custom 指令數比較。

在專案根目錄執行 CP3 驗證：

```powershell
Set-Location 'D:\10.13\2026-Computer-Architecture\instructions\19_CLZ'
python .\spec\clz_encoding.py
```

預期確認：

```text
clz a0, a1  ->  0x0005d50b
decode: {'rd': 10, 'rs1': 11, 'rs2': 0}
CLZ(0x80000000) = 0
CLZ(0x00010000) = 15
CLZ(0x00000001) = 31
CLZ(0x00000000) = 32
```

## 5. 測試案例

至少三組測試是作業要求，本組使用四組，包含全零邊界：

| 輸入 | 預期 CLZ | 類型 |
|---|---:|---|
| `0x80000000` | 0 | 最高位為 1 |
| `0x00010000` | 15 | 一般案例 |
| `0x00000001` | 31 | 最低位為 1 |
| `0x00000000` | 32 | 邊界案例 |

## 6. 指令數與效能比較

計數方法為**動態指令數，每次 CLZ function call 分開計算**。CP2 的
RV32IM baseline 使用 [`../src/rv32im/clz.s`](../src/rv32im/clz.s)，
custom CLZ 每次只使用一條指令。

| 輸入 | RV32IM 動態指令 | Custom 動態指令 | 減少指令 | Reduction |
|---|---:|---:|---:|---:|
| `0x80000000` | 14 | 1 | 13 | 92.9% |
| `0x00010000` | 21 | 1 | 20 | 95.2% |
| `0x00000001` | 23 | 1 | 22 | 95.7% |
| `0x00000000` | 3 | 1 | 2 | 66.7% |
| **四組合計** | **61** | **4** | **57** | **93.4%** |

靜態指令數則由 RV32IM baseline 的 25 條降為 custom CLZ 的 1 條，
減少 24 條，靜態減少比例為 96.0%。

若採用每條指令 1 clock 的理想單週期模型，四組測試由 61 clocks
降為 4 clocks，節省 57 clocks，加速比為 `61 / 4 = 15.25x`。這是依
trace 指令數換算的估算，不是實際 CPU pipeline、cache 或 hazard 的
cycle 量測；本階段不要求 cycle 模擬。

## 7. 與 CP2 trace runner 的關係

CP2 的 trace runner 位於 [`../tests/cp2_trace.py`](../tests/cp2_trace.py)，
會逐條執行 `clz.s` 中使用的 RV32I 指令，驗證結果、動態指令數與分支數。

執行方式：

```powershell
python .\tests\cp2_trace.py
```

CP2 trace 結果：

```text
input        result  dynamic  branches
0x80000000       0        14         6
0x00010000      15        21         6
0x00000001      31        23         6
0x00000000      32         3         1
CP2 RV32I trace tests passed.
```

## 8. RISC-V inline assembly

在 [`../src/rv32im/clz_wrapper.h`](../src/rv32im/clz_wrapper.h) 中，
custom instruction 使用：

```c
.insn r 0x0b, 5, 0, rd, rs1, rs2
```

對應為：

```text
.insn r opcode, funct3, funct7, rd, rs1, rs2
```

非 RISC-V 主機會 fallback 到 `clz_rv32im()`，因此一般 x86 Windows
環境可以編譯 wrapper，但不會真的執行 custom opcode。

## 9. 限制與注意事項

- CP3 encoder 驗證的是機器碼欄位與 golden model。
- Ripes 或一般 RISC-V 模擬器不一定支援此 custom opcode；若未修改
  processor decoder，不能宣稱已完成 custom instruction 的硬體執行。
- 本專題未使用 Spike、Ripes 或其他 cycle simulator 量測 CP3 cycle。
- 若要取得真實 cycles，必須使用支援 custom-0 `clz` 的 CPU 或修改後的
  simulator，並另外報告工具名稱與版本。

## 10. 相關檔案

| 檔案 | 用途 |
|---|---|
| [`clz_spec.md`](./clz_spec.md) | CP3 正式語意、機器碼與指令數規格 |
| [`clz_encoding.py`](./clz_encoding.py) | Encoder、decoder、golden model |
| [`../src/rv32im/clz.s`](../src/rv32im/clz.s) | RV32IM baseline |
| [`../tests/cp2_trace.py`](../tests/cp2_trace.py) | CP2 指令 trace 測試 |
| [`../report/CP3.md`](../report/CP3.md) | CP3 報告 |