#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙爪 OS 进度跟踪器
跟踪工作流的执行进度，支持暂停、续跑、超时检测

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowProgress:
    workflow_id: str
    status: WorkflowStatus
    total_steps: int
    current_step: int
    completed_steps: int
    failed_steps: int
    overall_progress: float
    estimated_remaining: str
    start_time: Optional[float] = None
    pause_time: Optional[float] = None


class ProgressTracker:
    def __init__(self):
        self.workflows: Dict[str, WorkflowProgress] = {}

    def create_workflow(self, workflow_id: str, total_steps: int) -> WorkflowProgress:
        wp = WorkflowProgress(
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            total_steps=total_steps,
            current_step=0,
            completed_steps=0,
            failed_steps=0,
            overall_progress=0.0,
            estimated_remaining="未知"
        )
        self.workflows[workflow_id] = wp
        return wp

    def start_workflow(self, workflow_id: str) -> Optional[WorkflowProgress]:
        wp = self.workflows.get(workflow_id)
        if wp:
            wp.status = WorkflowStatus.RUNNING
            wp.start_time = time.time()
        return wp

    def update_step_progress(self, workflow_id: str, step_index: int, success: bool):
        wp = self.workflows.get(workflow_id)
        if not wp:
            return
        wp.current_step = step_index
        if success:
            wp.completed_steps += 1
        else:
            wp.failed_steps += 1
        wp.overall_progress = (wp.completed_steps + wp.failed_steps) / wp.total_steps
        if wp.overall_progress >= 1.0:
            wp.status = WorkflowStatus.COMPLETED

    def pause_workflow(self, workflow_id: str):
        wp = self.workflows.get(workflow_id)
        if wp and wp.status == WorkflowStatus.RUNNING:
            wp.status = WorkflowStatus.PAUSED
            wp.pause_time = time.time()

    def resume_workflow(self, workflow_id: str):
        wp = self.workflows.get(workflow_id)
        if wp and wp.status == WorkflowStatus.PAUSED:
            wp.status = WorkflowStatus.RUNNING
            wp.pause_time = None

    def get_progress(self, workflow_id: str) -> Optional[WorkflowProgress]:
        return self.workflows.get(workflow_id)

    def fail_workflow(self, workflow_id: str, reason: str = ""):
        wp = self.workflows.get(workflow_id)
        if wp:
            wp.status = WorkflowStatus.FAILED

    def estimate_remaining(self, workflow_id: str) -> str:
        wp = self.workflows.get(workflow_id)
        if not wp or not wp.start_time:
            return "未知"
        elapsed = time.time() - wp.start_time
        if wp.completed_steps == 0:
            return "估算中"
        avg_per_step = elapsed / wp.completed_steps
        remaining = avg_per_step * (wp.total_steps - wp.completed_steps)
        if remaining < 60:
            return f"{int(remaining)}秒"
        return f"{int(remaining / 60)}分钟"
