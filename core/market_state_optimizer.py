"""
市场状态判断参数优化器
======================

基于历史数据验证结果，优化市场状态判断的参数：
1. 趋势方向阈值优化
2. 市场阶段判断条件优化
3. 信号权重优化

优化目标：
- 趋势方向准确率 > 50%
- 市场阶段方向一致性 > 55%
- 得分与收益正相关
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class OptimizedParams:
    """优化后的参数"""
    
    # 趋势方向阈值（原始: 20/-20）
    bullish_threshold: float = 20.0
    bearish_threshold: float = -20.0
    
    # 市场阶段判断阈值
    long_term_bull_threshold: float = 30.0
    long_term_bear_threshold: float = -30.0
    medium_term_strong_threshold: float = 20.0
    short_term_strong_threshold: float = 20.0
    
    # 信号权重
    short_weight: float = 0.3
    medium_weight: float = 0.4
    long_weight: float = 0.3
    
    # A股特色调整
    enable_contrarian: bool = False  # 启用逆向信号（熊市超跌反弹）
    oversold_bounce_threshold: float = -50.0  # 超跌反弹阈值
    
    def to_dict(self) -> Dict:
        return {
            "bullish_threshold": self.bullish_threshold,
            "bearish_threshold": self.bearish_threshold,
            "long_term_bull_threshold": self.long_term_bull_threshold,
            "long_term_bear_threshold": self.long_term_bear_threshold,
            "medium_term_strong_threshold": self.medium_term_strong_threshold,
            "short_term_strong_threshold": self.short_term_strong_threshold,
            "short_weight": self.short_weight,
            "medium_weight": self.medium_weight,
            "long_weight": self.long_weight,
            "enable_contrarian": self.enable_contrarian,
            "oversold_bounce_threshold": self.oversold_bounce_threshold,
        }


class MarketStateOptimizer:
    """市场状态参数优化器"""
    
    def __init__(self):
        self.best_params = OptimizedParams()
        self.optimization_history = []
    
    def analyze_score_distribution(self, predictions: List[Dict]) -> Dict:
        """分析得分分布与收益关系"""
        
        scores = []
        returns_5d = []
        returns_20d = []
        
        for p in predictions:
            score = p.get("trend_score")
            r5 = p.get("return_5d")
            r20 = p.get("return_20d")
            
            if all(v is not None and not np.isnan(v) for v in [score, r5, r20]):
                scores.append(score)
                returns_5d.append(r5)
                returns_20d.append(r20)
        
        scores = np.array(scores)
        returns_5d = np.array(returns_5d)
        returns_20d = np.array(returns_20d)
        
        # 分析不同得分区间的收益
        analysis = {
            "score_stats": {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": np.min(scores),
                "max": np.max(scores),
            },
            "return_by_score_bin": {},
            "optimal_thresholds": {},
        }
        
        # 按得分分组
        bins = [-100, -60, -40, -20, 0, 20, 40, 60, 100]
        for i in range(len(bins) - 1):
            low, high = bins[i], bins[i + 1]
            mask = (scores >= low) & (scores < high)
            if mask.sum() > 10:
                analysis["return_by_score_bin"][f"[{low}, {high})"] = {
                    "count": int(mask.sum()),
                    "avg_return_5d": float(returns_5d[mask].mean()),
                    "avg_return_20d": float(returns_20d[mask].mean()),
                    "win_rate_5d": float((returns_5d[mask] > 0).mean()),
                    "win_rate_20d": float((returns_20d[mask] > 0).mean()),
                }
        
        # 寻找最优阈值
        best_bull_threshold = 20
        best_bear_threshold = -20
        best_accuracy = 0
        
        for bull_th in [10, 15, 20, 25, 30, 35, 40]:
            for bear_th in [-10, -15, -20, -25, -30, -35, -40]:
                pred_up = scores > bull_th
                pred_down = scores < bear_th
                pred_sideways = ~pred_up & ~pred_down
                
                actual_up = returns_5d > 0.02
                actual_down = returns_5d < -0.02
                actual_sideways = ~actual_up & ~actual_down
                
                # 计算准确率
                correct = (
                    (pred_up & actual_up).sum() +
                    (pred_down & actual_down).sum() +
                    (pred_sideways & actual_sideways).sum()
                )
                total = len(scores)
                accuracy = correct / total if total > 0 else 0
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_bull_threshold = bull_th
                    best_bear_threshold = bear_th
        
        analysis["optimal_thresholds"] = {
            "bullish": best_bull_threshold,
            "bearish": best_bear_threshold,
            "best_accuracy": best_accuracy,
        }
        
        return analysis
    
    def analyze_phase_effectiveness(self, predictions: List[Dict]) -> Dict:
        """分析阶段判断有效性"""
        
        from collections import defaultdict
        
        phase_stats = defaultdict(lambda: {"returns": [], "expected_direction": None})
        
        # 阶段期望方向
        expected_directions = {
            "牛市确认(全周期共振)": "up",
            "牛市确认": "up",
            "牛市震荡": "sideways",
            "牛市短期调整": "down",  # 短期看跌
            "牛市中期调整": "down",
            "熊市确认(全周期共振)": "down",
            "熊市确认": "down",
            "熊市反弹": "up",  # 短期反弹
            "熊市技术反弹": "up",
            "熊市筑底": "sideways",
            "突破在即": "up",
            "破位风险": "down",
            "复苏初期": "up",
            "见顶回落": "down",
            "窄幅震荡": "sideways",
            "宽幅震荡": "sideways",
        }
        
        for p in predictions:
            phase = p.get("market_phase", "unknown")
            r20 = p.get("return_20d")
            
            if phase != "unknown" and r20 is not None and not np.isnan(r20):
                phase_stats[phase]["returns"].append(r20)
                phase_stats[phase]["expected_direction"] = expected_directions.get(phase, "sideways")
        
        # 分析每个阶段
        analysis = {}
        for phase, stats in phase_stats.items():
            if not stats["returns"]:
                continue
            
            returns = np.array(stats["returns"])
            expected = stats["expected_direction"]
            
            avg_return = np.mean(returns)
            actual_direction = "up" if avg_return > 0.02 else ("down" if avg_return < -0.02 else "sideways")
            
            # 方向匹配
            direction_match = actual_direction == expected
            
            # A股特色：熊市可能有超跌反弹
            if not direction_match and expected == "down" and avg_return > 0.02:
                # 可能是超跌反弹
                contrarian_opportunity = True
            else:
                contrarian_opportunity = False
            
            analysis[phase] = {
                "count": len(returns),
                "avg_return": float(avg_return),
                "expected_direction": expected,
                "actual_direction": actual_direction,
                "direction_match": direction_match,
                "contrarian_opportunity": contrarian_opportunity,
            }
        
        return analysis
    
    def optimize_for_astock(self, predictions: List[Dict]) -> OptimizedParams:
        """针对A股特点优化参数"""
        
        logger.info("开始A股参数优化...")
        
        # 分析得分分布
        score_analysis = self.analyze_score_distribution(predictions)
        logger.info(f"得分统计: mean={score_analysis['score_stats']['mean']:.2f}, "
                   f"std={score_analysis['score_stats']['std']:.2f}")
        
        # 分析阶段有效性
        phase_analysis = self.analyze_phase_effectiveness(predictions)
        
        # 检查是否存在反向指示
        contrarian_phases = [p for p, a in phase_analysis.items() if a.get("contrarian_opportunity")]
        if contrarian_phases:
            logger.info(f"发现逆向机会阶段: {contrarian_phases}")
        
        # 优化参数
        params = OptimizedParams()
        
        # 使用最优阈值
        if "optimal_thresholds" in score_analysis:
            params.bullish_threshold = score_analysis["optimal_thresholds"]["bullish"]
            params.bearish_threshold = score_analysis["optimal_thresholds"]["bearish"]
            logger.info(f"优化阈值: bullish={params.bullish_threshold}, bearish={params.bearish_threshold}")
        
        # A股特色调整
        # 检查熊市反弹特征
        bear_phases = [p for p in phase_analysis.keys() if "熊市" in p]
        if bear_phases:
            bear_returns = []
            for phase in bear_phases:
                if phase in phase_analysis:
                    bear_returns.append(phase_analysis[phase]["avg_return"])
            
            avg_bear_return = np.mean(bear_returns) if bear_returns else 0
            if avg_bear_return > 0.005:  # 熊市阶段平均收益为正
                params.enable_contrarian = True
                logger.info(f"启用逆向信号（熊市平均收益: {avg_bear_return:.2%}）")
        
        # 根据震荡市场的高识别率，调整权重
        params.short_weight = 0.2   # 降低短期权重（噪音多）
        params.medium_weight = 0.5  # 增加中期权重
        params.long_weight = 0.3    # 保持长期权重
        
        self.best_params = params
        logger.info(f"优化完成: {params.to_dict()}")
        
        return params
    
    def recalculate_trend_score(
        self,
        short_score: float,
        medium_score: float,
        long_score: float,
        params: Optional[OptimizedParams] = None
    ) -> float:
        """使用优化参数重新计算趋势得分"""
        
        if params is None:
            params = self.best_params
        
        # 加权计算
        weighted_score = (
            short_score * params.short_weight +
            medium_score * params.medium_weight +
            long_score * params.long_weight
        )
        
        # A股逆向调整
        if params.enable_contrarian:
            # 极度悲观时考虑反弹
            if weighted_score < params.oversold_bounce_threshold:
                # 超跌后可能反弹，适度调整
                weighted_score = weighted_score * 0.5  # 减弱看跌信号
        
        return weighted_score
    
    def predict_direction(
        self,
        score: float,
        params: Optional[OptimizedParams] = None
    ) -> str:
        """使用优化参数预测方向"""
        
        if params is None:
            params = self.best_params
        
        if score > params.bullish_threshold:
            return "up"
        elif score < params.bearish_threshold:
            return "down"
        else:
            return "sideways"
    
    def validate_optimized_params(self, predictions: List[Dict]) -> Dict:
        """验证优化后的参数"""
        
        logger.info("\n验证优化后的参数...")
        
        correct_up = 0
        correct_down = 0
        correct_sideways = 0
        total_up = 0
        total_down = 0
        total_sideways = 0
        
        for p in predictions:
            short = p.get("short_score", 0)
            medium = p.get("medium_score", 0)
            long = p.get("long_score", 0)
            actual = p.get("actual_trend_5d")
            
            if actual not in ["up", "down", "sideways"]:
                continue
            
            # 使用优化参数
            new_score = self.recalculate_trend_score(short, medium, long)
            predicted = self.predict_direction(new_score)
            
            if predicted == "up":
                total_up += 1
                if actual == "up":
                    correct_up += 1
            elif predicted == "down":
                total_down += 1
                if actual == "down":
                    correct_down += 1
            else:
                total_sideways += 1
                if actual == "sideways":
                    correct_sideways += 1
        
        total = total_up + total_down + total_sideways
        correct = correct_up + correct_down + correct_sideways
        
        results = {
            "overall_accuracy": correct / total if total > 0 else 0,
            "up_precision": correct_up / total_up if total_up > 0 else 0,
            "down_precision": correct_down / total_down if total_down > 0 else 0,
            "sideways_precision": correct_sideways / total_sideways if total_sideways > 0 else 0,
            "total_samples": total,
        }
        
        logger.info(f"优化后准确率: {results['overall_accuracy']:.2%}")
        logger.info(f"  看涨精确率: {results['up_precision']:.2%}")
        logger.info(f"  看跌精确率: {results['down_precision']:.2%}")
        logger.info(f"  震荡精确率: {results['sideways_precision']:.2%}")
        
        return results


def get_optimized_params() -> OptimizedParams:
    """获取优化后的参数（静态方法）"""
    # 基于历史验证的推荐参数
    return OptimizedParams(
        bullish_threshold=30,      # 提高看涨阈值（减少误报）
        bearish_threshold=-30,     # 降低看跌阈值
        short_weight=0.2,          # 降低短期权重
        medium_weight=0.5,         # 增加中期权重
        long_weight=0.3,           # 保持长期权重
        enable_contrarian=True,    # 启用逆向信号
        oversold_bounce_threshold=-50.0,
    )

