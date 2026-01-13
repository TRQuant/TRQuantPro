#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报策略 V6.0 - 完整回测验证

使用聚宽数据进行V6策略回测，验证策略在不同牛市时段的表现

版本: V6.0
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
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
logger.info("JQData认证成功")


# 导入策略模块
from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6
from core.tenbagger.tenbagger_scorer import TenbaggerStage


@dataclass
class BacktestResult:
    """回测结果"""
    period_name: str
    start_date: str
    end_date: str
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    avg_holding_days: float
    best_trade: float
    worst_trade: float


def simple_backtest(
    strategy: BullMarketStrategyV6,
    stocks: List[str],
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000,
) -> BacktestResult:
    """
    简化版回测
    
    使用聚宽数据进行日频回测
    """
    logger.info(f"开始回测: {start_date} ~ {end_date}, 股票数={len(stocks)}")
    
    # 获取价格数据
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
        logger.warning("无法获取价格数据")
        return BacktestResult(
            period_name="",
            start_date=start_date,
            end_date=end_date,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
            avg_holding_days=0,
            best_trade=0,
            worst_trade=0,
        )
    
    # 转换为pivot格式
    close_df = price_df.pivot(index='time', columns='code', values='close')
    
    # 计算每日收益率
    returns_df = close_df.pct_change().fillna(0)
    
    # 使用策略选择的股票
    decision = strategy.make_decision(
        as_of_date=start_date,
        candidate_stocks=stocks,
    )
    
    # 获取买入目标
    if not decision.allow_trade or not decision.buy_targets:
        logger.warning("策略不允许交易或无买入目标")
        return BacktestResult(
            period_name="",
            start_date=start_date,
            end_date=end_date,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
            avg_holding_days=0,
            best_trade=0,
            worst_trade=0,
        )
    
    # 根据买入目标构建等权重组合
    selected_stocks = [t['stock'] for t in decision.buy_targets]
    
    # 修复股票代码格式问题：确保格式一致
    # JQData返回的code格式可能是 '300339.XSHE' 或 '300339'
    # 需要统一格式
    close_df_columns_normalized = {col: col for col in close_df.columns}
    # 尝试匹配：先精确匹配，再尝试去掉后缀
    matched_stocks = []
    for stock in selected_stocks:
        if stock in close_df.columns:
            matched_stocks.append(stock)
        else:
            # 尝试去掉后缀匹配
            stock_base = stock.split('.')[0] if '.' in stock else stock
            for col in close_df.columns:
                col_base = col.split('.')[0] if '.' in col else col
                if stock_base == col_base:
                    matched_stocks.append(col)
                    break
    
    selected_stocks = list(set(matched_stocks))  # 去重
    
    if not selected_stocks:
        logger.warning(f"没有可用的选中股票。策略选中: {[t['stock'] for t in decision.buy_targets]}, "
                      f"数据中有: {list(close_df.columns[:5])}...")
        return BacktestResult(
            period_name="",
            start_date=start_date,
            end_date=end_date,
            total_return=0,
            annual_return=0,
            max_drawdown=0,
            sharpe_ratio=0,
            win_rate=0,
            total_trades=0,
            avg_holding_days=0,
            best_trade=0,
            worst_trade=0,
        )
    
    logger.info(f"选中股票: {selected_stocks}")
    
    # 计算组合收益率（等权重）
    portfolio_returns = returns_df[selected_stocks].mean(axis=1)
    
    # 计算累计收益
    cumulative_returns = (1 + portfolio_returns).cumprod()
    
    # 计算指标
    total_return = (cumulative_returns.iloc[-1] - 1) * 100
    
    trading_days = len(portfolio_returns)
    years = trading_days / 252
    annual_return = ((1 + total_return/100) ** (1/years) - 1) * 100 if years > 0 else total_return
    
    # 最大回撤
    rolling_max = cumulative_returns.expanding().max()
    drawdowns = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = abs(drawdowns.min()) * 100
    
    # 夏普比率
    rf_rate = 0.03  # 无风险利率
    excess_returns = portfolio_returns - rf_rate/252
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() > 0 else 0
    
    # 胜率
    win_rate = (portfolio_returns > 0).sum() / len(portfolio_returns) * 100
    
    # 各股票收益
    stock_returns = {}
    for stock in selected_stocks:
        stock_cum = (1 + returns_df[stock]).cumprod()
        stock_returns[stock] = (stock_cum.iloc[-1] - 1) * 100
    
    best_trade = max(stock_returns.values()) if stock_returns else 0
    worst_trade = min(stock_returns.values()) if stock_returns else 0
    
    result = BacktestResult(
        period_name="",
        start_date=start_date,
        end_date=end_date,
        total_return=total_return,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
        sharpe_ratio=sharpe_ratio,
        win_rate=win_rate,
        total_trades=len(selected_stocks),
        avg_holding_days=trading_days,
        best_trade=best_trade,
        worst_trade=worst_trade,
    )
    
    logger.info(f"回测结果: 总收益={total_return:.2f}%, 年化={annual_return:.2f}%, 最大回撤={max_drawdown:.2f}%")
    
    return result


def run_v6_backtest():
    """运行V6策略回测"""
    
    logger.info("=" * 70)
    logger.info("牛市高回报策略 V6.0 - 完整回测验证")
    logger.info("=" * 70)
    
    # 定义牛市回测时段
    bull_market_periods = {
        "2024_policy_bull": {
            "start_date": "2024-09-20",
            "end_date": "2024-10-15",
            "description": "2024政策牛（快牛）",
        },
        "2024_year_end": {
            "start_date": "2024-11-15",
            "end_date": "2024-12-15",
            "description": "2024年末行情",
        },
        "2020_summer_bull": {
            "start_date": "2020-06-15",
            "end_date": "2020-07-31",
            "description": "2020夏季牛市",
        },
    }
    
    # AI智能体核心标的
    ai_targets = [
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
        "300496.XSHE",  # 中科创达
        "688271.XSHG",  # 联影医疗
        "300010.XSHE",  # 豆神教育
    ]
    
    # 初始化策略
    strategy = BullMarketStrategyV6()
    
    # 存储回测结果
    results = []
    
    for period_name, config in bull_market_periods.items():
        logger.info(f"\n{'='*50}")
        logger.info(f"回测时段: {period_name} - {config['description']}")
        logger.info(f"{'='*50}")
        
        result = simple_backtest(
            strategy=strategy,
            stocks=ai_targets,
            start_date=config['start_date'],
            end_date=config['end_date'],
        )
        
        result.period_name = period_name
        results.append(result)
    
    # 生成报告
    print("\n" + "=" * 70)
    print("📊 牛市高回报策略 V6.0 - 回测结果汇总")
    print("=" * 70)
    
    print(f"\n{'时段':<20} {'总收益':<12} {'年化收益':<12} {'最大回撤':<10} {'夏普比率':<10}")
    print("-" * 70)
    
    for r in results:
        print(f"{r.period_name:<20} {r.total_return:>10.2f}% {r.annual_return:>10.2f}% {r.max_drawdown:>8.2f}% {r.sharpe_ratio:>8.2f}")
    
    print("-" * 70)
    
    # 平均指标
    avg_return = sum(r.total_return for r in results) / len(results)
    avg_annual = sum(r.annual_return for r in results) / len(results)
    avg_drawdown = sum(r.max_drawdown for r in results) / len(results)
    avg_sharpe = sum(r.sharpe_ratio for r in results) / len(results)
    
    print(f"{'平均':<20} {avg_return:>10.2f}% {avg_annual:>10.2f}% {avg_drawdown:>8.2f}% {avg_sharpe:>8.2f}")
    
    print("\n" + "=" * 70)
    
    # 打印当前交易规则
    print(strategy.get_trading_rules())
    
    # 保存结果
    output = {
        "version": "V6.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": [
            {
                "period_name": r.period_name,
                "start_date": r.start_date,
                "end_date": r.end_date,
                "total_return": r.total_return,
                "annual_return": r.annual_return,
                "max_drawdown": r.max_drawdown,
                "sharpe_ratio": r.sharpe_ratio,
                "win_rate": r.win_rate,
                "total_trades": r.total_trades,
            }
            for r in results
        ],
        "summary": {
            "avg_total_return": avg_return,
            "avg_annual_return": avg_annual,
            "avg_max_drawdown": avg_drawdown,
            "avg_sharpe_ratio": avg_sharpe,
        }
    }
    
    output_path = f"/home/taotao/.cursor/worktrees/TRQuant/ope/output/bull_market_v6_backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n回测结果已保存到: {output_path}")
    
    return results


if __name__ == "__main__":
    run_v6_backtest()
