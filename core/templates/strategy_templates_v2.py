# -*- coding: utf-8 -*-
"""
策略模板库（增强版 v2.0）
========================
支持多平台：JoinQuant / BulletTrade / PTrade / QMT

策略类型：
1. 动量策略 - 追涨杀跌
2. 价值策略 - 低估买入
3. 趋势策略 - 均线系统
4. 均值回归策略 - 超跌反弹
5. 多因子策略 - 综合评分
6. 主题轮动策略 - 板块轮动
7. 风险平价策略 - 波动率加权

新增功能：
- 多平台代码生成
- 参数范围验证
- 风控模块内置
- 策略说明文档
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import json


class Platform(Enum):
    """目标平台"""
    JOINQUANT = "joinquant"  # 聚宽
    BULLETTRADE = "bullettrade"  # BulletTrade
    PTRADE = "ptrade"  # 恒生PTrade
    QMT = "qmt"  # 迅投QMT


class StrategyCategory(Enum):
    """策略分类"""
    MOMENTUM = "momentum"
    VALUE = "value"
    TREND = "trend"
    MEAN_REVERSION = "mean_reversion"
    MULTI_FACTOR = "multi_factor"
    ROTATION = "rotation"
    RISK_PARITY = "risk_parity"


@dataclass
class ParamSpec:
    """参数规格"""
    name: str
    type: type
    default: Any
    min_val: Any = None
    max_val: Any = None
    description: str = ""
    
    def validate(self, value: Any) -> Tuple[bool, str]:
        """验证参数值"""
        if not isinstance(value, self.type):
            return False, f"类型错误: 期望{self.type.__name__}，得到{type(value).__name__}"
        if self.min_val is not None and value < self.min_val:
            return False, f"值太小: 最小{self.min_val}"
        if self.max_val is not None and value > self.max_val:
            return False, f"值太大: 最大{self.max_val}"
        return True, "OK"


@dataclass
class StrategyTemplateV2(ABC):
    """策略模板基类 V2"""
    name: str
    description: str
    category: StrategyCategory
    risk_level: str = "medium"  # low/medium/high
    suitable_market: str = "all"  # bull/bear/neutral/all
    
    @abstractmethod
    def get_param_specs(self) -> List[ParamSpec]:
        """获取参数规格"""
        pass
    
    def get_default_params(self) -> Dict[str, Any]:
        """获取默认参数"""
        return {spec.name: spec.default for spec in self.get_param_specs()}
    
    def validate_params(self, params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证所有参数"""
        errors = []
        specs = {s.name: s for s in self.get_param_specs()}
        
        for name, value in params.items():
            if name in specs:
                valid, msg = specs[name].validate(value)
                if not valid:
                    errors.append(f"{name}: {msg}")
        
        return len(errors) == 0, errors
    
    @abstractmethod
    def generate_joinquant(self, params: Dict[str, Any]) -> str:
        """生成聚宽代码"""
        pass
    
    def generate_bullettrade(self, params: Dict[str, Any]) -> str:
        """生成BulletTrade代码"""
        # 默认从聚宽代码转换
        jq_code = self.generate_joinquant(params)
        return self._convert_jq_to_bt(jq_code)
    
    def generate_ptrade(self, params: Dict[str, Any]) -> str:
        """生成PTrade代码"""
        jq_code = self.generate_joinquant(params)
        return self._convert_jq_to_ptrade(jq_code)
    
    def generate_code(self, params: Dict[str, Any] = None, platform: Platform = Platform.JOINQUANT) -> str:
        """生成指定平台代码"""
        p = {**self.get_default_params(), **(params or {})}
        
        # 验证参数
        valid, errors = self.validate_params(p)
        if not valid:
            raise ValueError(f"参数验证失败: {errors}")
        
        if platform == Platform.JOINQUANT:
            return self.generate_joinquant(p)
        elif platform == Platform.BULLETTRADE:
            return self.generate_bullettrade(p)
        elif platform == Platform.PTRADE:
            return self.generate_ptrade(p)
        elif platform == Platform.QMT:
            return self._convert_jq_to_qmt(self.generate_joinquant(p))
        else:
            raise ValueError(f"不支持的平台: {platform}")
    
    def get_doc(self) -> str:
        """获取策略文档"""
        specs = self.get_param_specs()
        param_doc = "\n".join([
            f"  - {s.name}: {s.description} (默认: {s.default}, 范围: {s.min_val}-{s.max_val})"
            for s in specs
        ])
        
        return f"""
策略名称: {self.name}
分类: {self.category.value}
风险等级: {self.risk_level}
适用市场: {self.suitable_market}

描述:
{self.description}

参数:
{param_doc}
"""
    
    # ==================== 平台转换 ====================
    
    def _convert_jq_to_bt(self, code: str) -> str:
        """聚宽 -> BulletTrade"""
        import re
        
        # 移除 jqdata 导入
        code = re.sub(r"from jqdata import \*\n?", "", code)
        
        # 添加 BulletTrade 头部
        header = f'''# -*- coding: utf-8 -*-
"""
策略: {self.name}
平台: BulletTrade
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

'''
        
        # API 转换
        # set_slippage(FixedSlippage(x)) -> set_slippage(x)
        code = re.sub(r"set_slippage\(FixedSlippage\(([\d.]+)\)\)", r"set_slippage(\1)", code)
        
        # set_order_cost 简化
        code = re.sub(r"set_order_cost\([^)]+\),?\s*type='stock'\)", "", code)
        
        # 保持 order_target_value 不变
        
        return header + code
    
    def _convert_jq_to_ptrade(self, code: str) -> str:
        """聚宽 -> PTrade"""
        import re
        
        # 移除 jqdata 导入
        code = re.sub(r"from jqdata import \*\n?", "", code)
        
        # 添加 PTrade 头部
        header = f'''# -*- coding: utf-8 -*-
"""
策略: {self.name}
平台: PTrade (恒生)
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

'''
        
        # API 转换
        # get_price -> get_history
        code = code.replace("get_price(", "get_history(")
        
        # get_index_stocks -> 使用固定股票池或自定义
        code = re.sub(
            r"get_index_stocks\(['\"](\w+)['\"](?:,\s*date=[^)]+)?\)",
            r"g.stock_pool",
            code
        )
        
        # 添加股票池初始化
        if "g.stock_pool" in code:
            init_stocks = """
    # PTrade: 手动设置股票池（替换 get_index_stocks）
    g.stock_pool = [
        '000001.XSHE', '000002.XSHE', '000063.XSHE', '000100.XSHE',
        '000333.XSHE', '000651.XSHE', '000725.XSHE', '000858.XSHE',
        '002027.XSHE', '002142.XSHE', '002475.XSHE', '002594.XSHE',
        '300059.XSHE', '300122.XSHE', '600000.XSHG', '600009.XSHG',
        '600016.XSHG', '600028.XSHG', '600030.XSHG', '600036.XSHG',
    ]
"""
            code = re.sub(
                r"(def initialize\(context\):)",
                r"\1" + init_stocks,
                code
            )
        
        # set_slippage
        code = re.sub(r"set_slippage\(FixedSlippage\(([\d.]+)\)\)", r"set_slippage(\1)", code)
        
        # set_order_cost 转换
        code = re.sub(
            r"set_order_cost\([^)]+\),?\s*type='stock'\)",
            "set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))",
            code
        )
        
        return header + code
    
    def _convert_jq_to_qmt(self, code: str) -> str:
        """聚宽 -> QMT"""
        import re
        
        # 添加 QMT 头部
        header = f'''# -*- coding: utf-8 -*-
"""
策略: {self.name}
平台: QMT (迅投)
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
注意: 需要在 QMT 客户端中运行
"""

import numpy as np
import pandas as pd

'''
        
        # 移除 jqdata 导入
        code = re.sub(r"from jqdata import \*\n?", "", code)
        
        # 转换 initialize -> init
        code = re.sub(r"def initialize\(context\):", "def init(ContextInfo):", code)
        
        # context -> ContextInfo
        code = code.replace("context.", "ContextInfo.")
        
        return header + code


# ==================== 具体策略模板 ====================

@dataclass
class MomentumTemplateV2(StrategyTemplateV2):
    """动量策略模板 V2"""
    name: str = "动量策略"
    description: str = "基于价格动量选股，追涨杀跌。适合趋势明显的牛市行情。"
    category: StrategyCategory = StrategyCategory.MOMENTUM
    risk_level: str = "high"
    suitable_market: str = "bull"
    
    def get_param_specs(self) -> List[ParamSpec]:
        return [
            ParamSpec("short_period", int, 5, 3, 20, "短期动量周期"),
            ParamSpec("long_period", int, 20, 10, 60, "长期动量周期"),
            ParamSpec("max_stocks", int, 10, 5, 30, "最大持股数"),
            ParamSpec("rebalance_days", int, 5, 1, 20, "调仓周期"),
            ParamSpec("stop_loss", float, 0.08, 0.03, 0.15, "止损比例"),
            ParamSpec("take_profit", float, 0.20, 0.10, 0.50, "止盈比例"),
        ]
    
    def generate_joinquant(self, params: Dict[str, Any]) -> str:
        return f'''# -*- coding: utf-8 -*-
"""动量策略 V2 - 自动生成"""
from jqdata import *

# 参数
SHORT_PERIOD = {params["short_period"]}
LONG_PERIOD = {params["long_period"]}
MAX_STOCKS = {params["max_stocks"]}
REBALANCE_DAYS = {params["rebalance_days"]}
STOP_LOSS = {params["stop_loss"]}
TAKE_PROFIT = {params["take_profit"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, 
                            open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.trade_count = 0
    g.cost_price = {{}}  # 成本价记录
    run_daily(check_stop, time='14:50')  # 止盈止损检查
    run_daily(rebalance, time='09:35')

def check_stop(context):
    """止盈止损检查"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        cost = g.cost_price.get(stock, pos.avg_cost)
        current = pos.price
        
        # 止损
        if current < cost * (1 - STOP_LOSS):
            order_target_value(stock, 0)
            log.info(f"止损卖出: {{stock}}")
        # 止盈
        elif current > cost * (1 + TAKE_PROFIT):
            order_target_value(stock, 0)
            log.info(f"止盈卖出: {{stock}}")

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    stocks = get_index_stocks('000300.XSHG')
    df = get_price(stocks, end_date=context.current_dt, frequency='daily', 
                   fields=['close'], count=LONG_PERIOD+5, panel=False)
    pivot = df.pivot(index='time', columns='code', values='close')
    
    # 计算动量
    mom_short = pivot.pct_change(SHORT_PERIOD).iloc[-1]
    mom_long = pivot.pct_change(LONG_PERIOD).iloc[-1]
    score = (mom_short * 0.5 + mom_long * 0.5)
    score = score[(mom_short > 0) & (mom_long > 0)].dropna()
    
    targets = score.nlargest(MAX_STOCKS).index.tolist()
    
    # 卖出不在目标的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    # 买入目标
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
        g.cost_price[stock] = get_current_data()[stock].last_price
'''


@dataclass
class MeanReversionTemplateV2(StrategyTemplateV2):
    """均值回归策略模板"""
    name: str = "均值回归策略"
    description: str = "买入超跌股票，等待回归均值。适合震荡市场。"
    category: StrategyCategory = StrategyCategory.MEAN_REVERSION
    risk_level: str = "medium"
    suitable_market: str = "neutral"
    
    def get_param_specs(self) -> List[ParamSpec]:
        return [
            ParamSpec("lookback", int, 20, 10, 60, "回看周期"),
            ParamSpec("std_threshold", float, 2.0, 1.5, 3.0, "标准差阈值"),
            ParamSpec("max_stocks", int, 10, 5, 20, "最大持股数"),
            ParamSpec("hold_days", int, 5, 3, 20, "持仓天数"),
        ]
    
    def generate_joinquant(self, params: Dict[str, Any]) -> str:
        return f'''# -*- coding: utf-8 -*-
"""均值回归策略 - 自动生成"""
from jqdata import *
import pandas as pd

LOOKBACK = {params["lookback"]}
STD_THRESHOLD = {params["std_threshold"]}
MAX_STOCKS = {params["max_stocks"]}
HOLD_DAYS = {params["hold_days"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    g.hold_info = {{}}  # 记录持仓天数
    run_daily(rebalance, time='09:35')

def rebalance(context):
    stocks = get_index_stocks('000300.XSHG')
    df = get_price(stocks, end_date=context.current_dt, 
                   fields=['close'], count=LOOKBACK+5, panel=False)
    pivot = df.pivot(index='time', columns='code', values='close')
    
    # 计算 Z-score
    mean = pivot.rolling(LOOKBACK).mean()
    std = pivot.rolling(LOOKBACK).std()
    zscore = (pivot - mean) / std
    current_z = zscore.iloc[-1].dropna()
    
    # 找超跌股票
    oversold = current_z[current_z < -STD_THRESHOLD]
    targets = oversold.nsmallest(MAX_STOCKS).index.tolist()
    
    # 更新持仓天数
    for stock in list(g.hold_info.keys()):
        g.hold_info[stock] += 1
    
    # 卖出持仓超过 HOLD_DAYS 的
    for stock in list(context.portfolio.positions.keys()):
        if g.hold_info.get(stock, 0) >= HOLD_DAYS:
            order_target_value(stock, 0)
            g.hold_info.pop(stock, None)
    
    # 买入新目标
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        if stock not in context.portfolio.positions:
            order_target_value(stock, cash)
            g.hold_info[stock] = 0
'''


@dataclass
class RotationTemplateV2(StrategyTemplateV2):
    """主题轮动策略模板"""
    name: str = "主题轮动策略"
    description: str = "基于行业/主题强度轮动，跟踪热点板块。"
    category: StrategyCategory = StrategyCategory.ROTATION
    risk_level: str = "high"
    suitable_market: str = "bull"
    
    def get_param_specs(self) -> List[ParamSpec]:
        return [
            ParamSpec("lookback", int, 10, 5, 30, "动量回看周期"),
            ParamSpec("top_sectors", int, 3, 1, 5, "选择板块数"),
            ParamSpec("stocks_per_sector", int, 3, 2, 10, "每板块选股数"),
            ParamSpec("rebalance_days", int, 5, 3, 20, "调仓周期"),
        ]
    
    def generate_joinquant(self, params: Dict[str, Any]) -> str:
        return f'''# -*- coding: utf-8 -*-
"""主题轮动策略 - 自动生成"""
from jqdata import *
import pandas as pd

LOOKBACK = {params["lookback"]}
TOP_SECTORS = {params["top_sectors"]}
STOCKS_PER_SECTOR = {params["stocks_per_sector"]}
REBALANCE_DAYS = {params["rebalance_days"]}

# 主题/行业列表
SECTORS = [
    ("人工智能", ["300124.XSHE", "002230.XSHE", "300033.XSHE"]),
    ("新能源", ["300750.XSHE", "002594.XSHE", "600438.XSHG"]),
    ("半导体", ["688981.XSHG", "002371.XSHE", "603501.XSHG"]),
    ("医药", ["300760.XSHE", "000661.XSHE", "603259.XSHG"]),
    ("消费", ["600519.XSHG", "000858.XSHE", "002304.XSHE"]),
]

def initialize(context):
    set_benchmark('000300.XSHG')
    g.trade_count = 0
    run_daily(rebalance, time='09:35')

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    # 计算各板块动量
    sector_momentum = []
    for name, stocks in SECTORS:
        df = get_price(stocks, end_date=context.current_dt, 
                      fields=['close'], count=LOOKBACK+1, panel=False)
        if df.empty:
            continue
        pivot = df.pivot(index='time', columns='code', values='close')
        mom = pivot.pct_change(LOOKBACK).iloc[-1].mean()
        sector_momentum.append((name, stocks, mom))
    
    # 选择动量最强的板块
    sector_momentum.sort(key=lambda x: x[2], reverse=True)
    top_sectors = sector_momentum[:TOP_SECTORS]
    
    # 构建目标持仓
    targets = []
    for name, stocks, mom in top_sectors:
        targets.extend(stocks[:STOCKS_PER_SECTOR])
    
    # 卖出不在目标的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    # 买入目标
    cash = context.portfolio.total_value / len(targets) if targets else 0
    for stock in targets:
        order_target_value(stock, cash)
'''


# ==================== 策略工厂 ====================

class StrategyFactory:
    """策略工厂"""
    
    _templates = {
        "momentum": MomentumTemplateV2,
        "mean_reversion": MeanReversionTemplateV2,
        "rotation": RotationTemplateV2,
    }
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """列出所有可用模板"""
        return list(cls._templates.keys())
    
    @classmethod
    def get_template(cls, name: str) -> StrategyTemplateV2:
        """获取策略模板"""
        if name not in cls._templates:
            raise ValueError(f"未知策略模板: {name}，可用: {cls.list_templates()}")
        return cls._templates[name]()
    
    @classmethod
    def create_strategy(
        cls, 
        name: str, 
        params: Dict[str, Any] = None, 
        platform: Platform = Platform.JOINQUANT
    ) -> str:
        """创建策略代码"""
        template = cls.get_template(name)
        return template.generate_code(params, platform)
    
    @classmethod
    def register_template(cls, name: str, template_class: type):
        """注册新模板"""
        cls._templates[name] = template_class


# ==================== 便捷函数 ====================

def create_strategy(
    strategy_type: str,
    params: Dict[str, Any] = None,
    platform: str = "joinquant"
) -> str:
    """
    创建策略代码
    
    Args:
        strategy_type: 策略类型 (momentum/mean_reversion/rotation)
        params: 策略参数
        platform: 目标平台 (joinquant/bullettrade/ptrade/qmt)
        
    Returns:
        策略代码
    """
    platform_enum = Platform(platform.lower())
    return StrategyFactory.create_strategy(strategy_type, params, platform_enum)


def list_strategies() -> List[Dict]:
    """列出所有策略"""
    result = []
    for name in StrategyFactory.list_templates():
        template = StrategyFactory.get_template(name)
        result.append({
            "name": name,
            "display_name": template.name,
            "description": template.description,
            "category": template.category.value,
            "risk_level": template.risk_level,
            "suitable_market": template.suitable_market,
            "params": [
                {
                    "name": s.name,
                    "type": s.type.__name__,
                    "default": s.default,
                    "min": s.min_val,
                    "max": s.max_val,
                    "description": s.description
                }
                for s in template.get_param_specs()
            ]
        })
    return result
