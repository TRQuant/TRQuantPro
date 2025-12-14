"""
文件名: code_2_1_05.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_05.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:28
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 数据源优先级配置
priority_config = {
    'daily': ['jqdata', 'akshare', 'tushare'],      # 日线数据优先级
    'minute': ['jqdata', 'akshare'],                # 分钟数据优先级
    'realtime': ['akshare', 'jqdata'],              # 实时数据优先级
    'fundamental': ['jqdata', 'tushare'],          # 基本面数据优先级
    'factor': ['jqdata'],                          # 因子数据优先级
}