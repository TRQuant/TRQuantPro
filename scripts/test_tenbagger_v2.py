#!/usr/bin/env python3
"""
十倍股早期识别系统V2测试脚本

测试内容:
1. 三层漏斗筛选
2. 规则引擎一票否决
3. 三轴阶段判定
4. 评分引擎V2
5. 通过率控制
6. 报告一致性

Author: TRQuant Team
Date: 2025-12-19
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from mcp_servers.utils.tenbagger_v2 import (
    get_evaluator_v2,
    get_candidate_funnel,
    get_rule_engine,
    get_scoring_engine_v2,
    get_tri_axis_stage_machine,
    get_pass_rate_controller,
    ReportGenerator
)


def create_test_data():
    """创建测试数据"""
    return [
        # 1. 优质早期成长股（应该推荐）
        {
            "symbol": "300001.SZ",
            "name": "早期成长A",
            "data": {
                # L0 硬过滤
                "is_st": False,
                "delisting_risk": False,
                "major_violation": False,
                "trading_days_ratio": 0.95,
                "financial_report_count": 4,
                "avg_turnover": 0.02,
                "missing_ratio": 0.1,
                # L1 早期结构信号
                "revenue_growth_qoq_change": 15,
                "profit_growth_change": 20,
                "gross_margin_change": 3,
                "capex_ratio": 0.08,
                "rd_ratio": 0.06,
                "event_count": 3,
                # L2 早期性约束
                "market_cap_percentile": 0.4,
                "price_change_24m": 0.5,
                "analyst_coverage": 8,
                "research_report_count": 5,
                # 三轴阶段
                "profit_growth": 35,
                "cash_flow_improvement": True,
                "consecutive_improvement_quarters": 3,
                "ma_trend": "bullish",
                "volume_increase_ratio": 1.8,
                "turnover_from_low_pct": 80,
                "breakout_signal": True,
                "relative_strength": 75,
                "announcement_count_3m": 5,
                "research_coverage_change": 3,
                "analyst_rating_upgrade": True,
                "industry_event_count": 2,
                "pe_rerating_signal": False,
                # 评分卡
                "revenue_growth": 30,
                "gross_margin": 35,
                "roe": 18,
                "cash_flow_ratio": 1.0,
                "debt_ratio": 35,
                "pe_percentile": 40,
                "institutional_ownership": 15,
                # 规则引擎
                "cash_flow_negative_years": 0,
                "short_debt_ratio": 0.3,
                "goodwill_ratio": 0.1,
                "non_recurring_ratio": 0.1,
                "pledge_ratio": 0.2,
                "near_pledge_liquidation": False,
                "receivable_revenue_ratio": 0.2,
                "inventory_revenue_ratio": 0.3,
                "audit_opinion": "standard",
                "has_major_lawsuit": False,
                "continuous_loss_years": 0
            }
        },
        # 2. 成熟大票（应该降级或不推荐）
        {
            "symbol": "600000.SH",
            "name": "成熟银行B",
            "data": {
                "is_st": False,
                "delisting_risk": False,
                "major_violation": False,
                "trading_days_ratio": 0.99,
                "financial_report_count": 4,
                "avg_turnover": 0.005,
                "missing_ratio": 0.0,
                # 早期信号弱
                "revenue_growth_qoq_change": 2,
                "profit_growth_change": 3,
                "gross_margin_change": 0.5,
                "capex_ratio": 0.02,
                "rd_ratio": 0.01,
                "event_count": 1,
                # 早期性约束触发
                "market_cap_percentile": 0.95,  # 市值过大
                "price_change_24m": 0.3,
                "analyst_coverage": 50,  # 覆盖过高
                "research_report_count": 100,
                # 三轴阶段（S0）
                "profit_growth": 5,
                "cash_flow_improvement": False,
                "consecutive_improvement_quarters": 1,
                "ma_trend": "neutral",
                "volume_increase_ratio": 1.0,
                "turnover_from_low_pct": 10,
                "breakout_signal": False,
                "relative_strength": 45,
                "announcement_count_3m": 2,
                "research_coverage_change": 0,
                "analyst_rating_upgrade": False,
                "industry_event_count": 0,
                "pe_rerating_signal": False,
                # 评分卡
                "revenue_growth": 5,
                "gross_margin": 20,
                "roe": 12,
                "cash_flow_ratio": 0.8,
                "debt_ratio": 85,
                "pe_percentile": 20,
                "institutional_ownership": 60,
                # 规则引擎
                "cash_flow_negative_years": 0,
                "short_debt_ratio": 0.5,
                "goodwill_ratio": 0.0,
                "non_recurring_ratio": 0.1,
                "pledge_ratio": 0.0,
                "near_pledge_liquidation": False,
                "receivable_revenue_ratio": 0.1,
                "inventory_revenue_ratio": 0.1,
                "audit_opinion": "standard",
                "has_major_lawsuit": False,
                "continuous_loss_years": 0
            }
        },
        # 3. 问题股票（应该被否决）
        {
            "symbol": "000001.SZ",
            "name": "问题股C",
            "data": {
                "is_st": True,  # 触发否决
                "delisting_risk": True,
                "major_violation": False,
                "trading_days_ratio": 0.7,
                "financial_report_count": 3,
                "avg_turnover": 0.01,
                "missing_ratio": 0.3,
                # 其他数据
                "revenue_growth_qoq_change": -10,
                "profit_growth_change": -20,
                "gross_margin_change": -5,
                "capex_ratio": 0.01,
                "rd_ratio": 0.01,
                "event_count": 0,
                "market_cap_percentile": 0.3,
                "price_change_24m": -0.5,
                "analyst_coverage": 2,
                "research_report_count": 1
            }
        },
        # 4. 数据缺失股票（应该低分）
        {
            "symbol": "002001.SZ",
            "name": "数据缺失D",
            "data": {
                "is_st": False,
                "delisting_risk": False,
                "major_violation": False,
                "trading_days_ratio": 0.85,
                "financial_report_count": 4,
                "avg_turnover": 0.015,
                "missing_ratio": 0.4,
                # 大部分数据缺失
                "market_cap_percentile": 0.5,
                "price_change_24m": 0.2
                # 其他数据故意不提供
            }
        },
        # 5. 高杠杆问题（应该被否决）
        {
            "symbol": "600001.SH",
            "name": "高杠杆E",
            "data": {
                "is_st": False,
                "delisting_risk": False,
                "major_violation": False,
                "trading_days_ratio": 0.9,
                "financial_report_count": 4,
                "avg_turnover": 0.02,
                "missing_ratio": 0.1,
                "debt_ratio": 85,  # 高负债
                "short_debt_ratio": 0.9,  # 高短债
                "cash_flow_negative_years": 3,
                "revenue_growth": 5
            }
        }
    ]


def test_v2_system():
    """测试V2系统"""
    print("=" * 60)
    print("十倍股早期识别系统 V2 测试")
    print("=" * 60)
    print()
    
    # 获取组件
    evaluator = get_evaluator_v2()
    evaluator.reset()  # 重置状态
    
    # 创建测试数据
    test_stocks = create_test_data()
    
    print(f"📊 测试数据: {len(test_stocks)} 只股票")
    print()
    
    # 批量评估
    print("🔄 开始评估...")
    reports = evaluator.batch_evaluate(test_stocks)
    
    print()
    print("📋 评估结果:")
    print("-" * 60)
    
    for report in reports:
        status = "✅ 推荐" if report.is_recommended else "❌ 不推荐"
        vetoed = "🚫 已否决" if report.is_vetoed else ""
        print(f"{report.symbol} {report.name}")
        print(f"  - 状态: {status} {vetoed}")
        print(f"  - 等级: {report.recommendation_level}")
        print(f"  - 分数: {report.final_score:.1f}")
        print(f"  - 阶段: {report.stage} (置信度: {report.stage_confidence:.0%})")
        print(f"  - 漏斗: {report.funnel_level}")
        print(f"  - 质量: {report.quality_flag}")
        print(f"  - 理由: {report.recommendation_reason}")
        if report.risk_warnings:
            print(f"  - 警告: {report.risk_warnings[:2]}")
        print()
    
    # 统计
    stats = evaluator.get_stats()
    print("📊 统计信息:")
    print("-" * 60)
    print(f"  总评估: {stats['total_evaluated']}")
    print(f"  推荐数: {stats['recommended']}")
    print(f"  推荐率: {stats['recommended'] / max(1, stats['total_evaluated']):.1%}")
    print(f"  否决数: {stats['rejected']}")
    print()
    
    print("等级分布:")
    for level, count in stats["by_level"].items():
        if count > 0:
            print(f"  {level}: {count}")
    print()
    
    print("阶段分布:")
    for stage, count in stats["by_stage"].items():
        if count > 0:
            print(f"  {stage}: {count}")
    print()
    
    # 生成报告
    print("📝 生成报告...")
    generator = ReportGenerator(evaluator)
    
    # 保存Markdown报告
    report_path = "/home/taotao/dev/QuantTest/TRQuant/docs/TENBAGGER_V2_TEST_REPORT.md"
    generator.save_report(report_path, format="markdown")
    print(f"  报告已保存: {report_path}")
    
    # 一致性报告
    consistency = evaluator.generate_consistency_report()
    print()
    print("✅ 一致性检查:")
    print(f"  运行ID: {consistency.run_id}")
    print(f"  L2通过率: {consistency.stats.l2_pass_rate:.1%}")
    if consistency.warnings:
        print(f"  ⚠️ 警告: {consistency.warnings}")
    else:
        print("  ✓ 无警告")
    
    print()
    print("=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_v2_system()

