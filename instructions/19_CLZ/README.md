# CLZ — Count Leading Zeros

本目錄是 group05 的專題題目 **CLZ**（Count Leading Zeros，前導零計數）。
組名：**CLZ**。

CLZ 接收一個 32-bit `uint32_t`，回傳從 bit 31 開始連續的 0 的個數；
輸入為 `0x00000000` 時，依規格回傳 `32`。

## 目錄結構

```text
19_CLZ/
├── README.md                 # 本文件
├── CONTRIBUTIONS.md          # 個人貢獻聲明
├── SUBMISSION.md             # Git 繳交流程與 tag 證據
├── spec/
│   ├── README.md             # CP3 規格索引
│   ├── clz_spec.md           # 6.7 格式的正式規格
│   └── clz_encoding.py       # encoder / decoder / golden model
├── src/
│   ├── README.md
│   ├── c_baseline/           # CP1：C baseline
│   │   ├── README.md
│   │   ├── clz.c
│   │   └── main.c
│   └── rv32im/               # CP2：RV32IM baseline 與 C wrapper
│       ├── README.md
│       ├── clz.s             # 16/8/4/2/1 分段檢查
│       ├── clz_loop.s        # 逐位元迴圈（比較用）
│       ├── clz_wrapper.h
│       ├── clz_wrapper.c
│       ├── test_clz.c
│       └── Makefile
├── tests/
│   ├── README.md
│   ├── EVIDENCE.md           # 工具、指令、實際輸出
│   ├── test_vectors.txt
│   ├── expected_output.txt
│   ├── actual_output.txt
│   ├── cp2_trace.py
│   ├── cp2_trace_output.txt
│   ├── cp2_trace_detail.txt
│   ├── cp3_test.py
│   ├── cp3_test_output.txt
│   ├── cp3_encoding_output.txt
│   ├── qemu/                 # QEMU RV32IM 執行用檔案
│   ├── qemu_output.txt
│   ├── qemu_disassembly.txt
│   └── qemu_size.txt
├── report/
│   ├── README.md
│   ├── CP1.md
│   ├── CP2.md
│   ├── CP3.md
│   └── figures/
│       ├── README.md
│       ├── cp1_c_baseline.png
│       ├── cp2_trace.png
│       ├── cp2_qemu.png
│       ├── cp3_tests.png
│       └── cp3_encoding.png
└── references/
    └── README.md
```

## 快速開始

以下指令都在 `instructions/19_CLZ` 目錄執行。

### CP1：C baseline

```text
gcc src/c_baseline/clz.c src/c_baseline/main.c -std=c11 -Wall -Wextra -Wpedantic -o clz.exe
./clz.exe
```

預期最後一行：`12/12 tests passed.`

### CP2：QEMU RV32IM 實際執行

```text
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -ffreestanding -fno-builtin -nostdlib -nostartfiles -T tests/qemu/link.ld -o tests/qemu/clz_qemu.elf tests/qemu/start.S src/rv32im/clz.s src/rv32im/clz_loop.s tests/qemu/test_qemu.c
qemu-system-riscv32 -machine virt -cpu rv32 -bios none -kernel tests/qemu/clz_qemu.elf -nographic -no-reboot
```

預期最後一行：`12/12 tests passed`

### CP2：RV32IM 指令數 trace

```text
python tests/cp2_trace.py
python tests/cp2_trace.py --detail 0x00010000
```

`cp2_trace.py` 會逐條執行 `src/rv32im/clz.s` 與 `src/rv32im/clz_loop.s`，
輸出動態指令數與條件分支數。完整工具與限制見
[`tests/EVIDENCE.md`](./tests/EVIDENCE.md)。

### CP3：語意與編碼

```text
python tests/cp3_test.py
python spec/clz_encoding.py
```

## 目前狀態

| Checkpoint | 內容 | 狀態 |
|---|---|---|
| CP1 | C baseline、12 組測試向量、預期輸出與實際輸出 | 完成 |
| CP2 | `clz.s`、`clz_loop.s`、C wrapper、靜態/動態指令數與分支數 | 完成 |
| CP3 | 語意、虛擬碼、R-type 編碼、3 個範例、指令數比較 | 完成 |

## 文件索引

| 文件 | 說明 |
|---|---|
| [`report/CP1.md`](./report/CP1.md) | CP1 演算法、測試設計與結果 |
| [`report/CP2.md`](./report/CP2.md) | CP2 組合語言、指令統計與兩種寫法比較 |
| [`report/CP3.md`](./report/CP3.md) | CP3 規格、編碼、範例與指令數比較 |
| [`spec/clz_spec.md`](./spec/clz_spec.md) | 6.7 格式的正式語意規格 |
| [`tests/EVIDENCE.md`](./tests/EVIDENCE.md) | 執行環境、指令與輸出證據 |
| [`CONTRIBUTIONS.md`](./CONTRIBUTIONS.md) | 個人貢獻聲明 |
