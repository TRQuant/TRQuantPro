"""聚宽 API 兼容层

实现聚宽 (JoinQuant) API 的本地兼容，使策略代码可以无缝迁移
"""

from typing import Optional, Dict, Any, List, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class SubPortfolio:
    """子账户"""
    cash: float = 0.0
    positions_value: float = 0.0
    total_value: float = 0.0
    available_cash: float = 0.0
    locked_cash: float = 0.0
    positions: Dict[str, "Position"] = field(default_factory=dict)


@dataclass
class Portfolio:
    """投资组合
    
    兼容聚宽的 portfolio 对象
    """
    cash: float = 0.0
    positions_value: float = 0.0
    total_value: float = 0.0
    available_cash: float = 0.0
    locked_cash: float = 0.0
    positions: Dict[str, "Position"] = field(default_factory=dict)
    starting_cash: float = 1000000.0
    returns: float = 0.0
    
    def __post_init__(self):
        self.total_value = self.cash + self.positions_value
        self.available_cash = self.cash - self.locked_cash


@dataclass
class Position:
    """持仓信息
    
    兼容聚宽的 position 对象
    """
    security: str = ""
    price: float = 0.0
    avg_cost: float = 0.0
    total_amount: int = 0
    closeable_amount: int = 0
    value: float = 0.0
    pnl: float = 0.0
    pnl_ratio: float = 0.0


@dataclass 
class GlobalVars:
    """全局变量容器 (g 对象)"""
    pass


class Context:
    """策略上下文
    
    兼容聚宽的 context 对象
    """
    
    def __init__(self, initial_capital: float = 1000000.0):
        """初始化上下文
        
        Args:
            initial_capital: 初始资金
        """
        self.portfolio = Portfolio(
            cash=initial_capital,
            starting_cash=initial_capital,
            total_value=initial_capital,
            available_cash=initial_capital
        )
        self.subportfolios: Dict[str, SubPortfolio] = {}
        self.current_dt: datetime = datetime.now()
        self.previous_date: Optional[datetime] = None
        self.run_params: Dict[str, Any] = {}
        
        # 全局变量
        self.g = GlobalVars()
        
        # 内部状态
        self._benchmark: str = "000300.XSHG"
        self._commission: float = 0.0003
        self._slippage: float = 0.001
        self._scheduled_funcs: List[Dict] = []
    
    def set_benchmark(self, security: str) -> None:
        """设置基准"""
        self._benchmark = security
    
    def set_commission(self, rate: float) -> None:
        """设置佣金"""
        self._commission = rate
    
    def set_slippage(self, rate: float) -> None:
        """设置滑点"""
        self._slippage = rate


class JQDataCompat:
    """聚宽 API 兼容类
    
    提供聚宽 API 的本地实现
    """
    
    def __init__(self, data_provider: Optional[Any] = None):
        """初始化
        
        Args:
            data_provider: 数据提供器
        """
        self.data_provider = data_provider
        self._context: Optional[Context] = None
        self._initialize_func: Optional[Callable] = None
        self._handle_data_func: Optional[Callable] = None
        self._before_trading_start_func: Optional[Callable] = None
        self._after_trading_end_func: Optional[Callable] = None
    
    def set_context(self, context: Context) -> None:
        """设置上下文"""
        self._context = context
    
    def get_context(self) -> Optional[Context]:
        """获取上下文"""
        return self._context


# 全局实例
_jq_compat = JQDataCompat()
_current_context: Optional[Context] = None


def get_current_context() -> Optional[Context]:
    """获取当前上下文"""
    global _current_context
    return _current_context


def set_current_context(context: Context) -> None:
    """设置当前上下文"""
    global _current_context
    _current_context = context


# ============ 聚宽 API 函数实现 ============

def set_benchmark(security: str) -> None:
    """设置回测基准
    
    Args:
        security: 基准证券代码，如 '000300.XSHG'
    """
    ctx = get_current_context()
    if ctx:
        ctx.set_benchmark(security)
    logger.debug(f"Set benchmark: {security}")


def set_commission(open_tax: float = 0, close_tax: float = 0.001,
                   open_commission: float = 0.0003, close_commission: float = 0.0003,
                   close_today_commission: float = 0, min_commission: float = 5) -> None:
    """设置手续费
    
    Args:
        open_tax: 买入印花税
        close_tax: 卖出印花税
        open_commission: 买入佣金
        close_commission: 卖出佣金
        close_today_commission: 平今佣金
        min_commission: 最低佣金
    """
    ctx = get_current_context()
    if ctx:
        ctx.set_commission(open_commission)
    logger.debug(f"Set commission: {open_commission}")


def set_slippage(rate: float = 0.001) -> None:
    """设置滑点
    
    Args:
        rate: 滑点比率
    """
    ctx = get_current_context()
    if ctx:
        ctx.set_slippage(rate)
    logger.debug(f"Set slippage: {rate}")


def order(security: str, amount: int, style: Optional[Any] = None) -> Optional[str]:
    """下单（按股数）
    
    Args:
        security: 证券代码
        amount: 买入数量（正数买入，负数卖出）
        style: 订单类型
        
    Returns:
        订单ID
    """
    ctx = get_current_context()
    if not ctx:
        return None
    
    logger.info(f"Order: {security}, amount={amount}")
    
    # 这里实现下单逻辑
    # 在回测模式下，更新持仓和资金
    # 在实盘模式下，调用券商接口
    
    return f"order_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def order_value(security: str, value: float, style: Optional[Any] = None) -> Optional[str]:
    """下单（按金额）
    
    Args:
        security: 证券代码
        value: 买入金额（正数买入，负数卖出）
        style: 订单类型
        
    Returns:
        订单ID
    """
    ctx = get_current_context()
    if not ctx:
        return None
    
    logger.info(f"Order value: {security}, value={value}")
    
    # 计算股数并下单
    # current_price = get_current_price(security)
    # amount = int(value / current_price / 100) * 100  # 整手
    
    return f"order_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def order_target(security: str, amount: int, style: Optional[Any] = None) -> Optional[str]:
    """目标下单（按目标股数）
    
    Args:
        security: 证券代码
        amount: 目标持仓数量
        style: 订单类型
        
    Returns:
        订单ID
    """
    ctx = get_current_context()
    if not ctx:
        return None
    
    # 获取当前持仓
    current_amount = 0
    if security in ctx.portfolio.positions:
        current_amount = ctx.portfolio.positions[security].total_amount
    
    # 计算差额
    delta = amount - current_amount
    
    if delta != 0:
        return order(security, delta, style)
    return None


def order_target_value(security: str, value: float, style: Optional[Any] = None) -> Optional[str]:
    """目标下单（按目标金额）
    
    Args:
        security: 证券代码
        value: 目标持仓金额
        style: 订单类型
        
    Returns:
        订单ID
    """
    ctx = get_current_context()
    if not ctx:
        return None
    
    # 获取当前持仓市值
    current_value = 0
    if security in ctx.portfolio.positions:
        current_value = ctx.portfolio.positions[security].value
    
    # 计算差额
    delta = value - current_value
    
    if abs(delta) > 100:  # 忽略小额调整
        return order_value(security, delta, style)
    return None


def get_price(security: Union[str, List[str]], 
              start_date: Optional[str] = None,
              end_date: Optional[str] = None,
              frequency: str = 'daily',
              fields: Optional[List[str]] = None,
              skip_paused: bool = False,
              fq: str = 'pre',
              count: Optional[int] = None) -> pd.DataFrame:
    """获取历史价格数据
    
    Args:
        security: 证券代码或代码列表
        start_date: 开始日期
        end_date: 结束日期
        frequency: 频率 ('daily', 'minute', 'tick')
        fields: 字段列表 ['open', 'close', 'high', 'low', 'volume']
        skip_paused: 是否跳过停牌
        fq: 复权方式 ('pre', 'post', None)
        count: 数据条数
        
    Returns:
        价格数据 DataFrame
    """
    if fields is None:
        fields = ['open', 'close', 'high', 'low', 'volume']
    
    logger.debug(f"Get price: {security}, {start_date} - {end_date}")
    
    # 这里需要调用数据提供器获取数据
    # 暂时返回空 DataFrame
    if isinstance(security, str):
        security = [security]
    
    # 生成模拟数据（开发阶段）
    if count:
        dates = pd.date_range(end=end_date or datetime.now(), periods=count, freq='D')
    else:
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = {}
    for sec in security:
        df = pd.DataFrame({
            'open': np.random.uniform(10, 100, len(dates)),
            'close': np.random.uniform(10, 100, len(dates)),
            'high': np.random.uniform(10, 100, len(dates)),
            'low': np.random.uniform(10, 100, len(dates)),
            'volume': np.random.uniform(1000000, 10000000, len(dates))
        }, index=dates)
        data[sec] = df
    
    if len(security) == 1:
        return data[security[0]][fields]
    
    return pd.concat(data, axis=1)


def history(count: int, 
            unit: str = '1d',
            field: str = 'close',
            security_list: Optional[List[str]] = None,
            df: bool = True,
            skip_paused: bool = False,
            fq: str = 'pre') -> Union[pd.DataFrame, Dict]:
    """获取历史数据
    
    Args:
        count: 数据条数
        unit: 时间单位 ('1d', '1m', '5m', etc.)
        field: 字段
        security_list: 证券列表
        df: 是否返回 DataFrame
        skip_paused: 是否跳过停牌
        fq: 复权方式
        
    Returns:
        历史数据
    """
    logger.debug(f"Get history: count={count}, unit={unit}, field={field}")
    
    # 调用 get_price 实现
    if security_list:
        return get_price(
            security_list,
            count=count,
            fields=[field]
        )
    
    return pd.DataFrame()


def attribute_history(security: str,
                      count: int,
                      unit: str = '1d',
                      fields: List[str] = ['open', 'close', 'high', 'low', 'volume'],
                      skip_paused: bool = True,
                      df: bool = True,
                      fq: str = 'pre') -> pd.DataFrame:
    """获取单个证券的历史数据
    
    Args:
        security: 证券代码
        count: 数据条数
        unit: 时间单位
        fields: 字段列表
        skip_paused: 是否跳过停牌
        df: 是否返回 DataFrame
        fq: 复权方式
        
    Returns:
        历史数据 DataFrame
    """
    return get_price(security, count=count, fields=fields)


def run_daily(func: Callable, time: str = 'every_bar') -> None:
    """设置每日运行的函数
    
    Args:
        func: 要运行的函数
        time: 运行时间 ('every_bar', 'open', 'close', 或具体时间如 '09:30')
    """
    ctx = get_current_context()
    if ctx:
        ctx._scheduled_funcs.append({
            'func': func,
            'time': time,
            'frequency': 'daily'
        })
    logger.debug(f"Scheduled daily func: {func.__name__} at {time}")


def schedule_function(func: Callable,
                      date_rule: Optional[Any] = None,
                      time_rule: Optional[Any] = None) -> None:
    """调度函数
    
    Args:
        func: 要调度的函数
        date_rule: 日期规则
        time_rule: 时间规则
    """
    ctx = get_current_context()
    if ctx:
        ctx._scheduled_funcs.append({
            'func': func,
            'date_rule': date_rule,
            'time_rule': time_rule
        })


def get_current_data() -> Dict[str, Any]:
    """获取当前数据"""
    return {}


def log_info(message: str) -> None:
    """记录信息日志"""
    logger.info(message)


def log_warning(message: str) -> None:
    """记录警告日志"""
    logger.warning(message)


def log_error(message: str) -> None:
    """记录错误日志"""
    logger.error(message)


# 证券代码转换
def normalize_code(code: str) -> str:
    """标准化证券代码
    
    将各种格式的代码转换为聚宽格式
    
    Args:
        code: 证券代码
        
    Returns:
        聚宽格式代码，如 '000001.XSHE'
    """
    code = str(code).strip()
    
    # 已经是聚宽格式
    if '.X' in code:
        return code
    
    # 去除可能的后缀
    code = code.replace('.SH', '').replace('.SZ', '')
    code = code.replace('.sh', '').replace('.sz', '')
    
    # 补齐6位
    code = code.zfill(6)
    
    # 判断交易所
    if code.startswith(('6', '5', '9')):
        return f"{code}.XSHG"  # 上海
    else:
        return f"{code}.XSHE"  # 深圳


def convert_to_local_code(jq_code: str) -> str:
    """转换聚宽代码为本地格式
    
    Args:
        jq_code: 聚宽格式代码
        
    Returns:
        本地格式代码，如 '000001.SZ'
    """
    if '.XSHG' in jq_code:
        return jq_code.replace('.XSHG', '.SH')
    elif '.XSHE' in jq_code:
        return jq_code.replace('.XSHE', '.SZ')
    return jq_code

