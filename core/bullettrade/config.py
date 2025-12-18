# -*- coding: utf-8 -*-
"""
BulletTrade 配置类

提供回测配置的封装
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime, date


@dataclass
class BTConfig:
    """BulletTrade回测配置"""
    
    # 基本配置
    start_date: str = ""  # 回测开始日期 'YYYY-MM-DD'
    end_date: str = ""    # 回测结束日期 'YYYY-MM-DD'
    initial_capital: float = 1000000.0  # 初始资金
    
    # 交易成本
    commission_rate: float = 0.0003  # 佣金率
    stamp_tax_rate: float = 0.001    # 印花税率
    slippage: float = 0.001          # 滑点
    min_commission: float = 5.0      # 最低佣金
    
    # 数据配置
    data_provider: str = "jqdata"    # 数据源: jqdata, akshare, mock
    benchmark: Optional[str] = "000300.XSHG"  # 基准指数
    frequency: str = "day"           # 回测频率: day, minute
    
    # 输出配置
    output_dir: str = "./backtest_results"  # 输出目录
    log_file: Optional[str] = None   # 日志文件路径
    generate_html: bool = True       # 是否生成HTML报告
    generate_csv: bool = True        # 是否生成CSV文件
    generate_images: bool = False    # 是否生成图片
    
    # 高级配置
    initial_positions: Optional[List[Dict[str, Any]]] = None  # 初始持仓
    extras: Optional[Dict[str, Any]] = None  # 额外参数
    algorithm_id: Optional[str] = None  # 算法ID
    
    def __post_init__(self):
        """验证配置"""
        if self.start_date and self.end_date:
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            if start >= end:
                raise ValueError(f"start_date({self.start_date}) 必须早于 end_date({self.end_date})")
        
        if self.initial_capital <= 0:
            raise ValueError(f"initial_capital 必须大于 0, 当前值: {self.initial_capital}")
        
        if self.frequency not in ("day", "minute"):
            raise ValueError(f"frequency 必须是 'day' 或 'minute', 当前值: {self.frequency}")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "initial_capital": self.initial_capital,
            "commission_rate": self.commission_rate,
            "stamp_tax_rate": self.stamp_tax_rate,
            "slippage": self.slippage,
            "min_commission": self.min_commission,
            "data_provider": self.data_provider,
            "benchmark": self.benchmark,
            "frequency": self.frequency,
            "output_dir": self.output_dir,
            "log_file": self.log_file,
            "generate_html": self.generate_html,
            "generate_csv": self.generate_csv,
            "generate_images": self.generate_images,
            "initial_positions": self.initial_positions,
            "extras": self.extras,
            "algorithm_id": self.algorithm_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BTConfig":
        """从字典创建配置"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class BTOptimizeConfig:
    """BulletTrade参数优化配置"""
    
    # 优化目标
    target_metric: str = "sharpe_ratio"  # 优化目标: sharpe_ratio, total_return, max_drawdown
    optimize_direction: str = "maximize"  # maximize 或 minimize
    
    # 参数空间
    param_grid: Dict[str, List[Any]] = field(default_factory=dict)
    
    # 优化方法
    method: str = "grid"  # grid, random, bayesian
    n_trials: int = 100   # 随机/贝叶斯优化的试验次数
    
    # 并行设置
    n_jobs: int = 1       # 并行任务数
    
    def __post_init__(self):
        """验证配置"""
        if self.target_metric not in ("sharpe_ratio", "total_return", "max_drawdown", "annual_return"):
            raise ValueError(f"不支持的优化目标: {self.target_metric}")
        
        if self.optimize_direction not in ("maximize", "minimize"):
            raise ValueError(f"optimize_direction 必须是 'maximize' 或 'minimize'")
        
        if self.method not in ("grid", "random", "bayesian"):
            raise ValueError(f"不支持的优化方法: {self.method}")


__all__ = ["BTConfig", "BTOptimizeConfig"]

