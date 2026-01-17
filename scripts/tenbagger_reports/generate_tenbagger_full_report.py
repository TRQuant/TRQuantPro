#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十倍股完整版增强报告生成脚本 (8标签页)
参考 TENBAGGER_REPORT_ENHANCED.html 的完整结构

【生成方法记录】
1. 数据来源：
   - JQData量化数据库：基本面数据、财务数据、估值数据
   - MongoDB数据库：十倍股评估结果、阶段分析、评分卡
   - AKShare：实时行情数据（可选）

2. 8个标签页结构：
   - 概览统计(overview)：核心统计、行业分布、关键发现
   - 十大案例(cases)：经典案例分析、共性总结
   - 阶段分析(stages)：三轴阶段判定体系
   - 因子体系(factors)：100分制评分体系
   - 识别代码(code)：JQData实现代码
   - 实战识别(realdata)：实际识别结果
   - 验证结果(validation)：体系有效性验证
   - 策略框架(strategy)：作战清单和卖出规则

3. 设计风格：Apple Design System
   - 亮色主题、高对比度配色
   - 渐变、阴影、圆角
   - 响应式布局

4. 使用方法：
   python scripts/generate_tenbagger_full_report.py

5. 输出：reports/tenbagger_full_report_YYYYMMDD_HHMMSS.html
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, date
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入必要的模块
import jqdatasdk as jq
from config.config_manager import get_config_manager

print("=" * 80)
print("🏆 十倍股完整版增强报告生成 (8标签页)")
print("=" * 80)
print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 账号配置
username = "13327806797"
password = "Taorui888"

# 计算最近三个月的日期范围
end_date = date.today()
start_date = end_date - timedelta(days=90)

print(f"数据时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
print()

# 1. 认证JQData
print("【步骤1】JQData账号认证")
print("-" * 80)
try:
    jq.auth(username, password)
    print("✅ 认证成功")
    
    account_info = jq.get_account_info()
    account_type = "正式账户" if account_info.get('query_count_limit', 0) >= 200000000 else "试用账户"
    expire_time = account_info.get('expire_time', 'N/A')
    date_range_start = account_info.get('date_range_start', 'N/A')
    date_range_end = account_info.get('date_range_end', 'N/A')
    
    print(f"账号类型: {account_type}")
    print(f"有效期: {expire_time}")
    print(f"数据范围: {date_range_start} 至 {date_range_end}")
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
    
    db_result = call_tenbagger_tool('tenbagger.db_rankings', {
        'top_n': 100,
        'min_score': 40
    })
    
    if db_result.get('ok'):
        rankings = db_result.get('data', {}).get('rankings', [])
        print(f"✅ 从数据库获取到 {len(rankings)} 只股票")
        
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
                
                # 获取财务数据
                fundamentals = {}
                try:
                    q = jq.query(
                        jq.valuation,
                        jq.indicator
                    ).filter(
                        jq.valuation.code == symbol
                    )
                    df = jq.get_fundamentals(q, date=end_date)
                    if not df.empty:
                        fundamentals = {
                            'pe': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else None,
                            'pb': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else None,
                            'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else None,
                            'roe': df['roe'].iloc[0] if 'roe' in df.columns else None,
                            'roa': df['roa'].iloc[0] if 'roa' in df.columns else None,
                            'gross_profit_margin': df['gross_profit_margin'].iloc[0] if 'gross_profit_margin' in df.columns else None,
                        }
                except:
                    pass
                
                rankings_data.append({
                    "symbol": symbol,
                    "name": name,
                    "score": rank.get('tenbagger_score', rank.get('total_score', rank.get('score', 0))),
                    "stage": rank.get('stage', rank.get('current_stage', 'S0')),
                    "level": rank.get('eval_level', rank.get('level', 'C')),
                    "scorecard_score": rank.get('scorecard_score', 0),
                    "mainline": rank.get('mainline', '未知'),
                    "fundamentals": fundamentals,
                    "industry": rank.get('industry', ''),
                    "growth_score": rank.get('growth_score', 0),
                    "momentum_score": rank.get('momentum_score', 0),
                    "risk_score": rank.get('risk_score', 0),
                })
    else:
        print(f"⚠️ 数据库获取失败: {db_result.get('error', '未知错误')}")
except Exception as e:
    print(f"⚠️ 获取排名失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 获取统计信息
print("\n【步骤3】获取统计信息")
print("-" * 80)

# 排序排名数据
rankings_data.sort(key=lambda x: x['score'], reverse=True)
recommended = [r for r in rankings_data if r['score'] >= 50.0]

# 统计信息
level_count = {}
stage_count = {}
industry_count = {}

for r in rankings_data:
    level_count[r['level']] = level_count.get(r['level'], 0) + 1
    stage_count[r['stage']] = stage_count.get(r['stage'], 0) + 1
    if r.get('industry'):
        industry_count[r['industry']] = industry_count.get(r['industry'], 0) + 1

# 统计S级以上
s_level_stocks = [r for r in rankings_data if r['level'] in ['S+', 'S', 'A']]
s2_stocks = [r for r in rankings_data if r['stage'] == 'S2']

print(f"✅ 统计完成")
print(f"  评估股票: {len(rankings_data)}只")
print(f"  推荐股票: {len(recommended)}只")
print(f"  S2阶段: {len(s2_stocks)}只")
print(f"  等级分布: {level_count}")
print(f"  阶段分布: {stage_count}")
print()

# 4. 十大经典案例（历史十倍股数据）
print("【步骤4】准备十大经典案例数据")
print("-" * 80)

classic_cases = [
    {"code": "600519.XSHG", "name": "贵州茅台", "return": "100x", "industry": "白酒", "period": "2001-2021", "catalyst": "消费升级+品牌效应"},
    {"code": "300750.XSHE", "name": "宁德时代", "return": "15x", "industry": "新能源", "period": "2018-2021", "catalyst": "新能源车渗透率提升"},
    {"code": "600276.XSHG", "name": "恒瑞医药", "return": "50x", "industry": "医药", "period": "2000-2021", "catalyst": "创新药+医保扩容"},
    {"code": "002475.XSHE", "name": "立讯精密", "return": "30x", "industry": "电子", "period": "2010-2021", "catalyst": "苹果产业链+消费电子"},
    {"code": "601012.XSHG", "name": "隆基绿能", "return": "20x", "industry": "光伏", "period": "2014-2021", "catalyst": "光伏平价+技术领先"},
    {"code": "002594.XSHE", "name": "比亚迪", "return": "15x", "industry": "新能源车", "period": "2019-2022", "catalyst": "刀片电池+整车放量"},
    {"code": "000858.XSHE", "name": "五粮液", "return": "80x", "industry": "白酒", "period": "2001-2021", "catalyst": "高端白酒需求增长"},
    {"code": "000333.XSHE", "name": "美的集团", "return": "30x", "industry": "家电", "period": "2013-2021", "catalyst": "效率提升+全球化"},
    {"code": "002352.XSHE", "name": "顺丰控股", "return": "10x", "industry": "物流", "period": "2017-2021", "catalyst": "电商物流+时效优势"},
    {"code": "300015.XSHE", "name": "爱尔眼科", "return": "50x", "industry": "医疗服务", "period": "2009-2021", "catalyst": "眼科连锁扩张"},
]

print(f"✅ 已准备 {len(classic_cases)} 个经典案例")

# 5. 生成完整HTML报告
print("\n【步骤5】生成完整版HTML报告 (8标签页)")
print("-" * 80)

generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 获取行业分布TOP10
industry_top10 = sorted(industry_count.items(), key=lambda x: x[1], reverse=True)[:10]

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股早期识别系统 - 完整版增强报告</title>
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
        }}

        .container {{ max-width: 1400px; margin: 0 auto; padding: 40px 24px; }}

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
        }}

        .hero h1 {{
            font-size: 48px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 16px;
            letter-spacing: -0.03em;
        }}

        .hero p {{ font-size: 22px; color: var(--text-secondary); max-width: 700px; margin: 0 auto 24px; }}
        .hero-meta {{ font-size: 14px; color: var(--text-tertiary); }}

        /* 导航标签 */
        .nav-tabs {{
            display: flex; gap: 8px; background: var(--bg-primary); padding: 12px;
            border-radius: var(--radius-lg); margin-bottom: 32px; box-shadow: var(--shadow-md);
            overflow-x: auto; flex-wrap: wrap;
        }}

        .nav-tab {{
            padding: 14px 24px; border: none; background: transparent;
            font-size: 15px; font-weight: 500; color: var(--text-secondary);
            border-radius: var(--radius-sm); cursor: pointer; transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .nav-tab:hover {{ background: var(--bg-secondary); color: var(--text-primary); }}
        .nav-tab.active {{ background: var(--accent-blue); color: white; }}

        /* 内容面板 */
        .panel {{ display: none; animation: fadeIn 0.4s ease; }}
        .panel.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        /* 卡片 */
        .card {{
            background: var(--bg-primary); border-radius: var(--radius-lg);
            padding: 40px; margin-bottom: 24px; box-shadow: var(--shadow-md);
        }}

        .card-title {{ font-size: 32px; font-weight: 700; color: var(--text-primary); margin-bottom: 24px; }}
        .card-subtitle {{ font-size: 20px; font-weight: 600; color: var(--text-primary); margin: 32px 0 20px; padding-bottom: 12px; border-bottom: 2px solid var(--bg-tertiary); }}

        /* 统计网格 */
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 24px 0; }}

        .stat-card {{
            background: var(--bg-secondary); padding: 24px; border-radius: var(--radius-md);
            text-align: center; transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-4px); }}

        .stat-value {{ font-size: 36px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }}
        .stat-value.blue {{ color: var(--accent-blue); }}
        .stat-value.green {{ color: var(--accent-green); }}
        .stat-value.orange {{ color: var(--accent-orange); }}
        .stat-value.red {{ color: var(--accent-red); }}
        .stat-value.purple {{ color: var(--accent-purple); }}
        .stat-label {{ font-size: 14px; font-weight: 500; color: var(--text-secondary); }}

        /* 表格 */
        .table-container {{ overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--border); margin: 24px 0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ background: var(--bg-secondary); padding: 16px 20px; text-align: left; font-weight: 600; color: var(--text-primary); border-bottom: 1px solid var(--border); }}
        td {{ padding: 16px 20px; border-bottom: 1px solid var(--bg-tertiary); color: var(--text-primary); }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover {{ background: var(--bg-secondary); }}

        .positive {{ color: var(--accent-green); font-weight: 600; }}
        .negative {{ color: var(--accent-red); font-weight: 600; }}

        /* 标签 */
        .badge {{ display: inline-block; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }}
        .badge-s-plus {{ background: #fef3c7; color: #92400e; }}
        .badge-s {{ background: #dcfce7; color: #166534; }}
        .badge-a {{ background: #dbeafe; color: #1e40af; }}
        .badge-b {{ background: #e0e7ff; color: #3730a3; }}
        .badge-c {{ background: #f3f4f6; color: #374151; }}
        .badge-d {{ background: #fee2e2; color: #991b1b; }}
        .badge-s0 {{ background: #f3f4f6; color: #6b7280; }}
        .badge-s1 {{ background: #fef3c7; color: #92400e; }}
        .badge-s2 {{ background: #dcfce7; color: #166534; }}
        .badge-s3 {{ background: #fee2e2; color: #991b1b; }}

        /* 案例卡片 */
        .case-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin: 24px 0; }}
        @media (max-width: 900px) {{ .case-grid {{ grid-template-columns: 1fr; }} }}

        .case-card {{
            background: var(--bg-secondary); border-radius: var(--radius-md); padding: 24px;
            border-left: 4px solid var(--accent-blue); transition: transform 0.2s, box-shadow 0.2s;
        }}
        .case-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-md); }}
        .case-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }}
        .case-title {{ font-size: 18px; font-weight: 600; color: var(--text-primary); }}
        .case-code {{ font-size: 13px; color: var(--text-tertiary); font-family: monospace; }}
        .case-multiplier {{ font-size: 24px; font-weight: 700; color: var(--accent-green); }}
        .case-meta {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px; }}
        .case-meta-item {{ display: flex; justify-content: space-between; font-size: 14px; }}
        .case-meta-label {{ color: var(--text-secondary); }}
        .case-meta-value {{ font-weight: 600; color: var(--text-primary); }}

        /* 提示框 */
        .alert {{ padding: 20px 24px; border-radius: var(--radius-md); margin: 24px 0; display: flex; align-items: flex-start; gap: 16px; }}
        .alert-info {{ background: #eff6ff; border-left: 4px solid var(--accent-blue); }}
        .alert-success {{ background: #f0fdf4; border-left: 4px solid var(--accent-green); }}
        .alert-warning {{ background: #fffbeb; border-left: 4px solid var(--accent-orange); }}
        .alert-icon {{ font-size: 24px; }}
        .alert-content {{ flex: 1; }}
        .alert-title {{ font-weight: 600; margin-bottom: 4px; }}

        /* 三轴网格 */
        .axis-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 24px 0; }}
        .axis-card {{ background: var(--bg-secondary); padding: 24px; border-radius: var(--radius-md); border-left: 4px solid var(--accent-blue); }}
        .axis-card h4 {{ font-size: 17px; font-weight: 600; margin-bottom: 16px; color: var(--text-primary); }}
        .axis-item {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--bg-tertiary); font-size: 14px; }}
        .axis-item:last-child {{ border-bottom: none; }}
        .axis-label {{ color: var(--text-secondary); }}
        .axis-value {{ font-weight: 600; }}

        /* 代码块 */
        .code-block {{
            background: #1e1e1e; color: #d4d4d4; padding: 24px; border-radius: var(--radius-md);
            overflow-x: auto; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            font-size: 13px; line-height: 1.7; margin: 24px 0; position: relative;
        }}
        .code-block::before {{
            content: attr(data-lang); position: absolute; top: 12px; right: 16px;
            font-size: 11px; color: #6e6e73; text-transform: uppercase; letter-spacing: 1px;
        }}

        /* 时间线 */
        .timeline {{ position: relative; padding-left: 48px; margin: 32px 0; }}
        .timeline::before {{ content: ''; position: absolute; left: 20px; top: 0; bottom: 0; width: 2px; background: var(--border); }}
        .timeline-item {{ position: relative; padding: 28px; background: var(--bg-secondary); border-radius: var(--radius-md); margin-bottom: 24px; }}
        .timeline-item::before {{
            content: ''; position: absolute; left: -36px; top: 32px; width: 14px; height: 14px;
            border-radius: 50%; background: var(--accent-blue); border: 3px solid var(--bg-primary); box-shadow: var(--shadow-sm);
        }}
        .timeline-item.s0::before {{ background: #9ca3af; }}
        .timeline-item.s1::before {{ background: #f59e0b; }}
        .timeline-item.s2::before {{ background: #10b981; }}
        .timeline-item.s3::before {{ background: #ef4444; }}

        /* 响应式 */
        @media (max-width: 768px) {{
            .hero {{ padding: 48px 24px; }}
            .hero h1 {{ font-size: 32px; }}
            .hero p {{ font-size: 18px; }}
            .card {{ padding: 24px; }}
            .card-title {{ font-size: 24px; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .nav-tabs {{ flex-wrap: wrap; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="hero">
            <div class="hero-badge">十倍股早期识别系统 V2.0 · 完整增强版</div>
            <h1>十倍股分析报告</h1>
            <p>基于JQData数据源，使用账号 {username} ({account_type})</p>
            <div class="hero-meta">
                数据时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} | 
                生成时间: {generation_time} |
                数据来源: JQData + MongoDB
            </div>
        </div>

        <!-- 导航标签 (8个) -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showPanel('overview')">📊 概览统计</button>
            <button class="nav-tab" onclick="showPanel('cases')">🏆 十大案例</button>
            <button class="nav-tab" onclick="showPanel('stages')">🔄 阶段分析</button>
            <button class="nav-tab" onclick="showPanel('factors')">📈 因子体系</button>
            <button class="nav-tab" onclick="showPanel('code')">💻 识别代码</button>
            <button class="nav-tab" onclick="showPanel('realdata')">🎯 实战识别</button>
            <button class="nav-tab" onclick="showPanel('validation')">✅ 验证结果</button>
            <button class="nav-tab" onclick="showPanel('strategy')">📋 策略框架</button>
        </div>

        <!-- Tab 1: 概览统计 -->
        <div id="overview" class="panel active">
            <div class="card">
                <h2 class="card-title">执行摘要</h2>
                
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
                        <div class="stat-value orange">{len(s2_stocks)}</div>
                        <div class="stat-label">S2阶段（最佳介入）</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value purple">{max([r['score'] for r in rankings_data] + [0]):.1f}</div>
                        <div class="stat-label">最高得分</div>
                    </div>
                </div>

                <h3 class="card-subtitle">等级分布</h3>
                <div class="stats-grid">
                    {' '.join([f'<div class="stat-card"><div class="stat-value">{v}</div><div class="stat-label">{k}级</div></div>' for k, v in sorted(level_count.items(), key=lambda x: ['S+','S','A','B','C','D'].index(x[0]) if x[0] in ['S+','S','A','B','C','D'] else 99)])}
                </div>

                <h3 class="card-subtitle">行业分布 TOP 10</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr><th>排名</th><th>行业</th><th>股票数</th><th>占比</th></tr>
                        </thead>
                        <tbody>
                            {''.join([f"<tr><td>{i+1}</td><td>{ind}</td><td>{cnt}</td><td>{cnt/len(rankings_data)*100:.1f}%</td></tr>" for i, (ind, cnt) in enumerate(industry_top10)])}
                        </tbody>
                    </table>
                </div>

                <div class="alert alert-info">
                    <span class="alert-icon">📊</span>
                    <div class="alert-content">
                        <div class="alert-title">关键发现</div>
                        <div>
                            <strong>S2阶段股票：</strong>共{len(s2_stocks)}只股票处于最佳介入期<br>
                            <strong>高评级股票：</strong>共{len(s_level_stocks)}只股票获得A级及以上评级<br>
                            <strong>数据完整性：</strong>已评估{len(rankings_data)}只股票，推荐率{len(recommended)/max(1,len(rankings_data))*100:.1f}%
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: 十大案例 -->
        <div id="cases" class="panel">
            <div class="card">
                <h2 class="card-title">十大经典十倍股案例</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">2000-2024年A股市场最具代表性的十倍股案例</p>

                <div class="case-grid">
'''

# 添加案例卡片
for case in classic_cases:
    html_content += f'''
                    <div class="case-card">
                        <div class="case-header">
                            <div>
                                <div class="case-title">{case['name']}</div>
                                <div class="case-code">{case['code']}</div>
                            </div>
                            <div class="case-multiplier">{case['return']}</div>
                        </div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">行业</span><span class="case-meta-value">{case['industry']}</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">周期</span><span class="case-meta-value">{case['period']}</span></div>
                            <div class="case-meta-item" style="grid-column: span 2"><span class="case-meta-label">催化剂</span><span class="case-meta-value">{case['catalyst']}</span></div>
                        </div>
                    </div>
'''

html_content += '''
                </div>

                <h3 class="card-subtitle">案例共性总结</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>📊 财务特征</h4>
                        <div class="axis-item"><span class="axis-label">ROE</span><span class="axis-value">15%+持续多年</span></div>
                        <div class="axis-item"><span class="axis-label">营收增速</span><span class="axis-value">20%+连续3年</span></div>
                        <div class="axis-item"><span class="axis-label">毛利率</span><span class="axis-value">行业领先</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>💰 估值特征</h4>
                        <div class="axis-item"><span class="axis-label">初期PE</span><span class="axis-value">20-40x</span></div>
                        <div class="axis-item"><span class="axis-label">PEG</span><span class="axis-value">&lt;1.5</span></div>
                        <div class="axis-item"><span class="axis-label">市值空间</span><span class="axis-value">10倍以上</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>🚀 催化剂类型</h4>
                        <div class="axis-item"><span class="axis-label">行业趋势</span><span class="axis-value">消费升级/新能源</span></div>
                        <div class="axis-item"><span class="axis-label">政策支持</span><span class="axis-value">产业政策/补贴</span></div>
                        <div class="axis-item"><span class="axis-label">技术突破</span><span class="axis-value">降本/增效</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 3: 阶段分析 -->
        <div id="stages" class="panel">
            <div class="card">
                <h2 class="card-title">十倍股成长阶段分析</h2>

                <div class="alert alert-info">
                    <span class="alert-icon">🔄</span>
                    <div class="alert-content">
                        <div class="alert-title">三轴阶段判定体系</div>
                        <div>基本面轴（Fundamental）+ 资金轴（Flow）+ 预期轴（Expectation）综合判定</div>
                    </div>
                </div>

                <h3 class="card-subtitle">阶段分布统计</h3>
                <div class="stats-grid">
'''

stage_names = {"S0": "观察期", "S1": "验证期", "S2": "导入期(最佳)", "S3": "放量期", "S4": "加速期", "S5": "成熟期"}
for stage, count in sorted(stage_count.items()):
    stage_desc = stage_names.get(stage, stage)
    html_content += f'''
                    <div class="stat-card">
                        <div class="stat-value blue">{count}</div>
                        <div class="stat-label">{stage}阶段<br><small>{stage_desc}</small></div>
                    </div>
'''

html_content += '''
                </div>

                <h3 class="card-subtitle">阶段定义与策略</h3>
                <div class="timeline">
                    <div class="timeline-item s0">
                        <h4 style="margin-bottom: 12px;">S0 - 观察期</h4>
                        <p style="color: var(--text-secondary);">无明显增长信号，排除或等待。基本面未确认，资金面平淡。</p>
                    </div>
                    <div class="timeline-item s1">
                        <h4 style="margin-bottom: 12px;">S1 - 验证期</h4>
                        <p style="color: var(--text-secondary);">早期信号出现，小仓位试错。基本面改善中，资金开始关注。</p>
                    </div>
                    <div class="timeline-item s2">
                        <h4 style="margin-bottom: 12px; color: var(--accent-green);">S2 - 导入期（最佳介入点）⭐</h4>
                        <p style="color: var(--text-secondary);">增长确认，资金流入，重点配置。业绩拐点确认，机构开始建仓。</p>
                    </div>
                    <div class="timeline-item s3">
                        <h4 style="margin-bottom: 12px; color: var(--accent-red);">S3 - 放量期</h4>
                        <p style="color: var(--text-secondary);">加速上涨，关注估值，谨慎持有。业绩兑现中，需关注估值天花板。</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 4: 因子体系 -->
        <div id="factors" class="panel">
            <div class="card">
                <h2 class="card-title">十倍股因子评分体系</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">100分制综合评分，7个维度全面评估</p>

                <h3 class="card-subtitle">评分维度与权重</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr><th>维度</th><th>权重</th><th>满分</th><th>评估内容</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>财务因子</td><td>25%</td><td>25分</td><td>ROE、营收增速、利润增速、毛利率</td></tr>
                            <tr><td>成长因子</td><td>20%</td><td>20分</td><td>市场空间、行业地位、研发投入</td></tr>
                            <tr><td>估值因子</td><td>15%</td><td>15分</td><td>PE、PB、PEG、市值空间</td></tr>
                            <tr><td>技术因子</td><td>15%</td><td>15分</td><td>相对强度、成交量、趋势</td></tr>
                            <tr><td>行业因子</td><td>10%</td><td>10分</td><td>行业景气度、政策支持</td></tr>
                            <tr><td>质量因子</td><td>10%</td><td>10分</td><td>治理结构、现金流、负债率</td></tr>
                            <tr><td>风险因子</td><td>5%</td><td>5分</td><td>波动率、回撤、流动性</td></tr>
                        </tbody>
                    </table>
                </div>

                <h3 class="card-subtitle">等级划分</h3>
                <div class="stats-grid">
                    <div class="stat-card"><div class="stat-value" style="color: #92400e;">S+</div><div class="stat-label">90分以上<br>核心持仓</div></div>
                    <div class="stat-card"><div class="stat-value green">S</div><div class="stat-label">80-89分<br>重点配置</div></div>
                    <div class="stat-card"><div class="stat-value blue">A</div><div class="stat-label">70-79分<br>积极买入</div></div>
                    <div class="stat-card"><div class="stat-value purple">B</div><div class="stat-label">60-69分<br>适度配置</div></div>
                    <div class="stat-card"><div class="stat-value">C</div><div class="stat-label">50-59分<br>观察等待</div></div>
                    <div class="stat-card"><div class="stat-value red">D</div><div class="stat-label">50分以下<br>不推荐</div></div>
                </div>
            </div>
        </div>

        <!-- Tab 5: 识别代码 -->
        <div id="code" class="panel">
            <div class="card">
                <h2 class="card-title">JQData十倍股识别代码</h2>

                <h3 class="card-subtitle">1. 认证与初始化</h3>
                <div class="code-block" data-lang="python">
<pre><code class="language-python"># 导入JQData SDK
import jqdatasdk as jq
from datetime import datetime, timedelta

# 认证
jq.auth('your_username', 'your_password')

# 获取账号信息
account_info = jq.get_account_info()
print(f"账号类型: {account_info.get('query_count_limit')}")
print(f"有效期: {account_info.get('expire_time')}")</code></pre>
                </div>

                <h3 class="card-subtitle">2. 候选股票筛选</h3>
                <div class="code-block" data-lang="python">
<pre><code class="language-python"># 获取全部股票
stocks = jq.get_all_securities(types=['stock'])

# 排除ST和退市股票
stocks = stocks[~stocks['display_name'].str.contains('ST|\\*')]
stocks = stocks[stocks['end_date'] > datetime.now().strftime('%Y-%m-%d')]

# 筛选主板和创业板
stocks = stocks[stocks.index.str.match(r'^(00|30|60)')]

# 获取估值数据筛选市值
q = jq.query(
    jq.valuation.code,
    jq.valuation.market_cap
).filter(
    jq.valuation.market_cap.between(50, 2000)  # 50-2000亿市值
)
valid_stocks = jq.get_fundamentals(q)</code></pre>
                </div>

                <h3 class="card-subtitle">3. 财务因子获取</h3>
                <div class="code-block" data-lang="python">
<pre><code class="language-python"># 获取财务指标
def get_financial_factors(stock_code, date):
    q = jq.query(
        jq.indicator.code,
        jq.indicator.roe,               # ROE
        jq.indicator.roa,               # ROA
        jq.indicator.gross_profit_margin,  # 毛利率
        jq.indicator.inc_revenue_year_on_year,  # 营收增速
        jq.indicator.inc_net_profit_year_on_year  # 利润增速
    ).filter(jq.indicator.code == stock_code)
    
    return jq.get_fundamentals(q, date=date)</code></pre>
                </div>

                <div class="alert alert-success">
                    <span class="alert-icon">💡</span>
                    <div class="alert-content">
                        <div class="alert-title">完整代码</div>
                        <div>完整的十倍股识别代码请参考：<code>mcp_servers/utils/tenbagger_v2/</code> 目录</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 6: 实战识别 -->
        <div id="realdata" class="panel">
            <div class="card">
                <h2 class="card-title">实战识别结果</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px;">基于{username}账号数据，识别时间：{generation_time}</p>
'''

# 添加TOP 20排名表格
html_content += f'''
                <h3 class="card-subtitle">Top 20 潜在十倍股</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr><th>排名</th><th>代码</th><th>名称</th><th>阶段</th><th>等级</th><th>得分</th><th>行业</th></tr>
                        </thead>
                        <tbody>
'''

for i, stock in enumerate(recommended[:20], 1):
    score_class = "positive" if stock['score'] >= 70 else ""
    html_content += f'''
                            <tr>
                                <td>{i}</td>
                                <td><code>{stock['symbol']}</code></td>
                                <td><strong>{stock['name']}</strong></td>
                                <td><span class="badge badge-{stock['stage'].lower()}">{stock['stage']}</span></td>
                                <td><span class="badge badge-{stock['level'].lower()}">{stock['level']}</span></td>
                                <td class="{score_class}">{stock['score']:.1f}</td>
                                <td>{stock.get('mainline', '-')}</td>
                            </tr>
'''

html_content += '''
                        </tbody>
                    </table>
                </div>

                <div class="alert alert-success">
                    <span class="alert-icon">🎯</span>
                    <div class="alert-content">
                        <div class="alert-title">投资建议</div>
                        <div>
'''

s2_names = ', '.join([f"{s['name']}({s['symbol']})" for s in s2_stocks[:5]]) if s2_stocks else '暂无S2阶段股票'
html_content += f'''
                            <strong>重点关注S2阶段股票：</strong>{s2_names}<br>
                            <strong>识别特征：</strong>业绩拐点确认、机构资金流入、估值合理
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 7: 验证结果 -->
        <div id="validation" class="panel">
            <div class="card">
                <h2 class="card-title">体系有效性验证</h2>

                <h3 class="card-subtitle">验证统计</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value blue">{len(rankings_data)}</div>
                        <div class="stat-label">样本量</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value green">{len(recommended)/max(1,len(rankings_data))*100:.0f}%</div>
                        <div class="stat-label">推荐通过率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value orange">{len(s2_stocks)}</div>
                        <div class="stat-label">S2阶段数量</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value purple">{sum([r['score'] for r in recommended])/max(1,len(recommended)):.1f}</div>
                        <div class="stat-label">平均得分</div>
                    </div>
                </div>

                <h3 class="card-subtitle">数据质量</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>数据来源</h4>
                        <div class="axis-item"><span class="axis-label">JQData</span><span class="axis-value">基本面+估值</span></div>
                        <div class="axis-item"><span class="axis-label">MongoDB</span><span class="axis-value">评估结果</span></div>
                        <div class="axis-item"><span class="axis-label">账号类型</span><span class="axis-value">{account_type}</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>评估覆盖</h4>
                        <div class="axis-item"><span class="axis-label">评估股票</span><span class="axis-value">{len(rankings_data)}只</span></div>
                        <div class="axis-item"><span class="axis-label">有效推荐</span><span class="axis-value">{len(recommended)}只</span></div>
                        <div class="axis-item"><span class="axis-label">S2阶段</span><span class="axis-value">{len(s2_stocks)}只</span></div>
                    </div>
                </div>

                <div class="alert alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-content">
                        <div class="alert-title">免责声明</div>
                        <div>本报告基于历史数据和量化模型生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 8: 策略框架 -->
        <div id="strategy" class="panel">
            <div class="card">
                <h2 class="card-title">十倍股策略框架</h2>

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

                <h3 class="card-subtitle">两条路线策略</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>路线A：趋势突破</h4>
                        <div class="axis-item"><span class="axis-label">入场</span><span class="axis-value">突破关键阻力位</span></div>
                        <div class="axis-item"><span class="axis-label">仓位</span><span class="axis-value">分批建仓</span></div>
                        <div class="axis-item"><span class="axis-label">止损</span><span class="axis-value">跌破突破位-3%</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>路线B：基本面驱动</h4>
                        <div class="axis-item"><span class="axis-label">入场</span><span class="axis-value">业绩拐点确认</span></div>
                        <div class="axis-item"><span class="axis-label">仓位</span><span class="axis-value">逐步加仓</span></div>
                        <div class="axis-item"><span class="axis-label">止损</span><span class="axis-value">逻辑破坏</span></div>
                    </div>
                </div>

                <div class="alert alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-content">
                        <div class="alert-title">风险提示</div>
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
'''

# 保存报告
report_dir = project_root / "reports"
report_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = report_dir / f"tenbagger_full_report_{username}_{timestamp}.html"

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 完整版报告已生成: {report_file}")
print(f"   - 评估股票: {len(rankings_data)}只")
print(f"   - 推荐股票: {len(recommended)}只")
print(f"   - S2阶段: {len(s2_stocks)}只")

if recommended:
    print(f"   - TOP 5: {', '.join([s['name'] for s in recommended[:5]])}")

print(f"\n文件大小: {report_file.stat().st_size / 1024:.1f} KB")
print("\n" + "=" * 80)
print("✅ 十倍股完整版增强报告生成完成！")
print("=" * 80)

# 6. 记录生成方法到知识库
print("\n【步骤6】记录生成方法到知识库")
print("-" * 80)

generation_record = {
    "report_file": str(report_file),
    "generation_time": generation_time,
    "username": username,
    "account_type": account_type,
    "data_range": f"{start_date} to {end_date}",
    "total_stocks": len(rankings_data),
    "recommended_stocks": len(recommended),
    "s2_stocks": len(s2_stocks),
    "tabs": ["overview", "cases", "stages", "factors", "code", "realdata", "validation", "strategy"],
    "script": "scripts/generate_tenbagger_full_report.py",
    "data_sources": ["JQData", "MongoDB"],
    "design_style": "Apple Design System"
}

# 保存生成记录
record_file = project_root / "docs" / "report_generation_records" / f"tenbagger_full_{timestamp}.json"
record_file.parent.mkdir(parents=True, exist_ok=True)

with open(record_file, 'w', encoding='utf-8') as f:
    json.dump(generation_record, f, ensure_ascii=False, indent=2)

print(f"✅ 生成记录已保存: {record_file}")

