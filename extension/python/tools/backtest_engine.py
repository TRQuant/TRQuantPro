#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地回测引擎
============

功能:
- 事件驱动回测
- 多股票支持
- 风控集成
- 绩效计算

遵循:
- 策略模式
- 单一职责原则
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class OrderSide(Enum):
    """订单方向"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """订单"""
    order_id: str
    symbol: str
    side: OrderSide
    quantity: int
    price: float
    timestamp: datetime
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    filled_price: float = 0.0
    commission: float = 0.0


@dataclass
class Position:
    """持仓"""
    symbol: str
    quantity: int = 0
    avg_cost: float = 0.0
    market_value: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0


@dataclass
class Portfolio:
    """投资组合"""
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    total_value: float = 0.0
    
    def update_value(self, prices: Dict[str, float]):
        """更新组合价值"""
        position_value = 0.0
        for symbol, pos in self.positions.items():
            if symbol in prices:
                pos.market_value = pos.quantity * prices[symbol]
                pos.unrealized_pnl = (prices[symbol] - pos.avg_cost) * pos.quantity
                position_value += pos.market_value
        self.total_value = self.cash + position_value


@dataclass
class BacktestConfig:
    """回测配置"""
    start_date: str
    end_date: str
    initial_capital: float = 1000000.0
    benchmark: str = "000300.XSHG"
    commission_rate: float = 0.0003
    slippage: float = 0.002
    # 风控参数
    max_position: float = 0.8
    single_stock_max: float = 0.1
    stop_loss: float = 0.08
    take_profit: float = 0.2


@dataclass
class BacktestResult:
    """回测结果"""
    # 基本信息
    start_date: str
    end_date: str
    initial_capital: float
    final_value: float
    
    # 收益指标
    total_return: float = 0.0
    annual_return: float = 0.0
    benchmark_return: float = 0.0
    alpha: float = 0.0
    beta: float = 0.0
    
    # 风险指标
    volatility: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0
    
    # 交易统计
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    
    # 时间序列
    equity_curve: List[Dict] = field(default_factory=list)
    drawdown_curve: List[Dict] = field(default_factory=list)
    trades: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital,
            'final_value': self.final_value,
            'total_return': self.total_return,
            'annual_return': self.annual_return,
            'benchmark_return': self.benchmark_return,
            'alpha': self.alpha,
            'beta': self.beta,
            'volatility': self.volatility,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio,
            'sortino_ratio': self.sortino_ratio,
            'calmar_ratio': self.calmar_ratio,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': self.win_rate,
            'profit_factor': self.profit_factor,
            'avg_win': self.avg_win,
            'avg_loss': self.avg_loss,
            'equity_curve': self.equity_curve,
            'drawdown_curve': self.drawdown_curve,
            'trades': self.trades
        }


class BacktestEngine:
    """
    本地回测引擎
    
    事件驱动架构:
    1. 数据事件 -> 策略信号 -> 订单生成 -> 订单执行 -> 持仓更新
    """
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.portfolio = Portfolio(cash=config.initial_capital)
        self.orders: List[Order] = []
        self.order_counter = 0
        self.current_date: Optional[datetime] = None
        self.current_prices: Dict[str, float] = {}
        
        # 历史数据
        self.equity_history: List[Dict] = []
        self.trade_history: List[Dict] = []
        
        # 策略回调
        self.on_bar: Optional[Callable] = None
        
    def set_strategy(self, on_bar: Callable):
        """设置策略回调函数"""
        self.on_bar = on_bar
        
    def buy(self, symbol: str, quantity: int, price: Optional[float] = None) -> Optional[Order]:
        """买入"""
        if price is None:
            price = self.current_prices.get(symbol, 0)
        if price <= 0:
            return None
            
        # 检查资金
        cost = quantity * price * (1 + self.config.commission_rate + self.config.slippage)
        if cost > self.portfolio.cash:
            return None
            
        # 检查单股仓位限制
        max_value = self.portfolio.total_value * self.config.single_stock_max
        if cost > max_value:
            quantity = int(max_value / price / 100) * 100
            if quantity <= 0:
                return None
                
        # 创建订单
        self.order_counter += 1
        order = Order(
            order_id=f"O{self.order_counter:06d}",
            symbol=symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            price=price,
            timestamp=self.current_date
        )
        
        # 执行订单
        self._execute_order(order)
        return order
        
    def sell(self, symbol: str, quantity: int, price: Optional[float] = None) -> Optional[Order]:
        """卖出"""
        if price is None:
            price = self.current_prices.get(symbol, 0)
        if price <= 0:
            return None
            
        # 检查持仓
        pos = self.portfolio.positions.get(symbol)
        if not pos or pos.quantity < quantity:
            quantity = pos.quantity if pos else 0
        if quantity <= 0:
            return None
            
        # 创建订单
        self.order_counter += 1
        order = Order(
            order_id=f"O{self.order_counter:06d}",
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=quantity,
            price=price,
            timestamp=self.current_date
        )
        
        # 执行订单
        self._execute_order(order)
        return order
        
    def _execute_order(self, order: Order):
        """执行订单"""
        # 计算成交价（考虑滑点）
        slippage_adj = self.config.slippage if order.side == OrderSide.BUY else -self.config.slippage
        filled_price = order.price * (1 + slippage_adj)
        
        # 计算手续费
        commission = order.quantity * filled_price * self.config.commission_rate
        
        if order.side == OrderSide.BUY:
            # 买入
            total_cost = order.quantity * filled_price + commission
            if total_cost > self.portfolio.cash:
                order.status = OrderStatus.REJECTED
                return
                
            self.portfolio.cash -= total_cost
            
            # 更新持仓
            if order.symbol not in self.portfolio.positions:
                self.portfolio.positions[order.symbol] = Position(symbol=order.symbol)
            pos = self.portfolio.positions[order.symbol]
            
            # 计算平均成本
            total_quantity = pos.quantity + order.quantity
            total_cost_basis = pos.avg_cost * pos.quantity + filled_price * order.quantity
            pos.avg_cost = total_cost_basis / total_quantity if total_quantity > 0 else 0
            pos.quantity = total_quantity
            
        else:
            # 卖出
            pos = self.portfolio.positions[order.symbol]
            proceeds = order.quantity * filled_price - commission
            
            # 计算已实现盈亏
            realized_pnl = (filled_price - pos.avg_cost) * order.quantity - commission
            pos.realized_pnl += realized_pnl
            
            self.portfolio.cash += proceeds
            pos.quantity -= order.quantity
            
            # 清空空仓
            if pos.quantity == 0:
                del self.portfolio.positions[order.symbol]
                
        # 更新订单状态
        order.status = OrderStatus.FILLED
        order.filled_quantity = order.quantity
        order.filled_price = filled_price
        order.commission = commission
        
        self.orders.append(order)
        
        # 记录交易
        self.trade_history.append({
            'date': self.current_date.strftime('%Y-%m-%d') if self.current_date else '',
            'symbol': order.symbol,
            'side': order.side.value,
            'quantity': order.quantity,
            'price': filled_price,
            'commission': commission
        })
        
    def _check_risk_control(self):
        """检查风控"""
        for symbol, pos in list(self.portfolio.positions.items()):
            price = self.current_prices.get(symbol, 0)
            if price <= 0:
                continue
                
            # 止损检查
            loss_pct = (price - pos.avg_cost) / pos.avg_cost if pos.avg_cost > 0 else 0
            if loss_pct < -self.config.stop_loss:
                self.sell(symbol, pos.quantity, price)
                continue
                
            # 止盈检查
            if loss_pct > self.config.take_profit:
                self.sell(symbol, pos.quantity, price)
                
    def run(self, data: Dict[str, List[Dict]]) -> BacktestResult:
        """
        运行回测
        
        Args:
            data: 股票数据，格式 {symbol: [{date, open, high, low, close, volume}, ...]}
            
        Returns:
            BacktestResult
        """
        if not self.on_bar:
            raise ValueError("策略未设置，请调用 set_strategy()")
            
        # 获取所有交易日期
        all_dates = set()
        for symbol_data in data.values():
            for bar in symbol_data:
                all_dates.add(bar['date'])
        dates = sorted(list(all_dates))
        
        # 初始化
        self.portfolio = Portfolio(cash=self.config.initial_capital)
        self.orders = []
        self.equity_history = []
        self.trade_history = []
        
        peak_value = self.config.initial_capital
        
        # 逐日回测
        for date_str in dates:
            self.current_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # 收集当日数据
            bars = {}
            for symbol, symbol_data in data.items():
                for bar in symbol_data:
                    if bar['date'] == date_str:
                        bars[symbol] = bar
                        self.current_prices[symbol] = bar['close']
                        break
                        
            if not bars:
                continue
                
            # 更新组合价值
            self.portfolio.update_value(self.current_prices)
            
            # 检查风控
            self._check_risk_control()
            
            # 调用策略
            try:
                self.on_bar(self, bars)
            except Exception as e:
                print(f"策略执行错误 {date_str}: {e}")
                
            # 再次更新价值
            self.portfolio.update_value(self.current_prices)
            
            # 记录权益
            current_value = self.portfolio.total_value
            peak_value = max(peak_value, current_value)
            drawdown = (peak_value - current_value) / peak_value if peak_value > 0 else 0
            
            self.equity_history.append({
                'date': date_str,
                'value': current_value,
                'cash': self.portfolio.cash,
                'positions_value': current_value - self.portfolio.cash,
                'drawdown': drawdown
            })
            
        # 计算结果
        return self._calculate_result()
        
    def _calculate_result(self) -> BacktestResult:
        """计算回测结果"""
        if not self.equity_history:
            return BacktestResult(
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                initial_capital=self.config.initial_capital,
                final_value=self.config.initial_capital
            )
            
        final_value = self.equity_history[-1]['value']
        total_return = (final_value - self.config.initial_capital) / self.config.initial_capital
        
        # 计算年化收益
        start = datetime.strptime(self.config.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.config.end_date, '%Y-%m-%d')
        years = (end - start).days / 365.0
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 计算最大回撤
        max_drawdown = max(e['drawdown'] for e in self.equity_history) if self.equity_history else 0
        
        # 计算波动率
        returns = []
        for i in range(1, len(self.equity_history)):
            prev = self.equity_history[i-1]['value']
            curr = self.equity_history[i]['value']
            if prev > 0:
                returns.append((curr - prev) / prev)
                
        volatility = 0.0
        if returns:
            import statistics
            volatility = statistics.stdev(returns) * (252 ** 0.5) if len(returns) > 1 else 0
            
        # 计算夏普比率
        risk_free_rate = 0.03
        sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # 交易统计
        winning_trades = sum(1 for t in self.trade_history if t['side'] == 'sell')
        # 简化计算
        win_rate = 0.5  # 需要更复杂的逻辑
        
        return BacktestResult(
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            initial_capital=self.config.initial_capital,
            final_value=final_value,
            total_return=total_return,
            annual_return=annual_return,
            volatility=volatility,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            total_trades=len(self.trade_history),
            winning_trades=winning_trades,
            win_rate=win_rate,
            equity_curve=self.equity_history,
            trades=self.trade_history
        )


class BacktestRunner:
    """
    回测运行器
    
    负责：
    - 加载数据
    - 运行回测
    - 生成报告
    """
    
    def __init__(self):
        self.data_loader = None
        
    def _auth_jqdata(self) -> bool:
        """认证JQData"""
        try:
            import jqdatasdk as jq
            
            # 从配置文件读取认证信息
            # 优先级: extension/config > 用户目录 > 项目根目录
            config_paths = [
                Path(__file__).parent.parent.parent / "config" / "jqdata_config.json",  # extension/config
                Path.home() / ".local/share/trquant/config/jqdata_config.json",
                Path.home() / ".jqdata_config.json",
                Path(__file__).parent.parent.parent.parent / "config" / "jqdata_config.json"  # TRQuant/config
            ]
            
            for config_path in config_paths:
                if config_path.exists():
                    import json
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        username = config.get('username')
                        password = config.get('password')
                        
                        if username and password:
                            jq.auth(username, password)
                            print(f"JQData认证成功 (配置: {config_path})")
                            return True
            
            print("未找到JQData配置文件，尝试检查是否已认证...")
            # 检查是否已手动认证
            try:
                test = jq.get_all_securities(types=['stock'], date=None)
                if test is not None and len(test) > 0:
                    print("JQData已认证")
                    return True
            except:
                pass
                
            return False
        except ImportError:
            print("jqdatasdk未安装，请运行: pip install jqdatasdk")
            return False
        except Exception as e:
            print(f"JQData认证失败: {e}")
            return False
    
    def load_data_from_jqdata(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, List[Dict]]:
        """从JQData加载数据"""
        try:
            import jqdatasdk as jq
            
            # 尝试认证
            if not self._auth_jqdata():
                raise Exception("JQData认证失败，请检查配置文件")
                
            data = {}
            for symbol in symbols:
                df = jq.get_price(
                    symbol, 
                    start_date=start_date, 
                    end_date=end_date,
                    frequency='daily',
                    fields=['open', 'high', 'low', 'close', 'volume']
                )
                if df is not None and not df.empty:
                    records = []
                    for idx, row in df.iterrows():
                        records.append({
                            'date': idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx),
                            'open': float(row['open']),
                            'high': float(row['high']),
                            'low': float(row['low']),
                            'close': float(row['close']),
                            'volume': int(row['volume'])
                        })
                    data[symbol] = records
                    print(f"加载 {symbol}: {len(records)} 条数据")
                            
            return data
        except Exception as e:
            print(f"JQData加载失败: {e}")
            return {}
            
    def load_data_from_akshare(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, List[Dict]]:
        """从AKShare加载数据"""
        try:
            import akshare as ak
            
            data = {}
            for symbol in symbols:
                # 转换股票代码格式
                code = symbol.split('.')[0]
                
                df = ak.stock_zh_a_hist(
                    symbol=code,
                    start_date=start_date.replace('-', ''),
                    end_date=end_date.replace('-', ''),
                    adjust="qfq"
                )
                
                if df is not None and not df.empty:
                    df = df.rename(columns={
                        '日期': 'date',
                        '开盘': 'open',
                        '最高': 'high',
                        '最低': 'low',
                        '收盘': 'close',
                        '成交量': 'volume'
                    })
                    data[symbol] = df[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict('records')
                    
            return data
        except Exception as e:
            print(f"AKShare加载失败: {e}")
            return {}
            
    def run_backtest(
        self,
        strategy_code: str,
        config: Dict[str, Any],
        data_source: str = 'akshare'
    ) -> Dict[str, Any]:
        """
        运行回测
        
        Args:
            strategy_code: 策略代码（Python）
            config: 回测配置
            data_source: 数据源 ('jqdata', 'akshare')
            
        Returns:
            回测结果字典
        """
        try:
            # 解析配置
            bt_config = BacktestConfig(
                start_date=config.get('start_date', '2023-01-01'),
                end_date=config.get('end_date', '2024-01-01'),
                initial_capital=config.get('initial_capital', 1000000),
                benchmark=config.get('benchmark', '000300.XSHG'),
                commission_rate=config.get('commission', 0.0003),
                slippage=config.get('slippage', 0.002),
                max_position=config.get('max_position', 0.8),
                single_stock_max=config.get('single_stock_max', 0.1),
                stop_loss=config.get('stop_loss', 0.08),
                take_profit=config.get('take_profit', 0.2)
            )
            
            # 获取股票池
            symbols = config.get('symbols', ['000001.XSHE'])
            
            # 加载数据
            data = None
            
            if data_source == 'jqdata':
                data = self.load_data_from_jqdata(symbols, bt_config.start_date, bt_config.end_date)
            elif data_source == 'akshare':
                data = self.load_data_from_akshare(symbols, bt_config.start_date, bt_config.end_date)
                
            if not data:
                return {
                    'success': False,
                    'error': f'无法加载数据。如使用JQData，请检查日期范围是否在账户权限内。当前请求: {bt_config.start_date} ~ {bt_config.end_date}'
                }
                
            # 创建引擎
            engine = BacktestEngine(bt_config)
            
            # 编译策略
            strategy_globals = {
                'engine': engine,
                'buy': engine.buy,
                'sell': engine.sell
            }
            
            # 执行策略定义
            exec(strategy_code, strategy_globals)
            
            # 获取on_bar函数
            if 'on_bar' not in strategy_globals:
                return {
                    'success': False,
                    'error': '策略代码必须定义 on_bar(engine, bars) 函数'
                }
                
            engine.set_strategy(strategy_globals['on_bar'])
            
            # 运行回测
            result = engine.run(data)
            
            return {
                'success': True,
                'result': result.to_dict()
            }
            
        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }


# 模块接口
def run_backtest(strategy_code: str, config: Dict[str, Any], data_source: str = 'akshare') -> Dict[str, Any]:
    """运行回测的便捷函数"""
    runner = BacktestRunner()
    return runner.run_backtest(strategy_code, config, data_source)


if __name__ == '__main__':
    # 测试
    test_strategy = '''
def on_bar(engine, bars):
    """简单均线策略"""
    for symbol, bar in bars.items():
        # 简单逻辑：收盘价高于开盘价就买入
        if bar['close'] > bar['open']:
            if symbol not in engine.portfolio.positions:
                engine.buy(symbol, 100)
        else:
            if symbol in engine.portfolio.positions:
                engine.sell(symbol, engine.portfolio.positions[symbol].quantity)
'''
    
    config = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'initial_capital': 100000,
        'symbols': ['000001.XSHE']
    }
    
    result = run_backtest(test_strategy, config)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))






