#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙爪 OS 步骤执行器
根据工作流步骤定义，调用龙脑OS获取推荐模型，执行并返回结果

版本：v1.0
创建：2026-07-28
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import time


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class StepDefinition:
    step_id: int
    name: str
    description: str
    recommended_models: List[str]
    input: Dict[str, Any]
    timeout_seconds: int = 300


class StepResult:
    def __init__(self, step_id: int, name: str):
        self.step_id = step_id
        self.name = name
        self.status = StepStatus.PENDING
        self.output: Optional[str] = None
        self.models_used: List[str] = []
        self.duration_seconds: float = 0.0
        self.error: Optional[str] = None


class StepExecutor:
    def __init__(self, brain_os_available: bool = True):
        self.brain_os_available = brain_os_available

    def query_brain_os(self, step: StepDefinition) -> List[str]:
        """模拟查询龙脑OS获取推荐模型（按接口契约 GET_STEP_MODELS）"""
        if not self.brain_os_available:
            return []
        return step.recommended_models

    def execute_step(self, step: StepDefinition, brain_os_available: bool = True) -> StepResult:
        result = StepResult(step.step_id, step.name)
        start_time = time.time()

        self.brain_os_available = brain_os_available

        models_to_use = self.query_brain_os(step)
        if not models_to_use:
            models_to_use = ["五层分析法"]
            result.models_used = models_to_use
        else:
            result.models_used = models_to_use

        try:
            result.status = StepStatus.COMPLETED
            result.output = f"步骤{step.step_id}执行完成"
        except Exception as e:
            result.status = StepStatus.FAILED
            result.error = str(e)

        result.duration_seconds = time.time() - start_time
        return result
