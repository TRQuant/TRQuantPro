"""
文件名: code_10_4_Colors.py
保存路径: code_library/010_Chapter10_Development_Guide/10.4/code_10_4_Colors.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.4_Desktop_System_Development_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: Colors

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/styles/theme.py
"""
主题系统 - 统一的颜色、字体、样式定义
"""

class Colors:
    """颜色定义"""
    # 主色调
    PRIMARY = "#2563eb"      # 蓝色
    ACCENT = "#f59e0b"       # 金色
    SUCCESS = "#10b981"      # 绿色
    WARNING = "#f59e0b"      # 橙色
    ERROR = "#ef4444"        # 红色
    
    # 背景色
    BG_PRIMARY = "#ffffff"   # 主背景（白色）
    BG_SECONDARY = "#f8fafc" # 次背景（浅灰）
    BG_TERTIARY = "#f1f5f9"  # 三级背景（更浅灰）
    BG_HOVER = "#e2e8f0"     # 悬停背景
    
    # 文字颜色
    TEXT_PRIMARY = "#1e293b"   # 主文字（深灰）
    TEXT_SECONDARY = "#475569" # 次文字（中灰）
    TEXT_MUTED = "#94a3b8"     # 弱文字（浅灰）
    
    # 边框颜色
    BORDER_PRIMARY = "#e2e8f0"   # 主边框
    BORDER_SECONDARY = "#cbd5e1" # 次边框

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
            background-color: #1d4ed8;
        }}
    """