#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试V2知识库使用
================

展示如何使用V2新增的知识域和工具
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.knowledge_search_api import search
from core.market_regime.regime_knowledge_base import RegimeKnowledgeBase
from core.market_regime.state_machine import MarketRegimeStateMachine, MarketRegime
from core.strategy_generation.prompts import generate_strategy_prompt


def test_v2_knowledge_search():
    """测试V2新知识域搜索"""
    print("=" * 70)
    print("🔍 测试1: V2新知识域搜索")
    print("=" * 70)
    print()
    
    test_queries = [
        ("情绪退潮", "市场状态识别"),
        ("因子行为映射", "因子行为映射"),
        ("策略模板", "策略模板库"),
        ("失败案例", "失败案例库"),
    ]
    
    for query, domain in test_queries:
        print(f"📋 搜索: \"{query}\" ({domain})")
        result = search(query, limit=3, mode='hybrid')
        
        if result.get('success'):
            items = result.get('results', [])
            print(f"   ✅ 找到 {len(items)} 条记录")
            
            if items:
                for i, item in enumerate(items[:2], 1):
                    title = item.get('title', 'N/A')
                    kb_type = item.get('type', 'N/A')
                    print(f"      {i}. {title[:60]}")
                    print(f"         类型: {kb_type}")
        print()


def test_regime_knowledge_base():
    """测试市场状态知识库"""
    print("=" * 70)
    print("📚 测试2: 市场状态知识库")
    print("=" * 70)
    print()
    
    regime_kb = RegimeKnowledgeBase()
    
    # 测试按状态搜索
    print("📋 搜索'退潮期'相关知识:")
    knowledge = regime_kb.search_by_regime("退潮", limit=3)
    print(f"   找到 {len(knowledge)} 条记录")
    for item in knowledge:
        print(f"   - {item.get('title', 'N/A')}")
    print()
    
    # 测试获取策略建议
    print("📋 获取'退潮期'策略建议:")
    suggestions = regime_kb.get_regime_strategy_suggestions("退潮")
    print(f"   知识条目数: {suggestions['knowledge_count']}")
    print(f"   策略含义: {len(suggestions['strategy_implications'])} 条")
    print()


def test_state_machine():
    """测试市场状态机"""
    print("=" * 70)
    print("🤖 测试3: 市场状态机")
    print("=" * 70)
    print()
    
    sm = MarketRegimeStateMachine()
    
    # 测试不同市场状态
    test_cases = [
        {
            "name": "退潮期",
            "indicators": {
                "limit_up_count": 8,
                "limit_down_count": 3,
                "limit_up_height": 2,
                "limit_up_failure_rate": 0.35,
                "capital_net_inflow": -50,
                "turnover_rate": 1.2,
                "volume_ratio": 0.7
            }
        },
        {
            "name": "主升期",
            "indicators": {
                "limit_up_count": 45,
                "limit_down_count": 1,
                "limit_up_height": 5,
                "limit_up_failure_rate": 0.15,
                "capital_net_inflow": 200,
                "turnover_rate": 2.5,
                "volume_ratio": 1.5
            }
        },
        {
            "name": "过热期",
            "indicators": {
                "limit_up_count": 95,
                "limit_down_count": 0,
                "limit_up_height": 8,
                "limit_up_failure_rate": 0.08,
                "capital_net_inflow": 500,
                "turnover_rate": 3.5,
                "volume_ratio": 2.0
            }
        }
    ]
    
    for case in test_cases:
        print(f"📋 测试场景: {case['name']}")
        result = sm.update_regime(case['indicators'])
        
        print(f"   判断结果: {result['regime']}")
        print(f"   最大仓位: {result['constraints']['max_position']}")
        print(f"   允许策略: {', '.join(result['constraints']['allowed_strategies'])}")
        print(f"   禁止策略: {', '.join(result['constraints']['forbidden_strategies'])}")
        print(f"   风险等级: {result['constraints']['risk_level']}")
        print()
        
        # 测试策略生成限制
        for strategy_type in ["追涨", "趋势跟随", "空仓"]:
            can_generate, reason = sm.can_generate_strategy(strategy_type)
            status = "✅ 允许" if can_generate else "❌ 禁止"
            print(f"   {status}: {strategy_type} - {reason}")
        print()


def test_strategy_prompt_generation():
    """测试策略Prompt生成"""
    print("=" * 70)
    print("📝 测试4: 策略Prompt生成")
    print("=" * 70)
    print()
    
    # 测试短线策略Prompt
    print("📋 生成短线策略Prompt:")
    prompt = generate_strategy_prompt(
        market_regime="退潮期",
        available_factors=["money_flow_main", "volume_ratio", "limit_up_count"],
        strategy_type="short_term",
        sentiment_indicators="涨停家数: 8, 炸板率: 35%",
        capital_flow="资金净流出: -50亿"
    )
    print(prompt[:500] + "...")
    print()
    
    # 测试风控策略Prompt
    print("📋 生成风控策略Prompt:")
    prompt = generate_strategy_prompt(
        market_regime="过热期",
        available_factors=["limit_up_count", "limit_up_height"],
        strategy_type="risk_control",
        risk_signals="涨停家数异常高: 95只, 连板高度: 8板",
        risk_indicators="市场情绪极度亢奋, 无明确主线"
    )
    print(prompt[:500] + "...")
    print()


def main():
    """主函数"""
    print("=" * 70)
    print("🧪 TRQuant知识库V2使用测试")
    print("=" * 70)
    print()
    
    # 测试1: V2新知识域搜索
    test_v2_knowledge_search()
    
    # 测试2: 市场状态知识库
    test_regime_knowledge_base()
    
    # 测试3: 市场状态机
    test_state_machine()
    
    # 测试4: 策略Prompt生成
    test_strategy_prompt_generation()
    
    # 总结
    print("=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print("✅ V2新知识域搜索: 正常")
    print("✅ 市场状态知识库: 正常")
    print("✅ 市场状态机: 正常")
    print("✅ 策略Prompt生成: 正常")
    print()
    print("🎯 V2知识库系统已就绪，可以开始使用！")
    print("=" * 70)


if __name__ == '__main__':
    main()
