# Jev 落地图鉴

收集 TypeSafe Jev（只回答选择题、输出概率的决策模型）的真实案例，按「让它判断什么」分类，每条附数字、来源和证据强度。另列一部分「跟进与复刻」：开源复刻、竞品和本地运行环境，与案例分开。

在线版：https://zhenninglang.github.io/jev-cases/

漏了什么或写错了，请[提交 Issue](https://github.com/ZhenningLang/jev-cases/issues/new)，附上来源链接。

## 结构

| 文件 | 作用 |
| --- | --- |
| `data/cases.json` | 案例数据，唯一的事实源；`"part": "follow"` 的类进「跟进与复刻」区，其余是落地 |
| `template.html` | 页面样式和骨架 |
| `build.py` | 把数据渲染进 `index.html`（静态页面，不靠 JS 也能读） |
| `scripts/pull_notes.sh` | 从私有 RSS 笔记拉取 Jev 相关条目和散落提及到 `.notes/`（不入库） |
| `scripts/update_prompt.md` | 每周更新时交给 agent 的提示词 |

## 更新

```bash
CLAW_HOST=user@host scripts/pull_notes.sh   # 拉笔记
# 让 agent 按 scripts/update_prompt.md 更新 data/cases.json
python3 build.py                            # 生成 index.html
# 分享图（可选）：Chrome headless 截 1200x630 到 og.png
git commit -am "update cases" && git push   # GitHub Pages 自动发布
```
