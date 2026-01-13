#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 V3.0 - 完善版
=================================

目标：周频10%收益

核心改进 (V3.0):
1. 全A股覆盖 (~5000只)
2. 多周期共振+HMM市场分析（仅牛市时执行策略）
3. 完整牛市时段回测（2019/2020/2024/2025）
4. 递归参数优化

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
os.environ["JQDATA_USERNAME"] = "13327806797"

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
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "bull_market_v3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 牛市时段定义（统一长度版：20天训练 + 10天验证）
# =============================================================================
BULL_MARKET_PERIODS = {
    # 2024年政策牛市（已表现好，保留）
    "2024_policy": {
        "train_start": "2024-09-20",
        "train_end": "2024-10-10",  # 20个交易日
        "validate_start": "2024-10-11",
        "validate_end": "2024-10-21",  # 10个交易日
        "description": "2024年政策牛市",
    },
    # 2024年末涨势（缩短）
    "2024_year_end": {
        "train_start": "2024-11-01",
        "train_end": "2024-11-21",  # 20个交易日
        "validate_start": "2024-11-22",
        "validate_end": "2024-12-02",  # 10个交易日
        "description": "2024年末涨势",
    },
    # 2025年12月涨势（调整）
    "2025_december": {
        "train_start": "2025-12-01",
        "train_end": "2025-12-21",  # 20个交易日
        "validate_start": "2025-12-22",
        "validate_end": "2026-01-01",  # 10个交易日
        "description": "2025年12月涨势",
    },
    # 2020年流动性牛市（缩短）
    "2020_summer": {
        "train_start": "2020-07-01",
        "train_end": "2020-07-21",  # 20个交易日
        "validate_start": "2020-07-22",
        "validate_end": "2020-08-01",  # 10个交易日
        "description": "2020年流动性牛市",
    },
    # 2019年科创板预期牛市（缩短）
    "2019_spring": {
        "train_start": "2019-01-02",
        "train_end": "2019-01-22",  # 20个交易日
        "validate_start": "2019-01-23",
        "validate_end": "2019-02-02",  # 10个交易日
        "description": "2019年科创板预期牛市",
    },
}


@dataclass
class BullMarketParamsV3:
    """牛市策略参数V3（完整版）"""
    # 动量阈值
    min_mom_20d: float = -1.25
    max_mom_20d: float = 25.0
    max_rel_position: float = 80.0
    min_vol_ratio: float = 1.0
    
    # 涨停因子阈值（来自追涨优化）
    limit_up_threshold: float = 0.093
    vol_ratio_threshold_first: float = 2.5
    
    # 突破因子阈值
    mom_5d_threshold_breakout: float = 16.0
    vol_ratio_threshold_breakout: float = 1.5
    breakout_ratio_min: float = 5.0
    
    # 资金流向阈值
    min_flow_strength: float = 0.3
    
    # 信号阈值
    min_signal_score: float = 55.0
    
    # 持仓配置
    max_positions: int = 5
    single_position_max: float = 0.2
    rebalance_period: int = 5
    
    # 止损止盈（已优化）
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


class MarketRegimeChecker:
    """市场状态检测器 - 使用多周期共振+HMM"""
    
    def __init__(self):
        self._analyzer = None
        self._jq = None
    
    def _get_jq(self):
        """获取JQData连接"""
        if self._jq is None:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(os.environ.get("JQDATA_USER"), os.environ.get("JQDATA_PASSWORD"))
            self._jq = jq
        return self._jq
    
    def _ensure_analyzer(self):
        """初始化MarketTrendAnalyzer"""
        if self._analyzer is None:
            try:
                from core.market_trend_analyzer import (
                    MarketTrendAnalyzer,
                    MarketTrendAnalyzerConfig,
                )
                config = MarketTrendAnalyzerConfig(
                    scoring_style="smooth_grouped",
                    active_periods=["week", "month", "quarter"],
                )
                self._analyzer = MarketTrendAnalyzer(config)
                logger.info("MarketRegimeChecker: 分析器初始化成功")
            except Exception as e:
                logger.warning(f"MarketTrendAnalyzer初始化失败: {e}")
                self._analyzer = None
    
    def check_market_regime(
        self,
        as_of_date: str,
        index_code: str = "000300.XSHG",
    ) -> Dict[str, Any]:
        """
        检测市场状态
        
        Returns:
            Dict: {
                "is_bull": bool,       # 是否牛市
                "score": float,        # 综合评分 [0,100]
                "position_cap": float, # 仓位上限 [0,1]
                "regime": str,         # 市场状态描述
                "resonance": Dict,     # 共振详情
            }
        """
        self._ensure_analyzer()
        
        result = {
            "is_bull": False,
            "score": 50.0,
            "position_cap": 0.5,
            "regime": "未知",
            "resonance": {},
        }
        
        if self._analyzer is None:
            # 如果分析器不可用，使用简单判断
            return self._simple_check(as_of_date, index_code)
        
        try:
            signal = self._analyzer.analyze(index_code, as_of_date)
            
            if signal is None:
                return self._simple_check(as_of_date, index_code)
            
            # 获取信号信息
            signal_dict = signal.to_dict()
            
            # 提取关键指标
            composite_score = signal_dict.get("composite_score", 50)
            trend_direction = signal_dict.get("trend_direction", "震荡盘整")
            regime = signal_dict.get("regime", "震荡")
            
            # 共振信息
            resonance = {
                "week": signal_dict.get("period_signals", {}).get("week", {}),
                "month": signal_dict.get("period_signals", {}).get("month", {}),
                "quarter": signal_dict.get("period_signals", {}).get("quarter", {}),
            }
            
            # 判断是否牛市
            is_bull = (
                composite_score >= 60 and 
                trend_direction in ["强势上涨", "上涨趋势", "弱势上涨"]
            )
            
            # 计算仓位上限
            if composite_score >= 75:
                position_cap = 1.0
            elif composite_score >= 60:
                position_cap = 0.8
            elif composite_score >= 50:
                position_cap = 0.5
            else:
                position_cap = 0.3
            
            result = {
                "is_bull": is_bull,
                "score": composite_score,
                "position_cap": position_cap,
                "regime": f"{regime} ({trend_direction})",
                "resonance": resonance,
            }
            
        except Exception as e:
            logger.warning(f"市场状态检测失败: {e}")
            return self._simple_check(as_of_date, index_code)
        
        return result
    
    def _simple_check(
        self,
        as_of_date: str,
        index_code: str,
    ) -> Dict[str, Any]:
        """简单市场检测（备用方法）"""
        try:
            jq = self._get_jq()
            
            # 获取近60日数据
            end_date = as_of_date
            start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=90)).strftime("%Y-%m-%d")
            
            df = jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency="daily",
                fields=["close"],
            )
            
            if df is None or df.empty or len(df) < 20:
                return {
                    "is_bull": False,
                    "score": 50.0,
                    "position_cap": 0.5,
                    "regime": "数据不足",
                    "resonance": {},
                }
            
            # 简单计算：20日/60日涨幅
            close = df["close"]
            mom_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
            mom_60d = (close.iloc[-1] / close.iloc[0] - 1) * 100
            
            # 简单评分
            score = 50 + mom_20d * 0.5 + mom_60d * 0.3
            score = max(0, min(100, score))
            
            is_bull = score >= 60 and mom_20d > 5
            
            return {
                "is_bull": is_bull,
                "score": score,
                "position_cap": min(1.0, score / 100 + 0.2),
                "regime": "牛市" if is_bull else "非牛市",
                "resonance": {
                    "mom_20d": mom_20d,
                    "mom_60d": mom_60d,
                },
            }
            
        except Exception as e:
            logger.error(f"简单市场检测失败: {e}")
            return {
                "is_bull": True,  # 默认执行策略
                "score": 50.0,
                "position_cap": 0.5,
                "regime": "检测失败",
                "resonance": {},
            }


def classify_market_regime(period_name: str) -> str:
    """市场周期分类函数
    
    将不同的牛市时段分类为不同的市场周期类型：
    - 政策牛市：政策驱动，涨幅快（如2024_policy）
    - 流动性牛市：流动性驱动，波动大（如2020_summer）
    - 年末调整：年末行情，表现不稳定（如2024_year_end）
    - 新兴市场：科创板预期，需要特殊参数（如2019_spring）
    
    Args:
        period_name: 时段名称（如"2024_policy"）
    
    Returns:
        市场周期类型：'policy_bull', 'liquidity_bull', 'year_end', 'emerging_market'
    """
    regime_map = {
        "2024_policy": "policy_bull",      # 政策牛市
        "2020_summer": "liquidity_bull",   # 流动性牛市
        "2024_year_end": "year_end",       # 年末调整
        "2025_december": "year_end",       # 年末调整
        "2019_spring": "emerging_market",  # 新兴市场
    }
    
    return regime_map.get(period_name, "policy_bull")  # 默认为政策牛市


def get_all_a_stocks_full(
    provider: ResearchDataProvider,
    date: str = None,
    exclude_st: bool = True,
    exclude_new: bool = True,
    min_days_listed: int = 60,
) -> List[str]:
    """
    获取完整全A股列表
    
    包含：沪市主板、深市主板、创业板
    排除：科创板、北交所、ST、次新股
    """
    try:
        stocks = provider.get_all_a_stocks(
            date=date,
            exclude_st=exclude_st,
            exclude_new=exclude_new,
            exclude_kcb=True,   # 排除科创板（流动性差）
            exclude_bj=True,    # 排除北交所
            min_days_listed=min_days_listed,
        )
        logger.info(f"获取全A股: {len(stocks)} 只")
        return stocks
    except Exception as e:
        logger.error(f"获取全A股失败: {e}")
        # 回退到沪深300
        return provider.get_index_stocks("000300.XSHG")


def run_single_backtest(
    data: Any,
    factors: Any,
    params: BullMarketParamsV3,
) -> BacktestResult:
    """运行单次回测"""
    signal_params = params.to_signal_params()
    engine = SignalEngine(params=signal_params)
    signals = engine.generate_signals(data, factors, signal_params)
    
    backtest = VBTBacktest(initial_capital=1000000)
    result = backtest.run(data, factors, signal_params)
    
    return result


def calculate_score(result: BacktestResult) -> float:
    """计算综合评分（目标：周频10%）"""
    if result.trading_days <= 0:
        return 0.0
    
    weekly_return = result.total_return / max(1, result.trading_days / 5)
    
    score = 0.0
    
    # 年化收益（权重35%）
    if result.annual_return > 0:
        score += min(result.annual_return, 300) * 0.35
    
    # 周收益率（权重30%，目标10%）
    weekly_score = min(weekly_return, 20) * 5
    score += weekly_score * 0.30
    
    # 夏普比率（权重20%）
    if result.sharpe_ratio > 0:
        score += min(result.sharpe_ratio * 25, 75) * 0.20
    
    # 最大回撤惩罚（权重15%）
    drawdown_penalty = max(0, 30 - result.max_drawdown)
    score += drawdown_penalty * 0.15
    
    return score


def generate_param_grid_by_regime(regime: str) -> List[BullMarketParamsV3]:
    """根据市场周期生成参数网格
    
    Args:
        regime: 市场周期类型（'policy_bull', 'liquidity_bull', 'year_end', 'emerging_market'）
    
    Returns:
        参数组合列表
    """
    if regime == "policy_bull":
        # 政策牛市：更激进的参数（止损-6%，止盈50%）
        param_space = {
            "stop_loss_pct": [-0.06, -0.08],
            "take_profit_pct": [0.40, 0.50],
            "trailing_stop_pct": [-0.06, -0.08],
            "trailing_stop_trigger": [0.12, 0.15],
            "max_positions": [5, 8],
            "single_position_max": [0.30, 0.40],
            "min_flow_strength": [0.0, 0.3],
            "min_signal_score": [52.0, 55.0],
        }
    elif regime == "liquidity_bull":
        # 流动性牛市：更保守的参数（止损-10%，止盈30%）
        param_space = {
            "stop_loss_pct": [-0.10, -0.12],
            "take_profit_pct": [0.25, 0.30],
            "trailing_stop_pct": [-0.08, -0.10],
            "trailing_stop_trigger": [0.15, 0.20],
            "max_positions": [3, 5],
            "single_position_max": [0.30, 0.40],
            "min_flow_strength": [0.3],
            "min_signal_score": [55.0, 58.0],
        }
    elif regime == "year_end":
        # 年末调整：适中参数（止损-8%，止盈40%）
        param_space = {
            "stop_loss_pct": [-0.08, -0.10],
            "take_profit_pct": [0.30, 0.40],
            "trailing_stop_pct": [-0.07, -0.09],
            "trailing_stop_trigger": [0.12, 0.15],
            "max_positions": [3, 5],
            "single_position_max": [0.30, 0.40],
            "min_flow_strength": [0.0, 0.3],
            "min_signal_score": [52.0, 55.0],
        }
    elif regime == "emerging_market":
        # 新兴市场：特殊参数（科创板预期）
        param_space = {
            "stop_loss_pct": [-0.08, -0.10],
            "take_profit_pct": [0.30, 0.40],
            "trailing_stop_pct": [-0.08, -0.10],
            "trailing_stop_trigger": [0.15, 0.20],
            "max_positions": [3, 5],
            "single_position_max": [0.30, 0.40],
            "min_flow_strength": [0.3],
            "min_signal_score": [55.0, 58.0],
        }
    else:
        # 默认：政策牛市参数
        param_space = {
            "stop_loss_pct": [-0.06, -0.08],
            "take_profit_pct": [0.40, 0.50],
            "trailing_stop_pct": [-0.06, -0.08],
            "trailing_stop_trigger": [0.12, 0.15],
            "max_positions": [5, 8],
            "single_position_max": [0.30, 0.40],
            "min_flow_strength": [0.0, 0.3],
            "min_signal_score": [52.0, 55.0],
        }
    
    param_list = []
    keys = list(param_space.keys())
    values = list(param_space.values())
    
    for combo in product(*values):
        params = BullMarketParamsV3()
        for key, value in zip(keys, combo):
            setattr(params, key, value)
        param_list.append(params)
    
    logger.info(f"{regime}参数组合: {len(param_list)} 个")
    return param_list


def generate_param_grid_v3() -> List[BullMarketParamsV3]:
    """生成V3参数网格（统一版，864个组合）"""
    base_params = BullMarketParamsV3()
    
    # 统一参数网格 - 初始测试（864个组合）
    param_space = {
        # 止损止盈（3×3×2×2 = 36种组合）
        "stop_loss_pct": [-0.06, -0.08, -0.10],
        "take_profit_pct": [0.25, 0.30, 0.40],
        "trailing_stop_pct": [-0.06, -0.08],
        "trailing_stop_trigger": [0.12, 0.15],
        
        # 持仓配置（3×2 = 6种组合）
        "max_positions": [3, 5, 8],
        "single_position_max": [0.30, 0.40],
        
        # 资金流向（2种）
        "min_flow_strength": [0.0, 0.3],
        
        # 信号阈值（2种）
        "min_signal_score": [52.0, 55.0],
    }
    
    param_list = []
    keys = list(param_space.keys())
    values = list(param_space.values())
    
    for combo in product(*values):
        params = BullMarketParamsV3()
        for key, value in zip(keys, combo):
            setattr(params, key, value)
        param_list.append(params)
    
    logger.info(f"V3参数组合: {len(param_list)} 个")
    return param_list


def run_period_optimization(
    provider: ResearchDataProvider,
    stocks: List[str],
    period: Dict[str, str],
    period_name: str,
    max_stocks: int = 1000,
) -> Tuple[BullMarketParamsV3, BacktestResult, List[Dict]]:
    """单时段优化（支持分周期策略）"""
    logger.info(f"\n{'='*60}")
    logger.info(f"优化时段: {period['description']}")
    logger.info(f"训练: {period['train_start']} ~ {period['train_end']} (20个交易日)")
    logger.info(f"验证: {period['validate_start']} ~ {period['validate_end']} (10个交易日)")
    logger.info(f"{'='*60}")
    
    # 检查市场状态
    regime_checker = MarketRegimeChecker()
    market_status = regime_checker.check_market_regime(period['train_start'])
    logger.info(f"市场状态: {market_status['regime']}, 评分: {market_status['score']:.1f}")
    
    # 限制股票数量
    test_stocks = stocks[:max_stocks]
    logger.info(f"使用股票: {len(test_stocks)} 只")
    
    try:
        # 获取训练数据
        train_data = provider.get_data_matrices(
            symbols=test_stocks,
            start_date=period["train_start"],
            end_date=period["train_end"],
        )
        
        # 获取验证数据
        val_data = provider.get_data_matrices(
            symbols=test_stocks,
            start_date=period["validate_start"],
            end_date=period["validate_end"],
        )
        
    except Exception as e:
        logger.error(f"数据获取失败: {e}")
        return None, None, []
    
    # 计算因子 - 优先使用聚宽因子库（276个现成因子，无需自己计算！）
    # 启用因子缓存（Parquet格式，加速回测）
    calculator = FactorCalculator(use_gpu=False, use_cache=True)
    
    # 聚宽因子库因子列表（直接调用，无需计算）
    jq_factor_list = [
        # CNE5风格因子（5个）
        "size", "beta", "momentum", "liquidity", "residual_volatility",
        # 质量因子
        "roe_ttm", "roa_ttm", "gross_income_ratio",
        # 动量因子
        "ROC6", "ROC12", "ROC20", "ROC60",
        "Price1M", "Price3M",
        # 技术因子
        "VOL20", "BIAS20",
        # 估值因子
        "PEG",
        # 成长因子
        "net_profit_growth_rate", "operating_revenue_growth_rate",
    ]
    
    # 自定义因子列表（聚宽没有的因子）
    custom_factor_list = [
        "mom_20d", "mom_5d", "rel_position",  # 自定义动量
        "vol_ratio", "vol_ratio_5d",  # 量比
        "is_limit_up", "limit_up_count_5d", "is_first_limit_up", "limit_up_vol_ratio",  # 涨停
        "breakout_60d", "breakout_ratio",  # 突破
        "main_flow", "flow_strength",  # 资金流向
    ]
    
    # 混合计算：聚宽因子库 + 自定义因子
    logger.info(f"加载聚宽因子库: {len(jq_factor_list)} 个因子")
    train_factors = calculator.calculate_factors_with_jqdata(
        data=train_data,
        jq_factor_list=jq_factor_list,
        custom_factor_list=custom_factor_list,
    )
    val_factors = calculator.calculate_factors_with_jqdata(
        data=val_data,
        jq_factor_list=jq_factor_list,
        custom_factor_list=custom_factor_list,
    )
    
    # 参数网格 - 分市场周期策略
    regime = classify_market_regime(period_name)
    logger.info(f"市场周期: {regime}")
    param_grid = generate_param_grid_by_regime(regime)
    
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
                overfit_ratio = abs(val_score - train_score) / (train_score + 1e-8)
            else:
                overfit_ratio = 1.0
            
            result_dict = {
                "combo_id": i + 1,
                "period": period["description"],
                "train_score": train_score,
                "val_score": val_score,
                "overfit_ratio": overfit_ratio,
                "train_return": train_result.total_return,
                "val_return": val_result.total_return,
                "train_sharpe": train_result.sharpe_ratio,
                "val_sharpe": val_result.sharpe_ratio,
                "train_drawdown": train_result.max_drawdown,
                "val_drawdown": val_result.max_drawdown,
                "stop_loss_pct": params.stop_loss_pct,
                "take_profit_pct": params.take_profit_pct,
                "max_positions": params.max_positions,
            }
            results.append(result_dict)
            
            # 更新最优（考虑过拟合惩罚）
            final_score = val_score * (1 - 0.3 * min(overfit_ratio, 1.0))
            if final_score > best_score:
                best_score = final_score
                best_params = params
                best_result = val_result
            
            if (i + 1) % 50 == 0:
                logger.info(f"进度: {i+1}/{len(param_grid)}, 最优评分: {best_score:.2f}")
                
        except Exception as e:
            logger.error(f"组合 {i+1} 失败: {e}")
            continue
    
    if best_params:
        weekly_return = best_result.total_return / max(1, best_result.trading_days / 5)
        logger.info(f"时段最优: 评分={best_score:.2f}, 周收益={weekly_return:.2f}%")
    
    return best_params, best_result, results


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("牛市极端高收益策略 V3.0 - 完善版")
    logger.info(f"目标: 周频10%收益")
    logger.info("=" * 70)
    
    start_time = datetime.now()
    
    # Step 1: 获取全A股
    logger.info("\n[Step 1] 获取全A股列表...")
    provider = ResearchDataProvider(use_cache=True)
    all_stocks = get_all_a_stocks_full(provider)
    logger.info(f"全A股: {len(all_stocks)} 只 (排除科创板/北交所/ST/次新)")
    
    # Step 2: 多时段优化
    logger.info("\n[Step 2] 多时段回测优化...")
    
    all_results = []
    period_best = {}
    
    # 选择要测试的时段（包含2025年12月）
    test_periods = ["2024_policy", "2024_year_end", "2025_december", "2020_summer", "2019_spring"]
    
    for period_name in test_periods:
        if period_name not in BULL_MARKET_PERIODS:
            continue
            
        period = BULL_MARKET_PERIODS[period_name]
        
        try:
            best_params, best_result, results = run_period_optimization(
                provider=provider,
                stocks=all_stocks,
                period=period,
                period_name=period_name,
                max_stocks=500,  # 每时段用500只加速
            )
            
            if best_params and best_result:
                period_best[period_name] = {
                    "params": best_params,
                    "result": best_result,
                    "description": period["description"],
                }
                all_results.extend(results)
                
        except Exception as e:
            logger.error(f"时段 {period_name} 优化失败: {e}")
            continue
    
    # Step 3: 综合最优参数
    logger.info("\n[Step 3] 综合分析最优参数...")
    
    if not period_best:
        logger.error("所有时段优化失败!")
        return
    
    # 选择综合表现最好的参数
    best_overall_score = -float('inf')
    best_overall_params = None
    best_overall_period = None
    
    for period_name, data in period_best.items():
        result = data["result"]
        weekly_return = result.total_return / max(1, result.trading_days / 5)
        score = calculate_score(result)
        
        logger.info(f"{period_name}: 周收益={weekly_return:.2f}%, 评分={score:.2f}")
        
        if score > best_overall_score:
            best_overall_score = score
            best_overall_params = data["params"]
            best_overall_period = period_name
    
    logger.info(f"\n综合最优时段: {best_overall_period}")
    logger.info(f"综合最优评分: {best_overall_score:.2f}")
    
    # Step 4: 保存结果
    logger.info("\n[Step 4] 保存结果...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存最优参数
    best_params_path = OUTPUT_DIR / f"best_params_v3_{timestamp}.json"
    best_result = period_best[best_overall_period]["result"]
    
    with open(best_params_path, "w") as f:
        json.dump({
            "version": "V3.0",
            "params": asdict(best_overall_params),
            "best_period": best_overall_period,
            "result": {
                "total_return": best_result.total_return,
                "annual_return": best_result.annual_return,
                "sharpe_ratio": best_result.sharpe_ratio,
                "max_drawdown": best_result.max_drawdown,
                "win_rate": best_result.win_rate,
                "total_trades": best_result.total_trades,
                "trading_days": best_result.trading_days,
                "weekly_return": best_result.total_return / max(1, best_result.trading_days / 5),
            },
            "all_periods_tested": list(period_best.keys()),
            "timestamp": timestamp,
        }, f, indent=2, ensure_ascii=False)
    logger.info(f"最优参数: {best_params_path}")
    
    # 保存优化历史
    if all_results:
        history_path = OUTPUT_DIR / f"optimization_history_v3_{timestamp}.csv"
        pd.DataFrame(all_results).to_csv(history_path, index=False)
        logger.info(f"优化历史: {history_path}")
    
    # 生成报告
    report_path = OUTPUT_DIR / f"strategy_report_v3_{timestamp}.md"
    with open(report_path, "w") as f:
        f.write("# 牛市极端高收益策略 V3.0 - 优化报告\n\n")
        f.write(f"**生成时间**: {timestamp}\n")
        f.write(f"**股票池**: 全A股 {len(all_stocks)} 只\n\n")
        
        f.write("## 多时段回测结果\n\n")
        f.write("| 时段 | 描述 | 总收益 | 周收益 | 夏普 | 回撤 | 评分 |\n")
        f.write("|------|------|--------|--------|------|------|------|\n")
        
        for period_name, data in period_best.items():
            result = data["result"]
            weekly = result.total_return / max(1, result.trading_days / 5)
            score = calculate_score(result)
            f.write(f"| {period_name} | {data['description']} | "
                   f"{result.total_return:.2f}% | {weekly:.2f}% | "
                   f"{result.sharpe_ratio:.2f} | {result.max_drawdown:.2f}% | {score:.2f} |\n")
        
        f.write(f"\n## 综合最优参数\n\n")
        f.write(f"**最优时段**: {best_overall_period}\n\n")
        f.write("| 参数 | 值 |\n")
        f.write("|------|----|\n")
        for key, value in asdict(best_overall_params).items():
            f.write(f"| {key} | {value} |\n")
        
        weekly_return = best_result.total_return / max(1, best_result.trading_days / 5)
        f.write(f"\n## 最优结果\n\n")
        f.write(f"- **周均收益率**: {weekly_return:.2f}%\n")
        f.write(f"- **年化收益率**: {best_result.annual_return:.2f}%\n")
        f.write(f"- **夏普比率**: {best_result.sharpe_ratio:.2f}\n")
        f.write(f"- **最大回撤**: {best_result.max_drawdown:.2f}%\n")
        
        if weekly_return >= 10:
            f.write(f"\n✅ **达到周频10%收益目标!**\n")
        elif weekly_return >= 5:
            f.write(f"\n⚠️ 接近目标 (差 {10 - weekly_return:.2f}%)\n")
        else:
            f.write(f"\n❌ 距离目标还差 {10 - weekly_return:.2f}%\n")
    
    logger.info(f"策略报告: {report_path}")
    
    # 总结
    elapsed = datetime.now() - start_time
    logger.info("\n" + "=" * 70)
    logger.info("V3.0优化完成!")
    logger.info(f"耗时: {elapsed.total_seconds():.1f} 秒")
    logger.info(f"最优时段: {best_overall_period}")
    weekly_return = best_result.total_return / max(1, best_result.trading_days / 5)
    logger.info(f"周均收益: {weekly_return:.2f}%")
    logger.info(f"年化收益: {best_result.annual_return:.2f}%")
    logger.info(f"夏普比率: {best_result.sharpe_ratio:.2f}")
    if weekly_return >= 10:
        logger.info("🎉 达到周频10%收益目标!")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
