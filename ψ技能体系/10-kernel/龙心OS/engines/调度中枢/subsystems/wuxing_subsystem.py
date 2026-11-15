# -*- coding: utf-8 -*-
"""
龙心OS · 五行人格心理学OS 常驻子系统（深度共生）
================================================

定位：凤系列三OS（凤爪·执行 / 凤心·决策 / 凤脑·知识）作为龙心OS 1+5 总调度的
**常驻五行执行子系统**。本模块是龙心侧的总调度入口，负责：
  - detect(text)        检测输入是否属于五行人格心理学域（亲密/亲子/领导/健康/测评/五行…）
  - dispatch(text)      经subprocess调用五行OS顶层编排器，跑通 凤爪→凤心→凤脑 全闭环
  - report_to_longxin() 将五行运行结果回灌龙心OS共享共生记忆（longxin_symbiosis_feed.jsonl）
  - heartbeat()         常驻存活探针，供龙心OS调度中枢健康检查

设计纪律（与五行OS内部一致）：
  - 全部导入/派发/写盘均 try/except 降级——五行OS不可达时龙心OS主流程不受任何影响。
  - 路径用 os.path.expanduser 解析，跨用户/跨机稳定。
  - 与五行OS侧 longxin_bridge 共享同一 feed 路径常量，保证双向闭环落点一致。

版本：v1.0（深度共生·2026-07-29）
"""

import os
import sys
import json
import subprocess
import datetime


# ──────────────────────────────────────────────────────────────────────────
# 路径解析（龙心侧 ↔ 五行侧必须一致）
# ──────────────────────────────────────────────────────────────────────────
def resolve_orchestrator():
    """定位五行人格心理学OS顶层编排器（subprocess隔离·与五行OS内部同构）"""
    p = os.path.expanduser(
        "~/.workbuddy/skills/五行人格心理学OS/framework/orchestrator.py"
    )
    return p if os.path.isfile(p) else None


def resolve_longxin_feed():
    """龙心OS ↔ 五行OS 共享共生记忆落点（单行JSON-Lines）。

    龙心侧作为总调度/记忆owner写入；五行侧 longxin_bridge 读取同一文件做上行治理核对。
    """
    return os.path.expanduser(
        "~/.workbuddy/skills/五行人格心理学OS/runtime/longxin_symbiosis_feed.jsonl"
    )


# 五行人格心理学域意图关键词（强信号；避免与CZ通用"成长"误触）
WUXING_INTENT_TOKENS = [
    "五行", "人格", "亲密", "吵架", "冷战", "对象", "伴侣", "夫妻", "老公", "老婆",
    "亲子", "孩子", "育儿", "教育", "测评", "身心灵", "拔阴取阳", "化克为生",
    "木行人", "火行人", "土行人", "金行人", "水行人", "阴阳", "九层",
    "凤心", "凤脑", "凤爪", "五行人格", "修炼", "五行测评",
]

# 情绪/状态类（中信号，需配合域词才触发，避免泛泛"焦虑"被通用CZ吞掉）
WUXING_STATE_TOKENS = ["失眠", "拖延", "关系", "迷茫", "愤怒", "焦虑"]


class WuxingSubsystem:
    """五行人格心理学OS 常驻子系统（龙心OS 总调度下的五行执行子系统）。"""

    name = "wuxing_os"
    display_name = "五行人格心理学OS（凤系列三OS）"
    resident = True  # 常驻：龙心OS调度中枢加载即注册，非按需临时挂载
    layer = "五行执行子系统"

    # ── 意图检测 ──────────────────────────────────────────────────────────
    def detect(self, text: str) -> bool:
        if not text:
            return False
        t = text
        for tok in WUXING_INTENT_TOKENS:
            if tok in t:
                return True
        # 中信号需至少命中2个，降低误触
        hit = sum(1 for tok in WUXING_STATE_TOKENS if tok in t)
        return hit >= 2

    # ── 派发：龙心 → 五行（运行 凤爪→凤心→凤脑 全闭环）────────────────────
    def dispatch(self, text: str, timeout: int = 90) -> dict:
        orch = resolve_orchestrator()
        if orch is None:
            return {
                "subsystem": self.name,
                "status": "unavailable",
                "reason": "五行OS编排器未挂载（优雅降级）",
                "raw": None,
            }
        try:
            proc = subprocess.run(
                [sys.executable, orch, "--json", text],
                capture_output=True, text=True, timeout=timeout,
            )
            if proc.returncode != 0:
                return {
                    "subsystem": self.name,
                    "status": "error",
                    "reason": proc.stderr.strip()[:300],
                    "raw": None,
                }
            raw = json.loads(proc.stdout)
            return {
                "subsystem": self.name,
                "status": "ok",
                "raw": raw,
                "closed_loop": raw.get("closed_loop"),
            }
        except subprocess.TimeoutExpired:
            return {"subsystem": self.name, "status": "timeout", "reason": "五行OS超时", "raw": None}
        except Exception as e:  # pragma: no cover - 永不拖垮龙心主流程
            return {"subsystem": self.name, "status": "error", "reason": str(e), "raw": None}

    # ── 回灌龙心：五行结果 → 龙心共享共生记忆 ────────────────────────────
    def report_to_longxin(self, text: str, dispatch_result: dict) -> dict:
        """将一次五行运行结果写入龙心OS共享共生记忆（单行JSON-Lines）。

        龙心作为总调度/记忆owner，是feed的唯一写入方；五行侧仅读同一文件做核对。
        """
        feed = resolve_longxin_feed()
        raw = dispatch_result.get("raw") or {}
        # 上行治理载荷（凤心→龙心）：从编排器结果中提取龙心统辖治理信息，便于共享记忆直接核对
        gov = None
        try:
            gov = (raw.get("longxin_governance")
                   or (raw.get("fengxin_decision") or {}).get("decision", {}).get("longxin_governance"))
        except Exception:
            gov = None
        entry = {
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "source": "龙心OS·调度中枢",
            "subsystem": self.name,
            "input": text,
            "status": dispatch_result.get("status"),
            "closed_loop": dispatch_result.get("closed_loop"),
            "governance": gov,
            "raw": raw,
        }
        try:
            os.makedirs(os.path.dirname(feed), exist_ok=True)
            with open(feed, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            entry["fed"] = True
            return entry
        except Exception as e:  # pragma: no cover
            entry["fed"] = False
            entry["feed_error"] = str(e)
            return entry

    # ── 常驻存活探针 ──────────────────────────────────────────────────────
    def heartbeat(self) -> dict:
        orch = resolve_orchestrator()
        return {
            "subsystem": self.name,
            "resident": self.resident,
            "layer": self.layer,
            "orchestrator_mounted": orch is not None,
            "status": "alive" if orch is not None else "degraded",
        }

    # ── 统一入口：detect → dispatch → report（深度共生四层闭环的龙心侧）──
    def handle(self, text: str, confidence: float = None) -> dict:
        if not self.detect(text):
            return {"subsystem": self.name, "handled": False}
        disp = self.dispatch(text)
        report = self.report_to_longxin(text, disp)
        return {
            "subsystem": self.name,
            "handled": True,
            "confidence": confidence,
            "dispatch": disp,
            "report": report,
        }


# 单例（常驻）
wuxing_subsystem = WuxingSubsystem()


if __name__ == "__main__":
    import sys as _sys
    _txt = " ".join(_sys.argv[1:]) or "我和对象吵架冷战了怎么办"
    _r = wuxing_subsystem.handle(_txt)
    print(json.dumps(_r, ensure_ascii=False, indent=2))
