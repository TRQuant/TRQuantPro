#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 - vectorbt优化版
=====================================

使用vectorbt作为回测引擎，实现10x~100x速度提升

优化目标：
- 周收益10%+ 的激进策略
- 训练集/验证集分离
- 过拟合检测

使用方法：
    python scripts/run_bull_market_optimization_vbt.py

输出：
    - output/bull_market_optimization_vbt/best_params_{timestamp}.json
    - output/bull_market_optimization_vbt/optimization_history_{timestamp}.csv
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
import logging
import time
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools

import pandas as pd
import numpy as np
from tqdm import tqdm

# 导入研究模块
from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalParams,
    VBTBacktest,
    BacktestResult,
    calculate_composite_score,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "output" / "bull_market_optimization_vbt"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class BullMarketStrategyParams:
    """牛市策略参数（用于网格搜索）"""
    # 动量阈值
    min_mom_20d: float = 5.0
    max_mom_20d: float = 50.0
    
    # 相对位置阈值
    max_rel_position: float = 80.0
    
    # 量比阈值
    min_vol_ratio: float = 1.0
    
    # 持仓限制
    max_positions: int = 10
    single_position_max: float = 0.2
    
    # 调仓周期
    rebalance_period: int = 5
    
    # 止损止盈
    stop_loss_pct: float = 0.08
    take_profit_pct: float = 0.20
    
    def to_signal_params(self) -> SignalParams:
        """转换为SignalParams"""
        return SignalParams(
            min_mom_20d=self.min_mom_20d,
            max_mom_20d=self.max_mom_20d,
            max_rel_position=self.max_rel_position,
            min_vol_ratio=self.min_vol_ratio,
            max_positions=self.max_positions,
            single_position_max=self.single_position_max,
            rebalance_period=self.rebalance_period,
            stop_loss_pct=self.stop_loss_pct,
            take_profit_pct=self.take_profit_pct,
        )


@dataclass
class OptimizationResult:
    """优化结果"""
    params: BullMarketStrategyParams
    train_result: BacktestResult
    validate_result: BacktestResult
    train_score: float
    validate_score: float
    overfit_ratio: float  # validate_score / train_score


class ProgressReporter:
    """进度报告器"""
    
    def __init__(self, total: int, desc: str = "优化进度"):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()
        self.pbar = tqdm(total=total, desc=desc)
    
    def update(self, result: Optional[OptimizationResult] = None):
        self.current += 1
        self.pbar.update(1)
        
        if result:
            self.pbar.set_postfix({
                'train': f'{result.train_score:.1f}',
                'val': f'{result.validate_score:.1f}',
                'overfit': f'{result.overfit_ratio:.2f}',
            })
    
    def close(self):
        self.pbar.close()
        elapsed = time.time() - self.start_time
        logger.info(f"优化完成，总耗时: {elapsed:.1f}秒")


def generate_param_grid() -> List[BullMarketStrategyParams]:
    """生成参数网格"""
    
    # 定义搜索空间
    param_space = {
        'min_mom_20d': [0.0, 5.0, 10.0],
        'max_mom_20d': [30.0, 50.0, 80.0],
        'max_rel_position': [60.0, 80.0, 100.0],
        'min_vol_ratio': [0.5, 1.0, 1.5],
        'max_positions': [5, 10, 15],
        'rebalance_period': [5, 10],  # 周调仓 or 双周调仓
    }
    
    # 生成所有组合
    keys = list(param_space.keys())
    values = list(param_space.values())
    combinations = list(itertools.product(*values))
    
    params_list = []
    for combo in combinations:
        param_dict = dict(zip(keys, combo))
        params = BullMarketStrategyParams(**param_dict)
        params_list.append(params)
    
    logger.info(f"生成参数组合数: {len(params_list)}")
    return params_list


def run_single_backtest(
    data_provider: ResearchDataProvider,
    factor_calc: FactorCalculator,
    backtest_engine: VBTBacktest,
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    universe: List[str],
) -> Tuple[BacktestResult, float]:
    """
    运行单次回测
    
    Returns:
        (BacktestResult, composite_score)
    """
    try:
        # 获取数据
        data = data_provider.get_data_matrices(
            symbols=universe,
            start_date=start_date,
            end_date=end_date,
        )
        
        # 计算因子
        factors = factor_calc.calculate_factors(data)
        
        # 运行回测
        signal_params = params.to_signal_params()
        result = backtest_engine.run(data, factors, signal_params)
        
        # 计算评分
        score = calculate_composite_score(result)
        
        return result, score
        
    except Exception as e:
        logger.error(f"回测失败: {e}")
        return BacktestResult(), -100.0


def grid_search_optimize(
    data_provider: ResearchDataProvider,
    universe: List[str],
    train_start: str,
    train_end: str,
    validate_start: str,
    validate_end: str,
    param_grid: Optional[List[BullMarketStrategyParams]] = None,
    top_k: int = 10,
) -> List[OptimizationResult]:
    """
    网格搜索优化
    
    Args:
        data_provider: 数据提供器
        universe: 股票池
        train_start/end: 训练集时间范围
        validate_start/end: 验证集时间范围
        param_grid: 参数网格
        top_k: 返回前K个结果
    
    Returns:
        Top-K优化结果
    """
    if param_grid is None:
        param_grid = generate_param_grid()
    
    factor_calc = FactorCalculator(use_gpu=False)
    backtest_engine = VBTBacktest(initial_capital=1000000)
    
    results = []
    reporter = ProgressReporter(len(param_grid), "网格搜索")
    
    for params in param_grid:
        try:
            # 训练集回测
            train_result, train_score = run_single_backtest(
                data_provider, factor_calc, backtest_engine,
                params, train_start, train_end, universe
            )
            
            # 验证集回测
            validate_result, validate_score = run_single_backtest(
                data_provider, factor_calc, backtest_engine,
                params, validate_start, validate_end, universe
            )
            
            # 计算过拟合比率
            overfit_ratio = validate_score / train_score if train_score > 0 else 0
            
            opt_result = OptimizationResult(
                params=params,
                train_result=train_result,
                validate_result=validate_result,
                train_score=train_score,
                validate_score=validate_score,
                overfit_ratio=overfit_ratio,
            )
            results.append(opt_result)
            reporter.update(opt_result)
            
        except Exception as e:
            logger.error(f"参数组合失败: {e}")
            reporter.update()
    
    reporter.close()
    
    # 按验证集评分排序
    results.sort(key=lambda x: x.validate_score, reverse=True)
    
    return results[:top_k]


def save_results(
    results: List[OptimizationResult],
    output_dir: Path,
) -> Tuple[Path, Path]:
    """保存优化结果"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存最优参数
    if results:
        best = results[0]
        best_params_path = output_dir / f"best_params_{timestamp}.json"
        with open(best_params_path, 'w') as f:
            json.dump({
                'params': asdict(best.params),
                'train_score': best.train_score,
                'validate_score': best.validate_score,
                'overfit_ratio': best.overfit_ratio,
                'train_result': best.train_result.to_dict(),
                'validate_result': best.validate_result.to_dict(),
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"最优参数已保存: {best_params_path}")
    
    # 保存优化历史
    history = []
    for i, result in enumerate(results):
        row = {
            'rank': i + 1,
            'train_score': result.train_score,
            'validate_score': result.validate_score,
            'overfit_ratio': result.overfit_ratio,
            **asdict(result.params),
            **{f'train_{k}': v for k, v in result.train_result.to_dict().items()},
            **{f'val_{k}': v for k, v in result.validate_result.to_dict().items()},
        }
        history.append(row)
    
    history_path = output_dir / f"optimization_history_{timestamp}.csv"
    pd.DataFrame(history).to_csv(history_path, index=False)
    logger.info(f"优化历史已保存: {history_path}")
    
    return best_params_path, history_path


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("牛市极端高收益策略 - vectorbt优化")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    # 1. 初始化数据提供器
    logger.info("Step 1: 初始化数据提供器...")
    data_provider = ResearchDataProvider(use_cache=True)
    
    # 2. 获取股票池（沪深300成分股）
    logger.info("Step 2: 获取股票池...")
    universe = data_provider.get_index_stocks('000300.XSHG')
    logger.info(f"股票池: {len(universe)}只")
    
    # 3. 定义训练集和验证集时间范围
    # 牛市区间：2019-2021年
    train_start = "2019-01-01"
    train_end = "2020-12-31"
    validate_start = "2021-01-01"
    validate_end = "2021-12-31"
    
    logger.info(f"训练集: {train_start} ~ {train_end}")
    logger.info(f"验证集: {validate_start} ~ {validate_end}")
    
    # 4. 运行网格搜索优化
    logger.info("Step 3: 运行网格搜索优化...")
    top_results = grid_search_optimize(
        data_provider=data_provider,
        universe=universe,
        train_start=train_start,
        train_end=train_end,
        validate_start=validate_start,
        validate_end=validate_end,
        top_k=10,
    )
    
    # 5. 保存结果
    logger.info("Step 4: 保存结果...")
    best_params_path, history_path = save_results(top_results, OUTPUT_DIR)
    
    # 6. 打印Top-5结果
    logger.info("\n" + "=" * 60)
    logger.info("Top-5 优化结果")
    logger.info("=" * 60)
    
    for i, result in enumerate(top_results[:5]):
        logger.info(f"\n--- Rank {i+1} ---")
        logger.info(f"训练集评分: {result.train_score:.2f}")
        logger.info(f"验证集评分: {result.validate_score:.2f}")
        logger.info(f"过拟合比率: {result.overfit_ratio:.2f}")
        logger.info(f"训练集年化: {result.train_result.annual_return:.2f}%")
        logger.info(f"验证集年化: {result.validate_result.annual_return:.2f}%")
        logger.info(f"参数: min_mom={result.params.min_mom_20d}, "
                   f"max_mom={result.params.max_mom_20d}, "
                   f"max_pos={result.params.max_rel_position}, "
                   f"vol_ratio={result.params.min_vol_ratio}, "
                   f"positions={result.params.max_positions}")
    
    # 7. 总结
    elapsed = time.time() - start_time
    logger.info("\n" + "=" * 60)
    logger.info(f"优化完成！总耗时: {elapsed:.1f}秒")
    logger.info(f"最优参数: {best_params_path}")
    logger.info(f"优化历史: {history_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
