"""
文件名: code_6_3_is_significant.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3_is_significant.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: is_significant

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from scipy import stats
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np

@dataclass
class ICResult:
    """IC计算结果"""
    factor_name: str
    date: datetime
    ic: float  # 信息系数（Pearson）
    rank_ic: float  # 秩相关IC（Spearman）
    p_value: float  # 显著性检验p值
    n_stocks: int  # 股票数量
    
    @property
    def is_significant(self) -> bool:
            """
    is_significant函数
    
    **设计原理**：
    - **核心功能**：实现is_significant的核心逻辑
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
        return self.p_value < 0.05

class FactorEvaluator:
    """因子评估器"""
    
    def __init__(self, jq_client=None):
        """
        初始化评估器
        
        Args:
            jq_client: JQData客户端
        """
        self.jq_client = jq_client
    
    def calculate_ic(
        self, 
        factor_values: pd.Series, 
        forward_returns: pd.Series, 
        method: str = "spearman"
    ) -> ICResult:
        """
        计算信息系数(IC)
        
        Args:
            factor_values: 因子值
            forward_returns: 未来收益率
            method: 相关系数方法 ('spearman' or 'pearson')
        
        Returns:
            ICResult: IC计算结果
        """
        # 对齐数据
        common_idx = factor_values.dropna().index.intersection(
            forward_returns.dropna().index
        )
        
        if len(common_idx) < 10:
            logger.warning(f"有效样本不足: {len(common_idx)}")
            return ICResult(
                factor_name="",
                date=datetime.now(),
                ic=np.nan,
                rank_ic=np.nan,
                p_value=1.0,
                n_stocks=len(common_idx),
            )
        
        factor = factor_values.loc[common_idx]
        returns = forward_returns.loc[common_idx]
        
        # 计算秩相关IC（Spearman）
        rank_ic, p_value = stats.spearmanr(factor, returns)
        
        # 计算Pearson IC
        pearson_ic, _ = stats.pearsonr(factor, returns)
        
        return ICResult(
            factor_name=getattr(factor_values, "name", ""),
            date=datetime.now(),
            ic=pearson_ic,
            rank_ic=rank_ic,
            p_value=p_value,
            n_stocks=len(common_idx),
        )