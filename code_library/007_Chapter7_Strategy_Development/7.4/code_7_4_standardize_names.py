"""
文件名: code_7_4_standardize_names.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.4/code_7_4_standardize_names.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.4_Strategy_Standardization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: standardize_names

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import re
from typing import Dict, List

class NamingStandardizer:
    """命名规范化器"""
    
    NAMING_RULES = {
        'class': r'^[A-Z][a-zA-Z0-9]*$',  # PascalCase
        'function': r'^[a-z][a-z0-9_]*$',  # snake_case
        'variable': r'^[a-z][a-z0-9_]*$',  # snake_case
        'constant': r'^[A-Z][A-Z0-9_]*$',  # UPPER_SNAKE_CASE
        'private': r'^_[a-z][a-z0-9_]*$'   # _leading_underscore
    }
    
    def standardize_names(self, code: str) -> str:
            """
    standardize_names函数
    
    **设计原理**：
    - **核心功能**：实现standardize_names的核心逻辑
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
        # 解析AST并规范化命名
        import ast
        
        try:
            tree = ast.parse(code)
            standardizer = NameStandardizer()
            standardizer.visit(tree)
            return ast.unparse(tree)
        except Exception as e:
            logger.warning(f"命名规范化失败: {e}")
            return code

class NameStandardizer(ast.NodeTransformer):
    """AST节点转换器，用于规范化命名"""
    
    def visit_FunctionDef(self, node):
        """规范化函数名"""
        if not re.match(r'^[a-z][a-z0-9_]*$', node.name):
            # 转换为snake_case
            node.name = self._to_snake_case(node.name)
        return self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """规范化类名"""
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
            # 转换为PascalCase
            node.name = self._to_pascal_case(node.name)
        return self.generic_visit(node)
    
    def _to_snake_case(self, name: str) -> str:
        """转换为snake_case"""
        # 处理驼峰命名
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _to_pascal_case(self, name: str) -> str:
        """转换为PascalCase"""
        words = name.split('_')
        return ''.join(word.capitalize() for word in words)