#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 - 周度布局报告生成脚本（阶段8.2）
=========================================================

使用方式:
    python scripts/generate_weekly_layout_v4.py [--date YYYY-MM-DD] [--top-n 5] [--output filename.html]

功能:
    - 生成"提前一周布局"计划
    - 输出多Tab HTML报告
    - 包含投资标的、入场/出场计划、交易策略、风险提示
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config


def main():
    parser = argparse.ArgumentParser(
        description="Investment Advisor V4.0 - 周度布局报告生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 生成今天的周度布局报告
    python scripts/generate_weekly_layout_v4.py

    # 指定日期
    python scripts/generate_weekly_layout_v4.py --date 2025-09-13

    # 指定推荐数量和输出文件名
    python scripts/generate_weekly_layout_v4.py --top-n 8 --output my_report.html
        """
    )

    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="锚点日期 (YYYY-MM-DD，默认今天)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="推荐标的数量 (默认: 5)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件名 (默认自动生成)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="显示详细日志",
    )

    args = parser.parse_args()

    # 验证日期格式
    if args.date:
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"❌ 日期格式错误: {args.date}，请使用 YYYY-MM-DD 格式")
            return 1

    print("=" * 70)
    print("Investment Advisor V4.0 - 周度布局报告生成")
    print("=" * 70)
    print(f"锚点日期: {args.date or '今天'}")
    print(f"推荐数量: {args.top_n}")
    print(f"输出文件: {args.output or '自动生成'}")
    print("=" * 70)
    print()

    try:
        # 初始化工作流
        config = AdvisorV4Config(
            train_start="2024-01-01",
            train_end="2024-12-31",
            val_start="2025-01-01",
            val_end="2025-08-31",
            test_start=args.date or datetime.now().strftime("%Y-%m-%d"),
            test_end=args.date or datetime.now().strftime("%Y-%m-%d"),
        )
        workflow = AdvisorV4Workflow(config=config, verbose=args.verbose)

        # 生成报告
        report_path = workflow.generate_weekly_layout_report(
            anchor_date=args.date,
            top_n=args.top_n,
            output_filename=args.output,
        )

        print()
        print("=" * 70)
        print("✅ 报告生成完成！")
        print("=" * 70)
        print(f"报告路径: {report_path}")
        print(f"请在浏览器中打开查看")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n❌ 生成报告失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
