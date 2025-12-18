"""
文件名: code_4_2___init__.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

import schedule
import time
from datetime import datetime

class MainlineFilterMonitor:
    """主线筛选监控器"""
    
    def __init__(self):
        self.filter = MainlineFilter()
        self.current_filtered = []
        self.last_update_time = None
    
    def auto_filter(self):
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
        # 获取所有主线
        mainlines = get_all_mainlines()
        
        # 设置筛选条件（可根据市场环境动态调整）
        criteria = self._get_auto_criteria()
        
        # 执行筛选
        filtered = self.filter.filter(mainlines, criteria)
        
        # 排序
        sorted_mainlines = self.filter.sort(
            filtered,
            sort_by="score",
            order="desc"
        )
        
        # 更新结果
        self.current_filtered = sorted_mainlines
        self.last_update_time = datetime.now()
        
        logger.info(f"自动筛选完成，筛选出{len(sorted_mainlines)}条主线")
        
        return sorted_mainlines
    
    def _get_auto_criteria(self) -> FilterCriteria:
        """获取自动筛选条件（可根据市场环境动态调整）"""
        # 获取市场状态
        market_status = get_market_status()
        
        if market_status['regime'] == 'risk_on':
            # 牛市：提高评分阈值，关注技术形态
            return FilterCriteria(
                min_score=75.0,
                top_n=10,
                require_trend_up=True
            )
        elif market_status['regime'] == 'risk_off':
            # 熊市：降低评分阈值，关注估值
            return FilterCriteria(
                min_score=60.0,
                top_n=5
            )
        else:
            # 震荡市：中等阈值
            return FilterCriteria(
                min_score=70.0,
                top_n=8
            )
    
    def start_auto_filter(self, interval_minutes: int = 60):
        """
        启动自动筛选
        
        Args:
            interval_minutes: 筛选间隔（分钟）
        """
        schedule.every(interval_minutes).minutes.do(self.auto_filter)
        
        # 立即执行一次
        self.auto_filter()
        
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(60)