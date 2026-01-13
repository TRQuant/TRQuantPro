#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库可视化统计仪表板
====================

生成知识库的统计图表和HTML报告
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️  Plotly未安装，将生成文本报告")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def load_knowledge_base():
    """加载知识库"""
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if not kb_file.exists():
        raise FileNotFoundError(f"知识库文件不存在: {kb_file}")
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    return kb.get('items', [])


def analyze_knowledge_base(items):
    """分析知识库"""
    stats = {
        'total': len(items),
        'by_type': Counter(),
        'by_reliability': Counter(),
        'by_source': Counter(),
        'by_knowledge_base': defaultdict(int),
        'quality_metrics': {
            'has_reliability': 0,
            'has_conclusion': 0,
            'has_tags': 0,
            'has_source': 0,
        },
        'content_length': {
            'min': float('inf'),
            'max': 0,
            'avg': 0,
        }
    }
    
    total_length = 0
    
    for item in items:
        # 按类型统计
        kb_type = item.get('type', 'unknown')
        stats['by_type'][kb_type] += 1
        
        # 按可靠性统计
        content = item.get('content', '')
        # 尝试多种匹配模式
        reliability_match = re.search(r'可靠性评级[：:]\s*([ABCD]级)', content)
        if not reliability_match:
            reliability_match = re.search(r'\*\*可靠性评级\*\*[：:]\s*([ABCD]级)', content)
        if not reliability_match:
            reliability_match = re.search(r'可靠性[：:]\s*([ABCD]级)', content)
        if reliability_match:
            reliability = reliability_match.group(1)
            stats['by_reliability'][reliability] += 1
        else:
            # 如果没有找到，标记为未标注
            stats['by_reliability']['未标注'] += 1
        
        # 按来源统计
        source = item.get('source', 'unknown')
        if source:
            stats['by_source'][source[:50]] += 1
        
        # 按知识库分类
        title = item.get('title', '')
        if '聚宽' in title or 'JQData' in title or 'JoinQuant' in title:
            stats['by_knowledge_base']['聚宽/JQData'] += 1
        if 'QMT' in title:
            stats['by_knowledge_base']['QMT'] += 1
        if 'BulletTrade' in title:
            stats['by_knowledge_base']['BulletTrade'] += 1
        if '资金流向' in title or '资金流向' in content:
            stats['by_knowledge_base']['资金流向'] += 1
        if '情绪' in title or '情绪' in content:
            stats['by_knowledge_base']['情绪因子'] += 1
        if '最佳实践' in title:
            stats['by_knowledge_base']['策略开发最佳实践'] += 1
        if '回测' in title or '回测' in content:
            stats['by_knowledge_base']['回测引擎对比'] += 1
        if 'AKShare' in title or 'akshare' in content.lower():
            stats['by_knowledge_base']['AKShare'] += 1
        
        # 质量指标
        if '可靠性评级' in content:
            stats['quality_metrics']['has_reliability'] += 1
        if '## 结论' in content or '### 结论' in content:
            stats['quality_metrics']['has_conclusion'] += 1
        if item.get('tags'):
            stats['quality_metrics']['has_tags'] += 1
        if item.get('source'):
            stats['quality_metrics']['has_source'] += 1
        
        # 内容长度
        content_len = len(content)
        total_length += content_len
        stats['content_length']['min'] = min(stats['content_length']['min'], content_len)
        stats['content_length']['max'] = max(stats['content_length']['max'], content_len)
    
    if stats['total'] > 0:
        stats['content_length']['avg'] = total_length / stats['total']
    
    return stats


def create_html_dashboard(stats, output_file='kb_dashboard.html'):
    """创建HTML仪表板"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TRQuant知识库统计仪表板</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.3s;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 TRQuant知识库统计仪表板</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>总知识条目数</h3>
                <div class="value">{stats['total']}</div>
            </div>
            <div class="stat-card">
                <h3>可靠性标注覆盖率</h3>
                <div class="value">{stats['quality_metrics']['has_reliability']/stats['total']*100:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>结论部分覆盖率</h3>
                <div class="value">{stats['quality_metrics']['has_conclusion']/stats['total']*100:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>平均内容长度</h3>
                <div class="value">{stats['content_length']['avg']:.0f}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 知识库分类统计</h2>
            <table>
                <tr>
                    <th>知识库</th>
                    <th>条目数</th>
                    <th>占比</th>
                    <th>进度</th>
                </tr>
"""
    
    # 知识库统计
    kb_targets = {
        '聚宽/JQData': 200,
        'QMT': 150,
        'BulletTrade': 50,
        '资金流向': 80,
        '情绪因子': 30,
    }
    
    for kb_name, count in sorted(stats['by_knowledge_base'].items(), key=lambda x: x[1], reverse=True):
        target = kb_targets.get(kb_name, 0)
        percentage = count / stats['total'] * 100 if stats['total'] > 0 else 0
        completion = count / target * 100 if target > 0 else 0
        
        html += f"""
                <tr>
                    <td><strong>{kb_name}</strong></td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {min(completion, 100)}%">
                                {completion:.1f}%
                            </div>
                        </div>
                    </td>
                </tr>
"""
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>📊 知识类型分布</h2>
            <table>
                <tr>
                    <th>类型</th>
                    <th>条目数</th>
                    <th>占比</th>
                </tr>
"""
    
    for kb_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / stats['total'] * 100 if stats['total'] > 0 else 0
        html += f"""
                <tr>
                    <td>{kb_type}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>⭐ 可靠性等级分布</h2>
            <table>
                <tr>
                    <th>可靠性等级</th>
                    <th>条目数</th>
                    <th>占比</th>
                </tr>
"""
    
    reliability_labels = {'A级': 'A级（高可靠性）', 'B级': 'B级（中高可靠性）', 'C级': 'C级（中可靠性）', 'D级': 'D级（低可靠性）'}
    for level in ['A级', 'B级', 'C级', 'D级']:
        count = stats['by_reliability'][level]
        percentage = count / stats['total'] * 100 if stats['total'] > 0 else 0
        label = reliability_labels.get(level, level)
        html += f"""
                <tr>
                    <td>{label}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""
    
    html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>✅ 质量指标</h2>
            <table>
                <tr>
                    <th>指标</th>
                    <th>数量</th>
                    <th>覆盖率</th>
                    <th>进度</th>
                </tr>
                <tr>
                    <td>可靠性标注</td>
                    <td>{stats['quality_metrics']['has_reliability']}</td>
                    <td>{stats['quality_metrics']['has_reliability']/stats['total']*100:.1f}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {stats['quality_metrics']['has_reliability']/stats['total']*100:.1f}%">
                                {stats['quality_metrics']['has_reliability']/stats['total']*100:.1f}%
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>结论部分</td>
                    <td>{stats['quality_metrics']['has_conclusion']}</td>
                    <td>{stats['quality_metrics']['has_conclusion']/stats['total']*100:.1f}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {stats['quality_metrics']['has_conclusion']/stats['total']*100:.1f}%">
                                {stats['quality_metrics']['has_conclusion']/stats['total']*100:.1f}%
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>标签</td>
                    <td>{stats['quality_metrics']['has_tags']}</td>
                    <td>{stats['quality_metrics']['has_tags']/stats['total']*100:.1f}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {stats['quality_metrics']['has_tags']/stats['total']*100:.1f}%">
                                {stats['quality_metrics']['has_tags']/stats['total']*100:.1f}%
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>来源</td>
                    <td>{stats['quality_metrics']['has_source']}</td>
                    <td>{stats['quality_metrics']['has_source']/stats['total']*100:.1f}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {stats['quality_metrics']['has_source']/stats['total']*100:.1f}%">
                                {stats['quality_metrics']['has_source']/stats['total']*100:.1f}%
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
        
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>TRQuant知识库统计仪表板</p>
        </div>
    </div>
</body>
</html>
"""
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding='utf-8')
    
    return output_path


def create_plotly_dashboard(stats):
    """使用Plotly创建交互式仪表板"""
    if not PLOTLY_AVAILABLE:
        return None
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('知识库分类统计', '知识类型分布', '可靠性等级分布', '质量指标'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # 1. 知识库分类统计（条形图）
    kb_data = sorted(stats['by_knowledge_base'].items(), key=lambda x: x[1], reverse=True)
    kb_names = [x[0] for x in kb_data]
    kb_counts = [x[1] for x in kb_data]
    
    fig.add_trace(
        go.Bar(x=kb_names, y=kb_counts, name='知识库', marker_color='#667eea'),
        row=1, col=1
    )
    
    # 2. 知识类型分布（饼图）
    type_data = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)
    type_names = [x[0] for x in type_data]
    type_counts = [x[1] for x in type_data]
    
    fig.add_trace(
        go.Pie(labels=type_names, values=type_counts, name='类型分布'),
        row=1, col=2
    )
    
    # 3. 可靠性等级分布（条形图）
    reliability_order = ['A级', 'B级', 'C级', 'D级']
    reliability_counts = [stats['by_reliability'][level] for level in reliability_order]
    reliability_labels = ['A级（高可靠性）', 'B级（中高可靠性）', 'C级（中可靠性）', 'D级（低可靠性）']
    
    fig.add_trace(
        go.Bar(x=reliability_labels, y=reliability_counts, name='可靠性', marker_color='#764ba2'),
        row=2, col=1
    )
    
    # 4. 质量指标（条形图）
    quality_metrics = ['可靠性标注', '结论部分', '标签', '来源']
    quality_counts = [
        stats['quality_metrics']['has_reliability'],
        stats['quality_metrics']['has_conclusion'],
        stats['quality_metrics']['has_tags'],
        stats['quality_metrics']['has_source']
    ]
    quality_percentages = [c / stats['total'] * 100 for c in quality_counts]
    
    fig.add_trace(
        go.Bar(x=quality_metrics, y=quality_percentages, name='覆盖率', marker_color='#f093fb'),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title_text='TRQuant知识库统计仪表板',
        height=1000,
        showlegend=False
    )
    
    return fig


def main():
    """主函数"""
    print("=" * 70)
    print("📊 创建知识库可视化统计仪表板")
    print("=" * 70)
    print()
    
    # 加载知识库
    print("📖 加载知识库...")
    items = load_knowledge_base()
    print(f"   ✅ 加载完成: {len(items)} 条知识条目")
    print()
    
    # 分析知识库
    print("🔍 分析知识库...")
    stats = analyze_knowledge_base(items)
    print("   ✅ 分析完成")
    print()
    
    # 创建HTML仪表板
    print("📝 生成HTML仪表板...")
    html_path = create_html_dashboard(stats, 'docs/knowledge_base/kb_dashboard.html')
    print(f"   ✅ HTML仪表板已生成: {html_path}")
    print()
    
    # 创建Plotly交互式图表
    if PLOTLY_AVAILABLE:
        print("📊 生成Plotly交互式图表...")
        fig = create_plotly_dashboard(stats)
        if fig:
            plotly_path = Path('docs/knowledge_base/kb_dashboard_plotly.html')
            fig.write_html(str(plotly_path))
            print(f"   ✅ Plotly图表已生成: {plotly_path}")
        print()
    
    # 打印统计摘要
    print("=" * 70)
    print("📊 统计摘要")
    print("=" * 70)
    print()
    print(f"总知识条目数: {stats['total']}条")
    print()
    print("知识库分类:")
    for kb_name, count in sorted(stats['by_knowledge_base'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  - {kb_name}: {count}条 ({percentage:.1f}%)")
    print()
    print("可靠性等级分布:")
    for level in ['A级', 'B级', 'C级', 'D级']:
        count = stats['by_reliability'][level]
        percentage = count / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  - {level}: {count}条 ({percentage:.1f}%)")
    print()
    print("质量指标:")
    print(f"  - 可靠性标注: {stats['quality_metrics']['has_reliability']}条 ({stats['quality_metrics']['has_reliability']/stats['total']*100:.1f}%)")
    print(f"  - 结论部分: {stats['quality_metrics']['has_conclusion']}条 ({stats['quality_metrics']['has_conclusion']/stats['total']*100:.1f}%)")
    print()
    print("=" * 70)
    print("✅ 仪表板生成完成！")
    print("=" * 70)
    print()
    print(f"📝 HTML仪表板: {html_path}")
    if PLOTLY_AVAILABLE:
        print(f"📊 Plotly图表: docs/knowledge_base/kb_dashboard_plotly.html")
    print()


if __name__ == '__main__':
    main()
