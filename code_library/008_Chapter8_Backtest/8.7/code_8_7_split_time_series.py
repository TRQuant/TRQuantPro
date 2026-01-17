"""
文件名: code_8_7_split_time_series.py
保存路径: code_library/008_Chapter8_Backtest/8.7/code_8_7_split_time_series.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.7_Walk_Forward_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: split_time_series

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

from typing import List, Tuple
from datetime import datetime, timedelta

class TimeSeriesSplitter:
    """时间序列分割器"""
    
    def split_time_series(
        self,
        start_date: str,
        end_date: str,
        train_period: int = 252,  # 训练集长度（交易日）
        test_period: int = 63,     # 测试集长度（交易日）
        step_size: int = 63        # 步长（交易日）
    ) -> List[Tuple[str, str, str, str]]:
            """
    split_time_series函数
    
    **设计原理**：
    - **核心功能**：实现split_time_series的核心逻辑
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
        splits = []
        
        current_date = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        while current_date < end:
            # 训练集
            train_start = current_date
            train_end = self._add_trading_days(train_start, train_period)
            
            # 测试集
            test_start = train_end
            test_end = self._add_trading_days(test_start, test_period)
            
            if test_end > end:
                break
            
            splits.append((
                train_start.strftime('%Y-%m-%d'),
                train_end.strftime('%Y-%m-%d'),
                test_start.strftime('%Y-%m-%d'),
                test_end.strftime('%Y-%m-%d')
            ))
            
            # 移动到下一个窗口
            current_date = self._add_trading_days(current_date, step_size)
        
        return splits
    
    def _add_trading_days(self, date: pd.Timestamp, days: int) -> pd.Timestamp:
        """添加交易日（简化版，实际需要考虑节假日）"""
        return date + pd.Timedelta(days=days)