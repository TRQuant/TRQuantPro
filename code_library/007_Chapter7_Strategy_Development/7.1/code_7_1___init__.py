"""
文件名: code_7_1___init__.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class TemplateLibrary:
    """策略模板库"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates: Dict[str, StrategyTemplate] = {}
        self._load_templates()
    
    def _load_templates(self):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        template_files = self.templates_dir.glob("*.json")
        for file in template_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    template = StrategyTemplate.from_dict(data)
                    self.templates[template.name] = template
            except Exception as e:
                logger.warning(f"加载模板失败 {file}: {e}")
    
    def get_template(
        self,
        name: str,
        version: str = None
    ) -> Optional[StrategyTemplate]:
        """获取模板"""
        template = self.templates.get(name)
        if not template:
            return None
        
        if version and version != template.version:
            # 从版本管理器获取指定版本
            version_manager = TemplateVersionManager(self.templates_dir)
            return version_manager.get_version(name, version)
        
        return template
    
    def list_templates(
        self,
        platform: PlatformType = None,
        template_type: TemplateType = None
    ) -> List[StrategyTemplate]:
        """列出模板"""
        templates = list(self.templates.values())
        
        if platform:
            templates = [t for t in templates if t.platform == platform]
        
        if template_type:
            templates = [t for t in templates if t.template_type == template_type]
        
        return templates
    
    def search_templates(
        self,
        query: str
    ) -> List[StrategyTemplate]:
        """搜索模板"""
        results = []
        query_lower = query.lower()
        
        for template in self.templates.values():
            if (query_lower in template.name.lower() or
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results