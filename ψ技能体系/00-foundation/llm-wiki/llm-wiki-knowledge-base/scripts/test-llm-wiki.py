# -*- coding: utf-8 -*-
# LLM Wiki 知识库完整功能测试脚本
# 龙心 OS · 2026-04-16

import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 路径配置
OPCCLAW_KB = Path.home() / '.OpcClaw 知识库' / 'knowledge-base'
LLM_WIKI_SKILL = Path.home() / '.agents' / 'skills' / 'llm-wiki-knowledge-base'

def test_directory_structure():
    """测试 1: 目录结构验证"""
    print('=' * 70)
    print('  测试 1: LLM Wiki 目录结构验证')
    print('=' * 70)
    print('')
    
    results = {}
    
    # 检查知识库目录
    results['知识库目录'] = OPCCLAW_KB.exists()
    print(f"知识库目录：{'✅ 存在' if results['知识库目录'] else '❌ 不存在'}")
    print(f"  路径：{OPCCLAW_KB}")
    
    # 检查 Skill 目录
    results['Skill 目录'] = LLM_WIKI_SKILL.exists()
    print(f"Skill 目录：{'✅ 存在' if results['Skill 目录'] else '❌ 不存在'}")
    print(f"  路径：{LLM_WIKI_SKILL}")
    
    # 检查核心文件
    core_files = [
        'SKILL.md',
        'compiler/ingest.py',
        'compiler/query.py',
        'compiler/lint.py',
        'scripts/health-check.py',
        'scripts/rebuild-index.py',
        'templates/entity-template.md',
        'templates/concept-template.md',
        'templates/comparison-template.md',
        'architecture/layer3-schema/structure.md',
        'architecture/layer3-schema/quality-rules.md',
        'architecture/layer3-schema/triggers.md',
        'reference/theory.md',
        'reference/sop.md',
        'triggers/trigger-rules.yaml',
        'triggers/skill-routes.yaml',
    ]
    
    print('')
    print('核心文件检查:')
    for file in core_files:
        file_path = LLM_WIKI_SKILL / file
        exists = file_path.exists()
        print(f"  {'✅' if exists else '❌'} {file}")
        results[file] = exists
    
    # 统计知识库文件
    if OPCCLAW_KB.exists():
        md_files = list(OPCCLAW_KB.glob('*.md'))
        print('')
        print(f'知识库文件数：{len(md_files)} 个')
        results['文件数'] = len(md_files)
    
    passed = sum(1 for v in results.values() if v is True)
    total = len(results)
    
    print('')
    print(f'测试 1 结果：{passed}/{total} 通过')
    
    return passed == total

def test_knowledge_files():
    """测试 2: 知识文件内容验证"""
    print('')
    print('=' * 70)
    print('  测试 2: 知识文件内容验证')
    print('=' * 70)
    print('')
    
    if not OPCCLAW_KB.exists():
        print('❌ 知识库目录不存在')
        return False
    
    md_files = list(OPCCLAW_KB.glob('*.md'))
    
    if not md_files:
        print('⚠️ 知识库为空')
        return False
    
    print(f'发现 {len(md_files)} 个知识文件:')
    print('')
    
    valid_count = 0
    for file in md_files[:10]:  # 只显示前 10 个
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 检查是否有基本结构
                has_title = content.startswith('#')
                has_content = len(content) > 100
                
                status = '✅' if (has_title and has_content) else '⚠️'
                print(f'{status} {file.name}')
                
                if has_title and has_content:
                    valid_count += 1
        except Exception as e:
            print(f'❌ {file.name} (读取失败：{e})')
    
    print('')
    print(f'有效文件数：{valid_count}/{min(len(md_files), 10)}')
    
    return valid_count > 0

def test_compiler_scripts():
    """测试 3: 编译器脚本验证"""
    print('')
    print('=' * 70)
    print('  测试 3: 编译器脚本验证')
    print('=' * 70)
    print('')
    
    scripts = [
        ('ingest.py', '知识编译'),
        ('lint.py', '健康检查'),
        ('health-check.py', '健康检查脚本'),
        ('rebuild-index.py', '重建索引'),
    ]
    
    results = {}
    
    for script, desc in scripts:
        script_path = LLM_WIKI_SKILL / 'compiler' / script if 'ingest' in script or 'lint' in script else LLM_WIKI_SKILL / 'scripts' / script
        
        if script_path.exists():
            print(f'✅ {desc} ({script})')
            
            # 检查脚本是否可执行
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    has_main = 'if __name__' in content or 'def main' in content
                    print(f'   结构：{"✅ 完整" if has_main else "⚠️ 缺少主函数"}')
                    results[script] = has_main
            except:
                print(f'   读取：❌ 失败')
                results[script] = False
        else:
            print(f'❌ {desc} ({script}) - 文件不存在')
            results[script] = False
    
    print('')
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f'测试 3 结果：{passed}/{total} 通过')
    
    return passed == total

def test_templates():
    """测试 4: 模板文件验证"""
    print('')
    print('=' * 70)
    print('  测试 4: 模板文件验证')
    print('=' * 70)
    print('')
    
    templates_dir = LLM_WIKI_SKILL / 'templates'
    
    if not templates_dir.exists():
        print('❌ 模板目录不存在')
        return False
    
    templates = list(templates_dir.glob('*.md'))
    
    print(f'发现 {len(templates)} 个模板文件:')
    print('')
    
    for tpl in templates:
        try:
            with open(tpl, 'r', encoding='utf-8') as f:
                content = f.read()
                has_structure = '#' in content
                print(f"{'✅' if has_structure else '⚠️'} {tpl.name}")
        except:
            print(f'❌ {tpl.name} (读取失败)')
    
    print('')
    print(f'模板状态：{"✅ 可用" if len(templates) > 0 else "❌ 缺失"}')
    
    return len(templates) > 0

def test_health_check():
    """测试 5: 运行健康检查（直接调用 lint 模块）"""
    print('')
    print('=' * 70)
    print('  测试 5: 运行健康检查')
    print('=' * 70)
    print('')
    
    lint_path = LLM_WIKI_SKILL / 'compiler' / 'lint.py'
    if not lint_path.exists():
        print('❌ lint.py 不存在')
        return False
    
    print('直接调用 compiler/lint.py...')
    print('')
    
    try:
        sys.path.insert(0, str(LLM_WIKI_SKILL / 'compiler'))
        import importlib.util
        spec = importlib.util.spec_from_file_location("lint", lint_path)
        lint = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lint)
        
        report = lint.check_wiki_health()
        if report:
            score = report.get('health_score', 0)
            print(f'健康分数：{score}/100')
            status = '✅ 通过' if score >= 60 else '⚠️ 需关注'
            print(f'健康检查：{status}')
        
        return True
    except Exception as e:
        print(f'❌ 执行失败：{e}')
        import traceback
        traceback.print_exc()
        return False

def test_three_layer_architecture():
    """测试 6: 三层架构验证"""
    print('')
    print('=' * 70)
    print('  测试 6: 三层架构验证')
    print('=' * 70)
    print('')
    
    layers = {
        '原始资料层': OPCCLAW_KB,
        'Wiki 本体层': OPCCLAW_KB,  # MEMORY.md 等
        'Schema 配置层': LLM_WIKI_SKILL / 'architecture' / 'layer3-schema',
    }
    
    print('三层架构检查:')
    print('')
    
    for name, path in layers.items():
        exists = path.exists()
        print(f"{'✅' if exists else '❌'} {name}")
        print(f"   路径：{path}")
        
        if exists:
            if path.is_dir():
                files = list(path.glob('*.md')) if path.exists() else []
                print(f"   文件：{len(files)} 个")
            else:
                print(f"   类型：文件")
        print('')
    
    # 检查 Schema 层规范文档
    schema_doc = LLM_WIKI_SKILL / 'architecture' / 'layer3-schema' / 'structure.md'
    if schema_doc.exists():
        print('✅ Schema 配置规范文档存在')
        return True
    else:
        print('⚠️ Schema 配置规范文档缺失')
        return False

def main():
    """主函数"""
    print('=' * 70)
    print('  LLM Wiki 知识库完整功能测试')
    print('=' * 70)
    print('')
    print(f'测试时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'知识库路径：{OPCCLAW_KB}')
    print(f'Skill 路径：{LLM_WIKI_SKILL}')
    print('')
    
    # 运行所有测试
    results = []
    
    results.append(('目录结构', test_directory_structure()))
    results.append(('知识文件', test_knowledge_files()))
    results.append(('编译器脚本', test_compiler_scripts()))
    results.append(('模板文件', test_templates()))
    results.append(('健康检查', test_health_check()))
    results.append(('三层架构', test_three_layer_architecture()))
    
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
        print('🎉 所有测试通过！LLM Wiki 知识库功能正常')
        print('')
        print('综合评分：100/100 (优秀)')
        return True
    elif passed >= total * 0.8:
        print('')
        print('✅ 大部分测试通过！LLM Wiki 知识库基本可用')
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
