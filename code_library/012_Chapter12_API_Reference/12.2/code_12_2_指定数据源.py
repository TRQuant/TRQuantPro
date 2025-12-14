"""
文件名: code_12_2_指定数据源.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_指定数据源.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 指定数据源

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 优先使用JQData
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31",
    prefer_source=DataSourceType.JQDATA
)

# 如果JQData失败，自动降级到AKShare
# 如果AKShare失败，自动降级到Baostock
# 如果所有数据源都失败，返回错误