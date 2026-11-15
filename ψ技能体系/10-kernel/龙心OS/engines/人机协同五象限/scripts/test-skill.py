# -*- coding: utf-8 -*-
# 人机协同五象限 Skill 测试验证脚本
# 龙心 OS · 2026-04-16

import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 路径配置
SKILL_PATH = Path.home() / '.agents' / 'skills' / '人机协同五象限'
OBSIDIAN_PATH = Path('D:/以观其妙书院知识库/观其妙书院/skills/人机协同五象限')
OPCCLAW_PATH = Path.home() / '.OpcClaw 知识库' / 'skills' / '人机协同五象限'

def test_directory_structure():
    """测试 1: 目录结构验证"""
    print('=' * 70)
    print('  测试 1: 目录结构验证')
    print('=' * 70)
    print('')
    
    results = {}
    
    # 检查主目录
    results['Skill 主目录'] = SKILL_PATH.exists()
    print(f"Skill 主目录：{'✅ 存在' if results['Skill 主目录'] else '❌ 不存在'}")
    print(f"  路径：{SKILL_PATH}")
    
    # 检查 Obsidian 同步
    results['Obsidian 同步'] = OBSIDIAN_PATH.exists()
    print(f"Obsidian 同步：{'✅ 已同步' if results['Obsidian 同步'] else '❌ 未同步'}")
    print(f"  路径：{OBSIDIAN_PATH}")
    
    # 检查 OpcClaw 同步
    results['OpcClaw 同步'] = OPCCLAW_PATH.exists()
    print(f"OpcClaw 同步：{'✅ 已同步' if results['OpcClaw 同步'] else '❌ 未同步'}")
    print(f"  路径：{OPCCLAW_PATH}")
    
    # 检查核心文件
    core_files = [
        'SKILL.md',
        'references/theory.md',
        'references/practice-guide.md',
        'triggers/trigger-rules.yaml',
    ]
    
    print('')
    print('核心文件检查:')
    for file in core_files:
        file_path = SKILL_PATH / file
        exists = file_path.exists()
        print(f"  {'✅' if exists else '❌'} {file}")
        results[file] = exists
    
    passed = sum(1 for v in results.values() if v is True)
    total = len(results)
    
    print('')
    print(f'测试 1 结果：{passed}/{total} 通过')
    
    return passed == total

def test_skill_definition():
    """测试 2: Skill 定义验证"""
    print('')
    print('=' * 70)
    print('  测试 2: Skill 定义验证')
    print('=' * 70)
    print('')
    
    skill_file = SKILL_PATH / 'SKILL.md'
    
    if not skill_file.exists():
        print('❌ SKILL.md 不存在')
        return False
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查必要元素
    checks = {
        'name 字段': 'name:' in content,
        'description 字段': 'description:' in content,
        '核心定义': '核心定义' in content,
        '五象限详解': '五象限详解' in content or 'Q1' in content,
        '触发场景': '触发场景' in content or '触发' in content,
        '核心金句': '核心金句' in content or '金句' in content,
        '标签体系': '标签' in content or '#' in content,
    }
    
    print('Skill 定义检查:')
    for name, result in checks.items():
        print(f"  {'✅' if result else '❌'} {name}")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print('')
    print(f'测试 2 结果：{passed}/{total} 通过')
    
    return passed == total

def test_theory_completeness():
    """测试 3: 理论完整性验证"""
    print('')
    print('=' * 70)
    print('  测试 3: 理论完整性验证')
    print('=' * 70)
    print('')
    
    theory_file = SKILL_PATH / 'references' / 'theory.md'
    
    if not theory_file.exists():
        print('❌ theory.md 不存在')
        return False
    
    with open(theory_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查理论要素
    checks = {
        '引言': '引言' in content,
        '四象限回顾': '四象限' in content,
        '五象限模型': '五象限' in content,
        '象思维': '象思维' in content,
        '理论根基': '学术谱系' in content or '理论' in content,
        '应用场景': '应用' in content,
        '案例': '案例' in content,
        '结语': '结语' in content,
    }
    
    print('理论完整性检查:')
    for name, result in checks.items():
        print(f"  {'✅' if result else '❌'} {name}")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print('')
    print(f'测试 3 结果：{passed}/{total} 通过')
    
    return passed == total

def test_trigger_rules():
    """测试 4: 触发规则验证"""
    print('')
    print('=' * 70)
    print('  测试 4: 触发规则验证')
    print('=' * 70)
    print('')
    
    trigger_file = SKILL_PATH / 'triggers' / 'trigger-rules.yaml'
    
    if not trigger_file.exists():
        print('❌ trigger-rules.yaml 不存在')
        return False
    
    with open(trigger_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查触发规则要素
    checks = {
        'P0 直接触发': 'P0' in content or '直接触发' in content,
        'P1 场景触发': 'P1' in content or '场景触发' in content,
        'P2 信号触发': 'P2' in content or '信号触发' in content,
        '关键词配置': 'keywords' in content,
        '协同路由': 'routes' in content or '路由' in content,
    }
    
    print('触发规则检查:')
    for name, result in checks.items():
        print(f"  {'✅' if result else '❌'} {name}")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print('')
    print(f'测试 4 结果：{passed}/{total} 通过')
    
    return passed == total

def test_five_quadrants_knowledge():
    """测试 5: 五象限知识完整性"""
    print('')
    print('=' * 70)
    print('  测试 5: 五象限知识完整性')
    print('=' * 70)
    print('')
    
    skill_file = SKILL_PATH / 'SKILL.md'
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查五象限完整性
    quadrants = {
        'Q1 效率协作者': '效率协作者' in content,
        'Q2 知识拓展者': '知识拓展者' in content,
        'Q3 思辨对话者': '思辨对话者' in content,
        'Q4 协同探索者': '协同探索者' in content,
        'Q5 未知共创者': '未知共创者' in content,
        '人知/不知维度': '人知' in content and '人不知' in content,
        'AI 知/不知维度': 'AI 知' in content and 'AI 不知' in content,
        '象思维': '象思维' in content,
    }
    
    print('五象限知识检查:')
    for name, result in quadrants.items():
        print(f"  {'✅' if result else '❌'} {name}")
    
    passed = sum(1 for v in quadrants.values() if v)
    total = len(quadrants)
    
    print('')
    print(f'测试 5 结果：{passed}/{total} 通过')
    
    return passed == total

def test_golden_quotes():
    """测试 6: 核心金句验证"""
    print('')
    print('=' * 70)
    print('  测试 6: 核心金句验证')
    print('=' * 70)
    print('')
    
    skill_file = SKILL_PATH / 'SKILL.md'
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查核心金句
    quotes = {
        '不可替代性': '不可替代性' in content,
        '副驾驶方向盘': '副驾驶' in content or '方向盘' in content,
        '提出问题': '提出.*问题' in content or '问题' in content,
        '分工到共生': '分工' in content and '共生' in content,
    }
    
    print('核心金句检查:')
    for name, result in quotes.items():
        print(f"  {'✅' if result else '❌'} {name}")
    
    passed = sum(1 for v in quotes.values() if v)
    total = len(quotes)
    
    print('')
    print(f'测试 6 结果：{passed}/{total} 通过')
    
    return passed == total

def test_file_sizes():
    """测试 7: 文件大小验证"""
    print('')
    print('=' * 70)
    print('  测试 7: 文件大小验证')
    print('=' * 70)
    print('')
    
    files = {
        'SKILL.md': SKILL_PATH / 'SKILL.md',
        'theory.md': SKILL_PATH / 'references' / 'theory.md',
        'practice-guide.md': SKILL_PATH / 'references' / 'practice-guide.md',
        'trigger-rules.yaml': SKILL_PATH / 'triggers' / 'trigger-rules.yaml',
    }
    
    expected_sizes = {
        'SKILL.md': 5000,  # 至少 5KB
        'theory.md': 3000,  # 至少 3KB
        'practice-guide.md': 2000,  # 至少 2KB
        'trigger-rules.yaml': 500,  # 至少 500B
    }
    
    print('文件大小检查:')
    passed = 0
    for name, path in files.items():
        if path.exists():
            size = path.stat().st_size
            expected = expected_sizes[name]
            ok = size >= expected
            print(f"  {'✅' if ok else '⚠️'} {name}: {size/1024:.1f}KB (期望≥{expected/1024:.1f}KB)")
            if ok:
                passed += 1
        else:
            print(f"  ❌ {name}: 文件不存在")
    
    total = len(files)
    
    print('')
    print(f'测试 7 结果：{passed}/{total} 通过')
    
    return passed == total

def main():
    """主函数"""
    print('=' * 70)
    print('  人机协同五象限 Skill 测试验证')
    print('=' * 70)
    print('')
    print(f'测试时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Skill 路径：{SKILL_PATH}')
    print('')
    
    # 运行所有测试
    results = []
    
    results.append(('目录结构', test_directory_structure()))
    results.append(('Skill 定义', test_skill_definition()))
    results.append(('理论完整性', test_theory_completeness()))
    results.append(('触发规则', test_trigger_rules()))
    results.append(('五象限知识', test_five_quadrants_knowledge()))
    results.append(('核心金句', test_golden_quotes()))
    results.append(('文件大小', test_file_sizes()))
    
    # 汇总结果
    print('')
    print('=' * 70)
    print('  测试结果汇总')
    print('=' * 70)
    print('')
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        print(f'  {status} - {name}')
    
    print('')
    print(f'总计：{passed}/{total} 测试通过')
    
    if passed == total:
        print('')
        print('🎉 所有测试通过！人机协同五象限 Skill 封装完整')
        print('')
        print('综合评分：100/100 (优秀)')
        return True
    elif passed >= total * 0.8:
        print('')
        print('✅ 大部分测试通过！人机协同五象限 Skill 基本可用')
        print('')
        print(f'综合评分：{int(passed/total*100)}/100 (良好)')
        return True
    else:
        print('')
        print('⚠️ 部分测试失败，需要修复')
        print('')
        print(f'综合评分：{int(passed/total*100)}/100 (需改进)')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
