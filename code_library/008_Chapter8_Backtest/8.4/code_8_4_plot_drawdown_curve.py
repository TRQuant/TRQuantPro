"""
文件名: code_8_4_plot_drawdown_curve.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_plot_drawdown_curve.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: plot_drawdown_curve

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class RiskVisualizer:
    """风险可视化器"""
    
    def plot_drawdown_curve(
        self,
        drawdown_curve: pd.Series,
        save_path: str = None
    ):
            """
    plot_drawdown_curve函数
    
    **设计原理**：
    - **核心功能**：实现plot_drawdown_curve的核心逻辑
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
        fig, ax = plt.subplots(figsize=(12, 6))
        
        dates = drawdown_curve.index
        drawdown_pct = drawdown_curve * 100
        
        ax.fill_between(dates, drawdown_pct, 0, alpha=0.3, color='red', label='回撤')
        ax.plot(dates, drawdown_pct, color='red', linewidth=1.5)
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('回撤 (%)', fontsize=12)
        ax.set_title('回撤曲线', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 格式化x轴日期
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig