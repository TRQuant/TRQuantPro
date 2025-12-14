"""
文件名: code_7_3_split_time_series.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.3/code_7_3_split_time_series.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: split_time_series

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class WalkForwardAnalyzer:
    """Walk-Forward分析器"""
    
    def split_time_series(
        self,
        start_date: str,
        end_date: str,
        train_period: int = 252,  # 训练期（交易日）
        test_period: int = 63,     # 测试期（交易日）
        step: int = 21             # 步长（交易日）
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
        from datetime import datetime, timedelta
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        splits = []
        current = start
        
        while current + timedelta(days=train_period + test_period) <= end:
            train_start = current
            train_end = current + timedelta(days=train_period)
            test_start = train_end
            test_end = test_start + timedelta(days=test_period)
            
            splits.append((
                train_start.strftime('%Y-%m-%d'),
                train_end.strftime('%Y-%m-%d'),
                test_start.strftime('%Y-%m-%d'),
                test_end.strftime('%Y-%m-%d')
            ))
            
            current += timedelta(days=step)
        
        return splits