"""
文件名: code_8_1_聚宽数据源集成.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_聚宽数据源集成.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 聚宽数据源集成

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.data_source_manager import DataSourceManager
from core.data_provider import DataProvider

# 初始化数据源管理器
data_manager = DataSourceManager()

# 配置聚宽数据源
from config.config_manager import get_config_manager
config_manager = get_config_manager()
jq_config = config_manager.get_jqdata_config()

# 初始化聚宽客户端
data_manager.init_jqdata(
    username=jq_config.get('username'),
    password=jq_config.get('password')
)

# 创建数据提供者
data_provider = DataProvider(jq_client=data_manager.get_jq_client())

# 获取价格数据（聚宽格式）
securities = ['000001.XSHE', '000002.XSHE']  # 聚宽股票代码格式
start_date = '2023-01-01'
end_date = '2024-12-31'

price_data = data_provider.get_price(
    securities=securities,
    start_date=start_date,
    end_date=end_date,
    frequency='day'  # 日线数据
)

# 数据格式：聚宽标准格式
# Index: 日期
# Columns: open, high, low, close, volume
print(price_data.head())