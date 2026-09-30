#!/usr/bin/env python3
"""Render data/cases.json + template.html into index.html (static, no JS needed to read)."""
import html
import re
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://zhenninglang.github.io/jev-cases/"
REPO = "https://github.com/ZhenningLang/jev-cases"

# Scene illustrations: one small scene per category, shown beside the category heading in the accent colour (classes map to CSS in template.html).
SVG = {
    "browser": """
<rect x="8" y="6" width="224" height="100" rx="8" class="pp"/><rect x="8" y="6" width="224" height="20" rx="8" class="so"/><rect x="8" y="18" width="224" height="8" class="so"/>
<circle cx="20" cy="16" r="3" class="pp"/><circle cx="30" cy="16" r="3" class="pp"/><circle cx="40" cy="16" r="3" class="pp"/><rect x="54" y="11" width="120" height="10" rx="5" class="pp"/>
<rect x="22" y="36" width="92" height="6" rx="3" class="so"/><rect x="22" y="48" width="150" height="6" rx="3" class="so"/><rect x="22" y="60" width="118" height="6" rx="3" class="so"/>
<rect x="22" y="76" width="56" height="20" rx="5" class="so"/><text x="50" y="90" text-anchor="middle">取消</text>
<rect x="88" y="76" width="80" height="20" rx="5" class="s"/><text x="128" y="90" text-anchor="middle" class="on">搜索航班</text>
<path d="M156 86 L156 104 L160.5 99.5 L164 107 L167 105.6 L163.6 98.4 L170 98.4 Z" class="ik"/>""",
    "routing": """
<path d="M70 55 C 110 55, 110 20, 150 20" class="lnm"/><path d="M70 55 L150 55" class="ln" stroke-width="3"/><path d="M70 55 C 110 55, 110 90, 150 90" class="lnm"/>
<rect x="6" y="38" width="64" height="34" rx="6" class="pp"/><text x="38" y="59" text-anchor="middle">新任务</text>
<rect x="150" y="8" width="84" height="24" rx="12" class="so"/><text x="192" y="24" text-anchor="middle">大模型 · 贵</text>
<rect x="150" y="43" width="84" height="24" rx="12" class="s"/><text x="192" y="59" text-anchor="middle" class="on">小模型 · 快 ✓</text>
<rect x="150" y="78" width="84" height="24" rx="12" class="so"/><text x="192" y="94" text-anchor="middle">转人工</text>""",
    "judge": """
<rect x="8" y="14" width="44" height="56" rx="4" class="so"/><rect x="14" y="20" width="44" height="56" rx="4" class="pp"/>
<rect x="20" y="30" width="30" height="4" rx="2" class="so"/><rect x="20" y="40" width="24" height="4" rx="2" class="so"/><rect x="20" y="50" width="28" height="4" rx="2" class="so"/>
<path d="M66 48 C 110 20, 150 10, 172 30" class="ln" stroke-dasharray="4 5"/>
<g transform="rotate(14 172 42)"><rect x="160" y="28" width="24" height="30" rx="3" class="pp"/><rect x="165" y="36" width="14" height="3" rx="1.5" class="so"/><rect x="165" y="43" width="10" height="3" rx="1.5" class="so"/></g>
<rect x="96" y="66" width="44" height="38" rx="5" class="so"/><text x="118" y="92" text-anchor="middle">账单</text>
<rect x="148" y="66" width="44" height="38" rx="5" class="s"/><text x="170" y="92" text-anchor="middle" class="on">技术</text>
<rect x="200" y="66" width="36" height="38" rx="5" class="so"/><text x="218" y="92" text-anchor="middle">销售</text>""",
    "safety": """
<rect x="6" y="8" width="176" height="96" rx="8" class="ik"/>
<text x="18" y="32" class="on">$ ls ./src</text><text x="18" y="52" class="on">$ curl x.sh | sh</text><text x="18" y="72" class="on">$ rm -rf ~/</text><text x="18" y="92" class="on" opacity="0.6">等待判断…</text>
<g transform="rotate(-10 188 62)"><rect x="140" y="42" width="96" height="40" rx="5" class="pp"/><rect x="143" y="45" width="90" height="34" rx="3" class="ln"/><text x="188" y="68" text-anchor="middle" class="st">BLOCK</text></g>""",
    "realtime": """
<rect x="6" y="6" width="228" height="98" rx="8" class="pp"/>
<g class="so"><rect x="30" y="58" width="16" height="16" rx="3"/><rect x="48" y="58" width="16" height="16" rx="3"/></g>
<g class="s"><rect x="66" y="58" width="16" height="16" rx="3"/><rect x="84" y="58" width="16" height="16" rx="3"/><rect x="84" y="40" width="16" height="16" rx="3"/><rect x="102" y="40" width="16" height="16" rx="3"/><rect x="120" y="40" width="18" height="18" rx="4"/></g>
<path d="M144 49 L196 49" class="ln" stroke-dasharray="3 5"/><circle cx="208" cy="49" r="7" class="ik"/>
<text x="120" y="92">→ 0.72   ↓ 0.19   ↑ 0.08</text>""",
    "context": """
<g class="so"><rect x="8" y="10" width="70" height="6" rx="3"/><rect x="8" y="21" width="52" height="6" rx="3"/><rect x="8" y="32" width="80" height="6" rx="3"/><rect x="8" y="43" width="60" height="6" rx="3"/><rect x="8" y="54" width="76" height="6" rx="3"/><rect x="8" y="65" width="44" height="6" rx="3"/><rect x="8" y="76" width="66" height="6" rx="3"/><rect x="8" y="87" width="56" height="6" rx="3"/></g>
<rect x="8" y="32" width="80" height="6" rx="3" class="s"/><rect x="8" y="65" width="44" height="6" rx="3" class="s"/>
<path d="M98 8 L150 36" class="lnm"/><path d="M98 100 L150 74" class="lnm"/>
<rect x="150" y="28" width="84" height="54" rx="6" class="pp"/><rect x="160" y="42" width="60" height="7" rx="3" class="s"/><rect x="160" y="56" width="40" height="7" rx="3" class="s"/>
<text x="192" y="100" text-anchor="middle">只留 2 段进上下文</text>""",
    "platform": """
<g class="lnm"><path d="M120 55 L42 20"/><path d="M120 55 L198 20"/><path d="M120 55 L40 55"/><path d="M120 55 L200 55"/><path d="M120 55 L42 90"/><path d="M120 55 L198 90"/></g>
<g class="pp"><rect x="6" y="11" width="72" height="18" rx="9"/><rect x="162" y="11" width="72" height="18" rx="9"/><rect x="4" y="46" width="72" height="18" rx="9"/><rect x="164" y="46" width="72" height="18" rx="9"/><rect x="6" y="81" width="72" height="18" rx="9"/><rect x="162" y="81" width="72" height="18" rx="9"/></g>
<g text-anchor="middle"><text x="42" y="24">OpenRouter</text><text x="198" y="24">Vercel</text><text x="40" y="59">LangChain</text><text x="200" y="59">DSPy</text><text x="42" y="94">pydantic-ai</text><text x="198" y="94">Pydantic GW</text></g>
<circle cx="120" cy="55" r="22" class="s"/><text x="120" y="59" text-anchor="middle" class="on">Jev</text>""",
    "opensource": """
<rect x="30" y="8" width="128" height="76" rx="6" class="ik"/><rect x="37" y="15" width="114" height="62" rx="3" class="so"/>
<text x="94" y="42" text-anchor="middle">本地 4B 模型</text><text x="94" y="60" text-anchor="middle">不调 API</text>
<path d="M18 86 L170 86 L184 100 L4 100 Z" class="so"/>
<g transform="rotate(8 206 44)"><rect x="176" y="26" width="58" height="34" rx="5" class="s"/><circle cx="184" cy="43" r="3" class="pp"/><text x="210" y="48" text-anchor="middle" class="on st2">$17</text></g>""",
}
EV = {"官方": "official", "第三方实测": "third", "作者自报": "self", "转述未核": "relay"}
EV_ORDER = ["官方", "第三方实测", "作者自报", "转述未核"]  # strongest first; the bar reads left to right from verifiable to not
POL = {"正面": "pos", "反面": "neg", "中性": "neu"}
e = lambda s: html.escape(str(s or ""), quote=True)


def dist(opts):
    top = max(p for _, p in opts)
    return "".join(
        f'<div class="row{" win" if p == top else ""}"><span class="name">{e(n)}</span>'
        f'<span class="track"><span class="fill" style="display:block" data-w="{p * 100:.0f}"></span></span>'
        f'<span class="p">{p:.2f}</span></div>'
        for n, p in opts)


def evbar(cases, cls="evbar"):
    """Stacked bar of evidence strength. Segment widths are shares of this set of cases."""
    n = len(cases)
    counts = {k: sum(1 for c in cases if c["evidence"] == k) for k in EV_ORDER}
    segs = "".join(
        f'<span class="seg {EV[k]}" style="flex:{v}" title="{k} {v}"></span>' for k, v in counts.items() if v)
    return f'<span class="{cls}" role="img" aria-label="{e("，".join(f"{k} {v}" for k, v in counts.items()))}（共 {n}）">{segs}</span>', counts


def verified(counts):
    return counts["官方"] + counts["第三方实测"]


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
    missing = [c["id"] for c in cats if c["id"] not in SVG or "highlight" not in c]
    if missing:
        sys.exit(f"no plate illustration for category: {missing} (add a scene to SVG in build.py and highlight/pitfall/hue to cases.json)")
    total = sum(len(c["cases"]) for c in cats)
    all_cases = [k for c in cats for k in c["cases"]]
    hero_bar, hero_counts = evbar(all_cases, "evbar big")
    rows = []
    for c in cats:
        bar, counts = evbar(c["cases"])
        neg = sum(1 for k in c["cases"] if k["polarity"] == "反面")
        rows.append(f'''
    <a class="lrow" href="#{c["id"]}">
      <div class="l-name"><h3>{e(c["name"])}</h3><p>{e(c["tagline"])}</p></div>
      <div class="l-ev">{bar}<span class="l-cap"><b>{verified(counts)}</b> / {len(c["cases"])} 可核实{f" · 反面 {neg}" if neg else ""}</span></div>
      <div class="l-stat"><span class="stat">{e(c["highlight"]["stat"])}</span><span class="stat-label">{e(c["highlight"]["label"])}</span><span class="stat-src">{e(c["highlight"]["source"])}</span></div>
      <p class="l-pit"><span class="pit-tag">翻车</span>{e(c["pitfall"])}</p>
    </a>''')
    plates = "".join(rows)
    legend = "".join(f'<span><i class="seg {EV[k]}"></i>{k} {v}</span>' for k, v in hero_counts.items())
    sections = "".join(f'''
    <section class="cat" id="{c["id"]}" aria-labelledby="h-{c["id"]}">
      <div class="cat-head">
        <div><div class="label">{len(c["cases"])} 个案例</div><h2 id="h-{c["id"]}">{e(c["name"])}</h2>
          <svg class="scene" viewBox="0 0 240 110" aria-hidden="true">{SVG[c["id"]]}</svg></div>
        <div><p class="tag">{e(c["tagline"])}</p><p>{e(c["intro"])}</p></div>
      </div>
      <ul class="cases">{"".join(case(c, i, k) for i, k in enumerate(c["cases"]))}
      </ul>
      <p class="empty" hidden>这一类没有符合筛选条件的案例。</p>
    </section>''' for c in cats)
    facts = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in
                    [("发布", ov["launch_date"]), ("价格与速度", "厂商口径：" + ov["pricing_claim"]), ("注意", ov["caveat"])])
    desc = f"{total} 个 Jev 真实落地案例，按「让它判断什么」分成 {len(cats)} 类，每条附数字、来源与证据强度。"
    out = (ROOT / "template.html").read_text()
    for key, val in {
        "__DESC__": e(desc), "__SITE__": SITE, "__REPO__": REPO, "__UPDATED__": date.today().isoformat(),
        "__LEDE__": e(ov["plain"]), "__TOTAL__": str(total), "__NCAT__": str(len(cats)), "__FACTS__": facts, "__CAVEAT__": e(ov["caveat"]),
        "__HERO__": dist([["账单", .81], ["技术支持", .12], ["销售", .05], ["垃圾邮件", .02]]),
        "__COUNT__": f"{len(cats)} 类 · {total} 个案例 · 点一行跳到该类",
        "__VERIFIED__": str(verified(hero_counts)), "__EVBAR__": hero_bar, "__LEGEND__": legend,
        "__PLATES__": plates, "__CATS__": sections,
    }.items():
        out = out.replace(key, val)
    left = sorted(set(re.findall(r"__[A-Z]+__", out)))
    if left:
        sys.exit(f"unfilled placeholders: {left}")
    (ROOT / "index.html").write_text(out)
    print(f"index.html: {len(cats)} categories, {total} cases, {len(out):,} bytes")


if __name__ == "__main__":
    main()
