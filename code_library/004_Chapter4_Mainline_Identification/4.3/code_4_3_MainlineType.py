"""
文件名: code_4_3_MainlineType.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_MainlineType.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: MainlineType

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from enum import Enum

class MainlineType(Enum):
    """主线类型"""
    
    POLICY = "policy"        # 政策驱动型
    INDUSTRY = "industry"    # 产业趋势型
    EVENT = "event"          # 事件驱动型
    CYCLE = "cycle"          # 周期轮动型
    THEME = "theme"          # 主题概念型