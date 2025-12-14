"""
文件名: code_10_9_FactorManager.py
保存路径: code_library/010_Chapter10_Development_Guide/10.9/code_10_9_FactorManager.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: FactorManager

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 定位入口类/接口
code_result = code_server.search(pattern="class FactorManager")
factor_manager_path = code_result["file_path"]

# 2. 查模块设计文档
docs_result = docs_server.query(query="因子库设计 接口约定 命名规范")
design_doc = docs_result["content"]

# 3. 校验文档结构
spec_result = spec_server.validate(
    spec_type="chapter",
    content=chapter_content
)

# 4. 新增因子（Dry Run）
factor_result = factor.create(
    name="momentum_20d",
    formula="close / close.shift(20) - 1",
    category="momentum",
    dry_run=True
)
confirm_token = factor_result["confirm_token"]

# 5. 执行创建（Execute）
factor_result = factor.create(
    name="momentum_20d",
    formula="close / close.shift(20) - 1",
    category="momentum",
    execute=True,
    confirm_token=confirm_token,
    evidence=True
)

# 6. 回测验证
backtest_result = workflow.run(
    workflow_type="backtest",
    factors=["momentum_20d"],
    start_date="2024-01-01",
    end_date="2024-12-31"
)
artifact_id = backtest_result["artifact_id"]

# 7. 生成对比报告
report_result = report.generate(
    baseline="factor-momentum_20d-v1.0",
    current="factor-momentum_20d-v1.1",
    metrics=["ic", "ir", "sharpe", "max_drawdown"]
)
compare_report = report_result["report_url"]

# 8. 记录证据
evidence.record(
    action="factor.create",
    trace_id=factor_result["trace_id"],
    purpose="新增20日动量因子",
    impact="影响因子库和策略生成",
    rollback="删除因子或回退版本",
    report_url=compare_report,
    artifact_id=artifact_id
)

# 9. Git提交和标签
git.commit(
    message=f"feat: 新增因子 momentum_20d [trace_id: {factor_result['trace_id']}]"
)
git.tag(f"factor-momentum_20d-v{factor_result['version']}")