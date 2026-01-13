#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试集成模型
================

测试集成模型是否能正常工作，不进行完整验证。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

from core.ensemble_market_trend import EnsembleMarketTrendAnalyzer
from datetime import datetime, timedelta

def main():
    """快速测试"""
    print("=" * 80)
    print("快速测试集成模型")
    print("=" * 80)
    
    # 初始化分析器
    analyzer = EnsembleMarketTrendAnalyzer()
    
    # 测试日期（最近一个交易日）
    test_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"\n测试日期: {test_date}")
    print(f"指数: 000300.XSHG (沪深300)\n")
    
    # 执行分析
    try:
        result = analyzer.analyze("000300.XSHG", test_date)
        
        print("=" * 80)
        print("集成分析结果")
        print("=" * 80)
        print(result.summary())
        print("\n各模型预测:")
        for pred in result.model_predictions:
            print(f"  - {pred.model_name}: {pred.trend.value} (置信度: {pred.confidence:.1%})")
        
        print(f"\n投票得分:")
        print(f"  牛市: {result.bull_score:.2f}")
        print(f"  熊市: {result.bear_score:.2f}")
        print(f"  震荡: {result.sideways_score:.2f}")
        
        print(f"\n模型权重:")
        for name, weight in result.weights.items():
            if weight > 0:
                print(f"  - {name}: {weight:.1%}")
        
        print("\n" + "=" * 80)
        print("✅ 集成模型测试通过")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
