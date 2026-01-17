"""
文件名: code_6_2_register_custom_factor.py
保存路径: code_library/006_Chapter6_Factor_Library/6.2/code_6_2_register_custom_factor.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.2_Factor_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: register_custom_factor

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def register_custom_factor(
    self,
    name: str,
    factor_class: Type[BaseFactor],
    category: str = "custom"
):
        """
    register_custom_factor函数
    
    **设计原理**：
    - **核心功能**：实现register_custom_factor的核心逻辑
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
    # 创建因子实例
    self._factors[name] = factor_class(
        jq_client=self.jq_client,
        cache_dir=self.cache_dir,
        use_cache=self.use_cache
    )
    
    # 添加到分类
    if category not in self.FACTOR_CATEGORIES:
        self.FACTOR_CATEGORIES[category] = []
    self.FACTOR_CATEGORIES[category].append(name)
    
    logger.info(f"注册自定义因子: {name} ({category})")