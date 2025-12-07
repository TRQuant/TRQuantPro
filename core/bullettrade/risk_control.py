"""风控引擎

实现实盘交易的风险控制功能：
- 回撤监控
- 止损/止盈
- 持仓限制
- 交易频率限制
- 异常告警
"""

from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, time, timedelta
import logging
import threading

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """风险级别"""
    NORMAL = "normal"       # 正常
    WARNING = "warning"     # 警告
    DANGER = "danger"       # 危险
    CRITICAL = "critical"   # 严重


class RiskAction(Enum):
    """风险处理动作"""
    NONE = "none"           # 无动作
    ALERT = "alert"         # 告警
    REDUCE = "reduce"       # 减仓
    STOP = "stop"           # 停止交易


@dataclass
class RiskRule:
    """风险规则
    
    Attributes:
        name: 规则名称
        enabled: 是否启用
        threshold: 触发阈值
        action: 触发动作
        cooldown: 冷却时间（秒）
    """
    name: str
    enabled: bool = True
    threshold: float = 0.0
    action: RiskAction = RiskAction.ALERT
    cooldown: int = 300  # 5分钟


@dataclass
class RiskConfig:
    """风控配置
    
    Attributes:
        max_drawdown: 最大回撤限制（%）
        daily_loss_limit: 日内最大亏损（%）
        single_position_limit: 单只股票最大仓位（%）
        total_position_limit: 总仓位上限（%）
        stop_loss: 止损比例（%）
        take_profit: 止盈比例（%）
        max_trades_per_day: 每日最大交易次数
        trade_time_start: 交易时段开始
        trade_time_end: 交易时段结束
    """
    # 回撤限制
    max_drawdown: float = 10.0
    daily_loss_limit: float = 5.0
    
    # 仓位限制
    single_position_limit: float = 20.0
    total_position_limit: float = 80.0
    
    # 止损止盈
    stop_loss: float = 8.0
    take_profit: float = 20.0
    
    # 交易限制
    max_trades_per_day: int = 50
    min_trade_interval: int = 60  # 秒
    
    # 交易时段
    trade_time_start: time = field(default_factory=lambda: time(9, 30))
    trade_time_end: time = field(default_factory=lambda: time(15, 0))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_drawdown": self.max_drawdown,
            "daily_loss_limit": self.daily_loss_limit,
            "single_position_limit": self.single_position_limit,
            "total_position_limit": self.total_position_limit,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "max_trades_per_day": self.max_trades_per_day,
            "trade_time_start": self.trade_time_start.isoformat(),
            "trade_time_end": self.trade_time_end.isoformat()
        }


@dataclass
class RiskEvent:
    """风险事件"""
    timestamp: datetime
    level: RiskLevel
    rule_name: str
    message: str
    action_taken: RiskAction
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskStatus:
    """风险状态"""
    level: RiskLevel = RiskLevel.NORMAL
    events: List[RiskEvent] = field(default_factory=list)
    is_trading_allowed: bool = True
    message: str = "正常"
    
    # 当日统计
    daily_pnl: float = 0.0
    daily_pnl_pct: float = 0.0
    current_drawdown: float = 0.0
    peak_value: float = 0.0
    trades_today: int = 0
    last_trade_time: Optional[datetime] = None


class RiskControlEngine:
    """风控引擎
    
    监控交易风险，执行风控策略
    
    Example:
        >>> config = RiskConfig(
        ...     max_drawdown=10.0,
        ...     stop_loss=8.0,
        ...     take_profit=20.0
        ... )
        >>> risk_engine = RiskControlEngine(config)
        >>> risk_engine.set_alert_callback(send_alert)
        >>> 
        >>> # 检查交易前风控
        >>> if risk_engine.check_pre_trade("000001.XSHE", 100, 10.0):
        ...     # 执行交易
        ...     pass
    """
    
    def __init__(self, config: Optional[RiskConfig] = None):
        """初始化风控引擎
        
        Args:
            config: 风控配置
        """
        self.config = config or RiskConfig()
        self._status = RiskStatus()
        self._lock = threading.Lock()
        
        # 回调
        self._on_alert: Optional[Callable[[RiskEvent], None]] = None
        self._on_action: Optional[Callable[[RiskAction, str], None]] = None
        
        # 初始化状态
        self._status.peak_value = 1000000.0  # 初始资金
    
    def set_alert_callback(self, callback: Callable[[RiskEvent], None]) -> None:
        """设置告警回调"""
        self._on_alert = callback
    
    def set_action_callback(self, callback: Callable[[RiskAction, str], None]) -> None:
        """设置动作回调"""
        self._on_action = callback
    
    def get_status(self) -> RiskStatus:
        """获取风控状态"""
        return self._status
    
    def update_account_value(
        self,
        current_value: float,
        daily_pnl: float,
        initial_value: float = 1000000.0
    ) -> RiskLevel:
        """更新账户价值，检查风险
        
        Args:
            current_value: 当前账户价值
            daily_pnl: 当日盈亏
            initial_value: 初始资金
            
        Returns:
            当前风险级别
        """
        with self._lock:
            # 更新峰值
            if current_value > self._status.peak_value:
                self._status.peak_value = current_value
            
            # 计算回撤
            drawdown = (self._status.peak_value - current_value) / self._status.peak_value * 100
            self._status.current_drawdown = drawdown
            
            # 计算日内盈亏
            self._status.daily_pnl = daily_pnl
            self._status.daily_pnl_pct = daily_pnl / initial_value * 100
            
            # 检查风险
            return self._check_risks()
    
    def _check_risks(self) -> RiskLevel:
        """检查各项风险"""
        max_level = RiskLevel.NORMAL
        
        # 检查最大回撤
        if self._status.current_drawdown >= self.config.max_drawdown:
            event = self._create_event(
                RiskLevel.CRITICAL,
                "max_drawdown",
                f"触发最大回撤限制: {self._status.current_drawdown:.2f}% >= {self.config.max_drawdown}%",
                RiskAction.STOP
            )
            self._handle_event(event)
            max_level = RiskLevel.CRITICAL
        elif self._status.current_drawdown >= self.config.max_drawdown * 0.8:
            event = self._create_event(
                RiskLevel.DANGER,
                "max_drawdown",
                f"接近最大回撤限制: {self._status.current_drawdown:.2f}%",
                RiskAction.ALERT
            )
            self._handle_event(event)
            if max_level.value < RiskLevel.DANGER.value:
                max_level = RiskLevel.DANGER
        
        # 检查日内亏损
        if abs(self._status.daily_pnl_pct) >= self.config.daily_loss_limit and self._status.daily_pnl_pct < 0:
            event = self._create_event(
                RiskLevel.CRITICAL,
                "daily_loss",
                f"触发日内亏损限制: {self._status.daily_pnl_pct:.2f}% >= {self.config.daily_loss_limit}%",
                RiskAction.STOP
            )
            self._handle_event(event)
            max_level = RiskLevel.CRITICAL
        
        # 更新状态
        self._status.level = max_level
        self._status.is_trading_allowed = max_level != RiskLevel.CRITICAL
        self._status.message = self._get_status_message(max_level)
        
        return max_level
    
    def check_pre_trade(
        self,
        security: str,
        amount: int,
        price: float,
        side: str = "buy",
        current_positions: Optional[Dict[str, float]] = None
    ) -> bool:
        """交易前风控检查
        
        Args:
            security: 证券代码
            amount: 交易数量
            price: 交易价格
            side: 买卖方向
            current_positions: 当前持仓
            
        Returns:
            是否允许交易
        """
        with self._lock:
            # 检查是否允许交易
            if not self._status.is_trading_allowed:
                logger.warning(f"交易被风控禁止: {self._status.message}")
                return False
            
            # 检查交易时段
            now = datetime.now().time()
            if not (self.config.trade_time_start <= now <= self.config.trade_time_end):
                logger.warning(f"当前时间 {now} 不在交易时段内")
                return False
            
            # 检查交易次数
            if self._status.trades_today >= self.config.max_trades_per_day:
                logger.warning(f"已达到每日最大交易次数: {self.config.max_trades_per_day}")
                return False
            
            # 检查交易间隔
            if self._status.last_trade_time:
                elapsed = (datetime.now() - self._status.last_trade_time).total_seconds()
                if elapsed < self.config.min_trade_interval:
                    logger.warning(f"交易间隔不足: {elapsed:.0f}s < {self.config.min_trade_interval}s")
                    return False
            
            # 检查仓位限制（仅买入时）
            if side == "buy" and current_positions:
                total_position = sum(current_positions.values())
                trade_value = amount * price
                
                # 单只股票仓位
                security_position = current_positions.get(security, 0) + trade_value
                if security_position > self._status.peak_value * self.config.single_position_limit / 100:
                    logger.warning(f"超过单只股票仓位限制: {self.config.single_position_limit}%")
                    return False
                
                # 总仓位
                new_total = total_position + trade_value
                if new_total > self._status.peak_value * self.config.total_position_limit / 100:
                    logger.warning(f"超过总仓位限制: {self.config.total_position_limit}%")
                    return False
            
            return True
    
    def record_trade(self, security: str, side: str, amount: int, price: float) -> None:
        """记录交易"""
        with self._lock:
            self._status.trades_today += 1
            self._status.last_trade_time = datetime.now()
    
    def check_position_risk(
        self,
        security: str,
        cost_basis: float,
        current_price: float
    ) -> Optional[RiskAction]:
        """检查持仓风险（止损止盈）
        
        Args:
            security: 证券代码
            cost_basis: 成本价
            current_price: 当前价
            
        Returns:
            建议动作
        """
        pnl_pct = (current_price - cost_basis) / cost_basis * 100
        
        # 止损
        if pnl_pct <= -self.config.stop_loss:
            event = self._create_event(
                RiskLevel.DANGER,
                "stop_loss",
                f"{security} 触发止损: {pnl_pct:.2f}% <= -{self.config.stop_loss}%",
                RiskAction.REDUCE
            )
            self._handle_event(event)
            return RiskAction.REDUCE
        
        # 止盈
        if pnl_pct >= self.config.take_profit:
            event = self._create_event(
                RiskLevel.WARNING,
                "take_profit",
                f"{security} 触发止盈: {pnl_pct:.2f}% >= {self.config.take_profit}%",
                RiskAction.ALERT
            )
            self._handle_event(event)
            return RiskAction.ALERT
        
        return None
    
    def reset_daily(self) -> None:
        """重置日内统计"""
        with self._lock:
            self._status.daily_pnl = 0.0
            self._status.daily_pnl_pct = 0.0
            self._status.trades_today = 0
            self._status.last_trade_time = None
            self._status.events = []
            
            # 如果之前被停止，检查是否可以恢复
            if self._status.level == RiskLevel.CRITICAL:
                self._status.level = RiskLevel.NORMAL
                self._status.is_trading_allowed = True
                self._status.message = "日内风控已重置"
    
    def _create_event(
        self,
        level: RiskLevel,
        rule_name: str,
        message: str,
        action: RiskAction
    ) -> RiskEvent:
        """创建风险事件"""
        return RiskEvent(
            timestamp=datetime.now(),
            level=level,
            rule_name=rule_name,
            message=message,
            action_taken=action,
            details={
                "current_drawdown": self._status.current_drawdown,
                "daily_pnl_pct": self._status.daily_pnl_pct,
                "trades_today": self._status.trades_today
            }
        )
    
    def _handle_event(self, event: RiskEvent) -> None:
        """处理风险事件"""
        self._status.events.append(event)
        logger.warning(f"[风控] {event.level.value}: {event.message}")
        
        # 触发告警
        if self._on_alert:
            self._on_alert(event)
        
        # 执行动作
        if event.action_taken != RiskAction.NONE and self._on_action:
            self._on_action(event.action_taken, event.message)
    
    def _get_status_message(self, level: RiskLevel) -> str:
        """获取状态消息"""
        messages = {
            RiskLevel.NORMAL: "正常",
            RiskLevel.WARNING: "警告：接近风控阈值",
            RiskLevel.DANGER: "危险：建议减仓",
            RiskLevel.CRITICAL: "严重：交易已暂停"
        }
        return messages.get(level, "未知")


def create_default_risk_config() -> RiskConfig:
    """创建默认风控配置"""
    return RiskConfig(
        max_drawdown=10.0,
        daily_loss_limit=5.0,
        single_position_limit=20.0,
        total_position_limit=80.0,
        stop_loss=8.0,
        take_profit=20.0,
        max_trades_per_day=50
    )



