#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
V6模块快速测试脚本
================

功能:
1. 逐个测试V6各模块是否正常工作
2. 不执行完整回测，只测试核心功能
3. 识别问题所在

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# JQData认证
def init_jqdata():
    """初始化JQData"""
    import jqdatasdk as jq
    config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
    with open(config_path) as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    logger.info("✅ JQData认证成功")
    return jq


def test_market_classifier():
    """测试市场分类器"""
    print("\n" + "="*60)
    print("测试1: MarketCharacterClassifierV6")
    print("="*60)
    
    try:
        from core.strategy.market_character_classifier_v6 import MarketCharacterClassifierV6
        
        start = time.time()
        classifier = MarketCharacterClassifierV6()
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        # 测试分类
        start = time.time()
        result = classifier.classify("2024-09-25")
        logger.info(f"✅ 分类成功 ({time.time()-start:.2f}s)")
        logger.info(f"   市场类型: {result.market_type.value}")
        logger.info(f"   策略模式: {result.strategy_mode.value}")
        logger.info(f"   置信度: {result.confidence:.0%}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_event_engine():
    """测试事件驱动引擎"""
    print("\n" + "="*60)
    print("测试2: EventDrivenEngineV6")
    print("="*60)
    
    try:
        from core.strategy.event_driven_engine_v6 import EventDrivenEngineV6
        
        start = time.time()
        engine = EventDrivenEngineV6()
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_risk_manager():
    """测试风险管理器"""
    print("\n" + "="*60)
    print("测试3: DynamicRiskManager")
    print("="*60)
    
    try:
        from core.strategy.dynamic_risk_manager import DynamicRiskManager
        
        start = time.time()
        manager = DynamicRiskManager()
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mainline_selector_mini():
    """测试主线选择器（迷你版）"""
    print("\n" + "="*60)
    print("测试4: DynamicMainlineSelector (迷你测试)")
    print("="*60)
    
    try:
        from core.strategy.dynamic_mainline_selector import DynamicMainlineSelector
        
        start = time.time()
        selector = DynamicMainlineSelector()
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        # 注意：完整identify_mainlines会很慢，这里只测试初始化
        logger.info("⚠️ 跳过完整主线识别测试（耗时约1-2分钟）")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tenbagger_scorer():
    """测试Tenbagger评分器"""
    print("\n" + "="*60)
    print("测试5: TenbaggerScorer")
    print("="*60)
    
    try:
        from core.tenbagger.tenbagger_scorer import TenbaggerScorer
        
        start = time.time()
        scorer = TenbaggerScorer()
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        # 简单测试评分
        test_stock = "000001.XSHE"
        start = time.time()
        stage, score = scorer.score_stock(test_stock, "2024-09-25")
        logger.info(f"✅ 评分成功 ({time.time()-start:.2f}s)")
        logger.info(f"   股票: {test_stock}")
        logger.info(f"   阶段: {stage.value}")
        logger.info(f"   评分: {score:.1f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_v6():
    """测试V6策略主类"""
    print("\n" + "="*60)
    print("测试6: BullMarketStrategyV6")
    print("="*60)
    
    try:
        from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6
        
        start = time.time()
        strategy = BullMarketStrategyV6(use_dynamic_mainline=False)  # 不使用动态主线加快测试
        logger.info(f"✅ 初始化成功 ({time.time()-start:.2f}s)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_backtest():
    """测试简化回测"""
    print("\n" + "="*60)
    print("测试7: 简化回测（固定主题模式）")
    print("="*60)
    
    try:
        import jqdatasdk as jq
        import pandas as pd
        import numpy as np
        from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6
        
        # 使用固定主题模式（不调用动态主线）
        strategy = BullMarketStrategyV6(use_dynamic_mainline=False)
        
        # AI主题股票
        test_stocks = [
            "002230.XSHE",  # 科大讯飞
            "688111.XSHG",  # 金山办公
            "300058.XSHE",  # 蓝色光标
            "300418.XSHE",  # 昆仑万维
            "600570.XSHG",  # 恒生电子
        ]
        
        start_date = "2024-09-20"
        end_date = "2024-10-15"
        
        # 1. 获取价格数据
        logger.info("获取价格数据...")
        start = time.time()
        price_df = jq.get_price(
            test_stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True,
        )
        logger.info(f"✅ 获取数据成功 ({time.time()-start:.2f}s), 行数={len(price_df)}")
        
        if price_df.empty:
            logger.error("❌ 无数据")
            return False
        
        # 2. 转换格式
        close_df = price_df.pivot(index='time', columns='code', values='close')
        logger.info(f"✅ 数据格式: {close_df.shape}")
        
        # 3. 调用策略决策
        logger.info("调用策略决策...")
        start = time.time()
        decision = strategy.make_decision(
            as_of_date=start_date,
            candidate_stocks=test_stocks,
            use_mainline=False,  # 强制使用固定主题模式
        )
        logger.info(f"✅ 决策完成 ({time.time()-start:.2f}s)")
        logger.info(f"   允许交易: {decision.allow_trade}")
        logger.info(f"   选股模式: {decision.selection_mode}")
        logger.info(f"   买入标的: {len(decision.buy_targets)}只")
        
        if decision.buy_targets:
            for t in decision.buy_targets[:3]:
                logger.info(f"   - {t['stock']}: {t.get('stage', 'N/A')}")
        
        # 4. 简化回测
        if decision.buy_targets:
            selected = [t['stock'] for t in decision.buy_targets]
            selected = [s for s in selected if s in close_df.columns]
            
            if selected:
                returns_df = close_df.pct_change().fillna(0)
                portfolio_returns = returns_df[selected].mean(axis=1)
                cumulative = (1 + portfolio_returns).cumprod()
                total_return = (cumulative.iloc[-1] - 1) * 100
                
                logger.info(f"✅ 回测完成")
                logger.info(f"   选中股票: {selected}")
                logger.info(f"   总收益率: {total_return:.2f}%")
                return True
        
        logger.warning("⚠️ 无可用股票进行回测")
        return True  # 策略本身正常，只是没有选中股票
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("="*70)
    print("V6模块快速测试")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 初始化JQData
    init_jqdata()
    
    # 测试结果
    results = {}
    
    # 逐个测试
    tests = [
        ("市场分类器", test_market_classifier),
        ("事件驱动引擎", test_event_engine),
        ("风险管理器", test_risk_manager),
        ("主线选择器", test_mainline_selector_mini),
        ("Tenbagger评分器", test_tenbagger_scorer),
        ("V6策略主类", test_strategy_v6),
        ("简化回测", test_simple_backtest),
    ]
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            results[name] = False
            logger.error(f"测试 {name} 异常: {e}")
    
    # 汇总
    print("\n" + "="*70)
    print("测试结果汇总")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n通过: {passed}/{len(results)}, 失败: {failed}/{len(results)}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
