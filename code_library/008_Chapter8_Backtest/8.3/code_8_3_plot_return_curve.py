"""
文件名: code_8_3_plot_return_curve.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_plot_return_curve.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: plot_return_curve

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager

class ReturnVisualizer:
    """收益可视化器"""
    
    def plot_return_curve(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: pd.DataFrame = None,
        save_path: str = None
    ):
            """
    plot_return_curve函数
    
    **设计原理**：
    - **核心功能**：实现plot_return_curve的核心逻辑
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
        
        equity_curve = equity_curve.sort_values('date')
        dates = pd.to_datetime(equity_curve['date'])
        
        # 策略收益曲线
        initial_equity = equity_curve['equity'].iloc[0]
        strategy_return = (equity_curve['equity'] / initial_equity - 1) * 100
        ax.plot(dates, strategy_return, label='策略收益', linewidth=2)
        
        # 基准收益曲线
        if benchmark_curve is not None:
            benchmark_curve = benchmark_curve.sort_values('date')
            benchmark_dates = pd.to_datetime(benchmark_curve['date'])
            initial_benchmark = benchmark_curve['equity'].iloc[0]
            benchmark_return = (benchmark_curve['equity'] / initial_benchmark - 1) * 100
            ax.plot(benchmark_dates, benchmark_return, label='基准收益', linewidth=2, linestyle='--')
        
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('累计收益率 (%)', fontsize=12)
        ax.set_title('收益曲线对比', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # 格式化x轴日期
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_monthly_returns(
        self,
        monthly_returns: pd.Series,
        save_path: str = None
    ):
        """绘制月度收益柱状图"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        colors = ['green' if x > 0 else 'red' for x in monthly_returns.values]
        ax.bar(range(len(monthly_returns)), monthly_returns.values * 100, color=colors, alpha=0.7)
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_xlabel('月份', fontsize=12)
        ax.set_ylabel('月度收益率 (%)', fontsize=12)
        ax.set_title('月度收益分布', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(monthly_returns)))
        ax.set_xticklabels([str(x) for x in monthly_returns.index], rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig