"""
回测引擎 - 集成三层回测架构（Fast + BulletTrade + QMT）

功能特性：
- 快速回测（Fast）：向量化计算，<5秒，用于策略初筛
- 标准回测（Standard）：事件驱动，<30秒，用于策略优化
- 精确回测（Precise）：BulletTrade/QMT，完整模拟，用于最终验证
- 支持聚宽策略代码生成和回测
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from tqdm import tqdm
import logging

from .trading_strategy import (
    TradingStrategy, TradingConfig, TradeSignal, Position, Trade,
    SignalType, ExitReason
)
from .multi_factor_calculator import MultiFactorCalculator
from .xgboost_predictor import XGBoostPredictor
from .joinquant_strategy_generator import JoinQuantStrategyGenerator

# 导入统一回测管理器
from core.backtest.unified_backtest_manager import (
    UnifiedBacktestManager,
    UnifiedBacktestConfig,
    UnifiedBacktestResult,
    BacktestLevel,
    DataFrequency,
    BaseStrategy,
)

logger = logging.getLogger(__name__)


@dataclass
class BacktestResult:
    """回测结果"""
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annualized_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_trades: int
    win_rate: float
    profit_factor: float
    avg_return: float
    hit_10pct_rate: float
    hit_5pct_rate: float
    trades: List[Trade] = field(default_factory=list)
    daily_equity: List[Dict] = field(default_factory=list)
    monthly_returns: Dict = field(default_factory=dict)


class V4StrategyAdapter(BaseStrategy):
    """V4.0策略适配器 - 将V4.0策略转换为UnifiedBacktestManager可用的策略"""
    
    def __init__(self, 
                 predictor: XGBoostPredictor,
                 trading_config: TradingConfig,
                 factor_calculator: MultiFactorCalculator,
                 jq_client,
                 stock_universe: List[str] = None,
                 fast_mode: bool = False):
        """
        Args:
            predictor: XGBoost预测模型
            trading_config: 交易配置
            factor_calculator: 因子计算器
            jq_client: JQData客户端
            stock_universe: 股票池
        """
        super().__init__()
        self.predictor = predictor
        self.trading_config = trading_config
        self.factor_calculator = factor_calculator
        self.jq = jq_client
        self.stock_universe = stock_universe or []
        self.fast_mode = fast_mode
        self.name = "V4.0多因子预测策略"
    
    def generate_weights(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成持仓权重（用于快速回测）"""
        if data is None or len(data) == 0:
            return pd.DataFrame()

        prices = data.copy()
        prices = prices.replace([np.inf, -np.inf], np.nan).ffill().bfill()

        # Fast层：仅使用价格数据的动量代理，避免JQData因子调用，确保<5秒可跑通
        if self.fast_mode:
            lookback = int(self.trading_config.max_holding_days) if self.trading_config else 5
            lookback = max(5, min(60, lookback))

            # 以自然周为调仓节奏：每个自然周的首个交易日调仓
            idx = prices.index
            if not isinstance(idx, pd.DatetimeIndex):
                idx = pd.to_datetime(idx)
            week_keys = idx.isocalendar().year.astype(str) + "-" + idx.isocalendar().week.astype(str)
            rebalance_dates = idx.to_series().groupby(week_keys).min().sort_values().tolist()

            weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

            for d in rebalance_dates:
                # 如果回测窗口很短（例如仅1周），可能没有足够历史用于 lookback 动量
                # 这里按“可用历史长度”自适应缩短 lookback，确保 Fast 层不会出现全程0交易的假象。
                if d not in prices.index:
                    continue
                pos = prices.index.get_loc(d)
                if isinstance(pos, slice):
                    # 不应发生：DatetimeIndex get_loc 返回 slice 仅在重复索引时出现
                    continue
                if pos <= 0:
                    continue

                eff_lb = min(int(lookback), int(pos))
                if eff_lb <= 0:
                    continue

                row = (prices.iloc[pos] / prices.iloc[pos - eff_lb] - 1.0)
                row = row.replace([np.inf, -np.inf], np.nan).dropna()
                if row.empty:
                    continue
                top_n = min(int(self.trading_config.max_positions), len(row)) if self.trading_config else min(10, len(row))
                row = row[row > 0]
                if row.empty:
                    continue
                picks = row.nlargest(top_n).index.tolist()
                if not picks:
                    continue
                weights.loc[d, picks] = 1.0 / len(picks)

            weights = weights.ffill().fillna(0.0)
            return weights

        # 非Fast层：保留原有逻辑（会调用JQData因子/预测器，速度更慢）
        last_date = prices.index[-1]
        date_str = last_date.strftime('%Y-%m-%d') if isinstance(last_date, pd.Timestamp) else str(last_date)
        codes = prices.columns.tolist()

        try:
            factors_df = self.factor_calculator.calculate_all_factors(codes, date_str)
        except Exception as e:
            logger.warning(f"因子计算失败: {e}")
            return pd.DataFrame(0, index=prices.index, columns=prices.columns)

        if factors_df is None or factors_df.empty:
            return pd.DataFrame(0, index=prices.index, columns=prices.columns)

        if self.predictor:
            try:
                predictions = self.predictor.predict(factors_df)
                factors_df['probability'] = [p.probability for p in predictions]
            except Exception as e:
                logger.warning(f"预测失败: {e}")
                factors_df['probability'] = 0.5
        else:
            factors_df['probability'] = 0.5

        strategy = TradingStrategy(self.trading_config)
        signals = strategy.generate_entry_signals(factors_df, date_str)

        weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        if signals:
            total_weight = sum(s.position_size for s in signals)
            if total_weight > 0:
                for signal in signals:
                    if signal.code in weights.columns:
                        weights.loc[last_date, signal.code] = signal.position_size / total_weight
        return weights


class BacktestEngine:
    """回测引擎 - 集成三层回测架构"""
    
    def __init__(self,
                 predictor: XGBoostPredictor = None,
                 trading_config: TradingConfig = None,
                 initial_capital: float = 1000000,
                 verbose: bool = True,
                 use_unified_backtest: bool = True):
        """
        Args:
            predictor: 预测模型
            trading_config: 交易配置
            initial_capital: 初始资金
            verbose: 是否打印详细信息
            use_unified_backtest: 是否使用统一回测管理器（默认True）
        """
        self.predictor = predictor
        self.trading_config = trading_config or TradingConfig()
        self.initial_capital = initial_capital
        self.verbose = verbose
        self.use_unified_backtest = use_unified_backtest
        
        self.factor_calculator = None
        self.jq = None
        self.strategy_generator = JoinQuantStrategyGenerator()
        
        self._init_jqdata()
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            self.jq = jq
            
            self.factor_calculator = MultiFactorCalculator(verbose=False)
            
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
    
    def get_trading_days(self, start_date: str, end_date: str) -> List[str]:
        """获取交易日列表"""
        days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        return [d.strftime('%Y-%m-%d') for d in days]
    
    def get_stock_universe(self, date: str) -> List[str]:
        """获取股票池"""
        stocks = self.jq.get_all_securities(types=['stock'], date=date)
        
        # 排除ST和科创板
        stocks = stocks[~stocks.index.str.startswith('688')]
        stocks = stocks[~stocks['display_name'].str.contains('ST')]
        
        return stocks.index.tolist()

    def get_fast_stock_universe(self, date: str, limit: int = 300) -> List[str]:
        """获取“快速验证层”股票池（速度优先）。

        默认使用 HS300 成分股作为小股票池，避免全市场扫描。
        """
        if self.jq is None:
            return []

        # 优先：沪深300成分股（通常无ST，质量更稳，且数量可控）
        try:
            stocks = self.jq.get_index_stocks("000300.XSHG")
            stocks = [s for s in stocks if not str(s).startswith("688")]
            return stocks[:limit]
        except Exception as e:
            logger.warning(f"get_index_stocks failed, fallback to all securities: {e}")

        # 回退：全市场（仍做过滤，但可能较慢）
        try:
            universe = self.get_stock_universe(date)
            return universe[:limit]
        except Exception:
            return []
    
    def get_daily_prices(self, codes: List[str], date: str) -> Dict[str, Dict]:
        """获取当日价格数据"""
        prices = self.jq.get_price(
            codes,
            end_date=date,
            count=1,
            frequency='daily',
            fields=['open', 'high', 'low', 'close', 'money'],
            panel=False,
            skip_paused=True,
            fq='post'
        )
        
        if prices is None or prices.empty:
            return {}
        
        result = {}
        for _, row in prices.iterrows():
            result[row['code']] = {
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'money': row['money'],
            }
        
        return result
    
    def determine_market_regime(self, date: str) -> str:
        """判断市场环境"""
        try:
            prices = self.jq.get_price(
                '000300.XSHG',
                end_date=date,
                count=20,
                frequency='daily',
                fields=['close'],
                fq='post'
            )
            
            if prices is None or len(prices) < 20:
                return "neutral"
            
            trend = (prices['close'].iloc[-1] / prices['close'].iloc[0] - 1) * 100
            
            if trend > 5:
                return "bull"
            elif trend < -5:
                return "bear"
            else:
                return "neutral"
        except:
            return "neutral"
    
    def run(self, 
            start_date: str,
            end_date: str,
            rebalance_freq: str = 'weekly',
            backtest_levels: List[str] = None) -> BacktestResult:
        """运行回测
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            rebalance_freq: 调仓频率 (daily/weekly/monthly)
            backtest_levels: 回测层级列表 ['fast', 'standard', 'precise']，默认['fast']
        
        Returns:
            BacktestResult: 回测结果（如果使用统一回测，返回Fast层结果）
        """
        backtest_levels = backtest_levels or ['fast']
        
        print(f"\n{'='*60}")
        print(f"【回测引擎】")
        print(f"回测区间: {start_date} ~ {end_date}")
        print(f"调仓频率: {rebalance_freq}")
        print(f"初始资金: {self.initial_capital:,.0f}")
        print(f"回测层级: {', '.join(backtest_levels)}")
        print(f"{'='*60}\n")
        
        # 如果使用统一回测管理器
        if self.use_unified_backtest:
            return self._run_unified_backtest(start_date, end_date, rebalance_freq, backtest_levels)
        
        # 否则使用原有逻辑（向后兼容）
        return self._run_legacy_backtest(start_date, end_date, rebalance_freq)
    
    def _run_unified_backtest(self,
                              start_date: str,
                              end_date: str,
                              rebalance_freq: str,
                              backtest_levels: List[str]) -> BacktestResult:
        """使用统一回测管理器运行回测"""
        
        # 1) 选择股票池（Fast层速度优先：HS300小池；标准/精确层也沿用，避免全市场拉取导致超慢）
        stock_universe = self.get_fast_stock_universe(start_date, limit=500)
        if not stock_universe:
            stock_universe = self.get_stock_universe(start_date)[:500]

        # 2. 创建策略适配器（Fast层优先使用fast_mode，确保快速验证可跑通）
        base_kwargs = dict(
            predictor=self.predictor,
            trading_config=self.trading_config,
            factor_calculator=self.factor_calculator,
            jq_client=self.jq,
            stock_universe=stock_universe[:500],  # 限制数量
        )
        
        # 3. 创建统一回测配置（Fast层必须走JQData真实数据口径；禁用mock；禁用AKShare初始化）
        # Fast层需要 warmup 数据（动量/周频调仓），因此向前扩展 start_date，但只统计 eval 窗口指标
        extended_start = start_date
        try:
            warmup_days = self.jq.get_trade_days(end_date=start_date, count=80)
            if warmup_days is not None and len(warmup_days) > 0:
                extended_start = str(warmup_days[0])[:10]
        except Exception:
            extended_start = start_date

        config = UnifiedBacktestConfig(
            start_date=extended_start,
            end_date=end_date,
            eval_start_date=start_date,
            eval_end_date=end_date,
            securities=stock_universe[:500],
            initial_capital=self.initial_capital,
            benchmark="000300.XSHG",
            frequency=DataFrequency.DAILY,
            commission_rate=0.0003,
            stamp_tax=0.001,
            slippage=0.001,
            max_positions=self.trading_config.max_positions,
            single_position_limit=self.trading_config.position_size,
            generate_report=False,
            use_mock=False,
            data_source="jqdata",
            parallel_workers=3,
        )
        
        # 4. 创建统一回测管理器
        manager = UnifiedBacktestManager(config)
        
        if self.verbose:
            def progress_callback(progress: float, message: str):
                print(f"[{progress*100:.0f}%] {message}")
            manager.set_progress_callback(progress_callback)
        
        results = {}
        
        # 4. 运行各层级回测
        if 'fast' in backtest_levels:
            print("\n【快速回测】")
            strategy_fast = V4StrategyAdapter(**base_kwargs, fast_mode=True)
            fast_result = manager.run_fast(strategy_fast)
            results['fast'] = fast_result
            if self.verbose:
                print(fast_result.summary())
        
        if 'standard' in backtest_levels:
            print("\n【标准回测】")
            strategy_standard = V4StrategyAdapter(**base_kwargs, fast_mode=False)
            standard_result = manager.run_standard(strategy_standard)
            results['standard'] = standard_result
            if self.verbose:
                print(standard_result.summary())
        
        if 'precise' in backtest_levels:
            print("\n【精确回测 - BulletTrade】")
            # 生成聚宽策略代码
            strategy_code = self._generate_strategy_code(start_date, end_date)
            
            # 运行BulletTrade回测
            precise_result = manager.run_precise(strategy_code, engine="bullettrade")
            results['precise'] = precise_result
            if self.verbose:
                print(precise_result.summary())
        
        # 5. 转换结果为BacktestResult格式（使用Fast层结果）
        if 'fast' in results and results['fast'].success:
            return self._convert_unified_result(results['fast'], start_date, end_date)
        elif 'standard' in results and results['standard'].success:
            return self._convert_unified_result(results['standard'], start_date, end_date)
        elif 'precise' in results and results['precise'].success:
            return self._convert_unified_result(results['precise'], start_date, end_date)
        else:
            # 返回失败结果
            return BacktestResult(
                start_date=start_date,
                end_date=end_date,
                initial_capital=self.initial_capital,
                final_capital=self.initial_capital,
                total_return=0.0,
                annualized_return=0.0,
                max_drawdown=0.0,
                sharpe_ratio=0.0,
                total_trades=0,
                win_rate=0.0,
                profit_factor=0.0,
                avg_return=0.0,
                hit_10pct_rate=0.0,
                hit_5pct_rate=0.0,
            )
    
    def _generate_strategy_code(self, start_date: str, end_date: str) -> str:
        """生成聚宽策略代码"""
        # TODO: 从workflow获取信号并生成代码
        # 目前先返回基础模板
        return self.strategy_generator.generate_strategy_code(
            strategy_name="V4.0多因子预测策略",
            v4_config={},
            trading_config=self.trading_config,
            signals_by_date={}
        )
    
    def _convert_unified_result(self, 
                                unified_result: UnifiedBacktestResult,
                                start_date: str,
                                end_date: str) -> BacktestResult:
        """将UnifiedBacktestResult转换为BacktestResult"""
        return BacktestResult(
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.initial_capital,
            final_capital=self.initial_capital * (1 + unified_result.total_return),
            total_return=unified_result.total_return,
            annualized_return=unified_result.annual_return,
            max_drawdown=unified_result.max_drawdown,
            sharpe_ratio=unified_result.sharpe_ratio,
            total_trades=unified_result.total_trades,
            win_rate=unified_result.win_rate,
            profit_factor=unified_result.profit_factor,
            avg_return=unified_result.total_return / max(unified_result.total_trades, 1),
            hit_10pct_rate=0.0,  # TODO: 从trades计算
            hit_5pct_rate=0.0,   # TODO: 从trades计算
        )
    
    def _run_legacy_backtest(self,
                             start_date: str,
                             end_date: str,
                             rebalance_freq: str) -> BacktestResult:
        """运行原有回测逻辑（向后兼容）"""
        print(f"\n{'='*60}")
        print(f"【回测引擎 - 传统模式】")
        print(f"回测区间: {start_date} ~ {end_date}")
        print(f"调仓频率: {rebalance_freq}")
        print(f"初始资金: {self.initial_capital:,.0f}")
        print(f"{'='*60}\n")
        
        # 初始化策略
        strategy = TradingStrategy(self.trading_config, self.initial_capital)
        
        # 获取交易日
        trading_days = self.get_trading_days(start_date, end_date)
        
        # 确定调仓日期
        if rebalance_freq == 'daily':
            rebalance_days = trading_days
        elif rebalance_freq == 'weekly':
            # 每周一调仓
            rebalance_days = []
            for i, day in enumerate(trading_days):
                dt = datetime.strptime(day, '%Y-%m-%d')
                if dt.weekday() == 0 or i == 0:  # 周一或第一天
                    rebalance_days.append(day)
        else:  # monthly
            # 每月第一个交易日
            rebalance_days = []
            current_month = None
            for day in trading_days:
                month = day[:7]
                if month != current_month:
                    rebalance_days.append(day)
                    current_month = month
        
        print(f"交易日数: {len(trading_days)}")
        print(f"调仓日数: {len(rebalance_days)}")
        
        # 缓存股票池和因子
        stock_universe = None
        factors_df = None
        
        # 回测主循环
        for day in tqdm(trading_days, desc="回测进度", ncols=80):
            
            # 获取持仓股票价格
            position_codes = list(strategy.positions.keys())
            
            if position_codes:
                prices = self.get_daily_prices(position_codes, day)
                
                # 检查出场条件
                for code in list(strategy.positions.keys()):
                    if code not in prices:
                        continue
                    
                    pos = strategy.positions[code]
                    price_data = prices[code]
                    
                    should_exit, exit_reason = strategy.check_exit_conditions(
                        pos, 
                        price_data['close'],
                        price_data['high'],
                        day
                    )
                    
                    if should_exit:
                        trade = strategy.execute_exit(code, price_data['close'], day, exit_reason)
                        if self.verbose and trade:
                            tqdm.write(f"  {day} 卖出 {trade.name}: {trade.return_pct:+.1%} ({exit_reason.value})")
            
            # 调仓日：生成新信号
            if day in rebalance_days:
                # 判断市场环境
                market_regime = self.determine_market_regime(day)
                strategy.set_market_regime(market_regime)
                
                # 获取股票池
                stock_universe = self.get_stock_universe(day)
                
                # 限制股票数量以加速
                sample_size = min(500, len(stock_universe))
                sample_codes = np.random.choice(stock_universe, sample_size, replace=False).tolist()
                
                # 计算因子
                try:
                    factors_df = self.factor_calculator.calculate_all_factors(sample_codes, day)
                except Exception as e:
                    logger.warning(f"因子计算失败 {day}: {e}")
                    factors_df = None
                
                # 预测
                if factors_df is not None and not factors_df.empty and self.predictor is not None:
                    try:
                        predictions = self.predictor.predict(factors_df)
                        factors_df['probability'] = [p.probability for p in predictions]
                    except Exception as e:
                        logger.warning(f"预测失败 {day}: {e}")
                        factors_df['probability'] = 0.5
                else:
                    if factors_df is not None:
                        factors_df['probability'] = 0.5
                
                # 添加当前价格
                if factors_df is not None and not factors_df.empty:
                    prices = self.get_daily_prices(factors_df['code'].tolist(), day)
                    factors_df['current_price'] = factors_df['code'].map(
                        lambda x: prices.get(x, {}).get('close', 0)
                    )
                    
                    # 生成入场信号
                    signals = strategy.generate_entry_signals(factors_df, day)
                    
                    # 执行入场
                    for signal in signals:
                        pos = strategy.execute_entry(signal)
                        if self.verbose and pos:
                            tqdm.write(f"  {day} 买入 {pos.name}: {pos.shares}股 @ {pos.entry_price:.2f}")
            
            # 更新权益
            all_codes = list(strategy.positions.keys())
            if all_codes:
                prices = self.get_daily_prices(all_codes, day)
                price_dict = {code: data['close'] for code, data in prices.items()}
            else:
                price_dict = {}
            
            strategy.update_equity(day, price_dict)
        
        # 强制平仓剩余持仓
        for code in list(strategy.positions.keys()):
            prices = self.get_daily_prices([code], trading_days[-1])
            if code in prices:
                strategy.execute_exit(code, prices[code]['close'], trading_days[-1], ExitReason.MANUAL)
        
        # 生成结果
        result = self._generate_result(strategy, start_date, end_date)
        
        self._print_summary(result)
        
        return result
    
    def run_simple(self,
                   candidates_list: List[Tuple[str, pd.DataFrame]],
                   price_cache: Dict = None) -> BacktestResult:
        """简化回测（使用预计算的候选股票）
        
        Args:
            candidates_list: [(date, candidates_df), ...] 
            price_cache: 价格缓存
        """
        print(f"\n【简化回测】处理 {len(candidates_list)} 个调仓周期")
        
        strategy = TradingStrategy(self.trading_config, self.initial_capital)
        
        dates = [item[0] for item in candidates_list]
        all_trading_days = self.get_trading_days(dates[0], dates[-1]) if self.jq else dates
        
        rebalance_idx = 0
        
        for day in tqdm(all_trading_days, desc="回测进度", ncols=80):
            # 检查出场
            for code in list(strategy.positions.keys()):
                pos = strategy.positions[code]
                
                # 获取价格
                if price_cache and code in price_cache and day in price_cache[code]:
                    price_data = price_cache[code][day]
                elif self.jq:
                    prices = self.get_daily_prices([code], day)
                    price_data = prices.get(code, {'close': pos.current_price, 'high': pos.highest_price})
                else:
                    continue
                
                should_exit, exit_reason = strategy.check_exit_conditions(
                    pos, price_data.get('close', pos.current_price),
                    price_data.get('high', pos.highest_price), day
                )
                
                if should_exit:
                    strategy.execute_exit(code, price_data['close'], day, exit_reason)
            
            # 调仓日
            if rebalance_idx < len(candidates_list) and day == candidates_list[rebalance_idx][0]:
                _, candidates = candidates_list[rebalance_idx]
                rebalance_idx += 1
                
                if candidates is not None and not candidates.empty:
                    signals = strategy.generate_entry_signals(candidates, day)
                    for signal in signals:
                        strategy.execute_entry(signal)
            
            # 更新权益
            price_dict = {}
            for code in strategy.positions.keys():
                if price_cache and code in price_cache and day in price_cache[code]:
                    price_dict[code] = price_cache[code][day]['close']
            strategy.update_equity(day, price_dict)
        
        return self._generate_result(strategy, dates[0], dates[-1])
    
    def _generate_result(self, 
                         strategy: TradingStrategy, 
                         start_date: str, 
                         end_date: str) -> BacktestResult:
        """生成回测结果"""
        perf = strategy.get_performance_summary()
        
        # 计算年化收益
        days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        total_return = (strategy.current_capital / strategy.initial_capital) - 1
        annualized_return = (1 + total_return) ** (365 / max(days, 1)) - 1 if total_return > -1 else -1
        
        # 月度收益
        if strategy.daily_equity:
            equity_df = pd.DataFrame(strategy.daily_equity)
            equity_df['date'] = pd.to_datetime(equity_df['date'])
            equity_df.set_index('date', inplace=True)
            monthly = equity_df['equity'].resample('M').last().pct_change().dropna()
            monthly_returns = {str(k.date()): v for k, v in monthly.items()}
        else:
            monthly_returns = {}
        
        return BacktestResult(
            start_date=start_date,
            end_date=end_date,
            initial_capital=strategy.initial_capital,
            final_capital=strategy.current_capital,
            total_return=total_return,
            annualized_return=annualized_return,
            max_drawdown=perf.get('max_drawdown', 0),
            sharpe_ratio=perf.get('sharpe_ratio', 0),
            total_trades=perf.get('total_trades', 0),
            win_rate=perf.get('win_rate', 0),
            profit_factor=perf.get('profit_factor', 0),
            avg_return=perf.get('avg_return', 0),
            hit_10pct_rate=perf.get('hit_10pct', 0),
            hit_5pct_rate=perf.get('hit_5pct', 0),
            trades=strategy.trades,
            daily_equity=strategy.daily_equity,
            monthly_returns=monthly_returns,
        )
    
    def _print_summary(self, result: BacktestResult):
        """打印回测摘要"""
        print(f"\n{'='*60}")
        print(f"【回测结果摘要】")
        print(f"{'='*60}")
        print(f"回测区间: {result.start_date} ~ {result.end_date}")
        print(f"初始资金: {result.initial_capital:,.0f}")
        print(f"最终资金: {result.final_capital:,.0f}")
        print(f"")
        print(f"【收益指标】")
        print(f"总收益率: {result.total_return:+.2%}")
        print(f"年化收益: {result.annualized_return:+.2%}")
        print(f"最大回撤: {result.max_drawdown:.2%}")
        print(f"夏普比率: {result.sharpe_ratio:.3f}")
        print(f"")
        print(f"【交易指标】")
        print(f"总交易次数: {result.total_trades}")
        print(f"胜率: {result.win_rate:.1%}")
        print(f"盈亏比: {result.profit_factor:.2f}")
        print(f"平均收益: {result.avg_return:.2%}")
        print(f"10%+命中率: {result.hit_10pct_rate:.1%}")
        print(f"5%+命中率: {result.hit_5pct_rate:.1%}")
        print(f"{'='*60}")


def main():
    """测试回测引擎"""
    engine = BacktestEngine(verbose=True)
    
    # 运行简短回测
    result = engine.run(
        start_date='2025-12-01',
        end_date='2025-12-15',
        rebalance_freq='weekly'
    )
    
    print(f"\n回测完成，总收益: {result.total_return:+.2%}")


if __name__ == '__main__':
    main()
