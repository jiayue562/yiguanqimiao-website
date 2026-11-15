# -*- coding: utf-8 -*-
# Prompt 上下文 A/B 测试

from datetime import datetime


class ABTest:
    def __init__(self):
        self.results = []

    def run(self, prompt, strategy_a, strategy_b, context_items, judge_fn=None):
        prompt_a = strategy_a(prompt, context_items)
        prompt_b = strategy_b(prompt, context_items)
        score_a = judge_fn(prompt_a) if judge_fn else len(prompt_a)
        score_b = judge_fn(prompt_b) if judge_fn else len(prompt_b)
        result = {
            "timestamp": datetime.now().isoformat(),
            "strategy_a": score_a,
            "strategy_b": score_b,
            "winner": "A" if score_a >= score_b else "B",
            "diff": abs(score_a - score_b)
        }
        self.results.append(result)
        return result

    def summary(self):
        if not self.results:
            return {"total": 0, "a_wins": 0, "b_wins": 0}
        a_wins = sum(1 for r in self.results if r["winner"] == "A")
        return {
            "total": len(self.results),
            "a_wins": a_wins,
            "b_wins": len(self.results) - a_wins,
            "a_win_rate": round(a_wins / len(self.results), 2)
        }
