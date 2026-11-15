# -*- coding: utf-8 -*-
# Prompt 上下文注入器

from typing import List, Dict, Optional


def inject(prompt, context_items, template=None, position="prefix"):
    if not context_items:
        return prompt
    ctx_lines = []
    for item in context_items:
        key = item.get("key", "")
        val = item.get("value", "")
        ctx_lines.append("--- %s ---\n%s" % (key, val))
    ctx_text = "\n\n".join(ctx_lines)
    if template:
        result = template.replace("{context}", ctx_text)
        result = result.replace("{prompt}", prompt)
        return result
    if position == "prefix":
        return "【上下文信息】\n%s\n\n【当前问题】\n%s" % (ctx_text, prompt)
    elif position == "suffix":
        return "%s\n\n【上下文信息】\n%s" % (prompt, ctx_text)
    elif position.startswith("replace:"):
        k = position.split(":", 1)[1]
        return prompt.replace("{%s}" % k, ctx_text)
    return prompt


def validate_injection(original, injected, max_ratio=0.5):
    if not original:
        return True
    ratio = (len(injected) - len(original)) / len(injected)
    return ratio <= max_ratio
