#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十倍股筛选流程 - 完整运行脚本
"""

import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("十倍股筛选流程 - 完整运行")
print("=" * 80)

# 1. 获取投资主线和候选池
print("\n【步骤1】获取投资主线和候选池")
print("-" * 80)

stock_list = []
try:
    from core.mainline_scanner import MainlineBasedScanner
    from jqdata.client import JQDataClient
    from config.config_manager import get_config_manager
    
    config = get_config_manager().get_jqdata_config()
    jq_client = JQDataClient(username=config.get("username"), password=config.get("password"))
    print("✅ JQData客户端初始化成功")
    
    scanner = MainlineBasedScanner(jq_client=jq_client)
    result = scanner.scan_from_mainlines(period="medium", min_score=60.0, max_mainlines=10, max_stocks_per_mainline=20)
    
    mainlines = result.get("mainlines", [])
    stocks = result.get("stocks", [])
    
    print(f"✅ 获取到 {len(mainlines)} 条投资主线")
    print(f"✅ 获取到 {len(stocks)} 只候选股票")
    
    for stock in stocks[:30]:
        stock_list.append({
            "symbol": stock.security_id,
            "name": getattr(stock, 'name', stock.security_id),
            "mainline": getattr(stock, 'mainline', "未知")
        })
    
    print(f"\n准备评估 {len(stock_list)} 只股票")
except Exception as e:
    print(f"❌ 获取候选池失败: {e}")
    import traceback
    traceback.print_exc()

# 2. 批量评估
print("\n【步骤2】批量评估十倍股潜力")
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
    except Exception as e:
        print(f"❌ 批量评估失败: {e}")
        import traceback
        traceback.print_exc()

# 3. 排序和筛选
print("\n【步骤3】排序和筛选")
print("-" * 80)

evaluated_stocks.sort(key=lambda x: x["total_score"], reverse=True)
recommended = [s for s in evaluated_stocks if s["total_score"] >= 50.0]

print(f"✅ 推荐股票数: {len(recommended)} 只 (A级及以上)")

level_count = {}
for s in recommended:
    level_count[s["eval_level"]] = level_count.get(s["eval_level"], 0) + 1

stage_count = {}
for s in recommended:
    stage_count[s["stage"]] = stage_count.get(s["stage"], 0) + 1

print(f"等级分布: {level_count}")
print(f"阶段分布: {stage_count}")

# 4. 生成报告
print("\n【步骤4】生成推荐列表报告")
print("-" * 80)

stage_names = {"S0": "观察期", "S1": "验证期", "S2": "导入期，最佳介入点", "S3": "放量期", "S4": "加速期", "S5": "成熟期"}

report_lines = [
    "# 早期十倍股推荐名录",
    "",
    f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
    "> **评估系统**: TRQuant十倍股早期识别系统  ",
    "> **数据来源**: JQData + MongoDB",
    "",
    "---",
    "",
    "## 📊 推荐概览",
    "",
    f"**评估股票数**: {len(evaluated_stocks)}只  ",
    f"**推荐股票数**: {len(recommended)}只  ",
    f"**等级分布**: {', '.join([f'{k}级: {v}只' for k, v in sorted(level_count.items(), reverse=True)])}",
    "",
    "**阶段分布**:",
]
for k, v in sorted(stage_count.items()):
    report_lines.append(f"- {k}阶段（{stage_names.get(k, k)}）: {v}只")

report_lines.extend([
    "",
    "---",
    "",
    "## 🎯 TOP 5 重点推荐",
    ""
])

for i, stock in enumerate(recommended[:5], 1):
    stars = "⭐" * (6 - i)
    stage_display = stage_names.get(stock["stage"], stock["stage"])
    report_lines.extend([
        f"### {i}. {stock['name']} ({stock['symbol']}) {stars}",
        "",
        f"- **等级**: {stock['eval_level']}级",
        f"- **总分**: {stock['total_score']:.1f}分",
        f"- **阶段**: {stock['stage']}（{stage_display}）",
        f"- **主线**: {stock['mainline']}",
        f"- **评分卡**: {stock['scorecard_score']:.1f}分",
        f"- **建议**: {stock['recommendation']}",
        ""
    ])

report_lines.extend([
    "---",
    "",
    "## 📋 完整推荐名录",
    "",
    "| 排名 | 代码 | 名称 | 阶段 | 等级 | 总分 | 评分卡 | 主线 |",
    "|------|------|------|------|------|------|--------|------|"
])

for i, stock in enumerate(recommended, 1):
    level_display = f"**{stock['eval_level']}**" if stock['eval_level'] in ['S+', 'S'] else stock['eval_level']
    report_lines.append(f"| {i} | {stock['symbol']} | {stock['name']} | {stock['stage']} | {level_display} | {stock['total_score']:.1f} | {stock['scorecard_score']:.1f} | {stock['mainline']} |")

report_lines.extend([
    "",
    "---",
    "",
    "## 📈 按主线分类",
    ""
])

mainline_groups = {}
for stock in recommended:
    ml = stock['mainline']
    if ml not in mainline_groups:
        mainline_groups[ml] = []
    mainline_groups[ml].append(stock)

for mainline, stocks in sorted(mainline_groups.items(), key=lambda x: len(x[1]), reverse=True):
    report_lines.append(f"### {mainline} ({len(stocks)}只)")
    report_lines.append("")
    for idx, stock in enumerate(sorted(stocks, key=lambda x: x['total_score'], reverse=True), 1):
        level_display = f"**{stock['eval_level']}级**" if stock['eval_level'] in ['S+', 'S'] else f"{stock['eval_level']}级"
        report_lines.append(f"{idx}. **{stock['name']}** ({stock['symbol']}) - {level_display}, {stock['total_score']:.1f}分, {stock['stage']}阶段")
    report_lines.append("")

s2_stocks = [s for s in recommended if s['stage'] == 'S2']
if s2_stocks:
    report_lines.extend([
        "---",
        "",
        "## 💡 投资建议",
        "",
        "### 最佳介入期股票（S2阶段）",
        "",
        "**S2阶段是十倍股的最佳介入期**，推荐重点关注：",
        ""
    ])
    for i, stock in enumerate(s2_stocks[:5], 1):
        report_lines.append(f"{i}. **{stock['name']}** ({stock['symbol']}) - {stock['mainline']}，{stock['total_score']:.1f}分")

report_lines.extend([
    "",
    "---",
    "",
    "## ⚠️ 风险提示",
    "",
    "1. **阶段风险**: S3阶段股票已进入放量期，需关注估值水平",
    "2. **行业风险**: 关注政策变化和行业周期",
    "3. **个股风险**: 建议结合基本面和技术面综合分析",
    "4. **数据风险**: 本评估基于历史数据，不构成投资建议",
    "",
    "---",
    "",
    "## 📚 评估说明",
    "",
    "- **评估维度**: 7个维度（阶段、评分卡、成长性、行业地位、另类数据、动量、风险）",
    "- **数据来源**: JQData财务数据 + MongoDB阶段数据",
    f"- **评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "- **有效期**: 建议每日更新评估结果",
    "",
    "---",
    "",
    "*本名录由TRQuant十倍股早期识别系统自动生成*"
])

report_path = project_root / "docs" / "TENBAGGER_RECOMMENDATION_LIST.md"
report_path.write_text("\n".join(report_lines), encoding='utf-8')

print(f"✅ 报告已生成: {report_path}")
print(f"   - 评估股票: {len(evaluated_stocks)}只")
print(f"   - 推荐股票: {len(recommended)}只")
if recommended:
    print(f"   - TOP 5: {', '.join([s['name'] for s in recommended[:5]])}")

print("\n" + "=" * 80)
print("✅ 十倍股筛选流程完成！")
print("=" * 80)
