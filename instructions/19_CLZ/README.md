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
| [`src/c_baseline/`](./src/c_baseline/) | C baseline 的 `clz.c` 函式與 `main.c` 測試程式 |
| [`instructions/19_CLZ/tests/`](./instructions/19_CLZ/tests/) | 測試向量與預期輸出 |
| [`report/CP1.md`](./report/CP1.md) | CP1 演算法設計、測試結果與分析 |
| [`report/CP2.md`](./report/CP2.md) | CP2 RV32IM 實作與指令統計 |
| [`report/CP3.md`](./report/CP3.md) | CP3 自訂指令規格、編碼與指令數比 |

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
cd src/c_baseline
gcc clz.c main.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

程式正常執行時會列出 10 組測試結果，例如：

```text
Test  1: CLZ(0x80000000) = 0
Test 10: CLZ(0x00000000) = 32
```

完整預期輸出請參考
[`instructions/19_CLZ/tests/expected_output.txt`](./instructions/19_CLZ/tests/expected_output.txt)。

## CP2 / CP3 補充

- CP2：[`src/rv32im/clz.s`](./src/rv32im/clz.s)、[`tests/cp2_trace.py`](./tests/cp2_trace.py)、[`report/CP2.md`](./report/CP2.md)
- CP3：[`spec/clz_spec.md`](./spec/clz_spec.md)、[`spec/clz_encoding.py`](./spec/clz_encoding.py)、[`report/CP3.md`](./report/CP3.md)
