"""
文件名: code_7_4_standardize_parameters.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.4/code_7_4_standardize_parameters.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.4_Strategy_Standardization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: standardize_parameters

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Type, Any, Dict
from dataclasses import dataclass

@dataclass
class ParameterDefinition:
    """参数定义"""
    
    name: str
    type: Type
    default: Any = None
    min_value: Any = None
    max_value: Any = None
    description: str = ""
    required: bool = False

class ParameterStandardizer:
    """参数规范化器"""
    
    def standardize_parameters(
        self,
        code: str,
        parameter_definitions: Dict[str, ParameterDefinition]
    ) -> str:
            """
    standardize_parameters函数
    
    **设计原理**：
    - **核心功能**：实现standardize_parameters的核心逻辑
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
        import ast
        
        try:
            tree = ast.parse(code)
            standardizer = ParameterStandardizerVisitor(parameter_definitions)
            standardizer.visit(tree)
            return ast.unparse(tree)
        except Exception as e:
            logger.warning(f"参数规范化失败: {e}")
            return code
    
    def validate_parameters(
        self,
        parameters: Dict[str, Any],
        parameter_definitions: Dict[str, ParameterDefinition]
    ) -> Tuple[bool, List[str]]:
        """
        验证参数
        
        Args:
            parameters: 参数字典
            parameter_definitions: 参数定义字典
        
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误列表)
        """
        errors = []
        
        for name, value in parameters.items():
            if name not in parameter_definitions:
                errors.append(f"未知参数: {name}")
                continue
            
            param_def = parameter_definitions[name]
            
            # 类型检查
            if not isinstance(value, param_def.type):
                errors.append(
                    f"参数 {name} 类型错误: 期望 {param_def.type.__name__}, "
                    f"实际 {type(value).__name__}"
                )
            
            # 范围检查
            if isinstance(value, (int, float)):
                if param_def.min_value is not None and value < param_def.min_value:
                    errors.append(
                        f"参数 {name} 值过小: {value} < {param_def.min_value}"
                    )
                if param_def.max_value is not None and value > param_def.max_value:
                    errors.append(
                        f"参数 {name} 值过大: {value} > {param_def.max_value}"
                    )
        
        # 检查必需参数
        for name, param_def in parameter_definitions.items():
            if param_def.required and name not in parameters:
                errors.append(f"缺少必需参数: {name}")
        
        return len(errors) == 0, errors