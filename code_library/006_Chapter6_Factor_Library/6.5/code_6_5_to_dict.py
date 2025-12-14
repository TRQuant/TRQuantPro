"""
文件名: code_6_5_to_dict.py
保存路径: code_library/006_Chapter6_Factor_Library/6.5/code_6_5_to_dict.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.5_Factor_Pool_Integration_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: to_dict

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from dataclasses import dataclass, field

from .factor_manager import FactorManager
from .factor_evaluator import FactorEvaluator
from .factor_storage import FactorStorage

@dataclass
class StockSignal:
    """股票信号"""
    
    code: str  # 股票代码
    name: str = ""  # 股票名称
    
    # 评分
    factor_score: float = 0.0  # 因子综合评分
    mainline_score: float = 0.0  # 主线评分
    combined_score: float = 0.0  # 综合评分
    
    # 因子明细
    factor_details: Dict[str, float] = field(default_factory=dict)
    
    # 分类
    period: str = "medium"  # 短/中/长期
    sector: str = ""  # 板块
    mainline: str = ""  # 所属主线
    
    # 信号强度
    signal_strength: str = "medium"  # strong/medium/weak
    entry_reason: str = ""  # 入选理由
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "factor_score": self.factor_score,
            "mainline_score": self.mainline_score,
            "combined_score": self.combined_score,
            "factor_details": self.factor_details,
            "period": self.period,
            "sector": self.sector,
            "mainline": self.mainline,
            "signal_strength": self.signal_strength,
            "entry_reason": self.entry_reason,
        }

class FactorPoolIntegration:
        """
    to_dict函数
    
    **设计原理**：
    - **核心功能**：实现to_dict的核心逻辑
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
    
    # 默认因子权重配置
    DEFAULT_FACTOR_WEIGHTS = {
        "short": {
            "PriceMomentum": 0.3,
            "Reversal": 0.2,
            "CompositeFlow": 0.3,
            "RelativeStrength": 0.2,
        },
        "medium": {
            "CompositeValue": 0.25,
            "CompositeGrowth": 0.25,
            "CompositeMomentum": 0.25,
            "CompositeQuality": 0.25,
        },
        "long": {
            "CompositeValue": 0.35,
            "CompositeGrowth": 0.30,
            "CompositeQuality": 0.25,
            "PriceMomentum": 0.10,
        },
    }
    
    def __init__(
        self,
        jq_client=None,
        factor_manager: Optional[FactorManager] = None,
        factor_storage: Optional[FactorStorage] = None,
        mainline_weight: float = 0.4,
        factor_weight: float = 0.6,
    ):
        """
        初始化
        
        Args:
            jq_client: JQData客户端
            factor_manager: 因子管理器（可选，自动创建）
            factor_storage: 因子存储（可选，自动创建）
            mainline_weight: 主线评分权重
            factor_weight: 因子评分权重
        """
        self.jq_client = jq_client
        
        # 因子管理器
        if factor_manager:
            self.factor_manager = factor_manager
        else:
            self.factor_manager = FactorManager(jq_client=jq_client)
        
        # 因子存储
        if factor_storage:
            self.factor_storage = factor_storage
        else:
            self.factor_storage = FactorStorage()
        
        # 权重配置
        self.mainline_weight = mainline_weight
        self.factor_weight = factor_weight