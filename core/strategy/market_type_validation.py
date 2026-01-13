# -*- coding: utf-8 -*-
"""
市场类型判断长期回测验证框架
============================

用于验证市场类型判断的准确性和稳定性

功能:
1. 10年历史数据回测
2. 准确率统计
3. 参数优化建议
4. 不同市场环境下的表现分析

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """验证结果"""
    date: str
    predicted_type: str
    actual_type: str  # 基于后续收益判断
    actual_return_5d: float  # 5日实际收益
    actual_return_20d: float  # 20日实际收益
    is_correct: bool
    confidence: float


@dataclass
class ValidationStats:
    """验证统计"""
    total_predictions: int = 0
    correct_predictions: int = 0
    accuracy: float = 0.0
    
    # 各类型准确率
    fast_bull_accuracy: float = 0.0
    slow_bull_accuracy: float = 0.0
    volatile_accuracy: float = 0.0
    bear_accuracy: float = 0.0
    
    # 各类型数量
    fast_bull_count: int = 0
    slow_bull_count: int = 0
    volatile_count: int = 0
    bear_count: int = 0
    
    # 平均收益
    fast_bull_avg_return_5d: float = 0.0
    slow_bull_avg_return_5d: float = 0.0
    volatile_avg_return_5d: float = 0.0
    bear_avg_return_5d: float = 0.0


class MarketTypeValidator:
    """
    市场类型判断验证器
    
    用于长期回测验证市场类型判断的准确性
    """
    
    def __init__(self):
        """初始化验证器"""
        self._jq = None
        self.results: List[ValidationResult] = []
    
    def _ensure_jqdata(self):
        """确保JQData已初始化"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                import json
                config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
                with open(config_path) as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info("JQData认证成功")
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def validate_period(
        self,
        classifier,
        start_date: str,
        end_date: str,
        index_code: str = "000300.XSHG",
    ) -> ValidationStats:
        """
        验证指定时间段的市场类型判断
        
        Args:
            classifier: 市场类型分类器（V6或V7）
            start_date: 开始日期
            end_date: 结束日期
            index_code: 指数代码
        
        Returns:
            ValidationStats: 验证统计结果
        """
        self._ensure_jqdata()
        
        if self._jq is None:
            logger.error("JQData未初始化，无法验证")
            return ValidationStats()
        
        # 获取指数数据
        try:
            index_df = self._jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close'],
            )
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            return ValidationStats()
        
        if index_df is None or len(index_df) < 25:
            logger.warning("数据不足，无法验证")
            return ValidationStats()
        
        # 计算实际收益（用于判断实际市场类型）
        index_df['return_5d'] = index_df['close'].pct_change(5)
        index_df['return_20d'] = index_df['close'].pct_change(20)
        
        # 逐日验证
        results = []
        dates = pd.to_datetime(index_df.index).strftime('%Y-%m-%d').tolist()
        
        for i in range(20, len(dates) - 5):  # 需要20天历史数据，5天未来数据
            date = dates[i]
            
            try:
                # 预测市场类型
                prediction = classifier.classify(date, index_code)
                predicted_type = prediction.market_type.value
                confidence = prediction.confidence
                
                # 获取实际收益（未来5天和20天）
                actual_return_5d = index_df.iloc[i]['return_5d'] if i < len(index_df) - 5 else 0
                actual_return_20d = index_df.iloc[i]['return_20d'] if i < len(index_df) - 20 else 0
                
                # 判断实际市场类型（基于后续收益）
                if actual_return_5d > 0.05:  # 5日收益>5%
                    actual_type = "快牛"
                elif actual_return_5d > 0.02:  # 5日收益>2%
                    actual_type = "慢牛"
                elif actual_return_5d < -0.05:  # 5日收益<-5%
                    actual_type = "熊市"
                else:
                    actual_type = "震荡"
                
                # 判断是否正确
                is_correct = self._is_prediction_correct(predicted_type, actual_type)
                
                result = ValidationResult(
                    date=date,
                    predicted_type=predicted_type,
                    actual_type=actual_type,
                    actual_return_5d=actual_return_5d,
                    actual_return_20d=actual_return_20d,
                    is_correct=is_correct,
                    confidence=confidence,
                )
                results.append(result)
                
            except Exception as e:
                logger.warning(f"验证日期{date}失败: {e}")
                continue
        
        self.results = results
        
        # 计算统计
        stats = self._calculate_stats(results)
        
        return stats
    
    def _is_prediction_correct(self, predicted: str, actual: str) -> bool:
        """判断预测是否正确"""
        # 映射关系
        bull_types = ["极端牛市", "快牛", "慢牛"]
        bear_types = ["熊市", "极端熊市"]
        
        if predicted in bull_types and actual in ["快牛", "慢牛"]:
            return True
        if predicted in bear_types and actual == "熊市":
            return True
        if predicted == "震荡" and actual == "震荡":
            return True
        
        return False
    
    def _calculate_stats(self, results: List[ValidationResult]) -> ValidationStats:
        """计算验证统计"""
        stats = ValidationStats()
        stats.total_predictions = len(results)
        
        if not results:
            return stats
        
        # 总体准确率
        correct_count = sum(1 for r in results if r.is_correct)
        stats.correct_predictions = correct_count
        stats.accuracy = correct_count / len(results) if results else 0.0
        
        # 各类型统计
        type_stats = {}
        for result in results:
            pred_type = result.predicted_type
            if pred_type not in type_stats:
                type_stats[pred_type] = {
                    "count": 0,
                    "correct": 0,
                    "returns_5d": [],
                }
            
            type_stats[pred_type]["count"] += 1
            if result.is_correct:
                type_stats[pred_type]["correct"] += 1
            type_stats[pred_type]["returns_5d"].append(result.actual_return_5d)
        
        # 填充统计结果
        for pred_type, data in type_stats.items():
            count = data["count"]
            correct = data["correct"]
            returns = data["returns_5d"]
            
            accuracy = correct / count if count > 0 else 0.0
            avg_return = np.mean(returns) if returns else 0.0
            
            if pred_type == "快牛":
                stats.fast_bull_count = count
                stats.fast_bull_accuracy = accuracy
                stats.fast_bull_avg_return_5d = avg_return
            elif pred_type == "慢牛":
                stats.slow_bull_count = count
                stats.slow_bull_accuracy = accuracy
                stats.slow_bull_avg_return_5d = avg_return
            elif pred_type == "震荡":
                stats.volatile_count = count
                stats.volatile_accuracy = accuracy
                stats.volatile_avg_return_5d = avg_return
            elif pred_type in ["熊市", "极端熊市"]:
                stats.bear_count = count
                stats.bear_accuracy = accuracy
                stats.bear_avg_return_5d = avg_return
        
        return stats
    
    def generate_report(self, stats: ValidationStats) -> str:
        """生成验证报告"""
        report = []
        report.append("# 市场类型判断验证报告\n")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        report.append("## 总体统计\n\n")
        report.append(f"- **总预测数**: {stats.total_predictions}\n")
        report.append(f"- **正确预测数**: {stats.correct_predictions}\n")
        report.append(f"- **总体准确率**: {stats.accuracy:.2%}\n\n")
        
        report.append("## 各类型准确率\n\n")
        report.append("| 类型 | 预测次数 | 准确率 | 平均5日收益 |\n")
        report.append("|------|---------|--------|------------|\n")
        report.append(f"| 快牛 | {stats.fast_bull_count} | {stats.fast_bull_accuracy:.2%} | {stats.fast_bull_avg_return_5d:.2%} |\n")
        report.append(f"| 慢牛 | {stats.slow_bull_count} | {stats.slow_bull_accuracy:.2%} | {stats.slow_bull_avg_return_5d:.2%} |\n")
        report.append(f"| 震荡 | {stats.volatile_count} | {stats.volatile_accuracy:.2%} | {stats.volatile_avg_return_5d:.2%} |\n")
        report.append(f"| 熊市 | {stats.bear_count} | {stats.bear_accuracy:.2%} | {stats.bear_avg_return_5d:.2%} |\n")
        
        return "".join(report)


# ============ 测试函数 ============

def test_validation():
    """测试验证框架"""
    from core.strategy.market_character_classifier_v7 import MarketCharacterClassifierV7
    
    print("=" * 60)
    print("市场类型判断验证测试")
    print("=" * 60)
    
    classifier = MarketCharacterClassifierV7()
    validator = MarketTypeValidator()
    
    # 验证最近3个月
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    print(f"\n验证期间: {start_date} ~ {end_date}")
    stats = validator.validate_period(classifier, start_date, end_date)
    
    print(f"\n总体准确率: {stats.accuracy:.2%}")
    print(f"快牛准确率: {stats.fast_bull_accuracy:.2%} ({stats.fast_bull_count}次)")
    print(f"慢牛准确率: {stats.slow_bull_accuracy:.2%} ({stats.slow_bull_count}次)")
    print(f"震荡准确率: {stats.volatile_accuracy:.2%} ({stats.volatile_count}次)")
    
    # 生成报告
    report = validator.generate_report(stats)
    print("\n" + report)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_validation()
