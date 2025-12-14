"""
文件名: code_4_3_MainlineStage.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_MainlineStage.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: MainlineStage

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from enum import Enum

class MainlineStage(Enum):
    """主线生命周期阶段"""
    
    EMERGING = "emerging"    # 启动期 - 政策信号出现，机构开始布局
    GROWING = "growing"      # 成长期 - 资金持续流入，业绩开始兑现
    MATURE = "mature"        # 成熟期 - 共识形成，估值较高
    DECLINING = "declining"  # 衰退期 - 资金撤离，预期下修