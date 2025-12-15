# -*- coding: utf-8 -*-
"""
策略导出器
=========
将策略代码导出为不同平台格式（PTrade/QMT/JoinQuant）
"""

import re
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path


class StrategyExporter:
    """策略导出器"""
    
    # PTrade API映射
    PTRADE_MAPPINGS = {
        # 数据获取
        "get_price": "get_history",
        "get_current_data": "get_snapshot",
        "get_security_info": "get_instrument",
        # 交易
        "order_target": "order_target",
        "order_target_value": "order_target_value",
        # 佣金设置
        r"set_commission\(PerTrade\(.*?\)\)": "set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))",
        r"set_slippage\(FixedSlippage\(.*?\)\)": "set_slippage(0.001)",
    }
    
    # QMT API映射
    QMT_MAPPINGS = {
        "get_price": "ContextInfo.get_market_data",
        "order_target": "order_target",
    }
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent.parent / "strategies"
    
    def export_to_ptrade(self, code: str, strategy_name: str = "strategy") -> str:
        """
        导出为PTrade格式
        
        PTrade主要差异:
        1. 数据获取API不同
        2. 佣金/滑点设置方式不同
        3. 不支持jqdata模块
        """
        # 移除jqdata导入
        code = re.sub(r"from jqdata import \*\n?", "", code)
        code = re.sub(r"import jqdata\n?", "", code)
        
        # 添加PTrade头部
        header = f'''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
平台: PTrade
导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

'''
        
        # API转换
        code = self._convert_api(code, self.PTRADE_MAPPINGS)
        
        # 修复佣金设置
        code = re.sub(
            r"set_slippage\(FixedSlippage\(([\d.]+)\)\)",
            r"set_slippage(\1)",
            code
        )
        
        return header + code
    
    def export_to_qmt(self, code: str, strategy_name: str = "strategy") -> str:
        """
        导出为QMT格式
        
        QMT主要差异:
        1. 使用ContextInfo获取数据
        2. 交易函数参数不同
        3. 不同的回调函数结构
        """
        header = f'''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
平台: QMT (迅投)
导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
注意: QMT策略需要在迅投客户端中运行
"""

import numpy as np
import pandas as pd

def init(ContextInfo):
    """初始化"""
    ContextInfo.set_universe(["000300.SH"])  # 设置股票池
    
'''
        
        # 转换initialize为init
        code = re.sub(r"def initialize\(context\):", "def init(ContextInfo):", code)
        code = re.sub(r"context\.", "ContextInfo.", code)
        
        # API转换
        code = self._convert_api(code, self.QMT_MAPPINGS)
        
        return header + code
    
    def export_to_joinquant(self, code: str, strategy_name: str = "strategy") -> str:
        """
        导出为JoinQuant格式（标准格式，基本不需转换）
        """
        header = f'''# -*- coding: utf-8 -*-
"""
策略名称: {strategy_name}
平台: JoinQuant (聚宽)
导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

'''
        return header + code
    
    def _convert_api(self, code: str, mappings: Dict[str, str]) -> str:
        """应用API映射"""
        for old, new in mappings.items():
            if old.startswith("r"):  # 正则表达式
                code = re.sub(old, new, code)
            else:
                code = code.replace(old, new)
        return code
    
    def save_strategy(self, code: str, filename: str, platform: str = "ptrade"):
        """保存策略到文件"""
        platform_dir = self.output_dir / platform
        platform_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = platform_dir / f"{filename}.py"
        filepath.write_text(code, encoding="utf-8")
        return str(filepath)


def export_strategy(code: str, platform: str = "ptrade", name: str = "strategy") -> str:
    """
    快捷导出函数
    
    Args:
        code: 策略代码
        platform: 目标平台 ptrade/qmt/joinquant
        name: 策略名称
        
    Returns:
        转换后的代码
    """
    exporter = StrategyExporter()
    
    if platform.lower() == "ptrade":
        return exporter.export_to_ptrade(code, name)
    elif platform.lower() == "qmt":
        return exporter.export_to_qmt(code, name)
    elif platform.lower() in ["joinquant", "jq"]:
        return exporter.export_to_joinquant(code, name)
    else:
        raise ValueError(f"不支持的平台: {platform}")
