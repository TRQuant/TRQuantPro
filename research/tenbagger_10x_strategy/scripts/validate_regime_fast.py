#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场环境判断快速验证（分批测试，显示进度）
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import logging
from datetime import datetime
from core.market_regime.comprehensive_regime_detector import (
    ComprehensiveRegimeDetector, MarketRegime
)

logging.basicConfig(level=logging.ERROR)  # 减少日志输出

# 关键测试节点（分批）
TEST_CASES = [
    ("2022-04-27", MarketRegime.BEAR, "4月底熊市低点"),
    ("2023-12-28", MarketRegime.VOLATILE, "年末震荡"),
    ("2024-02-05", MarketRegime.BEAR, "2月初恐慌低点"),
    ("2024-09-24", MarketRegime.BULL, "924行情启动"),
]

def test_batch(detector, cases):
    """测试一批案例"""
    results = []
    print(f"\n📊 测试 {len(cases)} 个案例...")
    
    for i, (date, expected, desc) in enumerate(cases, 1):
        try:
            print(f"  [{i}/{len(cases)}] {date} - {desc}", end=" ... ", flush=True)
            result = detector.detect(date)
            
            is_correct = result.regime == expected
            status = "✓" if is_correct else "✗"
            
            print(f"{status} 检测:{result.regime.value:12} 得分:{result.composite_score:+6.1f}")
            
            results.append({
                'date': date,
                'expected': expected.value,
                'detected': result.regime.value,
                'score': result.composite_score,
                'is_correct': is_correct,
            })
        except Exception as e:
            print(f"✗ 错误: {e}")
            results.append({'date': date, 'is_correct': False})
    
    return results

def main():
    print("="*60)
    print("市场环境判断快速验证（优化版）")
    print("="*60)
    
    detector = ComprehensiveRegimeDetector()
    
    # 分批测试
    results = test_batch(detector, TEST_CASES)
    
    # 统计
    correct = sum(1 for r in results if r.get('is_correct', False))
    total = len(results)
    
    print("\n" + "="*60)
    print(f"快速验证结果: {correct}/{total} = {correct/total*100:.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()
