"""
文件名: code_6_4___init__.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pathlib import Path
import logging

from .factor_manager import FactorManager
from .factor_storage import FactorStorage
from .factor_neutralizer import FactorNeutralizer
from .factor_evaluator import FactorEvaluator

class FactorPipeline:
    """
    因子计算流水线
    
    自动化完成：
    1. 数据获取与检查
    2. 因子计算
    3. 中性化处理（可选）
    4. 存储到数据库
    5. 绩效监控更新
    """
    
    def __init__(
        self,
        jq_client=None,
        factor_manager: Optional[FactorManager] = None,
        factor_storage: Optional[FactorStorage] = None,
        stock_pool: str = "all_a",  # 'all_a', 'hs300', 'zz500', 'zz1000'
        neutralize: bool = True,
        log_dir: Optional[Path] = None,
    ):
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
        self.jq_client = jq_client
        
        self.factor_manager = factor_manager or FactorManager(jq_client=jq_client)
        self.factor_storage = factor_storage or FactorStorage()
        self.neutralizer = FactorNeutralizer(jq_client=jq_client)
        self.evaluator = FactorEvaluator(jq_client=jq_client)
        
        self.stock_pool = stock_pool
        self.neutralize = neutralize
        
        self.log_dir = log_dir or Path.home() / ".local/share/trquant/logs/factors"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 运行统计
        self.run_stats = {
            "start_time": None,
            "end_time": None,
            "total_stocks": 0,
            "success_factors": 0,
            "failed_factors": 0,
            "skipped_stocks": 0,
            "errors": [],
        }