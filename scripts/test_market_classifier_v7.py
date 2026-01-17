#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试MarketCharacterClassifierV7改进效果
========================================

对比V6和V7在最近一个月的判断结果

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def test_v6_vs_v7():
    """对比V6和V7的判断结果"""
    print("=" * 70)
    print("市场类型判断 V6 vs V7 对比测试")
    print("=" * 70)
    
    # 测试日期：最近一个月
    test_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n测试日期: {test_date}")
    print(f"实际表现: 近一个月收益43.74%，周收益10.02%")
    print(f"预期判断: 快牛 → 激进模式")
    print()
    
    # V6判断
    print("-" * 70)
    print("V6判断结果:")
    print("-" * 70)
    try:
        from core.strategy.market_character_classifier_v6 import MarketCharacterClassifierV6
        v6_classifier = MarketCharacterClassifierV6()
        v6_result = v6_classifier.classify(test_date)
        
        print(f"  市场类型: {v6_result.market_type.value}")
        print(f"  策略模式: {v6_result.strategy_mode.value}")
        print(f"  趋势得分: {v6_result.trend_score:.1f}")
        print(f"  快速牛市信号: {v6_result.is_rapid_bull_signal}")
        print(f"  置信度: {v6_result.confidence:.0%}")
        
        if v6_result.market_type.value in ["快牛", "极端牛市"]:
            print("  ✅ V6正确识别为牛市")
        else:
            print(f"  ❌ V6误判为 {v6_result.market_type.value}")
    except Exception as e:
        print(f"  ❌ V6测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # V7判断
    print("-" * 70)
    print("V7判断结果:")
    print("-" * 70)
    try:
        from core.strategy.market_character_classifier_v7 import MarketCharacterClassifierV7
        v7_classifier = MarketCharacterClassifierV7()
        v7_result = v7_classifier.classify(test_date)
        
        print(f"  市场类型: {v7_result.market_type.value}")
        print(f"  策略模式: {v7_result.strategy_mode.value}")
        print(f"  趋势得分: {v7_result.trend_score:.1f}")
        print(f"  快速牛市信号: {v7_result.is_rapid_bull_signal}")
        print(f"  置信度: {v7_result.confidence:.0%}")
        
        if v7_result.market_type.value in ["快牛", "极端牛市"]:
            print("  ✅ V7正确识别为牛市")
        else:
            print(f"  ❌ V7误判为 {v7_result.market_type.value}")
    except Exception as e:
        print(f"  ❌ V7测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print("对比完成")
    print("=" * 70)


if __name__ == "__main__":
    test_v6_vs_v7()
