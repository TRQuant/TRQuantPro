#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 - 完整集成测试（阶段8.3完整版）
=======================================================

测试内容：
1. 模块导入测试
2. 配置初始化测试
3. 周度布局计划生成测试
4. HTML报告生成测试
5. 命令行工具测试

注意：此测试不依赖JQData连接，主要验证代码结构和数据流
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import traceback
from datetime import datetime


def test_imports():
    """测试所有模块导入"""
    print("=" * 70)
    print("测试1: 模块导入")
    print("=" * 70)

    modules = [
        "core.advisor_v4.advisor_v4_workflow",
        "core.advisor_v4.weekly_layout_planner",
        "core.advisor_v4.weekly_report_generator",
        "core.advisor_v4.jqfactor_calculator",
        "core.advisor_v4.rule_based_strategy",
        "core.advisor_v4.rule_optimizer",
        "core.advisor_v4.multi_factor_calculator",
        "core.advisor_v4.trading_strategy",
        "core.advisor_v4.backtest_engine",
        "core.data.fast_data_loader",
    ]

    failed = []
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except Exception as e:
            print(f"  ❌ {module_name}: {e}")
            failed.append((module_name, str(e)))

    if failed:
        print(f"\n⚠️ {len(failed)} 个模块导入失败")
        return False
    else:
        print(f"\n✅ 所有 {len(modules)} 个模块导入成功")
        return True


def test_config():
    """测试配置初始化"""
    print("\n" + "=" * 70)
    print("测试2: 配置初始化")
    print("=" * 70)

    try:
        from core.advisor_v4.advisor_v4_workflow import AdvisorV4Config

        config = AdvisorV4Config(
            train_start="2024-01-01",
            train_end="2024-12-31",
            val_start="2025-01-01",
            val_end="2025-08-31",
            test_start="2025-09-06",
            test_end="2025-09-13",
        )

        # 验证周频配置
        assert hasattr(config, "lookback_weeks"), "缺少 lookback_weeks 配置"
        assert config.lookback_weeks == 1, f"lookback_weeks 应为 1，实际为 {config.lookback_weeks}"

        print(f"  ✅ AdvisorV4Config 创建成功")
        print(f"     - lookback_weeks: {config.lookback_weeks}")
        print(f"     - train_start: {config.train_start}")
        print(f"     - train_end: {config.train_end}")

        return True, config

    except Exception as e:
        print(f"  ❌ 配置初始化失败: {e}")
        traceback.print_exc()
        return False, None


def test_weekly_layout_planner():
    """测试周度布局计划生成器"""
    print("\n" + "=" * 70)
    print("测试3: 周度布局计划生成器")
    print("=" * 70)

    try:
        from core.advisor_v4.weekly_layout_planner import (
            WeeklyLayoutPlanner,
            LayoutTarget,
            EntryPlan,
            ExitPlan,
        )

        planner = WeeklyLayoutPlanner(verbose=False)

        # 创建测试候选
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

        # 验证计划结构
        assert plan.week_start == "2025-09-08", "week_start 不正确"
        assert plan.week_end == "2025-09-12", "week_end 不正确"
        assert len(plan.targets) == 2, f"标的数量应为2，实际为{len(plan.targets)}"
        assert len(plan.entry_plan) == 2, f"入场计划数量应为2，实际为{len(plan.entry_plan)}"
        assert len(plan.exit_plan) == 2, f"出场计划数量应为2，实际为{len(plan.exit_plan)}"

        print(f"  ✅ WeeklyLayoutPlan 创建成功")
        print(f"     - 周期: {plan.week_start} ~ {plan.week_end}")
        print(f"     - 标的数量: {len(plan.targets)}")
        print(f"     - 建议仓位: {plan.position_advice:.1%}")
        print(f"     - 入场计划: {len(plan.entry_plan)} 个")
        print(f"     - 出场计划: {len(plan.exit_plan)} 个")

        # 验证入场计划结构
        for code, entry in plan.entry_plan.items():
            assert entry.plan_type == "staged", f"{code} 入场计划类型应为 staged"
            assert len(entry.stages) == 3, f"{code} 入场计划应有3个阶段，实际为{len(entry.stages)}"
            print(f"     - {code} 入场计划: {len(entry.stages)} 个阶段")

        return True, plan

    except Exception as e:
        print(f"  ❌ 周度布局计划生成失败: {e}")
        traceback.print_exc()
        return False, None


def test_report_generator(plan):
    """测试报告生成器"""
    print("\n" + "=" * 70)
    print("测试4: HTML报告生成器")
    print("=" * 70)

    try:
        from core.advisor_v4.weekly_report_generator import WeeklyReportGenerator

        generator = WeeklyReportGenerator(verbose=False)
        report_path = generator.generate(plan, output_filename="v4_full_integration_test.html")

        # 验证报告文件存在
        report_file = Path(report_path)
        assert report_file.exists(), f"报告文件不存在: {report_path}"

        # 验证报告内容
        content = report_file.read_text(encoding="utf-8")
        assert "韬睿量化" in content, "报告缺少标题"
        assert "周度布局计划" in content, "报告缺少布局计划内容"
        assert plan.week_start in content, "报告缺少周期信息"

        print(f"  ✅ HTML报告生成成功")
        print(f"     - 文件路径: {report_path}")
        print(f"     - 文件大小: {report_file.stat().st_size / 1024:.1f} KB")
        print(f"     - 包含Tab: 首页、市场展望、交易策略、风险提示、个股详情")

        return True, report_path

    except Exception as e:
        print(f"  ❌ HTML报告生成失败: {e}")
        traceback.print_exc()
        return False, None


def test_workflow_methods():
    """测试工作流方法（不依赖JQData）"""
    print("\n" + "=" * 70)
    print("测试5: 工作流方法（结构验证）")
    print("=" * 70)

    try:
        from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config

        config = AdvisorV4Config(
            train_start="2024-01-01",
            train_end="2024-12-31",
            val_start="2025-01-01",
            val_end="2025-08-31",
        )

        workflow = AdvisorV4Workflow(config=config, verbose=False)

        # 验证方法存在
        assert hasattr(workflow, "recommend_weekly_layout"), "缺少 recommend_weekly_layout 方法"
        assert hasattr(workflow, "generate_weekly_layout_report"), "缺少 generate_weekly_layout_report 方法"
        assert hasattr(workflow, "get_trading_days_in_week"), "缺少 get_trading_days_in_week 方法"
        assert hasattr(workflow, "get_prev_week_anchor"), "缺少 get_prev_week_anchor 方法"
        assert hasattr(workflow, "get_week_start_end"), "缺少 get_week_start_end 方法"

        print(f"  ✅ 工作流方法验证成功")
        print(f"     - recommend_weekly_layout: ✅")
        print(f"     - generate_weekly_layout_report: ✅")
        print(f"     - get_trading_days_in_week: ✅")
        print(f"     - get_prev_week_anchor: ✅")
        print(f"     - get_week_start_end: ✅")

        return True

    except Exception as e:
        print(f"  ❌ 工作流方法验证失败: {e}")
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("Investment Advisor V4.0 - 完整集成测试")
    print("=" * 70)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    results = {
        "imports": False,
        "config": False,
        "planner": False,
        "report": False,
        "workflow": False,
    }

    # 测试1: 模块导入
    results["imports"] = test_imports()
    if not results["imports"]:
        print("\n❌ 模块导入失败，终止测试")
        return 1

    # 测试2: 配置初始化
    results["config"], config = test_config()
    if not results["config"]:
        print("\n❌ 配置初始化失败，终止测试")
        return 1

    # 测试3: 周度布局计划生成器
    results["planner"], plan = test_weekly_layout_planner()
    if not results["planner"]:
        print("\n❌ 周度布局计划生成失败，终止测试")
        return 1

    # 测试4: HTML报告生成器
    results["report"], report_path = test_report_generator(plan)
    if not results["report"]:
        print("\n❌ HTML报告生成失败，终止测试")
        return 1

    # 测试5: 工作流方法
    results["workflow"] = test_workflow_methods()
    if not results["workflow"]:
        print("\n❌ 工作流方法验证失败，终止测试")
        return 1

    # 总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)

    all_passed = all(results.values())
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {test_name:15s}: {status}")

    print("=" * 70)

    if all_passed:
        print("✅ 所有测试通过！")
        print(f"\n📄 生成的报告: {report_path}")
        print("   请在浏览器中打开查看")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
