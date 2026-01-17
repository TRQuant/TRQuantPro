"""
文件名: code_6_5_process_candidate_pool.py
保存路径: code_library/006_Chapter6_Factor_Library/6.5/code_6_5_process_candidate_pool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.5_Factor_Pool_Integration_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: process_candidate_pool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def process_candidate_pool(
    self,
    stocks: List[str],
    date: Union[str, datetime],
    period: str = "medium",
    mainline_scores: Optional[Dict[str, float]] = None,
    factor_weights: Optional[Dict[str, float]] = None,
    top_n: int = 30,
) -> List[StockSignal]:
        """
    process_candidate_pool函数
    
    **设计原理**：
    - **核心功能**：实现process_candidate_pool的核心逻辑
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
    # 1. 计算因子评分
    factor_scores = self.calculate_factor_score(
        stocks, date, period, factor_weights
    )
    
    # 2. 获取主线评分（如果提供）
    if mainline_scores is None:
        mainline_scores = {}
    
    # 3. 计算综合评分
    combined_scores = pd.Series(0.0, index=stocks)
    
    for stock in stocks:
        factor_score = factor_scores.get(stock, 0.0)
        mainline_score = mainline_scores.get(stock, 0.0)
        
        # 融合评分
        combined_score = (
            factor_score * self.factor_weight +
            mainline_score * self.mainline_weight
        )
        
        combined_scores[stock] = combined_score
    
    # 4. 排序并选择前N只
    top_stocks = combined_scores.nlargest(top_n)
    
    # 5. 生成选股信号
    signals = []
    for stock, combined_score in top_stocks.items():
        factor_score = factor_scores.get(stock, 0.0)
        mainline_score = mainline_scores.get(stock, 0.0)
        
        # 获取因子明细
        factor_details = {}
        for factor_name in factor_weights or {}:
            try:
                result = self.factor_manager.calculate_factor(
                    factor_name, [stock], date
                )
                if result and not result.values.empty:
                    factor_details[factor_name] = result.values.iloc[0]
            except:
                pass
        
        # 确定信号强度
        if combined_score > 0.8:
            signal_strength = "strong"
        elif combined_score > 0.5:
            signal_strength = "medium"
        else:
            signal_strength = "weak"
        
        # 生成入选理由
        entry_reason = self._generate_entry_reason(
            stock, factor_score, mainline_score, factor_details
        )
        
        signal = StockSignal(
            code=stock,
            factor_score=factor_score,
            mainline_score=mainline_score,
            combined_score=combined_score,
            factor_details=factor_details,
            period=period,
            signal_strength=signal_strength,
            entry_reason=entry_reason,
        )
        
        signals.append(signal)
    
    return signals

def _generate_entry_reason(
    self,
    stock: str,
    factor_score: float,
    mainline_score: float,
    factor_details: Dict[str, float]
) -> str:
    """
    生成入选理由
    
    Args:
        stock: 股票代码
        factor_score: 因子评分
        mainline_score: 主线评分
        factor_details: 因子明细
    
    Returns:
        str: 入选理由
    """
    reasons = []
    
    if factor_score > 0.7:
        reasons.append("因子评分优秀")
    
    if mainline_score > 0.7:
        reasons.append("主线契合度高")
    
    # 找出表现最好的因子
    if factor_details:
        best_factor = max(factor_details.items(), key=lambda x: abs(x[1]))
        reasons.append(f"{best_factor[0]}因子表现突出")
    
    if not reasons:
        reasons.append("综合评分较高")
    
    return "；".join(reasons)