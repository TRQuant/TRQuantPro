"""
文件名: code_12_3_加载配置.py
保存路径: code_library/012_Chapter12_API_Reference/12.3/code_12_3_加载配置.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.3_Config_Reference_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 加载配置

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from config.config_manager import get_config_manager

config_manager = get_config_manager()

# 加载JQData配置
jq_config = config_manager.get_jqdata_config()
print(f"JQData用户名: {jq_config.get('username', 'N/A')}")

# 加载其他配置
postgres_config = config_manager.load_config('postgresql_config.json')