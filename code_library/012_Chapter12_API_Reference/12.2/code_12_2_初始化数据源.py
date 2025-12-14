"""
文件名: code_12_2_初始化数据源.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_初始化数据源.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 初始化数据源

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.data_source_manager import DataSourceManager

# 创建数据源管理器
ds_manager = DataSourceManager()

# 初始化所有数据源
success = ds_manager.initialize()
if success:
    print("数据源初始化成功")
else:
    print("数据源初始化失败")