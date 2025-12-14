"""
文件名: code_7_1_validate_parameters.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_validate_parameters.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: validate_parameters

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def validate_parameters(
    template_params: Dict[str, TemplateParameter],
    provided_params: Dict[str, Any]
) -> Tuple[bool, List[str]]:
        """
    validate_parameters函数
    
    **设计原理**：
    - **核心功能**：实现validate_parameters的核心逻辑
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
    errors = []
    
    # 检查必需参数
    for name, param_def in template_params.items():
        if param_def.required and name not in provided_params:
            errors.append(f"缺少必需参数: {name}")
    
    # 验证参数值
    for name, value in provided_params.items():
        if name not in template_params:
            errors.append(f"未知参数: {name}")
            continue
        
        param_def = template_params[name]
        
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
        
        # 可选值检查
        if param_def.choices and value not in param_def.choices:
            errors.append(
                f"参数 {name} 值不在可选范围内: {value} not in {param_def.choices}"
            )
    
    return len(errors) == 0, errors