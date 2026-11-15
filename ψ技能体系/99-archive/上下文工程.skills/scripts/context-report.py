# -*- coding: utf-8 -*-
# 上下文报告生成器

import sys, os, json, importlib.util
from pathlib import Path
from datetime import datetime

_BASE = str(Path(__file__).parent.parent)

def _load_mod(relpath):
    full = os.path.join(_BASE, relpath)
    name = os.path.splitext(os.path.basename(relpath))[0]
    spec = importlib.util.spec_from_file_location(name, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_score_mod = _load_mod("quality-assessment/scorer.py")
_check_mod = _load_mod("quality-assessment/checker.py")
_opt_mod = _load_mod("quality-assessment/optimizer.py")
score = _score_mod.score
check = _check_mod.check
auto_optimize = _opt_mod.auto_optimize

REPORT_DIR = Path(__file__).parent.parent / "reports"


def generate_report(context_items, session_id="unknown"):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / ("context-report_%s.json" % ts)
    sc = score(context_items)
    ch = check(context_items)
    opt = auto_optimize(context_items)
    report = {
        "report_id": "CR-%s" % ts,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "context_count": len(context_items),
        "health": ch,
        "quality": sc,
        "optimization": {
            "original_score": opt["original_score"],
            "optimized_score": opt["optimized_score"],
            "tips": opt["tips"]
        }
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    tc = [
        {"key": "project", "value": "AI OS 知识库", "priority": 1},
        {"key": "phase", "value": "Phase 5", "priority": 2},
    ]
    rp = generate_report(tc, "test-001")
    print("报告已生成: %s" % rp)
    data = json.loads(rp.read_text(encoding="utf-8"))
    print("质量评分: %d/100" % data["quality"]["score"])
    print("健康评分: %d/100" % data["health"]["score"])
