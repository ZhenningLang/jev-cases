# 每周更新：给 agent 的提示词

读 `.notes/jev_sections.md`、`.notes/jev_mentions.md`（`scripts/pull_notes.sh` 拉下来的笔记）和 `data/cases.json`。`jev_mentions.md` 是挂在无关条目下的 Jev 内容（如实测写进了别的新闻条目），别漏看。

1. 先分清两部分，不要混：
   - **落地**（主体，`part` 缺省）：有人把 Jev 本身用在具体场景并给出结果，或实测 Jev。纯营销回声、观点、科普、无来源的不要。
   - **跟进与复刻**（`"part": "follow"`）：别人照着 Jev 做的东西，不是 Jev 的落地。开源复刻、自训模型、本地部署方案放 `opensource`；竞品接口、托管和本地运行环境放 `rivals`。
   - 拿不准时问一句：去掉 Jev 这件事还成立吗？成立就是跟进，不成立就是落地。
2. 找出笔记里 `cases.json` 还没有的条目，按现有分类追加到该类末尾（单条链接 `#<类>-<序号>` 已被分享，不要插队或挪动已有条目）。只有一类攒够 4 个以上、且现有分类都放不下时，才新开一类；新开的落地类要在 `build.py` 的 `SVG` 里补一张示意图，跟进类不需要。
3. 字段照现有格式：`title / who / what(≤40字) / result(≤50字) / evidence / polarity / date / url`。
   - 数字、链接、人名只能照抄笔记原文，不补、不改。一行笔记挂了多个链接时，核对每个链接属于谁（如 `https://api.fxtwitter.com/status/<id>`），对不上就留空字符串。
   - `evidence`：官方（release notes 或官方账号）/ 第三方实测（独立的人测的）/ 作者自报 / 转述未核。
4. 如果新条目改变了某类的结论，同步改该类的 `intro`。
5. 跑 `python3 build.py`，确认输出的落地数、跟进数与预期一致，再提交。
