# CLZ C baseline（CP1）

## 函式介面

```c
uint32_t clz(uint32_t x);
```

輸入為 32-bit 無號整數，回傳從 bit 31 開始連續的 0 的個數。
`x == 0` 時回傳 `32`。

## 實作方法

依序檢查 16、8、4、2、1 位元區段：

1. 若高 16 位元全為 0，計數加 16，輸入左移 16 位。
2. 若接下來 8 位元全為 0，計數加 8，輸入左移 8 位。
3. 依序檢查 4、2、1 位元。
4. 全部為 0 時直接回傳 32。

## 測試案例（12 組）

| 測試 | 輸入 | 預期 CLZ | 說明 |
|---:|---|---:|---|
| 1 | `0x80000000` | 0 | bit 31 = 1 |
| 2 | `0x40000000` | 1 | 1 個前導零 |
| 3 | `0x20000000` | 2 | 2 個前導零 |
| 4 | `0x10000000` | 3 | nibble 邊界（bit 28） |
| 5 | `0x08000000` | 4 | bit 27，4 個前導零 |
| 6 | `0x01000000` | 7 | byte 邊界（bit 24） |
| 7 | `0x00100000` | 11 | bit 20 |
| 8 | `0x00010000` | 15 | 16-bit 邊界 |
| 9 | `0x00000001` | 31 | 最低位元為 1 |
| 10 | `0x00000000` | 32 | 全零邊界 |
| 11 | `0x00F00000` | 8 | 多個相鄰位元為 1 |
| 12 | `0x0000FFFF` | 16 | 低 16 位元全為 1 |

## 編譯與執行

從 `instructions/19_CLZ` 執行：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
./clz.exe
```

Windows PowerShell 也可以使用：

```powershell
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
.\clz.exe
```

預期最後一行：

```text
12/12 tests passed.
```

完整輸出見 [`../../tests/actual_output.txt`](../../tests/actual_output.txt)。
