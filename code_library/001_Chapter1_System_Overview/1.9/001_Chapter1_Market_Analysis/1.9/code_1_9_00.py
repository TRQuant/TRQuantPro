"""
文件名: code_1_9_00.py
保存路径: code_library/001_Chapter1_System_Overview/1.9/001_Chapter1_Market_Analysis/1.9/code_1_9_00.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.9_Database_Architecture_CN.md
提取时间: 2025-12-13 20:05:31
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 使用pandas + parquet
import pandas as pd

# 保存
df.to_parquet('data/market_data_2025_01.parquet', compression='snappy')

# 读取
df = pd.read_parquet('data/market_data_2025_01.parquet')