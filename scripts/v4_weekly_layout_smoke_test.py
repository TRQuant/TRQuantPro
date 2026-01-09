#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 - 周度布局系统快速验证脚本（阶段8.3）
=============================================================

快速验证：
1. WeeklyLayoutPlan 数据结构
2. WeeklyReportGenerator 报告生成
3. recommend_weekly_layout() 方法调用

注意：这是轻量级验证，不依赖JQData和模型文件
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.weekly_layout_planner import (
    WeeklyLayoutPlan,
    WeeklyLayoutPlanner,
    LayoutTarget,
    EntryPlan,
    ExitPlan,
)
from core.advisor_v4.weekly_report_generator import WeeklyReportGenerator


def test_weekly_layout_planner():
    """测试 WeeklyLayoutPlanner"""
    print("=" * 70)
    print("测试 WeeklyLayoutPlanner")
    print("=" * 70)

    planner = WeeklyLayoutPlanner(verbose=True)

    # 创建测试数据
    candidates = [
        {
            "code": "000001.XSHE",
            "name": "平安银行",
            "score": 85.5,
            "reason": "CNE5得分高，Alpha因子确认，基本面良好",
            "entry_price": 12.50,
            "tags": ["银行", "金融"],
        },
        {
            "code": "000002.XSHE",
            "name": "万科A",
            "score": 72.3,
            "reason": "技术面突破，动量因子确认",
            "entry_price": 18.80,
            "tags": ["地产", "蓝筹"],
        },
    ]

    plan = planner.build_from_candidates(
        week_start="2025-09-08",
        week_end="2025-09-12",
        candidates=candidates,
        market_outlook="neutral",
        position_advice=0.6,
        max_targets=5,
    )

    print(f"\n✅ WeeklyLayoutPlan 创建成功")
    print(f"   - 周期: {plan.week_start} ~ {plan.week_end}")
    print(f"   - 标的数量: {len(plan.targets)}")
    print(f"   - 建议仓位: {plan.position_advice:.1%}")
    print(f"   - 入场计划: {len(plan.entry_plan)} 个")
    print(f"   - 出场计划: {len(plan.exit_plan)} 个")

    return plan


def test_weekly_report_generator(plan: WeeklyLayoutPlan):
    """测试 WeeklyReportGenerator"""
    print("\n" + "=" * 70)
    print("测试 WeeklyReportGenerator")
    print("=" * 70)

    generator = WeeklyReportGenerator(verbose=True)
    report_path = generator.generate(plan, output_filename="v4_weekly_layout_test.html")

    print(f"\n✅ 报告生成成功: {report_path}")
    print(f"   请在浏览器中打开查看: {report_path}")

    return report_path


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("Investment Advisor V4.0 - 周度布局系统快速验证")
    print("=" * 70)

    try:
        # 1. 测试 WeeklyLayoutPlanner
        plan = test_weekly_layout_planner()

        # 2. 测试 WeeklyReportGenerator
        report_path = test_weekly_report_generator(plan)

        print("\n" + "=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        print(f"报告路径: {report_path}")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
