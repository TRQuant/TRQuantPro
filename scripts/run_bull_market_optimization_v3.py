#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略递归迭代优化 V3
================================

正式版本 - 使用完整BulletTrade回测引擎 + 严格错误处理

核心特性：
1. 使用正式BulletTradeBacktest回测（非简化版）
2. 集成DataPreloader数据预加载
3. GPU加速因子计算
4. 递归优化框架（粗网格→细网格→收敛）
5. 过拟合检测和惩罚机制
6. **严格错误处理：任何错误立即停止，需修复后重新运行**

目标: 周收益10%+ (激进策略)
回测引擎: BulletTrade (JQData数据源)
优化方法: 递归网格搜索 + 训练集/验证集分离

依赖模块:
- core.advisor_v4.bullettrade_backtest.BulletTradeBacktest
- core.advisor_v4.bullettrade_strategy_generator.StrategyConfig
- core.advisor_v4.data_preloader.DataPreloader
- core.bullettrade.result.BTResult
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
import numpy as np
import logging
import json
from dataclasses import dataclass, asdict, field
from itertools import product
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

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


# ==================== 严格错误处理类 ====================

class FatalError(Exception):
    """致命错误 - 必须停止运行"""
    pass


def check_and_raise(error_message: str, condition: bool = True):
    """
    检查条件，如果失败则抛出致命错误
    
    原则：如果某一步出现错误，立即停止运行，修复后再运行
    
    Args:
        error_message: 错误消息
        condition: 检查条件（True表示正常，False表示错误）
    """
    if not condition:
        logger.error(f"❌ 致命错误: {error_message}")
        logger.error("⚠️ 根据标准开发流程：遇到错误必须停止运行，修复后再运行")
        raise FatalError(error_message)


# ==================== 全局配置 ====================

class Config:
    """优化配置"""
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / 'output' / 'bull_market_optimization_v3'
    
    # 缓存目录
    CACHE_DIR = PROJECT_ROOT / 'data' / 'cache'
    
    # 递归优化配置
    MAX_RECURSIVE_ITERATIONS = 3    # 最大递归次数
    REFINEMENT_RATIO = 0.5          # 每次细化范围缩小比例
    CONVERGENCE_THRESHOLD = 0.05    # 收敛阈值（5%变化）
    
    # 过拟合检测
    OVERFIT_PENALTY_THRESHOLD = 2.0 # 过拟合惩罚阈值
    OVERFIT_PENALTY_FACTOR = 0.3    # 过拟合惩罚因子
    
    # 回测配置
    INITIAL_CAPITAL = 1000000.0     # 初始资金
    BENCHMARK = '000300.XSHG'       # 基准指数
    
    # 并行配置
    MAX_PARALLEL_BACKTESTS = 2      # 最大并行回测数（BulletTrade消耗资源较大）


# ==================== 数据类定义 ====================

@dataclass
class BullMarketStrategyParams:
    """牛市策略参数 - 映射到StrategyConfig"""
    
    # === 选股参数 ===
    max_stocks: int = 10                # 最大持股数量
    min_total_score: float = 30.0       # 最小综合得分
    
    # === 仓位参数 ===
    single_position_max: float = 0.20   # 单票最大仓位（20%）
    
    # === 止损止盈参数 ===
    stop_loss: float = -0.08            # 固定止损（-8%）
    take_profit: float = 0.30           # 固定止盈（+30%）
    trailing_stop: float = -0.08        # 移动止损（-8%）
    trailing_stop_trigger: float = 0.15 # 移动止损触发条件（盈利15%后启用）
    time_stop_days: int = 20            # 时间止损（持仓超过20个交易日）
    
    # === 因子筛选阈值 ===
    min_momentum_20d: float = 5.0       # 最小20日动量（%）
    max_momentum_20d: float = 30.0      # 最大20日动量（%）
    max_rel_position: float = 80.0      # 最大相对位置（%）
    min_market_cap: float = 30.0        # 最小市值（亿）
    max_market_cap: float = 200.0       # 最大市值（亿）
    min_momentum_5d: float = -5.0       # 最小5日动量（%）
    max_momentum_5d: float = 10.0       # 最大5日动量（%）
    min_turnover_rate: float = 2.0      # 最小换手率（%）
    max_turnover_rate: float = 10.0     # 最大换手率（%）
    min_roe: float = 0.0                # 最小ROE（%）
    
    def to_strategy_config(self):
        """转换为StrategyConfig"""
        from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig
        
        return StrategyConfig(
            max_stocks=self.max_stocks,
            min_total_score=self.min_total_score,
            single_position_max=self.single_position_max,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit,
            trailing_stop=self.trailing_stop,
            trailing_stop_trigger=self.trailing_stop_trigger,
            time_stop_days=self.time_stop_days,
            min_momentum_20d=self.min_momentum_20d,
            max_momentum_20d=self.max_momentum_20d,
            max_rel_position=self.max_rel_position,
            min_market_cap=self.min_market_cap,
            max_market_cap=self.max_market_cap,
            min_momentum_5d=self.min_momentum_5d,
            max_momentum_5d=self.max_momentum_5d,
            min_turnover_rate=self.min_turnover_rate,
            max_turnover_rate=self.max_turnover_rate,
            min_roe=self.min_roe,
        )


@dataclass
class BacktestResult:
    """回测结果（从BTResult转换）"""
    total_return: float = 0.0           # 总收益率（%）
    annual_return: float = 0.0          # 年化收益率（%）
    sharpe_ratio: float = 0.0           # 夏普比率
    max_drawdown: float = 0.0           # 最大回撤（%）
    win_rate: float = 0.0               # 胜率（%）
    total_trades: int = 0               # 总交易次数
    runtime_seconds: float = 0.0        # 运行耗时
    error: str = ""                     # 错误信息
    
    @classmethod
    def from_bt_result(cls, bt_result) -> "BacktestResult":
        """从BTResult转换"""
        if bt_result is None:
            return cls(error="BTResult为None")
        
        return cls(
            total_return=bt_result.total_return,
            annual_return=bt_result.annual_return,
            sharpe_ratio=bt_result.sharpe_ratio,
            max_drawdown=bt_result.max_drawdown,
            win_rate=bt_result.win_rate,
            total_trades=bt_result.total_trades,
            runtime_seconds=bt_result.runtime_seconds,
        )


# ==================== 数据预加载器 ====================

class DataCacheManager:
    """数据缓存管理器 - 封装DataPreloader"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.cache_dir = Config.CACHE_DIR
        self.preloader = None
        
        # 初始化数据预加载器（严格错误处理）
        try:
            from core.advisor_v4.data_preloader import DataPreloader
            self.preloader = DataPreloader(
                max_workers=3,  # JQData正式账号支持3个并发连接
                cache_dir=str(self.cache_dir),
                verbose=True,
                use_mongodb=True
            )
            check_and_raise("DataPreloader初始化失败", self.preloader is not None)
            logger.info("✅ DataPreloader已初始化（MongoDB支持）")
        except Exception as e:
            logger.error(f"❌ DataPreloader初始化异常: {e}")
            traceback.print_exc()
            raise FatalError(f"DataPreloader初始化失败: {e}")
        
        self._initialized = True
    
    def preload_data(self, start_date: str, end_date: str, stock_pool: List[str] = None, force_refresh: bool = False):
        """预加载数据到缓存（严格错误处理）"""
        check_and_raise("DataPreloader未初始化", self.preloader is not None)
        
        try:
            result = self.preloader.preload_market_data(
                start_date=start_date,
                end_date=end_date,
                stock_pool=stock_pool,
                force_refresh=force_refresh
            )
            check_and_raise("数据预加载返回None", result is not None)
            logger.info(f"✅ 数据预加载完成: {result.total_stocks}只股票, {result.total_trading_days}交易日")
            return result
        except FatalError:
            raise
        except Exception as e:
            logger.error(f"❌ 数据预加载异常: {e}")
            traceback.print_exc()
            raise FatalError(f"数据预加载失败: {e}")


# 全局数据缓存管理器
_cache_manager = None

def get_cache_manager() -> DataCacheManager:
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = DataCacheManager()
    return _cache_manager


# ==================== 进度报告器 ====================

class ProgressReporter:
    """进度报告器（带迭代信息）"""
    
    def __init__(self, total: int, desc: str = "", iteration: int = 1):
        self.total = total
        self.current = 0
        self.desc = desc
        self.iteration = iteration
        self.start_time = time.time()
        self.last_report_time = 0
        self.best_score = -float('inf')
        self.errors = 0
        self._lock = threading.Lock()
    
    def update(self, n: int = 1, score: float = None, error: bool = False):
        """更新进度（线程安全）"""
        with self._lock:
            self.current += n
            if error:
                self.errors += 1
            if score is not None and score > self.best_score:
                self.best_score = score
            
            now = time.time()
            progress_pct = self.current / self.total * 100
            
            if now - self.last_report_time >= 10 or progress_pct % 20 < 0.5:  # BulletTrade较慢，降低报告频率
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
        iter_str = f"[迭代{self.iteration}] " if self.iteration > 1 else ""
        
        logger.info(f"{iter_str}[{self.desc}] {self.current}/{self.total} ({progress_pct:.1f}%) | "
                   f"已用={elapsed/60:.1f}分钟 | ETA={eta_str}{best_str}{error_str}")
    
    def finish(self):
        """完成报告"""
        elapsed = time.time() - self.start_time
        iter_str = f"[迭代{self.iteration}] " if self.iteration > 1 else ""
        logger.info(f"{iter_str}[{self.desc}] 完成! 总用时={elapsed/60:.1f}分钟, "
                   f"成功={self.current-self.errors}, 错误={self.errors}")


# ==================== BulletTrade回测封装 ====================

def run_bullettrade_backtest(
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    task_id: str = None,
) -> BacktestResult:
    """
    执行正式BulletTrade回测（严格错误处理）
    
    Args:
        params: 策略参数
        start_date: 开始日期
        end_date: 结束日期
        task_id: 任务ID（用于输出目录）
    
    Returns:
        BacktestResult: 回测结果
    
    Raises:
        FatalError: 如果回测失败
    """
    start_time = time.time()
    
    try:
        from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest
        from core.bullettrade.config import BTConfig
        
        # 转换为StrategyConfig
        strategy_config = params.to_strategy_config()
        check_and_raise("StrategyConfig创建失败", strategy_config is not None)
        
        # 创建输出目录
        if task_id is None:
            task_id = f"backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_dir = Config.OUTPUT_DIR / 'backtests' / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置BulletTrade
        bt_config = BTConfig(
            start_date=start_date,
            end_date=end_date,
            initial_capital=Config.INITIAL_CAPITAL,
            benchmark=Config.BENCHMARK,
            frequency='day',
            data_provider='jqdata',
            output_dir=str(output_dir),
            generate_html=False,  # 优化过程中不生成HTML
            generate_csv=False,
        )
        
        # 创建回测实例
        backtest = BulletTradeBacktest(
            strategy_config=strategy_config,
            bt_config=bt_config,
            output_dir=str(output_dir),
            cache_dir=str(Config.CACHE_DIR)
        )
        check_and_raise("BulletTradeBacktest创建失败", backtest is not None)
        
        # 执行回测
        bt_result = backtest.run_backtest(
            start_date=start_date,
            end_date=end_date,
            initial_capital=Config.INITIAL_CAPITAL
        )
        
        check_and_raise(f"回测返回None（可能回测失败）", bt_result is not None)
        
        # 转换结果
        result = BacktestResult.from_bt_result(bt_result)
        result.runtime_seconds = time.time() - start_time
        
        # 检查回测是否有错误
        if result.error:
            raise FatalError(f"回测失败: {result.error}")
        
        # 检查回测结果有效性（严格错误处理）
        # 如果总收益为0且没有交易，可能是数据获取失败
        if result.total_return == 0.0 and result.total_trades == 0:
            raise FatalError(
                f"回测结果无效: 总收益为0且无交易（可能是数据获取失败）。"
                f"请检查：1) 数据是否已正确预加载 2) 策略代码是否正确 3) 股票池是否为空"
            )
        
        # 检查回测是否异常（年化收益为0且夏普比率异常）
        if result.annual_return == 0.0 and abs(result.sharpe_ratio) > 1000:
            raise FatalError(
                f"回测结果异常: 年化收益为0且夏普比率异常（{result.sharpe_ratio:.2f}）。"
                f"可能是数据问题或策略逻辑错误"
            )
        
        return result
    
    except FatalError:
        raise
    except Exception as e:
        logger.error(f"❌ BulletTrade回测异常: {e}")
        traceback.print_exc()
        raise FatalError(f"BulletTrade回测失败: {e}")


def calculate_composite_score(result: BacktestResult, overfit_ratio: float = 1.0) -> float:
    """
    计算综合评分 - 带过拟合惩罚
    
    Args:
        result: 回测结果
        overfit_ratio: 过拟合比率（train_score / validate_score）
    """
    if result.error:
        return -100.0
    
    base_score = (
        result.annual_return * 0.35 +           # 年化收益权重35%
        result.sharpe_ratio * 10 * 0.25 +       # 夏普比率权重25%（乘10归一化）
        (100 - abs(result.max_drawdown)) / 100 * 20 * 0.20 +  # 回撤控制20%
        result.win_rate * 0.20                  # 胜率权重20%
    )
    
    # 过拟合惩罚
    if overfit_ratio > Config.OVERFIT_PENALTY_THRESHOLD:
        penalty = (overfit_ratio - 1) * Config.OVERFIT_PENALTY_FACTOR
        base_score = base_score * (1 - min(penalty, 0.5))  # 最多惩罚50%
    
    return base_score


# ==================== 递归优化框架 ====================

def refine_param_grid(
    best_params: BullMarketStrategyParams,
    current_grid: Dict[str, List],
    refinement_ratio: float = 0.5
) -> Dict[str, List]:
    """围绕最优参数细化网格"""
    refined_grid = {}
    params_dict = asdict(best_params)
    
    for param_name, current_values in current_grid.items():
        if param_name not in params_dict:
            continue
        
        best_value = params_dict[param_name]
        current_min = min(current_values)
        current_max = max(current_values)
        n_values = len(current_values)
        
        # 计算细化范围
        range_size = (current_max - current_min) * refinement_ratio
        new_min = max(best_value - range_size / 2, current_min)
        new_max = min(best_value + range_size / 2, current_max)
        
        # 生成新的参数值列表
        if isinstance(best_value, int):
            new_values = np.linspace(new_min, new_max, n_values).astype(int)
            refined_grid[param_name] = list(np.unique(new_values))
        else:
            refined_grid[param_name] = list(np.round(np.linspace(new_min, new_max, n_values), 3))
    
    return refined_grid


def check_convergence(
    prev_best: Optional[BullMarketStrategyParams],
    current_best: BullMarketStrategyParams,
    threshold: float = 0.05
) -> bool:
    """检测是否收敛"""
    if prev_best is None:
        return False
    
    prev_dict = asdict(prev_best)
    curr_dict = asdict(current_best)
    
    for param_name in curr_dict:
        prev_val = prev_dict.get(param_name)
        curr_val = curr_dict[param_name]
        
        if isinstance(curr_val, (int, float)) and prev_val is not None and prev_val != 0:
            change_ratio = abs(curr_val - prev_val) / abs(prev_val)
            if change_ratio > threshold:
                return False
    
    return True


def grid_search_optimize(
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    param_grid: Dict[str, List],
    iteration: int = 1,
) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
    """
    网格搜索优化 - 使用正式BulletTrade回测（严格错误处理）
    
    Args:
        train_periods: 训练集时间段列表
        validate_period: 验证集时间段
        param_grid: 参数网格
        iteration: 当前迭代次数
    
    Returns:
        (最优参数, 优化历史)
    
    Raises:
        FatalError: 如果优化过程出现致命错误
    """
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    all_combinations = list(product(*param_values))
    total = len(all_combinations)
    
    logger.info(f"参数组合总数: {total}")
    
    progress = ProgressReporter(total, "BulletTrade网格搜索", iteration)
    
    best_params = None
    best_score = -float('inf')
    optimization_history = []
    
    # 默认参数
    default_params = asdict(BullMarketStrategyParams())
    
    for combo_idx, combo in enumerate(all_combinations):
        try:
            params_dict = dict(zip(param_names, combo))
            full_params = default_params.copy()
            full_params.update(params_dict)
            params = BullMarketStrategyParams(**full_params)
            
            task_id = f"iter{iteration}_combo{combo_idx}"
            
            # 训练集回测（严格错误处理）
            train_results = []
            for period_idx, (train_start, train_end) in enumerate(train_periods):
                result = run_bullettrade_backtest(
                    params, 
                    train_start, 
                    train_end,
                    task_id=f"{task_id}_train{period_idx}"
                )
                train_results.append(result)
            
            # 平均训练结果
            valid_train = [r for r in train_results if not r.error]
            check_and_raise(f"所有训练集回测失败（组合{combo_idx}）", len(valid_train) > 0)
            
            avg_train = BacktestResult(
                total_return=np.mean([r.total_return for r in valid_train]),
                annual_return=np.mean([r.annual_return for r in valid_train]),
                sharpe_ratio=np.mean([r.sharpe_ratio for r in valid_train]),
                max_drawdown=np.mean([r.max_drawdown for r in valid_train]),
                win_rate=np.mean([r.win_rate for r in valid_train]),
                total_trades=int(np.mean([r.total_trades for r in valid_train])),
                runtime_seconds=sum([r.runtime_seconds for r in valid_train]),
            )
            
            # 验证集回测（严格错误处理）
            validate_result = run_bullettrade_backtest(
                params, 
                validate_period[0], 
                validate_period[1],
                task_id=f"{task_id}_validate"
            )
            
            # 计算评分
            train_score = calculate_composite_score(avg_train)
            validate_score_raw = calculate_composite_score(validate_result)
            
            # 过拟合比率
            overfit_ratio = train_score / (validate_score_raw + 1e-6) if validate_score_raw > 0 else 0
            
            # 最终评分（带过拟合惩罚）
            validate_score = calculate_composite_score(validate_result, overfit_ratio)
            score = validate_score
            
            # 记录历史
            history_entry = {
                'params': params_dict,
                'train_score': train_score,
                'train_annual_return': avg_train.annual_return,
                'train_sharpe': avg_train.sharpe_ratio,
                'train_win_rate': avg_train.win_rate,
                'train_max_drawdown': avg_train.max_drawdown,
                'train_total_trades': avg_train.total_trades,
                'validate_score': validate_score,
                'validate_score_raw': validate_score_raw,
                'validate_annual_return': validate_result.annual_return,
                'validate_sharpe': validate_result.sharpe_ratio,
                'validate_win_rate': validate_result.win_rate,
                'validate_max_drawdown': validate_result.max_drawdown,
                'validate_total_trades': validate_result.total_trades,
                'overfit_ratio': overfit_ratio,
                'iteration': iteration,
                'runtime_seconds': avg_train.runtime_seconds + validate_result.runtime_seconds,
            }
            optimization_history.append(history_entry)
            
            # 更新最优
            if score > best_score:
                best_score = score
                best_params = params
                logger.info(f"  🎯 新最优: score={score:.4f}, "
                           f"年化={validate_result.annual_return:.1f}%, "
                           f"夏普={validate_result.sharpe_ratio:.2f}, "
                           f"回撤={validate_result.max_drawdown:.1f}%, "
                           f"胜率={validate_result.win_rate:.1f}%")
            
            progress.update(score=score)
        
        except FatalError:
            # 致命错误：停止运行
            logger.error(f"❌ 组合{combo_idx}出现致命错误，停止优化")
            raise
        except Exception as e:
            # 非致命错误：记录但继续
            progress.update(error=True)
            logger.warning(f"参数组合{combo_idx}失败: {e}")
            traceback.print_exc()
    
    progress.finish()
    return best_params, optimization_history


def recursive_grid_search(
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    initial_param_grid: Dict[str, List],
    max_iterations: int = 3,
    refinement_ratio: float = 0.5,
) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
    """
    递归网格搜索优化（严格错误处理）
    
    粗网格 → 细网格 → 收敛
    """
    logger.info("=" * 70)
    logger.info("开始递归网格搜索优化（BulletTrade正式回测）")
    logger.info(f"最大迭代次数: {max_iterations}, 细化比例: {refinement_ratio}")
    logger.info("=" * 70)
    
    current_grid = initial_param_grid
    prev_best = None
    all_history = []
    
    for iteration in range(1, max_iterations + 1):
        logger.info(f"\n{'='*30} 迭代 {iteration}/{max_iterations} {'='*30}")
        
        # 显示当前网格
        total_combos = 1
        for v in current_grid.values():
            total_combos *= len(v)
        logger.info(f"当前参数网格 ({total_combos}种组合):")
        for param, values in current_grid.items():
            logger.info(f"  {param}: {values}")
        
        # 执行网格搜索（严格错误处理）
        try:
            best_params, history = grid_search_optimize(
                train_periods,
                validate_period,
                current_grid,
                iteration=iteration,
            )
        except FatalError as e:
            logger.error(f"❌ 迭代{iteration}出现致命错误，停止递归优化")
            logger.error(f"错误信息: {e}")
            logger.error("⚠️ 请修复错误后重新运行")
            raise
        
        check_and_raise(f"迭代{iteration}未找到有效参数", best_params is not None)
        
        all_history.extend(history)
        
        # 检查收敛
        if check_convergence(prev_best, best_params, Config.CONVERGENCE_THRESHOLD):
            logger.info(f"✅ 参数已收敛，提前结束递归优化")
            break
        
        # 细化网格
        if iteration < max_iterations:
            current_grid = refine_param_grid(best_params, current_grid, refinement_ratio)
        
        prev_best = best_params
    
    return best_params, all_history


# ==================== JQData权限检查 ====================

def check_jqdata_permission():
    """
    检查JQData账号权限（严格错误处理）
    
    检查项：
    1. JQData SDK是否安装
    2. 账号认证是否成功
    3. 账号类型是否为正式账号
    4. 数据范围是否无限制
    5. 数据访问是否正常
    6. 设置环境变量供BulletTrade使用
    
    Raises:
        FatalError: 如果任何检查失败
    """
    import os
    
    logger.info("\n" + "=" * 70)
    logger.info("JQData权限检查")
    logger.info("=" * 70)
    
    # 1. 检查SDK安装
    try:
        import jqdatasdk as jq
        logger.info("✅ jqdatasdk已安装")
    except ImportError as e:
        raise FatalError(f"jqdatasdk未安装: {e}")
    
    # 2. 读取配置
    try:
        from config.config_manager import get_config_manager
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        check_and_raise("配置文件中缺少用户名", username is not None)
        check_and_raise("配置文件中缺少密码", password is not None)
        logger.info(f"✅ 配置文件读取成功: {username}")
        
        # 关键！设置环境变量供BulletTrade使用
        # BulletTrade引擎内部使用这些环境变量来认证JQData
        os.environ['JQDATA_USERNAME'] = username
        os.environ['JQDATA_USER'] = username
        os.environ['JQDATA_PASSWORD'] = password
        os.environ['JQDATA_PWD'] = password
        logger.info("✅ JQData环境变量已设置（供BulletTrade使用）")
        
    except Exception as e:
        raise FatalError(f"读取JQData配置失败: {e}")
    
    # 3. 认证
    try:
        jq.auth(username, password)
        logger.info("✅ JQData认证成功")
    except Exception as e:
        raise FatalError(f"JQData认证失败: {e}")
    
    # 4. 查询账号信息
    try:
        account_info = jq.get_account_info()
        check_and_raise("get_account_info返回None", account_info is not None)
        logger.info("✅ 账号信息查询成功")
    except Exception as e:
        raise FatalError(f"查询账号信息失败: {e}")
    
    # 5. 检查账号类型
    query_limit = account_info.get('query_count_limit', 0)
    license_type = account_info.get('license', 0)
    date_range_start = account_info.get('date_range_start', 'N/A')
    date_range_end = account_info.get('date_range_end', 'N/A')
    
    logger.info(f"  每日流量限制: {query_limit:,}条/天")
    logger.info(f"  License类型: {license_type}")
    logger.info(f"  数据开始日期: {date_range_start}")
    logger.info(f"  数据结束日期: {date_range_end}")
    
    # 检查是否为正式账号
    is_premium = query_limit >= 200000000  # 2亿条/天
    is_unlimited = date_range_start == '*' or date_range_end == '*'
    
    if not is_premium:
        raise FatalError(f"账号不是正式账号（高级版），每日流量限制: {query_limit:,}条/天")
    
    if not is_unlimited:
        raise FatalError(f"数据范围受限: {date_range_start} ~ {date_range_end}（应该是*表示无限制）")
    
    logger.info("✅ 账号类型: 正式账号（高级版）")
    logger.info("✅ 数据范围: 无限制")
    
    # 6. 测试数据访问（测试2005年数据）
    try:
        test_data = jq.get_price('000001.XSHE', start_date='2005-01-01', end_date='2005-01-10', frequency='daily')
        check_and_raise("无法访问2005-01-01的历史数据（可能不在数据范围内）", len(test_data) > 0)
        logger.info(f"✅ 历史数据访问测试通过: 000001.XSHE ({len(test_data)}条记录)")
    except Exception as e:
        error_msg = str(e)
        if "超出范围" in error_msg or "不在范围内" in error_msg:
            raise FatalError(f"数据范围受限: 无法访问2005-01-01的历史数据（试用账号限制）")
        else:
            raise FatalError(f"历史数据访问测试失败: {e}")
    
    # 7. 测试指数成分股
    try:
        index_stocks = jq.get_index_stocks('000300.XSHG', date='2020-01-01')
        check_and_raise("无法获取指数成分股", len(index_stocks) > 0)
        logger.info(f"✅ 指数成分股访问测试通过: 000300.XSHG ({len(index_stocks)}只）")
    except Exception as e:
        raise FatalError(f"指数成分股访问测试失败: {e}")
    
    logger.info("=" * 70)
    logger.info("✅ JQData权限检查全部通过")
    logger.info("=" * 70)


# ==================== 主函数 ====================

def main():
    """主函数（严格错误处理）"""
    start_time = time.time()
    
    logger.info("=" * 70)
    logger.info("牛市极端高收益策略递归迭代优化 V3")
    logger.info("=" * 70)
    logger.info("目标: 周收益10%+ | 回测引擎: BulletTrade（正式版）")
    logger.info("加速技术: DataPreloader + MongoDB缓存")
    logger.info("错误处理: 严格模式（任何错误立即停止）")
    
    try:
        # 步骤0: JQData权限检查（必须在所有操作之前）
        check_jqdata_permission()
        # 数据集配置
        train_periods = [
            ('2020-01-01', '2020-06-30'),  # 牛市上涨期（缩短以加快测试）
        ]
        validate_period = ('2020-07-01', '2020-12-31')  # 牛市中期
        
        logger.info(f"\n数据集:")
        for i, (start, end) in enumerate(train_periods, 1):
            logger.info(f"  训练集{i}: {start} ~ {end}")
        logger.info(f"  验证集: {validate_period[0]} ~ {validate_period[1]}")
        
        # 初始化数据缓存（严格错误处理）
        logger.info("\n初始化数据缓存...")
        cache_manager = get_cache_manager()
        
        # 预加载所有数据（严格错误处理）
        logger.info("预加载数据...")
        all_dates = []
        for start, end in train_periods:
            all_dates.extend([start, end])
        all_dates.extend(validate_period)
        min_date = min(all_dates)
        max_date = max(all_dates)
        cache_manager.preload_data(min_date, max_date)
        
        # 初始参数网格（精简版 - 减少组合数以加快测试）
        initial_param_grid = {
            # 持仓数量
            'max_stocks': [5, 10],
            
            # 动量参数
            'min_momentum_20d': [3.0, 8.0],
            'max_momentum_20d': [25.0, 35.0],
            
            # 相对位置
            'max_rel_position': [70.0, 85.0],
            
            # 止损止盈
            'stop_loss': [-0.06, -0.10],
        }
        
        total_combos = 1
        for v in initial_param_grid.values():
            total_combos *= len(v)
        
        logger.info(f"\n初始参数网格 ({total_combos}种组合):")
        for param, values in initial_param_grid.items():
            logger.info(f"  {param}: {values}")
        
        # 创建输出目录
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 执行递归优化（严格错误处理）
        best_params, all_history = recursive_grid_search(
            train_periods,
            validate_period,
            initial_param_grid,
            max_iterations=Config.MAX_RECURSIVE_ITERATIONS,
            refinement_ratio=Config.REFINEMENT_RATIO,
        )
        
        check_and_raise("优化未找到任何结果", best_params is not None)
        
        # 输出结果
        logger.info("\n" + "=" * 70)
        logger.info("🏆 最优参数")
        logger.info("=" * 70)
        for key, value in asdict(best_params).items():
            logger.info(f"  {key}: {value}")
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存最优参数
        params_path = Config.OUTPUT_DIR / f'best_params_{timestamp}.json'
        with open(params_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(best_params), f, ensure_ascii=False, indent=2)
        logger.info(f"\n✅ 最优参数已保存: {params_path}")
        
        # 保存优化历史
        if all_history:
            history_df = pd.DataFrame(all_history)
            history_df = history_df.sort_values('validate_score', ascending=False)
            history_path = Config.OUTPUT_DIR / f'optimization_history_{timestamp}.csv'
            history_df.to_csv(history_path, index=False, encoding='utf-8-sig')
            logger.info(f"✅ 优化历史已保存: {history_path}")
            
            # Top 5
            logger.info("\n📊 Top 5 参数组合:")
            top5_df = history_df.head(5)
            for idx, row in top5_df.iterrows():
                logger.info(f"  score={row['validate_score']:.4f}, "
                           f"年化={row['validate_annual_return']:.1f}%, "
                           f"夏普={row['validate_sharpe']:.2f}, "
                           f"回撤={row['validate_max_drawdown']:.1f}%, "
                           f"胜率={row['validate_win_rate']:.1f}%, "
                           f"过拟合比={row.get('overfit_ratio', 0):.2f}")
        
        # 使用最优参数进行最终验证（严格错误处理）
        logger.info("\n" + "-" * 70)
        logger.info("使用最优参数进行最终验证回测")
        
        final_result = run_bullettrade_backtest(
            best_params,
            validate_period[0],
            validate_period[1],
            task_id="final_validation"
        )
        
        logger.info(f"✅ 最终验证结果:")
        logger.info(f"   总收益: {final_result.total_return:.2f}%")
        logger.info(f"   年化收益: {final_result.annual_return:.2f}%")
        logger.info(f"   夏普比率: {final_result.sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {final_result.max_drawdown:.2f}%")
        logger.info(f"   胜率: {final_result.win_rate:.2f}%")
        logger.info(f"   总交易次数: {final_result.total_trades}")
        
    except FatalError as e:
        logger.error("\n" + "=" * 70)
        logger.error("❌ 致命错误：程序已停止")
        logger.error("=" * 70)
        logger.error(f"错误信息: {e}")
        logger.error("\n⚠️ 根据标准开发流程：")
        logger.error("   1. 遇到错误必须停止运行")
        logger.error("   2. 修复错误后重新运行")
        logger.error("   3. 不要忽略错误继续执行")
        sys.exit(1)
    except Exception as e:
        logger.error("\n" + "=" * 70)
        logger.error("❌ 未预期的异常：程序已停止")
        logger.error("=" * 70)
        logger.error(f"错误信息: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 总结
        total_time = time.time() - start_time
        logger.info("\n" + "=" * 70)
        logger.info(f"✅ 优化完成! 总用时: {total_time/60:.1f}分钟")
        logger.info("=" * 70)


if __name__ == '__main__':
    main()
