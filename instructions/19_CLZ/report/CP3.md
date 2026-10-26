CP3：自訂指令規格與編碼

## 1. 本次目標

完成 CLZ 自訂指令的語意規格、R-type 編碼、至少一組完整 32-bit
編碼位元說明，以及對 RV32IM baseline 的指令數比。R-type 欄位依老師
指定的順序與位元寬度 `7-5-5-3-5-7` 配置。

## 2. 設計內容

### 2.1 語意

- 指令：`clz rd, rs1`
- 語意：`rd = CLZ(rs1)`；`rs1 = 0` 時 `rd = 32`。
- `rs2` 不使用，固定為 0。
- 結果範圍：0 <= rd <= 32。

虛擬碼：

```text
CLZ(rs1):
    if rs1 == 0:
        return 32
    count = 0
    for i = 31 down to 0:
        if bit(rs1, i) == 1:
            return count
        count = count + 1
```

### 2.2 編碼

- Opcode：custom-0 = `0001011` (0x0B)
- Format：R-type
- funct3 / fun3 / f3 = `101` (5)
- funct7 / fun7 / f7 = `0000000`
- rd / rs1 / rs2 各 5 bits。

範例 `clz a0, a1` (`rd=x10`, `rs1=x11`) 的 32-bit 編碼：
`0x0005D50B` =
`0000000 00000 01011 101 01010 0001011`。

欄位寬度由左至右為：

| 欄位 | `fun7/f7` | `rs2` | `rs1` | `fun3/f3` | `rd` | `opcode` |
|---|---:|---:|---:|---:|---:|---:|
| 位元數 | 7 | 5 | 5 | 3 | 5 | 7 |

### 2.3 指令數比

- 計數方式：動態指令數 (per `clz` function call)。
- RV32IM baseline 靜態 25 條；custom 靜態 1 條。
- 樣本見 `../spec/clz_spec.md`。

## 3. 結果與分析

CLZ 是 bit-scan operation，RV32IM baseline 需 3..23 條動態指令；
自訂指令壓縮為 1 條，reduction 介於 66.7% ~ 95.7%。這個 reduction 隨
前導零越多而越高。

未模擬 cycle / pipeline，僅比較指令數；模擬器未使用。

## 4. 遭遇的問題與解法

- 需要指定 fun3 / fun7（RISC-V 標準名稱為 funct3 / funct7），因為
  custom-0 共用 opcode；本組選擇 `fun3=5`、`fun7=0`，並在報告中記錄。
- `rs2` 不使用但 R-type 仍保留欄位，固定為 0 以避免誤解成其他指令。

## 5. 白話說明

CP3 把 CLZ 變成一個新的 CPU 指令。因為 RISC-V 的自訂指令格式像
填表：opcode 說「這是 custom-0」，funct3 說「其中的 CLZ」，剩下的
欄位填暫存器編號。這樣編譯器 / 組譯器就知道要把哪個 bit 放在哪。

## 5.1 5 Whys

1. 為什麼要設計 custom CLZ？因為 baseline 需要多條位元檢查指令。
2. 為什麼使用 R-type？因為指令需要指定 `rd` 與 `rs1`，且課程統一要求 R-type。
3. 為什麼 `rs2` 固定為 0？因為 CLZ 是一元運算，不需要第二個輸入。
4. 為什麼選 `fun3=5`、`fun7=0`？因為 custom-0 仍需用欄位識別這個自訂指令。
5. 為什麼比較動態指令數而不是 cycle？因為作業明確不要求 cycle，且 pipeline 尚未教授。

## 6.1 測試方法

執行 `spec/clz_encoding.py` 可驗證編碼、解碼、四組 CLZ 邊界/一般案例，
以及指令數比較資料：

```text
python spec/clz_encoding.py
```

測試確認 `clz a0, a1 = 0x0005D50B`，且四組結果為
`0、15、31、32`。本次未使用模擬器。

## 6. AI 使用說明

- 工具：Copilot / IDE 助手。
- 用途：協助產生編碼欄位、golden model Python 與指令數表格。
- 本組自行驗證位元欄位、範例編碼值與結果範圍。

## 7. 小組資訊與貢獻聲明

同 [CONTRIBUTIONS.md](../CONTRIBUTIONS.md)：李玉蓉 28.33%、蔡珽州 28.33%、
吳軒宇 15%、温冠筑 28.34%。組名：CLZ。