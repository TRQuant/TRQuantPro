#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 - vectorbt递归优化框架 V2
============================================

基于vectorbt的高速回测引擎，实现递归网格搜索优化。

核心特性：
1. 完整止损止盈功能（与BulletTrade对齐）
2. 递归优化：粗网格 -> 细网格围绕最优参数
3. 过拟合检测与惩罚机制
4. 智能剪枝（训练集差则跳过验证集）
5. 与BulletTrade结果对比

使用方法：
    python scripts/run_bull_market_optimization_vbt_v2.py

输出：
    - output/bull_market_optimization_vbt_v2/best_params_{timestamp}.json
    - output/bull_market_optimization_vbt_v2/optimization_history_{timestamp}.csv
    - output/bull_market_optimization_vbt_v2/comparison_report.md
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
from itertools import product

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
OUTPUT_DIR = PROJECT_ROOT / "output" / "bull_market_optimization_vbt_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==================== 配置类 ====================

class OptimizationConfig:
    """优化配置"""
    # 时间范围（与BulletTrade V3对齐）
    TRAIN_START = "2020-01-01"
    TRAIN_END = "2020-06-30"
    VALIDATE_START = "2020-07-01"
    VALIDATE_END = "2020-12-31"
    
    # 递归优化配置
    MAX_RECURSIVE_ITERATIONS = 2    # 最大递归次数
    REFINEMENT_RATIO = 0.5          # 每次细化范围缩小比例
    CONVERGENCE_THRESHOLD = 0.05    # 收敛阈值（5%变化）
    
    # 过拟合检测
    OVERFIT_PENALTY_THRESHOLD = 2.0 # 过拟合惩罚阈值
    OVERFIT_PENALTY_FACTOR = 0.3    # 过拟合惩罚因子
    
    # 智能剪枝
    PRUNE_THRESHOLD = -20.0         # 训练集年化 < -20% 则剪枝
    
    # 回测配置
    INITIAL_CAPITAL = 1000000.0     # 初始资金
    BENCHMARK = '000300.XSHG'       # 基准指数


# ==================== 数据类定义 ====================

@dataclass
class BullMarketStrategyParams:
    """牛市策略参数 - 完整版（与BulletTrade对齐）"""
    
    # === 选股因子参数 ===
    min_mom_20d: float = 5.0        # 最小20日动量（%）
    max_mom_20d: float = 50.0       # 最大20日动量（%）
    max_rel_position: float = 80.0  # 最大相对位置（%）
    min_vol_ratio: float = 1.0      # 最小量比
    
    # === 持仓参数 ===
    max_positions: int = 10         # 最大持仓数
    single_position_max: float = 0.2  # 单票最大仓位
    
    # === 调仓周期 ===
    rebalance_period: int = 5       # 调仓周期（交易日）
    
    # === 止损止盈参数（完整版） ===
    stop_loss_pct: float = -0.08    # 固定止损（-8%）
    take_profit_pct: float = 0.30   # 固定止盈（+30%）
    trailing_stop_pct: float = -0.08  # 移动止损（-8%）
    trailing_stop_trigger: float = 0.15  # 移动止损触发条件（盈利15%后启用）
    time_stop_days: int = 20        # 时间止损（20交易日）
    partial_profit_1_pct: float = 0.20  # 第一批止盈（+20%）
    partial_profit_1_ratio: float = 0.50  # 第一批止盈比例（50%）
    
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
            trailing_stop_pct=self.trailing_stop_pct,
            trailing_stop_trigger=self.trailing_stop_trigger,
            time_stop_days=self.time_stop_days,
            partial_profit_1_pct=self.partial_profit_1_pct,
            partial_profit_1_ratio=self.partial_profit_1_ratio,
        )


@dataclass
class OptimizationResult:
    """优化结果"""
    params: BullMarketStrategyParams
    train_result: BacktestResult
    validate_result: BacktestResult
    train_score: float
    validate_score: float
    overfit_ratio: float
    final_score: float  # 考虑过拟合惩罚后的最终评分


# ==================== 工具函数 ====================

def generate_coarse_param_grid() -> List[BullMarketStrategyParams]:
    """
    生成粗网格参数（与BulletTrade V3对齐）
    
    参数选择依据 analysis_report_combo1.md 的建议
    """
    param_space = {
        # 止损止盈（最关键）
        'stop_loss_pct': [-0.06, -0.08, -0.10],
        'trailing_stop_pct': [-0.08, -0.10],
        
        # 选股因子
        'min_mom_20d': [0.0, 5.0, 10.0],
        'max_mom_20d': [30.0, 50.0],
        
        # 持仓配置
        'max_positions': [5, 8, 10],
    }
    
    keys = list(param_space.keys())
    values = list(param_space.values())
    combinations = list(product(*values))
    
    params_list = []
    for combo in combinations:
        param_dict = dict(zip(keys, combo))
        params = BullMarketStrategyParams(**param_dict)
        params_list.append(params)
    
    logger.info(f"粗网格参数组合数: {len(params_list)}")
    return params_list


def generate_fine_param_grid(
    best_params: BullMarketStrategyParams,
    refinement_ratio: float = 0.5,
) -> List[BullMarketStrategyParams]:
    """
    围绕最优参数生成细网格
    """
    def refine_range(center: float, step: float, count: int = 3) -> List[float]:
        """生成细化范围"""
        half_range = step * refinement_ratio
        return [center - half_range, center, center + half_range]
    
    # 对连续参数进行细化
    param_space = {
        'stop_loss_pct': refine_range(best_params.stop_loss_pct, 0.02),
        'trailing_stop_pct': refine_range(best_params.trailing_stop_pct, 0.02),
        'min_mom_20d': refine_range(best_params.min_mom_20d, 2.5),
        'max_mom_20d': refine_range(best_params.max_mom_20d, 10.0),
    }
    
    # 固定其他参数
    fixed_params = {
        'max_positions': best_params.max_positions,
        'max_rel_position': best_params.max_rel_position,
        'min_vol_ratio': best_params.min_vol_ratio,
        'single_position_max': best_params.single_position_max,
        'rebalance_period': best_params.rebalance_period,
        'take_profit_pct': best_params.take_profit_pct,
        'trailing_stop_trigger': best_params.trailing_stop_trigger,
        'time_stop_days': best_params.time_stop_days,
        'partial_profit_1_pct': best_params.partial_profit_1_pct,
        'partial_profit_1_ratio': best_params.partial_profit_1_ratio,
    }
    
    keys = list(param_space.keys())
    values = list(param_space.values())
    combinations = list(product(*values))
    
    params_list = []
    for combo in combinations:
        param_dict = dict(zip(keys, combo))
        param_dict.update(fixed_params)
        params = BullMarketStrategyParams(**param_dict)
        params_list.append(params)
    
    logger.info(f"细网格参数组合数: {len(params_list)}")
    return params_list


def calculate_final_score(
    train_score: float,
    validate_score: float,
    config: OptimizationConfig = OptimizationConfig(),
) -> Tuple[float, float]:
    """
    计算最终评分（考虑过拟合惩罚）
    
    Returns:
        (final_score, overfit_ratio)
    """
    if train_score <= 0:
        return validate_score, 0.0
    
    overfit_ratio = train_score / (validate_score + 1e-6)
    
    # 过拟合惩罚
    if overfit_ratio > config.OVERFIT_PENALTY_THRESHOLD:
        penalty = (overfit_ratio - 1) * config.OVERFIT_PENALTY_FACTOR
        penalty = min(penalty, 0.5)  # 最多惩罚50%
        final_score = validate_score * (1 - penalty)
    else:
        final_score = validate_score
    
    return final_score, overfit_ratio


# ==================== 回测执行 ====================

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
    param_grid: List[BullMarketStrategyParams],
    config: OptimizationConfig = OptimizationConfig(),
    top_k: int = 10,
    use_pruning: bool = True,
) -> List[OptimizationResult]:
    """
    网格搜索优化
    
    Args:
        data_provider: 数据提供器
        universe: 股票池
        param_grid: 参数网格
        config: 优化配置
        top_k: 返回前K个结果
        use_pruning: 是否使用智能剪枝
    
    Returns:
        Top-K优化结果
    """
    factor_calc = FactorCalculator(use_gpu=False)
    backtest_engine = VBTBacktest(initial_capital=config.INITIAL_CAPITAL)
    
    results = []
    pruned_count = 0
    
    pbar = tqdm(total=len(param_grid), desc="网格搜索")
    
    for params in param_grid:
        try:
            # 训练集回测
            train_result, train_score = run_single_backtest(
                data_provider, factor_calc, backtest_engine,
                params, config.TRAIN_START, config.TRAIN_END, universe
            )
            
            # 智能剪枝：训练集表现太差则跳过验证集
            if use_pruning and train_result.annual_return < config.PRUNE_THRESHOLD:
                pruned_count += 1
                pbar.update(1)
                pbar.set_postfix({'pruned': pruned_count})
                continue
            
            # 验证集回测
            validate_result, validate_score = run_single_backtest(
                data_provider, factor_calc, backtest_engine,
                params, config.VALIDATE_START, config.VALIDATE_END, universe
            )
            
            # 计算最终评分
            final_score, overfit_ratio = calculate_final_score(
                train_score, validate_score, config
            )
            
            opt_result = OptimizationResult(
                params=params,
                train_result=train_result,
                validate_result=validate_result,
                train_score=train_score,
                validate_score=validate_score,
                overfit_ratio=overfit_ratio,
                final_score=final_score,
            )
            results.append(opt_result)
            
            pbar.update(1)
            pbar.set_postfix({
                'train': f'{train_score:.1f}',
                'val': f'{validate_score:.1f}',
                'final': f'{final_score:.1f}',
            })
            
        except Exception as e:
            logger.error(f"参数组合失败: {e}")
            pbar.update(1)
    
    pbar.close()
    
    if pruned_count > 0:
        logger.info(f"智能剪枝跳过 {pruned_count} 个组合")
    
    # 按最终评分排序
    results.sort(key=lambda x: x.final_score, reverse=True)
    
    return results[:top_k]


def recursive_optimize(
    data_provider: ResearchDataProvider,
    universe: List[str],
    config: OptimizationConfig = OptimizationConfig(),
) -> List[OptimizationResult]:
    """
    递归优化：粗网格 -> 细网格
    """
    logger.info("=" * 60)
    logger.info("Round 1: 粗网格搜索")
    logger.info("=" * 60)
    
    # Round 1: 粗网格
    coarse_grid = generate_coarse_param_grid()
    coarse_results = grid_search_optimize(
        data_provider, universe, coarse_grid, config, top_k=10
    )
    
    if not coarse_results:
        logger.error("粗网格搜索无有效结果")
        return []
    
    logger.info(f"\n粗网格Top-3结果:")
    for i, r in enumerate(coarse_results[:3]):
        logger.info(f"  Rank {i+1}: final={r.final_score:.2f}, "
                   f"train={r.train_result.annual_return:.2f}%, "
                   f"val={r.validate_result.annual_return:.2f}%")
    
    # Round 2: 围绕Top-3进行细网格搜索
    logger.info("\n" + "=" * 60)
    logger.info("Round 2: 细网格搜索（围绕Top-3）")
    logger.info("=" * 60)
    
    fine_results = []
    for i, top_result in enumerate(coarse_results[:3]):
        logger.info(f"\n细化 Rank {i+1} 参数...")
        fine_grid = generate_fine_param_grid(
            top_result.params, config.REFINEMENT_RATIO
        )
        results = grid_search_optimize(
            data_provider, universe, fine_grid, config, top_k=5, use_pruning=False
        )
        fine_results.extend(results)
    
    # 合并所有结果并排序
    all_results = coarse_results + fine_results
    all_results.sort(key=lambda x: x.final_score, reverse=True)
    
    # 去重（保留最高分）
    seen = set()
    unique_results = []
    for r in all_results:
        key = (r.params.stop_loss_pct, r.params.trailing_stop_pct,
               r.params.min_mom_20d, r.params.max_mom_20d, r.params.max_positions)
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results[:10]


# ==================== 结果保存与报告 ====================

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
                'final_score': best.final_score,
                'overfit_ratio': best.overfit_ratio,
                'train_result': best.train_result.to_dict(),
                'validate_result': best.validate_result.to_dict(),
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"最优参数已保存: {best_params_path}")
    else:
        best_params_path = None
    
    # 保存优化历史
    history = []
    for i, result in enumerate(results):
        row = {
            'rank': i + 1,
            'train_score': result.train_score,
            'validate_score': result.validate_score,
            'final_score': result.final_score,
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


def generate_comparison_report(
    vbt_results: List[OptimizationResult],
    output_dir: Path,
) -> Path:
    """
    生成与BulletTrade的对比报告
    """
    # BulletTrade V3结果（从分析报告中提取）
    bt_result = {
        'train': {
            'total_return': -7.60,
            'annual_return': -15.53,
            'sharpe_ratio': -0.66,
            'max_drawdown': -17.26,
            'win_rate': 15.38,
            'total_trades': 212,
        },
        'validate': {
            'total_return': -10.79,
            'annual_return': -20.27,
            'sharpe_ratio': -0.62,
            'max_drawdown': -33.75,
            'win_rate': 19.84,
            'total_trades': 249,
        },
        'params': {
            'max_stocks': 5,
            'stop_loss': -0.06,
            'take_profit': 0.30,
            'trailing_stop': -0.08,
            'time_stop_days': 20,
        }
    }
    
    # 获取vectorbt最优结果
    if vbt_results:
        vbt_best = vbt_results[0]
        vbt_train = vbt_best.train_result
        vbt_val = vbt_best.validate_result
    else:
        return None
    
    report = f"""# vectorbt vs BulletTrade 回测对比报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. 回测配置对比

| 配置项 | BulletTrade | vectorbt |
|--------|-------------|----------|
| 训练集 | 2020-01-01 ~ 2020-06-30 | 2020-01-01 ~ 2020-06-30 |
| 验证集 | 2020-07-01 ~ 2020-12-31 | 2020-07-01 ~ 2020-12-31 |
| 初始资金 | 100万 | 100万 |
| 最大持仓 | {bt_result['params']['max_stocks']} | {vbt_best.params.max_positions} |
| 止损 | {bt_result['params']['stop_loss']:.0%} | {vbt_best.params.stop_loss_pct:.0%} |

---

## 2. 训练集结果对比

| 指标 | BulletTrade | vectorbt | 差异 |
|------|-------------|----------|------|
| 总收益率 | {bt_result['train']['total_return']:.2f}% | {vbt_train.total_return:.2f}% | {vbt_train.total_return - bt_result['train']['total_return']:.2f}% |
| 年化收益率 | {bt_result['train']['annual_return']:.2f}% | {vbt_train.annual_return:.2f}% | {vbt_train.annual_return - bt_result['train']['annual_return']:.2f}% |
| 夏普比率 | {bt_result['train']['sharpe_ratio']:.2f} | {vbt_train.sharpe_ratio:.2f} | {vbt_train.sharpe_ratio - bt_result['train']['sharpe_ratio']:.2f} |
| 最大回撤 | {bt_result['train']['max_drawdown']:.2f}% | {-vbt_train.max_drawdown:.2f}% | {-vbt_train.max_drawdown - bt_result['train']['max_drawdown']:.2f}% |
| 胜率 | {bt_result['train']['win_rate']:.2f}% | {vbt_train.win_rate:.2f}% | {vbt_train.win_rate - bt_result['train']['win_rate']:.2f}% |
| 交易次数 | {bt_result['train']['total_trades']} | {vbt_train.total_trades} | {vbt_train.total_trades - bt_result['train']['total_trades']} |

---

## 3. 验证集结果对比

| 指标 | BulletTrade | vectorbt | 差异 |
|------|-------------|----------|------|
| 总收益率 | {bt_result['validate']['total_return']:.2f}% | {vbt_val.total_return:.2f}% | {vbt_val.total_return - bt_result['validate']['total_return']:.2f}% |
| 年化收益率 | {bt_result['validate']['annual_return']:.2f}% | {vbt_val.annual_return:.2f}% | {vbt_val.annual_return - bt_result['validate']['annual_return']:.2f}% |
| 夏普比率 | {bt_result['validate']['sharpe_ratio']:.2f} | {vbt_val.sharpe_ratio:.2f} | {vbt_val.sharpe_ratio - bt_result['validate']['sharpe_ratio']:.2f} |
| 最大回撤 | {bt_result['validate']['max_drawdown']:.2f}% | {-vbt_val.max_drawdown:.2f}% | {-vbt_val.max_drawdown - bt_result['validate']['max_drawdown']:.2f}% |
| 胜率 | {bt_result['validate']['win_rate']:.2f}% | {vbt_val.win_rate:.2f}% | {vbt_val.win_rate - bt_result['validate']['win_rate']:.2f}% |
| 交易次数 | {bt_result['validate']['total_trades']} | {vbt_val.total_trades} | {vbt_val.total_trades - bt_result['validate']['total_trades']} |

---

## 4. vectorbt最优参数

```python
BullMarketStrategyParams(
    min_mom_20d={vbt_best.params.min_mom_20d},
    max_mom_20d={vbt_best.params.max_mom_20d},
    max_rel_position={vbt_best.params.max_rel_position},
    min_vol_ratio={vbt_best.params.min_vol_ratio},
    max_positions={vbt_best.params.max_positions},
    stop_loss_pct={vbt_best.params.stop_loss_pct},
    take_profit_pct={vbt_best.params.take_profit_pct},
    trailing_stop_pct={vbt_best.params.trailing_stop_pct},
    trailing_stop_trigger={vbt_best.params.trailing_stop_trigger},
    time_stop_days={vbt_best.params.time_stop_days},
)
```

---

## 5. 差异分析

### 5.1 主要差异来源

1. **交易执行时机**: BulletTrade使用盘中检查止损止盈，vectorbt使用日线级别
2. **交易成本**: BulletTrade精确模拟，vectorbt使用简化估算
3. **信号生成**: 因子计算和排序可能有细微差异
4. **持仓管理**: 权重分配逻辑略有不同

### 5.2 一致性评估

- 收益率方向一致性: {'一致' if (bt_result['validate']['annual_return'] * vbt_val.annual_return) >= 0 else '不一致'}
- 收益率差异率: {abs(vbt_val.annual_return - bt_result['validate']['annual_return']) / (abs(bt_result['validate']['annual_return']) + 1e-6) * 100:.1f}%
- 夏普比率差异: {abs(vbt_val.sharpe_ratio - bt_result['validate']['sharpe_ratio']):.2f}

---

## 6. 结论与建议

### 6.1 vectorbt优势
- 回测速度: ~0.1秒/次 (BulletTrade ~40分钟/次)
- 适合大规模参数搜索和快速迭代

### 6.2 BulletTrade优势
- 更接近真实交易执行
- 精确的盘中止损止盈

### 6.3 建议工作流
1. 使用vectorbt进行大规模参数搜索
2. 对Top-5参数使用BulletTrade验证
3. 最终参数上线前再用BulletTrade完整回测

---

*报告生成器: TRQuant vectorbt优化框架 V2*
"""
    
    report_path = output_dir / "comparison_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    logger.info(f"对比报告已保存: {report_path}")
    return report_path


# ==================== 主函数 ====================

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("牛市极端高收益策略 - vectorbt递归优化框架 V2")
    logger.info("=" * 60)
    
    start_time = time.time()
    config = OptimizationConfig()
    
    # 1. 初始化数据提供器
    logger.info("\nStep 1: 初始化数据提供器...")
    data_provider = ResearchDataProvider(use_cache=True)
    
    # 2. 获取股票池（沪深300成分股）
    logger.info("Step 2: 获取股票池...")
    universe = data_provider.get_index_stocks(config.BENCHMARK)
    logger.info(f"股票池: {len(universe)}只")
    
    # 3. 显示时间配置
    logger.info(f"\n时间配置:")
    logger.info(f"  训练集: {config.TRAIN_START} ~ {config.TRAIN_END}")
    logger.info(f"  验证集: {config.VALIDATE_START} ~ {config.VALIDATE_END}")
    
    # 4. 运行递归优化
    logger.info("\nStep 3: 运行递归优化...")
    top_results = recursive_optimize(data_provider, universe, config)
    
    # 5. 保存结果
    logger.info("\nStep 4: 保存结果...")
    best_params_path, history_path = save_results(top_results, OUTPUT_DIR)
    
    # 6. 生成对比报告
    logger.info("\nStep 5: 生成对比报告...")
    report_path = generate_comparison_report(top_results, OUTPUT_DIR)
    
    # 7. 打印Top-5结果
    logger.info("\n" + "=" * 60)
    logger.info("Top-5 优化结果")
    logger.info("=" * 60)
    
    for i, result in enumerate(top_results[:5]):
        logger.info(f"\n--- Rank {i+1} ---")
        logger.info(f"最终评分: {result.final_score:.2f}")
        logger.info(f"训练集: 年化={result.train_result.annual_return:.2f}%, "
                   f"夏普={result.train_result.sharpe_ratio:.2f}")
        logger.info(f"验证集: 年化={result.validate_result.annual_return:.2f}%, "
                   f"夏普={result.validate_result.sharpe_ratio:.2f}")
        logger.info(f"过拟合比率: {result.overfit_ratio:.2f}")
        logger.info(f"参数: stop_loss={result.params.stop_loss_pct}, "
                   f"trailing={result.params.trailing_stop_pct}, "
                   f"mom={result.params.min_mom_20d}-{result.params.max_mom_20d}, "
                   f"positions={result.params.max_positions}")
    
    # 8. 总结
    elapsed = time.time() - start_time
    logger.info("\n" + "=" * 60)
    logger.info(f"优化完成！总耗时: {elapsed:.1f}秒")
    logger.info(f"最优参数: {best_params_path}")
    logger.info(f"优化历史: {history_path}")
    logger.info(f"对比报告: {report_path}")
    logger.info("=" * 60)
    
    return top_results


if __name__ == "__main__":
    main()
