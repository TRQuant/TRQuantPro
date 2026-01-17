#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HMM V3.0 回测验证与递归优化
===========================

功能：
1. 历史回测验证（2019-2024）
2. 计算预测准确率
3. 递归优化参数到高置信度
4. 对比原版HMM

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
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


# ============== 配置 ==============

# 验证时间段
VALIDATION_PERIODS = [
    {"name": "2019", "start": "2019-01-01", "end": "2019-12-31"},
    {"name": "2020", "start": "2020-01-01", "end": "2020-12-31"},
    {"name": "2021", "start": "2021-01-01", "end": "2021-12-31"},
    {"name": "2022", "start": "2022-01-01", "end": "2022-12-31"},
    {"name": "2023", "start": "2023-01-01", "end": "2023-12-31"},
    {"name": "2024", "start": "2024-01-01", "end": "2024-12-31"},
]

# 采样频率（每N天验证一次）
SAMPLE_FREQUENCY = 5


# ============== 验证函数 ==============

def get_actual_market_type(df: pd.DataFrame, idx: int, horizon: int = 5) -> str:
    """
    根据未来收益判断实际市场类型
    
    Args:
        df: 价格数据
        idx: 当前索引
        horizon: 预测窗口（天）
        
    Returns:
        实际市场类型: 牛市/震荡/熊市
    """
    if idx + horizon >= len(df):
        return "震荡"
    
    current_price = df['close'].iloc[idx]
    future_price = df['close'].iloc[idx + horizon]
    future_return = (future_price / current_price - 1) * 100
    
    # 优化阈值：与HMM参数一致
    if future_return > 1.5:  # 5天涨>1.5%
        return "牛市"
    elif future_return < -1.5:  # 5天跌>1.5%
        return "熊市"
    else:
        return "震荡"


def validate_hmm(hmm, df: pd.DataFrame, start_idx: int = 60, sample_freq: int = 5) -> Dict[str, Any]:
    """
    验证HMM预测准确率
    
    Args:
        hmm: HMM模型
        df: 完整价格数据
        start_idx: 开始验证的索引（需要历史数据）
        sample_freq: 采样频率
        
    Returns:
        验证统计
    """
    results = []
    
    for i in range(start_idx, len(df) - 10, sample_freq):
        # 获取历史数据进行预测
        hist_df = df.iloc[:i+1].copy()
        
        try:
            result = hmm.analyze(hist_df)
            if result is None:
                continue
            
            predicted = result.current_state.value
            actual = get_actual_market_type(df, i, horizon=5)
            
            results.append({
                "date": df.index[i],
                "predicted": predicted,
                "actual": actual,
                "confidence": result.confidence,
                "is_correct": predicted == actual,
            })
        except Exception as e:
            continue
    
    if not results:
        return {"error": "无有效验证结果"}
    
    # 统计
    total = len(results)
    correct = sum(1 for r in results if r["is_correct"])
    accuracy = correct / total
    
    # 各类型统计
    type_stats = {}
    for market_type in ["牛市", "震荡", "熊市"]:
        type_results = [r for r in results if r["predicted"] == market_type]
        type_correct = sum(1 for r in type_results if r["is_correct"])
        type_count = len(type_results)
        type_accuracy = type_correct / type_count if type_count > 0 else 0
        
        type_stats[market_type] = {
            "count": type_count,
            "correct": type_correct,
            "accuracy": type_accuracy,
        }
    
    return {
        "total_predictions": total,
        "correct_predictions": correct,
        "accuracy": accuracy,
        "type_stats": type_stats,
        "avg_confidence": np.mean([r["confidence"] for r in results]),
    }


def validate_period(hmm, start_date: str, end_date: str, index_code: str = "000300.XSHG") -> Dict[str, Any]:
    """验证指定时间段"""
    try:
        df = jq.get_price(
            index_code,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'high', 'low', 'close', 'volume']
        )
        
        if df is None or len(df) < 100:
            return {"error": "数据不足"}
        
        return validate_hmm(hmm, df, start_idx=60, sample_freq=SAMPLE_FREQUENCY)
        
    except Exception as e:
        return {"error": str(e)}


# ============== 主函数 ==============

def main():
    """主函数"""
    print("=" * 70)
    print("HMM V3.0 回测验证与对比")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 导入HMM模型
    from core.hmm_optimized import OptimizedHMM
    from core.trend_ml import SimpleHMM
    
    hmm_v3 = OptimizedHMM(enable_dynamic_transition=True)
    hmm_old = SimpleHMM(use_astock_params=True)
    
    # 验证结果
    results_v3 = []
    results_old = []
    
    for period in VALIDATION_PERIODS:
        print(f"\n验证 {period['name']}:")
        
        # V3
        start_time = time.time()
        result_v3 = validate_period(hmm_v3, period['start'], period['end'])
        elapsed_v3 = time.time() - start_time
        
        # 原版
        start_time = time.time()
        result_old = validate_period(hmm_old, period['start'], period['end'])
        elapsed_old = time.time() - start_time
        
        if "error" not in result_v3:
            result_v3["period"] = period['name']
            result_v3["elapsed"] = elapsed_v3
            results_v3.append(result_v3)
            print(f"  V3准确率: {result_v3['accuracy']:.2%} (耗时: {elapsed_v3:.1f}s)")
        else:
            print(f"  V3: ❌ {result_v3['error']}")
        
        if "error" not in result_old:
            result_old["period"] = period['name']
            result_old["elapsed"] = elapsed_old
            results_old.append(result_old)
            print(f"  原版准确率: {result_old['accuracy']:.2%} (耗时: {elapsed_old:.1f}s)")
        else:
            print(f"  原版: ❌ {result_old['error']}")
    
    # 汇总
    print("\n" + "=" * 70)
    print("验证结果汇总")
    print("=" * 70)
    
    if results_v3:
        print("\n【优化版HMM V3.0】")
        print("-" * 50)
        
        total_v3 = sum(r["total_predictions"] for r in results_v3)
        correct_v3 = sum(r["correct_predictions"] for r in results_v3)
        overall_acc_v3 = correct_v3 / total_v3 if total_v3 > 0 else 0
        avg_conf_v3 = np.mean([r["avg_confidence"] for r in results_v3])
        
        print(f"总体准确率: {overall_acc_v3:.2%}")
        print(f"平均置信度: {avg_conf_v3:.2%}")
        print(f"总预测数: {total_v3}")
        
        print("\n各年度准确率:")
        for r in results_v3:
            print(f"  {r['period']}: {r['accuracy']:.2%}")
        
        # 各类型统计
        print("\n各类型准确率:")
        for market_type in ["牛市", "震荡", "熊市"]:
            type_count = sum(r["type_stats"].get(market_type, {}).get("count", 0) for r in results_v3)
            type_correct = sum(r["type_stats"].get(market_type, {}).get("correct", 0) for r in results_v3)
            type_acc = type_correct / type_count if type_count > 0 else 0
            print(f"  {market_type}: {type_acc:.2%} ({type_correct}/{type_count})")
    
    if results_old:
        print("\n【原版SimpleHMM】")
        print("-" * 50)
        
        total_old = sum(r["total_predictions"] for r in results_old)
        correct_old = sum(r["correct_predictions"] for r in results_old)
        overall_acc_old = correct_old / total_old if total_old > 0 else 0
        avg_conf_old = np.mean([r["avg_confidence"] for r in results_old])
        
        print(f"总体准确率: {overall_acc_old:.2%}")
        print(f"平均置信度: {avg_conf_old:.2%}")
        print(f"总预测数: {total_old}")
        
        print("\n各年度准确率:")
        for r in results_old:
            print(f"  {r['period']}: {r['accuracy']:.2%}")
        
        # 各类型统计
        print("\n各类型准确率:")
        for market_type in ["牛市", "震荡", "熊市"]:
            type_count = sum(r["type_stats"].get(market_type, {}).get("count", 0) for r in results_old)
            type_correct = sum(r["type_stats"].get(market_type, {}).get("correct", 0) for r in results_old)
            type_acc = type_correct / type_count if type_count > 0 else 0
            print(f"  {market_type}: {type_acc:.2%} ({type_correct}/{type_count})")
    
    # 对比
    if results_v3 and results_old:
        print("\n" + "=" * 70)
        print("【对比总结】")
        print("=" * 70)
        
        improvement = overall_acc_v3 - overall_acc_old
        print(f"V3 vs 原版: {overall_acc_v3:.2%} vs {overall_acc_old:.2%}")
        print(f"准确率提升: {improvement:+.2%}")
        
        if improvement > 0:
            print(f"✅ 优化版HMM V3准确率更高!")
        else:
            print(f"⚠️ 需要进一步优化参数")
    
    # 保存报告
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/hmm_validation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"hmm_v3_validation_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# HMM V3.0 回测验证报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if results_v3:
            f.write("## 优化版HMM V3.0\n\n")
            f.write(f"- **总体准确率**: {overall_acc_v3:.2%}\n")
            f.write(f"- **平均置信度**: {avg_conf_v3:.2%}\n")
            f.write(f"- **总预测数**: {total_v3}\n\n")
            
            f.write("### 各年度准确率\n\n")
            f.write("| 年度 | 准确率 | 预测数 |\n")
            f.write("|------|--------|--------|\n")
            for r in results_v3:
                f.write(f"| {r['period']} | {r['accuracy']:.2%} | {r['total_predictions']} |\n")
        
        if results_old:
            f.write("\n## 原版SimpleHMM\n\n")
            f.write(f"- **总体准确率**: {overall_acc_old:.2%}\n")
            f.write(f"- **平均置信度**: {avg_conf_old:.2%}\n")
            f.write(f"- **总预测数**: {total_old}\n\n")
        
        if results_v3 and results_old:
            f.write("\n## 对比总结\n\n")
            f.write(f"- V3准确率: {overall_acc_v3:.2%}\n")
            f.write(f"- 原版准确率: {overall_acc_old:.2%}\n")
            f.write(f"- 准确率提升: {improvement:+.2%}\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
