"""
文件名: code_6_2_to_dict.py
保存路径: code_library/006_Chapter6_Factor_Library/6.2/code_6_2_to_dict.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.2_Factor_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: to_dict

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

@dataclass
class FactorMetadata:
    """因子元数据"""
    factor_name: str
    category: str
    description: str
    definition: str  # 因子定义
    formula: str  # 计算公式
    evidence: str  # 实证证据
    direction: int  # 1=越大越好, -1=越小越好
    parameters: Dict[str, Any]  # 参数定义
    dependencies: List[str]  # 依赖的其他因子或数据
    status: str = "active"  # active, deprecated, experimental
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_name": self.factor_name,
            "category": self.category,
            "description": self.description,
            "definition": self.definition,
            "formula": self.formula,
            "evidence": self.evidence,
            "direction": self.direction,
            "parameters": self.parameters,
            "dependencies": self.dependencies,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }