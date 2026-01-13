#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速验证脚本（最近3个月）
==========================

用于快速测试验证框架，而不是完整的10年验证

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

# 修改验证时间段为最近3个月
VALIDATION_PERIODS = [
    {
        "name": "最近3个月",
        "start_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d"),
    },
]

# 增加采样频率（每10个交易日验证一次）
SAMPLE_FREQUENCY = 10

# 导入主验证脚本的其他部分
from scripts.validate_market_type_v7_long_term import (
    validate_period,
    calculate_stats,
    is_prediction_correct,
    optimize_parameters,
)

def main():
    """主函数（快速版本）"""
    print("="*70)
    print("市场类型判断 V7 快速验证（最近3个月）")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化V7分类器
    from core.strategy.market_character_classifier_v7 import MarketCharacterClassifierV7
    classifier = MarketCharacterClassifierV7(enable_validation=True)
    
    # 验证时间段
    all_results = []
    
    for i, period in enumerate(VALIDATION_PERIODS, 1):
        print(f"\n[{i}/{len(VALIDATION_PERIODS)}] {period['name']}")
        
        import time
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
    
    # 保存报告
    from pathlib import Path
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/market_type_validation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"validation_report_quick_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 市场类型判断 V7 快速验证报告（最近3个月）\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**总体准确率**: {overall_accuracy:.2%}\n\n")
        f.write(f"**总预测数**: {total_predictions}\n\n")
        f.write(f"**正确预测数**: {total_correct}\n\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
