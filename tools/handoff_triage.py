#!/usr/bin/env python3
"""转人工分流判定（零依赖规则基线）。

对一条会话做「可自动处理 / 需人工 / 立即升级」三态判定，
并生成交接摘要，避免 AI 越界承诺、避免用户被反复踢皮球。

v2 修订（2026-09）
------------------
v1 的判定优先级是「升级 > 需人工 > 敏感」，导致**凭据安全被判据需求降级**：
用户说「我要退款，顺便把我的银行卡号发你」时，命中「退款」走「转人工 P1」，
而「银行卡/密码/验证码」这条**安全红线**被跳过 —— 本该 P0 立即拦截、并明确
「禁止自动索要凭据」。v2 把「敏感」提到「需人工」之前：
    升级（P0）> 敏感（P0，凭据安全）> 需人工（P1）> 可自动（P3）> 需判断（P2）
另补：`升级` 命中时若同时命中敏感，摘要里两类都要列全，避免只看 route 漏掉安全提示。

用法:
    python3 handoff_triage.py --file session.txt
    echo "我要投诉 你们这是诈骗" | python3 handoff_triage.py --json
    python3 handoff_triage.py --selftest
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ESCALATE = ["投诉", "举报", "工商", "12315", "起诉", "律师", "曝光", "诈骗", "报警", "差评威胁"]
HUMAN_NEEDED = ["退款", "退货", "赔偿", "发票", "改地址", "特殊", "例外", "经理", "人工", "转人工"]
AUTO_OK = ["尺码", "尺寸", "颜色", "库存", "有货", "发货时间", "运费", "怎么用", "材质", "保质期"]
SENSITIVE = ["密码", "验证码", "身份证", "银行卡", "转账"]


def triage(text: str) -> dict:
    hits = {
        "升级": [w for w in ESCALATE if w in text],
        "敏感": [w for w in SENSITIVE if w in text],
        "需人工": [w for w in HUMAN_NEEDED if w in text],
        "可自动": [w for w in AUTO_OK if w in text],
    }
    # 顺序即优先级：凭据安全（敏感）优先于一般转人工
    if hits["升级"]:
        route, level, sla = "立即升级", "P0", "5 分钟内人工介入"
    elif hits["敏感"]:
        route, level, sla = "转人工", "P0", "立即，禁止自动索要凭据"
    elif hits["需人工"]:
        route, level, sla = "转人工", "P1", "15 分钟内响应"
    elif hits["可自动"]:
        route, level, sla = "自动应答", "P3", "即时"
    else:
        route, level, sla = "需判断", "P2", "建议人工确认后再答"

    summary = text.strip().replace("\n", " ")[:60]
    flat = [x for v in hits.values() for x in v]
    safety = "；安全提示：禁止自动索要或复述任何凭据" if hits["敏感"] else ""
    return {"route": route, "level": level, "sla": sla, "hits": hits,
            "handoff_summary": f"用户诉求：{summary}…（命中关键词：{'/'.join(flat) or '无'}）{safety}"}


def _selftest() -> int:
    """内嵌回归自测：核心断言是「凭据安全不被业务诉求降级」。"""
    checks: list[tuple[str, bool, str]] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))

    # 1) v1 的降级缺陷：退款 + 银行卡 → 必须是 P0 敏感
    r = triage("我要退款，顺便把我的银行卡号发你")
    ck("退款+银行卡 判 P0（不降级为 P1）", r["level"] == "P0", f"实际 {r['level']}")
    ck("退款+银行卡 命中敏感", bool(r["hits"]["敏感"]))
    ck("退款+银行卡 给出凭据安全提示", "禁止自动索要" in r["sla"])
    ck("退款+银行卡 摘要含安全提示", "安全提示" in r["handoff_summary"])

    # 2) 升级优先级仍高于敏感
    r2 = triage("我要投诉，还要报警，我有你们客服的密码")
    ck("升级+敏感 判升级", r2["route"] == "立即升级", f"实际 {r2['route']}")
    ck("升级+敏感 摘要仍列全敏感词", bool(r2["hits"]["敏感"]))
    ck("升级+敏感 摘要含安全提示", "安全提示" in r2["handoff_summary"])

    # 3) 纯升级
    ck("纯投诉判 P0 升级", triage("我要投诉你们这是诈骗")["route"] == "立即升级")
    # 4) 纯转人工
    r4 = triage("我想申请退货")
    ck("退货判 P1 转人工", r4["route"] == "转人工" and r4["level"] == "P1")
    # 5) 纯自动
    r5 = triage("请问有货吗")
    ck("库存咨询判自动应答", r5["route"] == "自动应答")
    # 6) 无法判断
    ck("无关键词判需判断", triage("嗯")["route"] == "需判断")
    # 7) 命中词要如实列出，不能只看 route
    ck("命中的词全部列出", set(r["hits"]["需人工"]) == {"退款"})
    ck("未命中的类别为空", r["hits"]["可自动"] == [])

    fails = [(n, d) for n, ok, d in checks if not ok]
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f" —— {d}" if not ok and d else ""))
    print(f"handoff_triage 自测：{len(checks) - len(fails)}/{len(checks)} 通过")
    return 1 if fails else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()

    ap = argparse.ArgumentParser(description="转人工分流判定")
    ap.add_argument("--file", help="会话内容；缺省 stdin")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    if not text.strip():
        print("错误：会话为空", file=sys.stderr)
        return 2

    r = triage(text)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"处置建议：{r['route']}（{r['level']}）　SLA：{r['sla']}")
        for k, v in r["hits"].items():
            if v:
                print(f"  [{k}] {', '.join(v)}")
        print(f"\n交接摘要：{r['handoff_summary']}")
    return 0 if r["route"] == "自动应答" else 1


if __name__ == "__main__":
    sys.exit(main())
