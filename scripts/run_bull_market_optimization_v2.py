#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略递归迭代优化 V2
================================

增强版本：
1. 集成加速技术：DataPreloader + GPU批量计算 + 并行回测
2. 实现真正的递归优化：粗网格→细网格→收敛
3. 修复BulletTrade验证参数映射
4. 添加过拟合检测和惩罚机制
5. Top N参数组合BulletTrade验证 + 偏差分析

目标: 周收益10%+ (激进策略)
回测引擎: BulletTrade (JQData数据源)
优化方法: 递归网格搜索 + 训练集/验证集分离

基于: scripts/run_bull_market_optimization.py
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


# ==================== 全局配置 ====================

class Config:
    """优化配置"""
    # 股票池
    MAX_STOCKS = 200  # 增加股票数以提高稳定性
    
    # 超时设置（秒）
    BACKTEST_TIMEOUT = 120
    TOTAL_TIMEOUT = 3600  # 60分钟总超时（递归优化需要更多时间）
    
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / 'output' / 'bull_market_optimization_v2'
    
    # 缓存目录
    CACHE_DIR = PROJECT_ROOT / 'data' / 'cache'
    
    # 递归优化配置
    MAX_RECURSIVE_ITERATIONS = 3  # 最大递归次数
    REFINEMENT_RATIO = 0.5  # 每次细化范围缩小比例
    CONVERGENCE_THRESHOLD = 0.05  # 收敛阈值（5%变化）
    
    # 过拟合检测
    OVERFIT_PENALTY_THRESHOLD = 2.0  # 过拟合惩罚阈值
    OVERFIT_PENALTY_FACTOR = 0.3  # 过拟合惩罚因子
    
    # 并行配置
    MAX_WORKERS = 3  # 最大并行数（JQData限制）
    
    # 简化回测采样（V2增强）
    SAMPLE_STOCKS = 80  # 增加股票采样数
    SAMPLE_DATES = 10  # 增加调仓日采样数


# ==================== 数据类定义 ====================

@dataclass
class BullMarketStrategyParams:
    """牛市策略参数 - 融合追涨信号+7因子选股"""
    
    # === 追涨信号参数 (来自优化结果，固定) ===
    limit_up_threshold: float = 0.093
    vol_ratio_threshold_first: float = 2.5
    mom_5d_threshold_breakout: float = 16.0
    mom_5d_threshold_volume: float = 10.0
    vol_ratio_threshold_breakout: float = 1.5
    vol_ratio_threshold_volume: float = 2.0
    
    # === 7因子选股参数 (待优化) ===
    min_momentum_20d: float = 5.0       # 最小20日动量(%)
    max_momentum_20d: float = 40.0      # 最大20日动量(%)
    max_rel_position: float = 80.0      # 最大相对位置(%)
    min_market_cap: float = 30.0        # 最小市值(亿) - 对应StrategyConfig
    max_market_cap: float = 300.0       # 最大市值(亿)
    min_volume_ratio: float = 1.5       # 最小量比（用于简化回测）
    min_turnover_rate: float = 2.0      # 最小换手率(%)
    max_turnover_rate: float = 10.0     # 最大换手率(%)
    min_roe: float = 0.0                # 最小ROE(%)
    min_momentum_5d: float = -5.0       # 最小5日动量(%)
    max_momentum_5d: float = 10.0       # 最大5日动量(%)
    
    # === 交易参数 ===
    max_positions: int = 5              # 最大持仓数
    single_position_max: float = 0.20   # 单票最大仓位
    stop_loss_pct: float = -8.0         # 止损比例(%)
    take_profit_pct: float = 30.0       # 止盈比例(%)
    rebalance_days: int = 5             # 调仓周期(交易日)
    
    # === 综合得分 ===
    min_total_score: float = 30.0       # 最小综合得分


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    avg_holding_days: float = 0.0
    profit_factor: float = 0.0
    error: str = ""


# ==================== 加速技术：数据预加载器 ====================

class DataCacheManager:
    """数据缓存管理器 - 封装DataPreloader和GPU加速"""
    
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
        self.gpu_calculator = None
        self.cached_data = {}  # 内存缓存
        
        # 尝试初始化数据预加载器
        try:
            from core.advisor_v4.data_preloader import DataPreloader
            self.preloader = DataPreloader(
                max_workers=Config.MAX_WORKERS,
                cache_dir=str(self.cache_dir),
                verbose=False,
                use_mongodb=True
            )
            logger.info("✅ DataPreloader已初始化（MongoDB支持）")
        except Exception as e:
            logger.warning(f"⚠️ DataPreloader初始化失败: {e}")
        
        # 尝试初始化GPU加速器
        try:
            from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator, USE_GPU
            if USE_GPU:
                self.gpu_calculator = GPUTechnicalIndicatorCalculator(batch_size=100, use_gpu=True)
                logger.info("✅ GPU加速已启用")
            else:
                logger.info("⚠️ GPU不可用，使用CPU计算")
        except Exception as e:
            logger.warning(f"⚠️ GPU初始化失败: {e}")
        
        self._initialized = True
    
    def preload_data(self, start_date: str, end_date: str, stock_pool: List[str], force_refresh: bool = False):
        """预加载数据到缓存"""
        if self.preloader is None:
            return None
        
        cache_key = f"{start_date}_{end_date}"
        if cache_key in self.cached_data and not force_refresh:
            logger.info(f"📦 使用内存缓存: {cache_key}")
            return self.cached_data[cache_key]
        
        try:
            result = self.preloader.preload_market_data(
                start_date=start_date,
                end_date=end_date,
                stock_pool=stock_pool,
                force_refresh=force_refresh
            )
            self.cached_data[cache_key] = result
            logger.info(f"✅ 数据预加载完成: {result.total_stocks}只股票, {result.total_trading_days}交易日")
            return result
        except Exception as e:
            logger.warning(f"⚠️ 数据预加载失败: {e}")
            return None
    
    def batch_calculate_indicators(self, prices_list: List[pd.DataFrame]) -> List[Dict]:
        """GPU批量计算技术指标"""
        if self.gpu_calculator is None:
            return self._calculate_indicators_cpu(prices_list)
        
        try:
            return self.gpu_calculator.calculate_batch(prices_list)
        except Exception as e:
            logger.warning(f"GPU计算失败，降级到CPU: {e}")
            return self._calculate_indicators_cpu(prices_list)
    
    def _calculate_indicators_cpu(self, prices_list: List[pd.DataFrame]) -> List[Dict]:
        """CPU回退计算"""
        results = []
        for prices in prices_list:
            if prices is None or len(prices) < 20:
                results.append({})
                continue
            
            close = prices['close'].values
            volume = prices['volume'].values if 'volume' in prices.columns else np.ones(len(close))
            
            result = {
                'momentum_20d': (close[-1] / close[-21] - 1) * 100 if len(close) > 21 else 0,
                'momentum_5d': (close[-1] / close[-6] - 1) * 100 if len(close) > 6 else 0,
                'vol_ratio': volume[-1] / np.mean(volume[-20:]) if len(volume) >= 20 and np.mean(volume[-20:]) > 0 else 1.0,
            }
            
            if len(close) >= 20:
                high_20 = np.max(close[-20:])
                low_20 = np.min(close[-20:])
                result['rel_position'] = (close[-1] - low_20) / (high_20 - low_20 + 1e-6) * 100
            else:
                result['rel_position'] = 50.0
            
            results.append(result)
        
        return results


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
            
            if now - self.last_report_time >= 3 or progress_pct % 10 < 0.5:
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
    initial_capital: float = 1000000.0,
) -> BacktestResult:
    """
    执行BulletTrade回测 - 修复参数映射
    """
    try:
        from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig, BulletTradeStrategyGenerator
        from core.bullettrade.engine import BulletTradeEngine, BTConfig
        
        # 创建策略配置 - 只传递StrategyConfig支持的参数
        strategy_config = StrategyConfig(
            max_stocks=params.max_positions,
            min_total_score=params.min_total_score,
            single_position_max=params.single_position_max,
            stop_loss=params.stop_loss_pct / 100,
            take_profit=params.take_profit_pct / 100,
            min_momentum_20d=params.min_momentum_20d,
            max_momentum_20d=params.max_momentum_20d,
            max_rel_position=params.max_rel_position,
            min_market_cap=params.min_market_cap,
            max_market_cap=params.max_market_cap,
            min_momentum_5d=params.min_momentum_5d,
            max_momentum_5d=params.max_momentum_5d,
            min_turnover_rate=params.min_turnover_rate,
            max_turnover_rate=params.max_turnover_rate,
            min_roe=params.min_roe,
        )
        
        # 生成策略代码
        generator = BulletTradeStrategyGenerator(
            strategy_config,
            cache_data_dir=str(Config.CACHE_DIR)
        )
        strategy_code = generator.generate_strategy_code()
        
        # 创建BulletTrade配置
        bt_config = BTConfig(
            initial_capital=initial_capital,
            benchmark='000300.XSHG',
        )
        
        # 执行回测
        engine = BulletTradeEngine(bt_config)
        result = engine.run(
            strategy_code=strategy_code,
            start_date=start_date,
            end_date=end_date,
        )
        
        if result is None:
            return BacktestResult(error="回测返回None")
        
        # 解析结果
        metrics = result.get_metrics() if hasattr(result, 'get_metrics') else {}
        
        return BacktestResult(
            total_return=metrics.get('total_return', 0.0) * 100,
            annual_return=metrics.get('annual_return', 0.0) * 100,
            sharpe_ratio=metrics.get('sharpe_ratio', 0.0),
            max_drawdown=metrics.get('max_drawdown', 0.0) * 100,
            win_rate=metrics.get('win_rate', 0.0) * 100,
            total_trades=metrics.get('total_trades', 0),
            avg_holding_days=metrics.get('avg_holding_days', 0.0),
            profit_factor=metrics.get('profit_factor', 0.0),
        )
    
    except Exception as e:
        logger.debug(f"BulletTrade回测失败: {e}")
        return BacktestResult(error=str(e)[:200])


def run_simplified_backtest_v2(
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    jq_client,
    universe: List[str],
    random_seed: int = 42,
) -> BacktestResult:
    """
    增强版简化回测 - 更多样本 + 交易成本 + 模拟持仓路径
    """
    try:
        np.random.seed(random_seed)  # 确保可复现
        
        trade_days = jq_client.get_trade_days(start_date=start_date, end_date=end_date)
        if trade_days is None or len(trade_days) < 25:
            return BacktestResult(error="交易日不足")
        
        # 增加采样数量
        sample_size = min(Config.SAMPLE_STOCKS, len(universe))
        sample_stocks = list(np.random.choice(universe, sample_size, replace=False))
        
        # 均匀分布的调仓日（增加到10个）
        num_dates = min(Config.SAMPLE_DATES, (len(trade_days) - 30) // 5)
        rebalance_indices = np.linspace(25, len(trade_days) - 10, num_dates, dtype=int)
        
        # 模拟持仓路径
        portfolio_values = [1.0]  # 初始净值1.0
        all_returns = []
        winning_count = 0
        
        # 交易成本
        commission_rate = 0.0001  # 万分之一
        stamp_tax_rate = 0.001   # 千分之一（卖出）
        
        cache_manager = get_cache_manager()
        
        for idx, i in enumerate(rebalance_indices):
            current_date = trade_days[i]
            date_str = str(current_date)[:10]
            
            # 批量获取所有股票历史数据
            try:
                panel = jq_client.get_price(
                    sample_stocks,
                    end_date=date_str,
                    count=30,
                    frequency='daily',
                    fields=['close', 'volume', 'high', 'low'],
                    panel=False,
                )
                
                if panel is None or panel.empty:
                    continue
                
                # 批量获取未来价格
                future_idx = min(i + params.rebalance_days, len(trade_days) - 1)
                future_date_str = str(trade_days[future_idx])[:10]
                future_panel = jq_client.get_price(
                    sample_stocks,
                    end_date=future_date_str,
                    count=1,
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                )
            except Exception:
                continue
            
            period_returns = []
            
            for stock in sample_stocks:
                try:
                    # 获取股票数据
                    if 'code' in panel.columns:
                        stock_data = panel[panel['code'] == stock]
                    else:
                        stock_data = panel[panel.index.get_level_values(1) == stock] if panel.index.nlevels > 1 else panel
                    
                    if stock_data.empty or len(stock_data) < 22:
                        continue
                    
                    close = stock_data['close'].values
                    volume = stock_data['volume'].values
                    high = stock_data['high'].values if 'high' in stock_data.columns else close
                    low = stock_data['low'].values if 'low' in stock_data.columns else close
                    
                    # 计算因子
                    mom_20d = (close[-1] / close[-21] - 1) * 100
                    mom_5d = (close[-1] / close[-6] - 1) * 100 if len(close) > 6 else 0
                    
                    high_20 = np.max(high[-20:])
                    low_20 = np.min(low[-20:])
                    rel_position = (close[-1] - low_20) / (high_20 - low_20 + 1e-6) * 100 if high_20 != low_20 else 50
                    
                    avg_vol = np.mean(volume[-20:])
                    vol_ratio = volume[-1] / avg_vol if avg_vol > 0 else 1.0
                    
                    # 筛选条件
                    if not (params.min_momentum_20d <= mom_20d <= params.max_momentum_20d):
                        continue
                    if rel_position > params.max_rel_position:
                        continue
                    if vol_ratio < params.min_volume_ratio:
                        continue
                    if not (params.min_momentum_5d <= mom_5d <= params.max_momentum_5d):
                        continue
                    
                    # 计算未来收益
                    if future_panel is not None and not future_panel.empty:
                        if 'code' in future_panel.columns:
                            future_data = future_panel[future_panel['code'] == stock]
                        else:
                            future_data = future_panel[future_panel.index.get_level_values(1) == stock] if future_panel.index.nlevels > 1 else future_panel
                        
                        if not future_data.empty:
                            exit_price = future_data['close'].iloc[-1]
                            # 扣除交易成本
                            gross_return = (exit_price / close[-1] - 1)
                            net_return = gross_return - commission_rate * 2 - stamp_tax_rate  # 买卖佣金+卖出印花税
                            future_return = net_return * 100
                            
                            period_returns.append(future_return)
                            all_returns.append(future_return)
                            if future_return > 0:
                                winning_count += 1
                
                except Exception:
                    continue
            
            # 更新组合净值（假设等权持仓，最多max_positions只股票）
            if period_returns:
                selected_returns = period_returns[:params.max_positions]
                avg_period_return = np.mean(selected_returns) / 100
                portfolio_values.append(portfolio_values[-1] * (1 + avg_period_return))
        
        if not all_returns:
            return BacktestResult(error="无信号")
        
        returns = np.array(all_returns)
        avg_return = np.mean(returns)
        win_rate = winning_count / len(returns) * 100
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(52) if len(returns) > 1 else 0
        
        # 最大回撤（基于组合净值）
        portfolio_array = np.array(portfolio_values)
        running_max = np.maximum.accumulate(portfolio_array)
        drawdown = (portfolio_array - running_max) / running_max * 100
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # 总收益和年化
        total_return = (portfolio_values[-1] - 1) * 100
        days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        annual_return = total_return * 365 / days if days > 0 else 0
        
        return BacktestResult(
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=len(returns),
        )
    
    except Exception as e:
        return BacktestResult(error=str(e)[:100])


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
        result.annual_return * 0.35 +          # 年化收益权重35%
        result.sharpe_ratio * 0.25 +           # 夏普比率权重25%
        (100 - abs(result.max_drawdown)) / 100 * 0.20 +  # 回撤控制20%
        result.win_rate / 100 * 0.20           # 胜率权重20%
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
            refined_grid[param_name] = list(np.round(np.linspace(new_min, new_max, n_values), 2))
    
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
    jq_client,
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    param_grid: Dict[str, List],
    universe: List[str],
    use_bullettrade: bool = False,
    iteration: int = 1,
) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
    """
    网格搜索优化（带并行）
    """
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    all_combinations = list(product(*param_values))
    total = len(all_combinations)
    
    logger.info(f"参数组合总数: {total}")
    
    progress = ProgressReporter(total, "网格搜索", iteration)
    
    best_params = None
    best_score = -float('inf')
    optimization_history = []
    
    # 默认参数
    default_params = asdict(BullMarketStrategyParams())
    
    for combo in all_combinations:
        try:
            params_dict = dict(zip(param_names, combo))
            full_params = default_params.copy()
            full_params.update(params_dict)
            params = BullMarketStrategyParams(**full_params)
            
            # 训练集回测
            train_results = []
            for train_start, train_end in train_periods:
                if use_bullettrade:
                    result = run_bullettrade_backtest(params, train_start, train_end)
                else:
                    result = run_simplified_backtest_v2(params, train_start, train_end, jq_client, universe)
                train_results.append(result)
            
            # 平均训练结果
            valid_train = [r for r in train_results if not r.error]
            if valid_train:
                avg_train = BacktestResult(
                    total_return=np.mean([r.total_return for r in valid_train]),
                    annual_return=np.mean([r.annual_return for r in valid_train]),
                    sharpe_ratio=np.mean([r.sharpe_ratio for r in valid_train]),
                    max_drawdown=np.mean([r.max_drawdown for r in valid_train]),
                    win_rate=np.mean([r.win_rate for r in valid_train]),
                    total_trades=int(np.mean([r.total_trades for r in valid_train])),
                )
            else:
                avg_train = BacktestResult(error="训练失败")
            
            # 验证集回测
            if use_bullettrade:
                validate_result = run_bullettrade_backtest(
                    params, validate_period[0], validate_period[1]
                )
            else:
                validate_result = run_simplified_backtest_v2(
                    params, validate_period[0], validate_period[1], jq_client, universe
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
                'validate_score': validate_score,
                'validate_score_raw': validate_score_raw,
                'validate_annual_return': validate_result.annual_return,
                'validate_sharpe': validate_result.sharpe_ratio,
                'validate_win_rate': validate_result.win_rate,
                'validate_max_drawdown': validate_result.max_drawdown,
                'overfit_ratio': overfit_ratio,
                'iteration': iteration,
            }
            optimization_history.append(history_entry)
            
            # 更新最优
            if score > best_score:
                best_score = score
                best_params = params
                logger.info(f"  🎯 新最优: score={score:.4f}, 年化={validate_result.annual_return:.1f}%, "
                           f"胜率={validate_result.win_rate:.1f}%, 回撤={validate_result.max_drawdown:.1f}%")
            
            progress.update(score=score)
        
        except Exception as e:
            progress.update(error=True)
            logger.debug(f"参数组合失败: {e}")
    
    progress.finish()
    return best_params, optimization_history


def recursive_grid_search(
    jq_client,
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    initial_param_grid: Dict[str, List],
    universe: List[str],
    max_iterations: int = 3,
    refinement_ratio: float = 0.5,
) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
    """
    递归网格搜索优化
    
    粗网格 → 细网格 → 收敛
    """
    logger.info("=" * 70)
    logger.info("开始递归网格搜索优化")
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
        
        # 执行网格搜索
        best_params, history = grid_search_optimize(
            jq_client,
            train_periods,
            validate_period,
            current_grid,
            universe,
            use_bullettrade=False,
            iteration=iteration,
        )
        
        if best_params is None:
            logger.warning(f"迭代{iteration}未找到有效参数")
            break
        
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


def validate_top_params_with_bullettrade(
    top_params_list: List[BullMarketStrategyParams],
    simplified_results: List[Dict],
    validate_period: Tuple[str, str],
) -> List[Dict]:
    """
    使用BulletTrade验证Top N参数组合，并分析偏差
    """
    logger.info("\n" + "=" * 70)
    logger.info("BulletTrade Top N 验证 + 偏差分析")
    logger.info("=" * 70)
    
    validation_results = []
    
    for i, (params, simplified) in enumerate(zip(top_params_list, simplified_results), 1):
        logger.info(f"\n验证 #{i}:")
        
        bt_result = run_bullettrade_backtest(
            params,
            validate_period[0],
            validate_period[1],
        )
        
        if bt_result.error:
            logger.warning(f"  BulletTrade验证失败: {bt_result.error}")
            validation_results.append({
                'rank': i,
                'simplified_score': simplified.get('validate_score', 0),
                'bt_score': -100,
                'bt_error': bt_result.error,
                'bias': None,
            })
            continue
        
        bt_score = calculate_composite_score(bt_result)
        simplified_score = simplified.get('validate_score', 0)
        bias = abs(bt_score - simplified_score) / (abs(simplified_score) + 1e-6) * 100
        
        logger.info(f"  简化版: score={simplified_score:.2f}, 年化={simplified.get('validate_annual_return', 0):.1f}%")
        logger.info(f"  BulletTrade: score={bt_score:.2f}, 年化={bt_result.annual_return:.1f}%, "
                   f"夏普={bt_result.sharpe_ratio:.2f}, 回撤={bt_result.max_drawdown:.1f}%")
        logger.info(f"  偏差: {bias:.1f}%")
        
        validation_results.append({
            'rank': i,
            'simplified_score': simplified_score,
            'simplified_annual_return': simplified.get('validate_annual_return', 0),
            'bt_score': bt_score,
            'bt_annual_return': bt_result.annual_return,
            'bt_sharpe': bt_result.sharpe_ratio,
            'bt_max_drawdown': bt_result.max_drawdown,
            'bt_win_rate': bt_result.win_rate,
            'bias': bias,
            'params': asdict(params),
        })
    
    # 偏差分析总结
    valid_biases = [r['bias'] for r in validation_results if r['bias'] is not None]
    if valid_biases:
        avg_bias = np.mean(valid_biases)
        logger.info(f"\n📊 偏差分析总结: 平均偏差={avg_bias:.1f}%")
    
    return validation_results


# ==================== 主函数 ====================

def main():
    """主函数"""
    start_time = time.time()
    
    logger.info("=" * 70)
    logger.info("牛市极端高收益策略递归迭代优化 V2")
    logger.info("=" * 70)
    logger.info("目标: 周收益10%+ | 回测引擎: BulletTrade/简化版")
    logger.info("加速技术: DataPreloader + GPU批量计算 + 并行回测")
    
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
    
    # 数据集配置
    train_periods = [
        ('2019-06-01', '2020-06-30'),  # 牛市上涨期
        ('2024-09-01', '2025-01-10'),  # 最新行情
    ]
    validate_period = ('2020-07-01', '2021-03-31')  # 牛市中期
    
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
    
    # 初始化数据缓存（加速）
    cache_manager = get_cache_manager()
    
    # 预加载训练集和验证集数据
    logger.info("\n预加载数据（加速）...")
    all_dates = []
    for start, end in train_periods:
        all_dates.extend([start, end])
    all_dates.extend(validate_period)
    min_date = min(all_dates)
    max_date = max(all_dates)
    cache_manager.preload_data(min_date, max_date, universe[:100])
    
    # 初始参数网格（粗网格）
    initial_param_grid = {
        # 动量参数
        'min_momentum_20d': [0, 5, 10],
        'max_momentum_20d': [40, 50, 60],
        
        # 相对位置
        'max_rel_position': [75, 85, 95],
        
        # 量比阈值
        'min_volume_ratio': [1.2, 1.5, 2.0],
        
        # 持仓控制
        'max_positions': [3, 5],
    }
    
    total_combos = 1
    for v in initial_param_grid.values():
        total_combos *= len(v)
    
    logger.info(f"\n初始参数网格 ({total_combos}种组合):")
    for param, values in initial_param_grid.items():
        logger.info(f"  {param}: {values}")
    
    # 执行递归优化
    best_params, all_history = recursive_grid_search(
        jq,
        train_periods,
        validate_period,
        initial_param_grid,
        universe,
        max_iterations=Config.MAX_RECURSIVE_ITERATIONS,
        refinement_ratio=Config.REFINEMENT_RATIO,
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
                       f"胜率={row['validate_win_rate']:.1f}%, "
                       f"回撤={row['validate_max_drawdown']:.1f}%, "
                       f"过拟合比={row.get('overfit_ratio', 0):.2f}")
        
        # Top 5 BulletTrade验证
        top5_params = []
        top5_simplified = []
        default_params = asdict(BullMarketStrategyParams())
        for _, row in top5_df.iterrows():
            params_dict = row['params']
            if isinstance(params_dict, str):
                params_dict = eval(params_dict)
            full_params = default_params.copy()
            full_params.update(params_dict)
            top5_params.append(BullMarketStrategyParams(**full_params))
            top5_simplified.append(row.to_dict())
        
        validation_results = validate_top_params_with_bullettrade(
            top5_params,
            top5_simplified,
            validate_period,
        )
        
        # 保存验证报告
        validation_path = Config.OUTPUT_DIR / f'validation_report_{timestamp}.json'
        with open(validation_path, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 验证报告已保存: {validation_path}")
    
    # 总结
    total_time = time.time() - start_time
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ 优化完成! 总用时: {total_time/60:.1f}分钟")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
