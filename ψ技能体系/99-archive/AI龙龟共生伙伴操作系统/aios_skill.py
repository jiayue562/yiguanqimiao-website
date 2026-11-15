#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI OS opencode skill 入口
opencode 通过此脚本调用 AI OS 调度引擎
"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-os')))

def handle_request(request: str) -> dict:
    from aios.scheduler.scheduler_main import SchedulerSession
    session = SchedulerSession(user_id='悟空')
    sid = session.create_session('悟空')
    result = session.process_request(sid, request)
    return {
        'session': result['session_id'],
        'intent': result['intent']['type'],
        'scene': result['scene']['type'],
        'engine': result['decision']['main_engine'],
        'skills': result['skill_execution']['skills'],
        'response': result['decision']['declaration_text'],
    }

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print(json.dumps({
            'name': 'AI OS 调度引擎',
            'description': '基于龙心OS的意图识别、场景分类、引擎路由调度系统',
            'usage': 'python aios_skill.py <自然语言请求>',
            'example': 'python aios_skill.py 我想学习Python编程',
        }, ensure_ascii=False))
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请输入请求文本'}, ensure_ascii=False))
        sys.exit(1)
    
    output = handle_request(' '.join(sys.argv[1:]))
    print(json.dumps(output, ensure_ascii=False))
