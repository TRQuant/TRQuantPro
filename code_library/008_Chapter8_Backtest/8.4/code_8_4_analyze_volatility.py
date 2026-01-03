"""
文件名: code_8_4_analyze_volatility.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_analyze_volatility.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_volatility

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class VolatilityAnalyzer:
    """波动率分析器"""
    
    def analyze_volatility(
        self,
        returns: pd.Series,
        frequency: str = 'daily'
    ) -> Dict[str, Any]:
        """
        分析波动率
        
        Args:
            returns: 收益率序列
            frequency: 频率（'daily', 'weekly', 'monthly'）
        
        Returns:
            Dict: 波动率分析结果
        """
        # 设计原理：年化波动率计算
        # 原因：不同频率的收益率需要不同的年化因子
        # 公式：年化波动率 = 收益率标准差 * sqrt(年交易天数)
        # 年交易天数：日线252天，周线52周，月线12月
        # 为什么这样设计：统一量纲，便于不同频率的策略对比
        if frequency == 'daily':
            annual_volatility = returns.std() * np.sqrt(252)
        elif frequency == 'weekly':
            annual_volatility = returns.std() * np.sqrt(52)
        elif frequency == 'monthly':
            annual_volatility = returns.std() * np.sqrt(12)
        else:
            annual_volatility = returns.std() * np.sqrt(252)
        
        # 设计原理：下行波动率（只考虑负收益）
        # 原因：下行波动率更准确反映策略的下行风险
        # 使用场景：计算索提诺比率时使用，比夏普比率更关注下行风险
        # 为什么这样设计：投资者更关注下行风险，上行波动是好事
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        # 设计原理：上行波动率（只考虑正收益）
        # 原因：上行波动率反映策略的收益波动
        # 使用场景：分析策略的收益稳定性
        # 为什么这样设计：上行波动率低表示收益稳定，上行波动率高表示收益波动大
        upside_returns = returns[returns > 0]
        upside_volatility = upside_returns.std() * np.sqrt(252) if len(upside_returns) > 0 else 0
        
        # 波动率分解（按时间段）
        volatility_by_period = self._decompose_volatility_by_period(returns)
        
        return {
            'annual_volatility': annual_volatility,
            'downside_volatility': downside_volatility,
            'upside_volatility': upside_volatility,
            'volatility_ratio': downside_volatility / annual_volatility if annual_volatility > 0 else 0,
            'volatility_by_period': volatility_by_period
        }
    
    def _decompose_volatility_by_period(self, returns: pd.Series) -> Dict[str, float]:
        """按时间段分解波动率"""
        returns.index = pd.to_datetime(returns.index)
        
        # 按年度分解
        yearly_vol = returns.groupby(returns.index.year).std() * np.sqrt(252)
        
        # 按季度分解
        quarterly_vol = returns.groupby([returns.index.year, returns.index.quarter]).std() * np.sqrt(252)
        
        return {
            'yearly_volatility': yearly_vol.to_dict(),
            'quarterly_volatility': quarterly_vol.to_dict()
        }