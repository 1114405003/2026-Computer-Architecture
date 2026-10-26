# CLZ source code

本資料夾包含 CLZ（Count Leading Zeros，計算前導零）的 CP1 與 CP2
原始碼。CLZ 接收 32-bit 無號整數，回傳從最高位開始連續的零數量；
輸入為 `0x00000000` 時依規格回傳 `32`。

## 目錄結構

```text
src/
├── README.md
├── c_baseline/
│   ├── clz.c
│   └── main.c
└── rv32im/
    ├── README.md
    ├── clz.s
    ├── clz_wrapper.c
    └── clz_wrapper.h
```

## CP1：C baseline

### 函式介面

```c
uint32_t clz(uint32_t x);
```

### 演算法

[`c_baseline/clz.c`](./c_baseline/clz.c) 使用 16、8、4、2、1 位元的
分段檢查。若目前區段全部為零，就累加該區段的位元數並將輸入左移
相同位數，最後定位最高位的 `1`。輸入為零時直接回傳 `32`。

### 編譯與執行

在專案根目錄執行：

```powershell
gcc src/c_baseline/clz.c src/c_baseline/main.c `
    -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
.\clz.exe
```

若 PowerShell 找不到 GCC，可先加入 MSYS2 UCRT64：

```powershell
$env:Path = 'C:\msys64\ucrt64\bin;' + $env:Path
```

CP1 使用 10 組測試向量，資料位於 [`../tests/`](../tests/)：

- [`test_vectors.txt`](../tests/test_vectors.txt)：輸入向量。
- [`expected_output.txt`](../tests/expected_output.txt)：預期輸出。

## CP2：RV32IM baseline

[`rv32im/`](./rv32im/) 是 CP2 的唯一 RV32IM 實作位置。它將 CP1
演算法改寫為 RV32I 基礎指令，不使用 Zbb 的原生 `clz` 指令。

CP2 的輸入與回傳值都使用 `a0`，詳細的組合語言、wrapper、測試方式與
指令統計請參考 [`rv32im/README.md`](./rv32im/README.md)。

## 相關測試與報告

| 內容 | 路徑 |
|---|---|
| CP1 測試向量 | [`../tests/test_vectors.txt`](../tests/test_vectors.txt) |
| CP1 預期輸出 | [`../tests/expected_output.txt`](../tests/expected_output.txt) |
| CP2 trace runner | [`../tests/cp2_trace.py`](../tests/cp2_trace.py) |
| CP1 報告 | [`../report/CP1.md`](../report/CP1.md) |
| CP2 報告 | [`../report/CP2.md`](../report/CP2.md) |
| CP3 規格 | [`../spec/README.md`](../spec/README.md) |
