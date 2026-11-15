#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
上下文管理器 — 多轮对话记忆 + 人在回路中的人工确认节点
实现龙心OS的会话级别上下文管理

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import json


class ConfirmLevel(Enum):
    AUTO = "auto"
    NOTIFY = "notify"
    CONFIRM = "confirm"
    APPROVE = "approve"


@dataclass
class ConversationTurn:
    turn_id: int
    query: str
    task_type: str
    task_level: str
    engines_activated: List[str]
    result_summary: str
    timestamp: float
    human_confirmed: bool = True


@dataclass
class SessionState:
    session_id: str
    turns: List[ConversationTurn] = field(default_factory=list)
    current_context: Dict[str, Any] = field(default_factory=dict)
    human_preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)


class ContextManager:
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

        self.confirm_rules = {
            "JY": ConfirmLevel.AUTO,
            "ZL": ConfirmLevel.APPROVE,
            "FA": ConfirmLevel.NOTIFY,
            "WD": ConfirmLevel.AUTO,
            "GT": ConfirmLevel.NOTIFY,
            "XX": ConfirmLevel.AUTO,
            "CZ": ConfirmLevel.NOTIFY,
            "CY": ConfirmLevel.NOTIFY,
        }

    def create_session(self, session_id: str) -> SessionState:
        self.sessions[session_id] = SessionState(session_id=session_id)
        return self.sessions[session_id]

    def get_session(self, session_id: str) -> Optional[SessionState]:
        return self.sessions.get(session_id)

    def add_turn(self, session_id: str, query: str, task_type: str,
                 task_level: str, engines: List[str], summary: str) -> ConversationTurn:
        session = self.sessions.get(session_id)
        if not session:
            session = self.create_session(session_id)

        turn = ConversationTurn(
            turn_id=len(session.turns) + 1,
            query=query,
            task_type=task_type,
            task_level=task_level,
            engines_activated=engines,
            result_summary=summary,
            timestamp=time.time(),
        )

        confirm_level = self.confirm_rules.get(task_type, ConfirmLevel.AUTO)
        if confirm_level == ConfirmLevel.APPROVE:
            turn.human_confirmed = False

        session.turns.append(turn)
        session.last_activity = time.time()
        return turn

    def confirm_turn(self, session_id: str, turn_id: int) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        for turn in session.turns:
            if turn.turn_id == turn_id:
                turn.human_confirmed = True
                return True
        return False

    def get_turn_history(self, session_id: str, last_n: int = 5) -> List[ConversationTurn]:
        session = self.sessions.get(session_id)
        if not session:
            return []
        return session.turns[-last_n:]

    def get_confirm_request(self, session_id: str, turn: ConversationTurn) -> Optional[Dict]:
        confirm_level = self.confirm_rules.get(turn.task_type, ConfirmLevel.AUTO)
        if confirm_level == ConfirmLevel.AUTO:
            return None

        message = f"【需要确认】任务类型: {turn.task_type}\n描述: {turn.query[:50]}...\n将激活: {', '.join(turn.engines_activated)}"

        if confirm_level == ConfirmLevel.APPROVE:
            message += "\n这是一个重大决策，请确认是否继续。"
            buttons = ["确认执行", "修改方案", "取消"]
        elif confirm_level == ConfirmLevel.CONFIRM:
            buttons = ["确认继续", "稍后决定"]
        else:
            buttons = ["知道了"]

        return {
            "session_id": session_id,
            "turn_id": turn.turn_id,
            "level": confirm_level.value,
            "message": message,
            "buttons": buttons,
        }

    def needs_human_confirm(self, task_type: str) -> bool:
        return self.confirm_rules.get(task_type, ConfirmLevel.AUTO) in [
            ConfirmLevel.CONFIRM, ConfirmLevel.APPROVE
        ]

    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        session = self.sessions.get(session_id)
        if not session:
            return None
        return {
            "session_id": session_id,
            "total_turns": len(session.turns),
            "duration_minutes": round((time.time() - session.created_at) / 60, 1),
            "last_activity_seconds_ago": round(time.time() - session.last_activity),
            "recent_tasks": [{"turn": t.turn_id, "type": t.task_type, "query": t.query[:30]}
                             for t in session.turns[-5:]],
        }

    def set_preference(self, session_id: str, key: str, value: Any):
        session = self.sessions.get(session_id)
        if session:
            session.human_preferences[key] = value


def demo():
    cm = ContextManager()
    session_id = "demo_001"

    turn1 = cm.add_turn(session_id, "为什么这个月毛利下降了？", "JY", "standard",
                        ["知识学习", "五色光"], "根因定位完成")
    print(f"Turn 1: {turn1.turn_id}, 需要确认: {not turn1.human_confirmed}")

    turn2 = cm.add_turn(session_id, "该不该开新店？", "ZL", "deep",
                        ["象思维", "五色光", "人机协同", "知识学习", "知行合一"],
                        "决策分析完成")
    confirm = cm.get_confirm_request(session_id, turn2)
    print(f"Turn 2: 需要人工确认: {confirm is not None}")
    if confirm:
        print(f"  确认信息: {confirm['message'][:50]}...")

    summary = cm.get_session_summary(session_id)
    print(f"会话摘要: {summary['total_turns']}轮, {summary['duration_minutes']}分钟")

if __name__ == "__main__":
    demo()
