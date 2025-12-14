"""
文件名: code_4_3_完整分析流程示例.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_完整分析流程示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 完整分析流程示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 初始化引擎
engine = AShareMainlineEngine()

# 运行完整分析
result = engine.run_full_analysis()

# 查看发现的主线
for mainline in result["mainlines"]:
    print(f"主线: {mainline.name}")
    print(f"评分: {mainline.score.total_score:.1f}")
    print(f"阶段: {mainline.stage.value}")
    print(f"类型: {mainline.type.value}")
    print(f"相关行业: {mainline.industries}")
    print("-" * 60)

# 查看数据溯源
for trace in result["data_traces"]:
    print(f"数据源: {trace.source_name} ({trace.provider})")

# 查看分析步骤
for step in result["analysis_steps"]:
    print(f"步骤: {step.step_name} - {step.method} ({step.duration}ms)")