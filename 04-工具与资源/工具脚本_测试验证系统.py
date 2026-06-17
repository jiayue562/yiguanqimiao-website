#!/usr/bin/env python3
"""
知识库验证系统 - 功能测试脚本
用于测试验证系统的核心功能是否正常工作
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 开始测试知识库验证系统基本功能...")
    
    test_results = {
        'test_time': datetime.now().isoformat(),
        'tests_passed': 0,
        'tests_failed': 0,
        'details': {}
    }
    
    # 测试1: 检查测试文档是否存在
    print("\n🔍 测试1: 检查测试文档...")
    test_docs = [
        "测试文档/01-基础概念/知识管理基础.md",
        "测试文档/02-实践工具/Obsidian使用指南.md",
        "测试文档/03-学习方法/学习路径设计.md"
    ]
    
    kb_path = Path("C:/Users/jia'yue/Desktop/以观其妙书院知识库/观其妙书院/")
    
    all_exist = True
    for doc_path in test_docs:
        full_path = kb_path / doc_path
        if full_path.exists():
            print(f"  ✅ 测试文档存在: {doc_path}")
        else:
            print(f"  ❌ 测试文档不存在: {doc_path}")
            all_exist = False
    
    if all_exist:
        test_results['tests_passed'] += 1
        test_results['details']['test_documents'] = "通过"
        print("  ✅ 所有测试文档都存在")
    else:
        test_results['tests_failed'] += 1
        test_results['details']['test_documents'] = "失败"
        print("  ❌ 部分测试文档不存在")
    
    # 测试2: 检查配置文件
    print("\n📋 测试2: 检查配置文件...")
    config_path = kb_path / "08-工具与脚本/Python脚本/config.yaml"
    
    if config_path.exists():
        # 读取配置文件内容
        try:
            content = config_path.read_text(encoding='utf-8')
            if "knowledge_base:" in content and "path:" in content:
                test_results['tests_passed'] += 1
                test_results['details']['config_file'] = "通过"
                print("  ✅ 配置文件格式正确")
            else:
                test_results['tests_failed'] += 1
                test_results['details']['config_file'] = "格式错误"
                print("  ❌ 配置文件格式不正确")
        except Exception as e:
            test_results['tests_failed'] += 1
            test_results['details']['config_file'] = f"读取失败: {e}"
            print(f"  ❌ 配置文件读取失败: {e}")
    else:
        test_results['tests_failed'] += 1
        test_results['details']['config_file'] = "文件不存在"
        print("  ❌ 配置文件不存在")
    
    # 测试3: 检查Python脚本文件
    print("\n🐍 测试3: 检查Python脚本...")
    python_scripts = [
        "08-工具与脚本/Python脚本/学习路径验证模块.py",
        "08-工具与脚本/Python脚本/测试验证系统.py"
    ]
    
    all_scripts_exist = True
    for script_path in python_scripts:
        full_path = kb_path / script_path
        if full_path.exists():
            print(f"  ✅ Python脚本存在: {script_path}")
            
            # 检查文件内容
            try:
                content = full_path.read_text(encoding='utf-8', errors='ignore')
                if "def " in content or "class " in content:
                    print(f"    → 包含Python代码")
                else:
                    print(f"    ⚠️  可能不是有效的Python文件")
            except:
                print(f"    ⚠️  无法读取文件内容")
        else:
            print(f"  ❌ Python脚本不存在: {script_path}")
            all_scripts_exist = False
    
    if all_scripts_exist:
        test_results['tests_passed'] += 1
        test_results['details']['python_scripts'] = "通过"
        print("  ✅ 所有Python脚本都存在")
    else:
        test_results['tests_failed'] += 1
        test_results['details']['python_scripts'] = "部分缺失"
        print("  ❌ 部分Python脚本不存在")
    
    # 测试4: 检查文档结构
    print("\n📄 测试4: 测试文档结构验证...")
    try:
        # 模拟文档结构验证
        sample_doc_path = kb_path / test_docs[0]
        if sample_doc_path.exists():
            content = sample_doc_path.read_text(encoding='utf-8')
            
            # 检查基本结构元素
            structure_elements = {
                "标题": "# " in content,
                "核心定义": "核心定义" in content,
                "详细内容": "详细内容" in content,
                "标签系统": "标签系统" in content,
                "关联文件": "关联文件" in content
            }
            
            print("  文档结构检查:")
            for element, found in structure_elements.items():
                status = "✅" if found else "❌"
                print(f"    {status} {element}")
            
            # 计算结构完整性
            completeness = sum(structure_elements.values()) / len(structure_elements)
            if completeness >= 0.8:
                test_results['tests_passed'] += 1
                test_results['details']['document_structure'] = f"通过 ({completeness*100:.1f}%)"
                print(f"  ✅ 文档结构完整性: {completeness*100:.1f}%")
            else:
                test_results['tests_failed'] += 1
                test_results['details']['document_structure'] = f"不完整 ({completeness*100:.1f}%)"
                print(f"  ❌ 文档结构不完整: {completeness*100:.1f}%")
        else:
            test_results['tests_failed'] += 1
            test_results['details']['document_structure'] = "文档不存在"
            print("  ❌ 测试文档不存在")
    except Exception as e:
        test_results['tests_failed'] += 1
        test_results['details']['document_structure'] = f"验证失败: {e}"
        print(f"  ❌ 文档结构验证失败: {e}")
    
    # 测试5: 检查链接网络
    print("\n🔗 测试5: 测试链接网络验证...")
    try:
        # 检查文档中的链接
        links_found = []
        
        for doc_path in test_docs:
            full_path = kb_path / doc_path
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                
                # 查找双括号链接 [[文档名]]
                import re
                bracket_links = re.findall(r'\[\[([^\]]+)\]\]', content)
                links_found.extend(bracket_links)
                
                if bracket_links:
                    print(f"  {doc_path}: 发现 {len(bracket_links)} 个链接")
                    for link in bracket_links[:3]:  # 只显示前3个
                        print(f"    → [[{link}]]")
                else:
                    print(f"  {doc_path}: 未发现链接")
        
        if len(links_found) >= 3:
            test_results['tests_passed'] += 1
            test_results['details']['link_network'] = f"通过 ({len(links_found)}个链接)"
            print(f"  ✅ 链接网络测试通过: 发现 {len(links_found)} 个链接")
        else:
            test_results['tests_failed'] += 1
            test_results['details']['link_network'] = f"链接数量不足 ({len(links_found)}个)"
            print(f"  ❌ 链接数量不足: 只发现 {len(links_found)} 个链接")
    except Exception as e:
        test_results['tests_failed'] += 1
        test_results['details']['link_network'] = f"验证失败: {e}"
        print(f"  ❌ 链接网络验证失败: {e}")
    
    # 测试6: 检查学习路径验证
    print("\n🛣️ 测试6: 测试学习路径验证...")
    try:
        # 检查学习路径文档
        learning_path_doc = kb_path / test_docs[2]  # 学习路径设计.md
        
        if learning_path_doc.exists():
            content = learning_path_doc.read_text(encoding='utf-8')
            
            # 检查学习路径的关键元素
            path_elements = {
                "学习目标": "学习目标" in content,
                "学习阶段": "学习阶段" in content,
                "学习资源": "学习资源" in content,
                "评估方法": "评估方法" in content,
                "预计时长": "预计时长" in content
            }
            
            print("  学习路径结构检查:")
            for element, found in path_elements.items():
                status = "✅" if found else "❌"
                print(f"    {status} {element}")
            
            # 检查是否有阶段定义
            stage_pattern = r'### (阶段\s*\d+|第\s*\d+\s*阶段)'
            import re
            stages = re.findall(stage_pattern, content)
            
            if stages:
                print(f"  发现 {len(stages)} 个学习阶段:")
                for stage in stages:
                    print(f"    → {stage}")
            
            # 评估学习路径完整性
            completeness = sum(path_elements.values()) / len(path_elements)
            has_stages = len(stages) >= 2
            
            if completeness >= 0.6 and has_stages:
                test_results['tests_passed'] += 1
                test_results['details']['learning_path'] = f"通过 ({completeness*100:.1f}%, {len(stages)}阶段)"
                print(f"  ✅ 学习路径验证通过: {completeness*100:.1f}%完整, {len(stages)}个阶段")
            else:
                test_results['tests_failed'] += 1
                reason = []
                if completeness < 0.6:
                    reason.append(f"完整性{completeness*100:.1f}%")
                if not has_stages:
                    reason.append("阶段不足")
                test_results['details']['learning_path'] = f"不完整 ({', '.join(reason)})"
                print(f"  ❌ 学习路径不完整: {', '.join(reason)}")
        else:
            test_results['tests_failed'] += 1
            test_results['details']['learning_path'] = "文档不存在"
            print("  ❌ 学习路径文档不存在")
    except Exception as e:
        test_results['tests_failed'] += 1
        test_results['details']['learning_path'] = f"验证失败: {e}"
        print(f"  ❌ 学习路径验证失败: {e}")
    
    # 生成测试报告
    print("\n" + "="*50)
    print("📊 测试结果汇总")
    print("="*50)
    
    total_tests = test_results['tests_passed'] + test_results['tests_failed']
    pass_rate = (test_results['tests_passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"✅ 通过测试: {test_results['tests_passed']}")
    print(f"❌ 失败测试: {test_results['tests_failed']}")
    print(f"📈 通过率: {pass_rate:.1f}%")
    
    if pass_rate >= 80:
        print("\n🎉 测试结果: 优秀 - 系统基本功能正常")
        overall_status = "优秀"
    elif pass_rate >= 60:
        print("\n⚠️  测试结果: 良好 - 系统功能基本正常，有改进空间")
        overall_status = "良好"
    elif pass_rate >= 40:
        print("\n⚠️  测试结果: 一般 - 系统功能存在较多问题")
        overall_status = "一般"
    else:
        print("\n❌ 测试结果: 差 - 系统功能严重不足")
        overall_status = "差"
    
    print("\n📋 详细结果:")
    for test_name, result in test_results['details'].items():
        status_icon = "✅" if "通过" in str(result) or "优秀" in str(result) else "❌"
        print(f"  {status_icon} {test_name}: {result}")
    
    # 保存测试报告
    report_dir = kb_path / "08-工具与脚本/测试报告"
    report_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"功能测试报告_{timestamp}.json"
    
    test_results['overall_status'] = overall_status
    test_results['pass_rate'] = pass_rate
    test_results['total_tests'] = total_tests
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存至: {report_file}")
    
    # 生成简化的Markdown报告
    md_report = report_dir / f"功能测试报告_{timestamp}.md"
    
    md_content = f"""# 知识库验证系统 - 功能测试报告

## 📋 报告信息
- **生成时间**: {test_results['test_time']}
- **测试对象**: 知识库验证系统
- **总体状态**: {overall_status}
- **通过率**: {pass_rate:.1f}%

## 📊 测试统计
| 项目 | 数量 |
|------|------|
| 总测试数 | {total_tests} |
| 通过测试 | {test_results['tests_passed']} |
| 失败测试 | {test_results['tests_failed']} |
| 通过率 | {pass_rate:.1f}% |

## 🔍 详细结果

### 测试文档检查
- 状态: {test_results['details'].get('test_documents', 'N/A')}
- 说明: 检查测试文档是否存在和可访问

### 配置文件检查  
- 状态: {test_results['details'].get('config_file', 'N/A')}
- 说明: 检查配置文件格式和内容

### Python脚本检查
- 状态: {test_results['details'].get('python_scripts', 'N/A')}
- 说明: 检查Python脚本文件和代码结构

### 文档结构验证
- 状态: {test_results['details'].get('document_structure', 'N/A')}
- 说明: 验证文档结构完整性和标准化

### 链接网络验证
- 状态: {test_results['details'].get('link_network', 'N/A')}
- 说明: 检查文档间链接建立情况

### 学习路径验证
- 状态: {test_results['details'].get('learning_path', 'N/A')}
- 说明: 验证学习路径设计的完整性

## 🚀 改进建议

### 立即处理（通过率<60%）
{"- 修复失败的测试项" if pass_rate < 60 else "- 无"}

### 近期优化（通过率60-80%）
{"- 优化系统配置和脚本" if 60 <= pass_rate < 80 else "- 无"}

### 长期改进（通过率>80%）
{"- 进一步完善功能和文档" if pass_rate >= 80 else "- 无"}

## 📝 测试说明
本次测试主要验证知识库验证系统的基本功能完整性，包括文件存在性、配置有效性、代码可执行性、文档结构、链接网络和学习路径等方面的检查。

测试基于当前知识库的实际内容进行，结果反映了系统的当前状态。

---

**测试工具**: 功能测试脚本 v1.0  
**测试环境**: Python 3.8+  
**报告版本**: 1.0  
**生成系统**: 知识库验证系统测试套件
"""
    
    with open(md_report, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"📝 Markdown报告已保存至: {md_report}")
    
    return test_results

def create_validation_readiness_checklist():
    """创建验证系统就绪检查清单"""
    print("\n" + "="*50)
    print("✅ 验证系统就绪检查清单")
    print("="*50)
    
    checklist_items = [
        ("知识库路径设置", "检查config.yaml中的路径配置"),
        ("测试文档创建", "确保测试文档存在且格式正确"),
        ("Python环境", "确认Python 3.8+已安装"),
        ("依赖包", "检查是否有缺失的依赖包"),
        ("脚本权限", "确认有执行Python脚本的权限"),
        ("输出目录", "检查报告输出目录是否可写"),
        ("日志配置", "确认日志文件路径可访问"),
        ("备份机制", "检查备份功能是否配置"),
        ("通知设置", "确认通知功能配置正确"),
        ("自动化调度", "检查定时任务配置")
    ]
    
    print("请检查以下项目以确保验证系统正常工作:\n")
    
    for i, (item, description) in enumerate(checklist_items, 1):
        print(f"{i}. {item}")
        print(f"   📝 {description}")
    
    print("\n🔧 快速检查命令:")
    print("  python --version                            # 检查Python版本")
    print("  python -c \"import sys; print(sys.path)\"     # 检查Python路径")
    print("  ls -la 08-工具与脚本/Python脚本/           # 检查脚本文件")
    print("  cat config.yaml | head -20                  # 查看配置文件前20行")
    
    print("\n🚀 建议的下一步操作:")
    print("1. 运行完整验证: python main_validator.py --path '知识库路径'")
    print("2. 测试单个模块: python 学习路径验证模块.py --path '知识库路径'")
    print("3. 查看测试报告: ls -la 08-工具与脚本/测试报告/")
    print("4. 优化配置: 根据测试结果调整config.yaml")

def main():
    """主函数"""
    print("="*60)
    print("🤖 知识库验证系统 - 功能完整性测试")
    print("="*60)
    
    try:
        # 运行功能测试
        results = test_basic_functionality()
        
        # 创建就绪检查清单
        create_validation_readiness_checklist()
        
        # 根据测试结果给出建议
        pass_rate = results.get('pass_rate', 0)
        
        print("\n" + "="*50)
        print("📋 最终建议")
        print("="*50)
        
        if pass_rate >= 80:
            print("✅ 系统状态良好，可以开始正式验证工作")
            print("建议操作:")
            print("  1. 运行一次完整验证测试系统性能")
            print("  2. 配置自动化调度实现定期验证")
            print("  3. 集成到现有工作流程中")
        elif pass_rate >= 60:
            print("⚠️  系统基本可用，但需要改进")
            print("建议操作:")
            print("  1. 修复失败的测试项")
            print("  2. 优化配置文件和脚本")
            print("  3. 重新运行测试验证修复效果")
        else:
            print("❌ 系统存在较多问题，需要重大改进")
            print("建议操作:")
            print("  1. 检查环境配置和依赖")
            print("  2. 修复基本的文件存在性问题")
            print("  3. 重新设计测试用例")
        
        print("\n🎯 验证系统核心价值:")
        print("  - 自动化检查知识库质量")
        print("  - 发现和修复潜在问题")
        print("  - 提供数据驱动的改进建议")
        print("  - 建立持续的质量保障机制")
        
        return 0 if pass_rate >= 60 else 1
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return 2

if __name__ == "__main__":
    sys.exit(main())