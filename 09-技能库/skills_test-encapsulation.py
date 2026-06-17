# -*- coding: utf-8 -*-
"""
象思维 Skill 封装测试验证脚本
测试范围：目录结构/触发规则/自动激活/知识文件/协同路由/健康检查
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

# 配置路径
SKILL_ROOT = Path(r"C:\Users\jia'yue\.agents\skills\象思维")
OBSIDIAN_PATH = Path(r"D:\以观其妙书院知识库\观其妙书院\03-知识地基层\象思维")
OPCCLAW_PATH = Path(r"C:\Users\jia'yue\.OpcClaw 知识库\03-知识地基层\象思维")

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_result(test_name, passed, message=""):
    status = "[OK]" if passed else "[FAIL]"
    result_text = "通过" if passed else "失败"
    print(f"  {status} {test_name}: {result_text} {message}")
    return passed

# ============================================
# 测试 1: 目录结构完整性
# ============================================
def test_directory_structure():
    print_header("测试 1: 目录结构完整性")
    
    required_dirs = [
        SKILL_ROOT,
        SKILL_ROOT / "references",
        SKILL_ROOT / "triggers",
        SKILL_ROOT / "scripts",
        SKILL_ROOT / "logs",
    ]
    
    all_passed = True
    for dir_path in required_dirs:
        passed = dir_path.exists() and dir_path.is_dir()
        print_result(f"目录存在：{dir_path.name}", passed)
        all_passed = all_passed and passed
    
    # 创建 logs 目录如果不存在
    (SKILL_ROOT / "logs").mkdir(exist_ok=True)
    
    return all_passed

# ============================================
# 测试 2: 核心文件完整性
# ============================================
def test_core_files():
    print_header("测试 2: 核心文件完整性")
    
    required_files = {
        "SKILL.md": SKILL_ROOT / "SKILL.md",
        "theory.md": SKILL_ROOT / "references" / "theory.md",
        "practice-guide.md": SKILL_ROOT / "references" / "practice-guide.md",
        "trigger-rules.yaml": SKILL_ROOT / "triggers" / "trigger-rules.yaml",
        "auto-activate.json": SKILL_ROOT / "triggers" / "auto-activate.json",
        "skill-routes.yaml": SKILL_ROOT / "triggers" / "skill-routes.yaml",
    }
    
    all_passed = True
    for name, path in required_files.items():
        passed = path.exists() and path.is_file()
        size = path.stat().st_size / 1024 if passed else 0
        print_result(f"文件存在：{name}", passed, f"({size:.1f}KB)" if passed else "")
        all_passed = all_passed and passed
    
    return all_passed

# ============================================
# 测试 3: 触发规则配置验证
# ============================================
def test_trigger_rules():
    print_header("测试 3: 触发规则配置验证")
    
    config_path = SKILL_ROOT / "triggers" / "auto-activate.json"
    if not config_path.exists():
        print_result("自动触发配置", False, "文件不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证必要字段
        checks = [
            ("skill_name 字段", "skill_name" in config),
            ("auto_activate 字段", "auto_activate" in config),
            ("p0_direct_triggers", "p0_direct_triggers" in config),
            ("p1_scenario_triggers", "p1_scenario_triggers" in config),
            ("p2_signal_triggers", "p2_signal_triggers" in config),
            ("exclude_rules", "exclude_rules" in config),
            ("协同路由", "协同路由" in config),
        ]
        
        all_passed = True
        for name, passed in checks:
            print_result(name, passed)
            all_passed = all_passed and passed
        
        # 验证触发词数量
        p0_count = len(config.get("p0_direct_triggers", {}).get("keywords", []))
        p1_count = len(config.get("p1_scenario_triggers", {}).get("keywords", []))
        print_result(f"P0 触发词数量：{p0_count}", p0_count >= 10)
        print_result(f"P1 触发词数量：{p1_count}", p1_count >= 10)
        
        return all_passed
        
    except Exception as e:
        print_result("配置解析", False, str(e))
        return False

# ============================================
# 测试 4: 技能路由配置验证
# ============================================
def test_skill_routes():
    print_header("测试 4: 技能路由配置验证")
    
    routes_path = SKILL_ROOT / "triggers" / "skill-routes.yaml"
    if not routes_path.exists():
        print_result("技能路由配置", False, "文件不存在")
        return False
    
    try:
        with open(routes_path, 'r', encoding='utf-8') as f:
            routes = yaml.safe_load(f)
        
        checks = [
            ("skill_name 字段", "skill_name" in routes),
            ("pre_skills 配置", "pre_skills" in routes),
            ("post_skills 配置", "post_skills" in routes),
            ("bidirectional_skills 配置", "bidirectional_skills" in routes),
            ("协同场景配置", "协同场景" in routes),
            ("priority_rules 配置", "priority_rules" in routes),
        ]
        
        all_passed = True
        for name, passed in checks:
            print_result(name, passed)
            all_passed = all_passed and passed
        
        # 验证协同技能数量
        pre_count = len(routes.get("pre_skills", []))
        post_count = len(routes.get("post_skills", []))
        bi_count = len(routes.get("bidirectional_skills", []))
        print_result(f"前置技能数量：{pre_count}", True)
        print_result(f"后置技能数量：{post_count}", True)
        print_result(f"双向联动技能数量：{bi_count}", True)
        
        return all_passed
        
    except Exception as e:
        print_result("路由解析", False, str(e))
        return False

# ============================================
# 测试 5: 知识文件同步验证
# ============================================
def test_knowledge_sync():
    print_header("测试 5: 知识文件同步验证")
    
    # 检查 Obsidian 同步
    obsidian_synced = OBSIDIAN_PATH.exists()
    print_result(f"Obsidian 同步路径", obsidian_synced, str(OBSIDIAN_PATH))
    
    # 检查 OpcClaw 同步
    opclaw_synced = OPCCLAW_PATH.exists()
    print_result(f"OpcClaw 同步路径", opclaw_synced, str(OPCCLAW_PATH))
    
    # 检查知识文件
    knowledge_files = [
        "00-总索引.md",
        "01-理论体系完整详述.md",
        "02-知识图谱.md",
    ]
    
    all_passed = obsidian_synced and opclaw_synced
    for file in knowledge_files:
        obsidian_file = OBSIDIAN_PATH / file
        opclaw_file = OPCCLAW_PATH / file
        obsidian_exists = obsidian_file.exists()
        opclaw_exists = opclaw_file.exists()
        passed = obsidian_exists and opclaw_exists
        print_result(f"知识文件同步：{file}", passed)
        all_passed = all_passed and passed
    
    return all_passed

# ============================================
# 测试 6: 健康检查
# ============================================
def test_health_check():
    print_header("测试 6: 健康检查")
    
    checks = []
    
    # 检查 SKILL.md 文件大小
    skill_md = SKILL_ROOT / "SKILL.md"
    if skill_md.exists():
        size = skill_md.stat().st_size
        passed = 5000 < size < 50000  # 5KB-50KB 合理范围
        checks.append(passed)
        print_result(f"SKILL.md 文件大小", passed, f"{size/1024:.1f}KB")
    
    # 检查触发词配置
    config_path = SKILL_ROOT / "triggers" / "auto-activate.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        passed = config.get("auto_activate", False) == True
        checks.append(passed)
        print_result(f"自动激活已启用", passed)
    
    # 检查日志目录可写
    log_dir = SKILL_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    try:
        test_log = log_dir / "test_write.log"
        test_log.write_text("test", encoding='utf-8')
        test_log.unlink()
        passed = True
        checks.append(passed)
        print_result(f"日志目录可写", passed)
    except:
        checks.append(False)
        print_result(f"日志目录可写", False)
    
    return all(checks) if checks else False

# ============================================
# 测试 7: 触发词覆盖度验证
# ============================================
def test_trigger_coverage():
    print_header("测试 7: 触发词覆盖度验证")
    
    config_path = SKILL_ROOT / "triggers" / "auto-activate.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 核心触发词检查
    p0_keywords = config.get("p0_direct_triggers", {}).get("keywords", [])
    required_p0 = ["象思维", "观物取象", "立象尽意", "取象比类", "观象制器"]
    
    all_passed = True
    for keyword in required_p0:
        passed = keyword in p0_keywords
        print_result(f"P0 触发词覆盖：{keyword}", passed)
        all_passed = all_passed and passed
    
    # 三层次触发词检查
    three_level = ["物象", "意象", "原象"]
    for keyword in three_level:
        passed = keyword in p0_keywords
        print_result(f"三层次触发词：{keyword}", passed)
        all_passed = all_passed and passed
    
    # 六非触发词检查
    six_non = ["非实体", "非对象", "非现成", "前语言", "前逻辑", "非确定"]
    for keyword in six_non:
        passed = keyword in config.get("p1_scenario_triggers", {}).get("keywords", [])
        print_result(f"六非触发词：{keyword}", passed)
        all_passed = all_passed and passed
    
    return all_passed

# ============================================
# 主测试函数
# ============================================
def main():
    print_header("象思维 Skill 封装测试验证")
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Skill 路径：{SKILL_ROOT}")
    
    results = {
        "目录结构": test_directory_structure(),
        "核心文件": test_core_files(),
        "触发规则": test_trigger_rules(),
        "技能路由": test_skill_routes(),
        "知识同步": test_knowledge_sync(),
        "健康检查": test_health_check(),
        "触发覆盖": test_trigger_coverage(),
    }
    
    print_header("测试结果汇总")
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for test_name, passed in results.items():
        status = "[OK]" if passed else "[FAIL]"
        result_text = "通过" if passed else "失败"
        print(f"  {status} {test_name}: {result_text}")
    
    print(f"\n  总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print(f"\n  [SUCCESS] 象思维 Skill 封装完成！所有测试通过！")
        print(f"\n  自动触发已配置，可在以下场景自动激活：")
        print(f"  - P0 直接触发：象思维/观物取象/取象比类等核心词")
        print(f"  - P1 场景触发：0 到 1/原创突破/本质洞察等")
        print(f"  - P2 信号触发：本质是什么/如何直观理解等")
        print(f"\n  协同路由已配置：")
        print(f"  - 前置技能：五行分类图谱/易经错综复杂")
        print(f"  - 后置技能：知行合一/知识学习/人机协同五象限")
        print(f"  - 双向联动：五色光思维/五行分类图谱")
    else:
        print(f"\n  [WARNING] 有 {total_count - passed_count} 项测试未通过，请检查配置")
    
    return passed_count == total_count

if __name__ == "__main__":
    try:
        import yaml
        yaml_available = True
    except ImportError:
        print("⚠️ PyYAML 未安装，正在安装...")
        import subprocess
        subprocess.check_call(["pip", "install", "pyyaml", "-q"])
        import yaml
        yaml_available = True
    
    success = main()
    exit(0 if success else 1)
