"""
股票池数据模型

定义股票池的核心数据结构，确保与前后模块的数据格式兼容：
- 输入：主线识别模块的 latest_heatmap_scores.json
- 输出：标准化股票池JSON，供因子模块和策略模块使用
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
import json
from pathlib import Path


class PoolSource(Enum):
    """股票入池来源"""
    MAINLINE = "mainline"           # 主线强势股
    TECH_BREAKOUT = "tech_breakout" # 技术突破股
    BROKER = "broker"               # 券商金股
    GURUFOCUS = "gurufocus"         # GuruFocus筛选
    CUSTOM = "custom"               # 自定义筛选
    MANUAL = "manual"               # 手动添加


class PoolType(Enum):
    """持仓类型"""
    CORE = "core"           # 核心仓位（60%）
    SATELLITE = "satellite" # 卫星仓位（30%）
    WATCH = "watch"         # 观察仓位（10%）


class Period(Enum):
    """投资周期"""
    SHORT = "short"     # 短期（1-20日）
    MEDIUM = "medium"   # 中期（20-120日）
    LONG = "long"       # 长期（120-500日）


class SignalAction(Enum):
    """交易信号动作"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    WATCH = "watch"     # 观察，等待时机


@dataclass
class TechSignal:
    """技术信号"""
    name: str                       # 信号名称
    triggered: bool                 # 是否触发
    value: float = 0.0              # 信号值
    description: str = ""           # 描述
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class StockPoolItem:
    """
    股票池条目
    
    这是股票池的核心数据单元，包含：
    - 基本信息：代码、名称、行业
    - 入池信息：来源、原因、时间
    - 分类信息：周期、持仓类型、优先级
    - 评分信息：主线评分、技术信号
    - 联动信息：关联的主线、因子评分（预留）
    """
    # 基本信息
    code: str                       # 股票代码
    name: str                       # 股票名称
    industry: str = ""              # 所属行业
    sector: str = ""                # 所属板块/概念
    
    # 入池信息
    source: str = "mainline"        # 入池来源（PoolSource枚举值）
    entry_reason: str = ""          # 入池原因
    entry_date: str = ""            # 入池日期
    
    # 分类信息
    period: str = "medium"          # 投资周期（Period枚举值）
    pool_type: str = "core"         # 持仓类型（PoolType枚举值）
    priority: int = 3               # 优先级（1最高，5最低）
    
    # 评分信息（与主线识别模块衔接）
    mainline_name: str = ""         # 关联的主线名称
    mainline_score: float = 0.0     # 主线综合评分
    heat_score: float = 0.0         # 热度评分
    funds_score: float = 0.0        # 资金评分
    momentum_score: float = 0.0     # 动量评分
    
    # 技术信号
    tech_signals: List[str] = field(default_factory=list)  # 技术信号列表
    
    # 价格信息
    current_price: float = 0.0      # 当前价格
    change_pct: float = 0.0         # 涨跌幅
    
    # 因子评分（供因子模块填充）
    factor_scores: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 0.0    # 综合因子得分
    
    # 元信息
    update_time: str = ""           # 最后更新时间
    notes: str = ""                 # 备注
    
    def __post_init__(self):
        if not self.entry_date:
            self.entry_date = datetime.now().strftime("%Y-%m-%d")
        if not self.update_time:
            self.update_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典（用于JSON序列化）"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StockPoolItem':
        """从字典创建"""
        return cls(**data)
    
    def update_factor_score(self, factor_name: str, score: float):
        """更新因子评分（供因子模块调用）"""
        self.factor_scores[factor_name] = score
        self.update_time = datetime.now().isoformat()
    
    def calculate_composite_score(self, weights: Dict[str, float] = None):
        """计算综合评分"""
        if not self.factor_scores:
            return
        
        if weights is None:
            # 默认等权
            weights = {k: 1.0 / len(self.factor_scores) for k in self.factor_scores}
        
        self.composite_score = sum(
            self.factor_scores.get(k, 0) * v 
            for k, v in weights.items()
        )


@dataclass
class StockPool:
    """
    股票池
    
    管理一组股票池条目，提供：
    - 增删改查操作
    - 分类筛选
    - 与前后模块的数据交换
    """
    # 元信息
    version: str = "1.0"
    created_at: str = ""
    updated_at: str = ""
    description: str = ""
    
    # 股票列表
    stocks: List[StockPoolItem] = field(default_factory=list)
    
    # 统计信息
    summary: Dict[str, Any] = field(default_factory=dict)
    
    # 来源信息（与主线识别模块衔接）
    mainline_source: str = ""       # 主线识别结果文件路径
    mainline_timestamp: str = ""    # 主线识别时间戳
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def add_stock(self, item: StockPoolItem) -> bool:
        """添加股票（去重）"""
        if not any(s.code == item.code for s in self.stocks):
            self.stocks.append(item)
            self._update_summary()
            return True
        return False
    
    def remove_stock(self, code: str) -> bool:
        """移除股票"""
        original_len = len(self.stocks)
        self.stocks = [s for s in self.stocks if s.code != code]
        if len(self.stocks) < original_len:
            self._update_summary()
            return True
        return False
    
    def get_stock(self, code: str) -> Optional[StockPoolItem]:
        """获取股票"""
        for s in self.stocks:
            if s.code == code:
                return s
        return None
    
    def filter_by_source(self, source: str) -> List[StockPoolItem]:
        """按来源筛选"""
        return [s for s in self.stocks if s.source == source]
    
    def filter_by_period(self, period: str) -> List[StockPoolItem]:
        """按周期筛选"""
        return [s for s in self.stocks if s.period == period]
    
    def filter_by_pool_type(self, pool_type: str) -> List[StockPoolItem]:
        """按持仓类型筛选"""
        return [s for s in self.stocks if s.pool_type == pool_type]
    
    def filter_by_priority(self, max_priority: int) -> List[StockPoolItem]:
        """按优先级筛选（<=max_priority）"""
        return [s for s in self.stocks if s.priority <= max_priority]
    
    def get_codes(self) -> List[str]:
        """获取所有股票代码（供因子模块使用）"""
        return [s.code for s in self.stocks]
    
    def get_top_stocks(self, n: int = 20, sort_by: str = "priority") -> List[StockPoolItem]:
        """获取排名靠前的股票"""
        if sort_by == "priority":
            sorted_stocks = sorted(self.stocks, key=lambda x: x.priority)
        elif sort_by == "mainline_score":
            sorted_stocks = sorted(self.stocks, key=lambda x: x.mainline_score, reverse=True)
        elif sort_by == "composite_score":
            sorted_stocks = sorted(self.stocks, key=lambda x: x.composite_score, reverse=True)
        else:
            sorted_stocks = self.stocks
        return sorted_stocks[:n]
    
    def _update_summary(self):
        """更新统计信息"""
        self.updated_at = datetime.now().isoformat()
        
        # 按来源统计
        by_source = {}
        for s in self.stocks:
            by_source[s.source] = by_source.get(s.source, 0) + 1
        
        # 按周期统计
        by_period = {}
        for s in self.stocks:
            by_period[s.period] = by_period.get(s.period, 0) + 1
        
        # 按持仓类型统计
        by_pool_type = {}
        for s in self.stocks:
            by_pool_type[s.pool_type] = by_pool_type.get(s.pool_type, 0) + 1
        
        self.summary = {
            "total_count": len(self.stocks),
            "by_source": by_source,
            "by_period": by_period,
            "by_pool_type": by_pool_type
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        self._update_summary()
        return {
            "_meta": {
                "version": self.version,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "description": self.description
            },
            "mainline_source": self.mainline_source,
            "mainline_timestamp": self.mainline_timestamp,
            "summary": self.summary,
            "stocks": [s.to_dict() for s in self.stocks]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StockPool':
        """从字典创建"""
        meta = data.get("_meta", {})
        stocks = [StockPoolItem.from_dict(s) for s in data.get("stocks", [])]
        return cls(
            version=meta.get("version", "1.0"),
            created_at=meta.get("created_at", ""),
            updated_at=meta.get("updated_at", ""),
            description=meta.get("description", ""),
            stocks=stocks,
            summary=data.get("summary", {}),
            mainline_source=data.get("mainline_source", ""),
            mainline_timestamp=data.get("mainline_timestamp", "")
        )
    
    def save(self, filepath: Path):
        """保存到文件"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: Path) -> 'StockPool':
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class TradeSignal:
    """
    交易信号
    
    股票池 → 因子评分 → 【交易信号】→ 策略执行
    
    这是连接股票池和策略模块的桥梁
    """
    signal_id: str                  # 信号ID
    stock_code: str                 # 股票代码
    stock_name: str                 # 股票名称
    
    # 信号信息
    action: str                     # 动作（SignalAction枚举值）
    target_position: float = 0.0    # 目标仓位比例（0-1）
    current_position: float = 0.0   # 当前仓位比例
    
    # 价格信息
    entry_price: float = 0.0        # 建议入场价
    stop_loss: float = 0.0          # 止损价
    take_profit: float = 0.0        # 止盈价
    current_price: float = 0.0      # 当前价格
    
    # 来源信息
    strategy: str = ""              # 策略名称
    pool_source: str = ""           # 股票池来源
    reason: str = ""                # 信号原因
    
    # 优先级和有效期
    priority: int = 3               # 优先级（1-5）
    valid_until: str = ""           # 有效期
    
    # 状态
    status: str = "pending"         # pending/executed/cancelled/expired
    
    # 时间戳
    created_at: str = ""
    executed_at: str = ""
    
    # 因子评分（来自因子模块）
    factor_scores: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 0.0
    
    def __post_init__(self):
        if not self.signal_id:
            self.signal_id = f"{self.stock_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TradeSignal':
        return cls(**data)
    
    def to_ptrade_order(self) -> Dict:
        """转换为PTrade订单格式"""
        return {
            "stock": self.stock_code,
            "action": self.action.upper(),
            "price": self.entry_price,
            "amount": self.target_position,  # 需要转换为具体股数
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit
        }
    
    def to_qmt_order(self) -> Dict:
        """转换为QMT订单格式"""
        return {
            "stockcode": self.stock_code,
            "tradetype": 23 if self.action == "buy" else 24,  # QMT交易类型
            "price": self.entry_price,
            "volume": 0  # 需要根据仓位计算
        }


# ============================================================
# 与前后模块衔接的辅助函数
# ============================================================

def load_mainline_scores(filepath: Path = None) -> Dict:
    """
    读取主线识别模块的输出
    
    这是与前置模块（主线识别）的衔接点
    
    Returns:
        主线识别结果字典
    """
    if filepath is None:
        filepath = Path.home() / ".local/share/trquant/reports/heatmap/latest_heatmap_scores.json"
    
    if not filepath.exists():
        return {"scores": [], "high_heat_mainlines": [], "timestamp": ""}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_pool_for_factor_module(pool: StockPool, filepath: Path = None):
    """
    保存股票池供因子模块使用
    
    这是与后续模块（因子开发）的衔接点
    """
    if filepath is None:
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = Path.home() / f".local/share/trquant/data/stock_pool/daily/pool_{date_str}.json"
    
    pool.save(filepath)
    return filepath


def load_pool_for_strategy_module(filepath: Path = None) -> StockPool:
    """
    加载股票池供策略模块使用
    
    这是与后续模块（策略生成）的衔接点
    """
    if filepath is None:
        # 加载最新的股票池
        pool_dir = Path.home() / ".local/share/trquant/data/stock_pool/daily"
        pool_files = sorted(pool_dir.glob("pool_*.json"), reverse=True)
        if pool_files:
            filepath = pool_files[0]
        else:
            return StockPool()
    
    return StockPool.load(filepath)




