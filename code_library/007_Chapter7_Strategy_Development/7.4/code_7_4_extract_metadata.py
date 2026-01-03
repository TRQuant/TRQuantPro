"""
文件名: code_7_4_extract_metadata.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.4/code_7_4_extract_metadata.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.4_Strategy_Standardization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: extract_metadata

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

@dataclass
class StrategyMetadata:
    """策略元数据定义"""
    
    name: str
    description: str = ""
    author: str = ""
    version: str = "1.0.0"
    platform: str = "ptrade"
    strategy_type: str = ""
    factors: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    research_card_refs: List[str] = field(default_factory=list)
    rule_refs: List[str] = field(default_factory=list)

class MetadataStandardizer:
    """元数据规范化器"""
    
    def extract_metadata(self, code: str) -> StrategyMetadata:
            """
    extract_metadata函数
    
    **设计原理**：
    - **核心功能**：实现extract_metadata的核心逻辑
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
        metadata = StrategyMetadata(name="未命名策略")
        
        # 从文档字符串提取
        docstring = self._extract_docstring(code)
        if docstring:
            metadata.description = self._parse_description(docstring)
            metadata.author = self._parse_author(docstring)
        
        # 从代码中提取参数
        metadata.parameters = self._extract_parameters(code)
        
        # 从代码中提取因子
        metadata.factors = self._extract_factors(code)
        
        return metadata
    
    def validate_metadata(
        self,
        metadata: StrategyMetadata
    ) -> Tuple[bool, List[str]]:
        """
        验证元数据
        
        Args:
            metadata: 策略元数据
        
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误列表)
        """
        errors = []
        
        # 检查必需字段
        if not metadata.name:
            errors.append("策略名称不能为空")
        
        if not metadata.description:
            errors.append("策略描述不能为空")
        
        if not metadata.platform:
            errors.append("平台类型不能为空")
        
        # 验证版本号格式
        if not re.match(r'^\d+\.\d+\.\d+$', metadata.version):
            errors.append(f"版本号格式错误: {metadata.version}")
        
        return len(errors) == 0, errors