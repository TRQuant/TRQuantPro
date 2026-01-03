"""
文件名: code_8_4_analyze_sharpe_ratio.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_analyze_sharpe_ratio.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_sharpe_ratio

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class SharpeRatioAnalyzer:
    """夏普比率分析器"""
    
    def analyze_sharpe_ratio(
        self,
        returns: pd.Series,
        risk_free_rate: float = 0.03,
        frequency: str = 'daily'
    ) -> Dict[str, Any]:
        """
        分析夏普比率
        
        Args:
            returns: 收益率序列
            risk_free_rate: 无风险利率（年化）
            frequency: 频率（'daily', 'weekly', 'monthly'）
        
        Returns:
            Dict: 夏普比率分析结果
        """
        # 年化收益率
        if frequency == 'daily':
            annual_return = returns.mean() * 252
            annual_volatility = returns.std() * np.sqrt(252)
        elif frequency == 'weekly':
            annual_return = returns.mean() * 52
            annual_volatility = returns.std() * np.sqrt(52)
        elif frequency == 'monthly':
            annual_return = returns.mean() * 12
            annual_volatility = returns.std() * np.sqrt(12)
        else:
            annual_return = returns.mean() * 252
            annual_volatility = returns.std() * np.sqrt(252)
        
        # 设计原理：夏普比率（风险调整后收益）
        # 原因：衡量单位风险的超额收益，是常用的风险调整指标
        # 公式：夏普比率 = (年化收益率 - 无风险利率) / 年化波动率
        # 为什么这样设计：综合考虑收益和风险，便于策略对比
        # 评价标准：>1为良好，>2为优秀，>3为卓越
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
        
        # 设计原理：索提诺比率（使用下行波动率）
        # 原因：只考虑下行风险，比夏普比率更关注策略的下行保护能力
        # 公式：索提诺比率 = (年化收益率 - 无风险利率) / 年化下行波动率
        # 为什么这样设计：投资者更关注下行风险，上行波动是好事
        # 适用场景：评估策略的下行风险控制能力
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = (annual_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
        
        # Calmar比率（年化收益 / 最大回撤）
        # 需要从净值曲线计算最大回撤
        calmar_ratio = None  # 需要equity_curve
        
        return {
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'risk_free_rate': risk_free_rate,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'excess_return': annual_return - risk_free_rate
        }