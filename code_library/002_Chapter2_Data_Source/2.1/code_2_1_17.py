"""
文件名: code_2_1_17.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_17.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:37:09
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 在Cursor中调用MCP工具
# 查询数据源管理相关文档
results = kb.query(
    query="数据源管理接口设计 BaseDataSource",
    scope="both",  # manual + engineering
    top_k=5
)

# 查询结果包含：
# - 开发手册中的相关章节
# - 代码库中的BaseDataSource实现
# - 数据源管理器的使用示例