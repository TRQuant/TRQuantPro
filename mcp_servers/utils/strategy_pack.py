"""
M2: Strategy Pack 策略插件层

提供策略插件化架构：
- 策略基类定义
- 策略注册与发现
- 策略生命周期管理
- 策略配置与参数

Author: TRQuant Team
Date: 2025-12-18
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Type, Callable
from enum import Enum
from datetime import datetime
import logging
import importlib
import inspect

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """策略类型"""
    FACTOR = "factor"           # 因子策略
    MOMENTUM = "momentum"       # 动量策略
    VALUE = "value"             # 价值策略
    GROWTH = "growth"           # 成长策略
    EVENT = "event"             # 事件驱动
    TENBAGGER = "tenbagger"     # 十倍股
    HYBRID = "hybrid"           # 混合策略


class StrategyStatus(Enum):
    """策略状态"""
    DRAFT = "draft"             # 草稿
    TESTING = "testing"         # 测试中
    ACTIVE = "active"           # 激活
    PAUSED = "paused"           # 暂停
    DEPRECATED = "deprecated"   # 已废弃


@dataclass
class StrategyConfig:
    """策略配置"""
    name: str                           # 策略名称
    version: str = "1.0.0"              # 版本号
    strategy_type: StrategyType = StrategyType.FACTOR
    description: str = ""               # 描述
    author: str = ""                    # 作者
    
    # 参数配置
    params: Dict[str, Any] = field(default_factory=dict)
    
    # 风控配置
    max_position: float = 0.1           # 单票最大仓位
    stop_loss: float = 0.08             # 止损线
    take_profit: float = 0.2            # 止盈线
    max_drawdown: float = 0.15          # 最大回撤
    
    # 运行配置
    universe: str = "HS300"             # 股票池
    rebalance_freq: str = "weekly"      # 调仓频率
    benchmark: str = "000300.SH"        # 基准
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "strategy_type": self.strategy_type.value,
            "description": self.description,
            "author": self.author,
            "params": self.params,
            "max_position": self.max_position,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "max_drawdown": self.max_drawdown,
            "universe": self.universe,
            "rebalance_freq": self.rebalance_freq,
            "benchmark": self.benchmark
        }


class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, config: StrategyConfig):
        self.config = config
        self.status = StrategyStatus.DRAFT
        self._signals: List[Dict] = []
        self._positions: Dict[str, float] = {}
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def strategy_type(self) -> StrategyType:
        return self.config.strategy_type
    
    @abstractmethod
    def generate_signals(self, data: Dict[str, Any]) -> List[Dict]:
        """
        生成交易信号
        
        Args:
            data: 市场数据
        
        Returns:
            信号列表 [{"symbol": "xxx", "action": "buy/sell", "weight": 0.1}, ...]
        """
        pass
    
    @abstractmethod
    def select_stocks(self, universe: List[str], data: Dict[str, Any]) -> List[str]:
        """
        选股逻辑
        
        Args:
            universe: 股票池
            data: 市场数据
        
        Returns:
            选中的股票列表
        """
        pass
    
    def on_init(self):
        """策略初始化回调"""
        logger.info(f"策略初始化: {self.name}")
    
    def on_start(self):
        """策略启动回调"""
        self.status = StrategyStatus.ACTIVE
        logger.info(f"策略启动: {self.name}")
    
    def on_stop(self):
        """策略停止回调"""
        self.status = StrategyStatus.PAUSED
        logger.info(f"策略停止: {self.name}")
    
    def validate(self) -> bool:
        """验证策略配置"""
        if not self.config.name:
            return False
        if self.config.max_position <= 0 or self.config.max_position > 1:
            return False
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """获取策略信息"""
        return {
            "name": self.name,
            "type": self.strategy_type.value,
            "status": self.status.value,
            "config": self.config.to_dict(),
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }


class StrategyRegistry:
    """策略注册表"""
    
    def __init__(self):
        self._strategies: Dict[str, Type[BaseStrategy]] = {}
        self._instances: Dict[str, BaseStrategy] = {}
        self._metadata: Dict[str, Dict] = {}
    
    def register(self, name: str, strategy_class: Type[BaseStrategy], 
                 metadata: Optional[Dict] = None) -> bool:
        """
        注册策略类
        
        Args:
            name: 策略名称
            strategy_class: 策略类
            metadata: 元数据
        """
        if not issubclass(strategy_class, BaseStrategy):
            logger.error(f"策略类必须继承BaseStrategy: {strategy_class}")
            return False
        
        self._strategies[name] = strategy_class
        self._metadata[name] = metadata or {}
        logger.info(f"策略已注册: {name}")
        return True
    
    def unregister(self, name: str) -> bool:
        """注销策略"""
        if name in self._strategies:
            del self._strategies[name]
            if name in self._metadata:
                del self._metadata[name]
            if name in self._instances:
                del self._instances[name]
            logger.info(f"策略已注销: {name}")
            return True
        return False
    
    def get_class(self, name: str) -> Optional[Type[BaseStrategy]]:
        """获取策略类"""
        return self._strategies.get(name)
    
    def create_instance(self, name: str, config: StrategyConfig) -> Optional[BaseStrategy]:
        """创建策略实例"""
        strategy_class = self._strategies.get(name)
        if not strategy_class:
            logger.error(f"策略未注册: {name}")
            return None
        
        instance = strategy_class(config)
        self._instances[f"{name}_{config.version}"] = instance
        return instance
    
    def get_instance(self, key: str) -> Optional[BaseStrategy]:
        """获取策略实例"""
        return self._instances.get(key)
    
    def list_strategies(self) -> List[Dict[str, Any]]:
        """列出所有注册的策略"""
        result = []
        for name, cls in self._strategies.items():
            meta = self._metadata.get(name, {})
            result.append({
                "name": name,
                "class": cls.__name__,
                "module": cls.__module__,
                "description": meta.get("description", ""),
                "type": meta.get("type", "unknown"),
                "author": meta.get("author", "")
            })
        return result
    
    def list_instances(self) -> List[Dict[str, Any]]:
        """列出所有策略实例"""
        return [inst.get_info() for inst in self._instances.values()]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        type_counts = {}
        for name, cls in self._strategies.items():
            stype = self._metadata.get(name, {}).get("type", "unknown")
            type_counts[stype] = type_counts.get(stype, 0) + 1
        
        return {
            "total_registered": len(self._strategies),
            "total_instances": len(self._instances),
            "by_type": type_counts
        }


# ==================== 内置策略实现 ====================

class FactorStrategy(BaseStrategy):
    """因子策略"""
    
    def generate_signals(self, data: Dict[str, Any]) -> List[Dict]:
        signals = []
        factors = data.get("factors", {})
        threshold = self.config.params.get("threshold", 0.7)
        
        for symbol, score in factors.items():
            if score >= threshold:
                signals.append({
                    "symbol": symbol,
                    "action": "buy",
                    "weight": min(score / 10, self.config.max_position),
                    "reason": f"因子得分: {score:.2f}"
                })
        
        return signals
    
    def select_stocks(self, universe: List[str], data: Dict[str, Any]) -> List[str]:
        factors = data.get("factors", {})
        threshold = self.config.params.get("threshold", 0.7)
        
        selected = [s for s in universe if factors.get(s, 0) >= threshold]
        return sorted(selected, key=lambda x: factors.get(x, 0), reverse=True)


class TenbaggerStrategy(BaseStrategy):
    """十倍股策略"""
    
    def generate_signals(self, data: Dict[str, Any]) -> List[Dict]:
        signals = []
        stages = data.get("stages", {})
        scorecards = data.get("scorecards", {})
        
        min_stage = self.config.params.get("min_stage", 2)
        min_score = self.config.params.get("min_score", 50)
        
        for symbol in stages.keys():
            stage_num = int(stages.get(symbol, "S0")[1])
            score = scorecards.get(symbol, {}).get("total_score", 0)
            
            if stage_num >= min_stage and score >= min_score:
                signals.append({
                    "symbol": symbol,
                    "action": "buy",
                    "weight": self.config.max_position,
                    "reason": f"阶段S{stage_num}, 评分{score:.1f}"
                })
        
        return signals
    
    def select_stocks(self, universe: List[str], data: Dict[str, Any]) -> List[str]:
        stages = data.get("stages", {})
        scorecards = data.get("scorecards", {})
        
        min_stage = self.config.params.get("min_stage", 2)
        min_score = self.config.params.get("min_score", 50)
        
        candidates = []
        for symbol in universe:
            stage_num = int(stages.get(symbol, "S0")[1])
            score = scorecards.get(symbol, {}).get("total_score", 0)
            
            if stage_num >= min_stage and score >= min_score:
                candidates.append((symbol, stage_num, score))
        
        # 按阶段和评分排序
        candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return [c[0] for c in candidates]


class MomentumStrategy(BaseStrategy):
    """动量策略"""
    
    def generate_signals(self, data: Dict[str, Any]) -> List[Dict]:
        signals = []
        returns = data.get("returns", {})
        lookback = self.config.params.get("lookback_days", 20)
        threshold = self.config.params.get("momentum_threshold", 0.05)
        
        for symbol, ret in returns.items():
            if ret >= threshold:
                signals.append({
                    "symbol": symbol,
                    "action": "buy",
                    "weight": self.config.max_position,
                    "reason": f"{lookback}日动量: {ret*100:.1f}%"
                })
        
        return signals
    
    def select_stocks(self, universe: List[str], data: Dict[str, Any]) -> List[str]:
        returns = data.get("returns", {})
        threshold = self.config.params.get("momentum_threshold", 0.05)
        
        selected = [s for s in universe if returns.get(s, 0) >= threshold]
        return sorted(selected, key=lambda x: returns.get(x, 0), reverse=True)


# ==================== 全局实例 ====================

_registry: Optional[StrategyRegistry] = None


def get_strategy_registry() -> StrategyRegistry:
    """获取策略注册表单例"""
    global _registry
    if _registry is None:
        _registry = StrategyRegistry()
        # 注册内置策略
        _registry.register("factor", FactorStrategy, {
            "type": "factor",
            "description": "多因子选股策略",
            "author": "TRQuant"
        })
        _registry.register("tenbagger", TenbaggerStrategy, {
            "type": "tenbagger",
            "description": "十倍股识别策略",
            "author": "TRQuant"
        })
        _registry.register("momentum", MomentumStrategy, {
            "type": "momentum",
            "description": "动量策略",
            "author": "TRQuant"
        })
    return _registry
