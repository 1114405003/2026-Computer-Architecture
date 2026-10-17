# CLZ CP2 - RV32IM 實作

本文件為 `CLZ` 指令的 CP2 內容，使用標準 RV32IM 指令實作
32-bit 整數的前導零計數，不使用 RISC-V `Zbb` 擴充中的 `clz` 指令。

## 語意

`clz_rv32im(rs1)` 回傳 `rs1` 從 bit 31 開始連續的零數量。

- `rs1 = 0` 時回傳 `32`
- `0x80000000` 時回傳 `0`
- 回傳值範圍為 `0..32`

## 檔案

| 檔案 | 用途 |
|---|---|
| `rv32im/clz.S` | RV32IM 組合語言函式 |
| `rv32im/test_clz.c` | 測試驅動程式與 11 組測試向量 |
| `rv32im/Makefile` | 使用 `riscv64-unknown-elf-gcc` 編譯 RV32IM 目標檔 |
| `rv32im/README.md` | CP2 設計、指令統計與分析 |

## 編譯

在 `rv32im` 目錄執行：

```bash
make
```

編譯選項固定為 `-march=rv32im -mabi=ilp32`。Makefile 預設產生
`clz.o` 與 `test_clz.o`，再依課堂指定的 startup 與 linker script
連結成可在模擬器執行的映像檔。

本實作及測試內容須由組員自行理解、驗證，並在 CP2 報告的 AI 使用說明中揭露必要的協助。
