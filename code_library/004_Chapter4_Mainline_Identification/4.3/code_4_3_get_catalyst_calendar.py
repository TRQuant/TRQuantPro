"""
文件名: code_4_3_get_catalyst_calendar.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.3/code_4_3_get_catalyst_calendar.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: get_catalyst_calendar

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def get_catalyst_calendar(self, days: int = 90) -> List[Catalyst]:
        """
    get_catalyst_calendar函数
    
    **设计原理**：
    - **核心功能**：实现get_catalyst_calendar的核心逻辑
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
    # 1. 获取政策日历
    policy_calendar = self._get_policy_calendar(days)
    
    # 2. 获取业绩发布日历
    earnings_calendar = self._get_earnings_calendar(days)
    
    # 3. 获取事件驱动日历
    event_calendar = self._get_event_calendar(days)
    
    # 4. 合并并排序
    catalysts = self._merge_and_sort_catalysts(
        policy_calendar, earnings_calendar, event_calendar
    )
    
    return catalysts