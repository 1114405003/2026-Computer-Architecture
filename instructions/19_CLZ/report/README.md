# CLZ 報告索引

本資料夾包含 CP1–CP3 的書面報告。每份報告都依 HOMEWORK 5.3 的 1–6 段
順序撰寫，並在「5. 白話說明」下附 5 Whys。

| Checkpoint | 檔案 | 主要內容 |
|---|---|---|
| CP1 | [`CP1.md`](./CP1.md) | C baseline、12 組測試、實際輸出 |
| CP2 | [`CP2.md`](./CP2.md) | `clz.s`、`clz_loop.s`、靜態／動態指令數、寫法比較 |
| CP3 | [`CP3.md`](./CP3.md) | 語意、虛擬碼、R-type 編碼、3 個範例、指令數比較 |

## 數據標示原則

- **靜態指令數**：只計算函式原始碼中的指令，不計 label、註解與指示詞。
- **動態指令數**：由 [`../tests/cp2_trace.py`](../tests/cp2_trace.py)
  逐條執行組合語言取得；工具為 Python 3.12.10。輸出在
  [`../tests/cp2_trace_output.txt`](../tests/cp2_trace_output.txt)。
- **執行證據**：`clz.s` 與 `clz_loop.s` 由 `riscv32-unknown-elf-gcc`
  14.2.0 組譯，並在 QEMU 11.1.2 `virt` 機器執行，12/12 通過；輸出在
  [`../tests/qemu_output.txt`](../tests/qemu_output.txt)。
- **終端截圖**：放在 [`figures/`](./figures/)，只作為輔助證據；文字輸出
  仍以 [`../tests/`](../tests/) 的檔案為準。
- **cycle／CPI／加速比**：本次不比較。課程尚未教授 pipeline，作業也不
  要求 cycle 數，因此報告不把指令數換算成 clock。

## 快速結論

| 項目 | RV32IM baseline | CLZ 自訂指令 |
|---|---:|---:|
| 靜態指令數（分段檢查） | 25 | 1 |
| 靜態指令數（逐位元迴圈） | 11 | 1 |
| `0x80000000` 動態指令數 | 14 | 1 |
| `0x00010000` 動態指令數 | 21 | 1 |
| `0x00000001` 動態指令數 | 23 | 1 |
| `0x00000000` 動態指令數 | 3 | 1 |

完整表格與分析分別在 CP2、CP3 報告中。
