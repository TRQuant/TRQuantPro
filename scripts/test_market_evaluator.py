#!/usr/bin/env python3
"""
测试市场趋势环境综合评估模块
=============================
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_imports():
    """测试模块导入"""
    print("\n" + "="*60)
    print("1. 测试模块导入")
    print("="*60)
    
    try:
        from core.market_environment_evaluator import (
            MarketEnvironmentEvaluator,
            get_market_environment_evaluator,
            EvaluationResult
        )
        print("✅ market_environment_evaluator 导入成功")
    except Exception as e:
        print(f"❌ market_environment_evaluator 导入失败: {e}")
        return False
    
    try:
        from core.dynamic_signals import (
            DynamicSignalProvider,
            get_dynamic_signal_provider,
            DynamicSignals,
            trend_score,
            market_regime,
            reversal_signal,
            suggested_position_ratio,
            allocation_style_shift,
            risk_exposure_score,
            volatility_regime,
            trade_frequency_suggestion
        )
        print("✅ dynamic_signals 导入成功")
    except Exception as e:
        print(f"❌ dynamic_signals 导入失败: {e}")
        return False
    
    try:
        from core.signal_fusion import (
            SignalFusion,
            get_signal_fusion,
            FusionMethod,
            ModelWeight,
            FusionResult
        )
        print("✅ signal_fusion 导入成功")
    except Exception as e:
        print(f"❌ signal_fusion 导入失败: {e}")
        return False
    
    return True


def test_evaluator_init():
    """测试评估器初始化"""
    print("\n" + "="*60)
    print("2. 测试评估器初始化")
    print("="*60)
    
    try:
        from core.market_environment_evaluator import get_market_environment_evaluator
        
        # 不传入jq_client，使用自动初始化
        evaluator = get_market_environment_evaluator()
        print(f"✅ 评估器初始化成功")
        print(f"  - TrendAnalyzer: {type(evaluator.trend_analyzer).__name__}")
        print(f"  - RegimeDetector: {type(evaluator.regime_detector).__name__}")
        print(f"  - IBDAnalyzer: {type(evaluator.ibd_analyzer).__name__}")
        print(f"  - HMM Model: {type(evaluator.hmm_model).__name__}")
        print(f"  - Trend Classifier: {type(evaluator.trend_classifier).__name__}")
        return evaluator
    except Exception as e:
        print(f"❌ 评估器初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_evaluation(evaluator):
    """测试综合评估"""
    print("\n" + "="*60)
    print("3. 测试综合评估")
    print("="*60)
    
    if evaluator is None:
        print("⚠️ 跳过测试（评估器未初始化）")
        return None
    
    try:
        result = evaluator.evaluate(index_code="000001.XSHG")
        
        print(f"✅ 综合评估执行成功")
        print(f"  - 评估日期: {result.evaluation_date}")
        print(f"  - 指数代码: {result.index_code}")
        print(f"  - 成功状态: {result.success}")
        print(f"  - 趋势得分: {result.trend_score:.3f}")
        print(f"  - 市场环境: {result.market_regime}")
        print(f"  - 反转信号: {result.reversal_signal:.3f}")
        print(f"  - 风险得分: {result.risk_score:.1f}")
        
        if result.warnings:
            print(f"  - 警告数量: {len(result.warnings)}")
            for w in result.warnings[:3]:  # 只显示前3条
                print(f"    * {w[:80]}...")
        
        return result
    except Exception as e:
        print(f"❌ 综合评估失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_dynamic_signals(eval_result):
    """测试动态信号接口"""
    print("\n" + "="*60)
    print("4. 测试动态信号接口")
    print("="*60)
    
    try:
        from core.dynamic_signals import get_dynamic_signal_provider
        
        provider = get_dynamic_signal_provider()
        
        # 测试单个接口（使用eval_result避免重复计算）
        ts = provider.trend_score(eval_result=eval_result) if eval_result else 0.0
        mr = provider.market_regime(eval_result=eval_result) if eval_result else "unknown"
        rs = provider.reversal_signal(eval_result=eval_result) if eval_result else 0.0
        spr = provider.suggested_position_ratio(eval_result=eval_result) if eval_result else 0.5
        ass = provider.allocation_style_shift(eval_result=eval_result) if eval_result else "balanced"
        res = provider.risk_exposure_score(eval_result=eval_result) if eval_result else 50.0
        vr = provider.volatility_regime(eval_result=eval_result) if eval_result else "medium"
        tfs = provider.trade_frequency_suggestion(eval_result=eval_result) if eval_result else "daily"
        
        print("✅ 动态信号接口测试成功:")
        print(f"  1. trend_score: {ts:.3f}")
        print(f"  2. market_regime: {mr}")
        print(f"  3. reversal_signal: {rs:.3f}")
        print(f"  4. suggested_position_ratio: {spr:.2%}")
        print(f"  5. allocation_style_shift: {ass}")
        print(f"  6. risk_exposure_score: {res:.1f}")
        print(f"  7. volatility_regime: {vr}")
        print(f"  8. trade_frequency_suggestion: {tfs}")
        
        return True
    except Exception as e:
        print(f"❌ 动态信号接口测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_signal_fusion(eval_result):
    """测试信号融合"""
    print("\n" + "="*60)
    print("5. 测试信号融合")
    print("="*60)
    
    if eval_result is None:
        print("⚠️ 跳过测试（无评估结果）")
        return False
    
    try:
        from core.signal_fusion import get_signal_fusion, FusionMethod
        
        fusion = get_signal_fusion()
        
        # 测试加权平均融合
        result_wa = fusion.fuse(eval_result, method=FusionMethod.WEIGHTED_AVERAGE)
        print(f"✅ 加权平均融合:")
        print(f"  - 融合趋势得分: {result_wa.fused_trend_score:.3f}")
        print(f"  - 融合市场环境: {result_wa.fused_market_regime}")
        print(f"  - 置信度: {result_wa.confidence:.2%}")
        print(f"  - 一致性: {result_wa.consistency:.2%}")
        
        # 测试投票融合
        result_vote = fusion.fuse(eval_result, method=FusionMethod.VOTING)
        print(f"✅ 投票融合:")
        print(f"  - 融合趋势得分: {result_vote.fused_trend_score:.3f}")
        print(f"  - 融合市场环境: {result_vote.fused_market_regime}")
        
        # 测试一致性融合
        result_cons = fusion.fuse(eval_result, method=FusionMethod.CONSENSUS)
        print(f"✅ 一致性融合:")
        print(f"  - 融合趋势得分: {result_cons.fused_trend_score:.3f}")
        print(f"  - 融合市场环境: {result_cons.fused_market_regime}")
        
        return True
    except Exception as e:
        print(f"❌ 信号融合测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("市场趋势环境综合评估模块测试")
    print("="*60)
    
    results = {
        "imports": False,
        "evaluator_init": False,
        "evaluation": False,
        "dynamic_signals": False,
        "signal_fusion": False
    }
    
    # 1. 测试导入
    results["imports"] = test_imports()
    
    # 2. 测试评估器初始化
    evaluator = test_evaluator_init()
    results["evaluator_init"] = evaluator is not None
    
    # 3. 测试综合评估
    eval_result = test_evaluation(evaluator)
    results["evaluation"] = eval_result is not None
    
    # 4. 测试动态信号接口
    results["dynamic_signals"] = test_dynamic_signals(eval_result)
    
    # 5. 测试信号融合
    results["signal_fusion"] = test_signal_fusion(eval_result)
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = 0
    total = len(results)
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！模块可以正常使用。")
    else:
        print("\n⚠️ 部分测试未通过，请检查错误信息。")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

