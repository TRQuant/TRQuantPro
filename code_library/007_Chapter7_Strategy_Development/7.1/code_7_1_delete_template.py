"""
文件名: code_7_1_delete_template.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_delete_template.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: delete_template

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def delete_template(
    template_name: str,
    force: bool = False
) -> bool:
        """
    delete_template函数
    
    **设计原理**：
    - **核心功能**：实现delete_template的核心逻辑
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
    template = template_manager.get_template(template_name)
    if not template:
        return False
    
    # 检查依赖
    if not force:
        dependents = template_manager.get_dependents(template_name)
        if dependents:
            raise ValueError(
                f"模板被以下策略依赖，无法删除: {dependents}"
            )
    
    # 删除模板
    template_manager.delete_template(template_name)
    
    return True