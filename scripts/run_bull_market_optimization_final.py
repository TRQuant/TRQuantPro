#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 - 最终优化脚本
=================================

目标：周频10%收益

功能：
1. 全A股股票池（约3000只）
2. 完整因子体系（动量+涨停+突破+资金流向）
3. 多信号类型评分
4. 牛市时段回测验证
5. 递归参数优化

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from itertools import product
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

# 设置JQData环境变量
os.environ["JQDATA_USER"] = "13327806797"
os.environ["JQDATA_PASSWORD"] = "Taorui888"

from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalEngine,
    SignalParams,
    VBTBacktest,
    BacktestResult,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "bull_market_final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class BullMarketParams:
    """牛市策略参数（基于已优化结果）"""
    # 动量阈值
    min_mom_20d: float = -1.25
    max_mom_20d: float = 25.0
    max_rel_position: float = 80.0
    min_vol_ratio: float = 1.0
    
    # 涨停因子阈值
    limit_up_threshold: float = 0.093
    vol_ratio_threshold_first: float = 2.5
    
    # 突破因子阈值
    mom_5d_threshold_breakout: float = 16.0
    vol_ratio_threshold_breakout: float = 1.5
    breakout_ratio_min: float = 5.0
    
    # 资金流向阈值
    min_flow_strength: float = 0.5
    
    # 信号阈值
    min_signal_score: float = 55.0
    
    # 持仓配置
    max_positions: int = 5
    single_position_max: float = 0.2
    rebalance_period: int = 5
    
    # 止损止盈
    stop_loss_pct: float = -0.10
    take_profit_pct: float = 0.30
    trailing_stop_pct: float = -0.09
    trailing_stop_trigger: float = 0.15
    time_stop_days: int = 20
    partial_profit_1_pct: float = 0.20
    partial_profit_1_ratio: float = 0.50
    
    def to_signal_params(self) -> SignalParams:
        """转换为SignalParams"""
        return SignalParams(
            min_mom_20d=self.min_mom_20d,
            max_mom_20d=self.max_mom_20d,
            max_rel_position=self.max_rel_position,
            min_vol_ratio=self.min_vol_ratio,
            limit_up_threshold=self.limit_up_threshold,
            vol_ratio_threshold_first=self.vol_ratio_threshold_first,
            mom_5d_threshold_breakout=self.mom_5d_threshold_breakout,
            vol_ratio_threshold_breakout=self.vol_ratio_threshold_breakout,
            breakout_ratio_min=self.breakout_ratio_min,
            min_flow_strength=self.min_flow_strength,
            min_signal_score=self.min_signal_score,
            max_positions=self.max_positions,
            single_position_max=self.single_position_max,
            rebalance_period=self.rebalance_period,
            stop_loss_pct=self.stop_loss_pct,
            take_profit_pct=self.take_profit_pct,
            trailing_stop_pct=self.trailing_stop_pct,
            trailing_stop_trigger=self.trailing_stop_trigger,
            time_stop_days=self.time_stop_days,
            partial_profit_1_pct=self.partial_profit_1_pct,
            partial_profit_1_ratio=self.partial_profit_1_ratio,
        )


# 牛市时段定义
BULL_MARKET_PERIODS = {
    "2019_spring": {
        "train": ("2019-01-01", "2019-03-15"),
        "validate": ("2019-03-16", "2019-04-30"),
        "description": "科创板预期牛市"
    },
    "2020_summer": {
        "train": ("2020-07-01", "2020-08-15"),
        "validate": ("2020-08-16", "2020-09-30"),
        "description": "流动性牛市"
    },
    "2024_policy": {
        "train": ("2024-09-20", "2024-11-15"),
        "validate": ("2024-11-16", "2024-12-31"),
        "description": "政策牛市"
    },
}


def run_single_backtest(
    data: Any,
    factors: Any,
    params: BullMarketParams,
    initial_capital: float = 1000000,
) -> BacktestResult:
    """运行单次回测"""
    signal_params = params.to_signal_params()
    
    # 生成信号
    engine = SignalEngine(params=signal_params)
    signals = engine.generate_signals(data, factors, signal_params)
    
    # 运行回测
    backtest = VBTBacktest(initial_capital=initial_capital)
    result = backtest.run(data, factors, signal_params)
    
    return result


def calculate_score(result: BacktestResult) -> float:
    """计算综合评分（目标：周频10%）"""
    # 周收益率目标
    weekly_return = result.total_return / max(1, result.trading_days / 5)
    
    # 评分公式
    score = 0.0
    
    # 年化收益（权重40%）
    if result.annual_return > 0:
        score += min(result.annual_return, 200) * 0.4
    
    # 夏普比率（权重20%）
    if result.sharpe_ratio > 0:
        score += min(result.sharpe_ratio * 20, 60) * 0.2
    
    # 最大回撤惩罚（权重20%）
    drawdown_penalty = max(0, 30 - result.max_drawdown)
    score += drawdown_penalty * 0.2
    
    # 周收益率（权重20%，目标10%）
    weekly_score = min(weekly_return * 10, 100) * 0.2
    score += weekly_score
    
    return score


def generate_param_grid() -> List[BullMarketParams]:
    """生成参数网格（基于已优化结果微调）"""
    base_params = BullMarketParams()
    
    # 微调参数范围
    param_space = {
        # 止损止盈微调
        "stop_loss_pct": [-0.08, -0.10, -0.12],
        "take_profit_pct": [0.25, 0.30, 0.35],
        "trailing_stop_pct": [-0.08, -0.09, -0.10],
        
        # 持仓配置
        "max_positions": [3, 5, 8],
        
        # 资金流向阈值
        "min_flow_strength": [0.0, 0.3, 0.5],
    }
    
    # 生成所有组合
    param_list = []
    keys = list(param_space.keys())
    values = list(param_space.values())
    
    for combo in product(*values):
        params = BullMarketParams()
        for key, value in zip(keys, combo):
            setattr(params, key, value)
        param_list.append(params)
    
    logger.info(f"生成参数组合: {len(param_list)} 个")
    return param_list


def run_optimization(
    stocks: List[str],
    period: Dict[str, Tuple[str, str]],
    max_stocks: int = 500,
) -> Tuple[BullMarketParams, BacktestResult, List[Dict]]:
    """运行优化"""
    logger.info(f"开始优化: {period['description']}")
    logger.info(f"训练集: {period['train']}, 验证集: {period['validate']}")
    
    # 限制股票数量（加速测试）
    test_stocks = stocks[:max_stocks]
    logger.info(f"使用 {len(test_stocks)} 只股票")
    
    # 获取数据
    provider = ResearchDataProvider(use_cache=True)
    
    # 训练集数据
    train_start, train_end = period["train"]
    train_data = provider.get_data_matrices(
        symbols=test_stocks,
        start_date=train_start,
        end_date=train_end,
    )
    
    # 验证集数据
    val_start, val_end = period["validate"]
    val_data = provider.get_data_matrices(
        symbols=test_stocks,
        start_date=val_start,
        end_date=val_end,
    )
    
    # 计算因子
    calculator = FactorCalculator(use_gpu=False)
    train_factors = calculator.calculate_factors(train_data)
    val_factors = calculator.calculate_factors(val_data)
    
    # 生成参数网格
    param_grid = generate_param_grid()
    
    # 遍历参数组合
    results = []
    best_score = -float('inf')
    best_params = None
    best_result = None
    
    for i, params in enumerate(param_grid):
        try:
            # 训练集回测
            train_result = run_single_backtest(train_data, train_factors, params)
            train_score = calculate_score(train_result)
            
            # 验证集回测
            val_result = run_single_backtest(val_data, val_factors, params)
            val_score = calculate_score(val_result)
            
            # 过拟合检测
            if train_score > 0:
                overfit_ratio = abs(val_score - train_score) / train_score
            else:
                overfit_ratio = 1.0
            
            # 记录结果
            result_dict = {
                "combo_id": i + 1,
                "params": asdict(params),
                "train_score": train_score,
                "val_score": val_score,
                "overfit_ratio": overfit_ratio,
                "train_return": train_result.total_return,
                "val_return": val_result.total_return,
                "train_sharpe": train_result.sharpe_ratio,
                "val_sharpe": val_result.sharpe_ratio,
                "train_drawdown": train_result.max_drawdown,
                "val_drawdown": val_result.max_drawdown,
            }
            results.append(result_dict)
            
            # 更新最优
            final_score = val_score * (1 - 0.2 * overfit_ratio)
            if final_score > best_score:
                best_score = final_score
                best_params = params
                best_result = val_result
            
            if (i + 1) % 10 == 0:
                logger.info(f"进度: {i+1}/{len(param_grid)}, "
                           f"当前最优验证集评分: {best_score:.2f}")
                
        except Exception as e:
            logger.error(f"组合 {i+1} 失败: {e}")
            continue
    
    logger.info(f"优化完成! 最优验证集评分: {best_score:.2f}")
    logger.info(f"最优参数: stop_loss={best_params.stop_loss_pct}, "
               f"take_profit={best_params.take_profit_pct}, "
               f"max_positions={best_params.max_positions}")
    
    return best_params, best_result, results


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("牛市极端高收益策略 - 最终优化")
    logger.info(f"目标: 周频10%收益")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    # 获取全A股
    logger.info("Step 1: 获取全A股股票列表...")
    provider = ResearchDataProvider(use_cache=True)
    try:
        all_stocks = provider.get_all_a_stocks(exclude_st=True, exclude_kcb=True)
        logger.info(f"全A股: {len(all_stocks)} 只")
    except Exception as e:
        logger.warning(f"获取全A股失败: {e}, 使用沪深300")
        all_stocks = provider.get_index_stocks("000300.XSHG")
    
    # 选择牛市时段
    period_name = "2020_summer"  # 使用流动性牛市作为主要测试
    period = BULL_MARKET_PERIODS[period_name]
    
    logger.info(f"\nStep 2: 运行优化 ({period['description']})...")
    
    # 运行优化
    best_params, best_result, all_results = run_optimization(
        stocks=all_stocks,
        period=period,
        max_stocks=300,  # 限制300只加速
    )
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存最优参数
    best_params_path = OUTPUT_DIR / f"best_params_{timestamp}.json"
    with open(best_params_path, "w") as f:
        json.dump({
            "params": asdict(best_params),
            "result": {
                "total_return": best_result.total_return,
                "annual_return": best_result.annual_return,
                "sharpe_ratio": best_result.sharpe_ratio,
                "max_drawdown": best_result.max_drawdown,
                "win_rate": best_result.win_rate,
                "total_trades": best_result.total_trades,
            },
            "period": period,
            "timestamp": timestamp,
        }, f, indent=2)
    logger.info(f"最优参数已保存: {best_params_path}")
    
    # 保存优化历史
    history_path = OUTPUT_DIR / f"optimization_history_{timestamp}.csv"
    history_df = pd.DataFrame(all_results)
    history_df.to_csv(history_path, index=False)
    logger.info(f"优化历史已保存: {history_path}")
    
    # 生成报告
    report_path = OUTPUT_DIR / f"optimization_report_{timestamp}.md"
    with open(report_path, "w") as f:
        f.write("# 牛市极端高收益策略 - 优化报告\n\n")
        f.write(f"**生成时间**: {timestamp}\n")
        f.write(f"**牛市时段**: {period['description']} ({period['train'][0]} ~ {period['validate'][1]})\n\n")
        
        f.write("## 最优参数\n\n")
        f.write("| 参数 | 值 |\n")
        f.write("|------|----|\n")
        for key, value in asdict(best_params).items():
            f.write(f"| {key} | {value} |\n")
        
        f.write("\n## 回测结果\n\n")
        f.write("| 指标 | 值 |\n")
        f.write("|------|----|\n")
        f.write(f"| 总收益率 | {best_result.total_return:.2f}% |\n")
        f.write(f"| 年化收益率 | {best_result.annual_return:.2f}% |\n")
        f.write(f"| 夏普比率 | {best_result.sharpe_ratio:.2f} |\n")
        f.write(f"| 最大回撤 | {best_result.max_drawdown:.2f}% |\n")
        f.write(f"| 胜率 | {best_result.win_rate:.2f}% |\n")
        f.write(f"| 总交易次数 | {best_result.total_trades} |\n")
        
        weekly_return = best_result.total_return / max(1, best_result.trading_days / 5)
        f.write(f"\n**周均收益率**: {weekly_return:.2f}%\n")
        
        if weekly_return >= 10:
            f.write("\n✅ **达到周频10%收益目标**\n")
        else:
            f.write(f"\n⚠️ **距离目标还差 {10 - weekly_return:.2f}%**\n")
    
    logger.info(f"报告已保存: {report_path}")
    
    # 输出总结
    elapsed = datetime.now() - start_time
    logger.info("\n" + "=" * 60)
    logger.info("优化完成!")
    logger.info(f"耗时: {elapsed.total_seconds():.1f} 秒")
    logger.info(f"最优年化收益: {best_result.annual_return:.2f}%")
    logger.info(f"最优夏普比率: {best_result.sharpe_ratio:.2f}")
    weekly_return = best_result.total_return / max(1, best_result.trading_days / 5)
    logger.info(f"周均收益率: {weekly_return:.2f}%")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
