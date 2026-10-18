# 19_CLZ/rv32im/（CP2）

- 對應 Checkpoint：**CP2**
- 內容：RV32IM 組合語言實作與指令統計（僅使用 RV32IM 指令）

## 檔案

| 檔案 | 說明 |
|---|---|
| [`clz.S`](./clz.S) | 依 CP1 二分搜尋流程實作的 RV32IM CLZ 函式 |
| [`../report/CP2.md`](../report/CP2.md) | CP2 設計說明、測試結果與指令統計 |

## 呼叫介面

- 輸入：`a0`，32-bit `rs1` 值。
- 輸出：`a0`，前導零數量；輸入為零時回傳 `32`。
- 暫存器：使用 caller-saved 的 `t0`、`t1`，不修改 callee-saved 暫存器。
- 組合語言檔沒有使用 `clz` 指令或其他非 RV32IM 指令。
