#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场状态判断系统验证
====================

目的：验证市场环境趋势判断的准确性，不涉及投资收益计算。

验证内容：
1. 趋势方向判断准确性（看涨/看跌/震荡）
2. 市场阶段识别准确性（14种阶段）
3. IBD状态判断准确性
4. 多模型一致性分析

验证方法：
- 将模型预测与实际市场走势对比
- 统计准确率、精确率、召回率
- 分析各阶段的后续走势统计特征
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import logging

# 项目路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def initialize_components():
    """初始化组件"""
    from config.config_manager import ConfigManager
    from jqdata.client import JQDataClient
    from core.trend_analyzer import TrendAnalyzer
    from core.ibd_style_analyzer import IBDStyleAnalyzer
    from core.market_regime.market_regime_detector import get_market_regime_detector
    
    config_manager = ConfigManager()
    jq_config = config_manager.get_config("jqdata_config.json")
    
    jq_client = JQDataClient()
    jq_client.authenticate(
        username=jq_config.get("username"),
        password=jq_config.get("password")
    )
    
    return {
        "jq_client": jq_client,
        "trend_analyzer": TrendAnalyzer(jq_client=jq_client),
        "ibd_analyzer": IBDStyleAnalyzer(),
        "regime_detector": get_market_regime_detector(),
    }


def get_price_data(jq_client, index_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """获取价格数据"""
    df = jq_client.get_price(
        index_code,
        start_date=start_date,
        end_date=end_date,
        frequency="daily",
        fields=["open", "high", "low", "close", "volume"]
    )
    
    if df is not None and len(df) > 0:
        # 计算不同周期的实际走势
        df["return_5d"] = df["close"].shift(-5) / df["close"] - 1   # 未来5天收益
        df["return_10d"] = df["close"].shift(-10) / df["close"] - 1  # 未来10天收益
        df["return_20d"] = df["close"].shift(-20) / df["close"] - 1  # 未来20天收益
        
        # 实际趋势方向（基于未来收益）
        df["actual_trend_5d"] = df["return_5d"].apply(
            lambda x: "up" if x > 0.02 else ("down" if x < -0.02 else "sideways") if pd.notna(x) else None
        )
        df["actual_trend_20d"] = df["return_20d"].apply(
            lambda x: "up" if x > 0.05 else ("down" if x < -0.05 else "sideways") if pd.notna(x) else None
        )
    
    return df


def generate_state_predictions(components: Dict, price_df: pd.DataFrame, index_code: str) -> List[Dict]:
    """生成状态预测"""
    predictions = []
    total = len(price_df)
    
    for i, (date, row) in enumerate(price_df.iterrows()):
        if i < 60 or i >= total - 20:  # 跳过前60天和后20天
            continue
        
        date_str = date.strftime("%Y-%m-%d")
        
        if i % 100 == 0:
            logger.info(f"处理进度: {i}/{total} ({date_str})")
        
        record = {
            "date": date_str,
            "close": row["close"],
            "actual_trend_5d": row["actual_trend_5d"],
            "actual_trend_20d": row["actual_trend_20d"],
            "return_5d": row["return_5d"],
            "return_20d": row["return_20d"],
        }
        
        # 趋势分析预测
        try:
            trend_result = components["trend_analyzer"].analyze_market(
                index_code=index_code,
                date=date_str
            )
            if trend_result:
                record["trend_score"] = trend_result.composite_score
                record["short_score"] = trend_result.short_term.score
                record["medium_score"] = trend_result.medium_term.score
                record["long_score"] = trend_result.long_term.score
                record["market_phase"] = trend_result.market_phase
                
                # 预测方向
                score = trend_result.composite_score
                if score > 20:
                    record["predicted_trend"] = "up"
                elif score < -20:
                    record["predicted_trend"] = "down"
                else:
                    record["predicted_trend"] = "sideways"
            else:
                record["trend_score"] = 0
                record["predicted_trend"] = "unknown"
                record["market_phase"] = "unknown"
        except Exception as e:
            record["trend_score"] = 0
            record["predicted_trend"] = "unknown"
            record["market_phase"] = "unknown"
        
        # IBD分析
        try:
            ibd_result = components["ibd_analyzer"].analyze(
                index_code=index_code,
                date=date_str,
                lookback_days=60
            )
            if ibd_result:
                record["ibd_status"] = ibd_result.market_status.value
                record["distribution_count"] = ibd_result.distribution_count
            else:
                record["ibd_status"] = "unknown"
        except:
            record["ibd_status"] = "unknown"
        
        predictions.append(record)
    
    return predictions


def validate_trend_direction(predictions: List[Dict]) -> Dict:
    """验证趋势方向判断准确性"""
    logger.info("\n" + "=" * 60)
    logger.info("1. 趋势方向判断准确性验证")
    logger.info("=" * 60)
    
    # 统计5天预测准确性
    correct_5d = 0
    total_5d = 0
    confusion_5d = defaultdict(lambda: defaultdict(int))
    
    for p in predictions:
        predicted = p.get("predicted_trend")
        actual = p.get("actual_trend_5d")
        
        if predicted in ["up", "down", "sideways"] and actual in ["up", "down", "sideways"]:
            total_5d += 1
            confusion_5d[predicted][actual] += 1
            if predicted == actual:
                correct_5d += 1
    
    accuracy_5d = correct_5d / total_5d if total_5d > 0 else 0
    
    # 分类准确率
    up_correct = confusion_5d["up"]["up"]
    up_total = sum(confusion_5d["up"].values())
    up_precision = up_correct / up_total if up_total > 0 else 0
    
    down_correct = confusion_5d["down"]["down"]
    down_total = sum(confusion_5d["down"].values())
    down_precision = down_correct / down_total if down_total > 0 else 0
    
    sideways_correct = confusion_5d["sideways"]["sideways"]
    sideways_total = sum(confusion_5d["sideways"].values())
    sideways_precision = sideways_correct / sideways_total if sideways_total > 0 else 0
    
    logger.info(f"\n5天趋势预测:")
    logger.info(f"  总样本数: {total_5d}")
    logger.info(f"  整体准确率: {accuracy_5d:.2%}")
    logger.info(f"  看涨预测精确率: {up_precision:.2%} ({up_correct}/{up_total})")
    logger.info(f"  看跌预测精确率: {down_precision:.2%} ({down_correct}/{down_total})")
    logger.info(f"  震荡预测精确率: {sideways_precision:.2%} ({sideways_correct}/{sideways_total})")
    
    # 混淆矩阵
    logger.info(f"\n混淆矩阵 (预测 vs 实际):")
    logger.info(f"              实际上涨  实际下跌  实际震荡")
    logger.info(f"  预测上涨:     {confusion_5d['up']['up']:4d}      {confusion_5d['up']['down']:4d}      {confusion_5d['up']['sideways']:4d}")
    logger.info(f"  预测下跌:     {confusion_5d['down']['up']:4d}      {confusion_5d['down']['down']:4d}      {confusion_5d['down']['sideways']:4d}")
    logger.info(f"  预测震荡:     {confusion_5d['sideways']['up']:4d}      {confusion_5d['sideways']['down']:4d}      {confusion_5d['sideways']['sideways']:4d}")
    
    return {
        "accuracy_5d": accuracy_5d,
        "up_precision": up_precision,
        "down_precision": down_precision,
        "sideways_precision": sideways_precision,
        "confusion_matrix": dict(confusion_5d),
    }


def validate_market_phase(predictions: List[Dict]) -> Dict:
    """验证市场阶段识别准确性"""
    logger.info("\n" + "=" * 60)
    logger.info("2. 市场阶段识别准确性验证")
    logger.info("=" * 60)
    
    # 按阶段分组统计后续走势
    phase_stats = defaultdict(lambda: {"returns": [], "count": 0})
    
    for p in predictions:
        phase = p.get("market_phase", "unknown")
        return_20d = p.get("return_20d")
        
        if phase != "unknown" and return_20d is not None and not np.isnan(return_20d):
            phase_stats[phase]["returns"].append(return_20d)
            phase_stats[phase]["count"] += 1
    
    # 计算每个阶段的统计特征
    results = {}
    logger.info(f"\n各市场阶段后续20天走势统计:")
    logger.info(f"{'阶段':<25} {'样本数':<8} {'平均收益':<10} {'中位收益':<10} {'胜率':<8} {'方向一致性':<10}")
    logger.info("-" * 80)
    
    for phase, stats in sorted(phase_stats.items(), key=lambda x: -np.mean(x[1]["returns"]) if x[1]["returns"] else 0):
        returns = stats["returns"]
        if not returns:
            continue
        
        avg_return = np.mean(returns)
        median_return = np.median(returns)
        win_rate = np.mean([r > 0 for r in returns])
        
        # 方向一致性：看涨阶段应该后续上涨，看跌阶段应该后续下跌
        is_bullish_phase = "牛市" in phase or "突破" in phase or "复苏" in phase
        is_bearish_phase = "熊市" in phase or "破位" in phase or "见顶" in phase
        
        if is_bullish_phase:
            consistency = np.mean([r > 0 for r in returns])
        elif is_bearish_phase:
            consistency = np.mean([r < 0 for r in returns])
        else:
            consistency = np.mean([abs(r) < 0.03 for r in returns])  # 震荡阶段应该小幅波动
        
        logger.info(f"{phase:<25} {stats['count']:<8} {avg_return:>+8.2%}   {median_return:>+8.2%}   {win_rate:>6.1%}   {consistency:>8.1%}")
        
        results[phase] = {
            "count": stats["count"],
            "avg_return": avg_return,
            "median_return": median_return,
            "win_rate": win_rate,
            "consistency": consistency,
        }
    
    # 计算整体有效性
    valid_phases = [p for p, s in results.items() if s["count"] >= 10]
    if valid_phases:
        avg_consistency = np.mean([results[p]["consistency"] for p in valid_phases])
        logger.info(f"\n整体阶段方向一致性: {avg_consistency:.2%}")
    
    return results


def validate_ibd_status(predictions: List[Dict]) -> Dict:
    """验证IBD状态判断准确性"""
    logger.info("\n" + "=" * 60)
    logger.info("3. IBD状态判断准确性验证")
    logger.info("=" * 60)
    
    # 按IBD状态分组
    ibd_stats = defaultdict(lambda: {"returns": [], "count": 0})
    
    for p in predictions:
        status = p.get("ibd_status", "unknown")
        return_20d = p.get("return_20d")
        
        if status != "unknown" and return_20d is not None and not np.isnan(return_20d):
            ibd_stats[status]["returns"].append(return_20d)
            ibd_stats[status]["count"] += 1
    
    results = {}
    logger.info(f"\n各IBD状态后续20天走势统计:")
    logger.info(f"{'状态':<25} {'样本数':<8} {'平均收益':<10} {'中位收益':<10} {'胜率':<8}")
    logger.info("-" * 70)
    
    # IBD状态期望
    expected_direction = {
        "confirmed_uptrend": "up",
        "uptrend_pressure": "down",
        "correction": "down",
        "rally_attempt": "up",
    }
    
    for status, stats in sorted(ibd_stats.items(), key=lambda x: -np.mean(x[1]["returns"]) if x[1]["returns"] else 0):
        returns = stats["returns"]
        if not returns:
            continue
        
        avg_return = np.mean(returns)
        median_return = np.median(returns)
        win_rate = np.mean([r > 0 for r in returns])
        
        logger.info(f"{status:<25} {stats['count']:<8} {avg_return:>+8.2%}   {median_return:>+8.2%}   {win_rate:>6.1%}")
        
        # 验证方向一致性
        expected = expected_direction.get(status)
        if expected == "up":
            consistency = win_rate
        elif expected == "down":
            consistency = 1 - win_rate
        else:
            consistency = 0.5
        
        results[status] = {
            "count": stats["count"],
            "avg_return": avg_return,
            "win_rate": win_rate,
            "consistency": consistency,
        }
    
    # 验证IBD核心逻辑
    logger.info(f"\nIBD状态有效性验证:")
    
    if "confirmed_uptrend" in results and "correction" in results:
        uptrend_return = results["confirmed_uptrend"]["avg_return"]
        correction_return = results["correction"]["avg_return"]
        
        is_valid = uptrend_return > correction_return
        logger.info(f"  确认上涨 vs 市场调整: {'✅' if is_valid else '❌'}")
        logger.info(f"    确认上涨平均收益: {uptrend_return:+.2%}")
        logger.info(f"    市场调整平均收益: {correction_return:+.2%}")
    
    return results


def validate_score_vs_return(predictions: List[Dict]) -> Dict:
    """验证趋势得分与实际收益的相关性"""
    logger.info("\n" + "=" * 60)
    logger.info("4. 趋势得分与实际收益相关性验证")
    logger.info("=" * 60)
    
    scores = []
    returns_5d = []
    returns_20d = []
    
    for p in predictions:
        score = p.get("trend_score")
        r5 = p.get("return_5d")
        r20 = p.get("return_20d")
        
        if score is not None and r5 is not None and r20 is not None:
            if not (np.isnan(score) or np.isnan(r5) or np.isnan(r20)):
                scores.append(score)
                returns_5d.append(r5)
                returns_20d.append(r20)
    
    # 计算相关系数
    if len(scores) > 10:
        corr_5d = np.corrcoef(scores, returns_5d)[0, 1]
        corr_20d = np.corrcoef(scores, returns_20d)[0, 1]
        
        logger.info(f"\n趋势得分与实际收益相关性:")
        logger.info(f"  与5天收益相关系数: {corr_5d:.4f}")
        logger.info(f"  与20天收益相关系数: {corr_20d:.4f}")
        
        # 分位数分析
        score_array = np.array(scores)
        return_20d_array = np.array(returns_20d)
        
        quantiles = [0, 20, 40, 60, 80, 100]
        logger.info(f"\n得分分位数与平均收益:")
        logger.info(f"{'得分范围':<20} {'样本数':<10} {'平均20天收益':<15}")
        logger.info("-" * 50)
        
        for i in range(len(quantiles) - 1):
            low = np.percentile(score_array, quantiles[i])
            high = np.percentile(score_array, quantiles[i + 1])
            mask = (score_array >= low) & (score_array < high)
            
            if mask.sum() > 0:
                avg_return = return_20d_array[mask].mean()
                logger.info(f"[{low:>+6.1f}, {high:>+6.1f})      {mask.sum():<10} {avg_return:>+10.2%}")
        
        return {
            "correlation_5d": corr_5d,
            "correlation_20d": corr_20d,
            "sample_count": len(scores),
        }
    
    return {}


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("市场状态判断系统验证")
    logger.info("=" * 60)
    
    # 配置
    INDEX_CODE = "000001.XSHG"
    START_DATE = "2020-01-01"
    END_DATE = "2025-12-31"
    
    logger.info(f"验证时间: {START_DATE} ~ {END_DATE}")
    logger.info(f"验证指数: {INDEX_CODE}")
    
    # 初始化
    logger.info("\n初始化组件...")
    try:
        components = initialize_components()
        logger.info("✅ 组件初始化成功")
    except Exception as e:
        logger.error(f"❌ 初始化失败: {e}")
        return
    
    # 获取价格数据
    logger.info("\n获取价格数据...")
    price_df = get_price_data(components["jq_client"], INDEX_CODE, START_DATE, END_DATE)
    if price_df is None or len(price_df) == 0:
        logger.error("❌ 获取价格数据失败")
        return
    logger.info(f"✅ 获取 {len(price_df)} 条数据")
    
    # 生成预测
    logger.info("\n生成状态预测...")
    predictions = generate_state_predictions(components, price_df, INDEX_CODE)
    logger.info(f"✅ 生成 {len(predictions)} 条预测")
    
    # 验证趋势方向
    trend_results = validate_trend_direction(predictions)
    
    # 验证市场阶段
    phase_results = validate_market_phase(predictions)
    
    # 验证IBD状态
    ibd_results = validate_ibd_status(predictions)
    
    # 验证得分相关性
    corr_results = validate_score_vs_return(predictions)
    
    # 汇总
    logger.info("\n" + "=" * 60)
    logger.info("验证结果汇总")
    logger.info("=" * 60)
    
    logger.info(f"\n1. 趋势方向判断:")
    logger.info(f"   整体准确率: {trend_results['accuracy_5d']:.2%}")
    logger.info(f"   目标: >50% (随机基准)")
    logger.info(f"   结果: {'✅ 有效' if trend_results['accuracy_5d'] > 0.50 else '❌ 无效'}")
    
    logger.info(f"\n2. 市场阶段识别:")
    if phase_results:
        avg_consistency = np.mean([s["consistency"] for s in phase_results.values() if s["count"] >= 10])
        logger.info(f"   平均方向一致性: {avg_consistency:.2%}")
        logger.info(f"   目标: >55%")
        logger.info(f"   结果: {'✅ 有效' if avg_consistency > 0.55 else '❌ 需优化'}")
    
    logger.info(f"\n3. IBD状态判断:")
    if "confirmed_uptrend" in ibd_results and "correction" in ibd_results:
        is_valid = ibd_results["confirmed_uptrend"]["avg_return"] > ibd_results["correction"]["avg_return"]
        logger.info(f"   方向区分有效性: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    logger.info(f"\n4. 得分相关性:")
    if corr_results:
        corr = corr_results.get("correlation_20d", 0)
        logger.info(f"   得分与20天收益相关性: {corr:.4f}")
        logger.info(f"   目标: >0.1 (正相关)")
        logger.info(f"   结果: {'✅ 有效' if corr > 0.1 else '⚠️ 相关性较弱'}")
    
    logger.info("\nauth success ")


if __name__ == "__main__":
    main()

