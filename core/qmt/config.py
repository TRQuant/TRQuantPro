# -*- coding: utf-8 -*-
"""
QMT回测配置
===========

QMT(xtquant)回测引擎的配置类
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class QMTDataPeriod(Enum):
    """数据周期"""
    MIN_1 = "1m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    MIN_60 = "60m"
    DAY = "1d"
    WEEK = "1w"


class QMTBroker(Enum):
    """支持的券商"""
    GUOJIN = "国金证券"
    GUOSHENG = "国盛证券"
    GUOXIN = "国信证券"
    HAITONG = "海通证券"
    HUAXIN = "华鑫证券"
    OTHER = "其他"


@dataclass
class QMTConfig:
    """QMT回测配置"""
    
    # 回测时间范围
    start_date: str  # YYYY-MM-DD 或 YYYYMMDD
    end_date: str
    
    # 资金和费用
    initial_capital: float = 1000000.0
    commission_rate: float = 0.0003  # 佣金率
    stamp_tax_rate: float = 0.001    # 印花税(卖出)
    slippage: float = 0.001          # 滑点
    min_commission: float = 5.0      # 最低佣金
    
    # 基准和数据
    benchmark: str = "000300.SH"     # 基准指数
    data_period: QMTDataPeriod = QMTDataPeriod.DAY
    stock_pool: List[str] = field(default_factory=list)  # 股票池
    
    # QMT连接配置
    qmt_path: str = ""               # miniQMT路径
    broker: QMTBroker = QMTBroker.GUOJIN
    account_id: str = ""             # 账户ID (实盘用)
    
    # 输出配置
    output_dir: str = "./qmt_backtest_results"
    log_level: str = "INFO"
    save_trades: bool = True
    save_positions: bool = True
    
    # 额外参数
    extras: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        # 标准化日期格式
        self.start_date = self._normalize_date(self.start_date)
        self.end_date = self._normalize_date(self.end_date)
        
        # 设置默认QMT路径
        if not self.qmt_path:
            import platform
            if platform.system() == "Windows":
                self.qmt_path = "C:/国金QMT/userdata_mini"
            else:
                self.qmt_path = ""  # Linux下无法直接使用miniQMT
    
    def _normalize_date(self, date_str: str) -> str:
        """标准化日期格式为YYYYMMDD"""
        if "-" in date_str:
            return date_str.replace("-", "")
        return date_str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "initial_capital": self.initial_capital,
            "commission_rate": self.commission_rate,
            "stamp_tax_rate": self.stamp_tax_rate,
            "slippage": self.slippage,
            "benchmark": self.benchmark,
            "data_period": self.data_period.value,
            "qmt_path": self.qmt_path,
            "broker": self.broker.value,
            "output_dir": self.output_dir,
        }


@dataclass
class QMTOptimizeConfig:
    """QMT参数优化配置"""
    
    param_grid: Dict[str, List[Any]]  # 参数网格
    target_metric: str = "sharpe_ratio"  # 目标指标
    method: str = "grid"  # grid/random/bayesian
    max_iterations: int = 100
    n_jobs: int = 1       # 并行数
    early_stopping: bool = True
    cv_splits: int = 0    # 交叉验证折数(0=不使用)
    
    def get_param_combinations(self) -> List[Dict]:
        """获取参数组合"""
        import itertools
        
        keys = list(self.param_grid.keys())
        values = list(self.param_grid.values())
        
        combinations = []
        for combo in itertools.product(*values):
            combinations.append(dict(zip(keys, combo)))
        
        if self.method == "random" and len(combinations) > self.max_iterations:
            import random
            combinations = random.sample(combinations, self.max_iterations)
        
        return combinations[:self.max_iterations]
