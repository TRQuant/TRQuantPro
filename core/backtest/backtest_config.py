"""回测配置管理

定义回测参数和配置文件解析
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import yaml
import json
import logging

logger = logging.getLogger(__name__)


class BacktestFrequency(Enum):
    """回测频率"""
    DAILY = "day"
    MINUTE = "minute"
    TICK = "tick"


@dataclass
class BacktestConfig:
    """回测配置
    
    Attributes:
        strategy_path: 策略文件路径
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        frequency: 回测频率
        initial_capital: 初始资金
        benchmark: 基准指数
        commission_rate: 佣金费率
        slippage: 滑点
        tax_rate: 印花税率
        data_provider: 数据源
        output_dir: 输出目录
        strategy_name: 策略名称
        strategy_version: 策略版本
    """
    strategy_path: str
    start_date: str = "2020-01-01"
    end_date: str = "2023-12-31"
    frequency: BacktestFrequency = BacktestFrequency.DAILY
    initial_capital: float = 1000000.0
    benchmark: str = "000300.XSHG"
    commission_rate: float = 0.0003
    slippage: float = 0.001
    tax_rate: float = 0.001
    data_provider: str = "jqdata"
    output_dir: Optional[str] = None
    strategy_name: Optional[str] = None
    strategy_version: str = "v1"
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        # 自动推断策略名称
        if not self.strategy_name:
            self.strategy_name = Path(self.strategy_path).stem
        
        # 自动设置输出目录
        if not self.output_dir:
            self.output_dir = f"backtests/{self.strategy_name}/{self.strategy_version}"
        
        # 转换频率
        if isinstance(self.frequency, str):
            self.frequency = BacktestFrequency(self.frequency)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "strategy_path": self.strategy_path,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "frequency": self.frequency.value if isinstance(self.frequency, BacktestFrequency) else self.frequency,
            "initial_capital": self.initial_capital,
            "benchmark": self.benchmark,
            "commission_rate": self.commission_rate,
            "slippage": self.slippage,
            "tax_rate": self.tax_rate,
            "data_provider": self.data_provider,
            "output_dir": self.output_dir,
            "strategy_name": self.strategy_name,
            "strategy_version": self.strategy_version,
            **self.extra_params
        }
    
    def save(self, path: Optional[str] = None) -> str:
        """保存配置到文件
        
        Args:
            path: 文件路径，默认保存到输出目录
            
        Returns:
            保存的文件路径
        """
        if not path:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            path = f"{self.output_dir}/config.yaml"
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False)
        
        logger.info(f"Config saved to: {path}")
        return path
    
    @classmethod
    def from_file(cls, path: str) -> "BacktestConfig":
        """从文件加载配置
        
        Args:
            path: 配置文件路径 (YAML 或 JSON)
            
        Returns:
            BacktestConfig 实例
        """
        path = Path(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif path.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {path.suffix}")
        
        return cls(**data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BacktestConfig":
        """从字典创建配置"""
        return cls(**data)
    
    def validate(self) -> List[str]:
        """验证配置
        
        Returns:
            错误信息列表，空列表表示配置有效
        """
        errors = []
        
        # 检查策略文件
        if not Path(self.strategy_path).exists():
            errors.append(f"策略文件不存在: {self.strategy_path}")
        
        # 检查日期
        try:
            from datetime import datetime
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            if start >= end:
                errors.append("开始日期必须早于结束日期")
        except ValueError as e:
            errors.append(f"日期格式错误: {e}")
        
        # 检查资金
        if self.initial_capital <= 0:
            errors.append("初始资金必须大于0")
        
        # 检查费率
        if self.commission_rate < 0 or self.commission_rate > 0.1:
            errors.append("佣金费率应在 0-10% 之间")
        
        if self.slippage < 0 or self.slippage > 0.1:
            errors.append("滑点应在 0-10% 之间")
        
        return errors


def create_config(
    strategy_path: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000.0,
    **kwargs
) -> BacktestConfig:
    """创建回测配置的便捷函数
    
    Args:
        strategy_path: 策略文件路径
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        **kwargs: 其他配置参数
        
    Returns:
        BacktestConfig 实例
    """
    return BacktestConfig(
        strategy_path=strategy_path,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        **kwargs
    )


