#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十倍股综合报告生成脚本
使用账号 13327806797，基于最近三个月数据生成最新报告
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
print("十倍股综合报告生成 - 使用账号 13327806797")
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
    print(f"账号类型: {'正式账户' if account_info.get('query_count_limit', 0) >= 200000000 else '试用账户'}")
    print(f"有效期: {account_info.get('expire_time', 'N/A')}")
    print(f"数据范围: {account_info.get('date_range_start', 'N/A')} 至 {account_info.get('date_range_end', 'N/A')}")
    print()
except Exception as e:
    print(f"❌ 认证失败: {e}")
    sys.exit(1)

# 2. 获取投资主线和候选池
print("【步骤2】获取投资主线和候选池")
print("-" * 80)

stock_list = []
try:
    from core.mainline_scanner import MainlineBasedScanner
    
    jq_client = JQDataClient()
    jq_client.authenticate(username, password)
    print("✅ JQData客户端初始化成功")
    
    scanner = MainlineBasedScanner(jq_client=jq_client)
    result = scanner.scan_from_mainlines(
        period="medium", 
        min_score=60.0, 
        max_mainlines=10, 
        max_stocks_per_mainline=20
    )
    
    mainlines = result.get("mainlines", [])
    stocks = result.get("stocks", [])
    
    print(f"✅ 获取到 {len(mainlines)} 条投资主线")
    print(f"✅ 获取到 {len(stocks)} 只候选股票")
    
    for stock in stocks[:50]:  # 增加评估数量
        stock_list.append({
            "symbol": stock.security_id,
            "name": getattr(stock, 'name', stock.security_id),
            "mainline": getattr(stock, 'mainline', "未知")
        })
    
    print(f"\n准备评估 {len(stock_list)} 只股票")
    print()
except Exception as e:
    print(f"❌ 获取候选池失败: {e}")
    import traceback
    traceback.print_exc()
    stock_list = []

# 如果主线扫描没有获取到股票，从数据库获取已有的十倍股排名
if not stock_list:
    print("⚠️ 主线扫描未获取到股票，尝试从数据库获取已有排名...")
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
            
            # 转换为评估格式
            for rank in rankings:
                symbol = rank.get('symbol', rank.get('code', rank.get('security_id', '')))
                if symbol:
                    stock_list.append({
                        "symbol": symbol,
                        "name": rank.get('name', rank.get('stock_name', symbol)),
                        "mainline": "数据库已有评估"
                    })
        else:
            print(f"⚠️ 数据库获取失败: {db_result.get('error', '未知错误')}")
    except Exception as e:
        print(f"⚠️ 从数据库获取失败: {e}")

# 3. 批量评估十倍股潜力
print("【步骤3】批量评估十倍股潜力")
print("-" * 80)

evaluated_stocks = []
if stock_list:
    try:
        from extension.python.tenbagger_commands import tenbagger_evaluate
        
        for i, stock_info in enumerate(stock_list, 1):
            symbol = stock_info["symbol"]
            name = stock_info["name"]
            print(f"评估 {i}/{len(stock_list)}: {symbol} ({name})", end=" ... ", flush=True)
            
            try:
                result = tenbagger_evaluate(symbol)
                if "error" not in result:
                    eval_level = str(result.get("eval_level", "D")).replace("EvalLevel.", "")
                    evaluated_stocks.append({
                        "symbol": symbol,
                        "name": name,
                        "mainline": stock_info.get("mainline", "未知"),
                        "stage": result.get("stage", "S0"),
                        "scorecard_score": result.get("scorecard_score", 0),
                        "total_score": result.get("total_score", 0),
                        "eval_level": eval_level,
                        "recommendation": result.get("recommendation", "")
                    })
                    print(f"✅ {result.get('total_score', 0):.1f}分, {eval_level}")
                else:
                    print(f"❌ {result.get('error', 'Unknown')[:30]}")
            except Exception as e:
                print(f"❌ {str(e)[:50]}")
        
        print(f"\n✅ 完成评估: {len(evaluated_stocks)} 只股票")
        print()
    except Exception as e:
        print(f"❌ 批量评估失败: {e}")
        import traceback
        traceback.print_exc()

# 4. 排序和筛选
print("【步骤4】排序和筛选")
print("-" * 80)

evaluated_stocks.sort(key=lambda x: x["total_score"], reverse=True)
recommended = [s for s in evaluated_stocks if s["total_score"] >= 50.0]

print(f"✅ 推荐股票数: {len(recommended)} 只 (总分≥50分)")

level_count = {}
for s in recommended:
    level_count[s["eval_level"]] = level_count.get(s["eval_level"], 0) + 1

stage_count = {}
for s in recommended:
    stage_count[s["stage"]] = stage_count.get(s["stage"], 0) + 1

print(f"等级分布: {level_count}")
print(f"阶段分布: {stage_count}")
print()

# 5. 生成综合HTML报告
print("【步骤5】生成综合HTML报告")
print("-" * 80)

stage_names = {
    "S0": "观察期", 
    "S1": "验证期", 
    "S2": "导入期，最佳介入点", 
    "S3": "放量期", 
    "S4": "加速期", 
    "S5": "成熟期"
}

# 获取股票详细信息（用于报告）
def get_stock_details(symbol):
    """获取股票详细信息"""
    try:
        stock_info = jq.get_security_info(symbol)
        if stock_info:
            return {
                "display_name": stock_info.display_name if hasattr(stock_info, 'display_name') else None,
                "name": stock_info.name if hasattr(stock_info, 'name') else None,
                "start_date": str(stock_info.start_date) if hasattr(stock_info, 'start_date') else None
            }
    except:
        pass
    return None

# 生成HTML报告
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股综合报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 36px;
            margin-bottom: 15px;
        }}
        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 50px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section-title {{
            font-size: 28px;
            color: #333;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 4px solid #667eea;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
        }}
        .summary-card .number {{
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .summary-card .label {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .info-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }}
        .info-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        .info-table tr:hover {{
            background: #f8f9fa;
        }}
        .score-high {{
            color: #28a745;
            font-weight: bold;
        }}
        .score-medium {{
            color: #ffc107;
            font-weight: bold;
        }}
        .score-low {{
            color: #dc3545;
        }}
        .stage-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        .stage-s2 {{
            background: #d4edda;
            color: #155724;
        }}
        .stage-s3 {{
            background: #fff3cd;
            color: #856404;
        }}
        .stage-s0 {{
            background: #e2e3e5;
            color: #383d41;
        }}
        .level-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        .level-s {{
            background: #d4edda;
            color: #155724;
        }}
        .level-a {{
            background: #cce5ff;
            color: #004085;
        }}
        .level-b {{
            background: #fff3cd;
            color: #856404;
        }}
        .level-c {{
            background: #f8d7da;
            color: #721c24;
        }}
        .mainline-tag {{
            display: inline-block;
            padding: 4px 10px;
            background: #e9ecef;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 5px;
        }}
        .top5-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .top5-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .top5-item h3 {{
            color: #333;
            margin-bottom: 15px;
        }}
        .top5-item .details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .top5-item .detail-item {{
            display: flex;
            flex-direction: column;
        }}
        .top5-item .detail-label {{
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }}
        .top5-item .detail-value {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .stat-card .label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
        .stat-card .value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            font-size: 14px;
            border-top: 1px solid #eee;
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 十倍股综合报告</h1>
            <div class="subtitle">账号: {username} | 数据范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}</div>
            <div class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="content">
            <!-- 执行摘要 -->
            <div class="section">
                <h2 class="section-title">📊 执行摘要</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="number">{len(evaluated_stocks)}</div>
                        <div class="label">评估股票数</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">{len(recommended)}</div>
                        <div class="label">推荐股票数</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">{len([s for s in recommended if s['stage'] == 'S2'])}</div>
                        <div class="label">S2阶段（最佳介入）</div>
                    </div>
                    <div class="summary-card">
                        <div class="number">{max([s['total_score'] for s in recommended] + [0]):.1f}</div>
                        <div class="label">最高得分</div>
                    </div>
                </div>
            </div>
            
            <!-- 统计信息 -->
            <div class="section">
                <h2 class="section-title">📈 统计信息</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">等级分布</div>
                        <div class="value">
                            {', '.join([f'{k}级: {v}只' for k, v in sorted(level_count.items(), reverse=True)]) if level_count else '无数据'}
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="label">阶段分布</div>
                        <div class="value">
                            {', '.join([f'{k}: {v}只' for k, v in sorted(stage_count.items())]) if stage_count else '无数据'}
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="label">平均得分</div>
                        <div class="value">
                            {f"{sum([s['total_score'] for s in recommended]) / len(recommended):.1f}" if recommended and len(recommended) > 0 else "0.0"}
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="label">数据来源</div>
                        <div class="value">JQData + MongoDB</div>
                    </div>
                </div>
            </div>
            
            <!-- TOP 5 重点推荐 -->
            <div class="section">
                <h2 class="section-title">⭐ TOP 5 重点推荐</h2>
                <div class="top5-section">
"""

for i, stock in enumerate(recommended[:5], 1):
    stars = "⭐" * (6 - i)
    stage_display = stage_names.get(stock["stage"], stock["stage"])
    stock_details = get_stock_details(stock["symbol"])
    display_name = stock_details.get("display_name") if stock_details else stock["name"]
    
    html_content += f"""
                    <div class="top5-item">
                        <h3>{i}. {display_name} ({stock['symbol']}) {stars}</h3>
                        <div class="details">
                            <div class="detail-item">
                                <div class="detail-label">等级</div>
                                <div class="detail-value">
                                    <span class="level-badge level-{stock['eval_level'].lower()}">{stock['eval_level']}级</span>
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">总分</div>
                                <div class="detail-value score-high">{stock['total_score']:.1f}分</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">阶段</div>
                                <div class="detail-value">
                                    <span class="stage-badge stage-{stock['stage'].lower()}">{stock['stage']} ({stage_display})</span>
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">评分卡</div>
                                <div class="detail-value">{stock['scorecard_score']:.1f}分</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">投资主线</div>
                                <div class="detail-value">
                                    <span class="mainline-tag">{stock['mainline']}</span>
                                </div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">建议</div>
                                <div class="detail-value" style="font-size: 14px;">{stock['recommendation']}</div>
                            </div>
                        </div>
                    </div>
"""

html_content += """
                </div>
            </div>
            
            <!-- 完整推荐名录 -->
            <div class="section">
                <h2 class="section-title">📋 完整推荐名录</h2>
                <table class="info-table">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>代码</th>
                            <th>名称</th>
                            <th>阶段</th>
                            <th>等级</th>
                            <th>总分</th>
                            <th>评分卡</th>
                            <th>投资主线</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for i, stock in enumerate(recommended, 1):
    stock_details = get_stock_details(stock["symbol"])
    display_name = stock_details.get("display_name") if stock_details else stock["name"]
    stage_display = stage_names.get(stock["stage"], stock["stage"])
    
    score_class = "score-high" if stock['total_score'] >= 70 else ("score-medium" if stock['total_score'] >= 60 else "score-low")
    
    html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td>{stock['symbol']}</td>
                            <td>{display_name}</td>
                            <td><span class="stage-badge stage-{stock['stage'].lower()}">{stock['stage']}</span></td>
                            <td><span class="level-badge level-{stock['eval_level'].lower()}">{stock['eval_level']}</span></td>
                            <td class="{score_class}">{stock['total_score']:.1f}</td>
                            <td>{stock['scorecard_score']:.1f}</td>
                            <td><span class="mainline-tag">{stock['mainline']}</span></td>
                        </tr>
"""

html_content += """
                    </tbody>
                </table>
            </div>
            
            <!-- 按主线分类 -->
            <div class="section">
                <h2 class="section-title">📈 按投资主线分类</h2>
"""

mainline_groups = {}
for stock in recommended:
    ml = stock['mainline']
    if ml not in mainline_groups:
        mainline_groups[ml] = []
    mainline_groups[ml].append(stock)

for mainline, stocks in sorted(mainline_groups.items(), key=lambda x: len(x[1]), reverse=True):
    html_content += f"""
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: #667eea;">{mainline} ({len(stocks)}只)</h3>
                <table class="info-table">
                    <thead>
                        <tr>
                            <th>代码</th>
                            <th>名称</th>
                            <th>阶段</th>
                            <th>等级</th>
                            <th>总分</th>
                            <th>评分卡</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    for stock in sorted(stocks, key=lambda x: x['total_score'], reverse=True):
        stock_details = get_stock_details(stock["symbol"])
        display_name = stock_details.get("display_name") if stock_details else stock["name"]
        score_class = "score-high" if stock['total_score'] >= 70 else ("score-medium" if stock['total_score'] >= 60 else "score-low")
        
        html_content += f"""
                        <tr>
                            <td>{stock['symbol']}</td>
                            <td>{display_name}</td>
                            <td><span class="stage-badge stage-{stock['stage'].lower()}">{stock['stage']}</span></td>
                            <td><span class="level-badge level-{stock['eval_level'].lower()}">{stock['eval_level']}</span></td>
                            <td class="{score_class}">{stock['total_score']:.1f}</td>
                            <td>{stock['scorecard_score']:.1f}</td>
                        </tr>
"""
    html_content += """
                    </tbody>
                </table>
"""

# S2阶段股票（最佳介入点）
s2_stocks = [s for s in recommended if s['stage'] == 'S2']
if s2_stocks:
    html_content += f"""
            <!-- 最佳介入期股票 -->
            <div class="section">
                <h2 class="section-title">💡 最佳介入期股票（S2阶段）</h2>
                <div style="background: #d4edda; padding: 20px; border-radius: 8px; border-left: 5px solid #28a745; margin-bottom: 20px;">
                    <p style="font-size: 16px; color: #155724; margin-bottom: 15px;">
                        <strong>重要提示：</strong>S2阶段是十倍股的最佳介入期，推荐重点关注以下股票：
                    </p>
                </div>
                <table class="info-table">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>代码</th>
                            <th>名称</th>
                            <th>等级</th>
                            <th>总分</th>
                            <th>评分卡</th>
                            <th>投资主线</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    for i, stock in enumerate(s2_stocks[:10], 1):
        stock_details = get_stock_details(stock["symbol"])
        display_name = stock_details.get("display_name") if stock_details else stock["name"]
        score_class = "score-high" if stock['total_score'] >= 70 else ("score-medium" if stock['total_score'] >= 60 else "score-low")
        
        html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td>{stock['symbol']}</td>
                            <td>{display_name}</td>
                            <td><span class="level-badge level-{stock['eval_level'].lower()}">{stock['eval_level']}</span></td>
                            <td class="{score_class}">{stock['total_score']:.1f}</td>
                            <td>{stock['scorecard_score']:.1f}</td>
                            <td><span class="mainline-tag">{stock['mainline']}</span></td>
                        </tr>
"""
    html_content += """
                    </tbody>
                </table>
            </div>
"""

# 风险提示和评估说明
html_content += f"""
            <!-- 风险提示 -->
            <div class="section">
                <h2 class="section-title">⚠️ 风险提示</h2>
                <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 5px solid #ffc107;">
                    <ul style="line-height: 2; color: #856404;">
                        <li><strong>阶段风险：</strong>S3阶段股票已进入放量期，需关注估值水平</li>
                        <li><strong>行业风险：</strong>关注政策变化和行业周期</li>
                        <li><strong>个股风险：</strong>建议结合基本面和技术面综合分析</li>
                        <li><strong>数据风险：</strong>本评估基于历史数据，不构成投资建议</li>
                    </ul>
                </div>
            </div>
            
            <!-- 评估说明 -->
            <div class="section">
                <h2 class="section-title">📚 评估说明</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <ul style="line-height: 2;">
                        <li><strong>评估维度：</strong>7个维度（阶段、评分卡、成长性、行业地位、另类数据、动量、风险）</li>
                        <li><strong>数据来源：</strong>JQData财务数据 + MongoDB阶段数据</li>
                        <li><strong>数据时间范围：</strong>{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}（最近3个月）</li>
                        <li><strong>评估时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                        <li><strong>有效期：</strong>建议每日更新评估结果</li>
                        <li><strong>账号信息：</strong>{username} ({'正式账户' if account_info.get('query_count_limit', 0) >= 200000000 else '试用账户'})</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>TRQuant 十倍股早期识别系统 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px; font-size: 12px;">*本报告由TRQuant十倍股早期识别系统自动生成，不构成投资建议*</p>
        </div>
    </div>
</body>
</html>
"""

# 保存报告
report_dir = project_root / "reports"
report_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = report_dir / f"tenbagger_comprehensive_report_{username}_{timestamp}.html"

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 报告已生成: {report_file}")
print(f"   - 评估股票: {len(evaluated_stocks)}只")
print(f"   - 推荐股票: {len(recommended)}只")
if recommended:
    print(f"   - TOP 5: {', '.join([s['name'] for s in recommended[:5]])}")
    print(f"   - S2阶段（最佳介入）: {len(s2_stocks)}只")

print("\n" + "=" * 80)
print("✅ 十倍股综合报告生成完成！")
print("=" * 80)

