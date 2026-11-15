# -*- coding: utf-8 -*-
# 跨 Skills 依赖追踪器

from datetime import datetime
from collections import defaultdict


class DependencyTracker:
    def __init__(self):
        self._chains = defaultdict(list)

    def record_call(self, chain_id, source, target):
        self._chains[chain_id].append({
            "source": source,
            "target": target,
            "timestamp": datetime.now().isoformat()
        })

    def get_chain(self, chain_id):
        return self._chains.get(chain_id, [])

    def detect_cycles(self):
        graph = defaultdict(set)
        for chain in self._chains.values():
            for call in chain:
                graph[call["source"]].add(call["target"])
        cycles = []
        visited = set()

        def dfs(node, path):
            if node in path:
                idx = path.index(node)
                cycles.append(path[idx:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            for nb in graph.get(node, []):
                dfs(nb, path + [node])

        for node in graph:
            dfs(node, [])
        return cycles

    def chain_depth(self, chain_id):
        return len(self._chains.get(chain_id, []))
