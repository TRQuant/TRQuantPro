"""
文件名: code_8_8_compare_strategies.py
保存路径: code_library/008_Chapter8_Backtest/8.8/code_8_8_compare_strategies.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.8_Optimization_Suggestions_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: compare_strategies

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class StrategyComparator:
    """策略对比器"""
    
    def compare_strategies(
        self,
        strategy1_result: Dict[str, Any],
        strategy2_result: Dict[str, Any]
    ) -> Dict[str, Any]:
            """
    compare_strategies函数
    
    **设计原理**：
    - **核心功能**：实现compare_strategies的核心逻辑
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
        comparison = {
            'return_comparison': self._compare_returns(
                strategy1_result.get('return_metrics', {}),
                strategy2_result.get('return_metrics', {})
            ),
            'risk_comparison': self._compare_risks(
                strategy1_result.get('risk_metrics', {}),
                strategy2_result.get('risk_metrics', {})
            ),
            'trade_comparison': self._compare_trades(
                strategy1_result.get('trade_metrics', {}),
                strategy2_result.get('trade_metrics', {})
            ),
            'overall_improvement': self._calculate_overall_improvement(
                strategy1_result, strategy2_result
            )
        }
        
        return comparison
    
    def _compare_returns(
        self,
        return1: Dict[str, Any],
        return2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """对比收益指标"""
        return {
            'total_return': {
                'strategy1': return1.get('total_return', 0),
                'strategy2': return2.get('total_return', 0),
                'improvement': return2.get('total_return', 0) - return1.get('total_return', 0)
            },
            'annual_return': {
                'strategy1': return1.get('annual_return', 0),
                'strategy2': return2.get('annual_return', 0),
                'improvement': return2.get('annual_return', 0) - return1.get('annual_return', 0)
            }
        }
    
    def _compare_risks(
        self,
        risk1: Dict[str, Any],
        risk2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """对比风险指标"""
        return {
            'max_drawdown': {
                'strategy1': risk1.get('max_drawdown', 0),
                'strategy2': risk2.get('max_drawdown', 0),
                'improvement': risk1.get('max_drawdown', 0) - risk2.get('max_drawdown', 0)  # 回撤越小越好
            },
            'sharpe_ratio': {
                'strategy1': risk1.get('sharpe_ratio', 0),
                'strategy2': risk2.get('sharpe_ratio', 0),
                'improvement': risk2.get('sharpe_ratio', 0) - risk1.get('sharpe_ratio', 0)
            }
        }
    
    def _compare_trades(
        self,
        trade1: Dict[str, Any],
        trade2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """对比交易指标"""
        return {
            'win_rate': {
                'strategy1': trade1.get('win_rate', 0),
                'strategy2': trade2.get('win_rate', 0),
                'improvement': trade2.get('win_rate', 0) - trade1.get('win_rate', 0)
            },
            'turnover_rate': {
                'strategy1': trade1.get('turnover_rate', 0),
                'strategy2': trade2.get('turnover_rate', 0),
                'improvement': trade1.get('turnover_rate', 0) - trade2.get('turnover_rate', 0)  # 换手率越低越好
            }
        }
    
    def _calculate_overall_improvement(
        self,
        strategy1_result: Dict[str, Any],
        strategy2_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """计算整体改进"""
        return {
            'is_improved': True,  # 需要根据具体指标判断
            'improvement_score': 0.0,  # 改进得分
            'key_improvements': []  # 关键改进点
        }