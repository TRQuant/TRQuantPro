"""策略模板库"""
from .strategy_templates import (
    StrategyTemplate,
    MomentumTemplate,
    ValueTemplate,
    TrendTemplate,
    MultiFactorTemplate,
    get_template,
    list_templates
)

from .advanced_templates import (
    RotationTemplate,
    PairTradingTemplate,
    MeanReversionTemplate,
    BreakoutTemplate,
    get_advanced_template,
    list_advanced_templates,
    ADVANCED_TEMPLATES
)

# 基础模板名称映射
BASIC_TEMPLATE_NAMES = ["momentum", "value", "trend", "multi_factor"]

def list_all_templates():
    """列出所有模板名称"""
    return BASIC_TEMPLATE_NAMES + list_advanced_templates()

def get_any_template(name: str):
    """获取任意模板（基础或高级）"""
    if name in BASIC_TEMPLATE_NAMES:
        return get_template(name)
    return get_advanced_template(name)

def get_all_template_info():
    """获取所有模板的详细信息"""
    info = []
    
    # 基础模板
    for name in BASIC_TEMPLATE_NAMES:
        t = get_template(name)
        if t:
            info.append({
                "name": name,
                "description": getattr(t, "description", "基础策略"),
                "type": "basic"
            })
    
    # 高级模板
    for name in list_advanced_templates():
        t = get_advanced_template(name)
        if t:
            info.append({
                "name": name,
                "description": getattr(t, "description", "高级策略"),
                "type": "advanced"
            })
    
    return info
