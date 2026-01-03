"""
文件名: code_7_1___post_init__.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1___post_init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __post_init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

class TemplateType(Enum):
    """模板类型"""
    MULTI_FACTOR = "multi_factor"      # 多因子策略
    MOMENTUM_GROWTH = "momentum_growth"  # 动量成长策略
    VALUE = "value"                    # 价值投资策略
    MARKET_NEUTRAL = "market_neutral"  # 市场中性策略

class PlatformType(Enum):
    """平台类型"""
    PTRADE = "ptrade"  # PTrade平台
    QMT = "qmt"        # QMT平台

@dataclass
class StrategyTemplate:
    """策略模板定义"""
    
    # 基本信息
    name: str                          # 模板名称
    template_type: TemplateType         # 模板类型
    platform: PlatformType             # 平台类型
    version: str = "1.0.0"             # 模板版本
    
    # 模板内容
    header: str                        # 模板头部（元信息）
    parameters: Dict[str, Any]         # 参数定义
    initialize_code: str               # 初始化函数代码
    trading_code: str                  # 交易逻辑代码
    helper_functions: str              # 辅助函数代码
    risk_control_code: str             # 风控代码
    
    # 元数据
    description: str = ""               # 模板描述
    author: str = ""                    # 作者
    created_at: str = ""                # 创建时间
    updated_at: str = ""                # 更新时间
    tags: List[str] = None             # 标签列表
    
    # 依赖关系
    dependencies: List[str] = None     # 依赖的模板列表
    required_factors: List[str] = None # 必需的因子列表
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []
        if self.required_factors is None:
            self.required_factors = []