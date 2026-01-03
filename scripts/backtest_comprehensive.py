#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场状态信号综合回测框架
========================

验证方法：
1. 信号准确率 - 计算预测准确率、精确率、召回率
2. 滚动验证 (Walk-Forward) - 样本外测试
3. 策略收益验证 - 转化为可交易策略，计算收益指标

数据范围: 2020-01-01 至 2025-12-31
指数: 000001.XSHG (上证指数)

目标:
- 趋势方向准确率 > 55%
- IBD跟踪日胜率 > 55%
- 策略夏普比率 > 0.5
- 最大回撤 < 15%
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import logging
import json

# 项目路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 导入核心模块
try:
    from core.market_state_definitions import (
        UnifiedMarketState,
        MarketRegime,
        TrendDirection,
        MarketPhase,
        determine_market_phase,
        score_to_trend_direction,
    )
    from core.trend_analyzer import TrendAnalyzer
    from core.ibd_style_analyzer import IBDStyleAnalyzer, MarketStatus
    from core.market_regime.market_regime_detector import MarketRegimeDetector, get_market_regime_detector
    from jqdata.client import JQDataClient
    IMPORTS_OK = True
except ImportError as e:
    logger.error(f"Import error: {e}")
    IMPORTS_OK = False


@dataclass
class BacktestConfig:
    """回测配置"""
    start_date: str = "2020-01-01"
    end_date: str = "2025-12-31"
    index_code: str = "000001.XSHG"
    initial_capital: float = 1000000.0
    
    # Walk-forward参数
    train_days: int = 252       # 训练期天数（1年）
    test_days: int = 63         # 测试期天数（3个月）
    step_days: int = 21         # 滚动步长（1个月）
    
    # 信号参数
    trend_threshold: float = 10.0  # 趋势信号阈值
    position_scale: float = 1.0    # 仓位比例系数
    
    # 交易成本
    commission_rate: float = 0.001  # 佣金率
    slippage: float = 0.001         # 滑点


@dataclass
class SignalAccuracyResult:
    """信号准确率结果"""
    signal_name: str
    total_signals: int = 0
    correct_signals: int = 0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    
    # 分类统计
    true_positive: int = 0
    true_negative: int = 0
    false_positive: int = 0
    false_negative: int = 0
    
    def calculate_metrics(self):
        """计算各项指标"""
        total = self.true_positive + self.true_negative + self.false_positive + self.false_negative
        if total > 0:
            self.total_signals = total
            self.correct_signals = self.true_positive + self.true_negative
            self.accuracy = self.correct_signals / total
        
        # 精确率
        if self.true_positive + self.false_positive > 0:
            self.precision = self.true_positive / (self.true_positive + self.false_positive)
        
        # 召回率
        if self.true_positive + self.false_negative > 0:
            self.recall = self.true_positive / (self.true_positive + self.false_negative)
        
        # F1分数
        if self.precision + self.recall > 0:
            self.f1_score = 2 * self.precision * self.recall / (self.precision + self.recall)
    
    def to_dict(self) -> Dict:
        return {
            "signal_name": self.signal_name,
            "total_signals": self.total_signals,
            "correct_signals": self.correct_signals,
            "accuracy": round(self.accuracy, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
        }


@dataclass
class StrategyResult:
    """策略回测结果"""
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    trade_count: int = 0
    avg_holding_days: float = 0.0
    
    # 与基准对比
    benchmark_return: float = 0.0
    benchmark_sharpe: float = 0.0
    alpha: float = 0.0
    beta: float = 0.0
    information_ratio: float = 0.0
    
    # 净值序列
    portfolio_values: pd.Series = None
    benchmark_values: pd.Series = None
    drawdown_series: pd.Series = None
    
    def to_dict(self) -> Dict:
        return {
            "total_return": round(self.total_return, 4),
            "annual_return": round(self.annual_return, 4),
            "sharpe_ratio": round(self.sharpe_ratio, 4),
            "max_drawdown": round(self.max_drawdown, 4),
            "win_rate": round(self.win_rate, 4),
            "profit_factor": round(self.profit_factor, 4),
            "trade_count": self.trade_count,
            "benchmark_return": round(self.benchmark_return, 4),
            "benchmark_sharpe": round(self.benchmark_sharpe, 4),
            "alpha": round(self.alpha, 4),
        }


class ComprehensiveBacktester:
    """综合回测器"""
    
    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig()
        self.jq_client = None
        self.trend_analyzer = None
        self.ibd_analyzer = None
        self.regime_detector = None
        
        # 缓存数据
        self.price_data: pd.DataFrame = None
        self.signal_history: List[Dict] = []
        
    def initialize(self) -> bool:
        """初始化回测器"""
        try:
            # 初始化JQData
            self.jq_client = JQDataClient()
            from config.config_manager import ConfigManager
            config_manager = ConfigManager()
            jq_config = config_manager.get_config("jqdata_config.json")
            self.jq_client.authenticate(
                username=jq_config.get("username"),
                password=jq_config.get("password")
            )
            
            # 初始化分析器
            self.trend_analyzer = TrendAnalyzer(jq_client=self.jq_client)
            self.ibd_analyzer = IBDStyleAnalyzer()
            self.regime_detector = get_market_regime_detector()
            
            logger.info("✅ 回测器初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 回测器初始化失败: {e}")
            return False
    
    def load_price_data(self) -> bool:
        """加载价格数据"""
        try:
            logger.info(f"加载价格数据: {self.config.index_code}")
            logger.info(f"时间范围: {self.config.start_date} ~ {self.config.end_date}")
            
            self.price_data = self.jq_client.get_price(
                self.config.index_code,
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                frequency="daily",
                fields=["open", "high", "low", "close", "volume"]
            )
            
            if self.price_data is None or len(self.price_data) == 0:
                logger.error("无法获取价格数据")
                return False
            
            # 计算收益率
            self.price_data["return"] = self.price_data["close"].pct_change()
            self.price_data["return_5d"] = self.price_data["close"].pct_change(5)
            self.price_data["return_20d"] = self.price_data["close"].pct_change(20)
            
            logger.info(f"✅ 加载 {len(self.price_data)} 条价格数据")
            return True
            
        except Exception as e:
            logger.error(f"❌ 加载价格数据失败: {e}")
            return False
    
    def generate_signals(self) -> bool:
        """生成信号"""
        logger.info("开始生成市场信号...")
        
        self.signal_history = []
        total_days = len(self.price_data)
        
        for i, (date, row) in enumerate(self.price_data.iterrows()):
            if i < 60:  # 跳过前60天（需要历史数据计算指标）
                continue
            
            date_str = date.strftime("%Y-%m-%d")
            
            if i % 50 == 0:
                logger.info(f"  处理进度: {i}/{total_days} ({date_str})")
            
            signal = {
                "date": date_str,
                "close": row["close"],
                "return_1d": row["return"] if not pd.isna(row["return"]) else 0,
                "return_5d": row["return_5d"] if not pd.isna(row["return_5d"]) else 0,
                "return_20d": row["return_20d"] if not pd.isna(row["return_20d"]) else 0,
            }
            
            try:
                # 趋势分析
                trend_result = self.trend_analyzer.analyze_market(
                    index_code=self.config.index_code,
                    date=date_str
                )
                if trend_result:
                    signal["trend_score"] = trend_result.composite_score
                    signal["short_score"] = trend_result.short_term.score
                    signal["medium_score"] = trend_result.medium_term.score
                    signal["long_score"] = trend_result.long_term.score
                    signal["market_phase"] = trend_result.market_phase
                else:
                    signal["trend_score"] = 0
                    signal["short_score"] = 0
                    signal["medium_score"] = 0
                    signal["long_score"] = 0
                    signal["market_phase"] = "unknown"
                    
            except Exception as e:
                signal["trend_score"] = 0
                signal["short_score"] = 0
                signal["medium_score"] = 0
                signal["long_score"] = 0
                signal["market_phase"] = "unknown"
            
            try:
                # IBD分析
                ibd_result = self.ibd_analyzer.analyze(
                    index_code=self.config.index_code,
                    date=date_str,
                    lookback_days=60
                )
                if ibd_result:
                    signal["ibd_status"] = ibd_result.market_status.value
                    signal["distribution_count"] = ibd_result.distribution_count
                    signal["ftd_count"] = len(ibd_result.follow_through_days)
                else:
                    signal["ibd_status"] = "unknown"
                    signal["distribution_count"] = 0
                    signal["ftd_count"] = 0
                    
            except Exception as e:
                signal["ibd_status"] = "unknown"
                signal["distribution_count"] = 0
                signal["ftd_count"] = 0
            
            self.signal_history.append(signal)
        
        logger.info(f"✅ 生成 {len(self.signal_history)} 个信号")
        return True
    
    def validate_signal_accuracy(self) -> Dict[str, SignalAccuracyResult]:
        """验证信号准确率"""
        logger.info("\n" + "=" * 60)
        logger.info("验证方法A: 信号准确率")
        logger.info("=" * 60)
        
        results = {}
        
        # 1. 趋势方向准确率
        results["trend_direction"] = self._validate_trend_direction()
        
        # 2. 趋势强度准确率
        results["trend_strength"] = self._validate_trend_strength()
        
        # 3. IBD状态准确率
        results["ibd_status"] = self._validate_ibd_status()
        
        # 打印结果
        for name, result in results.items():
            logger.info(f"\n{result.signal_name}:")
            logger.info(f"  总信号数: {result.total_signals}")
            logger.info(f"  准确率: {result.accuracy:.2%}")
            logger.info(f"  精确率: {result.precision:.2%}")
            logger.info(f"  召回率: {result.recall:.2%}")
            logger.info(f"  F1分数: {result.f1_score:.2%}")
        
        return results
    
    def _validate_trend_direction(self) -> SignalAccuracyResult:
        """验证趋势方向准确率"""
        result = SignalAccuracyResult(signal_name="趋势方向")
        
        for i, signal in enumerate(self.signal_history[:-5]):
            trend_score = signal.get("trend_score", 0)
            future_return = self.signal_history[i + 5].get("return_5d", 0)
            
            # 预测方向
            predicted_up = trend_score > self.config.trend_threshold
            predicted_down = trend_score < -self.config.trend_threshold
            
            # 实际方向
            actual_up = future_return > 0.01  # 上涨超过1%
            actual_down = future_return < -0.01  # 下跌超过1%
            
            # 统计
            if predicted_up:
                if actual_up:
                    result.true_positive += 1
                else:
                    result.false_positive += 1
            elif predicted_down:
                if actual_down:
                    result.true_negative += 1
                else:
                    result.false_negative += 1
        
        result.calculate_metrics()
        return result
    
    def _validate_trend_strength(self) -> SignalAccuracyResult:
        """验证趋势强度准确率"""
        result = SignalAccuracyResult(signal_name="趋势强度")
        
        for i, signal in enumerate(self.signal_history[:-20]):
            trend_score = signal.get("trend_score", 0)
            future_return = self.signal_history[i + 20].get("return_20d", 0)
            
            # 强信号预测
            strong_bullish = trend_score > 50
            strong_bearish = trend_score < -50
            
            # 实际强趋势
            actual_strong_up = future_return > 0.05  # 20天上涨5%
            actual_strong_down = future_return < -0.05  # 20天下跌5%
            
            if strong_bullish:
                if actual_strong_up:
                    result.true_positive += 1
                else:
                    result.false_positive += 1
            elif strong_bearish:
                if actual_strong_down:
                    result.true_negative += 1
                else:
                    result.false_negative += 1
        
        result.calculate_metrics()
        return result
    
    def _validate_ibd_status(self) -> SignalAccuracyResult:
        """验证IBD状态准确率"""
        result = SignalAccuracyResult(signal_name="IBD状态")
        
        for i, signal in enumerate(self.signal_history[:-20]):
            ibd_status = signal.get("ibd_status", "unknown")
            future_return = self.signal_history[i + 20].get("return_20d", 0)
            
            # IBD看涨状态
            ibd_bullish = ibd_status in ["confirmed_uptrend", "rally_attempt"]
            ibd_bearish = ibd_status in ["correction", "uptrend_pressure"]
            
            # 实际走势
            actual_up = future_return > 0.02
            actual_down = future_return < -0.02
            
            if ibd_bullish:
                if actual_up:
                    result.true_positive += 1
                else:
                    result.false_positive += 1
            elif ibd_bearish:
                if actual_down:
                    result.true_negative += 1
                else:
                    result.false_negative += 1
        
        result.calculate_metrics()
        return result
    
    def walk_forward_validation(self) -> List[Dict]:
        """Walk-Forward滚动验证"""
        logger.info("\n" + "=" * 60)
        logger.info("验证方法B: Walk-Forward滚动验证")
        logger.info("=" * 60)
        
        results = []
        signal_df = pd.DataFrame(self.signal_history)
        signal_df["date"] = pd.to_datetime(signal_df["date"])
        signal_df.set_index("date", inplace=True)
        
        total_days = len(signal_df)
        train_days = self.config.train_days
        test_days = self.config.test_days
        step_days = self.config.step_days
        
        window_num = 0
        start_idx = 0
        
        while start_idx + train_days + test_days <= total_days:
            window_num += 1
            train_start = start_idx
            train_end = start_idx + train_days
            test_start = train_end
            test_end = min(test_start + test_days, total_days)
            
            train_data = signal_df.iloc[train_start:train_end]
            test_data = signal_df.iloc[test_start:test_end]
            
            # 训练期统计（计算信号阈值）
            train_mean = train_data["trend_score"].mean()
            train_std = train_data["trend_score"].std()
            
            # 测试期验证
            correct = 0
            total = 0
            
            for i in range(len(test_data) - 5):
                score = test_data.iloc[i]["trend_score"]
                future_return = test_data.iloc[i + 5]["return_5d"] if i + 5 < len(test_data) else 0
                
                # 动态阈值
                threshold = train_mean + 0.5 * train_std
                
                if score > threshold and future_return > 0:
                    correct += 1
                elif score < -threshold and future_return < 0:
                    correct += 1
                elif abs(score) <= threshold and abs(future_return) < 0.02:
                    correct += 1
                
                total += 1
            
            accuracy = correct / total if total > 0 else 0
            
            result = {
                "window": window_num,
                "train_start": train_data.index[0].strftime("%Y-%m-%d"),
                "train_end": train_data.index[-1].strftime("%Y-%m-%d"),
                "test_start": test_data.index[0].strftime("%Y-%m-%d"),
                "test_end": test_data.index[-1].strftime("%Y-%m-%d"),
                "accuracy": accuracy,
                "sample_size": total,
            }
            results.append(result)
            
            logger.info(f"窗口 {window_num}: 测试期 {result['test_start']} ~ {result['test_end']}, "
                       f"准确率: {accuracy:.2%}")
            
            start_idx += step_days
        
        # 汇总
        avg_accuracy = np.mean([r["accuracy"] for r in results])
        std_accuracy = np.std([r["accuracy"] for r in results])
        
        logger.info(f"\nWalk-Forward汇总:")
        logger.info(f"  总窗口数: {len(results)}")
        logger.info(f"  平均准确率: {avg_accuracy:.2%}")
        logger.info(f"  准确率标准差: {std_accuracy:.2%}")
        
        return results
    
    def backtest_strategy(self) -> StrategyResult:
        """策略回测"""
        logger.info("\n" + "=" * 60)
        logger.info("验证方法C: 策略收益验证")
        logger.info("=" * 60)
        
        result = StrategyResult()
        
        # 初始化
        capital = self.config.initial_capital
        position = 0.0  # 当前仓位
        portfolio_values = []
        benchmark_values = []
        positions = []
        trades = []
        
        initial_price = self.signal_history[0]["close"]
        benchmark_capital = capital
        
        for i, signal in enumerate(self.signal_history):
            current_price = signal["close"]
            trend_score = signal.get("trend_score", 0)
            risk_factor = 1.0 - signal.get("distribution_count", 0) * 0.1
            risk_factor = max(0.3, risk_factor)
            
            # 计算目标仓位
            if trend_score > 60:
                target_position = 1.0 * risk_factor
            elif trend_score > 30:
                target_position = 0.7 * risk_factor
            elif trend_score > 0:
                target_position = 0.4 * risk_factor
            elif trend_score > -30:
                target_position = 0.2
            else:
                target_position = 0.0
            
            target_position *= self.config.position_scale
            target_position = min(1.0, max(0.0, target_position))
            
            # 调仓
            if abs(target_position - position) > 0.1:
                # 计算交易成本
                trade_value = abs(target_position - position) * capital
                cost = trade_value * (self.config.commission_rate + self.config.slippage)
                capital -= cost
                
                trades.append({
                    "date": signal["date"],
                    "action": "buy" if target_position > position else "sell",
                    "old_position": position,
                    "new_position": target_position,
                    "cost": cost,
                })
                
                position = target_position
            
            # 更新资金
            daily_return = signal.get("return_1d", 0)
            capital *= (1 + daily_return * position)
            
            # 基准
            benchmark_capital = self.config.initial_capital * (current_price / initial_price)
            
            portfolio_values.append(capital)
            benchmark_values.append(benchmark_capital)
            positions.append(position)
        
        # 转为Series
        dates = [datetime.strptime(s["date"], "%Y-%m-%d") for s in self.signal_history]
        result.portfolio_values = pd.Series(portfolio_values, index=dates)
        result.benchmark_values = pd.Series(benchmark_values, index=dates)
        
        # 计算回撤
        rolling_max = result.portfolio_values.cummax()
        result.drawdown_series = (result.portfolio_values - rolling_max) / rolling_max
        
        # 计算指标
        result.total_return = (capital - self.config.initial_capital) / self.config.initial_capital
        years = len(self.signal_history) / 252
        result.annual_return = (1 + result.total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 计算夏普比率
        daily_returns = result.portfolio_values.pct_change().dropna()
        if len(daily_returns) > 0 and daily_returns.std() > 0:
            result.sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
        
        result.max_drawdown = result.drawdown_series.min()
        result.trade_count = len(trades)
        
        # 计算基准指标
        result.benchmark_return = (benchmark_capital - self.config.initial_capital) / self.config.initial_capital
        benchmark_returns = result.benchmark_values.pct_change().dropna()
        if len(benchmark_returns) > 0 and benchmark_returns.std() > 0:
            result.benchmark_sharpe = benchmark_returns.mean() / benchmark_returns.std() * np.sqrt(252)
        
        # Alpha
        result.alpha = result.annual_return - result.benchmark_return / years if years > 0 else 0
        
        # 胜率
        if trades:
            winning_trades = 0
            for i, trade in enumerate(trades[:-1]):
                next_trade = trades[i + 1]
                if trade["action"] == "buy":
                    # 买入后到下次交易是否盈利
                    trade_date_idx = next(j for j, s in enumerate(self.signal_history) if s["date"] == trade["date"])
                    next_date_idx = next(j for j, s in enumerate(self.signal_history) if s["date"] == next_trade["date"])
                    if next_date_idx > trade_date_idx:
                        price_change = (self.signal_history[next_date_idx]["close"] / 
                                       self.signal_history[trade_date_idx]["close"]) - 1
                        if price_change > 0:
                            winning_trades += 1
            result.win_rate = winning_trades / len(trades) if trades else 0
        
        # 打印结果
        logger.info(f"\n策略回测结果:")
        logger.info(f"  总收益率: {result.total_return:.2%}")
        logger.info(f"  年化收益率: {result.annual_return:.2%}")
        logger.info(f"  夏普比率: {result.sharpe_ratio:.2f}")
        logger.info(f"  最大回撤: {result.max_drawdown:.2%}")
        logger.info(f"  交易次数: {result.trade_count}")
        logger.info(f"  胜率: {result.win_rate:.2%}")
        logger.info(f"\n基准对比:")
        logger.info(f"  基准收益率: {result.benchmark_return:.2%}")
        logger.info(f"  基准夏普: {result.benchmark_sharpe:.2f}")
        logger.info(f"  Alpha: {result.alpha:.2%}")
        
        return result
    
    def run_full_backtest(self) -> Dict[str, Any]:
        """运行完整回测"""
        logger.info("=" * 60)
        logger.info("市场状态信号综合回测")
        logger.info("=" * 60)
        logger.info(f"回测时间: {self.config.start_date} ~ {self.config.end_date}")
        logger.info(f"标的指数: {self.config.index_code}")
        logger.info("=" * 60)
        
        # 1. 初始化
        if not self.initialize():
            return {"success": False, "error": "初始化失败"}
        
        # 2. 加载数据
        if not self.load_price_data():
            return {"success": False, "error": "加载数据失败"}
        
        # 3. 生成信号
        if not self.generate_signals():
            return {"success": False, "error": "生成信号失败"}
        
        # 4. 信号准确率验证
        accuracy_results = self.validate_signal_accuracy()
        
        # 5. Walk-Forward验证
        walk_forward_results = self.walk_forward_validation()
        
        # 6. 策略回测
        strategy_result = self.backtest_strategy()
        
        # 7. 汇总
        logger.info("\n" + "=" * 60)
        logger.info("回测结果汇总")
        logger.info("=" * 60)
        
        summary = {
            "success": True,
            "config": {
                "start_date": self.config.start_date,
                "end_date": self.config.end_date,
                "index_code": self.config.index_code,
            },
            "accuracy": {k: v.to_dict() for k, v in accuracy_results.items()},
            "walk_forward": {
                "windows": len(walk_forward_results),
                "avg_accuracy": np.mean([r["accuracy"] for r in walk_forward_results]),
                "results": walk_forward_results,
            },
            "strategy": strategy_result.to_dict(),
            "targets": {
                "trend_accuracy_target": 0.55,
                "trend_accuracy_actual": accuracy_results["trend_direction"].accuracy,
                "trend_accuracy_pass": accuracy_results["trend_direction"].accuracy >= 0.55,
                "sharpe_target": 0.5,
                "sharpe_actual": strategy_result.sharpe_ratio,
                "sharpe_pass": strategy_result.sharpe_ratio >= 0.5,
                "max_dd_target": -0.15,
                "max_dd_actual": strategy_result.max_drawdown,
                "max_dd_pass": strategy_result.max_drawdown >= -0.15,
            },
        }
        
        # 打印目标达成情况
        logger.info("\n目标达成情况:")
        for key, val in summary["targets"].items():
            if key.endswith("_pass"):
                metric_name = key.replace("_pass", "")
                status = "✅" if val else "❌"
                logger.info(f"  {metric_name}: {status}")
        
        return summary
    
    def save_results(self, results: Dict, filepath: str):
        """保存回测结果"""
        # 移除不可序列化的对象
        save_data = {
            "success": results.get("success"),
            "config": results.get("config"),
            "accuracy": results.get("accuracy"),
            "walk_forward": {
                "windows": results["walk_forward"]["windows"],
                "avg_accuracy": results["walk_forward"]["avg_accuracy"],
            },
            "strategy": results.get("strategy"),
            "targets": results.get("targets"),
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False, default=lambda x: bool(x) if isinstance(x, (bool, np.bool_)) else x)
        
        logger.info(f"结果已保存到: {filepath}")


def main():
    """主函数"""
    config = BacktestConfig(
        start_date="2020-01-01",
        end_date="2025-12-31",
        index_code="000001.XSHG",
    )
    
    backtester = ComprehensiveBacktester(config)
    results = backtester.run_full_backtest()
    
    # 只有成功时才保存结果
    if not results.get("success", False):
        logger.error(f"回测失败: {results.get('error', 'Unknown error')}")
        return results
    
    # 保存结果
    output_dir = os.path.join(PROJECT_ROOT, "backtest_results")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"comprehensive_backtest_{timestamp}.json")
    backtester.save_results(results, output_file)
    
    return results


if __name__ == "__main__":
    main()

