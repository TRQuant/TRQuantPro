"""
文件名: code_4_1_维度配置.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_维度配置.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 维度配置

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

SCORING_CONFIG = {
    # 维度权重配置（参考中金、华泰多因子框架）
    "dimension_weights": {
        "policy": 0.20,       # 政策支持度
        "capital": 0.25,      # 资金认可度
        "industry": 0.20,     # 产业景气度
        "technical": 0.15,    # 技术形态度
        "valuation": 0.10,    # 估值合理度
        "foresight": 0.10,    # 前瞻领先度
    },
    # ... 各维度因子配置
}