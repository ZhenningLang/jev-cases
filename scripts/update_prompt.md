# 每周更新：给 agent 的提示词

读 `.notes/jev_sections.md`（`scripts/pull_notes.sh` 拉下来的笔记）和 `data/cases.json`。

1. 找出笔记里 `cases.json` 还没有的**真实落地或实测案例**：有人把 Jev 用在具体场景并给出结果。纯营销回声、观点、无来源的不要。
2. 按现有分类追加。只有一类攒够 4 个以上案例、且现有分类都放不下时，才新开一类；新类要在 `build.py` 的 `ART` 里补一张示意图。
3. 字段照现有格式：`title / who / what(≤40字) / result(≤50字) / evidence / polarity / date / url`。
   - 数字、链接、人名只能照抄笔记原文，不补、不改。没有 URL 就留空字符串。
   - `evidence`：官方（release notes 或官方账号）/ 第三方实测（独立的人测的）/ 作者自报 / 转述未核。
4. 如果新案例改变了某类的结论，同步改该类的 `intro`。
5. 跑 `python3 build.py`，确认输出的案例数与预期一致，再提交。
