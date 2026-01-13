#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报策略 V6.0 - 专业回测版本
==================================

使用VBTBacktestV5专业回测引擎

特点:
1. 止损止盈逻辑
2. 持仓跟踪（成本价、最高价、入场日期）
3. 交易成本计算（买入/卖出分别计算）
4. 数值异常检测

作者: TRQuant Team
版本: V6.0-professional
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
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

# AI主题核心股票
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


# ============== 数据构建 ==============

def build_data_matrices(
    stocks: List[str],
    start_date: str,
    end_date: str,
) -> Optional['DataMatrices']:
    """
    构建DataMatrices数据结构
    
    Args:
        stocks: 股票列表
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        DataMatrices或None
    """
    from core.research.data_provider import DataMatrices
    
    logger.info(f"  获取数据: {start_date} ~ {end_date}, {len(stocks)}只股票")
    
    try:
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
            logger.warning("  无法获取价格数据")
            return None
        
        # 转换为矩阵格式
        close = price_df.pivot(index='time', columns='code', values='close')
        open_ = price_df.pivot(index='time', columns='code', values='open')
        high = price_df.pivot(index='time', columns='code', values='high')
        low = price_df.pivot(index='time', columns='code', values='low')
        volume = price_df.pivot(index='time', columns='code', values='volume')
        
        # 过滤有效股票（至少有50%数据的）
        valid_ratio = close.notna().sum() / len(close)
        valid_stocks = valid_ratio[valid_ratio > 0.5].index.tolist()
        
        if not valid_stocks:
            logger.warning("  无有效股票")
            return None
        
        # 过滤并填充缺失值
        close = close[valid_stocks].ffill().bfill()
        open_ = open_[valid_stocks].ffill().bfill()
        high = high[valid_stocks].ffill().bfill()
        low = low[valid_stocks].ffill().bfill()
        volume = volume[valid_stocks].fillna(0)
        
        # 构建is_tradeable（简化：非停牌即可交易）
        is_tradeable = volume > 0
        
        data = DataMatrices(
            close=close,
            open=open_,
            high=high,
            low=low,
            volume=volume,
            is_tradeable=is_tradeable,
        )
        
        logger.info(f"  ✅ 数据构建完成: {data.shape}")
        return data
        
    except Exception as e:
        logger.error(f"  ❌ 数据获取失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def build_signals_from_strategy(
    data: 'DataMatrices',
    selected_stocks: List[str],
    rebalance_freq: int = 5,
) -> Optional['SignalMatrices']:
    """
    基于策略选股结果构建信号矩阵
    
    Args:
        data: 数据矩阵
        selected_stocks: 策略选中的股票
        rebalance_freq: 调仓频率（交易日数）
    
    Returns:
        SignalMatrices或None
    """
    from core.research.signals import SignalMatrices
    
    try:
        dates = data.dates
        symbols = data.symbols
        n_dates = len(dates)
        n_symbols = len(symbols)
        
        # 初始化矩阵
        entries = pd.DataFrame(False, index=dates, columns=symbols)
        exits = pd.DataFrame(False, index=dates, columns=symbols)
        scores = pd.DataFrame(0.0, index=dates, columns=symbols)
        target_weights = pd.DataFrame(0.0, index=dates, columns=symbols)
        
        # 设置调仓日
        rebalance_dates = [dates[i] for i in range(0, n_dates, rebalance_freq)]
        rebalance_mask = pd.Series(False, index=dates)
        rebalance_mask[rebalance_dates] = True
        
        # 过滤有效选中股票
        valid_selected = [s for s in selected_stocks if s in symbols]
        
        if not valid_selected:
            logger.warning("  无有效选中股票")
            return None
        
        # 在调仓日设置信号
        for date in rebalance_dates:
            entries.loc[date, valid_selected] = True
            
            # 等权重
            weight = 1.0 / len(valid_selected)
            target_weights.loc[date, valid_selected] = weight
            
            # 评分（使用当日收益率作为评分的一部分）
            for stock in valid_selected:
                scores.loc[date, stock] = 100.0  # 固定高分
        
        signals = SignalMatrices(
            entries=entries,
            exits=exits,
            scores=scores,
            target_weights=target_weights,
            rebalance_mask=rebalance_mask,
        )
        
        logger.info(f"  ✅ 信号构建完成: 调仓日={len(rebalance_dates)}, 选中股票={len(valid_selected)}")
        return signals
        
    except Exception as e:
        logger.error(f"  ❌ 信号构建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============== 回测函数 ==============

def run_professional_backtest(
    period: Dict,
    use_strategy: bool = True,
) -> Dict:
    """
    使用VBTBacktestV5运行专业回测
    
    Args:
        period: 时段配置
        use_strategy: 是否使用V6策略选股
    
    Returns:
        回测结果字典
    """
    from core.research.vbt_backtest_v5 import VBTBacktestV5
    from core.research.signals import SignalParams
    from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6
    
    name = period['name']
    start_date = period['start_date']
    end_date = period['end_date']
    
    result = {
        "period_name": name,
        "start_date": start_date,
        "end_date": end_date,
        "total_return": 0.0,
        "weekly_return": 0.0,
        "annual_return": 0.0,
        "max_drawdown": 0.0,
        "sharpe_ratio": 0.0,
        "win_rate": 0.0,
        "total_trades": 0,
        "selected_stocks": [],
        "error": None,
    }
    
    logger.info(f"\n{'='*60}")
    logger.info(f"时段: {name} ({start_date} ~ {end_date})")
    logger.info(f"{'='*60}")
    
    try:
        # 1. 构建数据矩阵
        logger.info("  [1/4] 构建数据矩阵...")
        start_time = time.time()
        
        data = build_data_matrices(AI_THEME_STOCKS, start_date, end_date)
        if data is None:
            result["error"] = "数据获取失败"
            return result
        
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 2. 策略选股
        logger.info("  [2/4] 策略选股...")
        start_time = time.time()
        
        if use_strategy:
            strategy = BullMarketStrategyV6(use_dynamic_mainline=False)
            decision = strategy.make_decision(
                as_of_date=start_date,
                candidate_stocks=AI_THEME_STOCKS,
                use_mainline=False,
            )
            
            if not decision.allow_trade or not decision.buy_targets:
                logger.warning("  策略不允许交易或无标的")
                result["error"] = "策略不允许交易"
                return result
            
            selected_stocks = [t['stock'] for t in decision.buy_targets]
            logger.info(f"  市场类型: {decision.market_type}")
            logger.info(f"  策略模式: {decision.strategy_mode}")
        else:
            # 直接使用全部股票
            selected_stocks = data.symbols
        
        result["selected_stocks"] = selected_stocks
        result["total_trades"] = len(selected_stocks)
        
        logger.info(f"  选中股票: {len(selected_stocks)}只")
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 3. 构建信号矩阵
        logger.info("  [3/4] 构建信号矩阵...")
        start_time = time.time()
        
        signals = build_signals_from_strategy(
            data=data,
            selected_stocks=selected_stocks,
            rebalance_freq=5,  # 周频调仓
        )
        
        if signals is None:
            result["error"] = "信号构建失败"
            return result
        
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 4. 运行VBTBacktestV5
        logger.info("  [4/4] 运行VBTBacktestV5专业回测...")
        start_time = time.time()
        
        # 配置信号参数
        params = SignalParams(
            max_positions=5,
            single_position_max=0.25,
            rebalance_period=5,
            stop_loss_pct=-0.08,
            take_profit_pct=0.30,
            trailing_stop_pct=-0.09,
            trailing_stop_trigger=0.15,
        )
        
        # 创建回测引擎（华泰证券标准）
        backtest = VBTBacktestV5(
            initial_cash=1_000_000,
            commission_rate=0.0001,  # 佣金: 0.01% (万分之一)
            stamp_duty=0.001,  # 印花税: 0.1% (千分之一，仅卖出)
            slippage=0.001,  # 滑点: 0.1%
            transfer_fee_rate=0.00001,  # 过户费: 0.001% (买卖双向)
            regulatory_fee_rate=0.0000687,  # 监管费: 0.00687% (买卖双向)
            min_commission=5.0,  # 最低佣金: 5元
        )
        
        # 运行回测
        backtest_result = backtest.run_with_signals(
            data=data,
            signals=signals,
            params=params,
        )
        
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 提取结果
        result["total_return"] = backtest_result.total_return
        result["annual_return"] = backtest_result.annual_return
        result["max_drawdown"] = backtest_result.max_drawdown
        result["sharpe_ratio"] = backtest_result.sharpe_ratio
        result["win_rate"] = backtest_result.win_rate
        
        # 计算周收益率
        trading_days = len(data.dates)
        weeks = trading_days / 5
        if weeks > 0:
            result["weekly_return"] = ((1 + result["total_return"]/100) ** (1/weeks) - 1) * 100
        else:
            result["weekly_return"] = result["total_return"]
        
        logger.info(f"  ✅ 回测完成!")
        logger.info(f"      总收益: {result['total_return']:.2f}%")
        logger.info(f"      周收益: {result['weekly_return']:.2f}%")
        logger.info(f"      年化: {result['annual_return']:.2f}%")
        logger.info(f"      夏普比: {result['sharpe_ratio']:.2f}")
        logger.info(f"      最大回撤: {result['max_drawdown']:.2f}%")
        logger.info(f"      胜率: {result['win_rate']:.2f}%")
        
    except Exception as e:
        logger.error(f"  ❌ 回测失败: {e}")
        import traceback
        traceback.print_exc()
        result["error"] = str(e)
    
    return result


# ============== 主函数 ==============

def main():
    """主函数"""
    print("="*70)
    print("牛市高回报策略 V6.0 - 专业回测 (VBTBacktestV5)")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 计算最近一个月
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    recent_month_period = {
        "name": "最近一个月",
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "description": "近一个月回测"
    }
    
    results = []
    
    # 只回测最近一个月
    print(f"\n[1/1] {recent_month_period['name']}")
    result = run_professional_backtest(recent_month_period, use_strategy=True)
    results.append(result)
    
    # 生成报告
    print("\n" + "="*70)
    print("回测结果汇总 (VBTBacktestV5专业引擎)")
    print("="*70)
    
    print("\n| 时段 | 总收益 | 周收益 | 年化 | 夏普 | 回撤 | 胜率 | 股票数 |")
    print("|------|--------|--------|------|------|------|------|--------|")
    
    for r in results:
        if r.get("error"):
            print(f"| {r['period_name']} | - | - | - | - | - | - | ❌ {r['error']} |")
        else:
            print(f"| {r['period_name']} | {r['total_return']:.2f}% | {r['weekly_return']:.2f}% | "
                  f"{r['annual_return']:.2f}% | {r['sharpe_ratio']:.2f} | {r['max_drawdown']:.2f}% | "
                  f"{r['win_rate']:.1f}% | {r['total_trades']} |")
    
    # 计算平均值
    valid_results = [r for r in results if not r.get("error")]
    if valid_results:
        avg_return = np.mean([r['total_return'] for r in valid_results])
        avg_weekly = np.mean([r['weekly_return'] for r in valid_results])
        avg_annual = np.mean([r['annual_return'] for r in valid_results])
        avg_sharpe = np.mean([r['sharpe_ratio'] for r in valid_results])
        avg_dd = np.mean([r['max_drawdown'] for r in valid_results])
        avg_wr = np.mean([r['win_rate'] for r in valid_results])
        
        print(f"| **平均** | **{avg_return:.2f}%** | **{avg_weekly:.2f}%** | "
              f"**{avg_annual:.2f}%** | **{avg_sharpe:.2f}** | **{avg_dd:.2f}%** | "
              f"**{avg_wr:.1f}%** | - |")
    
    # 保存报告
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/bull_market_v6_professional")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"backtest_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 牛市高回报策略 V6.0 专业回测报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**回测引擎**: VBTBacktestV5\n")
        f.write(f"**选股模式**: 固定AI主题 + V6策略决策\n\n")
        
        f.write("## 回测参数\n\n")
        f.write("### 交易成本（华泰证券标准）\n\n")
        f.write("| 参数 | 值 | 说明 |\n")
        f.write("|------|----|------|\n")
        f.write("| 初始资金 | 100万 | - |\n")
        f.write("| 佣金率 | 0.01% | 买卖双向 |\n")
        f.write("| 印花税 | 0.1% | 仅卖出 |\n")
        f.write("| 过户费 | 0.001% | 买卖双向 |\n")
        f.write("| 监管费 | 0.00687% | 买卖双向 |\n")
        f.write("| 滑点 | 0.1% | - |\n")
        f.write("| 最低佣金 | 5元 | 单笔最低 |\n\n")
        f.write("### 策略参数\n\n")
        f.write("| 参数 | 值 |\n")
        f.write("|------|----|\n")
        f.write("| 最大持仓 | 5只 |\n")
        f.write("| 单只上限 | 25% |\n")
        f.write("| 止损 | -8% |\n")
        f.write("| 止盈 | +30% |\n")
        f.write("| 移动止损 | -9%（盈利15%后启用）|\n\n")
        
        f.write("## 回测结果\n\n")
        f.write("| 时段 | 总收益 | 周收益 | 年化 | 夏普 | 回撤 | 胜率 |\n")
        f.write("|------|--------|--------|------|------|------|------|\n")
        
        for r in results:
            if r.get("error"):
                f.write(f"| {r['period_name']} | - | - | - | - | - | ❌ {r['error']} |\n")
            else:
                f.write(f"| {r['period_name']} | {r['total_return']:.2f}% | {r['weekly_return']:.2f}% | "
                       f"{r['annual_return']:.2f}% | {r['sharpe_ratio']:.2f} | {r['max_drawdown']:.2f}% | "
                       f"{r['win_rate']:.1f}% |\n")
        
        if valid_results:
            f.write(f"| **平均** | **{avg_return:.2f}%** | **{avg_weekly:.2f}%** | "
                   f"**{avg_annual:.2f}%** | **{avg_sharpe:.2f}** | **{avg_dd:.2f}%** | "
                   f"**{avg_wr:.1f}%** |\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results


if __name__ == "__main__":
    main()
