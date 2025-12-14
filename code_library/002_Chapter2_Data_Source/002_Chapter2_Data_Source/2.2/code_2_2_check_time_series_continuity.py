"""
文件名: code_2_2_check_time_series_continuity.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_check_time_series_continuity.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:30:09
函数/类名: check_time_series_continuity

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def check_time_series_continuity(self, data: pd.DataFrame, 
                                 trading_calendar: List[str] = None) -> Dict[str, Any]:
        """
    check_time_series_continuity函数
    
    **设计原理**：
    - **核心功能**：实现check_time_series_continuity的核心逻辑
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
    result = {
        "is_continuous": True,
        "missing_dates": [],
        "duplicate_dates": [],
        "continuity_score": 1.0
    }
    
    # 获取日期
    if data.index.name == 'date':
        dates = pd.to_datetime(data.index)
    elif 'date' in data.columns:
        dates = pd.to_datetime(data['date'])
    else:
        return result
    
    # 检查重复日期
    duplicate_dates = dates[dates.duplicated()].tolist()
    result["duplicate_dates"] = [str(d) for d in duplicate_dates]
    
    # 检查缺失日期
    if trading_calendar:
        # 使用交易日历检查
        expected_dates = pd.to_datetime(trading_calendar)
        missing_dates = set(expected_dates) - set(dates)
        result["missing_dates"] = [str(d) for d in sorted(missing_dates)]
    else:
        # 简单检查：检查是否有大的时间间隔
        date_diff = dates.diff()
        large_gaps = date_diff[date_diff > pd.Timedelta(days=3)]
        if len(large_gaps) > 0:
            result["is_continuous"] = False
            result["missing_dates"] = [str(dates.iloc[i]) for i in large_gaps.index]
    
    # 计算连续性得分
    if len(dates) > 0:
        if trading_calendar:
            expected_count = len(trading_calendar)
            actual_count = len(dates)
            result["continuity_score"] = actual_count / expected_count
        else:
            result["continuity_score"] = 1.0 if result["is_continuous"] else 0.8
    
    return result