#!/bin/bash
# 文档整理脚本

cd /home/taotao/dev/QuantTest/TRQuant/extension/docs

# 1. 架构设计文档
mv ARCHITECTURE.md ARCHITECTURE_DESIGN.md SYSTEM_OVERVIEW.md DATA_ANALYSIS_ARCHITECTURE.md DESIGN.md 01_architecture/ 2>/dev/null
mv "市场趋势识别模块设计（韬睿量化系统）.pdf" "机构级量化研究与实盘交易平台构建方案.pdf" 01_architecture/ 2>/dev/null

# 2. 开发指南
mv INSTALLATION.md USAGE.md DEVELOPMENT_ROADMAP.md DEVELOPMENT_PRINCIPLES.md DEV_DEBUG_WORKFLOW.md 02_development_guides/ 2>/dev/null
mv COMPLETE_DEVELOPMENT_WORKFLOW.md DEVELOPMENT_LOG.md DEVELOPMENT_MILESTONES.md DEVELOPMENT_STATUS_REPORT.md 02_development_guides/ 2>/dev/null
mv PROJECT_SYNC_GUIDE.md QUICK_SYNC_GUIDE.md CONFIG_VERIFICATION.md REVIEW_CHECKLIST.md 02_development_guides/ 2>/dev/null
mv PROJECT_ANALYSIS_SUMMARY.md PROJECT_DIRECTORY_EXPLANATION.md TODO_CLEANUP_SUMMARY.md 02_development_guides/ 2>/dev/null
mv CURSOR_EXTENSION_RESEARCH_GOAL.md cursor_interactive_feedback_setup.md cursor_untitled_chat.md 02_development_guides/ 2>/dev/null
mv mcp_setup_guide.md markdown-import-rules.md token_optimization_rule.md 02_development_guides/ 2>/dev/null
mv "Cursor规则制定建议.mhtml" 02_development_guides/ 2>/dev/null

# 3. 模块文档
mv CANDIDATE_POOL_MODULE.md CANDIDATE_POOL_IMPLEMENTATION_SUMMARY.md STOCK_SELECTION_MODULE_DEVELOPMENT.md 03_modules/ 2>/dev/null
mv FACTOR_MODULE_DESIGN.md MARKET_TREND_MODULE.md TIME_DIMENSION_IMPLEMENTATION.md TIME_DIMENSION_PRINCIPLES.md 03_modules/ 2>/dev/null
mv FIVE_DIMENSION_EXECUTION_PLAN.md FIVE_DIMENSION_IMPLEMENTATION_PLAN.md FIVE_DIMENSION_REDESIGN_PLAN.md FIVE_DIMENSION_TASK_BREAKDOWN.md 03_modules/ 2>/dev/null
mv FUNDS_DIMENSION_DATA_ANALYSIS.md HEATMAP_DEVELOPMENT_PLAN.md HEATMAP_FIX_PHASE1.md HEATMAP_INTEGRATION_ISSUES.md 03_modules/ 2>/dev/null
mv HEATMAP_SYSTEM_ARCHITECTURE.md HEATMAP_SYSTEM_COMPLETE.md MAINLINE_HEATMAP_INTEGRATION.md 03_modules/ 2>/dev/null
mv DATA_SOURCE_DEVELOPMENT.md DATA_SOURCE_EVALUATION.md DATA_SOURCE_INTEGRATION.md DATA_SOURCE_QUICK_REF.md 03_modules/ 2>/dev/null
mv "Alpha因子模块集成方案设计.pdf" "补充alpha模块完善建议.pdf" "补充因子构建模块完善建议.pdf" 03_modules/ 2>/dev/null
mv "市场主线识别模块之热度评分设计方案.pdf" "市场主线识别模块五维评分系统设计方案.pdf" 03_modules/ 2>/dev/null
mv "韬睿量化系统个股筛选模块构建方案.pdf" "五维评分系统设计方案_提取.txt" "热度评分设计方案.txt" 03_modules/ 2>/dev/null
mv MODULE_API_REFERENCE.md 03_modules/ 2>/dev/null

# 4. 平台集成文档
mv PTRADE_BRIDGE_GUIDE.md PTRADE_CURSOR_INTEGRATION.md QMT_BRIDGE_GUIDE.md QUANTCONNECT_BRIDGE_GUIDE.md 04_platform_integration/ 2>/dev/null
mv "QMT vs JQData 在A股量化系统中的应用对比.pdf" "QMT作为量化数据源的可行性研究.pdf" 04_platform_integration/ 2>/dev/null
mv "A股量化数据源多维度比较.pdf" 04_platform_integration/ 2>/dev/null

# 5. 参考书籍PDF
mv "A股与港股量化投资实操指南.pdf" "A股主线识别量化流程建议书.pdf" "A股板块主线量化选股方法论设计.pdf" 05_reference_books/ 2>/dev/null
mv "高倍股分析与策略实践：从因子框架到交易落地.pdf" "高倍股量化投资策略（QuantConnect实现）.pdf" "高倍股量化投资策略（QuantConnect实现）.docx" 05_reference_books/ 2>/dev/null
mv "第二册：宏观经济手册 - 宏观经济与股市走向追踪.pdf" "QuantConnect策略库深度研究报告.pdf" 05_reference_books/ 2>/dev/null
mv "QuantConnect平台策略开发：AI方法与传统策略的比较.docx" "市场主流量化助手平台对比分析报告.pdf" 05_reference_books/ 2>/dev/null
mv "主流开源量化研究平台与AI助手项目综述.pdf" "韬睿量化系统操作手册.pdf" 05_reference_books/ 2>/dev/null
mv "小资金投资者的策略探讨.docx" "目录.docx" 05_reference_books/ 2>/dev/null
mv "Ubuntu 24.04 LTS 金融_AI 工作站搭建手册.pdf" "Ubuntu 24.04 LTS 金融_AI 工作站搭建手册.docx" 05_reference_books/ 2>/dev/null
mv "Cursor IDE 插件定制开发调研报告.pdf" 05_reference_books/ 2>/dev/null
mv Quantconnect-*.pdf 1Quantconnect-*.pdf 2Quantconnect-*.pdf 3Quantconnect-*.pdf 4Quantconnect-*.pdf 05_reference_books/ 2>/dev/null

# 6. 测试和报告
mv BACKTEST_TEST_RESULTS.md TEST_SUMMARY.md PHASE1_COMPLETION_REPORT.md NEXT_STEPS_AFTER_DATA_SOURCE_TEST.md 06_testing_reports/ 2>/dev/null
mv project_status_snapshot.md project_rules_report.md project_rules_report.json project_format_optimization_report.md 06_testing_reports/ 2>/dev/null

# 7. 工作流文档
mv integrated_workflow_prompt.md "市场之盾与选股之矛.md" "第二册_宏观经济与股市走向追踪.md" 07_workflow/ 2>/dev/null
mv "策略优化器学习引擎文档.md" "学习引擎工作流程图.md" 07_workflow/ 2>/dev/null
mv "美股实操手册_Astro_Cursor_GPT全流程总结.md" astro-plan.md astro_document_system_architecture.md 07_workflow/ 2>/dev/null

# 8. AI工具相关
mv AI_MODEL_QUICK_REF.md AI_MODEL_STRATEGY.md AUTO_COMMIT_GUIDE.md chat_history_backup.md 08_ai_tools/ 2>/dev/null
mv finance-glossary-feature.md glossary-api-usage.md 08_ai_tools/ 2>/dev/null

# 9. 遗留文件（保留在根目录或移动到legacy）
mv index.html workstation.csv README.md 09_legacy/ 2>/dev/null

echo "文档整理完成！"

