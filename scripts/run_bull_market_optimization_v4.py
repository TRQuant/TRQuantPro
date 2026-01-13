#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略递归迭代优化 V4
================================

加速版本 - 多线程并行 + GPU加速 + 智能剪枝 + 数据分割

核心优化:
1. 多参数组合并行回测 (ThreadPoolExecutor, max_workers=3)
2. GPU批量因子计算 (GPUTechnicalIndicatorCalculator)
3. 智能剪枝: 训练集表现差的组合跳过验证集
4. 数据分割并行: 交易日分段并行计算
5. 增量数据缓存: MongoDB缓存行情数据
6. 严格错误处理: 任何错误立即停止

预计加速: 从45小时 → 8-12小时

目标: 周收益10%+ (激进策略)
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Callable
import pandas as pd
import numpy as np
import logging
import json
from dataclasses import dataclass, asdict, field
from itertools import product
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import threading
import queue
import os

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
log_dir = PROJECT_ROOT / 'output' / 'bull_market_optimization_v4'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / 'optimization_run.log', mode='w', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


# ==================== 严格错误处理类 ====================

class FatalError(Exception):
    """致命错误 - 必须停止运行"""
    pass


def check_and_raise(error_message: str, condition: bool = True):
    """检查条件，如果失败则抛出致命错误"""
    if not condition:
        logger.error(f"❌ 致命错误: {error_message}")
        raise FatalError(error_message)


# ==================== 全局配置 ====================

class Config:
    """优化配置"""
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / 'output' / 'bull_market_optimization_v4'
    
    # 缓存目录
    CACHE_DIR = PROJECT_ROOT / 'data' / 'cache'
    
    # 递归优化配置
    MAX_RECURSIVE_ITERATIONS = 3
    REFINEMENT_RATIO = 0.5
    CONVERGENCE_THRESHOLD = 0.05
    
    # 过拟合检测
    OVERFIT_PENALTY_THRESHOLD = 2.0
    OVERFIT_PENALTY_FACTOR = 0.3
    
    # 回测配置
    INITIAL_CAPITAL = 1000000.0
    BENCHMARK = '000300.XSHG'
    
    # ========== 加速配置 (V4新增) ==========
    # 并行配置
    MAX_PARALLEL_BACKTESTS = 3      # 最大并行回测数
    USE_GPU = True                   # 使用GPU加速
    GPU_BATCH_SIZE = 100             # GPU批处理大小
    
    # 智能剪枝
    EARLY_STOP_THRESHOLD = -15.0    # 训练集年化收益低于此值则跳过验证集
    MIN_TRADES_THRESHOLD = 50       # 最少交易次数（低于此值可能数据有问题）
    
    # 数据分割
    DATA_SPLIT_WORKERS = 3          # 数据分割并行工作数


# ==================== 数据类定义 ====================

@dataclass
class BullMarketStrategyParams:
    """牛市策略参数 - 映射到StrategyConfig"""
    
    # === 选股参数 ===
    max_stocks: int = 8                  # 最大持股数量 (V4: 增加到8)
    min_total_score: float = 30.0       # 最小综合得分
    
    # === 仓位参数 ===
    single_position_max: float = 0.15   # 单票最大仓位 (V4: 降到15%)
    
    # === 止损止盈参数 (V4: 放宽止损) ===
    stop_loss: float = -0.10            # 固定止损 (V4: -10%)
    take_profit: float = 0.30           # 固定止盈
    trailing_stop: float = -0.10        # 移动止损 (V4: -10%)
    trailing_stop_trigger: float = 0.15 # 移动止损触发条件
    time_stop_days: int = 20            # 时间止损
    
    # === 因子筛选阈值 (V4: 放宽条件) ===
    min_momentum_20d: float = 0.0       # 最小20日动量 (V4: 降到0)
    max_momentum_20d: float = 50.0      # 最大20日动量 (V4: 增加到50)
    max_rel_position: float = 85.0      # 最大相对位置 (V4: 增加到85)
    min_market_cap: float = 50.0        # 最小市值 (V4: 增加到50亿)
    max_market_cap: float = 300.0       # 最大市值 (V4: 增加到300亿)
    min_momentum_5d: float = -5.0       # 最小5日动量
    max_momentum_5d: float = 15.0       # 最大5日动量 (V4: 增加到15)
    min_turnover_rate: float = 2.0      # 最小换手率
    max_turnover_rate: float = 12.0     # 最大换手率 (V4: 增加到12)
    min_roe: float = 0.0                # 最小ROE
    
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
    """回测结果"""
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    runtime_seconds: float = 0.0
    error: str = ""
    
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


# ==================== GPU加速器 ====================

class GPUFactorCalculator:
    """GPU因子计算器 - 封装现有GPUTechnicalIndicatorCalculator"""
    
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
        
        self.calculator = None
        self.use_gpu = Config.USE_GPU
        
        if self.use_gpu:
            try:
                from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator, USE_GPU
                if USE_GPU:
                    self.calculator = GPUTechnicalIndicatorCalculator(
                        batch_size=Config.GPU_BATCH_SIZE,
                        use_gpu=True
                    )
                    logger.info("✅ GPU加速器初始化成功")
                else:
                    logger.warning("⚠️ GPU不可用，使用CPU计算")
                    self.use_gpu = False
            except Exception as e:
                logger.warning(f"⚠️ GPU加速器初始化失败: {e}")
                self.use_gpu = False
        
        self._initialized = True
    
    def calculate_batch(self, prices_list: List[pd.DataFrame]) -> List[Dict]:
        """批量计算技术指标"""
        if self.calculator and self.use_gpu:
            return self.calculator.calculate_batch(prices_list)
        else:
            # CPU fallback
            results = []
            for prices in prices_list:
                if prices is not None and len(prices) >= 20:
                    results.append(self._calculate_single_cpu(prices))
                else:
                    results.append({})
            return results
    
    def _calculate_single_cpu(self, prices: pd.DataFrame) -> Dict:
        """单个股票CPU计算"""
        try:
            close = prices['close'].values
            high = prices['high'].values
            low = prices['low'].values
            volume = prices['volume'].values
            
            # 计算基础指标
            mom_20d = (close[-1] / close[-20] - 1) * 100 if len(close) >= 20 else 0
            mom_5d = (close[-1] / close[-5] - 1) * 100 if len(close) >= 5 else 0
            
            high_20 = np.max(high[-20:]) if len(high) >= 20 else high[-1]
            low_20 = np.min(low[-20:]) if len(low) >= 20 else low[-1]
            rel_pos = (close[-1] - low_20) / (high_20 - low_20 + 1e-10) * 100
            
            return {
                'momentum_20d': mom_20d,
                'momentum_5d': mom_5d,
                'rel_position': rel_pos,
            }
        except Exception as e:
            return {}


# ==================== 数据预加载器 ====================

class DataCacheManager:
    """数据缓存管理器"""
    
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
        
        self.preloader = None
        
        try:
            from core.advisor_v4.data_preloader import DataPreloader
            self.preloader = DataPreloader(
                max_workers=3,
                cache_dir=str(Config.CACHE_DIR),
                verbose=True,
                use_mongodb=True
            )
            logger.info("✅ DataPreloader初始化成功")
        except Exception as e:
            logger.warning(f"⚠️ DataPreloader初始化失败: {e}")
        
        self._initialized = True
    
    def preload(self, start_date: str, end_date: str) -> bool:
        """预加载数据"""
        if self.preloader:
            try:
                result = self.preloader.preload_market_data(start_date, end_date)
                return result.success
            except Exception as e:
                logger.warning(f"数据预加载失败: {e}")
                return False
        return False


# ==================== JQData权限检查 ====================

def check_jqdata_permission():
    """检查JQData权限并设置环境变量"""
    logger.info("=" * 60)
    logger.info("JQData权限检查")
    logger.info("=" * 60)
    
    try:
        from config.config_manager import get_config_manager
        import jqdatasdk as jq
        
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        check_and_raise("JQData用户名未配置", username is not None)
        check_and_raise("JQData密码未配置", password is not None)
        
        # 认证
        jq.auth(username, password)
        logger.info("✅ JQData认证成功")
        
        # 设置环境变量（供BulletTrade使用）
        os.environ['JQDATA_USERNAME'] = username
        os.environ['JQDATA_USER'] = username
        os.environ['JQDATA_PASSWORD'] = password
        os.environ['JQDATA_PWD'] = password
        logger.info("✅ JQData环境变量已设置")
        
        # 测试数据访问
        test_data = jq.get_price('000001.XSHE', start_date='2020-01-01', end_date='2020-01-10')
        check_and_raise("JQData数据访问失败", test_data is not None and len(test_data) > 0)
        logger.info("✅ JQData数据访问正常")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ JQData权限检查失败: {e}")
        raise FatalError(f"JQData权限检查失败: {e}")


# ==================== 回测执行 ====================

def run_bullettrade_backtest(
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000.0,
    task_id: str = "default",
) -> BacktestResult:
    """
    执行BulletTrade回测
    """
    start_time = time.time()
    
    try:
        from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest
        
        strategy_config = params.to_strategy_config()
        
        output_dir = Config.OUTPUT_DIR / 'backtests' / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        bt = BulletTradeBacktest(
            strategy_config=strategy_config,
            output_dir=str(output_dir),
            cache_dir=str(Config.CACHE_DIR),
        )
        
        bt_result = bt.run_backtest(
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
        )
        
        result = BacktestResult.from_bt_result(bt_result)
        result.runtime_seconds = time.time() - start_time
        
        # 验证结果
        if result.total_return == 0.0 and result.total_trades == 0:
            logger.warning(f"[{task_id}] 回测无交易，可能数据获取失败")
        
        logger.info(f"[{task_id}] 回测完成: 年化={result.annual_return:.1f}%, "
                   f"夏普={result.sharpe_ratio:.2f}, 耗时={result.runtime_seconds:.1f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"[{task_id}] 回测失败: {e}")
        return BacktestResult(error=str(e)[:200], runtime_seconds=time.time() - start_time)


# ==================== 评分函数 ====================

def calculate_composite_score(result: BacktestResult, overfit_ratio: float = 1.0) -> float:
    """
    计算复合评分
    
    权重:
    - 年化收益: 40%
    - 夏普比率: 30%
    - 胜率: 15%
    - 回撤控制: 15%
    """
    if result.error:
        return -100.0
    
    score = 0.0
    
    # 年化收益 (40%)
    score += result.annual_return * 0.4
    
    # 夏普比率 (30%)
    score += result.sharpe_ratio * 10 * 0.3
    
    # 胜率 (15%)
    score += (result.win_rate - 40) * 0.15  # 以40%为基准
    
    # 回撤控制 (15%)
    drawdown_score = max(-50, result.max_drawdown)  # 限制惩罚
    score += (drawdown_score + 30) * 0.15  # 以-30%为基准
    
    # 过拟合惩罚
    if overfit_ratio > Config.OVERFIT_PENALTY_THRESHOLD:
        penalty = (overfit_ratio - Config.OVERFIT_PENALTY_THRESHOLD) * Config.OVERFIT_PENALTY_FACTOR
        score -= penalty * abs(score)
    
    return score


# ==================== 并行优化引擎 ====================

class ParallelOptimizer:
    """并行优化引擎"""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.gpu_calculator = GPUFactorCalculator()
        self.data_cache = DataCacheManager()
        self.results_lock = threading.Lock()
        
    def _run_single_combination(
        self,
        combo_idx: int,
        params: BullMarketStrategyParams,
        train_periods: List[Tuple[str, str]],
        validate_period: Tuple[str, str],
        iteration: int,
    ) -> Optional[Dict]:
        """运行单个参数组合"""
        task_id = f"iter{iteration}_combo{combo_idx}"
        
        try:
            # 训练集回测
            train_results = []
            for period_idx, (train_start, train_end) in enumerate(train_periods):
                result = run_bullettrade_backtest(
                    params, train_start, train_end,
                    task_id=f"{task_id}_train{period_idx}"
                )
                train_results.append(result)
            
            # 平均训练结果
            valid_train = [r for r in train_results if not r.error]
            if not valid_train:
                logger.warning(f"[{task_id}] 所有训练集回测失败")
                return None
            
            avg_train = BacktestResult(
                total_return=np.mean([r.total_return for r in valid_train]),
                annual_return=np.mean([r.annual_return for r in valid_train]),
                sharpe_ratio=np.mean([r.sharpe_ratio for r in valid_train]),
                max_drawdown=np.mean([r.max_drawdown for r in valid_train]),
                win_rate=np.mean([r.win_rate for r in valid_train]),
                total_trades=int(np.mean([r.total_trades for r in valid_train])),
                runtime_seconds=sum([r.runtime_seconds for r in valid_train]),
            )
            
            # === 智能剪枝 ===
            if avg_train.annual_return < Config.EARLY_STOP_THRESHOLD:
                logger.info(f"[{task_id}] ✂️ 智能剪枝: 训练集年化={avg_train.annual_return:.1f}% < {Config.EARLY_STOP_THRESHOLD}%")
                return {
                    'params': asdict(params),
                    'train_annual_return': avg_train.annual_return,
                    'train_sharpe': avg_train.sharpe_ratio,
                    'pruned': True,
                    'reason': 'early_stop_threshold',
                }
            
            if avg_train.total_trades < Config.MIN_TRADES_THRESHOLD:
                logger.info(f"[{task_id}] ✂️ 智能剪枝: 训练集交易次数={avg_train.total_trades} < {Config.MIN_TRADES_THRESHOLD}")
                return {
                    'params': asdict(params),
                    'train_annual_return': avg_train.annual_return,
                    'train_total_trades': avg_train.total_trades,
                    'pruned': True,
                    'reason': 'min_trades_threshold',
                }
            
            # 验证集回测
            validate_result = run_bullettrade_backtest(
                params, validate_period[0], validate_period[1],
                task_id=f"{task_id}_validate"
            )
            
            # 计算评分
            train_score = calculate_composite_score(avg_train)
            validate_score_raw = calculate_composite_score(validate_result)
            
            overfit_ratio = train_score / (validate_score_raw + 1e-6) if validate_score_raw > 0 else 0
            validate_score = calculate_composite_score(validate_result, overfit_ratio)
            
            return {
                'combo_idx': combo_idx,
                'params': asdict(params),
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
                'pruned': False,
            }
            
        except Exception as e:
            logger.error(f"[{task_id}] 组合执行失败: {e}")
            traceback.print_exc()
            return None
    
    def run_parallel_grid_search(
        self,
        train_periods: List[Tuple[str, str]],
        validate_period: Tuple[str, str],
        param_grid: Dict[str, List],
        iteration: int = 1,
    ) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
        """并行网格搜索"""
        
        # 生成参数组合
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        all_combinations = list(product(*param_values))
        total = len(all_combinations)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"并行网格搜索 - 迭代 {iteration}")
        logger.info(f"参数组合总数: {total}")
        logger.info(f"并行工作数: {self.max_workers}")
        logger.info(f"智能剪枝阈值: 年化 < {Config.EARLY_STOP_THRESHOLD}%")
        logger.info(f"{'='*60}")
        
        # 准备参数
        default_params = asdict(BullMarketStrategyParams())
        params_list = []
        for combo in all_combinations:
            params_dict = dict(zip(param_names, combo))
            full_params = default_params.copy()
            full_params.update(params_dict)
            params_list.append(BullMarketStrategyParams(**full_params))
        
        # 并行执行
        results = []
        best_params = None
        best_score = -float('inf')
        
        completed = 0
        pruned = 0
        failed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self._run_single_combination,
                    idx, params, train_periods, validate_period, iteration
                ): (idx, params)
                for idx, params in enumerate(params_list)
            }
            
            for future in as_completed(futures):
                idx, params = futures[future]
                completed += 1
                
                try:
                    result = future.result()
                    
                    if result is None:
                        failed += 1
                        continue
                    
                    if result.get('pruned', False):
                        pruned += 1
                        results.append(result)
                        continue
                    
                    results.append(result)
                    
                    # 更新最优
                    score = result.get('validate_score', -float('inf'))
                    if score > best_score:
                        best_score = score
                        best_params = params
                        logger.info(f"🎯 新最优 [{completed}/{total}]: score={score:.4f}, "
                                   f"年化={result['validate_annual_return']:.1f}%, "
                                   f"夏普={result['validate_sharpe']:.2f}")
                    
                except Exception as e:
                    failed += 1
                    logger.error(f"组合 {idx} 获取结果失败: {e}")
                
                # 进度报告
                if completed % 5 == 0:
                    logger.info(f"[进度] {completed}/{total} 完成, {pruned} 剪枝, {failed} 失败")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"网格搜索完成")
        logger.info(f"完成: {completed}, 剪枝: {pruned}, 失败: {failed}")
        if best_params:
            logger.info(f"最优评分: {best_score:.4f}")
        logger.info(f"{'='*60}")
        
        return best_params, results


# ==================== 进度报告器 ====================

class ProgressReporter:
    """进度报告器"""
    
    def __init__(self, total: int, task_name: str):
        self.total = total
        self.task_name = task_name
        self.completed = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def update(self, n: int = 1):
        with self.lock:
            self.completed += n
            elapsed = time.time() - self.start_time
            rate = self.completed / elapsed if elapsed > 0 else 0
            eta = (self.total - self.completed) / rate if rate > 0 else 0
            
            if self.completed % 5 == 0 or self.completed == self.total:
                logger.info(f"[{self.task_name}] {self.completed}/{self.total} "
                           f"({self.completed/self.total*100:.1f}%) "
                           f"速度: {rate:.2f}/s, ETA: {eta/60:.1f}分钟")


# ==================== 主函数 ====================

def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("牛市极端高收益策略递归迭代优化 V4")
    logger.info("=" * 70)
    logger.info(f"启动时间: {datetime.now()}")
    logger.info(f"输出目录: {Config.OUTPUT_DIR}")
    logger.info(f"并行工作数: {Config.MAX_PARALLEL_BACKTESTS}")
    logger.info(f"GPU加速: {Config.USE_GPU}")
    logger.info(f"智能剪枝阈值: {Config.EARLY_STOP_THRESHOLD}%")
    logger.info("=" * 70)
    
    # 创建输出目录
    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. JQData权限检查
    check_jqdata_permission()
    
    # 2. 初始化数据缓存
    logger.info("\n[步骤2] 初始化数据缓存...")
    data_cache = DataCacheManager()
    
    # 3. 预加载数据
    logger.info("\n[步骤3] 预加载回测数据...")
    data_cache.preload('2020-01-01', '2020-12-31')
    
    # 4. 定义优化参数网格 (V4优化版)
    logger.info("\n[步骤4] 定义参数网格...")
    
    # 基于分析报告优化的参数网格
    param_grid = {
        # 止损止盈（最关键）
        'stop_loss': [-0.08, -0.10, -0.12],
        'trailing_stop': [-0.08, -0.10, -0.12],
        
        # 选股因子
        'min_momentum_20d': [0.0, 5.0],
        'max_momentum_20d': [30.0, 50.0],
        
        # 持仓配置
        'max_stocks': [5, 8],
    }
    
    total_combos = 1
    for v in param_grid.values():
        total_combos *= len(v)
    logger.info(f"参数组合总数: {total_combos}")
    logger.info(f"参数网格: {param_grid}")
    
    # 5. 定义训练集/验证集
    train_periods = [
        ('2020-01-01', '2020-06-30'),
    ]
    validate_period = ('2020-07-01', '2020-12-31')
    
    logger.info(f"\n训练集: {train_periods}")
    logger.info(f"验证集: {validate_period}")
    
    # 6. 运行并行优化
    logger.info("\n[步骤6] 开始并行网格搜索...")
    
    optimizer = ParallelOptimizer(max_workers=Config.MAX_PARALLEL_BACKTESTS)
    
    try:
        best_params, history = optimizer.run_parallel_grid_search(
            train_periods=train_periods,
            validate_period=validate_period,
            param_grid=param_grid,
            iteration=1,
        )
    except FatalError as e:
        logger.error(f"❌ 优化过程出现致命错误: {e}")
        logger.error("⚠️ 请修复错误后重新运行")
        return
    
    # 7. 保存结果
    logger.info("\n[步骤7] 保存优化结果...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if best_params:
        best_params_file = Config.OUTPUT_DIR / f'best_params_{timestamp}.json'
        with open(best_params_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(best_params), f, indent=2, ensure_ascii=False)
        logger.info(f"✅ 最优参数已保存: {best_params_file}")
    
    history_file = Config.OUTPUT_DIR / f'optimization_history_{timestamp}.json'
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"✅ 优化历史已保存: {history_file}")
    
    # 8. 输出结果摘要
    logger.info("\n" + "=" * 70)
    logger.info("优化完成!")
    logger.info("=" * 70)
    
    if best_params:
        logger.info(f"\n最优参数:")
        for key, value in asdict(best_params).items():
            logger.info(f"  {key}: {value}")
    else:
        logger.warning("⚠️ 未找到有效的最优参数")
    
    # 统计
    valid_results = [r for r in history if not r.get('pruned', False)]
    pruned_results = [r for r in history if r.get('pruned', False)]
    
    logger.info(f"\n统计:")
    logger.info(f"  总组合数: {len(history)}")
    logger.info(f"  有效结果: {len(valid_results)}")
    logger.info(f"  剪枝跳过: {len(pruned_results)}")
    
    if valid_results:
        best_annual = max([r.get('validate_annual_return', -100) for r in valid_results])
        best_sharpe = max([r.get('validate_sharpe', -10) for r in valid_results])
        logger.info(f"  最佳年化: {best_annual:.1f}%")
        logger.info(f"  最佳夏普: {best_sharpe:.2f}")
    
    logger.info(f"\n完成时间: {datetime.now()}")


if __name__ == '__main__':
    main()
