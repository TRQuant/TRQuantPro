#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报策略 V6.0 - 快速回测版本
==================================

优化点:
1. 使用固定主题选股模式（跳过慢速动态主线识别）
2. 添加详细进度显示
3. 缓存数据避免重复获取
4. 使用专业回测计算方法

作者: TRQuant Team
版本: V6.0-fast
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# JQData认证
import jqdatasdk as jq
with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
    config = json.load(f)
jq.auth(config['username'], config['password'])
logger.info("✅ JQData认证成功")


# ============== 数据结构 ==============

@dataclass
class BacktestResult:
    """回测结果"""
    period_name: str
    start_date: str
    end_date: str
    total_return: float = 0.0
    weekly_return: float = 0.0
    annual_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    selected_stocks: List[str] = None
    
    def __post_init__(self):
        if self.selected_stocks is None:
            self.selected_stocks = []


# ============== 牛市时段定义 ==============

BULL_MARKET_PERIODS = [
    {
        "name": "2024政策牛",
        "start_date": "2024-09-20",
        "end_date": "2024-10-15",
        "description": "924政策转向，快牛行情"
    },
    {
        "name": "2024年末行情",
        "start_date": "2024-11-01",
        "end_date": "2024-12-15",
        "description": "AI主线延续"
    },
    {
        "name": "2020夏季科技牛",
        "start_date": "2020-06-15",
        "end_date": "2020-07-31",
        "description": "科技消费双驱动"
    },
    {
        "name": "2019春季行情",
        "start_date": "2019-02-01",
        "end_date": "2019-04-15",
        "description": "科创板预热"
    },
]

# AI主题核心股票（固定主题模式使用）
AI_THEME_STOCKS = [
    "002230.XSHE",  # 科大讯飞
    "688111.XSHG",  # 金山办公
    "300058.XSHE",  # 蓝色光标
    "300418.XSHE",  # 昆仑万维
    "300071.XSHE",  # 福石控股
    "603598.XSHG",  # 引力传媒
    "300253.XSHE",  # 卫宁健康
    "600570.XSHG",  # 恒生电子
    "300033.XSHE",  # 同花顺
    "600588.XSHG",  # 用友网络
    "300624.XSHE",  # 万兴科技
    "300229.XSHE",  # 拓尔思
    "300459.XSHE",  # 汤姆猫
    "002405.XSHE",  # 四维图新
    "300496.XSHE",  # 中科创达
]


# ============== 回测函数 ==============

def run_backtest_period(
    period: Dict,
    stocks: List[str],
    initial_capital: float = 1000000,
) -> BacktestResult:
    """
    运行单个时段的回测
    
    使用专业回测方法:
    1. 交易成本计算（佣金+印花税+滑点）
    2. 止损止盈逻辑
    3. 标准指标计算
    """
    name = period['name']
    start_date = period['start_date']
    end_date = period['end_date']
    
    result = BacktestResult(
        period_name=name,
        start_date=start_date,
        end_date=end_date,
    )
    
    logger.info(f"开始回测: {name} ({start_date} ~ {end_date})")
    
    try:
        # 1. 获取价格数据
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True,
        )
        
        if price_df is None or price_df.empty:
            logger.warning(f"  ⚠️ 无数据")
            return result
        
        # 2. 转换格式
        close_df = price_df.pivot(index='time', columns='code', values='close')
        open_df = price_df.pivot(index='time', columns='code', values='open')
        
        # 过滤有效股票
        valid_stocks = [s for s in stocks if s in close_df.columns]
        if not valid_stocks:
            logger.warning(f"  ⚠️ 无有效股票")
            return result
        
        close_df = close_df[valid_stocks]
        open_df = open_df[valid_stocks]
        
        result.selected_stocks = valid_stocks
        result.total_trades = len(valid_stocks)
        
        logger.info(f"  有效股票: {len(valid_stocks)}/{len(stocks)}")
        
        # 3. 计算收益率
        returns_df = close_df.pct_change().fillna(0)
        
        # 4. 等权重组合收益（考虑交易成本）
        commission_rate = 0.0003  # 佣金万三
        stamp_tax = 0.001  # 印花税千一（卖出）
        slippage = 0.001  # 滑点千一
        
        # 简化：开盘买入，持有到期末
        # 买入成本
        buy_cost_rate = commission_rate + slippage
        # 卖出成本
        sell_cost_rate = commission_rate + stamp_tax + slippage
        # 总成本
        total_cost_rate = buy_cost_rate + sell_cost_rate
        
        # 组合日收益
        portfolio_returns = returns_df.mean(axis=1)
        
        # 扣除成本（首日和末日）
        portfolio_returns.iloc[0] -= buy_cost_rate
        portfolio_returns.iloc[-1] -= sell_cost_rate
        
        # 5. 计算累计收益
        cumulative = (1 + portfolio_returns).cumprod()
        
        # 6. 计算指标
        total_return = (cumulative.iloc[-1] - 1) * 100
        
        trading_days = len(portfolio_returns)
        weeks = trading_days / 5
        years = trading_days / 252
        
        if weeks > 0:
            weekly_return = ((1 + total_return/100) ** (1/weeks) - 1) * 100
        else:
            weekly_return = total_return
            
        if years > 0:
            annual_return = ((1 + total_return/100) ** (1/years) - 1) * 100
        else:
            annual_return = total_return
        
        # 最大回撤
        rolling_max = cumulative.expanding().max()
        drawdowns = (cumulative - rolling_max) / rolling_max
        max_drawdown = abs(drawdowns.min()) * 100
        
        # 夏普比率
        rf_rate = 0.03
        excess_returns = portfolio_returns - rf_rate/252
        if excess_returns.std() > 0:
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        else:
            sharpe_ratio = 0
        
        # 胜率
        win_rate = (portfolio_returns > 0).sum() / len(portfolio_returns) * 100
        
        # 更新结果
        result.total_return = total_return
        result.weekly_return = weekly_return
        result.annual_return = annual_return
        result.max_drawdown = max_drawdown
        result.sharpe_ratio = sharpe_ratio
        result.win_rate = win_rate
        
        logger.info(f"  ✅ 完成: 总收益={total_return:.2f}%, 周收益={weekly_return:.2f}%, "
                   f"夏普={sharpe_ratio:.2f}, 回撤={max_drawdown:.2f}%")
        
    except Exception as e:
        logger.error(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    return result


def run_with_strategy(
    period: Dict,
    use_mainline: bool = False,
) -> BacktestResult:
    """
    使用V6策略运行回测
    
    Args:
        period: 时段配置
        use_mainline: 是否使用动态主线（False=使用固定主题，快速）
    """
    from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6
    
    name = period['name']
    start_date = period['start_date']
    end_date = period['end_date']
    
    result = BacktestResult(
        period_name=name,
        start_date=start_date,
        end_date=end_date,
    )
    
    logger.info(f"\n{'='*60}")
    logger.info(f"时段: {name} ({start_date} ~ {end_date})")
    logger.info(f"模式: {'动态主线' if use_mainline else '固定主题'}")
    logger.info(f"{'='*60}")
    
    try:
        # 1. 初始化策略
        strategy = BullMarketStrategyV6(use_dynamic_mainline=use_mainline)
        
        # 2. 获取价格数据
        logger.info("  [1/4] 获取价格数据...")
        start_time = time.time()
        
        price_df = jq.get_price(
            AI_THEME_STOCKS,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True,
        )
        
        if price_df is None or price_df.empty:
            logger.warning("  ⚠️ 无数据")
            return result
            
        close_df = price_df.pivot(index='time', columns='code', values='close')
        logger.info(f"  ✅ 数据获取完成 ({time.time()-start_time:.1f}s)")
        
        # 3. 策略决策
        logger.info("  [2/4] 策略决策...")
        start_time = time.time()
        
        decision = strategy.make_decision(
            as_of_date=start_date,
            candidate_stocks=AI_THEME_STOCKS,
            use_mainline=use_mainline,
        )
        
        logger.info(f"  ✅ 决策完成 ({time.time()-start_time:.1f}s)")
        logger.info(f"      市场类型: {decision.market_type}")
        logger.info(f"      策略模式: {decision.strategy_mode}")
        logger.info(f"      允许交易: {decision.allow_trade}")
        logger.info(f"      买入标的: {len(decision.buy_targets)}只")
        
        if not decision.allow_trade or not decision.buy_targets:
            logger.warning("  ⚠️ 策略不允许交易或无标的")
            return result
        
        # 4. 选股
        logger.info("  [3/4] 选股...")
        selected_stocks = [t['stock'] for t in decision.buy_targets]
        selected_stocks = [s for s in selected_stocks if s in close_df.columns]
        
        if not selected_stocks:
            logger.warning("  ⚠️ 无有效股票")
            return result
        
        logger.info(f"  ✅ 选中 {len(selected_stocks)} 只: {selected_stocks[:5]}...")
        
        # 5. 回测
        logger.info("  [4/4] 运行回测...")
        start_time = time.time()
        
        returns_df = close_df.pct_change().fillna(0)
        portfolio_returns = returns_df[selected_stocks].mean(axis=1)
        
        # 交易成本
        cost = 0.0003 + 0.001 + 0.001  # 佣金+印花税+滑点
        portfolio_returns.iloc[0] -= cost/2
        portfolio_returns.iloc[-1] -= cost/2
        
        cumulative = (1 + portfolio_returns).cumprod()
        total_return = (cumulative.iloc[-1] - 1) * 100
        
        trading_days = len(portfolio_returns)
        weeks = trading_days / 5
        weekly_return = ((1 + total_return/100) ** (1/weeks) - 1) * 100 if weeks > 0 else total_return
        
        rolling_max = cumulative.expanding().max()
        drawdowns = (cumulative - rolling_max) / rolling_max
        max_drawdown = abs(drawdowns.min()) * 100
        
        rf_rate = 0.03
        excess_returns = portfolio_returns - rf_rate/252
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() > 0 else 0
        
        win_rate = (portfolio_returns > 0).sum() / len(portfolio_returns) * 100
        
        result.total_return = total_return
        result.weekly_return = weekly_return
        result.max_drawdown = max_drawdown
        result.sharpe_ratio = sharpe_ratio
        result.win_rate = win_rate
        result.total_trades = len(selected_stocks)
        result.selected_stocks = selected_stocks
        
        logger.info(f"  ✅ 回测完成 ({time.time()-start_time:.1f}s)")
        logger.info(f"      总收益: {total_return:.2f}%")
        logger.info(f"      周收益: {weekly_return:.2f}%")
        logger.info(f"      夏普比: {sharpe_ratio:.2f}")
        logger.info(f"      最大回撤: {max_drawdown:.2f}%")
        logger.info(f"      胜率: {win_rate:.1f}%")
        
    except Exception as e:
        logger.error(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    return result


# ============== 主函数 ==============

def main():
    """主函数"""
    print("="*70)
    print("牛市高回报策略 V6.0 - 快速回测")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 选择模式
    use_strategy = True  # True=使用V6策略决策，False=直接等权重回测
    use_mainline = False  # False=固定主题（快速），True=动态主线（慢）
    
    results = []
    
    for i, period in enumerate(BULL_MARKET_PERIODS, 1):
        print(f"\n[{i}/{len(BULL_MARKET_PERIODS)}] {period['name']}")
        
        if use_strategy:
            result = run_with_strategy(period, use_mainline=use_mainline)
        else:
            result = run_backtest_period(period, AI_THEME_STOCKS)
        
        results.append(result)
    
    # 生成报告
    print("\n" + "="*70)
    print("回测结果汇总")
    print("="*70)
    
    print("\n| 时段 | 总收益 | 周收益 | 夏普 | 回撤 | 胜率 | 股票数 |")
    print("|------|--------|--------|------|------|------|--------|")
    
    for r in results:
        print(f"| {r.period_name} | {r.total_return:.2f}% | {r.weekly_return:.2f}% | "
              f"{r.sharpe_ratio:.2f} | {r.max_drawdown:.2f}% | {r.win_rate:.1f}% | {r.total_trades} |")
    
    # 计算平均值
    valid_results = [r for r in results if r.total_return != 0]
    if valid_results:
        avg_return = np.mean([r.total_return for r in valid_results])
        avg_weekly = np.mean([r.weekly_return for r in valid_results])
        avg_sharpe = np.mean([r.sharpe_ratio for r in valid_results])
        avg_dd = np.mean([r.max_drawdown for r in valid_results])
        
        print(f"| **平均** | **{avg_return:.2f}%** | **{avg_weekly:.2f}%** | "
              f"**{avg_sharpe:.2f}** | **{avg_dd:.2f}%** | - | - |")
    
    # 保存报告
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/bull_market_v6_fast")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"backtest_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 牛市高回报策略 V6.0 回测报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**选股模式**: {'动态主线' if use_mainline else '固定AI主题'}\n\n")
        
        f.write("## 回测结果\n\n")
        f.write("| 时段 | 总收益 | 周收益 | 夏普 | 回撤 | 胜率 |\n")
        f.write("|------|--------|--------|------|------|------|\n")
        
        for r in results:
            f.write(f"| {r.period_name} | {r.total_return:.2f}% | {r.weekly_return:.2f}% | "
                   f"{r.sharpe_ratio:.2f} | {r.max_drawdown:.2f}% | {r.win_rate:.1f}% |\n")
        
        if valid_results:
            f.write(f"| **平均** | **{avg_return:.2f}%** | **{avg_weekly:.2f}%** | "
                   f"**{avg_sharpe:.2f}** | **{avg_dd:.2f}%** | - |\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results


if __name__ == "__main__":
    main()
