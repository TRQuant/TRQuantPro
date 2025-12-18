"""
文件名: code_12_2_get_price_data.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_get_price_data.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 获取价格数据

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.data_source_manager import DataSourceManager, DataSourceType

# 初始化数据源管理器
ds_manager = DataSourceManager()
ds_manager.initialize()

# 获取价格数据
result = ds_manager.get_price(
    code="000001.XSHE",  # 股票代码
    start_date="2024-01-01",  # 开始日期
    end_date="2024-12-31",  # 结束日期
    frequency="daily",  # 数据频率: "daily", "1m", "5m", "15m", "30m", "60m"
    fields=["open", "close", "high", "low", "volume"],  # 字段列表
    prefer_source=None  # 优先数据源（可选）
)

# 检查结果
if result.success:
    data = result.data
    print(f"数据源: {result.source.value}")
    print(f"数据形状: {data.shape}")
    print(data.head())
else:
    print(f"获取数据失败: {result.error}")