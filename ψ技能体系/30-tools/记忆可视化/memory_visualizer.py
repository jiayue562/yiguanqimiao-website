#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
记忆可视化引擎
生成记忆增长图表、知识图谱、时间轴

版本：v1.0
创建：2026-04-17
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️ 未安装 matplotlib，请运行：pip install matplotlib")


class MemoryVisualizer:
    """记忆可视化引擎"""
    
    def __init__(self, memory_dir: str):
        """
        初始化可视化引擎
        
        Args:
            memory_dir: 记忆目录路径
        """
        self.memory_dir = Path(memory_dir)
        self.memories = []
        self.stats = {}
        
    def load_memories(self) -> int:
        """加载记忆文件"""
        print(f"📂 加载记忆：{self.memory_dir}")
        
        memory_files = sorted(self.memory_dir.glob("*.md"))
        
        for file_path in memory_files:
            if file_path.name.startswith("embedding_cache"):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # 提取元数据
                file_date = file_path.stem
                word_count = len(content.split())
                
                # 提取标签
                tags = []
                for line in content.split('\n')[:50]:
                    if line.startswith('- **标签**:'):
                        tags = line.replace('- **标签**:', '').strip().split(',')
                        
                self.memories.append({
                    'file': file_path.name,
                    'date': file_date,
                    'word_count': word_count,
                    'tags': [t.strip() for t in tags],
                    'path': str(file_path)
                })
                
            except Exception as e:
                print(f"⚠️ 读取失败 {file_path.name}: {e}")
                
        print(f"✅ 加载 {len(self.memories)} 个记忆文件")
        return len(self.memories)
        
    def calculate_stats(self) -> Dict:
        """计算统计信息"""
        if not self.memories:
            return {}
            
        # 按日期统计
        daily_counts = Counter(m['date'] for m in self.memories)
        
        # 按标签统计
        all_tags = []
        for m in self.memories:
            all_tags.extend(m['tags'])
        tag_counts = Counter(all_tags)
        
        # 计算趋势
        dates = sorted([datetime.strptime(m['date'], '%Y-%m-%d') for m in self.memories])
        if len(dates) > 1:
            date_range = (dates[-1] - dates[0]).days + 1
            daily_avg = len(self.memories) / date_range
        else:
            daily_avg = 0
            
        self.stats = {
            'total_memories': len(self.memories),
            'total_words': sum(m['word_count'] for m in self.memories),
            'date_range': {
                'start': min(m['date'] for m in self.memories),
                'end': max(m['date'] for m in self.memories)
            },
            'daily_counts': dict(daily_counts),
            'tag_counts': dict(tag_counts.most_common(20)),
            'daily_average': round(daily_avg, 2),
            'most_active_day': daily_counts.most_common(1)[0] if daily_counts else None
        }
        
        return self.stats
        
    def generate_text_report(self) -> str:
        """生成文本报告"""
        if not self.stats:
            self.calculate_stats()
            
        report = f"""
# 记忆可视化报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**记忆总数**: {self.stats['total_memories']}  
**总字数**: {self.stats['total_words']:,}  
**日期范围**: {self.stats['date_range']['start']} ~ {self.stats['date_range']['end']}  
**日均增长**: {self.stats['daily_average']} 条/天

## 📈 增长趋势

"""
        # 添加最近 7 天数据
        report += "### 最近 7 天\n\n"
        recent_dates = sorted(self.stats['daily_counts'].keys())[-7:]
        for date in recent_dates:
            count = self.stats['daily_counts'][date]
            bar = '█' * count
            report += f"- {date}: {bar} ({count}条)\n"
            
        # 热门标签
        report += "\n## 🏷️ 热门标签\n\n"
        top_tags = list(self.stats['tag_counts'].items())[:10]
        for i, (tag, count) in enumerate(top_tags, 1):
            report += f"{i}. #{tag} ({count}次)\n"
            
        # 最活跃日期
        if self.stats['most_active_day']:
            date, count = self.stats['most_active_day']
            report += f"\n## 💡 洞察\n\n"
            report += f"- 最活跃日期：{date} ({count}条记忆)\n"
            report += f"- 平均每天创建 {self.stats['daily_average']} 条记忆\n"
            
        report += f"\n---\n_记忆可视化报告 · {datetime.now().strftime('%Y-%m-%d')} · 龙心 OS_\n"
        
        return report
        
    def generate_growth_chart(self, output_file: str = None, days: int = 30):
        """
        生成增长图表
        
        Args:
            output_file: 输出文件路径
            days: 显示最近天数
        """
        if not HAS_MATPLOTLIB:
            print("❌ matplotlib 未安装，跳过图表生成")
            return
            
        # 准备数据
        recent_dates = sorted(self.stats['daily_counts'].keys())[-days:]
        counts = [self.stats['daily_counts'].get(d, 0) for d in recent_dates]
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in recent_dates]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(dates, counts, color='steelblue', alpha=0.7)
        
        # 格式化
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        plt.xticks(rotation=45)
        
        ax.set_xlabel('日期')
        ax.set_ylabel('记忆数量')
        ax.set_title(f'记忆增长趋势（最近{days}天）')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=150)
            print(f"📊 图表已保存：{output_file}")
        else:
            plt.show()
            
        plt.close()
        
    def generate_tag_cloud_data(self) -> List[Dict]:
        """生成标签云数据"""
        if not self.stats:
            self.calculate_stats()
            
        tag_data = []
        max_count = max(self.stats['tag_counts'].values()) if self.stats['tag_counts'] else 1
        
        for tag, count in self.stats['tag_counts'].items():
            size = 1 + (count / max_count) * 2  # 字体大小 1-3
            tag_data.append({
                'tag': tag,
                'count': count,
                'size': round(size, 1)
            })
            
        return sorted(tag_data, key=lambda x: x['count'], reverse=True)


def main():
    """主函数"""
    memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    viz = MemoryVisualizer(str(memory_dir))
    viz.load_memories()
    viz.calculate_stats()
    
    # 生成文本报告
    report = viz.generate_text_report()
    print(report)
    
    # 保存报告
    report_file = Path.home() / f"memory-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"📄 报告已保存：{report_file}")
    
    # 生成标签云数据
    tag_data = viz.generate_tag_cloud_data()
    print("\n🏷️ 标签云数据:")
    for item in tag_data[:10]:
        print(f"  #{item['tag']} (大小：{item['size']}, 次数：{item['count']})")


if __name__ == "__main__":
    main()
