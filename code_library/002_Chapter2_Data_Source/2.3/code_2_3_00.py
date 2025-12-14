"""
文件名: code_2_3_00.py
保存路径: code_library/002_Chapter2_Data_Source/2.3/code_2_3_00.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.3_Data_Storage_Architecture_CN.md
提取时间: 2025-12-13 20:36:29
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.data_center import DataCenter
import json

# 初始化数据中心
dc = DataCenter()

# 添加数据源配置
dc.add_data_source(
    name="jqdata",
    source_type="jqdata",
    config={
        "username": "your_username",
        "password": "your_password",  # 实际应加密存储
        "api_url": "https://dataapi.joinquant.com"
    },
    priority=10  # 高优先级
)

# 查询数据源配置
config = dc.get_data_source_config("jqdata")
print(f"数据源状态: {config['status']}")
print(f"最后健康检查: {config['last_health_check']}")

# 记录数据获取日志
dc.log_data_fetch(
    source_name="jqdata",
    data_type="daily",
    symbol="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31",
    record_count=245,
    fetch_duration_ms=1200,
    status="success"
)