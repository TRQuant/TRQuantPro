"""
陈小群战法回测引擎
==================

封装陈小群战法的完整回测逻辑，提供简洁的API接口。

使用方式:
    from core.strategies.chen_xiaoqun import (
        ChenXiaoqunBacktestConfig,
        ChenXiaoqunBacktestEngine,
        ChenXiaoqunBacktestResult
    )
    
    config = ChenXiaoqunBacktestConfig(
        start_date='2025-12-01',
        end_date='2026-01-14'
    )
    engine = ChenXiaoqunBacktestEngine(config)
    result = engine.run(market_data_history, trade_days, jq_client)
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np

from .emotion_cycle import judge_emotion_cycle_with_confirmation
from .stock_selection import select_first_board_stocks, select_dragon_stocks
from .theme_analyzer import identify_top_themes

logger = logging.getLogger(__name__)


@dataclass
class ChenXiaoqunBacktestConfig:
    """回测配置"""
    start_date: str = ''
    end_date: str = ''
    initial_capital: float = 1000000.0
    commission: float = 0.0003      # 佣金率
    stamp_tax: float = 0.001        # 印花税
    slippage: float = 0.001         # 滑点
    stop_loss_pct: float = -0.08    # 止损比例（-8%，陈小群策略标准）
    take_profit_pct: float = 0.30   # 止盈比例（+30%，陈小群策略标准）
    max_holding_days: int = 5       # 最大持仓天数（短线策略）


@dataclass
class ChenXiaoqunBacktestResult:
    """回测结果"""
    start_date: str = ''
    end_date: str = ''
    initial_capital: float = 0.0
    final_capital: float = 0.0
    total_return: float = 0.0
    annualized_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    total_trades: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    daily_equity: List[Dict] = field(default_factory=list)
    trades: List[Dict] = field(default_factory=list)
    daily_cycles: List[Dict] = field(default_factory=list)
    strategy_stats: Dict[str, int] = field(default_factory=dict)
    
    def summary(self) -> str:
        """生成回测摘要"""
        return f"""
========== 陈小群战法回测结果 ==========
回测期间: {self.start_date} ~ {self.end_date}
初始资金: {self.initial_capital:,.0f}元
最终资金: {self.final_capital:,.0f}元
总收益率: {self.total_return*100:.2f}%
年化收益率: {self.annualized_return*100:.2f}%
最大回撤: {self.max_drawdown*100:.2f}%
夏普比率: {self.sharpe_ratio:.2f}
总交易次数: {self.total_trades}
胜率: {self.win_rate*100:.2f}%
盈亏比: {self.profit_factor:.2f}
==========================================
"""


class ChenXiaoqunBacktestEngine:
    """陈小群战法回测引擎"""
    
    def __init__(self, config: ChenXiaoqunBacktestConfig):
        """初始化回测引擎"""
        self.config = config
        self.initial_capital = config.initial_capital
        self.commission = config.commission
        self.stamp_tax = config.stamp_tax
        self.slippage = config.slippage
        
        # 状态变量
        self.cash = self.initial_capital
        self.positions: Dict[str, Dict] = {}  # {code: {shares, cost, buy_date, board_count}}
        self.equity_history: List[Dict] = []
        self.trades: List[Dict] = []
        self.daily_cycles: List[Dict] = []
        self.strategy_stats = {'首板卡位术': 0, '龙头战法': 0, '精选龙头': 0}
        
        # 缓存
        self._price_cache: Dict[str, Dict] = {}  # {code_date: price_info_dict}
        self._history_cycles: List[Dict] = []
        
    def reset(self):
        """重置引擎状态"""
        self.cash = self.initial_capital
        self.positions = {}
        self.equity_history = []
        self.trades = []
        self.daily_cycles = []
        self.strategy_stats = {'首板卡位术': 0, '龙头战法': 0, '精选龙头': 0}
        self._price_cache = {}
        self._history_cycles = []
    
    def run(self, 
            market_data_history: Dict[str, Dict],
            trade_days: List[str],
            jq_client: Any = None,
            verbose: bool = True) -> ChenXiaoqunBacktestResult:
        """
        执行回测
        
        Args:
            market_data_history: 市场数据字典 {date: {limit_up_count, zhaban_rate, max_height, limit_up_df}}
            trade_days: 交易日列表
            jq_client: JQData客户端（可选，用于获取价格数据）
            verbose: 是否输出详细日志
            
        Returns:
            ChenXiaoqunBacktestResult
        """
        self.reset()
        
        if verbose:
            print(f"🚀 开始执行回测...")
            print(f"   回测日期范围: {trade_days[0] if trade_days else 'N/A'} 至 {trade_days[-1] if trade_days else 'N/A'}")
            print(f"   交易天数: {len(trade_days)}天")
        
        prev_cycle = None
        
        for idx, date_str in enumerate(trade_days):
            # 获取当日市场数据
            limit_up_data = market_data_history.get(date_str)
            
            # 数据校验
            has_valid_data = False
            limit_up_count = 0
            zhaban_rate = 0
            max_height = 0
            limit_up_df = None
            avg_inflow = 0.0
            
            if limit_up_data is not None and isinstance(limit_up_data, dict):
                required_keys = ['limit_up_count', 'zhaban_rate', 'max_height']
                if all(k in limit_up_data for k in required_keys):
                    has_valid_data = True
                    limit_up_count = limit_up_data.get('limit_up_count', 0)
                    zhaban_rate = limit_up_data.get('zhaban_rate', 0)
                    max_height = limit_up_data.get('max_height', 0)
                    limit_up_df = limit_up_data.get('limit_up_df')
                    avg_inflow = limit_up_data.get('avg_inflow', 0.0)
            
            # 处理每日交易（即使数据缺失，也要处理已有持仓）
            actions = self._process_daily_trading(
                date_str=date_str,
                limit_up_count=limit_up_count,
                zhaban_rate=zhaban_rate,
                max_height=max_height,
                limit_up_df=limit_up_df,
                avg_inflow=avg_inflow,
                jq_client=jq_client,
                prev_cycle=prev_cycle,
                has_valid_data=has_valid_data
            )
            
            # 更新前一周期
            if self.daily_cycles:
                prev_cycle = self.daily_cycles[-1].get('cycle')
            
            # 显示周期变化
            if verbose and self.daily_cycles:
                current_cycle_info = self.daily_cycles[-1]
                if prev_cycle != current_cycle_info.get('cycle'):
                    print(f"\n   [{date_str}] 情绪周期: {prev_cycle or '初始'} -> {current_cycle_info.get('cycle')} | 策略: {current_cycle_info.get('strategy')}")
            
            # 进度显示
            if verbose and (idx + 1) % max(1, len(trade_days) // 5) == 0:
                current_value = self.get_portfolio_value(date_str, {})
                pnl = (current_value / self.initial_capital - 1) * 100
                print(f"   进度: {idx+1}/{len(trade_days)}, 权益: {current_value:,.0f}元, 收益: {pnl:.2f}%")
        
        # 计算回测指标
        result = self._calculate_result(trade_days)
        
        if verbose:
            print(f"\n✅ 回测完成！")
            print(result.summary())
        
        return result
    
    def _process_daily_trading(self,
                               date_str: str,
                               limit_up_count: int,
                               zhaban_rate: float,
                               max_height: int,
                               limit_up_df: Optional[pd.DataFrame],
                               avg_inflow: float,
                               jq_client: Any,
                               prev_cycle: Optional[str],
                               has_valid_data: bool = True) -> List[Dict]:
        """处理每日交易逻辑"""
        actions = []
        
        # 1. 判断情绪周期（仅在有有效数据时）
        if has_valid_data:
            # 准备history_cycles：只传递周期字符串列表
            history_cycle_strings = [c.get('cycle', '') for c in self._history_cycles[-3:] if isinstance(c, dict) and 'cycle' in c]
            
            cycle_info = judge_emotion_cycle_with_confirmation(
                limit_up_count=limit_up_count,
                zhaban_rate=zhaban_rate,
                max_height=max_height,
                avg_inflow=avg_inflow,
                history_cycles=history_cycle_strings if history_cycle_strings else None
            )
            
            current_cycle = cycle_info['cycle']
            target_position = self._parse_position_str(cycle_info['position'])
            current_strategy = cycle_info['strategy']
            
            # 记录周期（完整信息）
            self.daily_cycles.append({
                'date': date_str,
                'cycle': current_cycle,
                'position': target_position,
                'strategy': current_strategy,
                'confidence': cycle_info.get('confidence', 0)
            })
            # 记录到history_cycles（仅周期字符串，用于下次判断）
            self._history_cycles.append({
                'date': date_str,
                'cycle': current_cycle,
                'limit_up_count': limit_up_count
            })
        else:
            # 数据缺失时，使用上一日的周期和策略
            if self.daily_cycles:
                last_cycle_info = self.daily_cycles[-1]
                current_cycle = last_cycle_info.get('cycle', '未知')
                target_position = last_cycle_info.get('position', 0.0)
                current_strategy = last_cycle_info.get('strategy', '观望')
            else:
                current_cycle = '未知'
                target_position = 0.0
                current_strategy = '观望'
            
            # 记录周期（标记为数据缺失）
            self.daily_cycles.append({
                'date': date_str,
                'cycle': current_cycle,
                'position': target_position,
                'strategy': current_strategy,
                'confidence': 0,
                'data_missing': True
            })
        
        # 2. 识别最强题材（仅在有有效数据时）
        top_themes = []
        selected_stocks = []
        
        if has_valid_data:
            if limit_up_df is not None and isinstance(limit_up_df, pd.DataFrame) and not limit_up_df.empty:
                try:
                    top_themes = identify_top_themes(limit_up_df, top_n=5)
                except Exception as e:
                    logger.debug(f"题材识别失败: {e}")
            
            # 3. 选股
            df_for_selection = limit_up_df if limit_up_df is not None and isinstance(limit_up_df, pd.DataFrame) else pd.DataFrame()
            
            # 优化选股逻辑：优先选择连板数更高的股票（二板、三板）
            # 1. 优先选择连板数>=2的股票（龙头战法，二板、三板）
            # 使用优化后的连板股票选择器（双重验证连板数）
            try:
                from .consecutive_board_selector import select_consecutive_board_stocks
                
                # 优先使用优化后的连板股票选择器
                dragon_stocks_optimized = select_consecutive_board_stocks(
                    limit_up_data=df_for_selection,
                    date_str=date_str,
                    jq_client=jq_client,
                    min_board_count=2,
                    top_n=5,
                    top_themes=top_themes
                ) if not df_for_selection.empty else []
                
                # 如果优化后的选择器选中了股票，使用它；否则使用原始选择器
                if dragon_stocks_optimized:
                    dragon_stocks = dragon_stocks_optimized
                    logger.info(f"{date_str} 使用优化后的连板股票选择器，选中{len(dragon_stocks)}只")
                else:
                    dragon_stocks = select_dragon_stocks(
                        limit_up_data=df_for_selection,
                        date_str=date_str,
                        top_themes=top_themes
                    ) if not df_for_selection.empty else []
                    logger.info(f"{date_str} 使用原始选择器，选中{len(dragon_stocks)}只")
            except Exception as e:
                logger.warning(f"{date_str} 优化选择器失败，使用原始选择器: {e}")
                dragon_stocks = select_dragon_stocks(
                    limit_up_data=df_for_selection,
                    date_str=date_str,
                    top_themes=top_themes
                ) if not df_for_selection.empty else []
            
            # 2. 如果没有连板股票，再选择首板股票（首板卡位术）
            first_board_stocks = select_first_board_stocks(
                limit_up_data=df_for_selection,
                date_str=date_str,
                top_themes=top_themes
            ) if not df_for_selection.empty else []
            
            # 3. 合并选股结果，优先连板股票
            if dragon_stocks:
                # 有连板股票，优先选择（最多2只最强龙头）
                selected_stocks = dragon_stocks[:2]
                logger.info(f"{date_str} 选中连板股票: {len(dragon_stocks)}只，选择前2只")
                for stock in selected_stocks:
                    logger.info(f"  - {stock.get('name', '')} ({stock.get('code', '')}): {stock.get('board_count', 0)}板")
            elif first_board_stocks:
                # 没有连板股票，选择首板股票（最多3只）
                selected_stocks = first_board_stocks[:3]
                logger.info(f"{date_str} 没有连板股票，选择首板股票: {len(first_board_stocks)}只，选择前3只")
            else:
                selected_stocks = []
                logger.info(f"{date_str} 没有选中任何股票")
            
            # 4. 逐步减仓策略：如果有持仓，不买入新股票
            if current_strategy == '逐步减仓' and self.positions:
                logger.info(f"{date_str} 逐步减仓策略，有持仓，不买入新股票")
                selected_stocks = []
        
        # 4. 获取价格数据（无论是否有有效数据，都要获取持仓股票价格）
        all_codes = [s['jq_code'] for s in selected_stocks if 'jq_code' in s]
        all_codes.extend(list(self.positions.keys()))
        
        price_data = self._get_stock_prices(all_codes, date_str, jq_client)
        
        # 5. 检查止损止盈（无论是否有有效数据，都要检查持仓）
        # 关键：必须每天检查止损，即使没有新的市场数据
        exit_actions = self._check_exits(date_str, price_data, zhaban_rate if has_valid_data else 0)
        actions.extend(exit_actions)
        
        # 如果执行了卖出，重新计算权益和持仓价值
        if exit_actions:
            current_value = self.get_portfolio_value(date_str, price_data)
            current_position_value = sum(
                pos['shares'] * (price_data.get(code, {}).get('close', pos['cost']) if isinstance(price_data.get(code), dict) else price_data.get(code, pos['cost']))
                for code, pos in self.positions.items()
            )
        
        # 6. 计算当前权益和持仓价值（无论是否有有效数据都需要）
        current_value = self.get_portfolio_value(date_str, price_data)
        current_position_value = sum(
            pos['shares'] * (price_data.get(code, {}).get('close', pos['cost']) if isinstance(price_data.get(code), dict) else price_data.get(code, pos['cost']))
            for code, pos in self.positions.items()
        )
        
        # 7. 执行买入（仅在有有效数据且有仓位空间时）
        if has_valid_data:
            current_position_pct = current_position_value / current_value if current_value > 0 else 0
            position_diff = target_position - current_position_pct
            
            if position_diff > 0.05 and selected_stocks:
                # 有加仓空间
                # 聚焦总龙头：最多买入3只（陈小群策略特点）
                max_stocks = min(3, len(selected_stocks))
                for stock in selected_stocks[:max_stocks]:
                    jq_code = stock.get('jq_code')
                    if not jq_code or jq_code in self.positions:
                        continue
                    
                    # 获取价格信息
                    price_info = price_data.get(jq_code)
                    if not price_info:
                        continue
                    
                    # 检查停牌
                    if price_info.get('paused', False):
                        logger.debug(f"{jq_code} 停牌，跳过买入")
                        continue
                    
                    # 判断是否涨停
                    is_limit_up = price_info.get('is_limit_up', False)
                    
                    # 获取连板数（从选股结果中获取）
                    board_count = stock.get('board_count', 1)
                    
                    # 决定买入价格（根据连板数决定是否打板）
                    buy_price = self._decide_buy_price(price_info, current_strategy, board_count, is_limit_up)
                    if buy_price is None:
                        logger.debug(f"{jq_code} 策略不允许买入（涨停且策略不允许追板）")
                        continue
                    
                    # 计算目标仓位（三板斧仓位管理，优先于情绪周期目标仓位）
                    target_stock_position = self._calculate_sanbanfu_position(board_count, current_position_pct)
                    # 三板斧仓位管理优先：严格按照连板数决定单只股票仓位
                    # 首板10%，二板50%，三板40%，不受情绪周期目标仓位限制（但不超过总仓位上限90%）
                    # 如果当前仓位+目标股票仓位超过90%，则调整
                    max_total_position = 0.90  # 总仓位上限90%
                    available_position = max_total_position - current_position_pct
                    stock_position = min(target_stock_position, available_position)
                    
                    # 如果计算出的仓位太小（小于1%），跳过买入
                    if stock_position < 0.01:
                        logger.debug(f"{jq_code} 仓位不足（需要{target_stock_position:.2%}，可用{available_position:.2%}）")
                        continue
                    
                    # 记录买入尝试
                    logger.info(f"{date_str} 尝试买入 {stock.get('name', jq_code)} ({jq_code}): "
                              f"连板数={board_count}, 价格={buy_price:.2f}, 仓位={stock_position:.2%}")
                    
                    if self.execute_buy(date_str, jq_code, buy_price, stock_position, board_count=board_count):
                        logger.info(f"{date_str} ✅ 买入成功: {stock.get('name', jq_code)} ({jq_code}), "
                                  f"连板数={board_count}, 仓位={stock_position:.2%}")
                        strategy_name = current_strategy.split('（')[0]
                        self.strategy_stats[strategy_name] = self.strategy_stats.get(strategy_name, 0) + 1
                        actions.append({
                            'action': 'buy',
                            'code': stock.get('code', jq_code),
                            'name': stock.get('name', ''),
                            'reason': current_strategy,
                            'position': stock_position,
                            'price': buy_price
                        })
                        # 买入后重新计算权益
                        current_value = self.get_portfolio_value(date_str, price_data)
                        current_position_value = sum(
                            pos['shares'] * (price_data.get(code, {}).get('close', pos['cost']) if isinstance(price_data.get(code), dict) else price_data.get(code, pos['cost']))
                            for code, pos in self.positions.items()
                        )
        
        # 8. 记录当日权益（无论是否有有效数据都要记录）
        self.equity_history.append({
            'date': date_str,
            'equity': current_value,
            'cash': self.cash,
            'position_value': current_position_value,
            'position_count': len(self.positions)
        })
        
        return actions
    
    def _get_stock_prices(self, codes: List[str], date_str: str, jq_client: Any) -> Dict[str, Dict]:
        """
        获取股票价格数据（完整信息）
        
        Returns:
            Dict[str, Dict]: {code: {
                'close': 收盘价,
                'open': 开盘价,
                'high': 最高价,
                'low': 最低价,
                'high_limit': 涨停价,
                'low_limit': 跌停价,
                'pre_close': 昨收,
                'paused': 是否停牌,
                'is_limit_up': 是否涨停,
                'is_limit_down': 是否跌停
            }}
        """
        price_data = {}
        
        if not jq_client:
            # 如果没有jq_client，使用持仓成本作为价格
            for code in codes:
                if code in self.positions:
                    price_data[code] = {
                        'close': self.positions[code]['cost'],
                        'open': self.positions[code]['cost'],
                        'high': self.positions[code]['cost'],
                        'low': self.positions[code]['cost'],
                        'high_limit': self.positions[code]['cost'] * 1.1,
                        'low_limit': self.positions[code]['cost'] * 0.9,
                        'pre_close': self.positions[code]['cost'],
                        'paused': False,
                        'is_limit_up': False,
                        'is_limit_down': False
                    }
            return price_data
        
        for code in codes:
            try:
                # 检查缓存
                cache_key = f"{code}_{date_str}"
                if cache_key in self._price_cache:
                    price_data[code] = self._price_cache[cache_key]
                    continue
                
                # 从JQData获取完整价格数据
                # 支持jqdatasdk直接调用或封装后的client
                if hasattr(jq_client, 'get_price'):
                    # 封装后的client
                    df = jq_client.get_price(
                        code,
                        start_date=date_str,
                        end_date=date_str,
                        frequency='daily',
                        fields=['open', 'close', 'high', 'low', 'high_limit', 'low_limit', 'pre_close', 'paused']
                    )
                else:
                    # 直接使用jqdatasdk
                    import jqdatasdk as jq
                    df = jq.get_price(
                        code,
                        start_date=date_str,
                        end_date=date_str,
                        frequency='daily',
                        fields=['open', 'close', 'high', 'low', 'high_limit', 'low_limit', 'pre_close', 'paused']
                    )
                
                if df is not None and not df.empty:
                    row = df.iloc[0]
                    price_info = {
                        'close': float(row.get('close', 0)),
                        'open': float(row.get('open', 0)),
                        'high': float(row.get('high', 0)),
                        'low': float(row.get('low', 0)),
                        'high_limit': float(row.get('high_limit', 0)),
                        'low_limit': float(row.get('low_limit', 0)),
                        'pre_close': float(row.get('pre_close', 0)),
                        'paused': bool(row.get('paused', False)),
                        'is_limit_up': False,
                        'is_limit_down': False
                    }
                    
                    # 判断是否涨停/跌停（容差0.01元）
                    if price_info['high_limit'] > 0:
                        price_info['is_limit_up'] = abs(price_info['close'] - price_info['high_limit']) < 0.01
                    if price_info['low_limit'] > 0:
                        price_info['is_limit_down'] = abs(price_info['close'] - price_info['low_limit']) < 0.01
                    
                    price_data[code] = price_info
                    self._price_cache[cache_key] = price_info
            except Exception as e:
                logger.debug(f"获取{code}价格失败: {e}")
                # 如果获取失败，使用持仓成本
                if code in self.positions:
                    cost = self.positions[code]['cost']
                    price_data[code] = {
                        'close': cost,
                        'open': cost,
                        'high': cost,
                        'low': cost,
                        'high_limit': cost * 1.1,
                        'low_limit': cost * 0.9,
                        'pre_close': cost,
                        'paused': False,
                        'is_limit_up': False,
                        'is_limit_down': False
                    }
        
        return price_data
    
    def _decide_buy_price(self, price_info: Dict, strategy: str, board_count: int = 1, is_limit_up: bool = False) -> float:
        """
        决定买入价格（支持打板买入，体现陈小群策略特点）
        
        策略（根据连板数）：
        - 首板（board_count=1）：开盘价买入（如果开盘未涨停）或扫板买入（如果开盘涨停）
        - 二板及以上（board_count>=2）：打板买入（涨停价买入）
        - 逐步减仓：不追涨停，使用收盘价（如果未涨停）
        
        Args:
            price_info: 价格信息字典
            strategy: 当前策略
            board_count: 连板数（1=首板，2=二板，3=三板等）
            is_limit_up: 是否涨停
            
        Returns:
            买入价格，如果无法买入则返回None
        """
        # 逐步减仓策略：不追涨停
        if '逐步减仓' in strategy:
            if is_limit_up:
                return None  # 不追涨停
            return price_info.get('close', price_info.get('open', 0))
        
        # 根据连板数决定买入逻辑
        if board_count >= 2:
            # 连板股票（二板及以上）：必须打板买入
            if is_limit_up:
                return price_info.get('high_limit', price_info.get('close', 0))
            else:
                # 如果未涨停，使用收盘价（但这种情况很少）
                return price_info.get('close', price_info.get('open', 0))
        else:
            # 首板：开盘价买入（如果开盘未涨停）或扫板买入（如果开盘涨停）
            if is_limit_up:
                # 开盘即涨停，扫板买入
                return price_info.get('high_limit', price_info.get('close', 0))
            else:
                # 开盘未涨停，使用开盘价买入
                return price_info.get('open', price_info.get('close', 0))
    
    def _calculate_sanbanfu_position(self, board_count: int, current_position: float = 0.0) -> float:
        """
        计算三板斧仓位（陈小群策略核心）
        
        规则：
        - 首板：10%试错仓
        - 二板：50%主攻仓（在首板10%基础上加仓40%）
        - 三板及以上：40%加仓仓（在二板50%基础上加仓40%，总仓位90%）
        
        Args:
            board_count: 连板数（1=首板，2=二板，3=三板等）
            current_position: 当前仓位（0-1之间）
        
        Returns:
            目标仓位（0-1之间）
        """
        if board_count == 1:
            return 0.10  # 首板10%试错仓
        elif board_count == 2:
            return 0.50  # 二板50%主攻仓
        elif board_count >= 3:
            # 三板40%加仓仓（在已有50%基础上再加40%，总仓位90%）
            # 如果当前已有仓位，计算需要加仓的金额
            if current_position >= 0.50:
                return 0.40  # 在已有50%基础上再加40%
            else:
                return 0.50  # 如果当前仓位不足50%，先补到50%
        else:
            return 0.0
    
    def _decide_sell_price(self, price_info: Dict, reason: str) -> float:
        """
        决定卖出价格
        
        策略：
        - 止损/止盈：使用收盘价
        - 跌停：不能卖出（返回None）
        - 炸板：使用当前价格（可能是盘中价格）
        
        Args:
            price_info: 价格信息字典
            reason: 卖出原因
            
        Returns:
            卖出价格，如果无法卖出则返回None
        """
        # 如果跌停，不能卖出
        if price_info.get('is_limit_down', False):
            return None
        
        # 如果停牌，不能卖出
        if price_info.get('paused', False):
            return None
        
        # 根据原因决定卖出价格
        if '炸板' in reason:
            # 炸板：使用当前价格（可能是盘中价格，这里用收盘价模拟）
            return price_info.get('close', price_info.get('open', 0))
        else:
            # 止损/止盈：使用收盘价
            return price_info.get('close', price_info.get('open', 0))
    
    def _check_exits(self, date_str: str, price_data: Dict[str, Dict], zhaban_rate: float) -> List[Dict]:
        """检查止损止盈"""
        actions = []
        
        for code, pos in list(self.positions.items()):
            price_info = price_data.get(code)
            # 如果价格数据获取失败，使用持仓成本（但记录警告）
            if not price_info:
                logger.warning(f"{code} 价格数据获取失败，使用持仓成本进行止损检查")
                # 创建一个模拟的价格信息字典
                price_info = {
                    'close': pos['cost'],
                    'open': pos['cost'],
                    'high': pos['cost'],
                    'low': pos['cost'],
                    'high_limit': pos['cost'] * 1.1,
                    'low_limit': pos['cost'] * 0.9,
                    'pre_close': pos['cost'],
                    'paused': False,
                    'is_limit_up': False,
                    'is_limit_down': False
                }
            
            # 兼容旧格式（如果是float）
            if isinstance(price_info, (int, float)):
                current_price = price_info
            else:
                current_price = price_info.get('close', pos['cost'])
            
            cost = pos['cost']
            pnl_pct = (current_price - cost) / cost
            
            # 计算持仓天数
            buy_date = pos.get('buy_date', date_str)
            try:
                days_held = (datetime.strptime(date_str, '%Y-%m-%d') - datetime.strptime(buy_date, '%Y-%m-%d')).days
            except:
                days_held = 0
            
            # T+1规则：买入当天不能卖出
            if days_held == 0:
                continue  # 跳过当日买入的股票
            
            exit_reason = None
            
            # 止损检查（优先级最高，严格执行-8%）
            if pnl_pct <= self.config.stop_loss_pct:
                exit_reason = f'止损({pnl_pct*100:.1f}%)'
            # 提前止损：如果连续2天未涨停且亏损超过-5%，提前止损
            elif days_held >= 2 and pnl_pct <= -0.05:
                # 检查是否连续2天未涨停（需要历史数据，这里简化处理）
                exit_reason = f'提前止损({pnl_pct*100:.1f}%，连续下跌)'
            # 严格止损：如果亏损超过-6%，立即止损（接近-8%止损线）
            elif pnl_pct <= -0.06:
                exit_reason = f'严格止损({pnl_pct*100:.1f}%，接近止损线)'
            # 止盈检查
            elif pnl_pct >= self.config.take_profit_pct:
                exit_reason = f'止盈({pnl_pct*100:.1f}%)'
            # 移动止盈：从最高点回撤-10%止盈（如果已经盈利超过+20%）
            elif pnl_pct >= 0.20:
                # 获取持仓期间的最高价
                max_price = pos.get('max_price', cost)
                if current_price > max_price:
                    # 更新最高价
                    pos['max_price'] = current_price
                    max_price = current_price
                
                # 如果从最高点回撤超过-10%，止盈
                if max_price > cost:
                    drawdown_from_high = (current_price - max_price) / max_price
                    if drawdown_from_high <= -0.10:
                        exit_reason = f'移动止盈({pnl_pct*100:.1f}%，从最高点回撤{drawdown_from_high*100:.1f}%)'
                elif pnl_pct >= 0.30:
                    # 如果已经达到+30%，立即止盈
                    exit_reason = f'止盈({pnl_pct*100:.1f}%)'
            # 持仓时间过长
            elif days_held >= self.config.max_holding_days:
                exit_reason = f'持仓超{self.config.max_holding_days}天'
            # 炸板率过高（市场风险）
            elif zhaban_rate > 35 and pnl_pct > 0:
                exit_reason = f'炸板率过高({zhaban_rate:.1f}%)锁定利润'
            
            if exit_reason:
                # 决定卖出价格（考虑跌停等因素）
                sell_price = self._decide_sell_price(price_info, exit_reason)
                if sell_price is not None:
                    if self.execute_sell(date_str, code, sell_price, exit_reason):
                        actions.append({
                            'action': 'sell',
                            'code': code,
                            'reason': exit_reason,
                            'pnl_pct': pnl_pct,
                            'price': sell_price
                        })
                else:
                    logger.debug(f"{code} 无法卖出（跌停或停牌）")
        
        return actions
    
    def get_portfolio_value(self, date_str: str, price_data: Dict[str, Dict]) -> float:
        """计算组合市值"""
        position_value = 0
        for code, pos in self.positions.items():
            price_info = price_data.get(code)
            if price_info:
                # 新格式：字典
                if isinstance(price_info, dict):
                    position_value += pos['shares'] * price_info.get('close', pos['cost'])
                else:
                    # 旧格式：float
                    position_value += pos['shares'] * price_info
            else:
                position_value += pos['shares'] * pos['cost']
        return self.cash + position_value
    
    def execute_buy(self, date: str, code: str, price: float, target_weight: float, board_count: int = 1) -> bool:
        """执行买入"""
        # 计算目标金额
        total_value = self.cash + sum(
            pos['shares'] * price for pos in self.positions.values()
        )
        target_amount = total_value * target_weight
        
        # 考虑滑点
        actual_price = price * (1 + self.slippage)
        
        # 计算可买股数（100股整数倍）
        shares = int(target_amount / actual_price / 100) * 100
        if shares <= 0:
            return False
        
        # 计算交易成本
        amount = shares * actual_price
        commission = max(amount * self.commission, 5)  # 最低5元
        total_cost = amount + commission
        
        if total_cost > self.cash:
            # 资金不足，调整股数
            shares = int((self.cash - 5) / actual_price / (1 + self.commission) / 100) * 100
            if shares <= 0:
                return False
            amount = shares * actual_price
            commission = max(amount * self.commission, 5)
            total_cost = amount + commission
        
        # 执行买入
        self.cash -= total_cost
        
        if code in self.positions:
            # 加仓
            old_pos = self.positions[code]
            total_shares = old_pos['shares'] + shares
            total_cost_basis = old_pos['cost'] * old_pos['shares'] + amount
            self.positions[code] = {
                'shares': total_shares,
                'cost': total_cost_basis / total_shares,
                'board_count': old_pos.get('board_count', 0) + 1,
                'buy_date': old_pos.get('buy_date', date),
                'max_price': max(old_pos.get('max_price', actual_price), actual_price)  # 记录最高价
            }
        else:
            # 新建仓位
            self.positions[code] = {
                'shares': shares,
                'cost': actual_price,
                'board_count': board_count,  # 使用传入的board_count
                'buy_date': date,
                'max_price': actual_price  # 记录最高价（用于移动止盈）
            }
        
        # 记录交易
        self.trades.append({
            'date': date,
            'code': code,
            'action': 'buy',
            'shares': shares,
            'price': actual_price,
            'amount': amount,
            'commission': commission,
            'pnl': 0
        })
        
        return True
    
    def execute_sell(self, date: str, code: str, price: float, reason: str) -> bool:
        """执行卖出"""
        if code not in self.positions:
            return False
        
        pos = self.positions[code]
        shares = pos['shares']
        cost = pos['cost']
        
        # 考虑滑点
        actual_price = price * (1 - self.slippage)
        
        # 计算交易成本
        amount = shares * actual_price
        commission = max(amount * self.commission, 5)
        stamp_tax = amount * self.stamp_tax
        total_fee = commission + stamp_tax
        
        # 计算盈亏
        pnl = amount - total_fee - (shares * cost)
        
        # 执行卖出
        self.cash += amount - total_fee
        del self.positions[code]
        
        # 记录交易
        self.trades.append({
            'date': date,
            'code': code,
            'action': 'sell',
            'shares': shares,
            'price': actual_price,
            'amount': amount,
            'commission': commission,
            'stamp_tax': stamp_tax,
            'pnl': pnl,
            'reason': reason
        })
        
        return True
    
    def _calculate_result(self, trade_days: List[str]) -> ChenXiaoqunBacktestResult:
        """计算回测结果"""
        if not self.equity_history:
            return ChenXiaoqunBacktestResult(
                start_date=trade_days[0] if trade_days else '',
                end_date=trade_days[-1] if trade_days else '',
                initial_capital=self.initial_capital,
                final_capital=self.initial_capital,
                strategy_stats=self.strategy_stats
            )
        
        # 基本指标
        final_equity = self.equity_history[-1]['equity'] if self.equity_history else self.initial_capital
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        
        # 年化收益率
        days = len(trade_days)
        annualized_return = ((1 + total_return) ** (252 / max(days, 1))) - 1 if days > 0 else 0
        
        # 最大回撤
        max_drawdown = 0
        peak = self.initial_capital
        for eq in self.equity_history:
            if eq['equity'] > peak:
                peak = eq['equity']
            drawdown = (peak - eq['equity']) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 夏普比率
        if len(self.equity_history) > 1:
            returns = []
            for i in range(1, len(self.equity_history)):
                prev_eq = self.equity_history[i-1]['equity']
                curr_eq = self.equity_history[i]['equity']
                if prev_eq > 0:
                    returns.append((curr_eq - prev_eq) / prev_eq)
            
            if returns:
                avg_return = np.mean(returns)
                std_return = np.std(returns) if len(returns) > 1 else 0.0001
                sharpe_ratio = (avg_return * 252 - 0.03) / (std_return * np.sqrt(252)) if std_return > 0 else 0
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        # 交易统计
        total_trades = len(self.trades)
        sell_trades = [t for t in self.trades if t['action'] == 'sell']
        winning_trades = [t for t in sell_trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in sell_trades if t.get('pnl', 0) <= 0]
        
        win_rate = len(winning_trades) / len(sell_trades) if sell_trades else 0
        
        total_profit = sum(t.get('pnl', 0) for t in winning_trades)
        total_loss = abs(sum(t.get('pnl', 0) for t in losing_trades))
        profit_factor = total_profit / total_loss if total_loss > 0 else 0
        
        return ChenXiaoqunBacktestResult(
            start_date=trade_days[0] if trade_days else '',
            end_date=trade_days[-1] if trade_days else '',
            initial_capital=self.initial_capital,
            final_capital=final_equity,
            total_return=total_return,
            annualized_return=annualized_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            total_trades=total_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            daily_equity=self.equity_history,
            trades=self.trades,
            daily_cycles=self.daily_cycles,
            strategy_stats=self.strategy_stats
        )
    
    @staticmethod
    def _parse_position_str(pos_str) -> float:
        """将仓位字符串转换为数值（0-1之间）"""
        if not isinstance(pos_str, str):
            return float(pos_str) if pos_str else 0.0
        
        pos_str = pos_str.strip().rstrip('+')
        
        # 处理范围格式 "20-30%" -> 取中值 0.25
        if '-' in pos_str and '%' in pos_str:
            parts = pos_str.replace('%', '').split('-')
            if len(parts) == 2:
                try:
                    min_val = float(parts[0]) / 100
                    max_val = float(parts[1]) / 100
                    return (min_val + max_val) / 2
                except:
                    pass
        
        # 处理百分比格式 "10%" -> 0.1
        if '%' in pos_str:
            try:
                return float(pos_str.replace('%', '')) / 100
            except:
                pass
        
        try:
            return float(pos_str)
        except:
            return 0.0


def run_chen_xiaoqun_backtest(
    market_data_history: Dict[str, Dict],
    trade_days: List[str],
    jq_client: Any = None,
    config: Optional[ChenXiaoqunBacktestConfig] = None,
    verbose: bool = True
) -> ChenXiaoqunBacktestResult:
    """
    快捷函数：运行陈小群战法回测
    
    Args:
        market_data_history: 市场数据字典
        trade_days: 交易日列表
        jq_client: JQData客户端（可选）
        config: 回测配置（可选）
        verbose: 是否输出详细日志
        
    Returns:
        ChenXiaoqunBacktestResult
    """
    if config is None:
        config = ChenXiaoqunBacktestConfig()
    
    engine = ChenXiaoqunBacktestEngine(config)
    return engine.run(market_data_history, trade_days, jq_client, verbose)
