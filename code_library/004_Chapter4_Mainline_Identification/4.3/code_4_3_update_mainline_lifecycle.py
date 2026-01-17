"""
文件名: code_4_3_update_mainline_lifecycle.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_update_mainline_lifecycle.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: update_mainline_lifecycle

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def update_mainline_lifecycle(mainline: Mainline) -> Mainline:
        """
    update_mainline_lifecycle函数
    
    **设计原理**：
    - **核心功能**：实现update_mainline_lifecycle的核心逻辑
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
    # 1. 计算评分趋势
    score_trend = mainline.score.get_trend()  # 近20日评分变化率
    
    # 2. 计算市场表现
    market_performance = mainline.get_market_performance()  # 近20日收益率
    
    # 3. 计算资金流向趋势
    capital_trend = mainline.get_capital_trend()  # 近20日资金流入趋势
    
    # 4. 判断生命周期阶段
    if score_trend > 0.1 and market_performance > 0.05 and capital_trend > 0:
        # 评分上升、市场表现良好、资金流入，进入成长期
        if mainline.stage == MainlineStage.EMERGING:
            mainline.stage = MainlineStage.GROWING
    elif score_trend < -0.1 or market_performance < -0.05 or capital_trend < -0.1:
        # 评分下降或市场表现不佳或资金流出，进入衰退期
        if mainline.stage in [MainlineStage.GROWING, MainlineStage.MATURE]:
            mainline.stage = MainlineStage.DECLINING
    elif mainline.stage == MainlineStage.GROWING and score_trend < 0.05:
        # 成长期但评分增长放缓，进入成熟期
        mainline.stage = MainlineStage.MATURE
    
    # 5. 更新生命周期时间戳
    mainline.lifecycle_updated_at = datetime.now()
    
    return mainline