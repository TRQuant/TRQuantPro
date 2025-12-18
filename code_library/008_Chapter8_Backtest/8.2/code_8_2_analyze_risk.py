"""
文件名: code_8_2_analyze_risk.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_analyze_risk.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_risk

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

class RiskAnalyzer:
    """风险分析器"""
    
    def analyze_risk(
        self,
        equity_curve: pd.DataFrame,
        returns: pd.Series,
        benchmark_returns: pd.Series = None
    ) -> Dict[str, Any]:
        """
        分析风险
        
        Args:
            equity_curve: 净值曲线
            returns: 日收益率序列
            benchmark_returns: 基准收益率序列（可选）
        
        Returns:
            Dict: 风险分析结果
        """
        # 最大回撤
        max_drawdown, max_drawdown_duration, drawdown_curve = self._calculate_max_drawdown(equity_curve)
        
        # 设计原理：波动率年化
        # 原因：日波动率需要年化，便于比较和评估
        # 公式：年化波动率 = 日波动率 * sqrt(252)，252为年交易日数
        volatility = returns.std() * np.sqrt(252)
        
        # 设计原理：下行波动率（只考虑负收益）
        # 原因：下行波动率更准确反映策略的下行风险
        # 使用场景：计算索提诺比率时使用，比夏普比率更关注下行风险
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        # 设计原理：夏普比率（风险调整后收益）
        # 原因：衡量单位风险的超额收益，是常用的风险调整指标
        # 公式：夏普比率 = (年化收益率 - 无风险利率) / 年化波动率
        # 无风险利率：默认3%，可根据实际情况调整
        risk_free_rate = 0.03
        sharpe_ratio = (returns.mean() * 252 - risk_free_rate) / volatility if volatility > 0 else 0
        
        # 设计原理：索提诺比率（使用下行波动率）
        # 原因：只考虑下行风险，比夏普比率更关注策略的下行保护能力
        # 公式：索提诺比率 = (年化收益率 - 无风险利率) / 年化下行波动率
        # 适用场景：评估策略的下行风险控制能力
        sortino_ratio = (returns.mean() * 252 - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
        
        # 信息比率（相对于基准）
        information_ratio = None
        if benchmark_returns is not None:
            excess_returns = returns - benchmark_returns
            information_ratio = excess_returns.mean() * np.sqrt(252) / excess_returns.std() if excess_returns.std() > 0 else 0
        
        # VaR（风险价值，95%置信度）
        var_95 = np.percentile(returns, 5) * np.sqrt(252)
        
        # CVaR（条件风险价值）
        cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * np.sqrt(252) if len(returns[returns <= np.percentile(returns, 5)]) > 0 else 0
        
        # 回撤统计
        drawdown_stats = self._analyze_drawdowns(drawdown_curve)
        
        return {
            'max_drawdown': max_drawdown,
            'max_drawdown_duration': max_drawdown_duration,
            'volatility': volatility,
            'downside_volatility': downside_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'information_ratio': information_ratio,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'drawdown_stats': drawdown_stats
        }
    
    def _calculate_max_drawdown(
        self,
        equity_curve: pd.DataFrame
    ) -> Tuple[float, int, pd.Series]:
        """
        计算最大回撤
        
        **设计原理**：
        - **累计最高值法**：使用累计最高值计算回撤，避免重复计算
        - **相对回撤**：回撤 = (当前净值 - 历史最高净值) / 历史最高净值
        - **时间追踪**：记录最大回撤的开始和结束时间，计算持续时间
        
        **为什么这样设计**：
        1. **效率**：累计最高值法只需一次遍历，时间复杂度O(n)
        2. **准确性**：相对回撤更准确反映策略风险，不受初始资金影响
        3. **完整性**：同时计算回撤值和持续时间，提供全面的风险信息
        
        **算法说明**：
        - 使用`np.maximum.accumulate`计算累计最高值
        - 回撤 = (当前净值 - 累计最高净值) / 累计最高净值
        - 最大回撤 = 回撤序列的最小值（绝对值）
        
        **使用场景**：
        - 回测结果分析时，评估策略风险
        - 策略优化时，作为优化目标之一
        - 策略对比时，比较不同策略的风险水平
        
        **注意事项**：
        - 回撤为负值，计算时需要使用绝对值
        - 最大回撤持续时间从历史最高点到回撤最低点
        
        Returns:
            Tuple: (最大回撤, 最大回撤持续时间(天), 回撤曲线)
        """
        # 设计原理：按日期排序
        # 原因：回撤计算需要按时间顺序，确保累计最高值计算正确
        equity_curve = equity_curve.sort_values('date')
        equity = equity_curve['equity'].values
        
        # 设计原理：使用累计最高值计算回撤
        # 原因：只需一次遍历，效率高（O(n)）
        # 实现方式：np.maximum.accumulate计算累计最大值
        cumulative_max = np.maximum.accumulate(equity)
        
        # 设计原理：相对回撤计算
        # 原因：相对回撤更准确反映策略风险，不受初始资金影响
        # 公式：回撤 = (当前净值 - 历史最高净值) / 历史最高净值
        drawdown = (equity - cumulative_max) / cumulative_max
        drawdown_series = pd.Series(drawdown, index=equity_curve['date'])
        
        # 设计原理：最大回撤为回撤序列的最小值（绝对值）
        # 原因：回撤为负值，最小值对应最大回撤
        max_drawdown = abs(drawdown.min())
        
        # 设计原理：计算最大回撤持续时间
        # 原因：持续时间反映策略恢复能力，是重要的风险指标
        # 实现方式：从历史最高点到回撤最低点的时间差
        max_dd_idx = drawdown.idxmin()
        max_dd_start = equity_curve[equity_curve['equity'] == cumulative_max[drawdown.idxmin()]]['date'].iloc[0]
        max_dd_end = equity_curve.loc[equity_curve['date'] == max_dd_idx, 'date'].iloc[0]
        max_drawdown_duration = (max_dd_end - max_dd_start).days
        
        return max_drawdown, max_drawdown_duration, drawdown_series
    
    def _analyze_drawdowns(self, drawdown_curve: pd.Series) -> Dict[str, Any]:
        """分析回撤统计"""
        drawdowns = drawdown_curve[drawdown_curve < 0]
        
        return {
            'avg_drawdown': abs(drawdowns.mean()) if len(drawdowns) > 0 else 0,
            'max_drawdown': abs(drawdowns.min()) if len(drawdowns) > 0 else 0,
            'drawdown_count': len(drawdowns[drawdowns < drawdowns.shift(1)]),  # 回撤次数
            'avg_drawdown_duration': 0  # 需要进一步计算
        }