# -*- coding: utf-8 -*-
"""
事件驱动回测引擎
===============
借鉴Backtrader事件驱动架构设计

事件类型:
- TICK: 行情数据更新
- BAR: K线数据更新
- ORDER: 订单事件
- TRADE: 成交事件
- POSITION: 持仓变化
- SIGNAL: 策略信号

使用方式:
    from core.backtest.event_engine import EventEngine, EventType
    
    engine = EventEngine()
    engine.register(EventType.BAR, my_handler)
    engine.start()
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from queue import Queue, Empty
from threading import Thread
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class EventType(Enum):
    """事件类型枚举"""
    # 行情事件
    TICK = "tick"           # 逐笔数据
    BAR = "bar"             # K线数据
    
    # 交易事件
    ORDER = "order"         # 订单
    TRADE = "trade"         # 成交
    POSITION = "position"   # 持仓
    
    # 策略事件
    SIGNAL = "signal"       # 交易信号
    
    # 系统事件
    TIMER = "timer"         # 定时器
    LOG = "log"             # 日志
    ERROR = "error"         # 错误
    
    # 回测事件
    START = "start"         # 回测开始
    END = "end"             # 回测结束
    DAY_START = "day_start" # 交易日开始
    DAY_END = "day_end"     # 交易日结束


@dataclass
class Event:
    """事件数据类"""
    type: EventType
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    
    def __repr__(self):
        return f"Event({self.type.value}, {self.timestamp})"


@dataclass 
class BarData:
    """K线数据"""
    symbol: str
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float = 0.0
    open_interest: float = 0.0
    
    @property
    def typical_price(self) -> float:
        return (self.high + self.low + self.close) / 3
    
    @property
    def true_range(self) -> float:
        return self.high - self.low


@dataclass
class OrderData:
    """订单数据"""
    order_id: str
    symbol: str
    direction: str  # "buy" or "sell"
    price: float
    volume: float
    order_type: str = "limit"  # "limit" or "market"
    status: str = "pending"    # "pending", "filled", "cancelled"
    filled_volume: float = 0.0
    filled_price: float = 0.0
    create_time: datetime = field(default_factory=datetime.now)
    update_time: datetime = field(default_factory=datetime.now)


@dataclass
class TradeData:
    """成交数据"""
    trade_id: str
    order_id: str
    symbol: str
    direction: str
    price: float
    volume: float
    commission: float = 0.0
    slippage: float = 0.0
    trade_time: datetime = field(default_factory=datetime.now)


@dataclass
class PositionData:
    """持仓数据"""
    symbol: str
    volume: float
    frozen: float = 0.0
    cost: float = 0.0
    pnl: float = 0.0
    market_value: float = 0.0
    
    @property
    def available(self) -> float:
        return self.volume - self.frozen


@dataclass
class SignalData:
    """交易信号数据"""
    symbol: str
    signal_type: str  # "open_long", "close_long", "open_short", "close_short"
    strength: float = 1.0  # 信号强度 0-1
    price: float = 0.0     # 建议价格
    volume: float = 0.0    # 建议数量
    reason: str = ""       # 信号原因
    timestamp: datetime = field(default_factory=datetime.now)


class EventEngine:
    """
    事件驱动引擎
    
    借鉴Backtrader的事件驱动架构：
    - 异步事件队列
    - 多处理器注册
    - 优先级支持
    """
    
    def __init__(self, queue_size: int = 10000):
        """
        初始化事件引擎
        
        Args:
            queue_size: 事件队列大小
        """
        self._queue: Queue = Queue(maxsize=queue_size)
        self._handlers: Dict[EventType, List[Callable]] = {}
        self._general_handlers: List[Callable] = []
        self._active = False
        self._thread: Optional[Thread] = None
        self._timer_thread: Optional[Thread] = None
        self._timer_interval: float = 1.0
        
        # 统计
        self._event_count: Dict[EventType, int] = {}
        self._start_time: Optional[datetime] = None
        
    def register(self, event_type: EventType, handler: Callable, priority: int = 0):
        """
        注册事件处理器
        
        Args:
            event_type: 事件类型
            handler: 处理函数
            priority: 优先级（暂未实现）
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(f"注册处理器: {event_type.value} -> {handler.__name__}")
    
    def unregister(self, event_type: EventType, handler: Callable):
        """注销事件处理器"""
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
                logger.debug(f"注销处理器: {event_type.value} -> {handler.__name__}")
    
    def register_general(self, handler: Callable):
        """注册通用处理器（处理所有事件）"""
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)
    
    def put(self, event: Event):
        """放入事件"""
        try:
            self._queue.put_nowait(event)
        except Exception as e:
            logger.warning(f"事件队列已满，丢弃事件: {event}")
    
    def emit(self, event_type: EventType, data: Any = None, source: str = ""):
        """发送事件（便捷方法）"""
        event = Event(type=event_type, data=data, source=source)
        self.put(event)
    
    def start(self, use_thread: bool = True, enable_timer: bool = False):
        """
        启动事件引擎
        
        Args:
            use_thread: 是否使用独立线程
            enable_timer: 是否启用定时器
        """
        self._active = True
        self._start_time = datetime.now()
        
        if use_thread:
            self._thread = Thread(target=self._run, daemon=True)
            self._thread.start()
            logger.info("事件引擎已启动（线程模式）")
        
        if enable_timer:
            self._timer_thread = Thread(target=self._run_timer, daemon=True)
            self._timer_thread.start()
            logger.info("定时器已启动")
    
    def stop(self):
        """停止事件引擎"""
        self._active = False
        
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._timer_thread:
            self._timer_thread.join(timeout=2.0)
        
        logger.info("事件引擎已停止")
    
    def process_one(self, timeout: float = 0.1) -> bool:
        """
        处理单个事件（同步模式）
        
        Returns:
            是否处理了事件
        """
        try:
            event = self._queue.get(timeout=timeout)
            self._process_event(event)
            return True
        except Empty:
            return False
    
    def process_all(self):
        """处理所有待处理事件（同步模式）"""
        while not self._queue.empty():
            try:
                event = self._queue.get_nowait()
                self._process_event(event)
            except Empty:
                break
    
    def _run(self):
        """事件处理循环（线程模式）"""
        while self._active:
            try:
                event = self._queue.get(timeout=0.1)
                self._process_event(event)
            except Empty:
                continue
            except Exception as e:
                logger.error(f"事件处理异常: {e}")
    
    def _run_timer(self):
        """定时器循环"""
        while self._active:
            self.emit(EventType.TIMER)
            time.sleep(self._timer_interval)
    
    def _process_event(self, event: Event):
        """处理单个事件"""
        # 统计
        self._event_count[event.type] = self._event_count.get(event.type, 0) + 1
        
        # 通用处理器
        for handler in self._general_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"通用处理器异常: {handler.__name__} - {e}")
        
        # 特定类型处理器
        handlers = self._handlers.get(event.type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"事件处理器异常: {handler.__name__} - {e}")
    
    @property
    def pending_count(self) -> int:
        """待处理事件数"""
        return self._queue.qsize()
    
    @property
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = sum(self._event_count.values())
        return {
            "total_events": total,
            "by_type": {k.value: v for k, v in self._event_count.items()},
            "pending": self.pending_count,
            "handlers": {k.value: len(v) for k, v in self._handlers.items()},
            "uptime": (datetime.now() - self._start_time).total_seconds() if self._start_time else 0,
        }


class EventDrivenBacktester:
    """
    事件驱动回测器
    
    借鉴Backtrader的回测框架设计
    """
    
    def __init__(self, 
                 initial_capital: float = 1000000.0,
                 commission_rate: float = 0.0003,
                 slippage: float = 0.001,
                 stamp_tax: float = 0.001):
        """
        初始化回测器
        """
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        self.stamp_tax = stamp_tax
        
        # 事件引擎
        self.event_engine = EventEngine()
        
        # 状态
        self.cash = initial_capital
        self.positions: Dict[str, PositionData] = {}
        self.orders: Dict[str, OrderData] = {}
        self.trades: List[TradeData] = []
        self.equity_curve: List[Dict] = []
        
        # 当前状态
        self.current_datetime: Optional[datetime] = None
        self.current_bars: Dict[str, BarData] = {}
        
        # 注册核心处理器
        self._register_handlers()
        
        # 策略处理器
        self._strategy_handlers: List[Callable] = []
    
    def _register_handlers(self):
        """注册核心事件处理器"""
        self.event_engine.register(EventType.BAR, self._on_bar)
        self.event_engine.register(EventType.ORDER, self._on_order)
        self.event_engine.register(EventType.SIGNAL, self._on_signal)
        self.event_engine.register(EventType.DAY_END, self._on_day_end)
    
    def add_strategy(self, strategy_handler: Callable):
        """
        添加策略处理器
        
        Args:
            strategy_handler: 策略函数，签名为 (backtester, event) -> List[SignalData]
        """
        self._strategy_handlers.append(strategy_handler)
        logger.info(f"添加策略: {strategy_handler.__name__}")
    
    def _on_bar(self, event: Event):
        """处理K线事件"""
        bar: BarData = event.data
        self.current_bars[bar.symbol] = bar
        self.current_datetime = bar.datetime
        
        # 更新持仓市值
        if bar.symbol in self.positions:
            pos = self.positions[bar.symbol]
            pos.market_value = pos.volume * bar.close
            pos.pnl = pos.market_value - pos.cost * pos.volume
        
        # 调用策略
        for handler in self._strategy_handlers:
            try:
                signals = handler(self, event)
                if signals:
                    for signal in signals:
                        self.event_engine.emit(EventType.SIGNAL, signal)
            except Exception as e:
                logger.error(f"策略执行异常: {handler.__name__} - {e}")
    
    def _on_signal(self, event: Event):
        """处理交易信号"""
        signal: SignalData = event.data
        
        # 根据信号生成订单
        if signal.signal_type == "open_long":
            self._create_order(signal.symbol, "buy", signal.price, signal.volume)
        elif signal.signal_type == "close_long":
            if signal.symbol in self.positions:
                pos = self.positions[signal.symbol]
                self._create_order(signal.symbol, "sell", signal.price, pos.available)
    
    def _on_order(self, event: Event):
        """处理订单事件"""
        order: OrderData = event.data
        
        # 简化处理：立即成交
        if order.status == "pending":
            bar = self.current_bars.get(order.symbol)
            if bar:
                # 计算实际成交价（考虑滑点）
                if order.direction == "buy":
                    fill_price = bar.close * (1 + self.slippage)
                else:
                    fill_price = bar.close * (1 - self.slippage)
                
                # 计算手续费
                commission = fill_price * order.volume * self.commission_rate
                if order.direction == "sell":
                    commission += fill_price * order.volume * self.stamp_tax
                
                # 执行成交
                self._execute_trade(order, fill_price, commission)
    
    def _on_day_end(self, event: Event):
        """处理交易日结束事件"""
        # 记录净值
        total_value = self.cash
        for pos in self.positions.values():
            total_value += pos.market_value
        
        self.equity_curve.append({
            "datetime": self.current_datetime,
            "equity": total_value,
            "cash": self.cash,
            "positions_value": total_value - self.cash,
        })
    
    def _create_order(self, symbol: str, direction: str, price: float, volume: float):
        """创建订单"""
        order_id = f"{symbol}_{direction}_{datetime.now().strftime('%H%M%S%f')}"
        
        order = OrderData(
            order_id=order_id,
            symbol=symbol,
            direction=direction,
            price=price,
            volume=volume,
        )
        
        self.orders[order_id] = order
        self.event_engine.emit(EventType.ORDER, order)
    
    def _execute_trade(self, order: OrderData, fill_price: float, commission: float):
        """执行成交"""
        # 更新订单状态
        order.status = "filled"
        order.filled_price = fill_price
        order.filled_volume = order.volume
        order.update_time = self.current_datetime
        
        # 更新现金和持仓
        trade_value = fill_price * order.volume
        
        if order.direction == "buy":
            self.cash -= trade_value + commission
            
            if order.symbol not in self.positions:
                self.positions[order.symbol] = PositionData(symbol=order.symbol, volume=0, cost=0)
            
            pos = self.positions[order.symbol]
            # 计算新均价
            total_cost = pos.cost * pos.volume + fill_price * order.volume
            pos.volume += order.volume
            pos.cost = total_cost / pos.volume if pos.volume > 0 else 0
            pos.market_value = pos.volume * fill_price
            
        else:  # sell
            self.cash += trade_value - commission
            
            if order.symbol in self.positions:
                pos = self.positions[order.symbol]
                pos.volume -= order.volume
                if pos.volume <= 0:
                    del self.positions[order.symbol]
                else:
                    pos.market_value = pos.volume * fill_price
        
        # 记录成交
        trade = TradeData(
            trade_id=f"T_{order.order_id}",
            order_id=order.order_id,
            symbol=order.symbol,
            direction=order.direction,
            price=fill_price,
            volume=order.volume,
            commission=commission,
            trade_time=self.current_datetime,
        )
        self.trades.append(trade)
        
        self.event_engine.emit(EventType.TRADE, trade)
        logger.debug(f"成交: {trade.symbol} {trade.direction} {trade.volume}@{trade.price:.2f}")
    
    def run(self, bar_data: Dict[str, List[BarData]]) -> Dict[str, Any]:
        """
        运行回测
        
        Args:
            bar_data: K线数据 {symbol: [BarData, ...]}
            
        Returns:
            回测结果
        """
        logger.info("🚀 开始事件驱动回测")
        start_time = time.time()
        
        # 发送开始事件
        self.event_engine.emit(EventType.START)
        
        # 整理数据按时间排序
        all_bars = []
        for symbol, bars in bar_data.items():
            for bar in bars:
                all_bars.append(bar)
        all_bars.sort(key=lambda x: x.datetime)
        
        # 逐条处理
        current_date = None
        for bar in all_bars:
            # 日切换
            bar_date = bar.datetime.date()
            if current_date != bar_date:
                if current_date is not None:
                    self.event_engine.emit(EventType.DAY_END)
                    self.event_engine.emit(EventType.DAY_START, bar_date)
                current_date = bar_date
            
            # 发送K线事件
            self.event_engine.emit(EventType.BAR, bar)
            
            # 处理所有事件
            self.event_engine.process_all()
        
        # 最后一天结束
        self.event_engine.emit(EventType.DAY_END)
        self.event_engine.process_all()
        
        # 发送结束事件
        self.event_engine.emit(EventType.END)
        self.event_engine.process_all()
        
        # 计算结果
        run_time = time.time() - start_time
        result = self._calculate_result()
        result["run_time"] = run_time
        result["event_stats"] = self.event_engine.stats
        
        logger.info(f"✅ 回测完成: 收益={result['total_return']:.2%}, 耗时={run_time:.2f}秒")
        
        return result
    
    def _calculate_result(self) -> Dict[str, Any]:
        """计算回测结果"""
        import pandas as pd
        import numpy as np
        
        if not self.equity_curve:
            return {"total_return": 0, "sharpe_ratio": 0, "max_drawdown": 0}
        
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df.set_index("datetime", inplace=True)
        
        # 收益率
        total_return = (equity_df["equity"].iloc[-1] / self.initial_capital) - 1
        
        # 日收益率
        daily_returns = equity_df["equity"].pct_change().dropna()
        
        # 夏普比率
        if len(daily_returns) > 0 and daily_returns.std() > 0:
            sharpe_ratio = np.sqrt(252) * daily_returns.mean() / daily_returns.std()
        else:
            sharpe_ratio = 0
        
        # 最大回撤
        cummax = equity_df["equity"].cummax()
        drawdown = (equity_df["equity"] - cummax) / cummax
        max_drawdown = abs(drawdown.min())
        
        # 年化收益
        days = (equity_df.index[-1] - equity_df.index[0]).days
        annual_return = (1 + total_return) ** (365 / max(days, 1)) - 1 if days > 0 else 0
        
        # 胜率
        win_trades = sum(1 for t in self.trades if t.direction == "sell" and t.price > 0)
        total_sell_trades = sum(1 for t in self.trades if t.direction == "sell")
        win_rate = win_trades / total_sell_trades if total_sell_trades > 0 else 0
        
        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "total_trades": len(self.trades),
            "final_equity": equity_df["equity"].iloc[-1],
            "equity_curve": equity_df.to_dict(),
        }


# 便捷函数
def create_event_backtester(**kwargs) -> EventDrivenBacktester:
    """创建事件驱动回测器"""
    return EventDrivenBacktester(**kwargs)

