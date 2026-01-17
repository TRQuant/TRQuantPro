"""
文件名: code_8_6__generate_html_report.py
保存路径: code_library/008_Chapter8_Backtest/8.6/code_8_6__generate_html_report.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.6_Backtest_Report_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: _generate_html_report

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """
    _generate_html_report函数
    
    **设计原理**：
    - **核心功能**：实现_generate_html_report的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>回测报告 - {{ strategy_info.name }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .metric { margin: 10px 0; }
            .chart { margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>回测报告</h1>
        <h2>策略信息</h2>
        <p>策略名称: {{ strategy_info.name }}</p>
        <p>回测期间: {{ strategy_info.start_date }} 至 {{ strategy_info.end_date }}</p>
        
        <h2>收益指标</h2>
        <div class="metric">总收益率: {{ return_metrics.total_return | default('N/A') }}</div>
        <div class="metric">年化收益率: {{ return_metrics.annual_return | default('N/A') }}</div>
        
        <h2>风险指标</h2>
        <div class="metric">最大回撤: {{ risk_metrics.max_drawdown | default('N/A') }}</div>
        <div class="metric">夏普比率: {{ risk_metrics.sharpe_ratio | default('N/A') }}</div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    return template.render(**report_data)