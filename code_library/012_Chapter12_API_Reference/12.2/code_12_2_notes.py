"""
文件名: code_12_2_notes.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_notes.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 注意事项

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 首次获取数据（从数据源获取并缓存）
# 设计原理：首次获取时，数据源返回数据后自动缓存到MongoDB
# 缓存键：基于code、start_date、end_date、frequency生成
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# 再次获取相同数据（从缓存获取，速度更快）
# 设计原理：缓存命中时，直接从MongoDB读取，避免请求数据源
# 性能提升：缓存读取速度比数据源API快10-100倍
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)