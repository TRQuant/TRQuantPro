"""
文件名: code_6_1_stocks.py
保存路径: code_library/006_Chapter6_Factor_Library/6.1/code_6_1_stocks.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.1_Factor_Calculation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: stocks

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

from dataclasses import dataclass, field

@dataclass
class FactorResult:
    """因子计算结果"""
    
    name: str  # 因子名称
    date: datetime  # 计算日期
    values: pd.Series  # 因子值（index为股票代码）
    raw_values: Optional[pd.Series] = None  # 原始因子值（未处理）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def stocks(self) -> List[str]:
            """
    stocks函数
    
    **设计原理**：
    - **核心功能**：实现stocks的核心逻辑
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
        return self.values.index.tolist()
    
    @property
    def valid_count(self) -> int:
        """有效值数量"""
        return self.values.notna().sum()
    
    @property
    def coverage(self) -> float:
        """覆盖率"""
        return self.valid_count / len(self.values) if len(self.values) > 0 else 0
    
    def top_n(self, n: int = 30) -> List[str]:
        """获取因子值最高的N只股票"""
        return self.values.nlargest(n).index.tolist()
    
    def bottom_n(self, n: int = 30) -> List[str]:
        """获取因子值最低的N只股票"""
        return self.values.nsmallest(n).index.tolist()