#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Backtest Script - 快速回测验证脚本
=====================================

按效率优先原则，分阶段验证：
1. 1个月快速验证 - 验证代码逻辑
2. 3个月短周期验证 - 验证信号质量
3. 6个月中周期验证 - 验证策略稳定性
4. 完整3年验证 - 最终确认
"""

import sys
import os缺少长期持有信号判断
缺少阶段转换判断
已
import time
import argparse
from datetime import datetime, timedelta

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_quick_backtest(period: str = "1m"):
    """运行快速回测
    
    Args:
        period: 回测周期 - 1m(1月), 3m(3月), 6m(6月), 1y(1年), 3y(3年)
    """
    from research.tenbagger_10x_strategy.scripts.tenbagger_5x_2year_strategy import (
        TenBagger5X2YearStrategy
    )
    
    # 计算时间范围（使用正式账号的数据范围：2005-2024）
    end_date = "2024-06-30"  # 使用较近的日期
    
    period_map = {
        "1m": 30,
        "3m": 90,
        "6m": 180,
        "1y": 365,
        "2y": 730,
        "3y": 1095
    }
    
    days = period_map.get(period, 30)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=days)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    logger.info(f"="*60)
    logger.info(f"快速回测 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"="*60)
    
    # 创建策略实例
    strategy = TenBagger5X2YearStrategy()
    
    # 运行回测
    start_time = time.time()
    
    try:
        result = strategy.run_backtest(start_date, end_date)
        elapsed = time.time() - start_time
        
        logger.info(f"\n{'='*60}")
        logger.info(f"回测完成 - 耗时: {elapsed:.1f}秒")
        logger.info(f"{'='*60}")
        
        if result:
            # 注意：_calc_result中已经乘以100了
            logger.info(f"总收益率: {result.total_return:.2f}%")
            logger.info(f"年化收益率: {result.annualized_return:.2f}%")
            logger.info(f"夏普比率: {result.sharpe_ratio:.2f}")
            logger.info(f"最大回撤: {result.max_drawdown:.2f}%")
            logger.info(f"胜率: {result.win_rate:.1f}%")
            logger.info(f"盈亏比: {result.profit_factor:.2f}")
            logger.info(f"交易次数: {result.total_trades}")
            
            # 显示环境表现
            if result.regime_performance:
                logger.info(f"\n市场环境表现:")
                for regime, perf in result.regime_performance.items():
                    logger.info(f"  {regime}: {perf:.2f}%")
            
            return result
        else:
            logger.error("回测返回空结果")
            return None
            
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"回测失败 (耗时{elapsed:.1f}秒): {e}")
        import traceback
        traceback.print_exc()
        return None


def run_progressive_validation():
    """渐进式验证"""
    stages = [
        ("1m", "1个月快速验证"),
        ("3m", "3个月短周期验证"),
        ("6m", "6个月中周期验证"),
    ]
    
    results = {}
    
    for period, desc in stages:
        logger.info(f"\n{'#'*60}")
        logger.info(f"# 阶段: {desc}")
        logger.info(f"{'#'*60}")
        
        result = run_quick_backtest(period)
        
        if result:
            results[period] = {
                'total_return': result.total_return,
                'sharpe_ratio': result.sharpe_ratio,
                'max_drawdown': result.max_drawdown,
                'win_rate': result.win_rate,
                'trades': result.total_trades
            }
            logger.info(f"✅ {desc} 完成")
        else:
            logger.error(f"❌ {desc} 失败")
            break  # 短周期失败则停止
    
    # 汇总结果
    if results:
        logger.info(f"\n{'='*60}")
        logger.info("渐进式验证汇总")
        logger.info(f"{'='*60}")
        
        print(f"\n{'周期':<10} {'收益率':<12} {'夏普':<10} {'回撤':<12} {'胜率':<10} {'交易':<8}")
        print("-" * 62)
        for period, data in results.items():
            print(f"{period:<10} {data['total_return']:>8.2f}%  "
                  f"{data['sharpe_ratio']:>8.2f}  "
                  f"{data['max_drawdown']:>8.2f}%  "
                  f"{data['win_rate']:>6.1f}%  "
                  f"{data['trades']:>6d}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="快速回测验证")
    parser.add_argument(
        "-p", "--period", 
        choices=["1m", "3m", "6m", "1y", "2y", "3y"],
        default="1m",
        help="回测周期"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="运行渐进式验证（1m -> 3m -> 6m）"
    )
    
    args = parser.parse_args()
    
    if args.all:
        run_progressive_validation()
    else:
        run_quick_backtest(args.period)
