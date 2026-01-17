"""
文件名: code_12_2_query_data_source_status.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_query_data_source_status.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 查询数据源状态

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 获取所有数据源状态
all_status = ds_manager.get_all_status()
for source_type, status in all_status.items():
    print(f"{source_type.value}: {status.is_available}")

# 获取指定数据源状态
from core.data_source_manager import DataSourceType
jq_status = ds_manager.get_source_status(DataSourceType.JQDATA)
if jq_status:
    print(f"JQData状态: {jq_status.is_available}")
    print(f"账户类型: {jq_status.account_type.value}")
    print(f"日期范围: {jq_status.start_date} ~ {jq_status.end_date}")

# 获取JQData账户类型
account_type = ds_manager.get_jqdata_account_type()
print(f"JQData账户类型: {account_type.value}")