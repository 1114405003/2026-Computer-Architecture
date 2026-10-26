# CLZ 測試資料

本資料夾整合以下測試資料：

- `test_vectors.txt`：10 組輸入向量。
- `expected_output.txt`：對應的預期輸出。
- `cp2_trace.py`：CP2 RV32I trace runner。

## CLZ 指令規格

| 項目 | 內容 |
|---|---|
| 指令名稱 | `CLZ` |
| 題目類別 | 算術類 |
| 運算元類型 | 一元 |
| 輸入定義 | `rs1` 為 32-bit 位元向量 |
| 語意公式 | `rd = 前導 0 的個數`，`rs1 = 0` 時 `rd = 32` |

## 檔案索引

| 路徑 | 說明 |
|---|---|
| [`src/c_baseline/`](../src/c_baseline/) | CP1 的 `clz.c` 函式與 `main.c` 測試程式 |
| [`test_vectors.txt`](./test_vectors.txt) | 10 組輸入與預期 CLZ 值 |
| [`expected_output.txt`](./expected_output.txt) | 測試程式的預期輸出 |
| [`actual_output.txt`](./actual_output.txt) | LLVM MinGW clang 實際執行輸出 |
| [`cp3_test.py`](./cp3_test.py) | CP3 語意、邊界值與指令編碼測試 |
| [`../report/CP1.md`](../report/CP1.md) | CP1 演算法設計、測試結果與分析 |
| [`../report/CP3.md`](../report/CP3.md) | CP3 測試案例設計、結果整理與編碼驗證 |

CLZ 函式介面如下：

```c
uint32_t clz(uint32_t x);
```

函式接收一個 32-bit 無號整數，回傳從最高位元開始連續的前導零數量。
輸入為 `0x00000000` 時，依照規格回傳 `32`。

## C baseline 實作方法

實作依序檢查輸入的 16、8、4、2、1 位元區段。若目前區段全部為零，
就將計數器增加該區段的位元數，並將輸入值左移相同位數，繼續檢查。
輸入為零時直接回傳 `32`，避免全零值被誤判。

編譯與執行：

```text
gcc clz.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

## 測試案例

目前共有 10 組測試，表格記錄每組輸入與預期 CLZ 結果：

| 測試 | 輸入 | 預期輸出 | 測試目的 |
|---:|---|---:|---|
| 1 | `0x80000000` | `CLZ = 0` | 最高位元為 1 |
| 2 | `0x40000000` | `CLZ = 1` | 1 個前導零 |
| 3 | `0x20000000` | `CLZ = 2` | 2 個前導零 |
| 4 | `0x10000000` | `CLZ = 3` | 3 個前導零 |
| 5 | `0x08000000` | `CLZ = 4` | nibble 邊界 |
| 6 | `0x01000000` | `CLZ = 7` | byte 邊界 |
| 7 | `0x00100000` | `CLZ = 11` | 非邊界位元位置 |
| 8 | `0x00010000` | `CLZ = 15` | 16-bit 邊界 |
| 9 | `0x00000001` | `CLZ = 31` | 僅最低位元為 1 |
| 10 | `0x00000000` | `CLZ = 32` | 零輸入邊界案例 |
| 11 | `0x00F00000` | `CLZ = 8` | 多個相鄰位元為 1 |
| 12 | `0x0000FFFF` | `CLZ = 16` | 低 16 位元為 1 |

## 邊界值

- `0x80000000`：最高位元為 1，前導零數量為 0。
- `0x00000001`：只有最低位元為 1，前導零數量為 31。
- `0x00000000`：全零輸入，依規格回傳 32。

## 預期執行結果

測試程式會逐組比對實際結果與預期結果，並輸出 `PASS` 或 `FAIL`。
所有測試正確時，最後應輸出：

```text
10/10 tests passed.
```
### 執行分離的函式與測試程式

在 `instructions/19_CLZ` 目錄中執行：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

程式正常執行時會列出 10 組測試結果，並在每組顯示 `PASS` 或 `FAIL`：

```text
Test  1: CLZ(0x80000000) = 0 (expected 0) PASS
Test 10: CLZ(0x00000000) = 32 (expected 32) PASS
```

完整預期輸出請參考
[`expected_output.txt`](./expected_output.txt)。

完整實際輸出請參考
[`actual_output.txt`](./actual_output.txt)。

### CP3 測試

在專案根目錄執行：

```text
python instructions/19_CLZ/tests/cp3_test.py
```

此測試會驗證 5 組 CLZ 語意案例，以及 `clz x10, x11` 的 R-type
編碼與解碼結果；預期為 `6/6 CP3 tests passed.`。
