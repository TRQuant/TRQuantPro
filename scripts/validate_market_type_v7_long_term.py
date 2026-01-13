#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场类型判断 V7 长期回测验证
============================

使用5年历史数据验证V7准确率（2019-2024）

功能:
1. 5年历史数据回测（2019-2024）
2. 准确率统计（总体、各类型）
3. 参数优化建议
4. 性能优化（批量处理、缓存）

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# JQData认证
import jqdatasdk as jq
with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
    config = json.load(f)
jq.auth(config['username'], config['password'])
logger.info("✅ JQData认证成功")


# ============== 验证配置 ==============

# 验证时间段（5年：2019-2024）
VALIDATION_PERIODS = [
    {
        "name": "2019-2020",
        "start_date": "2019-01-01",
        "end_date": "2020-12-31",
    },
    {
        "name": "2021-2022",
        "start_date": "2021-01-01",
        "end_date": "2022-12-31",
    },
    {
        "name": "2023-2024",
        "start_date": "2023-01-01",
        "end_date": "2024-12-31",
    },
]

# 采样频率（每N个交易日验证一次，提高性能）
SAMPLE_FREQUENCY = 5  # 每5个交易日验证一次


# ============== 验证函数 ==============

def validate_period(
    classifier,
    start_date: str,
    end_date: str,
    index_code: str = "000300.XSHG",
    sample_freq: int = 5,
) -> Dict[str, Any]:
    """
    验证指定时间段的市场类型判断
    
    Args:
        classifier: 市场类型分类器（V7）
        start_date: 开始日期
        end_date: 结束日期
        index_code: 指数代码
        sample_freq: 采样频率（每N个交易日验证一次）
    
    Returns:
        验证结果字典
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"验证期间: {start_date} ~ {end_date}")
    logger.info(f"{'='*60}")
    
    # 获取指数数据
    try:
        index_df = jq.get_price(
            index_code,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
        )
    except Exception as e:
        logger.error(f"获取数据失败: {e}")
        return {"error": str(e)}
    
    if index_df is None or len(index_df) < 25:
        logger.warning("数据不足，无法验证")
        return {"error": "数据不足"}
    
    # 计算实际收益（用于判断实际市场类型）
    index_df['return_5d'] = index_df['close'].pct_change(5)
    index_df['return_20d'] = index_df['close'].pct_change(20)
    
    # 逐日验证（采样）
    results = []
    dates = pd.to_datetime(index_df.index).strftime('%Y-%m-%d').tolist()
    
    total_days = len(dates)
    validated_days = 0
    
    logger.info(f"总交易日: {total_days}, 采样频率: 每{sample_freq}天")
    
    for i in range(20, len(dates) - 5, sample_freq):  # 需要20天历史数据，5天未来数据
        date = dates[i]
        validated_days += 1
        
        if validated_days % 50 == 0:
            logger.info(f"  进度: {validated_days}/{len(range(20, len(dates)-5, sample_freq))} ({validated_days*100//len(range(20, len(dates)-5, sample_freq))}%)")
        
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
            is_correct = is_prediction_correct(predicted_type, actual_type)
            
            results.append({
                "date": date,
                "predicted_type": predicted_type,
                "actual_type": actual_type,
                "actual_return_5d": actual_return_5d,
                "actual_return_20d": actual_return_20d,
                "is_correct": is_correct,
                "confidence": confidence,
            })
            
        except Exception as e:
            logger.warning(f"验证日期{date}失败: {e}")
            continue
    
    # 计算统计
    stats = calculate_stats(results)
    stats["total_days"] = total_days
    stats["validated_days"] = validated_days
    
    return stats


def is_prediction_correct(predicted: str, actual: str) -> bool:
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


def calculate_stats(results: List[Dict]) -> Dict[str, Any]:
    """计算验证统计"""
    if not results:
        return {
            "total_predictions": 0,
            "accuracy": 0.0,
            "fast_bull_accuracy": 0.0,
            "slow_bull_accuracy": 0.0,
            "volatile_accuracy": 0.0,
            "bear_accuracy": 0.0,
        }
    
    total = len(results)
    correct = sum(1 for r in results if r["is_correct"])
    accuracy = correct / total if total > 0 else 0.0
    
    # 各类型统计
    type_stats = {}
    for result in results:
        pred_type = result["predicted_type"]
        if pred_type not in type_stats:
            type_stats[pred_type] = {
                "count": 0,
                "correct": 0,
                "returns_5d": [],
            }
        
        type_stats[pred_type]["count"] += 1
        if result["is_correct"]:
            type_stats[pred_type]["correct"] += 1
        type_stats[pred_type]["returns_5d"].append(result["actual_return_5d"])
    
    # 填充统计结果
    stats = {
        "total_predictions": total,
        "correct_predictions": correct,
        "accuracy": accuracy,
        "fast_bull_count": 0,
        "fast_bull_accuracy": 0.0,
        "fast_bull_avg_return_5d": 0.0,
        "slow_bull_count": 0,
        "slow_bull_accuracy": 0.0,
        "slow_bull_avg_return_5d": 0.0,
        "volatile_count": 0,
        "volatile_accuracy": 0.0,
        "volatile_avg_return_5d": 0.0,
        "bear_count": 0,
        "bear_accuracy": 0.0,
        "bear_avg_return_5d": 0.0,
    }
    
    for pred_type, data in type_stats.items():
        count = data["count"]
        correct = data["correct"]
        returns = data["returns_5d"]
        
        type_accuracy = correct / count if count > 0 else 0.0
        avg_return = np.mean(returns) if returns else 0.0
        
        if pred_type == "快牛":
            stats["fast_bull_count"] = count
            stats["fast_bull_accuracy"] = type_accuracy
            stats["fast_bull_avg_return_5d"] = avg_return
        elif pred_type == "慢牛":
            stats["slow_bull_count"] = count
            stats["slow_bull_accuracy"] = type_accuracy
            stats["slow_bull_avg_return_5d"] = avg_return
        elif pred_type == "震荡":
            stats["volatile_count"] = count
            stats["volatile_accuracy"] = type_accuracy
            stats["volatile_avg_return_5d"] = avg_return
        elif pred_type in ["熊市", "极端熊市"]:
            stats["bear_count"] = count
            stats["bear_accuracy"] = type_accuracy
            stats["bear_avg_return_5d"] = avg_return
    
    return stats


# ============== 参数优化 ==============

def optimize_parameters(
    validation_results: List[Dict],
    base_thresholds: Dict[str, float],
) -> Dict[str, float]:
    """
    根据验证结果优化参数
    
    Args:
        validation_results: 验证结果列表
        base_thresholds: 基础阈值
    
    Returns:
        优化后的阈值
    """
    logger.info("\n" + "="*60)
    logger.info("参数优化分析")
    logger.info("="*60)
    
    optimized = base_thresholds.copy()
    
    # 分析各类型准确率
    for result in validation_results:
        fast_bull_acc = result.get("fast_bull_accuracy", 0)
        slow_bull_acc = result.get("slow_bull_accuracy", 0)
        volatile_acc = result.get("volatile_accuracy", 0)
        
        # 如果快牛准确率<70%，提高阈值
        if fast_bull_acc < 0.7 and fast_bull_acc > 0:
            optimized["trend_score_fast_bull"] *= 1.1
            logger.info(f"  快牛准确率{fast_bull_acc:.2%} < 70%，提高快牛阈值10%")
        
        # 如果慢牛准确率<70%，提高阈值
        if slow_bull_acc < 0.7 and slow_bull_acc > 0:
            optimized["trend_score_slow_bull"] *= 1.1
            logger.info(f"  慢牛准确率{slow_bull_acc:.2%} < 70%，提高慢牛阈值10%")
        
        # 如果震荡准确率<75%，降低阈值（减少误判）
        if volatile_acc < 0.75 and volatile_acc > 0:
            optimized["trend_score_slow_bull"] *= 0.95
            logger.info(f"  震荡准确率{volatile_acc:.2%} < 75%，降低慢牛阈值5%")
    
    return optimized


# ============== 主函数 ==============

def main():
    """主函数"""
    print("="*70)
    print("市场类型判断 V7 长期回测验证（5年：2019-2024）")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化V7分类器
    from core.strategy.market_character_classifier_v7 import MarketCharacterClassifierV7
    classifier = MarketCharacterClassifierV7(enable_validation=True)
    
    # 验证各时间段
    all_results = []
    
    for i, period in enumerate(VALIDATION_PERIODS, 1):
        print(f"\n[{i}/{len(VALIDATION_PERIODS)}] {period['name']}")
        
        start_time = time.time()
        result = validate_period(
            classifier=classifier,
            start_date=period['start_date'],
            end_date=period['end_date'],
            sample_freq=SAMPLE_FREQUENCY,
        )
        elapsed = time.time() - start_time
        
        if "error" not in result:
            result["period_name"] = period['name']
            result["elapsed_time"] = elapsed
            all_results.append(result)
            
            print(f"  准确率: {result['accuracy']:.2%}")
            print(f"  耗时: {elapsed:.1f}s")
        else:
            print(f"  ❌ 验证失败: {result['error']}")
    
    # 汇总统计
    print("\n" + "="*70)
    print("验证结果汇总")
    print("="*70)
    
    if not all_results:
        print("❌ 无有效验证结果")
        return
    
    # 总体统计
    total_predictions = sum(r["total_predictions"] for r in all_results)
    total_correct = sum(r["correct_predictions"] for r in all_results)
    overall_accuracy = total_correct / total_predictions if total_predictions > 0 else 0.0
    
    print(f"\n总体统计:")
    print(f"  总预测数: {total_predictions}")
    print(f"  正确预测数: {total_correct}")
    print(f"  总体准确率: {overall_accuracy:.2%}")
    
    # 各类型统计
    print(f"\n各类型准确率:")
    print(f"  | 类型 | 预测次数 | 准确率 | 平均5日收益 |")
    print(f"  |------|---------|--------|------------|")
    
    type_totals = {
        "fast_bull": {"count": 0, "correct": 0, "returns": []},
        "slow_bull": {"count": 0, "correct": 0, "returns": []},
        "volatile": {"count": 0, "correct": 0, "returns": []},
        "bear": {"count": 0, "correct": 0, "returns": []},
    }
    
    for result in all_results:
        if result.get("fast_bull_count", 0) > 0:
            type_totals["fast_bull"]["count"] += result["fast_bull_count"]
            type_totals["fast_bull"]["correct"] += int(result["fast_bull_accuracy"] * result["fast_bull_count"])
        if result.get("slow_bull_count", 0) > 0:
            type_totals["slow_bull"]["count"] += result["slow_bull_count"]
            type_totals["slow_bull"]["correct"] += int(result["slow_bull_accuracy"] * result["slow_bull_count"])
        if result.get("volatile_count", 0) > 0:
            type_totals["volatile"]["count"] += result["volatile_count"]
            type_totals["volatile"]["correct"] += int(result["volatile_accuracy"] * result["volatile_count"])
        if result.get("bear_count", 0) > 0:
            type_totals["bear"]["count"] += result["bear_count"]
            type_totals["bear"]["correct"] += int(result["bear_accuracy"] * result["bear_count"])
    
    for type_name, data in type_totals.items():
        count = data["count"]
        correct = data["correct"]
        accuracy = correct / count if count > 0 else 0.0
        
        type_display = {
            "fast_bull": "快牛",
            "slow_bull": "慢牛",
            "volatile": "震荡",
            "bear": "熊市",
        }[type_name]
        
        print(f"  | {type_display} | {count} | {accuracy:.2%} | - |")
    
    # 参数优化建议
    optimized_thresholds = optimize_parameters(
        all_results,
        classifier.base_thresholds,
    )
    
    print(f"\n参数优化建议:")
    print(f"  原始阈值: {classifier.base_thresholds}")
    print(f"  优化阈值: {optimized_thresholds}")
    
    # 保存报告
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/market_type_validation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"validation_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 市场类型判断 V7 长期回测验证报告（5年：2019-2024）\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**验证时间段**: 2019-2024（5年）\n\n")
        
        f.write("## 总体统计\n\n")
        f.write(f"- **总预测数**: {total_predictions}\n")
        f.write(f"- **正确预测数**: {total_correct}\n")
        f.write(f"- **总体准确率**: {overall_accuracy:.2%}\n\n")
        
        f.write("## 各类型准确率\n\n")
        f.write("| 类型 | 预测次数 | 准确率 |\n")
        f.write("|------|---------|--------|\n")
        for type_name, data in type_totals.items():
            count = data["count"]
            correct = data["correct"]
            accuracy = correct / count if count > 0 else 0.0
            type_display = {
                "fast_bull": "快牛",
                "slow_bull": "慢牛",
                "volatile": "震荡",
                "bear": "熊市",
            }[type_name]
            f.write(f"| {type_display} | {count} | {accuracy:.2%} |\n")
        
        f.write("\n## 参数优化建议\n\n")
        f.write(f"**原始阈值**: {classifier.base_thresholds}\n\n")
        f.write(f"**优化阈值**: {optimized_thresholds}\n\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
