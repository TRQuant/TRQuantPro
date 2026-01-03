#!/bin/bash
# 整理剩余的文档

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

move_file() {
    local src="$1"
    local dst="$2"
    if [ -f "$src" ]; then
        mkdir -p "$(dirname "$dst")"
        mv "$src" "$dst"
        echo "✓ $(basename "$src") -> $(dirname "$dst")/"
    fi
}

echo "整理剩余文档..."

# 模块文档
move_file "CANDIDATE_POOL_IMPLEMENTATION_SUMMARY.md" "03_modules/CANDIDATE_POOL_IMPLEMENTATION_SUMMARY_ROOT.md"
move_file "CANDIDATE_POOL_MODULE.md" "03_modules/CANDIDATE_POOL_MODULE_ROOT.md"
move_file "FACTOR_MODULE_DESIGN.md" "03_modules/FACTOR_MODULE_DESIGN_ROOT.md"
move_file "FIVE_DIMENSION_EXECUTION_PLAN.md" "03_modules/FIVE_DIMENSION_EXECUTION_PLAN_ROOT.md"
move_file "FIVE_DIMENSION_IMPLEMENTATION_PLAN.md" "03_modules/FIVE_DIMENSION_IMPLEMENTATION_PLAN_ROOT.md"
move_file "FIVE_DIMENSION_REDESIGN_PLAN.md" "03_modules/FIVE_DIMENSION_REDESIGN_PLAN_ROOT.md"
move_file "FIVE_DIMENSION_TASK_BREAKDOWN.md" "03_modules/FIVE_DIMENSION_TASK_BREAKDOWN_ROOT.md"
move_file "FUNDS_DIMENSION_DATA_ANALYSIS.md" "03_modules/FUNDS_DIMENSION_DATA_ANALYSIS_ROOT.md"
move_file "HEATMAP_DEVELOPMENT_PLAN.md" "03_modules/HEATMAP_DEVELOPMENT_PLAN_ROOT.md"
move_file "HEATMAP_FIX_PHASE1.md" "03_modules/HEATMAP_FIX_PHASE1_ROOT.md"
move_file "HEATMAP_INTEGRATION_ISSUES.md" "03_modules/HEATMAP_INTEGRATION_ISSUES_ROOT.md"
move_file "HEATMAP_SYSTEM_ARCHITECTURE.md" "03_modules/HEATMAP_SYSTEM_ARCHITECTURE_ROOT.md"
move_file "HEATMAP_SYSTEM_COMPLETE.md" "03_modules/HEATMAP_SYSTEM_COMPLETE_ROOT.md"
move_file "MAINLINE_HEATMAP_INTEGRATION.md" "03_modules/MAINLINE_HEATMAP_INTEGRATION_ROOT.md"
move_file "MARKET_TREND_MODULE.md" "03_modules/MARKET_TREND_MODULE_ROOT.md"
move_file "MODULE_API_REFERENCE.md" "03_modules/MODULE_API_REFERENCE_ROOT.md"
move_file "STOCK_SELECTION_MODULE_DEVELOPMENT.md" "03_modules/STOCK_SELECTION_MODULE_DEVELOPMENT_ROOT.md"
move_file "TIME_DIMENSION_IMPLEMENTATION.md" "03_modules/TIME_DIMENSION_IMPLEMENTATION_ROOT.md"
move_file "TIME_DIMENSION_PRINCIPLES.md" "03_modules/TIME_DIMENSION_PRINCIPLES_ROOT.md"

# 平台集成文档
move_file "PTRADE_BRIDGE_GUIDE.md" "04_platform_integration/PTRADE_BRIDGE_GUIDE_ROOT.md"
move_file "PTRADE_CURSOR_INTEGRATION.md" "04_platform_integration/PTRADE_CURSOR_INTEGRATION_ROOT.md"
move_file "QMT_BRIDGE_GUIDE.md" "04_platform_integration/QMT_BRIDGE_GUIDE_ROOT.md"
move_file "QUANTCONNECT_BRIDGE_GUIDE.md" "04_platform_integration/QUANTCONNECT_BRIDGE_GUIDE_ROOT.md"

# 测试报告
move_file "NEXT_STEPS_AFTER_DATA_SOURCE_TEST.md" "06_testing_reports/NEXT_STEPS_AFTER_DATA_SOURCE_TEST_ROOT.md"
move_file "PHASE1_COMPLETION_REPORT.md" "06_testing_reports/PHASE1_COMPLETION_REPORT_ROOT.md"
move_file "project_format_optimization_report.md" "06_testing_reports/project_format_optimization_report_ROOT.md"
move_file "project_rules_report.md" "06_testing_reports/project_rules_report_ROOT.md"
move_file "project_status_snapshot.md" "06_testing_reports/project_status_snapshot_ROOT.md"

# 开发指南
move_file "IMPLEMENTATION_PLAN.md" "02_development_guides/project_guides/IMPLEMENTATION_PLAN_ROOT.md"
move_file "STRATEGY_OPTIMIZER_REVIEW.md" "02_development_guides/STRATEGY_OPTIMIZER_REVIEW.md"

# 文档整理相关（保留在根目录）
# move_file "文档分类整理报告.md" "文档分类整理报告.md"
# move_file "文档整理总结.md" "文档整理总结.md"
# move_file "韬睿系统开发状态总结.md" "韬睿系统开发状态总结.md"
# move_file "项目书创建指南.md" "项目书创建指南.md"

echo "完成！"
