# -*- coding: utf-8 -*-
"""
龙心OS · 龙爪OS 常驻子系统（深度共生·执行层）
============================================

定位：龙爪OS（项目执行层）作为龙心OS 1+5 总调度的**常驻执行子系统**。
本模块是龙心侧的总调度入口，负责：
  - detect(text)        检测输入是否属于项目执行域（项目/工作流/SOP/企业文化/味藏/落地…）
  - dispatch(text)      经subprocess调用龙爪OS编排器，跑通 路由→真实执行→进度追踪 全闭环
  - report_to_longxin() 将龙爪运行结果回灌龙心OS共享共生记忆（longzhao_symbiosis_feed.jsonl）
  - heartbeat()         常驻存活探针

设计纪律（与五行子系统同构）：
  - 全部导入/派发/写盘均 try/except 降级——龙爪OS不可达时龙心OS主流程不受影响。
  - 路径用 os.path.expanduser 解析，跨用户/跨机稳定。

版本：v1.0（深度共生·执行层·2026-07-29）
"""

import os
import sys
import json
import subprocess
import datetime


def resolve_orchestrator():
    """定位龙爪OS顶层编排器（subprocess隔离）。"""
    p = os.path.expanduser(
        "~/.workbuddy/skills/龙爪OS/framework/longzhao_orchestrator.py"
    )
    return p if os.path.isfile(p) else None


def resolve_longzhao_feed():
    """龙心OS ↔ 龙爪OS 共享共生记忆落点（单行JSON-Lines）。"""
    return os.path.expanduser(
        "~/.workbuddy/skills/龙爪OS/runtime/longzhao_symbiosis_feed.jsonl"
    )


# 项目执行域意图关键词（强信号）
LONGZHAO_INTENT_TOKENS = [
    "项目", "工作流", "SOP", "执行", "落地", "实施", "推进", "交付", "计划",
    "排期", "流程", "复盘", "里程碑", "周计划", "月计划", "任务分解",
    "企业文化", "味藏", "门店", "经营分析", "方案落地", "体系建设",
    "启动项目", "执行步骤", "查看状态", "调整计划",
]


class LongZhaoSubsystem:
    """龙爪OS 常驻子系统（龙心OS 总调度下的执行子系统）。"""

    name = "longzhao_os"
    display_name = "龙爪OS（项目执行层）"
    resident = True  # 常驻：龙心OS调度中枢加载即注册
    layer = "执行子系统"

    # ── 意图检测 ──────────────────────────────────────────────────────────
    def detect(self, text: str) -> bool:
        if not text:
            return False
        return any(tok in text for tok in LONGZHAO_INTENT_TOKENS)

    # ── 派发：龙心 → 龙爪（运行 路由→真实执行→进度追踪 全闭环）────────────
    def dispatch(self, text: str, timeout: int = 120) -> dict:
        orch = resolve_orchestrator()
        if orch is None:
            return {
                "subsystem": self.name,
                "status": "unavailable",
                "reason": "龙爪OS编排器未挂载（优雅降级）",
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
            return {"subsystem": self.name, "status": "timeout", "reason": "龙爪OS超时", "raw": None}
        except Exception as e:  # pragma: no cover - 永不拖垮龙心主流程
            return {"subsystem": self.name, "status": "error", "reason": str(e), "raw": None}

    # ── 回灌龙心：龙爪结果 → 龙心共享共生记忆 ────────────────────────────
    def report_to_longxin(self, text: str, dispatch_result: dict) -> dict:
        feed = resolve_longzhao_feed()
        raw = dispatch_result.get("raw") or {}
        entry = {
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "source": "龙心OS·调度中枢",
            "subsystem": self.name,
            "input": text,
            "status": dispatch_result.get("status"),
            "closed_loop": dispatch_result.get("closed_loop"),
            "project_type": raw.get("project_type"),
            "workflow_name": raw.get("workflow_name"),
            "progress": (raw.get("progress") or {}).get("overall_progress"),
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
longzhao_subsystem = LongZhaoSubsystem()


if __name__ == "__main__":
    import sys as _sys
    _txt = " ".join(_sys.argv[1:]) or "启动企业文化落地项目，做诊断分析"
    _r = longzhao_subsystem.handle(_txt)
    print(json.dumps(_r, ensure_ascii=False, indent=2))
