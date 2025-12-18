"""
文件名: code_12_1_class.py
保存路径: code_library/012_Chapter12_API_Reference/12.1/code_12_1_class.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.1_Module_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: class

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

@dataclass
class MarketTrendResult:
    """市场趋势分析结果"""
    
    short_term: TrendSignal  # 短期趋势（1-8周）
    medium_term: TrendSignal  # 中期趋势（9-24周）
    long_term: TrendSignal  # 长期趋势（25-48周）
    composite_score: float  # 综合评分（-100到+100）
    market_phase: str  # 市场阶段（牛市/熊市/震荡/复苏）
    analysis_date: datetime  # 分析日期
    index_code: str  # 指数代码