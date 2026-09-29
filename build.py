#!/usr/bin/env python3
"""Render data/cases.json + template.html into index.html (static, no JS needed to read)."""
import html
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://zhenninglang.github.io/jev-cases/"
REPO = "https://github.com/ZhenningLang/jev-cases"

# Plate illustrations: one sample question per category, drawn as a Jev-style answer.
# These are made-up examples of the question type, labelled 示意 on the page, not measured data.
ART = {
    "browser": {"type": "choice", "q": "下一步点哪个元素？", "opts": [["#search-btn", .86], ["#cookie-ok", .09], ["#nav-login", .04], ["其他", .01]]},
    "routing": {"type": "choice", "q": "这个任务交给哪个模型？", "opts": [["Astra·low", .64], ["Fable·high", .21], ["本地 Qwen", .15]]},
    "judge": {"type": "score", "q": "这篇文章和 AI 编程的相关度（1–5）", "ps": [.02, .05, .13, .52, .28]},
    "safety": {"type": "choice", "q": "这条 shell 命令怎么处理？", "opts": [["block", .69], ["confirm", .24], ["allow", .07]]},
    "realtime": {"type": "choice", "q": "贪吃蛇下一步往哪走？", "opts": [["→", .72], ["↓", .19], ["↑", .08], ["←", .01]]},
    "context": {"type": "noul", "q": "这段技能说明和当前任务相关吗？", "t": .83},
    "platform": {"type": "noul", "q": "这条回答被给定上下文支持吗？", "t": .91},
    "opensource": {"type": "choice", "q": "这条工单属于哪一类？（本地 4B）", "opts": [["退款", .74], ["物流", .17], ["其他", .09]]},
}
EV = {"官方": "official", "第三方实测": "third", "作者自报": "self", "转述未核": "relay"}
POL = {"正面": "pos", "反面": "neg", "中性": "neu"}
e = lambda s: html.escape(str(s or ""), quote=True)


def dist(opts):
    top = max(p for _, p in opts)
    return "".join(
        f'<div class="row{" win" if p == top else ""}"><span class="name">{e(n)}</span>'
        f'<span class="track"><span class="fill" style="display:block" data-w="{p * 100:.0f}"></span></span>'
        f'<span class="p">{p:.2f}</span></div>'
        for n, p in opts)


def art(a):
    if a["type"] == "score":
        top = max(a["ps"])
        viz = '<div class="scale">' + "".join(
            f'<div class="col{" win" if p == top else ""}"><div class="bar" data-h="{p / top * 100:.0f}"></div><span>{i + 1}</span></div>'
            for i, p in enumerate(a["ps"])) + "</div>"
    elif a["type"] == "noul":
        t = a["t"]
        viz = (f'<div class="noul"><div class="split"><div style="width:{t * 100:.0f}%;background:var(--accent)"></div>'
               f'<div style="width:{(1 - t) * 100:.0f}%;background:var(--bar)"></div></div>'
               f'<div class="legend"><span>true {t:.2f}</span><span>false {1 - t:.2f}</span></div></div>')
    else:
        viz = f'<div class="dist">{dist(a["opts"])}</div>'
    return (f'<div class="q">{e(a["q"])}</div>{viz}'
            f'<div style="display:flex;justify-content:space-between;color:var(--muted)"><span>{a["type"]}</span><span>示意</span></div>')


def case(c, i, k):
    cid = f'{c["id"]}-{i + 1}'
    ev, pol = EV.get(k["evidence"], "relay"), POL.get(k["polarity"], "neu")
    title = (f'<a href="{e(k["url"])}" target="_blank" rel="noopener">{e(k["title"])} ↗</a>' if k.get("url") else e(k["title"]))
    return f'''
        <li class="case" id="{cid}" data-ev="{ev}" data-pol="{pol}">
          <span class="date">{e(k.get("date", "")[5:])}</span>
          <div class="main">
            <div class="title">{title}<a class="anchor" href="#{cid}" aria-label="本案例链接">#</a><span class="who">{e(k["who"])}</span></div>
            <p class="what">{e(k["what"])}</p>
          </div>
          <div class="result"><span class="pol {pol}" title="{e(k["polarity"])}"></span>{e(k["result"])}</div>
          <span class="ev {ev}">{e(k["evidence"])}</span>
        </li>'''


def main():
    data = json.loads((ROOT / "data/cases.json").read_text())
    cats, ov = data["categories"], data["overview"]
    missing = [c["id"] for c in cats if c["id"] not in ART]
    if missing:
        sys.exit(f"no plate illustration for category: {missing} (add it to ART in build.py)")
    total = sum(len(c["cases"]) for c in cats)
    plates = "".join(f'''
    <a class="plate" href="#{c["id"]}">
      <div class="art" aria-hidden="true">{art(ART[c["id"]])}</div>
      <div class="body">
        <h3>{e(c["name"])}<span class="n">{len(c["cases"])} 例</span></h3>
        <p>{e(c["tagline"])}</p>
        <span class="go">查看案例 ↓</span>
      </div>
    </a>''' for c in cats)
    sections = "".join(f'''
    <section class="cat" id="{c["id"]}" aria-labelledby="h-{c["id"]}">
      <div class="cat-head">
        <div><div class="label">{len(c["cases"])} 个案例</div><h2 id="h-{c["id"]}">{e(c["name"])}</h2></div>
        <div><p class="tag">{e(c["tagline"])}</p><p>{e(c["intro"])}</p></div>
      </div>
      <ul class="cases">{"".join(case(c, i, k) for i, k in enumerate(c["cases"]))}
      </ul>
      <p class="empty" hidden>这一类没有符合筛选条件的案例。</p>
    </section>''' for c in cats)
    facts = "".join(f'<div><span class="label">{k}</span><b>{e(v)}</b></div>' for k, v in
                    [("发布", "2026-09-14"), ("收录案例", f"{total} 个"), ("分类", f"{len(cats)} 类")])
    desc = f"{total} 个 Jev 真实落地案例，按「让它判断什么」分成 {len(cats)} 类，每条附数字、来源与证据强度。"
    out = (ROOT / "template.html").read_text()
    for key, val in {
        "__DESC__": e(desc), "__SITE__": SITE, "__REPO__": REPO, "__UPDATED__": date.today().isoformat(),
        "__LEDE__": e(ov["what_is_jev"]), "__FACTS__": facts, "__CAVEAT__": e(ov["caveat"]),
        "__HERO__": dist([["billing", .81], ["tech-support", .12], ["sales", .05], ["spam", .02]]),
        "__COUNT__": f"{len(cats)} 类 · {total} 个案例 · 点卡片跳到该类",
        "__PLATES__": plates, "__CATS__": sections,
    }.items():
        out = out.replace(key, val)
    left = [t for t in ("__DESC__", "__SITE__", "__REPO__", "__PLATES__", "__CATS__") if t in out]
    if left:
        sys.exit(f"unfilled placeholders: {left}")
    (ROOT / "index.html").write_text(out)
    print(f"index.html: {len(cats)} categories, {total} cases, {len(out):,} bytes")


if __name__ == "__main__":
    main()
