"""
文件名: code_12_2_缓存管理.py
保存路径: code_library/012_Chapter12_API_Reference/12.2/code_12_2_缓存管理.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.2_Data_Source_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 缓存管理

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 清除指定股票的缓存
ds_manager.clear_cache(code="000001.XSHE")

# 清除所有缓存
ds_manager.clear_all_cache()

# 查看缓存状态
cache_status = ds_manager.get_cache_status()
print(f"缓存大小: {cache_status['size']}")
print(f"缓存文件数: {cache_status['file_count']}")