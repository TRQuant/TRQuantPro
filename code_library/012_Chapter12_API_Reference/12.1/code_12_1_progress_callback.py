"""
文件名: code_12_1_progress_callback.py
保存路径: code_library/012_Chapter12_API_Reference/12.1/code_12_1_progress_callback.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.1_Module_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: progress_callback

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.workflow_orchestrator import WorkflowOrchestrator

# 初始化工作流编排器
orchestrator = WorkflowOrchestrator()

# 执行完整工作流
def progress_callback(step_name: str, progress: int, message: str):
    print(f"[{step_name}] {progress}% - {message}")

result = orchestrator.run_full_workflow(callback=progress_callback)

# 查看结果
print(f"工作流执行: {'成功' if result.success else '失败'}")
for step_name, step_result in result.step_results.items():
    print(f"{step_name}: {step_result.summary}")

# 或执行单个步骤
trend_result = orchestrator.analyze_market_trend()
print(f"市场趋势: {trend_result.summary}")