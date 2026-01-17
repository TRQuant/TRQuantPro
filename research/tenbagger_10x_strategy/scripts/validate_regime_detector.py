#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场环境判断准确性验证
=====================

通过历史数据验证市场环境判断的准确性：
1. 选取2022-2024年的关键时间点
2. 检测当时的市场环境
3. 与实际走势对比
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

from core.market_regime.comprehensive_regime_detector import (
    ComprehensiveRegimeDetector, MarketRegime
)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


# 历史关键节点（已知的市场环境）
KNOWN_REGIMES = [
    # (日期, 预期环境, 描述, 之后30日涨跌幅)
    ("2022-01-05", MarketRegime.DISTRIBUTION, "2022年初顶部", -10),
    ("2022-04-27", MarketRegime.BEAR, "4月底熊市低点", 15),
    ("2022-07-05", MarketRegime.RECOVERY, "7月初反弹", -5),
    ("2022-10-31", MarketRegime.BEAR, "10月底再探底", 10),
    ("2023-01-30", MarketRegime.BULL, "2023年初反弹", 5),
    ("2023-05-08", MarketRegime.VOLATILE, "5月震荡调整", -3),
    ("2023-08-28", MarketRegime.BEAR, "8月底探底", 5),
    ("2023-12-28", MarketRegime.VOLATILE, "年末震荡", -5),
    ("2024-02-05", MarketRegime.BEAR, "2月初恐慌低点", 15),
    ("2024-05-20", MarketRegime.RECOVERY, "5月企稳反弹", 3),
    ("2024-09-24", MarketRegime.BULL, "924行情启动", 25),
    ("2024-10-08", MarketRegime.DISTRIBUTION, "10月高点派发", -10),
]


def validate_regime_detection():
    """验证市场环境判断准确性"""
    
    detector = ComprehensiveRegimeDetector()
    
    results = []
    
    print("="*80)
    print("市场环境判断准确性验证")
    print("="*80)
    print()
    
    for date_str, expected_regime, description, future_return in KNOWN_REGIMES:
        print(f"检测日期: {date_str} - {description}")
        
        try:
            result = detector.detect(date_str)
            detected = result.regime
            
            # 判断是否正确
            # 完全匹配或相近匹配（如BEAR和RECOVERY都是底部附近）
            is_correct = False
            is_close = False
            
            if detected == expected_regime:
                is_correct = True
            elif (detected in [MarketRegime.BEAR, MarketRegime.RECOVERY] and 
                  expected_regime in [MarketRegime.BEAR, MarketRegime.RECOVERY]):
                is_close = True
            elif (detected in [MarketRegime.BULL, MarketRegime.DISTRIBUTION] and
                  expected_regime in [MarketRegime.BULL, MarketRegime.DISTRIBUTION]):
                is_close = True
            
            # 验证与未来走势的一致性
            future_consistent = False
            if future_return > 5:  # 上涨
                if detected in [MarketRegime.BULL, MarketRegime.RECOVERY]:
                    future_consistent = True
            elif future_return < -5:  # 下跌
                if detected in [MarketRegime.BEAR, MarketRegime.DISTRIBUTION]:
                    future_consistent = True
            else:  # 震荡
                if detected == MarketRegime.VOLATILE:
                    future_consistent = True
            
            status = "✓ 正确" if is_correct else ("~ 接近" if is_close else "✗ 偏差")
            future_status = "✓" if future_consistent else "✗"
            
            print(f"  预期: {expected_regime.value:12} | 检测: {detected.value:12} | "
                  f"得分: {result.composite_score:+6.1f} | 置信度: {result.confidence:.0f}% | "
                  f"{status} | 未来{future_return:+d}% {future_status}")
            
            results.append({
                'date': date_str,
                'expected': expected_regime.value,
                'detected': detected.value,
                'score': result.composite_score,
                'confidence': result.confidence,
                'is_correct': is_correct,
                'is_close': is_close,
                'future_consistent': future_consistent,
            })
            
        except Exception as e:
            print(f"  错误: {e}")
            results.append({
                'date': date_str,
                'expected': expected_regime.value,
                'detected': 'ERROR',
                'score': 0,
                'confidence': 0,
                'is_correct': False,
                'is_close': False,
                'future_consistent': False,
            })
        
        print()
    
    # 统计
    print("="*80)
    print("验证统计")
    print("="*80)
    
    total = len(results)
    correct = sum(1 for r in results if r['is_correct'])
    close = sum(1 for r in results if r['is_close'])
    future_ok = sum(1 for r in results if r['future_consistent'])
    
    print(f"总样本: {total}")
    print(f"完全正确: {correct} ({correct/total*100:.1f}%)")
    print(f"接近正确: {close} ({close/total*100:.1f}%)")
    print(f"综合准确率: {(correct+close)/total*100:.1f}%")
    print(f"未来走势一致: {future_ok} ({future_ok/total*100:.1f}%)")
    
    return results


if __name__ == "__main__":
    results = validate_regime_detection()
