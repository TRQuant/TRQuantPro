#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场趋势分析模块参数优化脚本
==============================

使用遗传算法进行多目标参数优化，采用渐进式回测验证

核心功能:
1. 定义参数空间（指标权重、周期权重、因子分组权重等）
2. 渐进式回测：短周期(3个月) -> 中周期(6个月) -> 长周期(1年)
3. 多目标优化：IC、方向准确率、收益稳定性
4. 结果保存和分析

使用方法:
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python scripts/optimize_market_trend_params.py

版本: 1.0
日期: 2026-01-07
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
import logging
import argparse
import json
from collections import Counter
from dataclasses import dataclass, field, asdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============ 配置数据结构 ============

@dataclass
class BacktestPeriod:
    """回测周期配置"""
    name: str
    days: int
    weight: float  # 在最终评估中的权重
    min_signals: int  # 最少信号数


@dataclass 
class OptimizationConfig:
    """优化配置"""
    # 遗传算法参数
    population_size: int = 30
    generations: int = 50
    crossover_rate: float = 0.8
    mutation_rate: float = 0.15
    elite_ratio: float = 0.1
    early_stop_generations: int = 15
    
    # 回测配置
    sample_interval: int = 7  # 采样间隔天数（每周采样一次）
    forward_days: int = 5  # 评估未来N日收益
    
    # 渐进式回测周期
    periods: List[BacktestPeriod] = field(default_factory=lambda: [
        BacktestPeriod("short", 90, 0.25, 8),     # 3个月，权重25%
        BacktestPeriod("medium", 180, 0.35, 15),  # 6个月，权重35%
        BacktestPeriod("long", 300, 0.40, 25),    # 12个月，权重40%
    ])
    
    # 优化目标权重
    objective_weights: Dict[str, float] = field(default_factory=lambda: {
        "ic": 0.35,           # 信息系数
        "direction_acc": 0.25, # 方向准确率
        "week_ic": 0.15,      # 周线IC
        "return_corr": 0.15,  # 收益相关性
        "stability": 0.10,    # 稳定性
    })


# ============ 参数空间定义 ============

PARAMETER_SPACE = {
    # 模型权重
    "trend_weight": {"min": 0.5, "max": 0.95, "step": 0.05, "type": "float"},
    # "hmm_weight": 自动计算为 1 - trend_weight
    
    # 8维指标权重（需要归一化）
    "ma_weight": {"min": 0.10, "max": 0.35, "step": 0.02, "type": "float"},
    "macd_weight": {"min": 0.10, "max": 0.30, "step": 0.02, "type": "float"},
    "rsi_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    "bb_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    "vol_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    "kdj_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    "adx_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    "flow_weight": {"min": 0.05, "max": 0.20, "step": 0.02, "type": "float"},
    
    # 因子分组权重（用于smooth_grouped模式）
    "trend_group_weight": {"min": 0.30, "max": 0.60, "step": 0.05, "type": "float"},
    "oscillator_group_weight": {"min": 0.15, "max": 0.35, "step": 0.05, "type": "float"},
    "volatility_group_weight": {"min": 0.05, "max": 0.25, "step": 0.05, "type": "float"},
    # volume_group_weight 自动计算
    
    # 周期权重
    "week_period_weight": {"min": 0.20, "max": 0.50, "step": 0.05, "type": "float"},
    "month_period_weight": {"min": 0.25, "max": 0.45, "step": 0.05, "type": "float"},
    # quarter_period_weight 自动计算
    
    # 评分风格
    "scoring_style": {"choices": ["legacy", "smooth_grouped"], "type": "choice"},
}


# ============ JQData 初始化 ============

def init_jqdata() -> bool:
    """初始化JQData"""
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        
        if jq_config:
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            if jq.is_auth():
                logger.info("JQData认证成功")
                return True
        
        logger.warning("JQData认证失败")
        return False
    except Exception as e:
        logger.error(f"JQData初始化异常: {e}")
        return False


def get_trading_dates(start_date: str, end_date: str) -> List[str]:
    """获取交易日列表"""
    try:
        import jqdatasdk as jq
        dates = jq.get_trade_days(start_date=start_date, end_date=end_date)
        return [d.strftime("%Y-%m-%d") for d in dates]
    except Exception as e:
        logger.error(f"获取交易日失败: {e}")
        return []


def get_index_returns(index_code: str, dates: List[str]) -> pd.DataFrame:
    """获取指数收益率数据"""
    try:
        import jqdatasdk as jq
        
        if not dates:
            return pd.DataFrame()
        
        start_date = dates[0]
        end_date = dates[-1]
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=10)
        
        df = jq.get_price(
            index_code,
            start_date=start_dt.strftime("%Y-%m-%d"),
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            skip_paused=False,
            fq='pre',
        )
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.reset_index()
        df.columns = ['date', 'close']
        df['date'] = df['date'].dt.strftime("%Y-%m-%d")
        
        # 计算未来收益率
        df['fwd_ret_5d'] = df['close'].shift(-5) / df['close'] - 1
        df['fwd_ret_10d'] = df['close'].shift(-10) / df['close'] - 1
        
        return df
    except Exception as e:
        logger.error(f"获取指数数据失败: {e}")
        return pd.DataFrame()


# ============ 参数转换函数 ============

def params_to_config(params: Dict[str, Any]) -> Dict:
    """
    将优化参数转换为 MarketTrendAnalyzerConfig 格式
    
    自动归一化权重使总和为1
    """
    # 指标权重归一化
    indicator_keys = ["ma", "macd", "rsi", "bb", "vol", "kdj", "adx", "flow"]
    raw_indicator_weights = {k: params.get(f"{k}_weight", 0.125) for k in indicator_keys}
    total_ind = sum(raw_indicator_weights.values())
    indicator_weights = {k: v / total_ind for k, v in raw_indicator_weights.items()}
    
    # 因子分组权重归一化
    trend_g = params.get("trend_group_weight", 0.45)
    osc_g = params.get("oscillator_group_weight", 0.25)
    vol_g = params.get("volatility_group_weight", 0.15)
    volume_g = 1.0 - trend_g - osc_g - vol_g
    if volume_g < 0.05:
        volume_g = 0.05
        total_g = trend_g + osc_g + vol_g + volume_g
        trend_g /= total_g
        osc_g /= total_g
        vol_g /= total_g
        volume_g /= total_g
    
    factor_group_weights = {
        "trend": trend_g,
        "oscillator": osc_g,
        "volatility": vol_g,
        "volume": volume_g,
    }
    
    # 模型权重
    trend_weight = params.get("trend_weight", 0.8)
    hmm_weight = 1.0 - trend_weight
    
    return {
        "weights": {"trend": trend_weight, "hmm": hmm_weight},
        "indicator_weights": indicator_weights,
        "factor_group_weights": factor_group_weights,
        "scoring_style": params.get("scoring_style", "smooth_grouped"),
        "active_periods": ["week", "month", "quarter"],
    }


# ============ 回测评估函数 ============

_analyzer_cache = {}

def evaluate_params(
    params: Dict[str, Any],
    dates: List[str],
    returns_df: pd.DataFrame,
    sample_interval: int = 5,
    forward_days: int = 5,
    analyzer_cache_key: str = None,
) -> Dict[str, float]:
    """
    评估参数的适应度
    
    Args:
        params: 参数字典
        dates: 交易日列表
        returns_df: 收益率数据
        sample_interval: 采样间隔
        forward_days: 评估未来N日
        analyzer_cache_key: 缓存键（用于复用分析器）
        
    Returns:
        适应度字典 {metric: value}
    """
    global _analyzer_cache
    from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
    
    try:
        # 转换参数为配置
        config_dict = params_to_config(params)
        
        # 创建分析器（使用缓存避免重复初始化JQData和HMM）
        cache_key = str(sorted(config_dict.items()))
        if cache_key in _analyzer_cache:
            analyzer = _analyzer_cache[cache_key]
            # 更新配置
            analyzer.config.scoring_style = config_dict["scoring_style"]
            analyzer.config.weights = config_dict["weights"]
            analyzer.config.indicator_weights = config_dict["indicator_weights"]
            analyzer.config.factor_group_weights = config_dict["factor_group_weights"]
        else:
            config = MarketTrendAnalyzerConfig(
                scoring_style=config_dict["scoring_style"],
                weights=config_dict["weights"],
                indicator_weights=config_dict["indicator_weights"],
                factor_group_weights=config_dict["factor_group_weights"],
                active_periods=config_dict["active_periods"],
            )
            analyzer = MarketTrendAnalyzer(config)
            # 限制缓存大小
            if len(_analyzer_cache) > 10:
                _analyzer_cache.clear()
            _analyzer_cache[cache_key] = analyzer
        
        # 采样日期
        sample_dates = dates[::sample_interval]
        
        # 收集信号（使用单指数分析，更快）
        signals = []
        for date in sample_dates:
            try:
                signal = analyzer.analyze("000300.XSHG", as_of_date=date)
                if signal:
                    signals.append({
                        "date": date,
                        "score": signal.ensemble_score,
                        "position_cap": signal.workflow_params.position_target,
                        "week_score": signal.period_signals.get("week").score if "week" in signal.period_signals else 0,
                    })
            except:
                pass
        
        if len(signals) < 5:
            return {"ic": 0, "direction_acc": 0.5, "week_ic": 0, "return_corr": 0, "stability": 0.5}
        
        # 转为DataFrame并合并收益率
        signals_df = pd.DataFrame(signals)
        fwd_col = f"fwd_ret_{forward_days}d"
        if fwd_col not in returns_df.columns:
            fwd_col = "fwd_ret_5d"
        
        merged = signals_df.merge(returns_df[['date', fwd_col]], on='date', how='left')
        merged = merged.dropna(subset=[fwd_col])
        
        if len(merged) < 5:
            return {"ic": 0, "direction_acc": 0.5, "week_ic": 0, "return_corr": 0, "stability": 0.5}
        
        # 计算指标
        # 1. IC (信息系数)
        ic = merged['score'].corr(merged[fwd_col])
        if pd.isna(ic):
            ic = 0
        
        # 2. 方向准确率
        merged['pred_dir'] = merged['score'].apply(lambda x: 1 if x > 10 else (-1 if x < -10 else 0))
        merged['actual_dir'] = merged[fwd_col].apply(lambda x: 1 if x > 0.005 else (-1 if x < -0.005 else 0))
        directional = merged[merged['pred_dir'] != 0]
        if len(directional) > 0:
            direction_acc = (directional['pred_dir'] == directional['actual_dir']).mean()
        else:
            direction_acc = 0.5
        
        # 3. 周线IC
        week_ic = merged['week_score'].corr(merged[fwd_col])
        if pd.isna(week_ic):
            week_ic = 0
        
        # 4. 仓位-收益相关性
        return_corr = merged['position_cap'].corr(merged[fwd_col])
        if pd.isna(return_corr):
            return_corr = 0
        
        # 5. 稳定性 (滚动IC的稳定性)
        if len(merged) >= 10:
            rolling_ics = []
            window = max(5, len(merged) // 4)
            for i in range(0, len(merged) - window + 1, window // 2):
                sub = merged.iloc[i:i+window]
                if len(sub) >= 5:
                    sub_ic = sub['score'].corr(sub[fwd_col])
                    if not pd.isna(sub_ic):
                        rolling_ics.append(sub_ic)
            if rolling_ics:
                stability = 1 - np.std(rolling_ics)  # 标准差越小越稳定
            else:
                stability = 0.5
        else:
            stability = 0.5
        
        return {
            "ic": ic,
            "direction_acc": direction_acc,
            "week_ic": week_ic,
            "return_corr": return_corr,
            "stability": max(0, min(1, stability)),
        }
        
    except Exception as e:
        logger.warning(f"参数评估失败: {e}")
        return {"ic": 0, "direction_acc": 0.5, "week_ic": 0, "return_corr": 0, "stability": 0.5}


# ============ 遗传算法核心 ============

class MarketTrendOptimizer:
    """市场趋势分析参数优化器"""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.population: List[Dict] = []
        self.best_individual: Dict = None
        self.best_fitness: float = -float('inf')
        self.history: List[Dict] = []
        
        # 预加载数据
        self._dates_cache: Dict[str, List[str]] = {}
        self._returns_cache: Dict[str, pd.DataFrame] = {}
    
    def _sample_params(self) -> Dict[str, Any]:
        """随机采样参数"""
        params = {}
        for name, spec in PARAMETER_SPACE.items():
            if spec["type"] == "choice":
                params[name] = np.random.choice(spec["choices"])
            elif spec["type"] == "int":
                params[name] = np.random.randint(spec["min"], spec["max"] + 1)
            else:
                params[name] = np.random.uniform(spec["min"], spec["max"])
        return params
    
    def _mutate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """变异"""
        new_params = params.copy()
        for name, spec in PARAMETER_SPACE.items():
            if np.random.random() < self.config.mutation_rate:
                if spec["type"] == "choice":
                    new_params[name] = np.random.choice(spec["choices"])
                elif spec["type"] == "int":
                    delta = int((spec["max"] - spec["min"]) * 0.3)
                    new_val = new_params[name] + np.random.randint(-delta, delta + 1)
                    new_params[name] = max(spec["min"], min(spec["max"], new_val))
                else:
                    delta = (spec["max"] - spec["min"]) * 0.3
                    new_val = new_params[name] + np.random.uniform(-delta, delta)
                    new_params[name] = max(spec["min"], min(spec["max"], new_val))
        return new_params
    
    def _crossover(self, parent1: Dict, parent2: Dict) -> Tuple[Dict, Dict]:
        """交叉"""
        child1, child2 = parent1.copy(), parent2.copy()
        if np.random.random() < self.config.crossover_rate:
            keys = list(PARAMETER_SPACE.keys())
            crossover_point = np.random.randint(1, len(keys))
            for key in keys[crossover_point:]:
                child1[key], child2[key] = child2[key], child1[key]
        return child1, child2
    
    def _calculate_fitness(self, metrics: Dict[str, float]) -> float:
        """计算综合适应度"""
        weights = self.config.objective_weights
        fitness = 0.0
        for metric, weight in weights.items():
            value = metrics.get(metric, 0)
            fitness += weight * value
        return fitness
    
    def _evaluate_progressive(self, params: Dict[str, Any]) -> Tuple[float, Dict[str, Dict]]:
        """
        渐进式回测评估
        
        从短周期开始，如果短周期表现差则提前终止
        """
        period_results = {}
        total_fitness = 0.0
        
        for period in self.config.periods:
            # 获取数据
            if period.name not in self._dates_cache:
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=period.days)).strftime("%Y-%m-%d")
                self._dates_cache[period.name] = get_trading_dates(start_date, end_date)
                self._returns_cache[period.name] = get_index_returns("000300.XSHG", self._dates_cache[period.name])
            
            dates = self._dates_cache[period.name]
            returns_df = self._returns_cache[period.name]
            
            if len(dates) < period.min_signals:
                continue
            
            # 评估
            metrics = evaluate_params(
                params, dates, returns_df,
                sample_interval=self.config.sample_interval,
                forward_days=self.config.forward_days,
            )
            
            period_fitness = self._calculate_fitness(metrics)
            period_results[period.name] = {"metrics": metrics, "fitness": period_fitness}
            
            # 加权累计
            total_fitness += period.weight * period_fitness
            
            # 早停：仅在有有效评估且表现极差时才终止
            # period_fitness == -0.65 表示数据不足，不应早停
            if period.name == "short" and period_fitness < -0.1 and period_fitness > -0.5:
                logger.debug(f"短周期表现差({period_fitness:.3f})，提前终止")
                return -1.0, period_results
        
        return total_fitness, period_results
    
    def _select_parents(self, population_fitness: List[Tuple[Dict, float]]) -> List[Dict]:
        """轮盘赌选择"""
        # 归一化适应度
        fitnesses = [f for _, f in population_fitness]
        min_fit = min(fitnesses)
        adjusted = [f - min_fit + 0.1 for f in fitnesses]
        total = sum(adjusted)
        probs = [f / total for f in adjusted]
        
        # 选择
        selected = []
        for _ in range(len(population_fitness)):
            idx = np.random.choice(len(population_fitness), p=probs)
            selected.append(population_fitness[idx][0])
        return selected
    
    def optimize(self) -> Dict:
        """
        执行优化
        
        Returns:
            优化结果字典
        """
        logger.info(f"开始参数优化: 种群{self.config.population_size}, 代数{self.config.generations}")
        
        start_time = datetime.now()
        
        # 初始化种群
        self.population = [self._sample_params() for _ in range(self.config.population_size)]
        
        no_improve_count = 0
        
        for gen in range(self.config.generations):
            gen_start = datetime.now()
            
            # 评估种群
            population_fitness = []
            for i, params in enumerate(self.population):
                fitness, period_results = self._evaluate_progressive(params)
                population_fitness.append((params, fitness))
                
                # 更新最佳
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_individual = params.copy()
                    self.best_period_results = period_results
                    no_improve_count = 0
                    logger.info(f"  新最佳: fitness={fitness:.4f}")
            
            # 排序
            population_fitness.sort(key=lambda x: x[1], reverse=True)
            
            # 记录历史
            gen_best = population_fitness[0][1]
            gen_avg = np.mean([f for _, f in population_fitness])
            self.history.append({
                "generation": gen,
                "best_fitness": gen_best,
                "avg_fitness": gen_avg,
                "global_best": self.best_fitness,
            })
            
            gen_time = (datetime.now() - gen_start).total_seconds()
            logger.info(f"第{gen+1}代: best={gen_best:.4f}, avg={gen_avg:.4f}, global_best={self.best_fitness:.4f}, time={gen_time:.1f}s")
            
            # 早停检查
            no_improve_count += 1
            if no_improve_count >= self.config.early_stop_generations:
                logger.info(f"连续{no_improve_count}代无改进，早停")
                break
            
            # 精英保留
            elite_count = max(1, int(self.config.elite_ratio * self.config.population_size))
            elites = [p for p, _ in population_fitness[:elite_count]]
            
            # 选择
            parents = self._select_parents(population_fitness)
            
            # 交叉和变异
            next_population = elites.copy()
            while len(next_population) < self.config.population_size:
                p1, p2 = np.random.choice(len(parents), 2, replace=False)
                c1, c2 = self._crossover(parents[p1], parents[p2])
                c1 = self._mutate(c1)
                c2 = self._mutate(c2)
                next_population.extend([c1, c2])
            
            self.population = next_population[:self.config.population_size]
        
        runtime = (datetime.now() - start_time).total_seconds()
        
        return {
            "best_params": self.best_individual,
            "best_fitness": self.best_fitness,
            "best_period_results": getattr(self, 'best_period_results', {}),
            "generations_run": len(self.history),
            "runtime_seconds": runtime,
            "history": self.history,
        }


# ============ 结果分析和保存 ============

def print_optimization_result(result: Dict):
    """打印优化结果"""
    print("\n" + "=" * 70)
    print("市场趋势分析参数优化结果")
    print("=" * 70)
    
    print(f"\n【优化统计】")
    print(f"  运行代数: {result['generations_run']}")
    print(f"  运行时间: {result['runtime_seconds']:.1f}秒")
    print(f"  最佳适应度: {result['best_fitness']:.4f}")
    
    print(f"\n【最优参数】")
    best = result['best_params']
    
    print(f"  模型权重:")
    print(f"    trend_weight: {best.get('trend_weight', 0.8):.2f}")
    print(f"    hmm_weight: {1 - best.get('trend_weight', 0.8):.2f}")
    
    print(f"  评分风格: {best.get('scoring_style', 'smooth_grouped')}")
    
    print(f"  指标权重:")
    for ind in ["ma", "macd", "rsi", "bb", "vol", "kdj", "adx", "flow"]:
        print(f"    {ind}: {best.get(f'{ind}_weight', 0.125):.3f}")
    
    print(f"  因子分组权重:")
    print(f"    trend: {best.get('trend_group_weight', 0.45):.3f}")
    print(f"    oscillator: {best.get('oscillator_group_weight', 0.25):.3f}")
    print(f"    volatility: {best.get('volatility_group_weight', 0.15):.3f}")
    
    print(f"\n【各周期表现】")
    for period, data in result.get('best_period_results', {}).items():
        metrics = data.get('metrics', {})
        print(f"  {period}周期:")
        print(f"    IC: {metrics.get('ic', 0):.4f}")
        print(f"    方向准确率: {metrics.get('direction_acc', 0):.2%}")
        print(f"    周线IC: {metrics.get('week_ic', 0):.4f}")
        print(f"    仓位-收益相关: {metrics.get('return_corr', 0):.4f}")
        print(f"    稳定性: {metrics.get('stability', 0):.4f}")
        print(f"    综合适应度: {data.get('fitness', 0):.4f}")
    
    print("\n" + "=" * 70)


def save_result(result: Dict, output_dir: str):
    """保存优化结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存完整结果
    result_path = os.path.join(output_dir, f"optimization_result_{timestamp}.json")
    
    # 转换numpy类型
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(i) for i in obj]
        return obj
    
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(convert_numpy(result), f, indent=2, ensure_ascii=False)
    
    logger.info(f"结果已保存: {result_path}")
    
    # 保存最优配置为Python格式
    config_path = os.path.join(output_dir, f"optimized_config_{timestamp}.py")
    config_dict = params_to_config(result['best_params'])
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write('"""优化后的市场趋势分析配置"""\n\n')
        f.write(f'# 生成时间: {timestamp}\n')
        f.write(f'# 最佳适应度: {result["best_fitness"]:.4f}\n\n')
        f.write('OPTIMIZED_CONFIG = {\n')
        for key, value in config_dict.items():
            if isinstance(value, dict):
                f.write(f'    "{key}": {{\n')
                for k, v in value.items():
                    if isinstance(v, float):
                        f.write(f'        "{k}": {v:.4f},\n')
                    else:
                        f.write(f'        "{k}": {repr(v)},\n')
                f.write('    },\n')
            else:
                f.write(f'    "{key}": {repr(value)},\n')
        f.write('}\n')
    
    logger.info(f"配置已保存: {config_path}")
    
    return result_path, config_path


# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='市场趋势分析参数优化')
    parser.add_argument('--population', type=int, default=30, help='种群大小')
    parser.add_argument('--generations', type=int, default=50, help='迭代代数')
    parser.add_argument('--mutation', type=float, default=0.15, help='变异率')
    parser.add_argument('--early-stop', type=int, default=15, help='早停代数')
    parser.add_argument('--output', type=str, default='results/optimization', help='输出目录')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("市场趋势分析参数优化")
    print("=" * 70)
    print(f"\n配置:")
    print(f"  种群大小: {args.population}")
    print(f"  迭代代数: {args.generations}")
    print(f"  变异率: {args.mutation}")
    print(f"  早停代数: {args.early_stop}")
    
    # 初始化JQData
    if not init_jqdata():
        print("JQData初始化失败，退出")
        sys.exit(1)
    
    # 配置
    config = OptimizationConfig(
        population_size=args.population,
        generations=args.generations,
        mutation_rate=args.mutation,
        early_stop_generations=args.early_stop,
    )
    
    # 执行优化
    print("\n开始优化...")
    optimizer = MarketTrendOptimizer(config)
    result = optimizer.optimize()
    
    # 打印结果
    print_optimization_result(result)
    
    # 保存结果
    output_dir = os.path.join(project_root, args.output)
    result_path, config_path = save_result(result, output_dir)
    
    print(f"\n结果文件: {result_path}")
    print(f"配置文件: {config_path}")
    print("\n优化完成!")


if __name__ == "__main__":
    main()
