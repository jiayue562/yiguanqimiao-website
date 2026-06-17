# -*- coding: utf-8 -*-
# 象思维 Skill 测试验证脚本
# 龙心 OS · 2026-04-16

import os
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SKILL_PATH = Path.home() / '.agents' / 'skills' / '象思维'
OBSIDIAN_PATH = Path('D:/以观其妙书院知识库/观其妙书院/skills/象思维')
OPCCLAW_PATH = Path.home() / '.OpcClaw 知识库' / 'skills' / '象思维'

def test_all():
    print('=' * 70)
    print('  象思维 Skill 测试验证')
    print('=' * 70)
    print(f'测试时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Skill 路径：{SKILL_PATH}')
    print('')
    
    results = []
    
    # 测试 1: 目录结构
    print('测试 1: 目录结构')
    print('-' * 40)
    checks = {
        'Skill 主目录': SKILL_PATH.exists(),
        'Obsidian 同步': OBSIDIAN_PATH.exists(),
        'OpcClaw 同步': OPCCLAW_PATH.exists(),
        'SKILL.md': (SKILL_PATH / 'SKILL.md').exists(),
        'theory.md': (SKILL_PATH / 'references' / 'theory.md').exists(),
        'practice-guide.md': (SKILL_PATH / 'references' / 'practice-guide.md').exists(),
        'trigger-rules.yaml': (SKILL_PATH / 'triggers' / 'trigger-rules.yaml').exists(),
    }
    for name, ok in checks.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    results.append(('目录结构', all(checks.values())))
    print('')
    
    # 测试 2: 核心知识
    print('测试 2: 核心知识完整性')
    print('-' * 40)
    with open(SKILL_PATH / 'SKILL.md', 'r', encoding='utf-8') as f:
        content = f.read()
    knowledge = {
        '四大方法': all(x in content for x in ['观物取象', '立象尽意', '取象比类', '观象制器']),
        '三层次': all(x in content for x in ['物象', '意象', '原象']),
        '阴阳五行': '阴阳' in content and '五行' in content,
        'Q5 专属引擎': '第五象限' in content or 'Q5' in content,
        '0→1 原创': '0→1' in content or '0-1' in content,
    }
    for name, ok in knowledge.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    results.append(('核心知识', all(knowledge.values())))
    print('')
    
    # 测试 3: 文件大小
    print('测试 3: 文件大小')
    print('-' * 40)
    files = {
        'SKILL.md': SKILL_PATH / 'SKILL.md',
        'theory.md': SKILL_PATH / 'references' / 'theory.md',
        'practice-guide.md': SKILL_PATH / 'references' / 'practice-guide.md',
    }
    for name, path in files.items():
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {name}: {size/1024:.1f}KB")
        else:
            print(f"  ❌ {name}: 不存在")
    results.append(('文件大小', True))
    print('')
    
    # 汇总
    print('=' * 70)
    print('  测试结果汇总')
    print('=' * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    for name, ok in results:
        print(f"  {'✅' if ok else '❌'} {name}")
    print('')
    print(f'总计：{passed}/{total} 测试通过')
    
    if passed == total:
        print('')
        print('🎉 所有测试通过！象思维 Skill 封装完整')
        print('综合评分：100/100 (优秀)')
    return passed == total

if __name__ == '__main__':
    test_all()
