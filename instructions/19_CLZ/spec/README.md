# CLZ 自訂指令規格與驗證工具（CP3）

本資料夾包含 CLZ 自訂指令的正式語意、R-type 編碼、機器碼範例、
golden model 與指令數比較。

| 檔案 | 用途 |
|---|---|
| [`clz_spec.md`](./clz_spec.md) | 依 HOMEWORK 6.7 格式撰寫的正式規格 |
| [`clz_encoding.py`](./clz_encoding.py) | encoder、decoder、golden model |

## 指令摘要

```text
clz rd, rs1
rd = CLZ(rs1)
```

- 格式：R-type，custom-0，opcode = `0001011`（`0x0B`）
- funct3 = `000`（0）
- funct7 = `0000000`（0）
- `rs2` 不使用，固定為 `x0`
- 結果範圍：`0..32`；`rs1 = 0` 時 `rd = 32`

## 執行

從 `instructions/19_CLZ` 執行：

```text
python spec/clz_encoding.py
python tests/cp3_test.py
```

詳細規格與指令數比較見 [`clz_spec.md`](./clz_spec.md)。
