# CP1–CP3 圖表與補充資料

本資料夾存放報告引用的終端機截圖。截圖只作為輔助證據；可複製、可搜尋的
文字輸出仍放在 [`../../tests/`](../../tests/)。

## 圖片索引

| 檔案 | 對應報告 | 內容 |
|---|---|---|
| [`cp1_c_baseline.png`](./cp1_c_baseline.png) | [`../CP1.md`](../CP1.md) | CP1 C baseline：`gcc 16.2.0`、12 組測試、`12/12 tests passed.` |
| [`cp2_qemu.png`](./cp2_qemu.png) | [`../CP2.md`](../CP2.md) | QEMU 11.1.2 執行 RV32IM baseline，`12/12 tests passed` |
| [`cp2_trace.png`](./cp2_trace.png) | [`../CP2.md`](../CP2.md) | Python 3.12.10 trace runner 的動態指令數與分支數 |
| [`cp3_tests.png`](./cp3_tests.png) | [`../CP3.md`](../CP3.md) | CP3 語意、編碼與 `rd = x0` 測試，`9/9 CP3 tests passed.` |
| [`cp3_encoding.png`](./cp3_encoding.png) | [`../CP3.md`](../CP3.md) | 三個機器碼範例、golden model 與指令數資料 |

## 截圖原則

- 畫面包含實際指令、工具版本與最後的 `PASS`／`FAIL` 結果。
- 圖片只擷取終端機與必要的編輯器畫面，不截整個桌面。
- 報告中的數據以 `tests/*.txt` 的文字輸出為準；截圖用於快速確認執行畫面。
- 沒有被報告引用的圖片不要留在這個資料夾。

## 相關文字證據

- [`actual_output.txt`](../../tests/actual_output.txt)：CP1 C baseline 實際輸出。
- [`cp2_trace_output.txt`](../../tests/cp2_trace_output.txt)：CP2 動態指令數。
- [`cp2_trace_detail.txt`](../../tests/cp2_trace_detail.txt)：逐條 trace。
- [`qemu_output.txt`](../../tests/qemu_output.txt)：QEMU 執行輸出。
- [`cp3_test_output.txt`](../../tests/cp3_test_output.txt)：CP3 測試輸出。
- [`EVIDENCE.md`](../../tests/EVIDENCE.md)：工具版本、指令與限制。
