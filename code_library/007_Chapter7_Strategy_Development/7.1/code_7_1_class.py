"""
文件名: code_7_1_class.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_class.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: class

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

@dataclass
class TemplateParameter:
    """模板参数定义"""
    
    name: str                          # 参数名称
    type: type                         # 参数类型
    default: Any                       # 默认值
    description: str = ""               # 参数描述
    min_value: Optional[float] = None  # 最小值
    max_value: Optional[float] = None  # 最大值
    required: bool = False             # 是否必需
    choices: List[Any] = None          # 可选值列表

# 标准参数定义
STANDARD_PARAMETERS = {
    # 基础参数
    'stock_num': TemplateParameter(
        name='stock_num',
        type=int,
        default=10,
        description='持仓股票数量',
        min_value=1,
        max_value=50
    ),
    'rebalance_days': TemplateParameter(
        name='rebalance_days',
        type=int,
        default=20,
        description='调仓周期（交易日）',
        min_value=1,
        max_value=60
    ),
    
    # 风控参数
    'max_position': TemplateParameter(
        name='max_position',
        type=float,
        default=0.1,
        description='单票最大仓位（0-1）',
        min_value=0.01,
        max_value=1.0
    ),
    'stop_loss': TemplateParameter(
        name='stop_loss',
        type=float,
        default=0.08,
        description='止损线（0-1）',
        min_value=0.01,
        max_value=0.5
    ),
    'take_profit': TemplateParameter(
        name='take_profit',
        type=float,
        default=0.2,
        description='止盈线（0-1）',
        min_value=0.05,
        max_value=1.0
    ),
    
    # 因子配置
    'factors': TemplateParameter(
        name='factors',
        type=list,
        default=[],
        description='使用的因子列表',
        required=True
    ),
    'factor_weights': TemplateParameter(
        name='factor_weights',
        type=dict,
        default={},
        description='因子权重配置',
        required=False
    )
}