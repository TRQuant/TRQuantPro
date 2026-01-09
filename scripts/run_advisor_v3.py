#!/usr/bin/env python3
"""
V3.0 投资推荐系统 - 端到端测试脚本
==================================

运行完整的V3工作流，生成本周投资推荐报告。

使用方法:
    python scripts/run_advisor_v3.py [--style balanced] [--date 2026-01-07]

参数:
    --style: 筛选风格 (conservative/balanced/aggressive/trend/event)
    --date: 目标日期 (默认今天)
    --verbose: 是否打印详情
"""

import sys
import os
import argparse
from datetime import datetime

# 确保项目根目录在路径中
PROJECT_ROOT = "/home/taotao/.cursor/worktrees/TRQuant/ope"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    parser = argparse.ArgumentParser(description='V3.0 投资推荐系统')
    parser.add_argument('--style', type=str, default='balanced',
                        choices=['conservative', 'balanced', 'aggressive', 'trend', 'event'],
                        help='筛选风格')
    parser.add_argument('--date', type=str, default=None,
                        help='目标日期 (YYYY-MM-DD)')
    parser.add_argument('--verbose', action='store_true', default=True,
                        help='是否打印详情')
    parser.add_argument('--no-report', action='store_true',
                        help='不生成HTML报告')
    parser.add_argument('--no-save', action='store_true',
                        help='不保存到MongoDB')
    
    args = parser.parse_args()
    
    # 打印启动信息
    print("=" * 70)
    print("🚀 V3.0 投资推荐系统")
    print("=" * 70)
    print(f"📅 目标日期: {args.date or '今天'}")
    print(f"🎯 筛选风格: {args.style}")
    print(f"📄 生成报告: {'是' if not args.no_report else '否'}")
    print(f"💾 保存数据: {'是' if not args.no_save else '否'}")
    print("=" * 70)
    
    # JQData认证
    print("\n⏳ 正在认证JQData...")
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        print("✅ JQData认证成功")
        
        # 检查查询余量
        count = jq.get_query_count()
        print(f"   剩余查询次数: {count.get('spare', 'N/A')}")
        
    except Exception as e:
        print(f"❌ JQData认证失败: {e}")
        print("   请检查config/jqdata_config.json配置")
        sys.exit(1)
    
    # 导入并运行V3工作流
    print("\n⏳ 正在加载V3模块...")
    try:
        from core.advisor_v3 import WeeklyAdvisorV3, WorkflowConfig
        print("✅ V3模块加载成功")
    except ImportError as e:
        print(f"❌ V3模块加载失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 配置工作流
    config = WorkflowConfig(
        filter_style=args.style,
        verbose=args.verbose,
        generate_html=not args.no_report,
        save_to_mongodb=not args.no_save,
    )
    
    # 运行工作流
    print("\n⏳ 正在运行V3工作流...")
    advisor = WeeklyAdvisorV3(config)
    result = advisor.run(args.date)
    
    # 检查结果
    if "error" in result:
        print(f"\n❌ 工作流执行失败: {result['error']}")
        sys.exit(1)
    
    # 输出结果摘要
    print("\n" + "=" * 70)
    print("📊 执行结果摘要")
    print("=" * 70)
    
    # 市场趋势
    trend = result.get("market_trend", {})
    print(f"\n🎯 市场趋势:")
    print(f"   方向: {trend.get('direction', 'N/A')}")
    print(f"   评分: {trend.get('ensemble_score', 0):.1f}")
    print(f"   仓位: {trend.get('position_limit', 0)*100:.0f}%")
    print(f"   模式: {trend.get('strategy_mode', 'N/A')}")
    
    # 主线
    mainlines = result.get("mainlines", [])
    print(f"\n🏆 市场主线 (Top 5):")
    for i, ml in enumerate(mainlines[:5]):
        print(f"   {i+1}. {ml.get('name', 'N/A')} ({ml.get('total_score', 0):.1f}分)")
    
    # 推荐股票
    recommendations = result.get("recommendations", {})
    stocks = recommendations.get("stocks", [])
    print(f"\n💎 推荐股票 (Top 10):")
    for i, stock in enumerate(stocks[:10]):
        name = stock.get('name') or stock.get('code', 'N/A')
        print(f"   {i+1}. {name} ({stock.get('code', '')}) - "
              f"{stock.get('total_score', 0):.1f}分 [{stock.get('signal', 'N/A')}]")
    
    # 交易策略
    strategy = result.get("trading_strategy", {})
    print(f"\n📋 交易策略:")
    print(f"   {strategy.get('position_advice', 'N/A')}")
    
    # 报告路径
    if result.get("report_path"):
        print(f"\n📄 完整报告:")
        print(f"   {result.get('report_path')}")
    
    print("\n" + "=" * 70)
    print("✅ V3.0 工作流执行完成!")
    print("=" * 70)
    
    return result


if __name__ == "__main__":
    main()
