#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略递归迭代优化脚本

Phase 2: 选股规则迭代优化
- 创建递归迭代优化框架
- 使用训练集/验证集进行参数优化
- 防止过拟合

优化参数:
- 信号参数: LIMIT_UP_THRESHOLD, VOLUME_RATIO_THRESHOLD, MOM_5D_THRESHOLD等
- 交易参数: MAX_POSITIONS, STOP_LOSS_PCT, TAKE_PROFIT_PCT, REBALANCE_DAYS

数据集:
- 训练集: 2019-01-01~2020-06-30 + 2024-09-01~2025-06-30
- 验证集: 2020-07-01~2021-03-31
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
import logging
import json
from dataclasses import dataclass, asdict
from itertools import product

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class StrategyParams:
    """策略参数"""
    # 信号参数
    limit_up_threshold: float = 0.095
    vol_ratio_threshold_first: float = 3.0
    mom_5d_threshold_breakout: float = 15.0
    mom_5d_threshold_volume: float = 10.0
    vol_ratio_threshold_breakout: float = 1.5
    vol_ratio_threshold_volume: float = 2.0
    min_signal_score: float = 55.0
    
    # 交易参数
    max_positions: int = 2
    stop_loss_pct: float = -10.0
    take_profit_pct: float = 25.0
    rebalance_days: int = 5


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float = 0.0
    weekly_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    total_signals: int = 0


def calculate_composite_score(result: BacktestResult) -> float:
    """
    计算综合评分
    
    综合评分 = 周平均收益率 * 0.4 + 夏普比率 * 0.3 + (1 - 最大回撤) * 0.2 + 胜率 * 0.1
    """
    score = (
        result.weekly_return * 0.4 +
        result.sharpe_ratio * 0.3 +
        (1 - abs(result.max_drawdown)) * 0.2 +
        result.win_rate * 0.1
    )
    return score


def run_backtest(
    jq_client,
    params: StrategyParams,
    start_date: str,
    end_date: str,
    universe: Optional[List[str]] = None,
    max_stocks: int = 300,
) -> BacktestResult:
    """
    运行回测
    
    这是一个简化的回测函数，实际实现需要完整的回测逻辑
    这里使用信号统计来模拟回测结果
    """
    try:
        # 导入信号分析函数
        import importlib.util
        signal_analysis_path = PROJECT_ROOT / 'scripts' / 'analyze_chase_rise_signals.py'
        spec = importlib.util.spec_from_file_location("analyze_chase_rise_signals", signal_analysis_path)
        signal_analysis_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(signal_analysis_module)
        analyze_signals_for_period = signal_analysis_module.analyze_signals_for_period
        analyze_signal_statistics = signal_analysis_module.analyze_signal_statistics
        
        # 分析信号
        df = analyze_signals_for_period(
            jq_client,
            start_date,
            end_date,
            universe=universe,
            max_stocks=max_stocks,
            rebalance_days=params.rebalance_days,
            limit_up_threshold=params.limit_up_threshold,
            vol_ratio_threshold_first=params.vol_ratio_threshold_first,
            mom_5d_threshold_breakout=params.mom_5d_threshold_breakout,
            mom_5d_threshold_volume=params.mom_5d_threshold_volume,
            vol_ratio_threshold_breakout=params.vol_ratio_threshold_breakout,
            vol_ratio_threshold_volume=params.vol_ratio_threshold_volume,
        )
        
        if df.empty:
            return BacktestResult()
        
        # 统计结果
        stats = analyze_signal_statistics(df)
        
        if 'overall' not in stats:
            return BacktestResult()
        
        overall = stats['overall']
        
        # 计算周平均收益率（使用5日收益率作为代理）
        avg_return_5d = overall.get('avg_return', 0.0)
        weekly_return = avg_return_5d  # 简化为5日收益率
        
        # 计算胜率
        win_rate = overall.get('win_rate', 0.0)
        
        # 计算交易次数（信号数）
        total_signals = overall.get('total_signals', 0)
        total_trades = total_signals  # 简化：每个信号对应一次交易
        
        # 计算夏普比率（简化）
        # 这里使用平均收益率和收益率的波动性
        returns = df['future_return_5d'].values
        if len(returns) > 1:
            sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(252 / 5)  # 年化
        else:
            sharpe_ratio = 0.0
        
        # 计算最大回撤（简化）
        cumulative = np.cumprod(1 + returns / 100)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0.0
        
        return BacktestResult(
            total_return=weekly_return * (len(df) / 5),  # 简化的总收益
            weekly_return=weekly_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=total_trades,
            total_signals=total_signals,
        )
    
    except Exception as e:
        logger.debug(f"回测失败: {e}")
        return BacktestResult()


def grid_search_optimize(
    jq_client,
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    param_grid: Dict[str, List],
    universe: Optional[List[str]] = None,
    max_stocks: int = 300,
) -> Tuple[StrategyParams, Dict]:
    """
    网格搜索优化
    
    Args:
        jq_client: JQData客户端
        train_periods: 训练集时间段列表
        validate_period: 验证集时间段
        param_grid: 参数网格
        universe: 股票池
        max_stocks: 最大股票数
    
    Returns:
        Tuple[StrategyParams, Dict]: (最优参数, 优化历史)
    """
    logger.info("开始网格搜索优化")
    
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    
    total_combinations = 1
    for vals in param_values:
        total_combinations *= len(vals)
    
    logger.info(f"参数组合总数: {total_combinations}")
    
    best_params = None
    best_score = -float('inf')
    optimization_history = []
    
    combination_idx = 0
    for param_combo in product(*param_values):
        combination_idx += 1
        params_dict = dict(zip(param_names, param_combo))
        
        if combination_idx % 10 == 0:
            logger.info(f"  进度: {combination_idx}/{total_combinations}")
        
        # 创建参数对象
        params = StrategyParams(**params_dict)
        
        # 训练集回测
        train_results = []
        for train_start, train_end in train_periods:
            result = run_backtest(
                jq_client,
                params,
                train_start,
                train_end,
                universe=universe,
                max_stocks=max_stocks,
            )
            train_results.append(result)
        
        # 平均训练结果
        avg_train_result = BacktestResult(
            total_return=np.mean([r.total_return for r in train_results]),
            weekly_return=np.mean([r.weekly_return for r in train_results]),
            sharpe_ratio=np.mean([r.sharpe_ratio for r in train_results]),
            max_drawdown=np.mean([r.max_drawdown for r in train_results]),
            win_rate=np.mean([r.win_rate for r in train_results]),
            total_trades=int(np.mean([r.total_trades for r in train_results])),
            total_signals=int(np.mean([r.total_signals for r in train_results])),
        )
        
        # 验证集回测
        validate_result = run_backtest(
            jq_client,
            params,
            validate_period[0],
            validate_period[1],
            universe=universe,
            max_stocks=max_stocks,
        )
        
        # 计算综合评分（使用验证集结果）
        score = calculate_composite_score(validate_result)
        
        # 记录优化历史
        history_entry = {
            'params': asdict(params),
            'train_result': asdict(avg_train_result),
            'validate_result': asdict(validate_result),
            'score': score,
            'overfit_ratio': avg_train_result.sharpe_ratio / (validate_result.sharpe_ratio + 1e-6),
        }
        optimization_history.append(history_entry)
        
        # 更新最优参数
        if score > best_score:
            best_score = score
            best_params = params
            logger.info(f"  ✅ 找到更优参数，评分: {score:.4f}")
    
    logger.info(f"✅ 优化完成，最优评分: {best_score:.4f}")
    
    return best_params, optimization_history


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("追涨策略递归迭代优化")
    logger.info("=" * 70)
    
    # 初始化JQData
    try:
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        logger.info("✅ JQData连接成功")
    except Exception as e:
        logger.error(f"❌ JQData连接失败: {e}")
        return
    
    # 数据集划分
    train_periods = [
        ('2019-01-01', '2020-06-30'),
        ('2024-09-01', '2025-06-30'),
    ]
    validate_period = ('2020-07-01', '2021-03-31')
    
    # 获取股票池（限制数量以加速）
    try:
        securities = jq.get_all_securities(types=['stock'], date=validate_period[1])
        stocks = securities.index.tolist()
        universe = [
            code for code in stocks[:200]  # 限制200只股票
            if 'ST' not in str(securities.loc[code, 'display_name']).upper()
        ]
        logger.info(f"股票池: {len(universe)}只")
    except Exception as e:
        logger.error(f"获取股票池失败: {e}")
        return
    
    # 参数网格（简化版本，减少组合数以加速）
    param_grid = {
        'limit_up_threshold': [0.090, 0.095, 0.098],
        'vol_ratio_threshold_first': [2.5, 3.0, 3.5],
        'mom_5d_threshold_breakout': [13.0, 15.0, 17.0],
        'mom_5d_threshold_volume': [9.0, 10.0, 11.0],
        'max_positions': [2, 3],
        'stop_loss_pct': [-9.0, -10.0, -11.0],
        'take_profit_pct': [23.0, 25.0, 27.0],
        'rebalance_days': [5],
    }
    
    logger.info("\n参数网格:")
    for param, values in param_grid.items():
        logger.info(f"  {param}: {values}")
    
    # 执行网格搜索优化
    best_params, history = grid_search_optimize(
        jq,
        train_periods,
        validate_period,
        param_grid,
        universe=universe,
        max_stocks=0,  # 使用全部股票池
    )
    
    if best_params is None:
        logger.error("优化未找到任何结果")
        return
    
    # 打印最优参数
    logger.info("\n" + "=" * 70)
    logger.info("最优参数")
    logger.info("=" * 70)
    print("\n🏆 最优参数:")
    print("-" * 70)
    for key, value in asdict(best_params).items():
        print(f"  {key}: {value}")
    
    # 保存结果
    output_dir = PROJECT_ROOT / 'output' / 'chase_rise_optimization'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存最优参数
    params_path = output_dir / f'best_params_{timestamp}.json'
    with open(params_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(best_params), f, ensure_ascii=False, indent=2)
    logger.info(f"\n✅ 最优参数已保存: {params_path}")
    
    # 保存优化历史（Top 20）
    history_df = pd.DataFrame(history)
    history_df = history_df.sort_values('score', ascending=False).head(20)
    history_path = output_dir / f'optimization_history_{timestamp}.csv'
    history_df.to_csv(history_path, index=False, encoding='utf-8-sig')
    logger.info(f"✅ 优化历史已保存: {history_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("优化完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
