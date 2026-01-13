#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高收益策略V7 - 多时段回测脚本
=================================

功能:
1. 对多个牛市时段进行回测验证
2. 生成详细的回测报告
3. 对比不同周期的策略表现

牛市时段定义:
- 2014-2015: 杠杆牛市
- 2019: 春季攻势
- 2020: 科技牛市
- 2024-Q4: 政策牛市

作者: TRQuant Team
版本: V7.0
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

# JQData认证
def init_jqdata():
    """初始化JQData"""
    import jqdatasdk as jq
    config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
    with open(config_path) as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    logger.info(f"JQData认证成功")


# ============== 牛市时段定义 ==============

BULL_MARKET_PERIODS = [
    # 2014-2015 杠杆牛市（取关键时段）
    {
        "name": "2014杠杆牛初期",
        "start": "2014-07-01",
        "end": "2014-08-31",
        "description": "券商启动，杠杆资金入场"
    },
    {
        "name": "2014杠杆牛加速",
        "start": "2014-11-01",
        "end": "2014-12-31",
        "description": "全面启动，疯牛行情"
    },
    
    # 2019春季攻势
    {
        "name": "2019春季攻势",
        "start": "2019-02-01",
        "end": "2019-04-15",
        "description": "科创板预热，成长股反弹"
    },
    
    # 2020科技牛市
    {
        "name": "2020科技牛",
        "start": "2020-06-01",
        "end": "2020-07-31",
        "description": "科技消费双驱动"
    },
    
    # 2024政策牛市
    {
        "name": "2024政策牛初期",
        "start": "2024-09-20",
        "end": "2024-10-15",
        "description": "政策大转向，指数暴涨"
    },
    {
        "name": "2024政策牛延续",
        "start": "2024-11-01",
        "end": "2024-12-15",
        "description": "结构性行情，AI主线"
    },
    
    # 2025年初行情
    {
        "name": "2025年初行情",
        "start": "2025-01-02",
        "end": "2025-02-28",
        "description": "AI概念延续"
    },
]


# ============== 主函数 ==============

def main():
    """主函数"""
    print("="*70)
    print("牛市高收益策略V7 - 多时段回测")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 初始化JQData
    init_jqdata()
    
    # 2. 创建输出目录
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/bull_market_v7")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. 导入策略
    from core.strategy.bull_market_strategy_v7 import (
        BullMarketStrategyV7, StrategyConfigV7,
        StopLossConfig, TradeCostModel
    )
    
    # 4. 配置策略
    cost_model = TradeCostModel(
        commission_rate=0.0003,   # 万三佣金
        stamp_tax_rate=0.001,    # 千一印花税
        slippage=0.001,          # 千一滑点
        min_commission=5.0,      # 最低5元
    )
    
    stop_loss_config = StopLossConfig(
        stop_loss_pct=-0.10,           # 10%止损
        take_profit_pct=0.30,          # 30%止盈
        trailing_stop_pct=-0.09,       # 9%移动止损
        trailing_stop_trigger=0.15,    # 盈利15%启动移动止损
        time_stop_days=20,             # 20日时间止损
        soft_stop_enabled=True,        # 启用软止损
    )
    
    config = StrategyConfigV7(
        initial_capital=1000000,
        max_stocks_per_period=200,     # 每期最多200只
        cost_model=cost_model,
        stop_loss_config=stop_loss_config,
        use_cycle_adaptive=True,       # 启用周期自适应
        use_mainline_selection=True,   # 启用主线选股
        top_n_mainlines=3,             # 取Top3主线
    )
    
    # 5. 创建策略实例
    strategy = BullMarketStrategyV7(config)
    
    # 6. 运行多时段回测
    print(f"\n开始回测 {len(BULL_MARKET_PERIODS)} 个牛市时段...")
    print("-"*70)
    
    results = []
    
    for i, period in enumerate(BULL_MARKET_PERIODS, 1):
        name = period['name']
        start = period['start']
        end = period['end']
        desc = period.get('description', '')
        
        print(f"\n[{i}/{len(BULL_MARKET_PERIODS)}] {name}")
        print(f"    时间: {start} ~ {end}")
        print(f"    描述: {desc}")
        
        try:
            result = strategy.run_period(
                start_date=start,
                end_date=end,
                period_name=name,
            )
            
            results.append(result)
            
            print(f"    结果: 总收益={result.total_return:.2f}%, "
                  f"周收益={result.weekly_return:.2f}%, "
                  f"夏普={result.sharpe_ratio:.2f}")
            
            # 重置回测引擎
            strategy._backtest_engine = None
            
        except Exception as e:
            logger.error(f"    失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 7. 生成报告
    print("\n" + "="*70)
    print("生成回测报告...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"bull_market_v7_report_{timestamp}.md"
    
    report_text = strategy.generate_report(results, str(report_path))
    
    # 8. 保存详细结果
    results_data = [r.to_dict() for r in results]
    results_path = output_dir / f"bull_market_v7_results_{timestamp}.json"
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    # 9. 打印汇总
    print("\n" + "="*70)
    print("回测结果汇总")
    print("="*70)
    
    print("\n| 时段 | 周期 | 总收益 | 周收益 | 夏普 | 回撤 |")
    print("|------|------|--------|--------|------|------|")
    
    for r in results:
        print(f"| {r.period} | {r.cycle} | {r.total_return:.2f}% | "
              f"{r.weekly_return:.2f}% | {r.sharpe_ratio:.2f} | {r.max_drawdown:.2f}% |")
    
    # 平均值
    if results:
        avg_return = np.mean([r.total_return for r in results if r.total_return != 0])
        avg_weekly = np.mean([r.weekly_return for r in results if r.weekly_return != 0])
        avg_sharpe = np.mean([r.sharpe_ratio for r in results if r.sharpe_ratio != 0])
        
        print("-"*70)
        print(f"| **平均** | - | **{avg_return:.2f}%** | **{avg_weekly:.2f}%** | **{avg_sharpe:.2f}** | - |")
    
    print(f"\n报告保存至: {report_path}")
    print(f"结果保存至: {results_path}")
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results


if __name__ == "__main__":
    main()
