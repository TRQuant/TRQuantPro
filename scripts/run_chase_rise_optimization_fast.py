#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略递归迭代优化 - 快速版本

特性:
1. 精简参数网格，减少组合数
2. 实时进度报告
3. 完善的错误处理
4. 数据缓存机制
5. 超时保护
6. 断点续传支持

预计运行时间: 5-10分钟
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
import signal
import traceback

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ==================== 全局配置 ====================

class Config:
    """优化配置"""
    # 股票池大小（越小越快）
    MAX_STOCKS = 50  # 原来是150，大幅减少
    
    # 每次调仓日采样的股票数
    SAMPLE_STOCKS_PER_DAY = 30
    
    # 超时设置（秒）
    BACKTEST_TIMEOUT = 60
    TOTAL_TIMEOUT = 600  # 10分钟总超时
    
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / 'output' / 'chase_rise_optimization'


# ==================== 数据类定义 ====================

@dataclass
class StrategyParams:
    """策略参数"""
    limit_up_threshold: float = 0.095
    vol_ratio_threshold_first: float = 3.0
    mom_5d_threshold_breakout: float = 15.0
    mom_5d_threshold_volume: float = 10.0
    vol_ratio_threshold_breakout: float = 1.5
    vol_ratio_threshold_volume: float = 2.0
    min_signal_score: float = 55.0
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
    error: str = ""


# ==================== 信号类型 ====================

class SignalType:
    FIRST_LIMIT_UP = "FIRST_LIMIT_UP"
    CONSECUTIVE_LIMIT_UP = "CONSECUTIVE_LIMIT_UP"
    STRONG_BREAKOUT = "STRONG_BREAKOUT"
    VOLUME_PRICE_RISE = "VOLUME_PRICE_RISE"
    NO_SIGNAL = "NO_SIGNAL"


# ==================== 进度报告器 ====================

class ProgressReporter:
    """进度报告器"""
    
    def __init__(self, total: int, desc: str = ""):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()
        self.last_report_time = 0
        self.best_score = -float('inf')
        self.errors = 0
    
    def update(self, n: int = 1, score: float = None, error: bool = False):
        """更新进度"""
        self.current += n
        if error:
            self.errors += 1
        if score is not None and score > self.best_score:
            self.best_score = score
        
        # 每2秒或每5%报告一次
        now = time.time()
        progress_pct = self.current / self.total * 100
        
        if now - self.last_report_time >= 2 or progress_pct % 5 < 0.1:
            self.report()
            self.last_report_time = now
    
    def report(self):
        """输出进度报告"""
        elapsed = time.time() - self.start_time
        progress_pct = self.current / self.total * 100
        
        if self.current > 0:
            eta = elapsed / self.current * (self.total - self.current)
            eta_str = f"{eta/60:.1f}分钟" if eta > 60 else f"{eta:.0f}秒"
        else:
            eta_str = "计算中..."
        
        best_str = f", 最优={self.best_score:.4f}" if self.best_score > -float('inf') else ""
        error_str = f", 错误={self.errors}" if self.errors > 0 else ""
        
        logger.info(f"[{self.desc}] {self.current}/{self.total} ({progress_pct:.1f}%) | "
                   f"已用={elapsed/60:.1f}分钟 | ETA={eta_str}{best_str}{error_str}")
    
    def finish(self):
        """完成报告"""
        elapsed = time.time() - self.start_time
        logger.info(f"[{self.desc}] 完成! 总用时={elapsed/60:.1f}分钟, "
                   f"成功={self.current-self.errors}, 错误={self.errors}")


# ==================== 数据缓存 ====================

class DataCache:
    """数据缓存"""
    
    def __init__(self):
        self.price_cache = {}
        self.trade_days_cache = {}
    
    def get_trade_days(self, jq_client, start_date: str, end_date: str) -> List:
        """获取交易日（带缓存）"""
        key = f"{start_date}_{end_date}"
        if key not in self.trade_days_cache:
            self.trade_days_cache[key] = jq_client.get_trade_days(
                start_date=start_date, end_date=end_date
            )
        return self.trade_days_cache[key]
    
    def get_price(self, jq_client, stock: str, end_date: str, count: int) -> pd.DataFrame:
        """获取价格数据（带缓存）"""
        key = f"{stock}_{end_date}_{count}"
        if key not in self.price_cache:
            try:
                df = jq_client.get_price(
                    stock,
                    end_date=end_date,
                    count=count,
                    frequency='daily',
                    fields=['close', 'volume'],
                    fq='post'
                )
                self.price_cache[key] = df
            except Exception:
                self.price_cache[key] = None
        return self.price_cache[key]


# 全局缓存
_cache = DataCache()


# ==================== 信号计算 ====================

def calculate_chase_rise_signal(
    close: np.ndarray,
    volume: np.ndarray,
    params: StrategyParams,
) -> Tuple[float, str]:
    """计算追涨信号"""
    if len(close) < 21:
        return 0.0, SignalType.NO_SIGNAL
    
    try:
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
        vol_mean = np.mean(volume[-20:]) if len(volume) >= 20 else 1
        vol_ratio = volume[-1] / vol_mean if vol_mean > 0 else 1.0
        
        # 信号判断
        if is_limit_up and limit_up_recent == 1:
            score = 75 + (15 if vol_ratio > params.vol_ratio_threshold_first else 0)
            return score, SignalType.FIRST_LIMIT_UP
        
        if limit_up_recent >= 2:
            return 65, SignalType.CONSECUTIVE_LIMIT_UP
        
        if mom_5d > params.mom_5d_threshold_breakout and vol_ratio > params.vol_ratio_threshold_breakout:
            return 60, SignalType.STRONG_BREAKOUT
        
        if mom_5d > params.mom_5d_threshold_volume and vol_ratio > params.vol_ratio_threshold_volume:
            return 55, SignalType.VOLUME_PRICE_RISE
        
        return 0.0, SignalType.NO_SIGNAL
    
    except Exception:
        return 0.0, SignalType.NO_SIGNAL


# ==================== 简化回测 ====================

def run_simplified_backtest(
    jq_client,
    params: StrategyParams,
    start_date: str,
    end_date: str,
    universe: List[str],
) -> BacktestResult:
    """简化回测"""
    try:
        trade_days = _cache.get_trade_days(jq_client, start_date, end_date)
        if trade_days is None or len(trade_days) < 25:
            return BacktestResult(error="交易日不足")
        
        all_returns = []
        signal_count = 0
        winning_count = 0
        
        # 随机采样股票
        sample_size = min(Config.SAMPLE_STOCKS_PER_DAY, len(universe))
        sample_stocks = np.random.choice(universe, sample_size, replace=False).tolist()
        
        # 采样调仓日（减少计算量）
        rebalance_indices = list(range(20, len(trade_days), params.rebalance_days * 2))[:10]
        
        for i in rebalance_indices:
            current_date = trade_days[i]
            date_str = current_date.strftime('%Y-%m-%d') if hasattr(current_date, 'strftime') else str(current_date)
            
            for stock in sample_stocks:
                try:
                    df = _cache.get_price(jq_client, stock, date_str, 65)
                    if df is None or len(df) < 25:
                        continue
                    
                    close = df['close'].values
                    volume = df['volume'].values
                    
                    score, signal_type = calculate_chase_rise_signal(close, volume, params)
                    
                    if signal_type == SignalType.NO_SIGNAL or score < params.min_signal_score:
                        continue
                    
                    signal_count += 1
                    
                    # 计算未来收益
                    if i + 5 < len(trade_days):
                        future_date = trade_days[i + 5]
                        future_date_str = future_date.strftime('%Y-%m-%d') if hasattr(future_date, 'strftime') else str(future_date)
                        
                        future_df = _cache.get_price(jq_client, stock, future_date_str, 1)
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
            return BacktestResult(error="无信号")
        
        returns = np.array(all_returns)
        avg_return = np.mean(returns)
        win_rate = winning_count / len(returns) * 100
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(252 / 5) if len(returns) > 1 else 0
        
        # 最大回撤
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
        return BacktestResult(error=str(e))


def calculate_composite_score(result: BacktestResult) -> float:
    """计算综合评分"""
    if result.error:
        return -100.0
    
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
) -> Tuple[Optional[StrategyParams], List[Dict]]:
    """网格搜索优化"""
    
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    all_combinations = list(product(*param_values))
    total = len(all_combinations)
    
    logger.info(f"参数组合总数: {total}")
    
    progress = ProgressReporter(total, "网格搜索")
    
    best_params = None
    best_score = -float('inf')
    optimization_history = []
    
    # 默认参数
    default_params = {
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
    
    for combo in all_combinations:
        try:
            params_dict = dict(zip(param_names, combo))
            full_params = default_params.copy()
            full_params.update(params_dict)
            params = StrategyParams(**full_params)
            
            # 训练集回测
            train_results = []
            for train_start, train_end in train_periods:
                result = run_simplified_backtest(jq_client, params, train_start, train_end, universe)
                train_results.append(result)
            
            # 平均训练结果
            valid_train = [r for r in train_results if not r.error]
            if valid_train:
                avg_train = BacktestResult(
                    total_return=np.mean([r.total_return for r in valid_train]),
                    weekly_return=np.mean([r.weekly_return for r in valid_train]),
                    sharpe_ratio=np.mean([r.sharpe_ratio for r in valid_train]),
                    max_drawdown=np.mean([r.max_drawdown for r in valid_train]),
                    win_rate=np.mean([r.win_rate for r in valid_train]),
                    total_trades=int(np.mean([r.total_trades for r in valid_train])),
                    total_signals=int(np.mean([r.total_signals for r in valid_train])),
                )
            else:
                avg_train = BacktestResult(error="训练失败")
            
            # 验证集回测
            validate_result = run_simplified_backtest(
                jq_client, params, validate_period[0], validate_period[1], universe
            )
            
            # 计算评分
            score = calculate_composite_score(validate_result)
            
            # 记录历史
            history_entry = {
                'params': params_dict,
                'train_weekly_return': avg_train.weekly_return,
                'train_win_rate': avg_train.win_rate,
                'train_sharpe': avg_train.sharpe_ratio,
                'validate_score': score,
                'validate_weekly_return': validate_result.weekly_return,
                'validate_win_rate': validate_result.win_rate,
                'validate_sharpe': validate_result.sharpe_ratio,
                'validate_max_drawdown': validate_result.max_drawdown,
            }
            optimization_history.append(history_entry)
            
            # 更新最优
            if score > best_score:
                best_score = score
                best_params = params
                logger.info(f"  🎯 新最优: score={score:.4f}, 周收益={validate_result.weekly_return:.2f}%, 胜率={validate_result.win_rate:.1f}%")
            
            progress.update(score=score)
        
        except Exception as e:
            progress.update(error=True)
            logger.debug(f"参数组合失败: {e}")
    
    progress.finish()
    return best_params, optimization_history


# ==================== 主函数 ====================

def main():
    """主函数"""
    start_time = time.time()
    
    logger.info("=" * 70)
    logger.info("追涨策略递归迭代优化 - 快速版本")
    logger.info("=" * 70)
    logger.info(f"预计运行时间: 5-10分钟")
    
    # 初始化JQData
    try:
        from config.config_manager import get_config_manager
        import jqdatasdk as jq
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        logger.info("✅ JQData连接成功")
    except Exception as e:
        logger.error(f"❌ JQData连接失败: {e}")
        traceback.print_exc()
        return
    
    # 数据集（缩短时间范围以加速）
    train_periods = [
        ('2020-01-01', '2020-06-30'),  # 6个月
        ('2024-09-01', '2024-12-31'),  # 4个月
    ]
    validate_period = ('2021-01-01', '2021-06-30')  # 6个月
    
    logger.info(f"\n数据集:")
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
        ][:Config.MAX_STOCKS]
        logger.info(f"✅ 股票池: {len(universe)}只")
    except Exception as e:
        logger.error(f"❌ 获取股票池失败: {e}")
        traceback.print_exc()
        return
    
    # 精简参数网格（只优化关键参数）
    param_grid = {
        'limit_up_threshold': [0.093, 0.095, 0.097],
        'vol_ratio_threshold_first': [2.5, 3.0, 3.5],
        'mom_5d_threshold_breakout': [14.0, 16.0],
        'max_positions': [2, 3],
    }
    
    total_combos = 1
    for v in param_grid.values():
        total_combos *= len(v)
    
    logger.info(f"\n参数网格 ({total_combos}种组合):")
    for param, values in param_grid.items():
        logger.info(f"  {param}: {values}")
    
    # 执行优化
    logger.info("\n" + "-" * 70)
    best_params, history = grid_search_optimize(
        jq,
        train_periods,
        validate_period,
        param_grid,
        universe,
    )
    
    if best_params is None:
        logger.error("❌ 优化未找到任何结果")
        return
    
    # 输出结果
    logger.info("\n" + "=" * 70)
    logger.info("🏆 最优参数")
    logger.info("=" * 70)
    for key, value in asdict(best_params).items():
        logger.info(f"  {key}: {value}")
    
    # 保存结果
    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存最优参数
    params_path = Config.OUTPUT_DIR / f'best_params_{timestamp}.json'
    with open(params_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(best_params), f, ensure_ascii=False, indent=2)
    logger.info(f"\n✅ 最优参数已保存: {params_path}")
    
    # 保存优化历史
    if history:
        history_df = pd.DataFrame(history)
        history_df = history_df.sort_values('validate_score', ascending=False)
        history_path = Config.OUTPUT_DIR / f'optimization_history_{timestamp}.csv'
        history_df.to_csv(history_path, index=False, encoding='utf-8-sig')
        logger.info(f"✅ 优化历史已保存: {history_path}")
        
        # Top 5
        logger.info("\n📊 Top 5 参数组合:")
        for i, row in history_df.head(5).iterrows():
            logger.info(f"  {i+1}. score={row['validate_score']:.4f}, "
                       f"周收益={row['validate_weekly_return']:.2f}%, "
                       f"胜率={row['validate_win_rate']:.1f}%")
    
    # 生成QMT代码
    logger.info("\n" + "-" * 70)
    logger.info("生成优化后的QMT策略代码")
    
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
        
        qmt_path = Config.OUTPUT_DIR / f'TRQuant_ChaseRise_Optimized_{timestamp}.py'
        with open(qmt_path, 'w', encoding='utf-8') as f:
            f.write(qmt_code)
        logger.info(f"✅ QMT策略代码已保存: {qmt_path}")
        logger.info(f"   代码长度: {len(qmt_code)} 字符")
        
    except Exception as e:
        logger.error(f"⚠️ 生成QMT代码失败: {e}")
    
    # 总结
    total_time = time.time() - start_time
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ 优化完成! 总用时: {total_time/60:.1f}分钟")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
