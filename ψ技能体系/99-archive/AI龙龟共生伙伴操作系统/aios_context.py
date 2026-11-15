#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI OS 对话上下文获取器
每次回答用户问题前，执行此脚本获取当前 AI OS 的真实状态和数据。

使用方法：
  python aios_context.py        输出当前完整上下文（JSON）
  python aios_context.py --brief 输出精简版上下文（用于快速检查）
  python aios_context.py --goal "新目标"  设置一个新目标
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-os'))
sys.path.insert(0, ROOT)


def get_state() -> dict:
    """获取 AI OS 当前完整状态"""
    state = {"timestamp": __import__('datetime').datetime.now().isoformat()}

    # 1. 持久化状态
    state_path = os.path.expanduser("~/.aios/autonomous_state.json")
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            s = json.load(f)
        state["goals"] = [{"priority": g[0], "description": g[1], "created": g[2]} for g in s.get("goals", [])]
        state["lessons"] = s.get("lessons", [])
        state["cycle_count"] = s.get("cycle_count", 0)
        state["last_updated"] = s.get("updated_at", "")

    # 2. 决策引擎最新诊断
    try:
        from aios.decision.engine import DecisionEngine
        stores = {
            "金月湾": {"revenue_rate": 134.6, "tuna_rate": 132, "beverage_rate": 37.1,
                        "tuna_penetration": 24.3, "beverage_penetration": 32.6,
                        "moments_count": 13, "wechat_add": 0},
            "狮山": {"revenue_rate": 95.0, "tuna_rate": 32.7, "beverage_rate": 17,
                      "tuna_penetration": 7, "beverage_penetration": 0,
                      "moments_count": 33, "wechat_add": 2},
            "松山湖": {"revenue_rate": 110.7, "tuna_rate": 83, "beverage_rate": 524,
                        "tuna_penetration": 12, "beverage_penetration": 22.22,
                        "moments_count": 2, "wechat_add": 1},
        }
        engine = DecisionEngine()
        result = engine.run(stores)
        diag = result["diagnosis"]
        state["diagnosis"] = {
            "summary": diag["summary"],
            "business_issue_count": len(diag["business"]["issues"]),
            "structural_bottleneck_count": len(diag["structure"]["bottlenecks"]),
            "bottleneck_rate": diag["structure"]["bottleneck_rate"],
            "bottleneck_density": diag["structure"]["bottleneck_density"],
            "field_pressure": diag.get("field_pressure", {}),
        }
        state["tickets"] = {"count": len(result["dispatched_tickets"])}
        state["decision"] = {
            "must_do_count": len(result["decision"]["business_decision"]["must_do"]),
            "week_focus_count": len(result["decision"]["business_decision"]["week_focus"]),
            "compression_strategies": len(result["decision"]["bottleneck_compression"]),
        }
        state["maturity"] = {"level": result["maturity"]["level"], "name": result["maturity"]["name"]}
        state["governance"] = {"agents": result["governance"]["agents"]}
    except Exception as e:
        state["diagnosis_error"] = str(e)

    # 3. 审计日志摘要
    audit_path = os.path.expanduser("~/.aios/audit_log.jsonl")
    if os.path.exists(audit_path):
        with open(audit_path, 'r', encoding='utf-8') as f:
            logs = f.readlines()
        state["audit"] = {"total_actions": len(logs)}

    return state


def get_brief() -> dict:
    """获取精简版上下文（用于每次回答前快速检查）"""
    s = get_state()

    # 检查知识库可用状态
    obsidian_path = r"D:\以观其妙书院知识库\以观其妙书院"
    obsidian_available = os.path.exists(obsidian_path)
    skills_path = os.path.expanduser("~/.agents/skills")
    skills_count = len(os.listdir(skills_path)) if os.path.exists(skills_path) else 0

    return {
        "timestamp": s.get("timestamp", ""),
        "goals_count": len(s.get("goals", [])),
        "cycles": s.get("cycle_count", 0),
        "lessons": len(s.get("lessons", [])),
        "field_pressure": s.get("diagnosis", {}).get("field_pressure", {}).get("interpretation", "unknown"),
        "maturity": f"L{s.get('maturity', {}).get('level', '?')}",
        "tickets_pending": s.get("tickets", {}).get("count", 0),
        "must_do": s.get("decision", {}).get("must_do_count", 0),
        "agents": s.get("governance", {}).get("agents", 0),
        # 数据源可用性（供回答时判断用）
        "data_sources": {
            "aios_state": True,  # ~/.aios/ 始终可用
            "obsidian": obsidian_available,
            "skills": skills_count,
        },
    }


def search_knowledge(query: str, max_results: int = 5) -> list:
    """在 Obsidian 知识库中搜索与 query 相关的笔记"""
    obsidian_path = r"D:\以观其妙书院知识库\以观其妙书院"
    results = []

    if not os.path.exists(obsidian_path):
        return [{"error": "Obsidian vault not found"}]

    query_lower = query.lower()
    for root, dirs, files in os.walk(obsidian_path):
        # 跳过隐藏目录和脚本目录
        rel = os.path.relpath(root, obsidian_path)
        if any(part.startswith('.') for part in rel.split(os.sep)):
            continue

        for f in files:
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
                    content = fh.read(3000)  # 只读前3000字符
                if query_lower in content.lower():
                    rel_path = os.path.relpath(filepath, obsidian_path)
                    # 提取匹配段落的上下文
                    idx = content.lower().find(query_lower)
                    start = max(0, idx - 60)
                    end = min(len(content), idx + len(query) + 60)
                    snippet = content[start:end].replace('\n', ' ')
                    results.append({
                        "file": rel_path,
                        "snippet": snippet,
                    })
                    if len(results) >= max_results:
                        return results
            except:
                continue

    return results if results else [{"message": "No matches found"}]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--brief":
        print(json.dumps(get_brief(), ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "--search":
        query = ' '.join(sys.argv[2:])
        results = search_knowledge(query)
        text = json.dumps(results, ensure_ascii=False, indent=2)
        # Remove emoji for GBK terminal compatibility
        text = text.encode('utf-8', errors='replace').decode('utf-8')
        # Replace non-BMP characters
        text = ''.join(c for c in text if ord(c) < 0x10000 or c in '\n\r\t')
        print(text)
    else:
        print(json.dumps(get_state(), ensure_ascii=False, indent=2))
