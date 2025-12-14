"""
文件名: code_10_12_Colors.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12_Colors.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: Colors

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/styles/theme.py
class Colors:
    """颜色定义"""
    PRIMARY = "#667eea"
    ACCENT = "#f093fb"
    BG_PRIMARY = "#0d0d14"
    BG_SECONDARY = "#1a1a24"
    BG_TERTIARY = "#252532"
    BG_HOVER = "#2a2a3a"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0c0"
    TEXT_MUTED = "#808080"
    BORDER_PRIMARY = "#333344"
    SUCCESS = "#a6e3a1"
    WARNING = "#f9e2af"
    ERROR = "#f38ba8"

class Typography:
    """字体定义"""
    FONT_FAMILY = "Microsoft YaHei, Arial, sans-serif"
    FONT_SIZE_BASE = 14
    FONT_SIZE_LARGE = 18
    FONT_SIZE_SMALL = 12

class ButtonStyles:
    """按钮样式"""
    PRIMARY = f"""
        QPushButton {{
            background-color: {Colors.PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {Colors.ACCENT};
        }}
        QPushButton:pressed {{
            background-color: {Colors.PRIMARY}dd;
        }}
    """