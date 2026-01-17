"""
文件名: code_12_2_get_fundamental_data.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_get_fundamental_data.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 获取基本面数据

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.data_source_manager import DataSourceManager

# 初始化数据源管理器
ds_manager = DataSourceManager()
ds_manager.initialize()

# 获取最新基本面数据
fundamentals = ds_manager.get_fundamentals(
    security="000001.XSHE",
    date=None  # None表示最新数据
)

# 获取指定日期的基本面数据
fundamentals = ds_manager.get_fundamentals(
    security="000001.XSHE",
    date="2024-12-01"
)

# 查看基本面数据
print(f"PE: {fundamentals.get('pe', 'N/A')}")
print(f"PB: {fundamentals.get('pb', 'N/A')}")
print(f"ROE: {fundamentals.get('roe', 'N/A')}")
print(f"总市值: {fundamentals.get('market_cap', 'N/A')}")