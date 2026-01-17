#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十倍股增强版报告生成脚本
参考 TENBAGGER_REPORT_ENHANCED.html 的样式和结构
使用账号 13327806797，基于最近三个月数据生成增强版报告
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, date
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入必要的模块
import jqdatasdk as jq
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

print("=" * 80)
print("十倍股增强版报告生成 - 使用账号 13327806797")
print("=" * 80)
print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 账号配置
username = "13327806797"
password = "Taorui888"

# 计算最近三个月的日期范围
end_date = date.today()
start_date = end_date - timedelta(days=90)  # 最近3个月

print(f"数据时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
print()

# 1. 认证JQData
print("【步骤1】JQData账号认证")
print("-" * 80)
try:
    jq.auth(username, password)
    print("✅ 认证成功")
    
    # 获取账号信息
    account_info = jq.get_account_info()
    account_type = "正式账户" if account_info.get('query_count_limit', 0) >= 200000000 else "试用账户"
    print(f"账号类型: {account_type}")
    print(f"有效期: {account_info.get('expire_time', 'N/A')}")
    print(f"数据范围: {account_info.get('date_range_start', 'N/A')} 至 {account_info.get('date_range_end', 'N/A')}")
    print()
except Exception as e:
    print(f"❌ 认证失败: {e}")
    sys.exit(1)

# 2. 获取十倍股排名数据
print("【步骤2】获取十倍股排名数据")
print("-" * 80)

rankings_data = []
try:
    from extension.python.bridge import call_tenbagger_tool
    
    # 从数据库获取排名
    db_result = call_tenbagger_tool('tenbagger.db_rankings', {
        'top_n': 50,
        'min_score': 50
    })
    
    if db_result.get('ok'):
        rankings = db_result.get('data', {}).get('rankings', [])
        print(f"✅ 从数据库获取到 {len(rankings)} 只股票")
        
        # 获取股票名称
        for rank in rankings:
            symbol = rank.get('symbol', rank.get('code', rank.get('security_id', '')))
            if symbol:
                try:
                    stock_info = jq.get_security_info(symbol)
                    if stock_info:
                        name = stock_info.display_name if hasattr(stock_info, 'display_name') else stock_info.name
                    else:
                        name = symbol
                except:
                    name = rank.get('name', rank.get('stock_name', symbol))
                
                rankings_data.append({
                    "symbol": symbol,
                    "name": name,
                    "score": rank.get('tenbagger_score', rank.get('total_score', rank.get('score', 0))),
                    "stage": rank.get('stage', rank.get('current_stage', 'S0')),
                    "level": rank.get('eval_level', rank.get('level', 'C')),
                    "scorecard_score": rank.get('scorecard_score', 0),
                    "mainline": rank.get('mainline', '未知')
                })
    else:
        print(f"⚠️ 数据库获取失败: {db_result.get('error', '未知错误')}")
except Exception as e:
    print(f"⚠️ 获取排名失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 获取统计信息
print("【步骤3】获取统计信息")
print("-" * 80)

stats_data = {}
try:
    stats_result = call_tenbagger_tool('tenbagger.stats', {})
    if stats_result.get('ok'):
        stats_data = stats_result.get('data', {})
        print(f"✅ 获取统计成功")
        print(f"  总评估数: {stats_data.get('total_evaluated', 0)}")
        print(f"  等级分布: {stats_data.get('by_grade', {})}")
        print(f"  阶段分布: {stats_data.get('by_stage', {})}")
    else:
        print(f"⚠️ 获取统计失败: {stats_result.get('error', '未知错误')}")
except Exception as e:
    print(f"⚠️ 获取统计失败: {e}")

print()

# 4. 生成增强版HTML报告（参考TENBAGGER_REPORT_ENHANCED.html的样式）
print("【步骤4】生成增强版HTML报告")
print("-" * 80)

# 排序排名数据
rankings_data.sort(key=lambda x: x['score'], reverse=True)
recommended = [r for r in rankings_data if r['score'] >= 50.0]

# 统计信息
level_count = {}
stage_count = {}
for r in recommended:
    level_count[r['level']] = level_count.get(r['level'], 0) + 1
    stage_count[r['stage']] = stage_count.get(r['stage'], 0) + 1

stage_names = {
    "S0": "观察期", 
    "S1": "验证期", 
    "S2": "导入期，最佳介入点", 
    "S3": "放量期", 
    "S4": "加速期", 
    "S5": "成熟期"
}

# 生成HTML报告（参考TENBAGGER_REPORT_ENHANCED.html的样式）
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股早期识别系统 - 增强版分析报告</title>
    <!-- Prism.js 代码高亮 -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <!-- Chart.js 图表库 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        /* Apple Design System - 高对比度配色 */
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f5f5f7;
            --bg-tertiary: #e8e8ed;
            --text-primary: #1d1d1f;
            --text-secondary: #6e6e73;
            --text-tertiary: #86868b;
            --accent-blue: #0071e3;
            --accent-green: #34c759;
            --accent-red: #ff3b30;
            --accent-orange: #ff9500;
            --accent-purple: #af52de;
            --accent-teal: #5ac8fa;
            --border: #d2d2d7;
            --code-bg: #1d1d1f;
            --code-text: #f5f5f7;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --shadow-lg: 0 12px 40px rgba(0,0,0,0.12);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 20px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-secondary);
            color: var(--text-primary);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* 容器 */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 24px;
        }}

        /* 头部 */
        .hero {{
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            padding: 80px 40px;
            text-align: center;
            margin-bottom: 32px;
            box-shadow: var(--shadow-md);
        }}

        .hero-badge {{
            display: inline-block;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
        }}

        .hero h1 {{
            font-size: 56px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 16px;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 24px;
            color: var(--text-secondary);
            max-width: 700px;
            margin: 0 auto 24px;
        }}

        .hero-meta {{
            font-size: 14px;
            color: var(--text-tertiary);
        }}

        /* 导航标签 */
        .nav-tabs {{
            display: flex;
            gap: 8px;
            background: var(--bg-primary);
            padding: 12px;
            border-radius: var(--radius-lg);
            margin-bottom: 32px;
            box-shadow: var(--shadow-md);
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}

        .nav-tabs::-webkit-scrollbar {{ height: 0; }}

        .nav-tab {{
            padding: 14px 24px;
            border: none;
            background: transparent;
            font-size: 15px;
            font-weight: 500;
            color: var(--text-secondary);
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .nav-tab:hover {{
            background: var(--bg-secondary);
            color: var(--text-primary);
        }}

        .nav-tab.active {{
            background: var(--accent-blue);
            color: white;
        }}

        /* 内容面板 */
        .panel {{
            display: none;
            animation: fadeIn 0.4s ease;
        }}

        .panel.active {{ display: block; }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(16px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* 卡片 */
        .card {{
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            padding: 40px;
            margin-bottom: 32px;
            box-shadow: var(--shadow-md);
        }}

        .card-header {{
            margin-bottom: 32px;
        }}

        .card-title {{
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}

        .card-subtitle {{
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
            margin: 32px 0 20px;
        }}

        /* 统计网格 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }}

        .stat-card {{
            background: var(--bg-secondary);
            padding: 24px;
            border-radius: var(--radius-md);
            text-align: center;
        }}

        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}

        .stat-value.blue {{ color: var(--accent-blue); }}
        .stat-value.green {{ color: var(--accent-green); }}
        .stat-value.orange {{ color: var(--accent-orange); }}
        .stat-value.red {{ color: var(--accent-red); }}
        .stat-value.purple {{ color: var(--accent-purple); }}

        .stat-label {{
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
        }}

        /* 表格 */
        .table-container {{
            overflow-x: auto;
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            margin: 24px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}

        th {{
            background: var(--bg-secondary);
            padding: 16px 20px;
            text-align: left;
            font-weight: 600;
            color: var(--text-primary);
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }}

        td {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--bg-tertiary);
            color: var(--text-primary);
        }}

        tr:last-child td {{ border-bottom: none; }}
        tr:hover {{ background: var(--bg-secondary); }}

        .positive {{ color: var(--accent-green); font-weight: 600; }}
        .negative {{ color: var(--accent-red); font-weight: 600; }}

        /* 标签 */
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}

        .badge-s-plus {{ background: #fef3c7; color: #92400e; }}
        .badge-s {{ background: #dcfce7; color: #166534; }}
        .badge-a {{ background: #dbeafe; color: #1e40af; }}
        .badge-b {{ background: #e0e7ff; color: #3730a3; }}
        .badge-c {{ background: #f3f4f6; color: #374151; }}
        .badge-s0 {{ background: #f3f4f6; color: #6b7280; }}
        .badge-s1 {{ background: #fef3c7; color: #92400e; }}
        .badge-s2 {{ background: #dcfce7; color: #166534; }}
        .badge-s3 {{ background: #fee2e2; color: #991b1b; }}

        /* 提示框 */
        .alert {{
            padding: 20px 24px;
            border-radius: var(--radius-md);
            margin: 24px 0;
            display: flex;
            align-items: flex-start;
            gap: 16px;
        }}

        .alert-info {{
            background: #eff6ff;
            border-left: 4px solid var(--accent-blue);
        }}

        .alert-success {{
            background: #f0fdf4;
            border-left: 4px solid var(--accent-green);
        }}

        .alert-warning {{
            background: #fffbeb;
            border-left: 4px solid var(--accent-orange);
        }}

        .alert-icon {{ font-size: 24px; }}
        .alert-content {{ flex: 1; }}
        .alert-title {{ font-weight: 600; margin-bottom: 4px; }}

        /* 三轴网格 */
        .axis-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 24px 0;
        }}

        @media (max-width: 900px) {{
            .axis-grid {{ grid-template-columns: 1fr; }}
        }}

        .axis-card {{
            background: var(--bg-secondary);
            padding: 24px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--accent-blue);
        }}

        .axis-card h4 {{
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}

        .axis-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid var(--bg-tertiary);
            font-size: 14px;
        }}

        .axis-item:last-child {{ border-bottom: none; }}
        .axis-label {{ color: var(--text-secondary); }}
        .axis-value {{ font-weight: 600; }}

        /* 响应式 */
        @media (max-width: 768px) {{
            .hero {{ padding: 48px 24px; }}
            .hero h1 {{ font-size: 36px; }}
            .hero p {{ font-size: 18px; }}
            .card {{ padding: 24px; }}
            .card-title {{ font-size: 24px; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .stat-value {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="hero">
            <div class="hero-badge">十倍股早期识别系统 V2.0</div>
            <h1>十倍股增强版分析报告</h1>
            <p>基于JQData数据源，使用账号 {username} ({account_type})</p>
            <div class="hero-meta">
                数据时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} | 
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                数据来源：JQData量化数据库 + MongoDB
            </div>
        </div>

        <!-- 导航标签 -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showPanel('overview')">📊 概览</button>
            <button class="nav-tab" onclick="showPanel('rankings')">🏆 排名</button>
            <button class="nav-tab" onclick="showPanel('stages')">🔄 阶段分析</button>
            <button class="nav-tab" onclick="showPanel('strategy')">📈 策略框架</button>
        </div>

        <!-- 概览面板 -->
        <div id="overview" class="panel active">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">执行摘要</h2>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value blue">{len(rankings_data)}</div>
                        <div class="stat-label">评估股票数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value green">{len(recommended)}</div>
                        <div class="stat-label">推荐股票数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value orange">{len([r for r in recommended if r['stage'] == 'S2'])}</div>
                        <div class="stat-label">S2阶段（最佳介入）</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value purple">{max([r['score'] for r in recommended] + [0]):.1f}</div>
                        <div class="stat-label">最高得分</div>
                    </div>
                </div>

                <h3 class="card-subtitle">统计信息</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>等级分布</h4>
                        {''.join([f'<div class="axis-item"><span class="axis-label">{k}级</span><span class="axis-value">{v}只</span></div>' for k, v in sorted(level_count.items(), reverse=True)]) if level_count else '<div class="axis-item"><span class="axis-label">无数据</span></div>'}
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>阶段分布</h4>
                        {''.join([f'<div class="axis-item"><span class="axis-label">{k}阶段</span><span class="axis-value">{v}只</span></div>' for k, v in sorted(stage_count.items())]) if stage_count else '<div class="axis-item"><span class="axis-label">无数据</span></div>'}
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>数据质量</h4>
                        <div class="axis-item"><span class="axis-label">数据来源</span><span class="axis-value">JQData + MongoDB</span></div>
                        <div class="axis-item"><span class="axis-label">账号类型</span><span class="axis-value">{account_type}</span></div>
                        <div class="axis-item"><span class="axis-label">数据范围</span><span class="axis-value">{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}</span></div>
                        <div class="axis-item"><span class="axis-label">平均得分</span><span class="axis-value">{f"{sum([r['score'] for r in recommended]) / len(recommended):.1f}" if recommended and len(recommended) > 0 else "0.0"}</span></div>
                    </div>
                </div>

                <div class="alert alert-info">
                    <span class="alert-icon">📊</span>
                    <div class="alert-content">
                        <div class="alert-title">数据来源说明</div>
                        <div>
                            <strong>识别数据：</strong>JQData账号 {username} ({account_type})<br>
                            <strong>数据时间范围：</strong>{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}（最近3个月）<br>
                            <strong>评估系统：</strong>TRQuant十倍股早期识别系统 V2.0<br>
                            <strong>数据存储：</strong>MongoDB数据库
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 排名面板 -->
        <div id="rankings" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股排名列表</h2>
                </div>

                <h3 class="card-subtitle">Top {min(20, len(recommended))} 推荐股票</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>排名</th>
                                <th>代码</th>
                                <th>名称</th>
                                <th>阶段</th>
                                <th>等级</th>
                                <th>得分</th>
                                <th>评分卡</th>
                                <th>投资主线</th>
                            </tr>
                        </thead>
                        <tbody>
"""

for i, stock in enumerate(recommended[:20], 1):
    score_class = "positive" if stock['score'] >= 70 else ("positive" if stock['score'] >= 60 else "")
    html_content += f"""
                            <tr>
                                <td>{i}</td>
                                <td>{stock['symbol']}</td>
                                <td><strong>{stock['name']}</strong></td>
                                <td><span class="badge badge-{stock['stage'].lower()}">{stock['stage']}</span></td>
                                <td><span class="badge badge-{stock['level'].lower()}">{stock['level']}</span></td>
                                <td class="{score_class}">{stock['score']:.1f}</td>
                                <td>{stock['scorecard_score']:.1f}</td>
                                <td>{stock['mainline']}</td>
                            </tr>
"""

html_content += """
                        </tbody>
                    </table>
                </div>

                <div class="alert alert-success">
                    <span class="alert-icon">💡</span>
                    <div class="alert-content">
                        <div class="alert-title">投资建议</div>
                        <div>
                            <strong>重点关注S2阶段股票：</strong>S2阶段是十倍股的最佳介入期，推荐重点关注以下股票：<br>
                            {', '.join([f"{s['name']}({s['symbol']})" for s in recommended if s['stage'] == 'S2'][:5]) if [s for s in recommended if s['stage'] == 'S2'] else '暂无S2阶段股票'}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 阶段分析面板 -->
        <div id="stages" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股成长阶段分析</h2>
                </div>
                
                <div class="alert alert-info">
                    <span class="alert-icon">🔄</span>
                    <div class="alert-content">
                        <div class="alert-title">三轴阶段判定体系</div>
                        <div>基本面轴（Fundamental）+ 资金轴（Flow）+ 预期轴（Expectation）综合判定</div>
                    </div>
                </div>

                <h3 class="card-subtitle">阶段分布统计</h3>
                <div class="stats-grid">
"""

for stage, count in sorted(stage_count.items()):
    stage_desc = stage_names.get(stage, stage)
    html_content += f"""
                    <div class="stat-card">
                        <div class="stat-value blue">{count}</div>
                        <div class="stat-label">{stage}阶段<br><small>{stage_desc}</small></div>
                    </div>
"""

html_content += """
                </div>

                <h3 class="card-subtitle">阶段说明</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>S0 - 观察期</h4>
                        <div class="axis-item"><span class="axis-label">特征</span><span class="axis-value">无明显增长信号</span></div>
                        <div class="axis-item"><span class="axis-label">建议</span><span class="axis-value">排除或等待</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>S1 - 验证期</h4>
                        <div class="axis-item"><span class="axis-label">特征</span><span class="axis-value">早期信号出现</span></div>
                        <div class="axis-item"><span class="axis-label">建议</span><span class="axis-value">小仓位试错</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>S2 - 导入期（最佳介入点）</h4>
                        <div class="axis-item"><span class="axis-label">特征</span><span class="axis-value">增长确认，资金流入</span></div>
                        <div class="axis-item"><span class="axis-label">建议</span><span class="axis-value">重点配置</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-red);">
                        <h4>S3 - 放量期</h4>
                        <div class="axis-item"><span class="axis-label">特征</span><span class="axis-value">加速上涨，关注估值</span></div>
                        <div class="axis-item"><span class="axis-label">建议</span><span class="axis-value">谨慎持有</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 策略框架面板 -->
        <div id="strategy" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股策略框架</h2>
                </div>

                <h3 class="card-subtitle">十倍股作战清单</h3>
                <div class="stats-grid">
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-blue); margin-bottom: 12px;">【选股 Select】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">
                            ✓ 景气度明确<br>
                            ✓ 利润增长持续<br>
                            ✓ ROE/毛利率/现金流过关<br>
                            ✓ 研发与治理扎实
                        </div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-green); margin-bottom: 12px;">【买入 Buy】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">
                            ✓ 突破放量<br>
                            ✓ 相对强势<br>
                            ✓ 市场环境配合<br>
                            ✓ S2导入期信号确认
                        </div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-orange); margin-bottom: 12px;">【持有 Hold】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">
                            ✓ 让利润奔跑<br>
                            ✓ 只给赢家加仓<br>
                            ✓ 不摊平亏损<br>
                            ✓ 趋势线守仓
                        </div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-red); margin-bottom: 12px;">【卖出 Sell】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">
                            ✓ -7%~-8%无条件止损<br>
                            ✓ 高位加速警惕高潮顶<br>
                            ✓ 分批止盈+移动止损<br>
                            ✓ 大盘分配日降低仓位
                        </div>
                    </div>
                </div>

                <h3 class="card-subtitle">风险提示</h3>
                <div class="alert alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-content">
                        <div class="alert-title">重要提示</div>
                        <div>
                            <strong>阶段风险：</strong>S3阶段股票已进入放量期，需关注估值水平<br>
                            <strong>行业风险：</strong>关注政策变化和行业周期<br>
                            <strong>个股风险：</strong>建议结合基本面和技术面综合分析<br>
                            <strong>数据风险：</strong>本评估基于历史数据，不构成投资建议
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showPanel(panelId) {{
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""

# 保存报告
report_dir = project_root / "reports"
report_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = report_dir / f"tenbagger_enhanced_report_{username}_{timestamp}.html"

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 增强版报告已生成: {report_file}")
print(f"   - 评估股票: {len(rankings_data)}只")
print(f"   - 推荐股票: {len(recommended)}只")
if recommended:
    print(f"   - TOP 5: {', '.join([s['name'] for s in recommended[:5]])}")
    print(f"   - S2阶段（最佳介入）: {len([s for s in recommended if s['stage'] == 'S2'])}只")

print("\n" + "=" * 80)
print("✅ 十倍股增强版报告生成完成！")
print("=" * 80)

