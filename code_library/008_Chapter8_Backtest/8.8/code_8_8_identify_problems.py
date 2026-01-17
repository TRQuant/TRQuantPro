"""
文件名: code_8_8_identify_problems.py
保存路径: code_library/008_Chapter8_Backtest/8.8/code_8_8_identify_problems.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.8_Optimization_Suggestions_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: identify_problems

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, Any, List
from core.backtest_analyzer import BacktestAnalyzer

class ProblemIdentifier:
    """问题识别器"""
    
    def identify_problems(
        self,
        return_analysis: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        trade_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
            """
    identify_problems函数
    
    **设计原理**：
    - **核心功能**：实现identify_problems的核心逻辑
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
        problems = []
        
        # 收益问题
        problems.extend(self._identify_return_problems(return_analysis))
        
        # 风险问题
        problems.extend(self._identify_risk_problems(risk_analysis))
        
        # 交易问题
        problems.extend(self._identify_trade_problems(trade_analysis))
        
        # 按严重程度排序
        problems.sort(key=lambda x: x['severity'], reverse=True)
        
        return problems
    
    def _identify_return_problems(
        self,
        return_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """识别收益问题"""
        problems = []
        
        # 总收益率过低
        if return_analysis.get('total_return', 0) < 0.1:
            problems.append({
                'category': '收益',
                'problem': '总收益率过低',
                'description': f"总收益率仅为{return_analysis.get('total_return', 0):.2%}，低于10%",
                'severity': 'high',
                'suggestion': '检查选股逻辑和择时逻辑，考虑优化因子权重'
            })
        
        # 年化收益率过低
        if return_analysis.get('annual_return', 0) < 0.08:
            problems.append({
                'category': '收益',
                'problem': '年化收益率过低',
                'description': f"年化收益率仅为{return_analysis.get('annual_return', 0):.2%}，低于8%",
                'severity': 'high',
                'suggestion': '优化策略参数，提高收益稳定性'
            })
        
        # 收益稳定性差
        if return_analysis.get('monthly_volatility', 0) > 0.1:
            problems.append({
                'category': '收益',
                'problem': '收益波动性过大',
                'description': f"月度收益波动率为{return_analysis.get('monthly_volatility', 0):.2%}",
                'severity': 'medium',
                'suggestion': '增加风险控制措施，平滑收益曲线'
            })
        
        return problems
    
    def _identify_risk_problems(
        self,
        risk_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """识别风险问题"""
        problems = []
        
        # 最大回撤过大
        if risk_analysis.get('max_drawdown', 0) > 0.2:
            problems.append({
                'category': '风险',
                'problem': '最大回撤过大',
                'description': f"最大回撤为{risk_analysis.get('max_drawdown', 0):.2%}，超过20%",
                'severity': 'high',
                'suggestion': '增加止损机制，控制单只股票仓位'
            })
        
        # 夏普比率过低
        if risk_analysis.get('sharpe_ratio', 0) < 1.0:
            problems.append({
                'category': '风险',
                'problem': '夏普比率过低',
                'description': f"夏普比率为{risk_analysis.get('sharpe_ratio', 0):.2f}，低于1.0",
                'severity': 'medium',
                'suggestion': '优化收益风险比，提高风险调整收益'
            })
        
        return problems
    
    def _identify_trade_problems(
        self,
        trade_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """识别交易问题"""
        problems = []
        
        # 胜率过低
        if trade_analysis.get('win_rate', 0) < 0.5:
            problems.append({
                'category': '交易',
                'problem': '胜率过低',
                'description': f"胜率仅为{trade_analysis.get('win_rate', 0):.2%}，低于50%",
                'severity': 'high',
                'suggestion': '优化选股逻辑，提高买入信号质量'
            })
        
        # 换手率过高
        if trade_analysis.get('turnover_rate', 0) > 10:
            problems.append({
                'category': '交易',
                'problem': '换手率过高',
                'description': f"换手率为{trade_analysis.get('turnover_rate', 0):.2f}，交易过于频繁",
                'severity': 'medium',
                'suggestion': '降低调仓频率，减少交易成本'
            })
        
        return problems