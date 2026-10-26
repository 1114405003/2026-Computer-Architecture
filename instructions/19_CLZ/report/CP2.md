# CP2：RV32IM 實作

## 1. 本次目標

完成 CLZ 的 RV32IM 組合語言實作、C wrapper / inline assembly，並建立
指令統計，供 CP3 的自訂指令比對使用。

## 2. 設計內容

### 2.1 組合語言檔

`src/rv32im/clz.s` 以 pure RV32IM 實作：

- 入口 / 出口：`a0` 作為輸入與回傳值。
- `x == 0` 時直接回傳 32。
- 依序檢查 16、8、4、2、1 位元區段，必要時累計並左移。
- 只使用 `beq`、`bnez`、`addi`、`srli`、`slli`、`mv`、`ret`。

### 2.2 C wrapper / inline assembly

- `clz_rv32im(x)` 呼叫組合語言 baseline。
- `clz_insn(x)` 使用 `.insn r 0x0b, 5, 0, ...` 產生自訂 CLZ 指令；
  在非 RISC-V 平台 fallback 到 `clz_rv32im()`。

## 3. 結果與分析

使用 [`tests/cp2_trace.py`](../tests/cp2_trace.py) 執行現有 `clz.s` 的
RV32I subset trace runner。工具為 Python 3，未使用 Spike、Ripes 或其他
模擬器；runner 只實作本檔案實際使用的 `beq`、`bnez`、`addi`、`srli`、
`slli`、`ret`，並逐條累計執行次數與分支次數。執行命令：

```text
python tests/cp2_trace.py
```

完整輸出保存於 [`tests/cp2_trace_output.txt`](../tests/cp2_trace_output.txt)。

執行結果：

```text
input        result  dynamic  branches
0x80000000       0        14         6
0x00010000      15        21         6
0x00000001      31        23         6
0x00000000      32         3         1
CP2 RV32I trace tests passed.
```

| 輸入 | CLZ 結果 | RV32IM 動態指令數 | Baseline 分支數 | Reduction 到 custom |
|---|---:|---:|---:|---:|
| `0x80000000` | 0 | 14 | 6 | 92.9% |
| `0x00010000` | 15 | 21 | 6 | 95.2% |
| `0x00000001` | 31 | 23 | 6 | 95.7% |
| `0x00000000` | 32 | 3 | 1 | 66.7% |

Baseline 靜態指令數為 25 條（含分支指令 6 條）；custom CLZ 為 1 條。表中 reduction 為
`(baseline_dynamic - 1) / baseline_dynamic`。

若以「每條指令 1 clock、custom `clz` 也為 1 clock」的單週期模型估算，
則四組測試合計由 61 clocks 降為 4 clocks，少 57 clocks，clock reduction
為 93.4%，加速比為 15.25x。單一案例分別少 13、20、22、2 clocks，
加速比為 14x、21x、23x、3x。這是依 trace 指令數換算的估算，不是實際
處理器或模擬器的 cycle 量測；pipeline、cache、hazard 與記憶體等待均未計入。

## 4. 遭遇的問題與解法

- RV32IM 沒有 Zbb 的 `clz`，因此不能直接使用；實作必須回到位元檢查。
- 每個檢查層的靜態指令數固定，但動態指令數依輸入而異，
  因此 CP3 必須標明「動態指令數」。
- 全零輸入需在第一條 `beq` 處理，避免 fall-through 到位元檢查。

## 5. 白話說明

CP2 把 CP1 的 C 演算法翻成 RISC-V 組合語言。做法和 C 一樣，只是沒有
if 布林值，全部變成「比較 + 跳躍 + 位移」。自訂 `clz` 指令會把整段
baseline function 壓縮成 1 條指令。

## 5.1 5 Whys

1. 為什麼要用多條 RV32I 指令？因為 RV32IM 沒有 `clz` 指令。
2. 為什麼不能直接使用 `clz`？因為那是 Zbb 擴充，不屬於本 CP2 的 RV32IM 基線。
3. 為什麼採用 16/8/4/2/1 分段？因為每次可縮小尚未檢查的位元範圍。
4. 為什麼要統計動態指令數？因為不同輸入會在不同分支路徑結束。
5. 為什麼要用 trace runner？因為逐條執行同一份組合語言，能驗證結果與計數，而不是只手算。

## 6. AI 使用說明

- 工具：Copilot / IDE 助手。
- 用途：協助整理 RV32IM 指令流程、static/dynamic 指令數統計與 wrapper 格式。
- 本組自行確認位移方向、邊界輸入與所有指令數。

## 7. 小組資訊與貢獻聲明

| 組員 | 學號 | 負責內容 | 佔比 |
|---|---|---|---:|
| 李玉蓉（組長） | 1114405003 | C baseline / CLZ 演算法 | 28.33% |
| 蔡珽州 | 1114405054 | 測試案例 / 指令統計 | 28.33% |
| 吳軒宇 | 1114405005 | 報告撰寫 | 15% |
| 温冠筑 | 1114405021 | RV32IM 與自訂指令規格 | 28.34% |

開發分支：`dev/1114405003`、`dev/1114405054`、`dev/1114405005`、`dev/1114405021`。
