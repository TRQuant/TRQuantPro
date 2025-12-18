"""
文件名: code_4_1_adjust_weights_by_market_regime.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_adjust_weights_by_market_regime.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: adjust_weights_by_market_regime

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def adjust_weights_by_market_regime(
    market_regime: str,
    base_weights: Dict[str, float]
) -> Dict[str, float]:
        """
    adjust_weights_by_market_regime函数
    
    **设计原理**：
    - **核心功能**：实现adjust_weights_by_market_regime的核心逻辑
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
    if market_regime == "risk_on":
        # 牛市：提高技术、资金权重，降低估值权重
        adjusted = base_weights.copy()
        adjusted["technical"] *= 1.2
        adjusted["capital"] *= 1.1
        adjusted["valuation"] *= 0.8
    elif market_regime == "risk_off":
        # 熊市：提高估值、政策权重，降低技术权重
        adjusted = base_weights.copy()
        adjusted["valuation"] *= 1.3
        adjusted["policy"] *= 1.1
        adjusted["technical"] *= 0.7
    else:
        # 震荡市：保持基础权重
        adjusted = base_weights.copy()
    
    # 归一化权重
    total = sum(adjusted.values())
    return {k: v / total for k, v in adjusted.items()}