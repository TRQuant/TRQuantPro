"""
文件名: code_8_6_generate_charts.py
保存路径: code_library/008_Chapter8_Backtest/8.6/code_8_6_generate_charts.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.6_Backtest_Report_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: generate_charts

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import base64
from io import BytesIO

class ReportVisualizer:
    """报告可视化器"""
    
    def generate_charts(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: pd.DataFrame = None
    ) -> Dict[str, str]:
            """
    generate_charts函数
    
    **设计原理**：
    - **核心功能**：实现generate_charts的核心逻辑
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
        charts = {}
        
        # 收益曲线图
        charts['equity_curve'] = self._plot_equity_curve(equity_curve, benchmark_curve)
        
        # 回撤曲线图
        charts['drawdown_curve'] = self._plot_drawdown_curve(equity_curve)
        
        return charts
    
    def _plot_equity_curve(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: pd.DataFrame = None
    ) -> str:
        """绘制收益曲线图（返回Base64编码）"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dates = pd.to_datetime(equity_curve['date'])
        strategy_return = (equity_curve['equity'] / equity_curve['equity'].iloc[0] - 1) * 100
        
        ax.plot(dates, strategy_return, label='策略收益', linewidth=2)
        
        if benchmark_curve is not None:
            benchmark_return = (benchmark_curve['equity'] / benchmark_curve['equity'].iloc[0] - 1) * 100
            ax.plot(dates, benchmark_return, label='基准收益', linewidth=2, linestyle='--')
        
        ax.set_xlabel('日期')
        ax.set_ylabel('累计收益率 (%)')
        ax.set_title('收益曲线')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 转换为Base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"