"""
文件名: code_8_1_validate.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_validate.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: validate

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

@dataclass
class BacktestConfig:
    """回测配置"""
    
    start_date: str                    # 开始日期
    end_date: str                      # 结束日期
    initial_capital: float = 1000000.0  # 初始资金
    commission_rate: float = 0.0003    # 佣金率
    stamp_tax_rate: float = 0.001      # 印花税
    slippage: float = 0.001            # 滑点
    benchmark: str = "000300.XSHG"     # 基准
    position_limit: int = 20           # 最大持仓数
    rebalance_freq: str = "monthly"    # 调仓频率
    
    def validate(self) -> Tuple[bool, List[str]]:
            """
    validate函数
    
    **设计原理**：
    - **核心功能**：实现validate的核心逻辑
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
        errors = []
        
        # 验证日期
        try:
            start = pd.to_datetime(self.start_date)
            end = pd.to_datetime(self.end_date)
            if start >= end:
                errors.append("开始日期必须早于结束日期")
        except Exception as e:
            errors.append(f"日期格式错误: {e}")
        
        # 验证资金
        if self.initial_capital <= 0:
            errors.append("初始资金必须大于0")
        
        # 验证费率
        if self.commission_rate < 0 or self.commission_rate > 0.01:
            errors.append("佣金率必须在0-1%之间")
        
        return len(errors) == 0, errors