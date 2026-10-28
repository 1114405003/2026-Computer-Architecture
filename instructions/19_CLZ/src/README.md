# CLZ source code

本資料夾包含 CLZ 的 CP1 與 CP2 原始碼。

```text
src/
├── README.md
├── c_baseline/
│   ├── README.md
│   ├── clz.c
│   └── main.c
└── rv32im/
    ├── README.md
    ├── clz.s
    ├── clz_loop.s
    ├── clz_wrapper.h
    ├── clz_wrapper.c
    ├── test_clz.c
    └── Makefile
```

## CP1：C baseline

介面：

```c
uint32_t clz(uint32_t x);
```

[`c_baseline/clz.c`](./c_baseline/clz.c) 使用 16、8、4、2、1 位元分段檢查；
輸入為零時直接回傳 `32`。測試程式 [`c_baseline/main.c`](./c_baseline/main.c)
包含 12 組測試向量，會逐組比對並輸出 `PASS` 或 `FAIL`。

從 `instructions/19_CLZ` 執行：

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
./clz.exe
```

## CP2：RV32IM baseline

[`rv32im/`](./rv32im/) 包含兩個 RV32I 實作：

- `clz.s`：16/8/4/2/1 分段檢查（主要 baseline）。
- `clz_loop.s`：逐位元左移迴圈（只用於 CP2 寫法比較）。

兩者都不使用 Zbb 擴充的 `clz` 指令。C wrapper 位於
[`rv32im/clz_wrapper.h`](./rv32im/clz_wrapper.h)，使用
`.insn r 0x0b, 0, 0, rd, rs1, x0` 產生 custom-0 指令；非 RISC-V
平台會 fallback 到 `clz_rv32im()`。

詳細說明見 [`rv32im/README.md`](./rv32im/README.md)。

## 相關測試與報告

| 內容 | 路徑 |
|---|---|
| CP1 測試向量 | [`../tests/test_vectors.txt`](../tests/test_vectors.txt) |
| CP1 預期輸出 | [`../tests/expected_output.txt`](../tests/expected_output.txt) |
| CP1 實際輸出 | [`../tests/actual_output.txt`](../tests/actual_output.txt) |
| CP2 trace runner | [`../tests/cp2_trace.py`](../tests/cp2_trace.py) |
| CP3 規格 | [`../spec/clz_spec.md`](../spec/clz_spec.md) |
| CP1 報告 | [`../report/CP1.md`](../report/CP1.md) |
| CP2 報告 | [`../report/CP2.md`](../report/CP2.md) |
| CP3 報告 | [`../report/CP3.md`](../report/CP3.md) |
