#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略递归迭代优化 - 完整运行脚本

功能:
1. 使用训练集+验证集进行网格搜索优化
2. 找到最优参数组合
3. 生成优化后的QMT策略代码

数据集:
- 训练集1: 2019-01-01 ~ 2020-06-30 (上一轮牛熊周期)
- 训练集2: 2024-09-01 ~ 2025-06-30 (当前市场环境)
- 验证集: 2020-07-01 ~ 2021-03-31 (牛市初期)

优化参数:
- 信号参数: limit_up_threshold, vol_ratio_threshold, mom_5d_threshold
- 交易参数: max_positions, stop_loss_pct, take_profit_pct
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
import time

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


# ==================== 数据类定义 ====================

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


# ==================== 信号计算 ====================

class SignalType:
    """信号类型"""
    FIRST_LIMIT_UP = "FIRST_LIMIT_UP"
    CONSECUTIVE_LIMIT_UP = "CONSECUTIVE_LIMIT_UP"
    STRONG_BREAKOUT = "STRONG_BREAKOUT"
    VOLUME_PRICE_RISE = "VOLUME_PRICE_RISE"
    NO_SIGNAL = "NO_SIGNAL"


def calculate_chase_rise_signal(
    close: np.ndarray,
    volume: np.ndarray,
    params: StrategyParams,
) -> Tuple[float, str]:
    """计算追涨信号"""
    if len(close) < 21:
        return 0.0, SignalType.NO_SIGNAL
    
    score = 0.0
    signal_type = SignalType.NO_SIGNAL
    
    # 基础指标
    daily_return = close[-1] / close[-2] - 1 if len(close) >= 2 else 0
    is_limit_up = daily_return > params.limit_up_threshold
    
    # 近5日涨停计数
    limit_up_recent = 0
    for j in range(max(len(close)-5, 1), len(close)):
        if j > 0 and close[j] / close[j-1] - 1 > params.limit_up_threshold:
            limit_up_recent += 1
    
    # 5日动量
    mom_5d = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    
    # 量比
    vol_ratio = volume[-1] / np.mean(volume[-20:]) if len(volume) >= 20 and np.mean(volume[-20:]) > 0 else 1.0
    
    # 信号1: 首板启动
    if is_limit_up and limit_up_recent == 1:
        score = 75
        signal_type = SignalType.FIRST_LIMIT_UP
        if vol_ratio > params.vol_ratio_threshold_first:
            score += 15
        return score, signal_type
    
    # 信号2: 连板加速
    if limit_up_recent >= 2:
        score = 65
        signal_type = SignalType.CONSECUTIVE_LIMIT_UP
        return score, signal_type
    
    # 信号3: 强势突破
    if mom_5d > params.mom_5d_threshold_breakout and vol_ratio > params.vol_ratio_threshold_breakout:
        score = 60
        signal_type = SignalType.STRONG_BREAKOUT
        return score, signal_type
    
    # 信号4: 量价齐升
    if mom_5d > params.mom_5d_threshold_volume and vol_ratio > params.vol_ratio_threshold_volume:
        score = 55
        signal_type = SignalType.VOLUME_PRICE_RISE
        return score, signal_type
    
    return score, signal_type


# ==================== 简化回测 ====================

def run_simplified_backtest(
    jq_client,
    params: StrategyParams,
    start_date: str,
    end_date: str,
    universe: List[str],
) -> BacktestResult:
    """
    简化回测 - 基于信号统计
    """
    try:
        trade_days = jq_client.get_trade_days(start_date=start_date, end_date=end_date)
        if trade_days is None or len(trade_days) < 25:
            return BacktestResult()
        
        all_returns = []
        signal_count = 0
        winning_count = 0
        
        # 采样部分股票加速
        sample_stocks = universe[:min(100, len(universe))]
        
        # 在调仓日计算信号
        for i in range(20, len(trade_days), params.rebalance_days):
            current_date = trade_days[i]
            date_str = current_date.strftime('%Y-%m-%d') if hasattr(current_date, 'strftime') else str(current_date)
            
            for stock in sample_stocks:
                try:
                    # 获取历史数据
                    df = jq_client.get_price(
                        stock,
                        end_date=date_str,
                        count=65,
                        frequency='daily',
                        fields=['close', 'volume'],
                        fq='post'
                    )
                    
                    if df is None or len(df) < 25:
                        continue
                    
                    close = df['close'].values
                    volume = df['volume'].values
                    
                    # 计算信号
                    score, signal_type = calculate_chase_rise_signal(close, volume, params)
                    
                    if signal_type == SignalType.NO_SIGNAL or score < params.min_signal_score:
                        continue
                    
                    signal_count += 1
                    
                    # 计算未来5日收益
                    if i + 5 < len(trade_days):
                        future_date = trade_days[i + 5]
                        future_date_str = future_date.strftime('%Y-%m-%d') if hasattr(future_date, 'strftime') else str(future_date)
                        
                        future_df = jq_client.get_price(
                            stock,
                            end_date=future_date_str,
                            count=1,
                            frequency='daily',
                            fields=['close'],
                            fq='post'
                        )
                        
                        if future_df is not None and len(future_df) > 0:
                            entry_price = close[-1]
                            exit_price = future_df['close'].iloc[-1]
                            future_return = (exit_price / entry_price - 1) * 100
                            
                            all_returns.append(future_return)
                            if future_return > 0:
                                winning_count += 1
                
                except Exception:
                    continue
        
        if not all_returns:
            return BacktestResult()
        
        returns = np.array(all_returns)
        
        # 计算统计指标
        avg_return = np.mean(returns)
        win_rate = winning_count / len(returns) * 100 if len(returns) > 0 else 0
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(252 / 5) if len(returns) > 1 else 0
        
        # 最大回撤（简化）
        cumulative = np.cumprod(1 + returns / 100)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        return BacktestResult(
            total_return=avg_return * len(returns) / 5,
            weekly_return=avg_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=len(returns),
            total_signals=signal_count,
        )
    
    except Exception as e:
        logger.debug(f"回测失败: {e}")
        return BacktestResult()


def calculate_composite_score(result: BacktestResult) -> float:
    """计算综合评分"""
    score = (
        result.weekly_return * 0.4 +
        result.sharpe_ratio * 0.3 +
        (1 - abs(result.max_drawdown) / 100) * 0.2 +
        result.win_rate / 100 * 0.1
    )
    return score


# ==================== 网格搜索优化 ====================

def grid_search_optimize(
    jq_client,
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    param_grid: Dict[str, List],
    universe: List[str],
) -> Tuple[StrategyParams, List[Dict]]:
    """网格搜索优化"""
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
    
    start_time = time.time()
    combination_idx = 0
    
    for param_combo in product(*param_values):
        combination_idx += 1
        params_dict = dict(zip(param_names, param_combo))
        
        # 创建参数对象（补充默认值）
        full_params = {
            'limit_up_threshold': 0.095,
            'vol_ratio_threshold_first': 3.0,
            'mom_5d_threshold_breakout': 15.0,
            'mom_5d_threshold_volume': 10.0,
            'vol_ratio_threshold_breakout': 1.5,
            'vol_ratio_threshold_volume': 2.0,
            'min_signal_score': 55.0,
            'max_positions': 2,
            'stop_loss_pct': -10.0,
            'take_profit_pct': 25.0,
            'rebalance_days': 5,
        }
        full_params.update(params_dict)
        params = StrategyParams(**full_params)
        
        if combination_idx % 5 == 0:
            elapsed = time.time() - start_time
            eta = elapsed / combination_idx * (total_combinations - combination_idx)
            logger.info(f"  进度: {combination_idx}/{total_combinations} ({combination_idx/total_combinations*100:.1f}%) | ETA: {eta/60:.1f}分钟")
        
        # 训练集回测
        train_results = []
        for train_start, train_end in train_periods:
            result = run_simplified_backtest(
                jq_client, params, train_start, train_end, universe
            )
            train_results.append(result)
        
        # 平均训练结果
        if train_results:
            avg_train_result = BacktestResult(
                total_return=np.mean([r.total_return for r in train_results]),
                weekly_return=np.mean([r.weekly_return for r in train_results]),
                sharpe_ratio=np.mean([r.sharpe_ratio for r in train_results]),
                max_drawdown=np.mean([r.max_drawdown for r in train_results]),
                win_rate=np.mean([r.win_rate for r in train_results]),
                total_trades=int(np.mean([r.total_trades for r in train_results])),
                total_signals=int(np.mean([r.total_signals for r in train_results])),
            )
        else:
            avg_train_result = BacktestResult()
        
        # 验证集回测
        validate_result = run_simplified_backtest(
            jq_client, params, validate_period[0], validate_period[1], universe
        )
        
        # 计算综合评分
        train_score = calculate_composite_score(avg_train_result)
        validate_score = calculate_composite_score(validate_result)
        
        # 使用验证集评分作为最终评分
        score = validate_score
        
        # 记录优化历史
        history_entry = {
            'params': params_dict,
            'train_score': train_score,
            'train_weekly_return': avg_train_result.weekly_return,
            'train_sharpe': avg_train_result.sharpe_ratio,
            'train_win_rate': avg_train_result.win_rate,
            'train_max_drawdown': avg_train_result.max_drawdown,
            'validate_score': validate_score,
            'validate_weekly_return': validate_result.weekly_return,
            'validate_sharpe': validate_result.sharpe_ratio,
            'validate_win_rate': validate_result.win_rate,
            'validate_max_drawdown': validate_result.max_drawdown,
            'overfit_ratio': train_score / (validate_score + 1e-6) if validate_score != 0 else 0,
        }
        optimization_history.append(history_entry)
        
        # 更新最优参数
        if score > best_score:
            best_score = score
            best_params = params
            logger.info(f"  ✅ 新最优: 验证评分={score:.4f}, 周收益={validate_result.weekly_return:.2f}%, 胜率={validate_result.win_rate:.1f}%")
    
    total_time = time.time() - start_time
    logger.info(f"✅ 优化完成，用时: {total_time/60:.1f}分钟，最优评分: {best_score:.4f}")
    
    return best_params, optimization_history


# ==================== 主函数 ====================

def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("追涨策略递归迭代优化 - 完整运行")
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
        ('2019-06-01', '2020-03-31'),  # 缩短训练期以加速
        ('2024-09-01', '2025-01-10'),
    ]
    validate_period = ('2020-07-01', '2021-01-31')  # 缩短验证期以加速
    
    logger.info(f"\n数据集划分:")
    for i, (start, end) in enumerate(train_periods, 1):
        logger.info(f"  训练集{i}: {start} ~ {end}")
    logger.info(f"  验证集: {validate_period[0]} ~ {validate_period[1]}")
    
    # 获取股票池
    try:
        securities = jq.get_all_securities(types=['stock'], date=validate_period[1])
        stocks = securities.index.tolist()
        universe = [
            code for code in stocks
            if 'ST' not in str(securities.loc[code, 'display_name']).upper()
        ][:150]  # 限制150只股票
        logger.info(f"股票池: {len(universe)}只")
    except Exception as e:
        logger.error(f"获取股票池失败: {e}")
        return
    
    # 参数网格（精简版）
    param_grid = {
        'limit_up_threshold': [0.092, 0.095, 0.098],
        'vol_ratio_threshold_first': [2.5, 3.0, 3.5],
        'mom_5d_threshold_breakout': [14.0, 16.0],
        'mom_5d_threshold_volume': [9.0, 11.0],
        'max_positions': [2, 3],
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
        universe,
    )
    
    if best_params is None:
        logger.error("优化未找到任何结果")
        return
    
    # 打印最优参数
    logger.info("\n" + "=" * 70)
    logger.info("🏆 最优参数")
    logger.info("=" * 70)
    print("\n最优参数:")
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
    
    # 保存优化历史
    history_df = pd.DataFrame(history)
    history_df = history_df.sort_values('validate_score', ascending=False)
    history_path = output_dir / f'optimization_history_{timestamp}.csv'
    history_df.to_csv(history_path, index=False, encoding='utf-8-sig')
    logger.info(f"✅ 优化历史已保存: {history_path}")
    
    # 打印Top 10参数组合
    print("\n📊 Top 10 参数组合:")
    print("-" * 70)
    top10 = history_df.head(10)
    for i, row in top10.iterrows():
        print(f"  {i+1}. 验证评分={row['validate_score']:.4f}, "
              f"周收益={row['validate_weekly_return']:.2f}%, "
              f"胜率={row['validate_win_rate']:.1f}%, "
              f"过拟合比={row['overfit_ratio']:.2f}")
    
    # 生成优化后的QMT代码
    logger.info("\n" + "=" * 70)
    logger.info("生成优化后的QMT策略代码")
    logger.info("=" * 70)
    
    try:
        from core.qmt.chase_rise_strategy_generator import (
            ChaseRiseStrategyConfig,
            ChaseRiseStrategyGenerator,
        )
        
        config = ChaseRiseStrategyConfig(
            rebalance_days=best_params.rebalance_days,
            limit_up_threshold=best_params.limit_up_threshold,
            vol_ratio_threshold_first=best_params.vol_ratio_threshold_first,
            mom_5d_threshold_breakout=best_params.mom_5d_threshold_breakout,
            mom_5d_threshold_volume=best_params.mom_5d_threshold_volume,
            vol_ratio_threshold_breakout=best_params.vol_ratio_threshold_breakout,
            vol_ratio_threshold_volume=best_params.vol_ratio_threshold_volume,
            max_positions=best_params.max_positions,
            stop_loss_pct=best_params.stop_loss_pct,
            take_profit_pct=best_params.take_profit_pct,
        )
        
        generator = ChaseRiseStrategyGenerator(config)
        qmt_code = generator.generate_backtest_code()
        
        # 保存QMT代码
        qmt_path = output_dir / f'TRQuant_ChaseRise_Optimized_{timestamp}.py'
        with open(qmt_path, 'w', encoding='utf-8') as f:
            f.write(qmt_code)
        logger.info(f"✅ QMT策略代码已保存: {qmt_path}")
        print(f"\n📄 QMT代码长度: {len(qmt_code)} 字符")
        
    except Exception as e:
        logger.error(f"生成QMT代码失败: {e}")
        import traceback
        traceback.print_exc()
    
    logger.info("\n" + "=" * 70)
    logger.info("优化完成！")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
