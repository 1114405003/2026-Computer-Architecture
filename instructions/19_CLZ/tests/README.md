# group05-CLZ

## 專案簡介

本專案實作 CLZ（Count Leading Zeros，計算前導零）功能。程式接收一個
32-bit `uint32_t` 無號整數，回傳從最高位元開始連續的零數量；當輸入為
`0x00000000` 時，依規格回傳 `32`。

目前的 C baseline 使用固定的 16、8、4、2、1 位元分段檢查方式，在
`O(1)` 時間內完成計算，並包含 10 組測試案例，涵蓋一般輸入、最低位元
為 1，以及全零輸入等情況。

## 專案結構

| 路徑 | 說明 |
|---|---|
| [`src/c_baseline/`](../src/c_baseline/) | CP1 的 `clz.c` 函式與 `main.c` 測試程式 |
| [`test_vectors.txt`](./test_vectors.txt) | 10 組輸入與預期 CLZ 值 |
| [`expected_output.txt`](./expected_output.txt) | 測試程式的預期輸出 |
| [`../report/CP1.md`](../report/CP1.md) | CP1 演算法設計、測試結果與分析 |

## 編譯與執行

### 直接執行目前的 C baseline

在專案根目錄執行：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

Windows 環境可使用：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
clz.exe
```

### 執行分離的函式與測試程式

```text
cd instructions/19_CLZ
gcc clz.c main.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

程式正常執行時會列出 10 組測試結果，並在每組顯示 `PASS` 或 `FAIL`：

```text
Test  1: CLZ(0x80000000) = 0 (expected 0) PASS
Test 10: CLZ(0x00000000) = 32 (expected 32) PASS
```

完整預期輸出請參考
[`expected_output.txt`](./expected_output.txt)。
