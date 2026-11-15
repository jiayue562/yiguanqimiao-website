#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI OS 调度器封装 - 供 opencode skill 调用"""
import sys
import os
import json

# 添加项目根到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-os'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def init_scheduler():
    """初始化调度器"""
    from aios.scheduler.scheduler_main import SchedulerSession
    session = SchedulerSession(user_id='悟空')
    sid = session.create_session('悟空')
    return session, sid


def process_text(session, sid, user_input: str) -> dict:
    """处理自然语言请求，返回结构化结果"""
    result = session.process_request(sid, user_input)
    return {
        'intent': result['intent']['type'],
        'scene': result['scene']['type'],
        'engine': result['decision']['main_engine'],
        'skill_count': result['skill_execution']['skill_count'],
        'skills': result['skill_execution']['skills'],
        'response': result['decision']['declaration_text'],
    }


def cli():
    """CLI入口"""
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请输入请求文本'}))
        sys.exit(1)
    user_input = sys.argv[1]
    session, sid = init_scheduler()
    output = process_text(session, sid, user_input)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    cli()
