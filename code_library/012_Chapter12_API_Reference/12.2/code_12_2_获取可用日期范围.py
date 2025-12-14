"""
文件名: code_12_2_获取可用日期范围.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_获取可用日期范围.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 获取可用日期范围

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 获取所有数据源的最大日期范围
start_date, end_date = ds_manager.get_available_date_range()
print(f"可用日期范围: {start_date} ~ {end_date}")

# 获取指定数据源的日期范围
jq_start, jq_end = ds_manager.get_available_date_range(DataSourceType.JQDATA)
print(f"JQData日期范围: {jq_start} ~ {jq_end}")