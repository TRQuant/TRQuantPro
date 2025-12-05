# -*- coding: utf-8 -*-
"""
韬睿量化 - UI样式规范
====================

此文件定义了UI开发的强制性规范，所有新组件必须遵循这些规则。

## 核心原则

1. 高对比度优先 - 确保文字始终可读
2. 尺寸适配 - 容器必须能容纳内容
3. 一致性 - 使用预定义的样式常量
"""

from gui.styles.theme import Colors, Typography

# ============================================================
# 1. 颜色对比度规范
# ============================================================

class ContrastRules:
    """
    颜色对比度规则 - 必须遵循
    
    ✅ 正确做法：
    - 深色背景 (#0d0d14, #12121f, #181825) + 亮色文字 (#ffffff, #cdd6f4)
    - 亮色背景 (#3B82F6, #10B981, #F59E0B) + 深色文字 (#0d0d14, #1a1a2e)
    
    ❌ 错误做法：
    - 半透明彩色背景 + 同色系文字 (如 #10B98120 背景 + #10B981 文字)
    - 深色背景 + 深色文字
    - 亮色背景 + 亮色文字
    """
    
    # 深色背景上使用的文字颜色
    TEXT_ON_DARK = {
        "primary": "#ffffff",      # 主要文字 - 纯白
        "secondary": "#cdd6f4",    # 次要文字 - 亮灰
        "muted": "#9ca3af",        # 静音文字 - 中灰（最低可接受）
    }
    
    # 亮色/彩色背景上使用的文字颜色
    TEXT_ON_LIGHT = {
        "primary": "#0d0d14",      # 主要文字 - 深黑
        "secondary": "#1a1a2e",    # 次要文字 - 深灰
    }
    
    # 禁止的颜色组合
    FORBIDDEN_COMBINATIONS = [
        # (背景透明度, 文字颜色) - 同色系
        ("彩色20", "同色彩色"),   # 如 #10B98120 + #10B981
        ("彩色15", "同色彩色"),
        ("彩色10", "同色彩色"),
    ]


# ============================================================
# 2. 卡片尺寸规范
# ============================================================

class CardSizeRules:
    """
    卡片尺寸规则 - 确保内容不溢出
    
    原则：宽度 = 最长文字宽度 + padding*2 + 安全边距
    """
    
    # 最小卡片尺寸（根据内容类型）
    WORKFLOW_STEP = {
        "min_width": 120,
        "min_height": 90,
        "max_title_chars": 4,      # 标题最多4个汉字
        "max_desc_chars": 5,       # 描述最多5个汉字
        "padding": 8,
    }
    
    FEATURE_CARD = {
        "min_width": 180,
        "min_height": 120,
        "max_title_chars": 8,
        "padding": 16,
    }
    
    MODULE_CARD = {
        "min_width": 280,
        "min_height": 160,
        "padding": 20,
    }
    
    # 字体大小与容器宽度的关系
    FONT_SIZE_RULES = {
        # 容器宽度: 最大字体大小
        100: 10,
        120: 11,
        150: 12,
        180: 13,
        200: 14,
        250: 15,
        300: 16,
    }
    
    @staticmethod
    def get_max_font_size(container_width: int) -> int:
        """根据容器宽度获取最大字体大小"""
        for width, size in sorted(CardSizeRules.FONT_SIZE_RULES.items()):
            if container_width <= width:
                return size
        return 16


# ============================================================
# 3. 文字长度规范
# ============================================================

class TextLengthRules:
    """
    文字长度规则 - 避免溢出
    """
    
    # 不同场景的最大字符数（汉字）
    MAX_CHARS = {
        "workflow_title": 4,       # 工作流程标题
        "workflow_desc": 5,        # 工作流程描述
        "card_title": 8,           # 卡片标题
        "card_subtitle": 12,       # 卡片副标题
        "button_text": 6,          # 按钮文字
        "tag_text": 6,             # 标签文字
        "tab_title": 6,            # Tab标题
    }
    
    @staticmethod
    def truncate(text: str, max_chars: int, suffix: str = "...") -> str:
        """截断过长的文字"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars - len(suffix)] + suffix


# ============================================================
# 4. 预定义样式模板
# ============================================================

class StyleTemplates:
    """
    预定义样式模板 - 直接使用，避免手写样式出错
    """
    
    @staticmethod
    def workflow_step_card(color: str) -> str:
        """工作流程步骤卡片样式"""
        return f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 2px solid {color}50;
                border-radius: 10px;
            }}
            QFrame:hover {{
                border: 2px solid {color};
                background-color: {color}15;
            }}
        """
    
    @staticmethod
    def step_number(color: str) -> str:
        """步骤序号样式 - 彩色背景+深色文字"""
        return f"""
            font-size: 11px;
            font-weight: 700;
            color: #0d0d14;
            background-color: {color};
            padding: 2px 6px;
            border-radius: 8px;
        """
    
    @staticmethod
    def step_title() -> str:
        """步骤标题样式 - 白色文字"""
        return "font-size: 12px; font-weight: 600; color: #ffffff;"
    
    @staticmethod
    def step_desc() -> str:
        """步骤描述样式 - 亮灰文字"""
        return "font-size: 10px; color: #cdd6f4;"
    
    @staticmethod
    def colored_tag(color: str) -> str:
        """彩色标签样式 - 彩色背景+深色文字"""
        return f"""
            font-size: 11px;
            font-weight: 600;
            color: #0d0d14;
            background-color: {color};
            padding: 6px 12px;
            border-radius: 14px;
        """
    
    @staticmethod
    def indicator_tag() -> str:
        """指标标签样式 - 深色背景+亮色文字"""
        return f"""
            font-size: 9px;
            color: {Colors.TEXT_SECONDARY};
            background-color: {Colors.BG_TERTIARY};
            padding: 2px 6px;
            border-radius: 4px;
        """
    
    @staticmethod
    def flow_step(color: str) -> str:
        """流程步骤样式 - 实心彩色背景+深色文字"""
        return f"""
            QFrame {{
                background-color: {color};
                border: none;
                border-radius: 10px;
            }}
        """
    
    @staticmethod
    def flow_step_title() -> str:
        """流程步骤标题 - 深色文字"""
        return "font-size: 13px; font-weight: 700; color: #0d0d14;"
    
    @staticmethod
    def flow_step_desc() -> str:
        """流程步骤描述 - 深色文字"""
        return "font-size: 11px; color: #1a1a2e;"


# ============================================================
# 5. 验证函数
# ============================================================

def validate_text_length(text: str, context: str) -> bool:
    """
    验证文字长度是否符合规范
    
    Args:
        text: 要验证的文字
        context: 使用场景 (workflow_title, card_title, etc.)
    
    Returns:
        是否符合规范
    """
    max_chars = TextLengthRules.MAX_CHARS.get(context, 20)
    return len(text) <= max_chars


def get_safe_text(text: str, context: str) -> str:
    """
    获取安全的文字（自动截断）
    
    Args:
        text: 原始文字
        context: 使用场景
    
    Returns:
        截断后的文字
    """
    max_chars = TextLengthRules.MAX_CHARS.get(context, 20)
    return TextLengthRules.truncate(text, max_chars)





