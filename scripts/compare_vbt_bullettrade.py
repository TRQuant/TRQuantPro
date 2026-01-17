#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vectorbt vs BulletTrade回测对比脚本
===================================

功能：
1. 使用相同参数运行两种回测
2. 对比结果差异
3. 分析差异原因
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import json
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalParams,
    VBTBacktest,
    BacktestResult,
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compare_backtest_results(
    vbt_result: BacktestResult,
    bt_result: Dict[str, Any],
) -> pd.DataFrame:
    """对比回测结果"""
    
    comparison = {
        '指标': [
            '总收益率(%)',
            '年化收益率(%)',
            '夏普比率',
            '最大回撤(%)',
            '胜率(%)',
            '总交易次数',
        ],
        'vectorbt': [
            vbt_result.total_return,
            vbt_result.annual_return,
            vbt_result.sharpe_ratio,
            vbt_result.max_drawdown,
            vbt_result.win_rate,
            vbt_result.total_trades,
        ],
        'BulletTrade': [
            bt_result.get('total_return', 0) * 100,
            bt_result.get('annual_return', 0) * 100,
            bt_result.get('sharpe_ratio', 0),
            bt_result.get('max_drawdown', 0) * 100,
            bt_result.get('win_rate', 0) * 100,
            bt_result.get('total_trades', 0),
        ],
    }
    
    df = pd.DataFrame(comparison)
    
    # 计算差异
    df['差异'] = df['vectorbt'] - df['BulletTrade']
    df['差异率(%)'] = (df['差异'] / (df['BulletTrade'].abs() + 1e-8)) * 100
    
    return df


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("vectorbt vs BulletTrade 回测对比")
    logger.info("=" * 60)
    
    # 1. 准备数据
    logger.info("Step 1: 准备数据...")
    provider = ResearchDataProvider(use_cache=True)
    stocks = provider.get_index_stocks('000300.XSHG')[:50]  # 50只股票
    data = provider.get_data_matrices(
        symbols=stocks,
        start_date='2023-01-01',
        end_date='2024-06-30',
    )
    logger.info(f"数据准备完成: shape={data.shape}")
    
    # 2. 计算因子
    logger.info("Step 2: 计算因子...")
    calculator = FactorCalculator(use_gpu=False)
    factors = calculator.calculate_factors(data)
    
    # 3. 设置参数
    params = SignalParams(
        min_mom_20d=5.0,
        max_mom_20d=50.0,
        max_rel_position=80.0,
        min_vol_ratio=1.0,
        max_positions=10,
        rebalance_period=5,
        stop_loss_pct=-0.08,  # 止损-8%
        take_profit_pct=0.30,  # 止盈+30%
        trailing_stop_pct=-0.08,
        trailing_stop_trigger=0.15,
        time_stop_days=20,
        partial_profit_1_pct=0.20,
        partial_profit_1_ratio=0.50,
    )
    
    # 4. 运行vectorbt回测
    logger.info("Step 3: 运行vectorbt回测...")
    vbt_backtest = VBTBacktest(initial_capital=1000000)
    vbt_result = vbt_backtest.run(data, factors, params)
    
    logger.info(f"vectorbt结果: 总收益={vbt_result.total_return:.2f}%, "
               f"年化={vbt_result.annual_return:.2f}%, "
               f"夏普={vbt_result.sharpe_ratio:.2f}")
    
    # 5. 运行BulletTrade回测（需要实现）
    logger.info("Step 4: 运行BulletTrade回测...")
    logger.warning("⚠️ BulletTrade回测需要实现")
    
    # TODO: 实现BulletTrade回测
    # from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest
    # bt_backtest = BulletTradeBacktest(...)
    # bt_result = bt_backtest.run_backtest(...)
    
    # 暂时使用空结果
    bt_result = {}
    
    # 6. 对比结果
    logger.info("Step 5: 对比结果...")
    if bt_result:
        comparison = compare_backtest_results(vbt_result, bt_result)
        print("\n" + "=" * 80)
        print(comparison.to_string(index=False))
        print("=" * 80)
    else:
        logger.warning("⚠️ BulletTrade回测未实现，无法对比")
    
    # 7. 分析差异（手动分析）
    logger.info("\n" + "=" * 60)
    logger.info("差异分析")
    logger.info("=" * 60)
    logger.info("""
    关键差异（已实现）：
    1. 止损止盈：✅ vectorbt已实现（固定止损、分批止盈、移动止损、时间止损）
    2. 持仓管理：✅ vectorbt已实现（成本价、最高价、入场日期跟踪）
    3. 交易成本：✅ vectorbt已实现（区分买入/卖出，精确计算佣金和印花税）
    4. 调仓逻辑：✅ vectorbt已实现（基于权重矩阵，支持止损止盈调整）
    
    后续工作：
    - 实现BulletTrade回测对比功能
    - 对比结果一致性验证
    """)


if __name__ == "__main__":
    main()
