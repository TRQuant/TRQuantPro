"""
文件名: code_7_2_to_dict.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.2/code_7_2_to_dict.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.2_Strategy_Generation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: to_dict

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class StrategyDraft:
    """策略草案定义"""
    
    # 基本信息
    name: str                          # 策略名称
    description: str = ""               # 策略描述
    strategy_type: str = ""             # 策略类型
    platform: str = "ptrade"           # 目标平台
    
    # 股票池
    universe: List[str] = field(default_factory=list)  # 股票池
    
    # 选股逻辑
    entry: Dict[str, Any] = field(default_factory=dict)  # 买入条件
    exit: Dict[str, Any] = field(default_factory=dict)   # 卖出条件
    
    # 仓位管理
    position_sizing: Dict[str, Any] = field(default_factory=dict)  # 仓位配置
    
    # 风险控制
    risk: Dict[str, Any] = field(default_factory=dict)  # 风控配置
    
    # 成本配置
    cost: Dict[str, Any] = field(default_factory=dict)  # 成本配置
    
    # 因子配置
    factors: List[str] = field(default_factory=list)  # 使用的因子列表
    factor_weights: Dict[str, float] = field(default_factory=dict)  # 因子权重
    
    # 引用信息
    research_card_refs: List[str] = field(default_factory=list)  # 研究卡引用
    rule_refs: List[str] = field(default_factory=list)  # 规则引用
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
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
        return {
            'name': self.name,
            'description': self.description,
            'strategy_type': self.strategy_type,
            'platform': self.platform,
            'universe': self.universe,
            'entry': self.entry,
            'exit': self.exit,
            'position_sizing': self.position_sizing,
            'risk': self.risk,
            'cost': self.cost,
            'factors': self.factors,
            'factor_weights': self.factor_weights,
            'research_card_refs': self.research_card_refs,
            'rule_refs': self.rule_refs,
            'created_at': self.created_at,
            'version': self.version
        }