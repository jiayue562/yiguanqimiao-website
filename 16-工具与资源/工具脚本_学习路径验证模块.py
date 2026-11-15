#!/usr/bin/env python3
"""
学习路径验证模块
用于验证知识库中学习路径的可行性和有效性
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime
from collections import defaultdict

class LearningPathValidator:
    """学习路径验证器"""
    
    def __init__(self, knowledge_base_path: str):
        self.kb_path = Path(knowledge_base_path)
        self.learning_paths = []
        self.path_metadata = {}
        
    def discover_learning_paths(self) -> List[Dict]:
        """发现知识库中的学习路径"""
        print("🔍 正在发现学习路径...")
        
        # 查找学习路径文件
        path_patterns = ['*学习路径*', '*学习指南*', '*学习路线*', '*学习计划*']
        all_path_files = []
        
        for pattern in path_patterns:
            for ext in ['.md', '.yaml', '.yml', '.json']:
                files = list(self.kb_path.rglob(f'{pattern}{ext}'))
                all_path_files.extend(files)
        
        # 去重
        all_path_files = list(set(all_path_files))
        print(f"  发现 {len(all_path_files)} 个学习路径文件")
        
        # 解析学习路径
        for path_file in all_path_files:
            try:
                path_info = self._parse_learning_path(path_file)
                if path_info:
                    self.learning_paths.append(path_info)
                    self.path_metadata[str(path_file)] = path_info
            except Exception as e:
                print(f"  警告: 解析文件失败 {path_file}: {e}")
        
        return self.learning_paths
    
    def _parse_learning_path(self, file_path: Path) -> Optional[Dict]:
        """解析学习路径文件"""
        content = file_path.read_text(encoding='utf-8')
        
        # 提取基本信息
        path_info = {
            'file_path': str(file_path),
            'title': self._extract_title(content),
            'description': self._extract_description(content),
            'target_audience': self._extract_target_audience(content),
            'prerequisites': self._extract_prerequisites(content),
            'estimated_duration': self._extract_estimated_duration(content),
            'difficulty_level': self._extract_difficulty_level(content),
            'learning_objectives': self._extract_learning_objectives(content),
            'stages': self._extract_learning_stages(content),
            'resources': self._extract_resources(content),
            'assessment_methods': self._extract_assessment_methods(content),
            'tags': self._extract_tags(content)
        }
        
        # 过滤空路径
        if not path_info['stages']:
            return None
        
        return path_info
    
    def _extract_title(self, content: str) -> str:
        """提取标题"""
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return title_match.group(1) if title_match else "未命名学习路径"
    
    def _extract_description(self, content: str) -> str:
        """提取描述"""
        # 查找描述段落
        lines = content.split('\n')
        description = []
        capturing = False
        
        for line in lines:
            if line.startswith('## 概述') or line.startswith('## 简介'):
                capturing = True
                continue
            elif capturing and line.startswith('##'):
                break
            elif capturing and line.strip():
                description.append(line.strip())
        
        return ' '.join(description) if description else ""
    
    def _extract_target_audience(self, content: str) -> List[str]:
        """提取目标受众"""
        audience = []
        
        # 查找目标受众部分
        audience_section = re.search(r'目标受众[：:]\s*(.+)', content)
        if audience_section:
            audience_text = audience_section.group(1)
            audience = [a.strip() for a in re.split(r'[,，、]', audience_text)]
        
        # 查找标签中的受众信息
        audience_tags = re.findall(r'#(新手|初级|中级|高级|专家)', content)
        audience.extend(audience_tags)
        
        return list(set(audience))
    
    def _extract_prerequisites(self, content: str) -> List[str]:
        """提取先决条件"""
        prerequisites = []
        
        # 查找先决条件部分
        prereq_section = re.search(r'先决条件[：:]\s*(.+)', content)
        if prereq_section:
            prereq_text = prereq_section.group(1)
            prerequisites = [p.strip() for p in re.split(r'[,，、]', prereq_text)]
        
        return prerequisites
    
    def _extract_estimated_duration(self, content: str) -> Dict[str, int]:
        """提取预计时长"""
        duration = {'total_hours': 0, 'total_days': 0, 'weeks': 0}
        
        # 查找时长信息
        duration_patterns = [
            (r'预计时长[：:]\s*(\d+)\s*小时', 'total_hours'),
            (r'预计时长[：:]\s*(\d+)\s*天', 'total_days'),
            (r'预计时长[：:]\s*(\d+)\s*周', 'weeks'),
            (r'(\d+)\s*小时', 'total_hours'),
            (r'(\d+)\s*天', 'total_days'),
            (r'(\d+)\s*周', 'weeks')
        ]
        
        for pattern, key in duration_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    duration[key] = int(match.group(1))
                except ValueError:
                    pass
        
        # 计算总时长（小时）
        if duration['total_hours'] == 0:
            if duration['total_days'] > 0:
                duration['total_hours'] = duration['total_days'] * 8
            elif duration['weeks'] > 0:
                duration['total_hours'] = duration['weeks'] * 40
        
        return duration
    
    def _extract_difficulty_level(self, content: str) -> str:
        """提取难度级别"""
        difficulty_levels = ['入门', '初级', '中级', '高级', '专家']
        
        for level in difficulty_levels:
            if level in content:
                return level
        
        # 检查标签
        difficulty_tags = re.findall(r'#(入门|初级|中级|高级|专家)', content)
        if difficulty_tags:
            return difficulty_tags[0]
        
        return '未知'
    
    def _extract_learning_objectives(self, content: str) -> List[str]:
        """提取学习目标"""
        objectives = []
        
        # 查找学习目标部分
        lines = content.split('\n')
        capturing = False
        
        for line in lines:
            if line.startswith('## 学习目标') or line.startswith('## 学习目的'):
                capturing = True
                continue
            elif capturing and line.startswith('##'):
                break
            elif capturing and line.startswith('-'):
                objective = line[1:].strip()
                if objective:
                    objectives.append(objective)
        
        # 如果没找到列表格式，尝试其他格式
        if not objectives:
            obj_section = re.search(r'学习目标[：:]\s*(.+)', content)
            if obj_section:
                obj_text = obj_section.group(1)
                objectives = [o.strip() for o in re.split(r'[,，;；]', obj_text)]
        
        return objectives
    
    def _extract_learning_stages(self, content: str) -> List[Dict]:
        """提取学习阶段"""
        stages = []
        
        # 查找阶段标题
        stage_pattern = r'### (阶段\s*\d+|第\s*\d+\s*阶段|阶段\d+)[：:]?\s*(.+)'
        stage_matches = re.findall(stage_pattern, content)
        
        for stage_num, stage_title in stage_matches:
            # 查找该阶段的内容
            stage_content = self._extract_stage_content(content, stage_num, stage_title)
            
            stage_info = {
                'stage_number': stage_num.strip(),
                'stage_title': stage_title.strip(),
                'duration': self._extract_stage_duration(stage_content),
                'topics': self._extract_stage_topics(stage_content),
                'resources': self._extract_stage_resources(stage_content),
                'activities': self._extract_stage_activities(stage_content),
                'assessment': self._extract_stage_assessment(stage_content)
            }
            
            stages.append(stage_info)
        
        return stages
    
    def _extract_stage_content(self, content: str, stage_num: str, stage_title: str) -> str:
        """提取阶段内容"""
        # 查找阶段开始位置
        stage_start = f'### {stage_num}{stage_title}'
        start_pos = content.find(stage_start)
        
        if start_pos == -1:
            return ""
        
        # 查找下一个阶段开始位置
        remaining = content[start_pos:]
        next_stage_match = re.search(r'### (?:阶段\s*\d+|第\s*\d+\s*阶段|阶段\d+)', remaining[len(stage_start):])
        
        if next_stage_match:
            end_pos = start_pos + len(stage_start) + next_stage_match.start()
            return content[start_pos:end_pos]
        else:
            return content[start_pos:]
    
    def _extract_stage_duration(self, stage_content: str) -> Dict[str, int]:
        """提取阶段时长"""
        duration = {'hours': 0, 'days': 0}
        
        duration_patterns = [
            (r'时长[：:]\s*(\d+)\s*小时', 'hours'),
            (r'时长[：:]\s*(\d+)\s*天', 'days'),
            (r'(\d+)\s*小时', 'hours'),
            (r'(\d+)\s*天', 'days')
        ]
        
        for pattern, key in duration_patterns:
            match = re.search(pattern, stage_content)
            if match:
                try:
                    duration[key] = int(match.group(1))
                except ValueError:
                    pass
        
        return duration
    
    def _extract_stage_topics(self, stage_content: str) -> List[str]:
        """提取阶段主题"""
        topics = []
        
        # 查找主题列表
        topic_lines = re.findall(r'[-*]\s*(.+)', stage_content)
        topics.extend(topic_lines)
        
        # 查找主题标题
        topic_headers = re.findall(r'#### (.+)', stage_content)
        topics.extend(topic_headers)
        
        return list(set(topics))
    
    def _extract_stage_resources(self, stage_content: str) -> List[Dict]:
        """提取阶段资源"""
        resources = []
        
        # 查找资源链接
        resource_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', stage_content)
        for text, link in resource_links:
            if not link.startswith(('http://', 'https://')):
                resources.append({
                    'type': 'internal',
                    'title': text,
                    'path': link
                })
            else:
                resources.append({
                    'type': 'external',
                    'title': text,
                    'url': link
                })
        
        # 查找双括号链接
        double_bracket_links = re.findall(r'\[\[([^\]]+)\]\]', stage_content)
        for link in double_bracket_links:
            resources.append({
                'type': 'internal',
                'title': link,
                'path': link
            })
        
        return resources
    
    def _extract_stage_activities(self, stage_content: str) -> List[str]:
        """提取阶段活动"""
        activities = []
        
        # 查找活动部分
        activity_keywords = ['练习', '实验', '项目', '作业', '任务', '挑战']
        
        lines = stage_content.split('\n')
        for line in lines:
            for keyword in activity_keywords:
                if keyword in line and '活动' not in line:
                    activities.append(line.strip())
        
        return activities
    
    def _extract_stage_assessment(self, stage_content: str) -> List[str]:
        """提取阶段评估"""
        assessment_methods = []
        
        # 查找评估方法
        assessment_keywords = ['测试', '考试', '测验', '评估', '考核', '检查点']
        
        lines = stage_content.split('\n')
        for line in lines:
            for keyword in assessment_keywords:
                if keyword in line:
                    assessment_methods.append(line.strip())
        
        return assessment_methods
    
    def _extract_resources(self, content: str) -> List[Dict]:
        """提取资源"""
        resources = []
        
        # 查找资源部分
        lines = content.split('\n')
        capturing = False
        
        for line in lines:
            if line.startswith('## 资源') or line.startswith('## 参考资料'):
                capturing = True
                continue
            elif capturing and line.startswith('##'):
                break
            elif capturing and line.strip():
                # 解析资源行
                resource = self._parse_resource_line(line)
                if resource:
                    resources.append(resource)
        
        return resources
    
    def _parse_resource_line(self, line: str) -> Optional[Dict]:
        """解析资源行"""
        # 检查是否为链接格式
        link_match = re.match(r'[-*]\s*\[([^\]]+)\]\(([^)]+)\)', line)
        if link_match:
            text, link = link_match.groups()
            resource_type = 'external' if link.startswith(('http://', 'https://')) else 'internal'
            
            return {
                'type': resource_type,
                'title': text.strip(),
                'url': link if resource_type == 'external' else None,
                'path': link if resource_type == 'internal' else None
            }
        
        # 检查是否为双括号链接
        bracket_match = re.match(r'[-*]\s*\[\[([^\]]+)\]\]', line)
        if bracket_match:
            title = bracket_match.group(1)
            return {
                'type': 'internal',
                'title': title.strip(),
                'path': title
            }
        
        # 普通文本
        if line.strip().startswith('-') or line.strip().startswith('*'):
            title = line.lstrip('-* ').strip()
            if title:
                return {
                    'type': 'text',
                    'title': title
                }
        
        return None
    
    def _extract_assessment_methods(self, content: str) -> List[str]:
        """提取评估方法"""
        assessment_methods = []
        
        # 查找评估部分
        lines = content.split('\n')
        capturing = False
        
        for line in lines:
            if line.startswith('## 评估') or line.startswith('## 考核'):
                capturing = True
                continue
            elif capturing and line.startswith('##'):
                break
            elif capturing and (line.startswith('-') or line.startswith('*')):
                method = line.lstrip('-* ').strip()
                if method:
                    assessment_methods.append(method)
        
        return assessment_methods
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 查找标签行
        tag_line_match = re.search(r'标签[：:]\s*(.+)', content)
        if tag_line_match:
            tag_text = tag_line_match.group(1)
            tags.extend([t.strip() for t in re.split(r'[,，\s]+', tag_text)])
        
        # 查找井号标签
        hashtag_matches = re.findall(r'#([\w\u4e00-\u9fff\-]+)', content)
        tags.extend(hashtag_matches)
        
        return list(set(tags))
    
    def validate_path_feasibility(self, path_info: Dict) -> Dict:
        """验证学习路径的可行性"""
        validation_results = {
            'path_title': path_info.get('title', ''),
            'feasibility_score': 0,
            'issues': [],
            'strengths': [],
            'recommendations': []
        }
        
        # 1. 检查基本信息完整性
        basic_info_score = self._validate_basic_info(path_info)
        validation_results['feasibility_score'] += basic_info_score
        
        # 2. 检查阶段结构
        stage_score, stage_issues = self._validate_stages(path_info.get('stages', []))
        validation_results['feasibility_score'] += stage_score
        validation_results['issues'].extend(stage_issues)
        
        # 3. 检查资源可用性
        resource_score, resource_issues = self._validate_resources(path_info)
        validation_results['feasibility_score'] += resource_score
        validation_results['issues'].extend(resource_issues)
        
        # 4. 检查难度递进
        difficulty_score, difficulty_issues = self._validate_difficulty_progression(path_info)
        validation_results['feasibility_score'] += difficulty_score
        validation_results['issues'].extend(difficulty_issues)
        
        # 5. 检查时间合理性
        time_score, time_issues = self._validate_time_estimation(path_info)
        validation_results['feasibility_score'] += time_score
        validation_results['issues'].extend(time_issues)
        
        # 计算总分
        validation_results['feasibility_score'] = round(validation_results['feasibility_score'] / 5, 2)
        
        # 生成建议
        validation_results['recommendations'] = self._generate_feasibility_recommendations(
            validation_results['feasibility_score'],
            validation_results['issues']
        )
        
        return validation_results
    
    def _validate_basic_info(self, path_info: Dict) -> float:
        """验证基本信息完整性"""
        required_fields = [
            'title', 'description', 'target_audience', 'learning_objectives'
        ]
        
        score = 0
        for field in required_fields:
            if path_info.get(field):
                if isinstance(path_info[field], list):
                    if len(path_info[field]) > 0:
                        score += 5
                else:
                    if str(path_info[field]).strip():
                        score += 5
        
        return score
    
    def _validate_stages(self, stages: List[Dict]) -> Tuple[float, List[str]]:
        """验证学习阶段"""
        if not stages:
            return 0, ["未定义学习阶段"]
        
        score = 0
        issues = []
        
        # 检查阶段数量
        if len(stages) >= 3:
            score += 20
        elif len(stages) >= 2:
            score += 15
            issues.append("阶段数量较少，建议划分更多阶段")
        else:
            score += 5
            issues.append("阶段数量过少，建议重新设计阶段结构")
        
        # 检查每个阶段的完整性
        for i, stage in enumerate(stages, 1):
            stage_issues = []
            
            # 检查阶段标题
            if not stage.get('stage_title'):
                stage_issues.append(f"阶段{i}缺少标题")
            
            # 检查阶段主题
            if not stage.get('topics'):
                stage_issues.append(f"阶段{i}缺少学习主题")
            
            # 检查阶段资源
            if not stage.get('resources'):
                stage_issues.append(f"阶段{i}缺少学习资源")
            
            # 检查阶段活动
            if not stage.get('activities'):
                stage_issues.append(f"阶段{i}缺少学习活动")
            
            if stage_issues:
                issues.extend(stage_issues)
                score -= 5 * len(stage_issues)
            else:
                score += 5
        
        return min(max(score, 0), 20), issues
    
    def _validate_resources(self, path_info: Dict) -> Tuple[float, List[str]]:
        """验证资源可用性"""
        score = 0
        issues = []
        
        # 检查总资源
        total_resources = path_info.get('resources', [])
        stage_resources = []
        for stage in path_info.get('stages', []):
            stage_resources.extend(stage.get('resources', []))
        
        all_resources = total_resources + stage_resources
        
        if len(all_resources) >= 10:
            score += 20
        elif len(all_resources) >= 5:
            score += 15
            issues.append("学习资源数量偏少")
        else:
            score += 5
            issues.append("学习资源严重不足")
        
        # 检查资源类型分布
        resource_types = defaultdict(int)
        for resource in all_resources:
            resource_types[resource.get('type', 'unknown')] += 1
        
        # 检查是否有多种资源类型
        if len(resource_types) >= 3:
            score += 10
        elif len(resource_types) >= 2:
            score += 5
        else:
            issues.append("资源类型单一")
        
        return min(max(score, 0), 30), issues
    
    def _validate_difficulty_progression(self, path_info: Dict) -> Tuple[float, List[str]]:
        """验证难度递进"""
        score = 0
        issues = []
        
        stages = path_info.get('stages', [])
        if len(stages) < 2:
            return 10, ["阶段数量不足，无法评估难度递进"]
        
        # 分析阶段关键词
        difficulty_keywords = {
            '基础': 1, '入门': 1, '初级': 2, '中级': 3, 
            '高级': 4, '进阶': 4, '专家': 5, '深入': 4
        }
        
        stage_difficulties = []
        for i, stage in enumerate(stages, 1):
            stage_text = f"{stage.get('stage_title', '')} {' '.join(stage.get('topics', []))}"
            
            # 查找难度关键词
            max_difficulty = 1
            for keyword, level in difficulty_keywords.items():
                if keyword in stage_text:
                    max_difficulty = max(max_difficulty, level)
            
            stage_difficulties.append(max_difficulty)
        
        # 检查难度是否递增
        is_increasing = all(stage_difficulties[i] >= stage_difficulties[i-1] 
                          for i in range(1, len(stage_difficulties)))
        
        if is_increasing:
            score += 25
        else:
            score += 10
            issues.append("难度递进不明显，存在难度跳跃或倒退")
        
        return min(max(score, 0), 25), issues
    
    def _validate_time_estimation(self, path_info: Dict) -> Tuple[float, List[str]]:
        """验证时间估计合理性"""
        score = 0
        issues = []
        
        total_duration = path_info.get('estimated_duration', {})
        total_hours = total_duration.get('total_hours', 0)
        
        if total_hours == 0:
            return 5, ["未提供学习时长估计"]
        
        # 检查总时长合理性
        if 20 <= total_hours <= 200:
            score += 20
        elif total_hours < 20:
            score += 10
            issues.append(f"总学习时长偏短 ({total_hours}小时)")
        else:
            score += 15
            issues.append(f"总学习时长较长 ({total_hours}小时)，可能影响完成率")
        
        # 检查阶段时长分配
        stages = path_info.get('stages', [])
        if stages:
            stage_hours = []
            for stage in stages:
                stage_duration = stage.get('duration', {})
                stage_hours.append(stage_duration.get('hours', 0))
            
            # 检查是否有阶段时长为0
            zero_hour_stages = sum(1 for h in stage_hours if h == 0)
            if zero_hour_stages > 0:
                score -= 5 * zero_hour_stages
                issues.append(f"{zero_hour_stages}个阶段未指定学习时长")
            
            # 检查时长分配是否均衡
            if len(stage_hours) >= 2:
                avg_hours = sum(stage_hours) / len(stage_hours)
                imbalance_factor = max(stage_hours) / min(stage_hours) if min(stage_hours) > 0 else 0
                
                if 0.5 <= imbalance_factor <= 2:
                    score += 10
                else:
                    score += 5
                    issues.append("阶段学习时长分配不均衡")
        
        return min(max(score, 0), 30), issues
    
    def _generate_feasibility_recommendations(self, score: float, issues: List[str]) -> List[str]:
        """生成可行性建议"""
        recommendations = []
        
        if score >= 90:
            recommendations.append("学习路径设计优秀，可行性很高")
            recommendations.append("建议保持当前设计，定期更新内容")
        elif score >= 80:
            recommendations.append("学习路径设计良好，可行性较高")
            recommendations.append("建议优化存在的小问题")
        elif score >= 70:
            recommendations.append("学习路径设计一般，有改进空间")
            recommendations.append("建议重点关注存在的问题")
        elif score >= 60:
            recommendations.append("学习路径需要改进，可行性一般")
            recommendations.append("建议重新设计部分内容")
        else:
            recommendations.append("学习路径可行性较低，需要重大改进")
            recommendations.append("建议重新设计整个学习路径")
        
        # 根据具体问题添加建议
        if any("资源" in issue for issue in issues):
            recommendations.append("建议增加学习资源数量和多样性")
        
        if any("阶段" in issue and "数量" in issue for issue in issues):
            recommendations.append("建议优化阶段划分，确保学习流程清晰")
        
        if any("难度" in issue for issue in issues):
            recommendations.append("建议优化难度递进，确保学习曲线平滑")
        
        if any("时长" in issue for issue in issues):
            recommendations.append("建议优化时间分配，确保学习进度合理")
        
        return recommendations
    
    def validate_all_paths(self) -> Dict:
        """验证所有学习路径"""
        print("📊 正在验证学习路径...")
        
        # 发现所有学习路径
        self.discover_learning_paths()
        
        validation_results = {
            'total_paths': len(self.learning_paths),
            'validation_time': datetime.now().isoformat(),
            'path_validations': [],
            'overall_metrics': {
                'average_feasibility': 0,
                'path_distribution': defaultdict(int),
                'common_issues': defaultdict(int),
                'strengths': defaultdict(int)
            }
        }
        
        if not self.learning_paths:
            print("⚠️  未发现学习路径")
            return validation_results
        
        # 验证每个学习路径
        total_feasibility = 0
        all_issues = []
        all_strengths = []
        
        for i, path_info in enumerate(self.learning_paths, 1):
            print(f"  验证路径 {i}/{len(self.learning_paths)}: {path_info.get('title', '未命名')}")
            
            # 验证可行性
            path_validation = self.validate_path_feasibility(path_info)
            validation_results['path_validations'].append(path_validation)
            
            # 收集统计信息
            total_feasibility += path_validation['feasibility_score']
            
            # 统计问题
            for issue in path_validation['issues']:
                all_issues.append(issue)
                validation_results['overall_metrics']['common_issues'][issue] += 1
            
            # 统计优势
            for strength in path_validation['strengths']:
                all_strengths.append(strength)
                validation_results['overall_metrics']['strengths'][strength] += 1
            
            # 统计路径类型
            difficulty = path_info.get('difficulty_level', '未知')
            validation_results['overall_metrics']['path_distribution'][difficulty] += 1
        
        # 计算总体指标
        if validation_results['total_paths'] > 0:
            validation_results['overall_metrics']['average_feasibility'] = round(
                total_feasibility / validation_results['total_paths'], 2
            )
        
        # 获取最常见的问题和建议
        validation_results['overall_metrics']['top_issues'] = dict(
            sorted(validation_results['overall_metrics']['common_issues'].items(), 
                  key=lambda x: x[1], reverse=True)[:5]
        )
        
        validation_results['overall_metrics']['top_strengths'] = dict(
            sorted(validation_results['overall_metrics']['strengths'].items(),
                  key=lambda x: x[1], reverse=True)[:5]
        )
        
        print(f"✅ 验证完成!")
        print(f"   总路径数: {validation_results['total_paths']}")
        print(f"   平均可行性: {validation_results['overall_metrics']['average_feasibility']}")
        
        return validation_results
    
    def generate_path_recommendations(self, validation_results: Dict) -> List[str]:
        """生成路径优化建议"""
        recommendations = []
        
        overall_metrics = validation_results.get('overall_metrics', {})
        average_feasibility = overall_metrics.get('average_feasibility', 0)
        
        # 总体建议
        if average_feasibility >= 90:
            recommendations.append("总体学习路径设计优秀，继续保持")
        elif average_feasibility >= 80:
            recommendations.append("总体学习路径设计良好，可优化细节")
        elif average_feasibility >= 70:
            recommendations.append("总体学习路径设计一般，需要系统改进")
        else:
            recommendations.append("总体学习路径设计需要重大改进")
        
        # 根据常见问题生成建议
        top_issues = overall_metrics.get('top_issues', {})
        for issue, count in top_issues.items():
            if '资源' in issue:
                recommendations.append(f"共 {count} 个路径存在资源问题，建议统一资源标准")
            elif '阶段' in issue:
                recommendations.append(f"共 {count} 个路径存在阶段结构问题，建议优化阶段设计")
            elif '难度' in issue:
                recommendations.append(f"共 {count} 个路径存在难度问题，建议建立难度标准")
            elif '时长' in issue:
                recommendations.append(f"共 {count} 个路径存在时间问题，建议优化时间估计")
        
        # 路径类型分布建议
        path_distribution = overall_metrics.get('path_distribution', {})
        if '入门' not in path_distribution or path_distribution.get('入门', 0) == 0:
            recommendations.append("缺少入门级学习路径，建议补充")
        
        if '高级' not in path_distribution or path_distribution.get('高级', 0) == 0:
            recommendations.append("缺少高级学习路径，建议补充")
        
        return recommendations
    
    def save_validation_results(self, validation_results: Dict, output_dir: str = None) -> str:
        """保存验证结果"""
        if output_dir is None:
            output_dir = self.kb_path / "学习路径验证报告"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON结果
        json_file = output_path / f"learning_path_validation_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, ensure_ascii=False, indent=2)
        
        # 生成Markdown报告
        md_file = output_path / f"学习路径验证报告_{timestamp}.md"
        report_content = self._generate_markdown_report(validation_results)
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 报告已保存至: {md_file}")
        print(f"📊 数据已保存至: {json_file}")
        
        return str(md_file)
    
    def _generate_markdown_report(self, validation_results: Dict) -> str:
        """生成Markdown报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = [
            f"# 📚 学习路径验证报告",
            "",
            f"**生成时间**: {timestamp}",
            f"**知识库路径**: {self.kb_path}",
            f"**验证系统**: 学习路径验证模块 v1.0",
            "",
            "---",
            "",
            "## 📋 执行摘要",
            "",
            f"- **总学习路径数**: {validation_results.get('total_paths', 0)}",
            f"- **平均可行性得分**: {validation_results.get('overall_metrics', {}).get('average_feasibility', 0)}",
            f"- **验证时间**: {validation_results.get('validation_time', '')}",
            "",
            "## 📊 总体统计",
            "",
            "### 路径难度分布",
        ]
        
        # 添加难度分布
        path_distribution = validation_results.get('overall_metrics', {}).get('path_distribution', {})
        for difficulty, count in path_distribution.items():
            percentage = (count / validation_results['total_paths'] * 100) if validation_results['total_paths'] > 0 else 0
            report.append(f"- **{difficulty}**: {count} 条 ({percentage:.1f}%)")
        
        report.extend([
            "",
            "### 常见问题统计",
        ])
        
        # 添加常见问题
        top_issues = validation_results.get('overall_metrics', {}).get('top_issues', {})
        if top_issues:
            for issue, count in top_issues.items():
                report.append(f"- {issue}: {count} 次")
        else:
            report.append("- 未发现常见问题")
        
        report.extend([
            "",
            "### 主要优势统计",
        ])
        
        # 添加主要优势
        top_strengths = validation_results.get('overall_metrics', {}).get('top_strengths', {})
        if top_strengths:
            for strength, count in top_strengths.items():
                report.append(f"- {strength}: {count} 次")
        else:
            report.append("- 未统计到显著优势")
        
        report.extend([
            "",
            "## 🛣️ 各路径验证详情",
            "",
            "| 序号 | 路径标题 | 可行性得分 | 主要问题 | 建议 |",
            "|------|----------|------------|----------|------|",
        ])
        
        # 添加各路径详情
        for i, path_validation in enumerate(validation_results.get('path_validations', []), 1):
            title = path_validation.get('path_title', '未命名')
            if len(title) > 20:
                title = title[:17] + "..."
            
            score = path_validation.get('feasibility_score', 0)
            
            issues = path_validation.get('issues', [])
            main_issue = issues[0] if issues else "无"
            if len(main_issue) > 30:
                main_issue = main_issue[:27] + "..."
            
            recommendations = path_validation.get('recommendations', [])
            main_rec = recommendations[0] if recommendations else "无"
            if len(main_rec) > 30:
                main_rec = main_rec[:27] + "..."
            
            report.append(f"| {i} | {title} | {score} | {main_issue} | {main_rec} |")
        
        report.extend([
            "",
            "## 🚀 优化建议",
            "",
            "基于验证结果，提出以下优化建议：",
            "",
        ])
        
        # 添加优化建议
        recommendations = self.generate_path_recommendations(validation_results)
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. {rec}")
        
        report.extend([
            "",
            "## 📝 实施计划",
            "",
            "建议按以下优先级实施改进：",
            "",
            "### 高优先级（立即处理）",
            "- 修复严重可行性问题",
            "- 补充缺失的关键资源",
            "- 优化明显不合理的时间估计",
            "",
            "### 中优先级（近期优化）",
            "- 优化阶段结构设计",
            "- 完善难度递进逻辑",
            "- 丰富学习活动类型",
            "",
            "### 低优先级（长期改进）",
            "- 优化报告和评估体系",
            "- 增加个性化学习支持",
            "- 建立学习效果跟踪",
            "",
            "---",
            "",
            "> **报告说明**: 本报告由学习路径验证模块自动生成，数据基于当前知识库内容分析。",
            "",
            "**生成工具**: 学习路径验证模块 v1.0",
            f"**下次验证**: 建议 {datetime.now().strftime('%Y-%m-%d')}",
            ""
        ])
        
        return '\n'.join(report)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='学习路径验证工具')
    parser.add_argument('--path', type=str, required=True,
                       help='知识库路径')
    parser.add_argument('--output', type=str, default=None,
                       help='报告输出目录')
    
    args = parser.parse_args()
    
    # 检查路径
    kb_path = Path(args.path)
    if not kb_path.exists():
        print(f"❌ 错误: 路径不存在 - {args.path}")
        return
    
    print(f"🔍 开始学习路径验证...")
    print(f"📁 知识库路径: {kb_path}")
    
    # 创建验证器
    validator = LearningPathValidator(args.path)
    
    # 运行验证
    results = validator.validate_all_paths()
    
    # 保存结果
    report_path = validator.save_validation_results(results, args.output)
    
    print(f"\n🎉 验证完成!")
    print(f"📄 报告位置: {report_path}")
    
    # 输出关键指标
    avg_feasibility = results.get('overall_metrics', {}).get('average_feasibility', 0)
    total_paths = results.get('total_paths', 0)
    
    print(f"📊 关键指标:")
    print(f"   总路径数: {total_paths}")
    print(f"   平均可行性: {avg_feasibility}")
    
    if avg_feasibility >= 80:
        print("✅ 学习路径整体质量良好")
    elif avg_feasibility >= 70:
        print("⚠️  学习路径需要改进")
    else:
        print("❌ 学习路径需要重大改进")


if __name__ == "__main__":
    main()