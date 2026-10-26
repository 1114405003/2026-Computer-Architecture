# CP1 圖表與測試輸出

本資料夾保存 CP1 報告使用的補充材料。CLZ 是純位元運算的 C
baseline，因此本次沒有額外產生效能圖或圖片檔；測試結果以可複製的
純文字輸出呈現，避免手動轉錄造成誤差。

## 資料索引

| 資料 | 說明 |
|---|---|
| [`CP1.md`](../CP1.md) | C baseline 的演算法、測試設計與結果分析 |
| [`test_vectors.txt`](../../instructions/19_CLZ/tests/test_vectors.txt) | 10 組輸入與預期 CLZ 值 |
| [`expected_output.txt`](../../instructions/19_CLZ/tests/expected_output.txt) | 測試程式應產生的終端輸出 |
| [`clz.c`](../../src/c_baseline/clz.c) | C baseline 參考實作 |

## 測試涵蓋範圍

測試向量涵蓋以下情況：

- 最高位元為 `1`，確認前導零數量為 `0`。
- 不同位置的單一 `1`，確認一般輸入的前導零計數。
- 最低位元為 `1`，確認最大的一般結果 `31`。
- `0x00000000`，確認規格定義的特殊結果 `32`。

## 預期輸出

```text
Test  1: CLZ(0x80000000) = 0
Test  2: CLZ(0x40000000) = 1
Test  3: CLZ(0x20000000) = 2
Test  4: CLZ(0x10000000) = 3
Test  5: CLZ(0x08000000) = 4
Test  6: CLZ(0x01000000) = 7
Test  7: CLZ(0x00100000) = 11
Test  8: CLZ(0x00010000) = 15
Test  9: CLZ(0x00000001) = 31
Test 10: CLZ(0x00000000) = 32
```

上述結果應與 [`expected_output.txt`](../../instructions/19_CLZ/tests/expected_output.txt)
完全一致；若輸出不同，應先檢查測試向量、`uint32_t` 型別與全零輸入的
特殊處理。

## 產生方式

在專案根目錄編譯並執行 C baseline：

```text
gcc -std=c11 -Wall -Wextra -pedantic src/c_baseline/clz.c src/c_baseline/main.c -o clz
./clz
```

Windows 環境可使用相同的編譯參數產生 `clz.exe`，再執行：

```text
clz.exe
```
