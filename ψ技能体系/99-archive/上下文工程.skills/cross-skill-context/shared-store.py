# -*- coding: utf-8 -*-
# 跨 Skills 共享上下文存储

import json
from datetime import datetime
from pathlib import Path


class SharedStore:
    def __init__(self, persist_dir=None):
        self._memory = {}
        self._persist_dir = persist_dir

    def set(self, namespace, data, ttl_seconds=300):
        entry = {
            "data": data,
            "created_at": datetime.now().isoformat(),
            "expires_at": datetime.now().timestamp() + ttl_seconds
        }
        self._memory[namespace] = entry
        if self._persist_dir:
            path = Path(self._persist_dir) / ("%s.json" % namespace)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(entry, ensure_ascii=False), encoding="utf-8")

    def get(self, namespace):
        entry = self._memory.get(namespace)
        if not entry:
            return None
        if datetime.now().timestamp() > entry["expires_at"]:
            del self._memory[namespace]
            return None
        return entry["data"]

    def delete(self, namespace):
        self._memory.pop(namespace, None)

    def clear_expired(self):
        now = datetime.now().timestamp()
        expired = [k for k, v in self._memory.items() if now > v["expires_at"]]
        for k in expired:
            del self._memory[k]
        return len(expired)
