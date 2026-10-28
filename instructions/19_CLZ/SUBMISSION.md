# 繳交與 Git 流程

## 1. 目前遠端 tag

以 `git ls-remote --tags origin` 取得：

| Tag | Commit | 說明 |
|---|---|---|
| `cp1-submit` | `b72b111721ecb081c392eec7841cc2d15175a621` | CP1 繳交點 |
| `cp2-submit` | `5985985017b7a013bc286c30ca7658af9aa490d8` | CP2 繳交點 |
| `cp3-submit` | `4f518f5db99a429a6baed616a57905a563e5c97e` | CP3 繳交點 |

三個 tag 都存在於遠端。若課程平台以 tag 的推送時間判定，請以平台顯示
的時間為準；本文件只記錄目前遠端狀態。

## 2. 正確的分支與 PR 流程

HOMEWORK 5.1 要求每位組員在自己的 `dev/<學號>` 分支開發，不直接推到
`main`。下一次繳交請依下列流程：

```text
# 1. 從最新的 main 開自己的分支
git checkout main
git pull origin main
git checkout -b dev/<學號>

# 2. 在自己的分支修改、commit
git add <files>
git commit -m "<說明>"
git push -u origin dev/<學號>

# 3. 在 GitHub 開 Pull Request
#    base: main
#    compare: dev/<學號>        ← 不可以選 main 當 compare

# 4. 組長合併 PR 後，在 main 打 tag
git checkout main
git pull origin main
git tag -a cpX-submit -m "CPX submit"
git push origin cpX-submit
```

## 3. 本次已整理的項目

- 刪除重複的 `rv32im/` 實作，只保留 `src/rv32im/`。
- 刪除 `tests/tests/`、`tests/CONTRIBUTIONS.md`、`clz.exe` 與未引用圖片。
- `CONTRIBUTIONS.md` 放在題目目錄 `instructions/19_CLZ/`，不在 `tests/`。
- CP3 只保留一份報告，靜態與動態指令數分開標示。
- `funct3`／`funct7` 依公告改為 `000`／`0000000`。
- 補上 `clz_spec.md` 的 RV32IM baseline 片段。
- 由實際執行重新產生 `actual_output.txt`、`cp2_trace_output.txt`、
  `cp3_test_output.txt` 等證據檔。

## 4. 還需要組員完成

- 每位組員在自己的 `dev/<學號>` 分支留下至少一個有意義的 commit。
- 下一次 PR 的 compare 分支必須是 `dev/<學號>`，不是 `main`。
- PR 標題與內容要與該次 Checkpoint 一致，不要把 CP1 與 CP2 混在一起。
- 合併後再打 `cpX-submit` tag，並確認 tag 已推到遠端。
