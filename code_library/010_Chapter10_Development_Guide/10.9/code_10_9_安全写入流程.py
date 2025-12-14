"""
文件名: code_10_9_安全写入流程.py
保存路径: code_library/010_Chapter10_Development_Guide/10.9/code_10_9_安全写入流程.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 安全写入流程

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. Dry Run（预演）
result = factor.create(
    name="momentum_20d",
    formula="...",
    dry_run=True
)
confirm_token = result["confirm_token"]

# 2. Execute（执行）
result = factor.create(
    name="momentum_20d",
    formula="...",
    execute=True,
    confirm_token=confirm_token
)

# 3. Evidence Record（记录证据）
evidence.record(
    action="factor.create",
    trace_id=result["trace_id"],
    purpose="新增动量因子",
    impact="影响因子库和策略生成",
    rollback="删除因子或回退版本",
    report_url=result["report_url"]
)

# 4. Git Commit/Tag（版本化）
git.commit(
    message=f"feat: 新增因子 momentum_20d [trace_id: {result['trace_id']}]"
)
git.tag(f"factor-momentum_20d-v{result['version']}")

# 5. Report Compare（对比报告）
report.compare(
    baseline="factor-momentum_20d-v1.0",
    current="factor-momentum_20d-v1.1",
    metrics=["ic", "ir", "sharpe"]
)