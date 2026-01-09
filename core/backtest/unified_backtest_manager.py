# -*- coding: utf-8 -*-
"""
统一回测管理器
==============
三层回测架构：
1. 快速验证层 (Fast) - 向量化回测，<5秒，用于策略初筛
2. 标准回测层 (Standard) - 事件驱动，<30秒，用于策略优化
3. 精确回测层 (Precise) - BulletTrade/QMT，完整模拟，用于最终验证

支持特性：
- 多周期：分钟/小时/日/周
- 多频率：tick/1min/5min/15min/30min/60min/daily
- 策略生成到回测全流程
- 结果对比与报告生成
"""

import logging
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def _jqdata_price_worker(args: Dict[str, Any]) -> pd.DataFrame:
    """子进程：拉取一组股票的价格数据（JQData）。

    注意：必须是模块级函数，才能被 ProcessPoolExecutor pickle。
    """
    codes = args["codes"]
    start_date = args["start_date"]
    end_date = args["end_date"]
    frequency = args["frequency"]
    fields = args["fields"]

    import jqdatasdk as jq
    from config.config_manager import get_config_manager

    cm = get_config_manager()
    jq_cfg = cm.get_config("jqdata")
    jq.auth(jq_cfg.get("username"), jq_cfg.get("password"))

    df = jq.get_price(
        codes,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        fields=fields,
        panel=False,
        fq="post",
        skip_paused=True,
    )
    return df if df is not None else pd.DataFrame()


# ==================== 枚举定义 ====================

class BacktestLevel(Enum):
    """回测层级"""
    FAST = "fast"           # 快速验证层
    STANDARD = "standard"   # 标准回测层
    PRECISE = "precise"     # 精确回测层


class DataFrequency(Enum):
    """数据频率"""
    TICK = "tick"
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    MIN_60 = "60min"
    DAILY = "daily"
    WEEKLY = "weekly"


class BacktestEngine(Enum):
    """回测引擎类型"""
    VECTORIZED = "vectorized"   # 向量化引擎
    EVENT = "event"             # 事件驱动引擎
    BULLETTRADE = "bullettrade" # BulletTrade引擎
    QMT = "qmt"                 # QMT引擎


# ==================== 配置类 ====================

@dataclass
class UnifiedBacktestConfig:
    """统一回测配置"""
    # 基础配置
    start_date: str
    end_date: str
    # 评估窗口（允许加载更长历史用于warmup，但只统计eval区间）
    eval_start_date: Optional[str] = None
    eval_end_date: Optional[str] = None
    securities: List[str] = field(default_factory=list)
    initial_capital: float = 1000000.0
    benchmark: str = "000300.XSHG"
    
    # 频率配置
    frequency: DataFrequency = DataFrequency.DAILY
    
    # 交易成本
    commission_rate: float = 0.0003   # 佣金
    stamp_tax: float = 0.001          # 印花税
    slippage: float = 0.001           # 滑点
    
    # 仓位管理
    max_positions: int = 10
    single_position_limit: float = 0.2  # 单一持仓上限
    
    # 引擎配置
    engine: BacktestEngine = BacktestEngine.VECTORIZED
    level: BacktestLevel = BacktestLevel.FAST

    # 并发配置（主要用于 JQData 批量拉取加速；JoinQuant研究环境通常允许3连接）
    parallel_workers: int = 1
    
    # 输出配置
    output_dir: str = "output/backtest"
    generate_report: bool = True
    
    # 数据源配置
    use_mock: bool = True
    data_source: str = "auto"  # auto/jqdata/akshare/mock


@dataclass
class UnifiedBacktestResult:
    """统一回测结果"""
    success: bool = False
    error: Optional[str] = None
    
    # 基础指标
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    calmar_ratio: float = 0.0
    sortino_ratio: float = 0.0
    
    # 交易统计
    win_rate: float = 0.0
    total_trades: int = 0
    profit_factor: float = 0.0
    
    # 时间序列
    equity_curve: Optional[pd.Series] = None
    daily_returns: Optional[pd.Series] = None
    drawdown_curve: Optional[pd.Series] = None
    
    # 交易记录
    trades: Optional[pd.DataFrame] = None
    
    # 元数据
    duration_seconds: float = 0.0
    engine_used: str = ""
    level_used: str = ""
    config: Optional[UnifiedBacktestConfig] = None
    
    def to_dict(self) -> Dict:
        """转为字典"""
        return {
            "success": self.success,
            "error": self.error,
            "total_return": round(self.total_return * 100, 2),
            "annual_return": round(self.annual_return * 100, 2),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "win_rate": round(self.win_rate * 100, 2),
            "total_trades": self.total_trades,
            "duration_seconds": round(self.duration_seconds, 2),
            "engine": self.engine_used,
            "level": self.level_used,
        }
    
    def summary(self) -> str:
        """生成摘要"""
        if not self.success:
            return f"回测失败: {self.error}"
        
        return f"""
📊 回测结果摘要
{'='*40}
收益率: {self.total_return*100:.2f}%
年化收益: {self.annual_return*100:.2f}%
夏普比率: {self.sharpe_ratio:.2f}
最大回撤: {self.max_drawdown*100:.2f}%
卡尔玛比率: {self.calmar_ratio:.2f}
胜率: {self.win_rate*100:.1f}%
交易次数: {self.total_trades}
{'='*40}
引擎: {self.engine_used}
层级: {self.level_used}
耗时: {self.duration_seconds:.2f}秒
"""


# ==================== 策略接口 ====================

class BaseStrategy:
    """策略基类"""
    
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or {}
        self.name = self.__class__.__name__
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号
        
        Args:
            data: 价格数据，columns为股票代码，index为日期
            
        Returns:
            信号矩阵，1=买入，-1=卖出，0=持有
        """
        raise NotImplementedError
    
    def generate_weights(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        生成持仓权重
        
        Args:
            data: 价格数据
            
        Returns:
            权重矩阵，每行权重之和应为1
        """
        signals = self.generate_signals(data)
        # 等权重分配
        weights = signals.copy()
        weights[weights > 0] = 1
        weights[weights < 0] = 0
        row_sums = weights.sum(axis=1).replace(0, 1)
        return weights.div(row_sums, axis=0)
    
    def on_bar(self, date: datetime, data: Dict, positions: Dict, cash: float) -> List[Dict]:
        """
        事件驱动接口 - 处理K线
        
        Args:
            date: 当前日期
            data: 当日行情数据
            positions: 当前持仓
            cash: 可用资金
            
        Returns:
            订单列表 [{"symbol": str, "side": "buy"/"sell", "quantity": int, "price": float}]
        """
        return []


class MomentumStrategy(BaseStrategy):
    """动量策略"""
    
    def __init__(self, params: Dict = None):
        super().__init__(params)
        self.lookback = self.params.get("lookback", 20)
        self.top_n = self.params.get("top_n", 10)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成动量信号"""
        # 计算动量
        momentum = data.pct_change(self.lookback)
        
        # 信号矩阵
        signals = pd.DataFrame(0, index=data.index, columns=data.columns)
        
        for date in data.index[self.lookback:]:
            mom_values = momentum.loc[date].dropna()
            if len(mom_values) >= self.top_n:
                top_stocks = mom_values.nlargest(self.top_n).index
                signals.loc[date, top_stocks] = 1
        
        return signals


class MeanReversionStrategy(BaseStrategy):
    """均值回归策略"""
    
    def __init__(self, params: Dict = None):
        super().__init__(params)
        self.lookback = self.params.get("lookback", 20)
        self.std_threshold = self.params.get("std_threshold", 2.0)
        self.top_n = self.params.get("top_n", 10)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成均值回归信号"""
        # 计算Z分数
        rolling_mean = data.rolling(self.lookback).mean()
        rolling_std = data.rolling(self.lookback).std()
        z_score = (data - rolling_mean) / rolling_std
        
        signals = pd.DataFrame(0, index=data.index, columns=data.columns)
        
        for date in data.index[self.lookback:]:
            z_values = z_score.loc[date].dropna()
            # 买入超跌股票
            oversold = z_values[z_values < -self.std_threshold]
            if len(oversold) > 0:
                top_oversold = oversold.nsmallest(min(len(oversold), self.top_n)).index
                signals.loc[date, top_oversold] = 1
        
        return signals


# ==================== 统一回测管理器 ====================

class UnifiedBacktestManager:
    """统一回测管理器"""
    
    def __init__(self, config: UnifiedBacktestConfig = None):
        self.config = config or UnifiedBacktestConfig(
            start_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # 引擎实例缓存
        self._fast_engine = None
        self._event_engine = None
        self._bt_engine = None
        self._qmt_engine = None
        
        # 数据缓存
        self._price_data = None
        self._data_provider = None
        
        # 进度回调
        self._progress_callback = None
    
    def set_progress_callback(self, callback: Callable[[float, str], None]):
        """设置进度回调"""
        self._progress_callback = callback
    
    def _report_progress(self, progress: float, message: str):
        """报告进度"""
        if self._progress_callback:
            self._progress_callback(progress, message)
        logger.info(f"[{progress*100:.0f}%] {message}")
    
    # ==================== 数据加载 ====================
    
    def load_data(self, securities: List[str] = None) -> bool:
        """加载数据"""
        self._report_progress(0.1, "加载数据...")
        
        securities = securities or self.config.securities
        if not securities:
            logger.error("没有指定股票列表")
            return False
        
        try:
            # phase4-fastdata: 优先使用 FastDataLoader（close矩阵 + 增量更新 + 本地索引）
            if (not self.config.use_mock) and str(self.config.data_source).lower() == "jqdata":
                try:
                    from core.data.fast_data_loader import FastDataLoader, FastDataLoaderConfig

                    loader = FastDataLoader(
                        FastDataLoaderConfig(max_workers=int(getattr(self.config, "parallel_workers", 3)))
                    )
                    px = loader.get_close_matrix(
                        securities=securities,
                        start_date=self.config.start_date,
                        end_date=self.config.end_date,
                        frequency=self.config.frequency.value if hasattr(self.config.frequency, "value") else "daily",
                        parallel_workers=int(getattr(self.config, "parallel_workers", 3)),
                        use_cache=True,
                    )
                    if px is not None and not px.empty:
                        self._price_data = px
                        self._report_progress(
                            0.2,
                            f"FastDataLoader命中: {len(self._price_data)}天 x {len(self._price_data.columns)}股票",
                        )
                        return True
                except Exception as e:
                    logger.debug(f"FastDataLoader不可用/失败，回退UnifiedDataProviderV2: {e}")

            # 注意：core.data 默认会初始化 AKShare（会触发第三方依赖 warning 且拖慢初始化）
            # 回测默认优先“聚宽研究环境”，因此这里按需启用数据源，避免无谓依赖与开销。
            from core.data.unified_data_provider_v2 import (
                UnifiedDataProviderV2,
                DataRequest,
                DataSource,
            )

            enable_akshare = str(self.config.data_source).lower() == "akshare"
            enable_jqdata = str(self.config.data_source).lower() in ("auto", "jqdata", "cache")

            if self._data_provider is None:
                self._data_provider = UnifiedDataProviderV2(
                    use_mock=self.config.use_mock,
                    enable_jqdata=enable_jqdata,
                    enable_akshare=enable_akshare,
                )

            preferred = None
            if str(self.config.data_source).lower() == "jqdata":
                preferred = DataSource.JQDATA
            elif str(self.config.data_source).lower() == "akshare":
                preferred = DataSource.AKSHARE
            elif str(self.config.data_source).lower() == "mock":
                preferred = DataSource.MOCK

            freq = self.config.frequency.value if hasattr(self.config.frequency, "value") else "daily"

            # Fast/Standard层：默认只需要 close，减少数据量，加速加载
            # Phase4.2: 大股票池时启用 3 并发连接并行拉取（避免单次超大请求过慢/超时）
            use_parallel = (
                (not self.config.use_mock)
                and (str(self.config.data_source).lower() in ("jqdata", "auto", "cache"))
                and int(getattr(self.config, "parallel_workers", 1)) > 1
                and len(securities) >= 600
            )

            if use_parallel:
                data = self._load_data_parallel_jqdata(
                    securities=securities,
                    start_date=self.config.start_date,
                    end_date=self.config.end_date,
                    frequency=freq,
                    fields=["close"],
                    max_workers=int(self.config.parallel_workers),
                )
                if data is None or data.empty:
                    logger.error("并行数据加载失败: 返回为空")
                    return False
                response_data = data
            else:
                request = DataRequest(
                    securities=securities,
                    start_date=self.config.start_date,
                    end_date=self.config.end_date,
                    frequency=freq,
                    fields=["close"],
                    use_mock=self.config.use_mock,
                    preferred_source=preferred,
                )
                response = self._data_provider.get_data(request)
                if not response.success or response.data is None:
                    logger.error(f"数据加载失败: {response.error}")
                    return False
                response_data = response.data
            
            # 转换为pivot格式
            data = response_data
            if "time" in data.columns and "code" in data.columns:
                self._price_data = data.pivot(index="time", columns="code", values="close")
            elif "date" in data.columns and "code" in data.columns:
                self._price_data = data.pivot(index="date", columns="code", values="close")
            else:
                self._price_data = data
            
            self._report_progress(0.2, f"数据加载完成: {len(self._price_data)}天 x {len(self._price_data.columns)}股票")
            return True
            
        except Exception as e:
            logger.error(f"数据加载异常: {e}")
            return False

    @staticmethod
    def _load_data_parallel_jqdata(
        securities: List[str],
        start_date: str,
        end_date: str,
        frequency: str,
        fields: List[str],
        max_workers: int = 3,
    ) -> Optional[pd.DataFrame]:
        """并行拉取 JQData 数据（用于大股票池的批量加速）。

        Notes:
            - 每个子进程会各自执行一次 jq.auth（等价于占用一个“连接”）
            - 为了避免跨进程缓存竞争，这里直接调用 jqdatasdk，不走 UnifiedDataProviderV2 的磁盘缓存
        """
        from concurrent.futures import ProcessPoolExecutor, as_completed

        if not securities:
            return None

        max_workers = max(1, min(int(max_workers), 8))

        # 均匀切分
        chunks: List[List[str]] = []
        n = len(securities)
        step = max(1, int(np.ceil(n / max_workers)))
        for i in range(0, n, step):
            chunks.append(securities[i:i + step])

        results: List[pd.DataFrame] = []
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futs = [
                ex.submit(
                    _jqdata_price_worker,
                    {
                        "codes": ch,
                        "start_date": start_date,
                        "end_date": end_date,
                        "frequency": frequency,
                        "fields": fields,
                    },
                )
                for ch in chunks
            ]
            for fut in as_completed(futs):
                df = fut.result()
                if df is not None and not df.empty:
                    results.append(df)

        if not results:
            return None
        return pd.concat(results, ignore_index=True)
    
    # ==================== 三层回测 ====================
    
    def run_fast(self, strategy: BaseStrategy) -> UnifiedBacktestResult:
        """
        快速验证层回测
        
        目标：<5秒完成
        特点：向量化计算，无滑点/费用模拟
        """
        start_time = time.time()
        self._report_progress(0.3, "运行快速回测...")
        
        result = UnifiedBacktestResult(
            engine_used="vectorized",
            level_used="fast",
            config=self.config
        )
        
        try:
            if self._price_data is None:
                if not self.load_data():
                    result.error = "数据加载失败"
                    return result
            
            # 生成信号
            self._report_progress(0.4, "生成交易信号...")
            weights = strategy.generate_weights(self._price_data)
            
            # 计算收益
            self._report_progress(0.6, "计算收益...")
            # 显式关闭默认fill_method（避免FutureWarning；策略应自己处理缺失值）
            returns = self._price_data.pct_change(fill_method=None)
            
            # 向量化计算组合收益
            portfolio_returns = (weights.shift(1) * returns).sum(axis=1)
            
            # 简化的交易成本
            turnover = weights.diff().abs().sum(axis=1) / 2
            cost = turnover * self.config.commission_rate
            portfolio_returns = portfolio_returns - cost
            
            portfolio_returns = portfolio_returns.dropna()

            # 仅统计评估窗口（避免 warmup 数据污染指标）
            eval_start = self.config.eval_start_date or self.config.start_date
            eval_end = self.config.eval_end_date or self.config.end_date
            try:
                portfolio_returns = portfolio_returns.loc[eval_start:eval_end]
            except Exception:
                # 如果索引不是DatetimeIndex/不可切片，保持原样
                pass
            
            if len(portfolio_returns) == 0:
                result.error = "收益计算为空"
                return result
            
            # 计算指标
            self._report_progress(0.8, "计算绩效指标...")
            result = self._calculate_metrics(portfolio_returns, result)

            # Fast层：给出一个“近似交易次数”，用于快速验证是否发生调仓
            try:
                changes = weights.diff().abs()
                # 每个(日期, 股票)的权重变化视为一次交易侧事件（买/卖），除以2近似得到回合数
                approx_events = int((changes > 1e-12).sum().sum())
                result.total_trades = int(approx_events / 2)
            except Exception:
                result.total_trades = 0
            result.success = True
            result.duration_seconds = time.time() - start_time
            
            self._report_progress(1.0, f"快速回测完成，耗时{result.duration_seconds:.2f}秒")
            
        except Exception as e:
            logger.exception("快速回测异常")
            result.error = str(e)
            result.duration_seconds = time.time() - start_time
        
        return result
    
    def run_standard(self, strategy: BaseStrategy) -> UnifiedBacktestResult:
        """
        标准回测层
        
        目标：<30秒完成
        特点：事件驱动，完整交易成本模拟
        """
        start_time = time.time()
        self._report_progress(0.3, "运行标准回测...")
        
        result = UnifiedBacktestResult(
            engine_used="event",
            level_used="standard",
            config=self.config
        )
        
        try:
            if self._price_data is None:
                if not self.load_data():
                    result.error = "数据加载失败"
                    return result
            
            # 事件驱动回测
            cash = self.config.initial_capital
            positions = {}  # {symbol: {"shares": int, "cost": float}}
            equity_curve = []
            trades = []
            
            self._report_progress(0.4, "开始事件驱动模拟...")
            
            dates = self._price_data.index
            total_days = len(dates)
            
            for i, date in enumerate(dates):
                # 报告进度
                if i % max(1, total_days // 10) == 0:
                    self._report_progress(0.4 + 0.4 * i / total_days, f"模拟第{i+1}/{total_days}天")
                
                # 获取当日数据
                day_data = self._price_data.loc[date].to_dict()
                
                # 策略生成订单
                orders = strategy.on_bar(date, day_data, positions, cash)
                
                # 执行订单
                for order in orders:
                    symbol = order["symbol"]
                    side = order["side"]
                    price = day_data.get(symbol, 0)
                    
                    if price <= 0:
                        continue
                    
                    if side == "buy":
                        # 计算可买数量
                        max_value = min(
                            cash * 0.95,  # 留5%余量
                            self.config.initial_capital * self.config.single_position_limit
                        )
                        shares = int(max_value / price / 100) * 100  # 整百股
                        
                        if shares > 0:
                            cost = shares * price * (1 + self.config.commission_rate + self.config.slippage)
                            if cost <= cash:
                                cash -= cost
                                if symbol in positions:
                                    positions[symbol]["shares"] += shares
                                    positions[symbol]["cost"] += cost
                                else:
                                    positions[symbol] = {"shares": shares, "cost": cost}
                                trades.append({
                                    "date": date, "symbol": symbol, "side": "buy",
                                    "shares": shares, "price": price, "cost": cost
                                })
                    
                    elif side == "sell" and symbol in positions:
                        shares = positions[symbol]["shares"]
                        proceeds = shares * price * (1 - self.config.commission_rate - self.config.stamp_tax - self.config.slippage)
                        cash += proceeds
                        trades.append({
                            "date": date, "symbol": symbol, "side": "sell",
                            "shares": shares, "price": price, "proceeds": proceeds
                        })
                        del positions[symbol]
                
                # 计算当日权益
                position_value = sum(
                    pos["shares"] * day_data.get(sym, 0)
                    for sym, pos in positions.items()
                )
                equity = cash + position_value
                equity_curve.append({"date": date, "equity": equity})
            
            # 计算结果
            self._report_progress(0.9, "计算绩效指标...")
            
            equity_df = pd.DataFrame(equity_curve).set_index("date")
            daily_returns = equity_df["equity"].pct_change().dropna()
            
            result = self._calculate_metrics(daily_returns, result)
            result.success = True
            result.total_trades = len(trades)
            result.trades = pd.DataFrame(trades) if trades else None
            result.equity_curve = equity_df["equity"]
            result.duration_seconds = time.time() - start_time
            
            self._report_progress(1.0, f"标准回测完成，耗时{result.duration_seconds:.2f}秒")
            
        except Exception as e:
            logger.exception("标准回测异常")
            result.error = str(e)
            result.duration_seconds = time.time() - start_time
        
        return result
    
    def run_precise(self, strategy_code: str, engine: str = "bullettrade") -> UnifiedBacktestResult:
        """
        精确回测层
        
        目标：完整模拟
        特点：使用BulletTrade或QMT引擎
        """
        start_time = time.time()
        self._report_progress(0.3, f"运行精确回测 ({engine})...")
        
        result = UnifiedBacktestResult(
            engine_used=engine,
            level_used="precise",
            config=self.config
        )
        
        try:
            if engine == "bullettrade":
                result = self._run_bullettrade(strategy_code, result)
            elif engine == "qmt":
                result = self._run_qmt(strategy_code, result)
            else:
                result.error = f"未知引擎: {engine}"
            
            result.duration_seconds = time.time() - start_time
            
        except Exception as e:
            logger.exception(f"{engine}回测异常")
            result.error = str(e)
            result.duration_seconds = time.time() - start_time
        
        return result
    
    def _run_bullettrade(self, strategy_code: str, result: UnifiedBacktestResult) -> UnifiedBacktestResult:
        """运行BulletTrade回测"""
        try:
            # 确保使用 extension/venv 中的 BulletTrade
            import sys
            from pathlib import Path
            
            extension_venv = Path(__file__).parent.parent.parent / "extension" / "venv" / "lib" / "python3.12" / "site-packages"
            if extension_venv.exists() and str(extension_venv) not in sys.path:
                sys.path.insert(0, str(extension_venv))
            
            from core.bullettrade import BulletTradeEngine, BTConfig
            
            # BulletTrade 使用 'day' 或 'minute'，不是 '1d'
            freq_map = {
                DataFrequency.DAILY: "day",
                DataFrequency.WEEKLY: "day",  # 周线也用 day
                DataFrequency.MIN_1: "minute",
                DataFrequency.MIN_5: "minute",
                DataFrequency.MIN_15: "minute",
                DataFrequency.MIN_30: "minute",
                DataFrequency.MIN_60: "minute",
            }
            bt_frequency = freq_map.get(self.config.frequency, "day")
            
            bt_config = BTConfig(
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                initial_capital=self.config.initial_capital,
                benchmark=self.config.benchmark,
                frequency=bt_frequency,
                # 关键：快速验证默认不生成HTML/CSV，避免报告链路拖慢 & 触发外部依赖警告
                generate_html=bool(self.config.generate_report),
                generate_csv=bool(self.config.generate_report),
                output_dir=self.config.output_dir,
                extras={"stock_pool": self.config.securities} if self.config.securities else None,
            )
            
            engine = BulletTradeEngine(bt_config)
            bt_result = engine.run_backtest(strategy_code=strategy_code)
            
            # BTResult 没有 success 属性，使用 is_profitable 或其他指标判断
            result.success = True  # BulletTrade 执行成功即认为成功
            result.total_return = bt_result.total_return / 100 if bt_result.total_return else 0
            result.annual_return = bt_result.annual_return / 100 if bt_result.annual_return else 0
            result.sharpe_ratio = bt_result.sharpe_ratio or 0
            result.max_drawdown = bt_result.max_drawdown / 100 if bt_result.max_drawdown else 0
            result.win_rate = bt_result.win_rate / 100 if bt_result.win_rate else 0
            result.total_trades = bt_result.total_trades or 0
            
        except ImportError as e:
            result.error = f"BulletTrade未安装（应在 extension/venv 中）: {e}"
            result.success = False
        except Exception as e:
            result.error = f"BulletTrade回测失败: {e}"
            result.success = False
        
        return result
    
    def _run_qmt(self, strategy_code: str, result: UnifiedBacktestResult) -> UnifiedBacktestResult:
        """运行QMT回测"""
        try:
            from core.qmt import QMTEngine, QMTConfig
            
            qmt_config = QMTConfig(
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                initial_capital=self.config.initial_capital,
                benchmark=self.config.benchmark,
                stock_pool=self.config.securities,
            )
            
            engine = QMTEngine(qmt_config)
            qmt_result = engine.run_backtest(strategy_code=strategy_code)
            
            result.success = qmt_result.success
            result.total_return = qmt_result.total_return
            result.annual_return = qmt_result.annual_return
            result.sharpe_ratio = qmt_result.sharpe_ratio
            result.max_drawdown = qmt_result.max_drawdown
            result.win_rate = qmt_result.win_rate
            result.total_trades = qmt_result.total_trades
            
        except ImportError as e:
            result.error = f"QMT/xtquant未安装: {e}"
        except Exception as e:
            result.error = f"QMT回测失败: {e}"
        
        return result
    
    def _convert_frequency(self, freq: DataFrequency) -> str:
        """转换频率格式"""
        mapping = {
            DataFrequency.TICK: "tick",
            DataFrequency.MIN_1: "1m",
            DataFrequency.MIN_5: "5m",
            DataFrequency.MIN_15: "15m",
            DataFrequency.MIN_30: "30m",
            DataFrequency.MIN_60: "60m",
            DataFrequency.DAILY: "1d",
            DataFrequency.WEEKLY: "1w",
        }
        return mapping.get(freq, "1d")
    
    def _calculate_metrics(self, returns: pd.Series, result: UnifiedBacktestResult) -> UnifiedBacktestResult:
        """计算绩效指标"""
        if len(returns) == 0:
            return result
        
        # 累计收益
        cumulative = (1 + returns).cumprod()
        result.total_return = float(cumulative.iloc[-1] - 1)
        
        # 年化收益
        days = len(returns)
        result.annual_return = float((1 + result.total_return) ** (252 / max(days, 1)) - 1)
        
        # 夏普比率
        std = returns.std()
        if std > 0:
            result.sharpe_ratio = float(returns.mean() / std * np.sqrt(252))
        
        # 最大回撤
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        result.max_drawdown = float(drawdown.min())
        result.drawdown_curve = drawdown
        
        # 卡尔玛比率
        if result.max_drawdown < 0:
            result.calmar_ratio = float(result.annual_return / abs(result.max_drawdown))
        
        # 索提诺比率
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std()
            if downside_std > 0:
                result.sortino_ratio = float(returns.mean() / downside_std * np.sqrt(252))
        
        # 胜率
        result.win_rate = float((returns > 0).sum() / max(len(returns), 1))
        
        # 盈亏比
        gains = returns[returns > 0]
        losses = returns[returns < 0]
        if len(losses) > 0 and losses.mean() != 0:
            result.profit_factor = float(gains.sum() / abs(losses.sum())) if len(gains) > 0 else 0
        
        result.daily_returns = returns
        result.equity_curve = cumulative
        
        return result
    
    # ==================== 策略生成到回测流程 ====================
    
    def run_full_pipeline(
        self,
        strategy_type: str = "momentum",
        strategy_params: Dict = None,
        levels: List[BacktestLevel] = None
    ) -> Dict[str, UnifiedBacktestResult]:
        """
        运行完整的策略生成到回测流程
        
        Args:
            strategy_type: 策略类型 (momentum/mean_reversion/custom)
            strategy_params: 策略参数
            levels: 要运行的回测层级列表
            
        Returns:
            各层级回测结果
        """
        levels = levels or [BacktestLevel.FAST]
        strategy_params = strategy_params or {}
        
        # 创建策略
        if strategy_type == "momentum":
            strategy = MomentumStrategy(strategy_params)
        elif strategy_type == "mean_reversion":
            strategy = MeanReversionStrategy(strategy_params)
        else:
            raise ValueError(f"未知策略类型: {strategy_type}")
        
        results = {}
        
        # 加载数据
        if not self.load_data():
            return {"error": UnifiedBacktestResult(error="数据加载失败")}
        
        # 运行各层级回测
        for level in levels:
            logger.info(f"\n{'='*50}")
            logger.info(f"运行 {level.value} 层级回测")
            logger.info(f"{'='*50}")
            
            if level == BacktestLevel.FAST:
                results[level.value] = self.run_fast(strategy)
            elif level == BacktestLevel.STANDARD:
                results[level.value] = self.run_standard(strategy)
            elif level == BacktestLevel.PRECISE:
                # 精确回测需要策略代码
                strategy_code = self._generate_strategy_code(strategy_type, strategy_params)
                results[level.value] = self.run_precise(strategy_code)
        
        return results
    
    def _generate_strategy_code(self, strategy_type: str, params: Dict) -> str:
        """生成策略代码（BulletTrade API）"""
        if strategy_type == "momentum":
            return f'''
# 动量策略 - BulletTrade API
def initialize(context):
    context.lookback = {params.get("lookback", 20)}
    context.top_n = {params.get("top_n", 10)}
    context.stocks = {self.config.securities[:20]}

def handle_data(context, data):
    # 计算动量
    momentum = {{}}
    for stock in context.stocks:
        prices = data.history(stock, 'close', context.lookback + 1, '1d')
        if len(prices) > 0:
            momentum[stock] = prices[-1] / prices[0] - 1
    
    # 选择动量最大的股票
    sorted_stocks = sorted(momentum.items(), key=lambda x: x[1], reverse=True)
    selected = [s[0] for s in sorted_stocks[:context.top_n]]
    
    # 调仓 - 使用 order_target_value (BulletTrade API)
    total_value = context.portfolio.total_value
    weight = 1.0 / len(selected) if selected else 0
    
    # 清仓不在选择列表中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected:
            order_target_value(stock, 0)
    
    # 买入选中的股票
    for stock in selected:
        target_value = total_value * weight
        order_target_value(stock, target_value)
'''
        else:
            return "# 默认策略\ndef initialize(context): pass\ndef handle_data(context, data): pass"
    
    # ==================== 结果对比 ====================
    
    def compare_results(self, results: Dict[str, UnifiedBacktestResult]) -> pd.DataFrame:
        """对比各层级回测结果"""
        comparison = []
        
        for level, result in results.items():
            if isinstance(result, UnifiedBacktestResult):
                comparison.append({
                    "层级": level,
                    "总收益%": round(result.total_return * 100, 2),
                    "年化收益%": round(result.annual_return * 100, 2),
                    "夏普比率": round(result.sharpe_ratio, 2),
                    "最大回撤%": round(result.max_drawdown * 100, 2),
                    "胜率%": round(result.win_rate * 100, 1),
                    "交易次数": result.total_trades,
                    "耗时(秒)": round(result.duration_seconds, 2),
                })
        
        return pd.DataFrame(comparison)


# ==================== 便捷函数 ====================

def quick_backtest(
    securities: List[str],
    start_date: str,
    end_date: str,
    strategy: str = "momentum",
    level: str = "fast",
    **kwargs
) -> UnifiedBacktestResult:
    """
    快速回测入口
    
    Args:
        securities: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        strategy: 策略类型
        level: 回测层级
        **kwargs: 其他参数
        
    Returns:
        回测结果
    """
    config = UnifiedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        securities=securities,
        use_mock=kwargs.get("use_mock", True),
        initial_capital=kwargs.get("initial_capital", 1000000),
    )
    
    manager = UnifiedBacktestManager(config)
    
    results = manager.run_full_pipeline(
        strategy_type=strategy,
        strategy_params=kwargs,
        levels=[BacktestLevel(level)]
    )
    
    return results.get(level, UnifiedBacktestResult(error="回测失败"))
