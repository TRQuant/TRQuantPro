"""
文件名: code_5_3_weight_config.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_weight_config.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: 权重配置

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

DEFAULT_WEIGHTS = {
    'technical': 0.30,   # 技术面权重：30%
    'capital': 0.30,     # 资金面权重：30%
    'fundamental': 0.30, # 基本面权重：30%
    'sentiment': 0.10    # 情绪面权重：10%
}