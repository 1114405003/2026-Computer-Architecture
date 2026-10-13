# CLZ C Baseline

<<<<<<< Updated upstream:src/README.md
=======
本資料夾存放 CLZ（Count Leading Zeros）的 C 語言參考實作與測試程式，
用於驗證功能是否符合規格。

>>>>>>> Stashed changes:instructions/CLZ/README.md
- 對應 Checkpoint：CP1
- 內容：CLZ 的 C 參考實作與內建測試程式

## 函式介面

```c
uint32_t clz(uint32_t x);
```

函式接收 32-bit 無號整數，回傳從最高位元開始連續的前導零數量。
輸入為 `0x00000000` 時，依規格回傳 `32`。

## 實作方法

實作依序檢查 16、8、4、2、1 位元區段。若目前區段全為零，
就累加該區段的位元數並將輸入左移相同位數，藉此找出最高位的 `1`。
輸入為零時直接回傳 `32`。

## 編譯與執行

```text
gcc clz.c -std=c11 -Wall -Wextra -Wpedantic -o clz
./clz
```

Windows：

```text
gcc clz.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
clz.exe
```

## 測試案例

完整測試向量保存於 [`../tests/test_vectors.txt`](../tests/test_vectors.txt)，
測試程式會比對實際結果與預期結果，並在任一案例失敗時回傳非零狀態。

| Test case | Input | Expected CLZ | 測試目的 |
|---:|---|---:|---|
| 1 | `0x80000000` | 0 | 最高位元為 1 |
| 2 | `0x40000000` | 1 | 1 個前導零 |
| 3 | `0x20000000` | 2 | 2 個前導零 |
| 4 | `0x10000000` | 3 | 3 個前導零 |
| 5 | `0x08000000` | 4 | nibble 邊界 |
| 6 | `0x01000000` | 7 | byte 邊界 |
| 7 | `0x00100000` | 11 | 非邊界位元位置 |
| 8 | `0x00010000` | 15 | 16-bit 邊界 |
| 9 | `0x00000001` | 31 | 僅最低位元為 1 |
| 10 | `0x00000000` | 32 | 零輸入邊界案例 |
| 11 | `0x00F00000` | 8 | 多個相鄰位元為 1 |
| 12 | `0x0000FFFF` | 16 | 低 16 位元為 1 |
