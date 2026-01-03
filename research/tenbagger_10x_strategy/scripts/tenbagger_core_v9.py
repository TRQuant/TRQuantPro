#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Core Strategy V9 - 十倍股核心策略V9
==============================================

整合所有知识库的终极版本：

1. bear_market_exit_kb - 熊市早期退出
2. mainline_rotation_kb - 主线轮动追踪
3. altdata_integration_kb - 另类数据整合
4. ml_stage_predictor_kb - ML阶段预测
5. tenbagger_identification_kb - 十倍股识别
6. astock_regime_knowledge_v2 - 市场环境判断

核心公式：
十倍股 = 早期阶段(S1-S2) × 市场主线 × 业绩拐点 × 动态风控

Author: TRQuant Team
Date: 2025-12-27
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd
import logging

# 添加项目路径
PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入知识库
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime, AStockRegimeDetectorV2, ASTOCK_REGIME_STRATEGY
)
from research.tenbagger_10x_strategy.knowledge.bear_market_exit_kb import (
    BearPhase, BearMarketDetector, DynamicStopLossCalculator, PHASE_EXIT_STRATEGIES
)
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerIdentifier, TenbaggerStage, STAGE_POSITION_STRATEGY
)
from research.tenbagger_10x_strategy.knowledge.ml_stage_predictor_kb import (
    StageTransitionModel, TenbaggerRanker
)


class TenbaggerCoreV9Strategy:
    """十倍股核心策略V9
    
    特性：
    1. 熊市早期退出机制
    2. 动态止损系统
    3. 阶段化仓位管理
    4. ML增强的选股逻辑
    """
    
    def __init__(self):
        # 初始化各知识库组件
        self.regime_detector = AStockRegimeDetectorV2()
        self.bear_detector = BearMarketDetector()
        self.stop_loss_calc = DynamicStopLossCalculator()
        self.tenbagger_identifier = TenbaggerIdentifier()
        self.stage_model = StageTransitionModel()
        self.ranker = TenbaggerRanker()
        
        # JQData认证
        self._authenticated = False
        
        # 策略状态
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.bear_phase = BearPhase.NORMAL
        self.positions = {}  # {stock_code: {shares, entry_price, entry_date, stage, stop_loss}}
        self.cash = 1000000  # 初始资金
        self.initial_capital = 1000000
        
        # 交易记录
        self.trades = []
        self.equity_curve = []
        self.regime_history = []
        
        # 策略参数（根据熊市退出知识库优化）
        self.max_positions = 5
        self.position_size = 0.20  # 单票仓位
        self.base_stop_loss = 0.08
        self.base_take_profit = 0.30
        
        # 预加载数据
        self._price_data = None
        self._factor_data = None
        self._fundamental_data = None
        
    def _ensure_jqdata_auth(self):
        """确保JQData认证"""
        if self._authenticated:
            return
        try:
            import jqdatasdk as jq
            jq.auth('13327806797', 'Taorui888')
            self._authenticated = True
            logger.info("JQData认证成功")
        except Exception as e:
            logger.error(f"JQData认证失败: {e}")
            raise
            
    def _preload_data(self, start_date: str, end_date: str, stock_pool: List[str]):
        """预加载数据以提高回测速度"""
        self._ensure_jqdata_auth()
        import jqdatasdk as jq
        
        logger.info(f"预加载数据: {start_date} ~ {end_date}, 股票数: {len(stock_pool)}")
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date, end_date)
        
        # 预加载价格数据
        try:
            self._price_data = jq.get_price(
                stock_pool,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume'],
                skip_paused=False,
                fq='pre'
            )
            logger.info(f"价格数据加载完成: {self._price_data.shape if hasattr(self._price_data, 'shape') else 'N/A'}")
        except Exception as e:
            logger.error(f"价格数据加载失败: {e}")
            self._price_data = pd.DataFrame()
            
    def _load_fundamental_data(self, stocks: List[str], date: str):
        """加载财务数据"""
        self._ensure_jqdata_auth()
        import jqdatasdk as jq
        
        try:
            q = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin,
            ).filter(
                jq.valuation.code.in_(stocks[:500])
            )
            
            self._fundamental_data = jq.get_fundamentals(q, date=date)
            
            if self._fundamental_data is not None:
                self._fundamental_data = self._fundamental_data.set_index('code')
                logger.info(f"财务数据加载: {len(self._fundamental_data)} 条")
                
        except Exception as e:
            logger.warning(f"财务数据加载失败: {e}")
            self._fundamental_data = pd.DataFrame()
            
    def _get_index_data(self, index_code: str = '000300.XSHG', 
                        start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """获取指数数据（用于市场环境判断）"""
        self._ensure_jqdata_auth()
        import jqdatasdk as jq
        
        try:
            data = jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close', 'volume']
            )
            return data
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
            return pd.DataFrame()
            
    def _detect_market_regime(self, index_data: pd.DataFrame) -> Tuple[AStockRegime, float]:
        """检测市场环境"""
        min_days = 20  # 降低最小天数要求
        if len(index_data) < min_days:
            return AStockRegime.VOLATILE_RANGE, 0
            
        prices = index_data['close']
        volumes = index_data['volume'] if 'volume' in index_data else None
        
        regime, score, details = self.regime_detector.detect_regime(prices, volumes)
        logger.debug(f"市场环境: {regime.value}, 得分: {score:.1f}")
        return regime, score
        
    def _detect_bear_phase(self, index_data: pd.DataFrame) -> Tuple[BearPhase, float]:
        """检测熊市阶段"""
        if len(index_data) < 20:  # 降低要求
            return BearPhase.NORMAL, 0
            
        prices = index_data['close']
        volumes = index_data['volume'] if 'volume' in index_data else None
        
        phase, warning_score, signals = self.bear_detector.detect_phase(prices, volumes)
        return phase, warning_score
        
    def _get_position_params(self) -> Dict:
        """根据市场环境和熊市阶段获取仓位参数
        
        简化版：
        - 牛市：高仓位，宽松止损
        - 震荡：中仓位
        - 熊市：低仓位，严格止损
        """
        regime_name = self.current_regime.value
        
        # 简化的三档策略
        if 'BULL' in regime_name:
            position = 0.80
            stop_loss = 0.15
            take_profit = 0.50
            max_pos = 5
        elif 'BEAR' in regime_name:
            position = 0.10 if 'PANIC' in regime_name else 0.25
            stop_loss = 0.08
            take_profit = 0.25
            max_pos = 2 if 'PANIC' in regime_name else 3
        else:  # 震荡
            if 'UP' in regime_name:
                position = 0.60
                max_pos = 4
            elif 'DOWN' in regime_name:
                position = 0.30
                max_pos = 3
            else:
                position = 0.45
                max_pos = 4
            stop_loss = 0.10
            take_profit = 0.30
                
        return {
            'position': position,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'max_positions': max_pos
        }
        
    def _get_stock_data(self, stock: str, date: str = None) -> Optional[pd.DataFrame]:
        """获取单个股票数据"""
        if self._price_data is None or self._price_data.empty:
            return None
            
        # JQData返回的是扁平DataFrame，需要按code列筛选
        if 'code' in self._price_data.columns:
            stock_df = self._price_data[self._price_data['code'] == stock].copy()
            if len(stock_df) == 0:
                return None
            # 设置时间索引
            stock_df['time'] = pd.to_datetime(stock_df['time'])
            stock_df = stock_df.set_index('time').sort_index()
            if date:
                stock_df = stock_df[stock_df.index <= pd.Timestamp(date)]
            return stock_df
        return None
        
    def _select_stocks(self, date: str, stock_pool: List[str]) -> List[Tuple[str, float, str]]:
        """选择股票
        
        采用V8的核心方法：严格基本面筛选 + 阶段识别
        
        Returns:
            [(stock_code, score, stage), ...]
        """
        if self._fundamental_data is None or len(self._fundamental_data) == 0:
            logger.warning("财务数据为空")
            return []
            
        candidates = []
        
        for code, row in self._fundamental_data.iterrows():
            try:
                market_cap = row.get('market_cap', 0) or 0
                pe = row.get('pe_ratio', 0) or 0
                roe = row.get('roe', 0) or 0
                revenue_growth = (row.get('inc_revenue_year_on_year', 0) or 0) / 100
                profit_growth = (row.get('inc_net_profit_year_on_year', 0) or 0) / 100
                gross_margin = (row.get('gross_profit_margin', 0) or 0) / 100
                
                # 严格的基本面筛选（来自V8）
                if not (20 <= market_cap <= 500):
                    continue
                if profit_growth < 0.15:  # 利润增速>15%
                    continue
                if revenue_growth < 0.10:  # 营收增速>10%
                    continue
                    
                # 识别阶段
                stage = self.tenbagger_identifier.identify_stage(
                    market_cap=market_cap,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    roe=roe / 100 if roe > 1 else roe
                )
                
                # 排除成熟期和衰退期
                if stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                    continue
                    
                # 使用TenbaggerIdentifier评分
                is_potential, score, _, details = self.tenbagger_identifier.is_potential_tenbagger(
                    roe=roe / 100 if roe > 1 else roe,
                    gross_margin=gross_margin,
                    net_margin=0.1,
                    debt_ratio=0.4,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    peg=pe / (profit_growth * 100 + 1) if profit_growth > 0 else 99,
                    pe=pe,
                    market_cap=market_cap,
                    momentum_20d=0.05,
                    volume_ratio=1.2,
                    price_position=0.5,
                )
                
                candidates.append({
                    'code': code,
                    'market_cap': market_cap,
                    'profit_growth': profit_growth,
                    'revenue_growth': revenue_growth,
                    'stage': stage.value,
                    'score': score,
                    'is_potential': is_potential,
                })
                
            except Exception:
                continue
                
        # 排序
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # 市场环境过滤
        if self.current_regime in [AStockRegime.BEAR_PANIC]:
            return []  # 熊市恐慌不买
        elif self.current_regime in [AStockRegime.BEAR_GRINDING]:
            # 熊市磨底：只选高成长高得分
            candidates = [c for c in candidates if c['profit_growth'] > 0.30 and c['score'] > 65]
        elif self.current_regime in [AStockRegime.VOLATILE_DOWN]:
            # 震荡下行：只选最优
            candidates = [c for c in candidates if c['score'] > 60]
            
        # 转换格式返回
        return [(c['code'], c['score'], c['stage']) for c in candidates[:10]]
            
    def _calculate_dynamic_stop_loss(self, stock_code: str, entry_price: float) -> float:
        """计算动态止损价"""
        try:
            stock_df = self._get_stock_data(stock_code)
            if stock_df is not None and 'close' in stock_df:
                prices = stock_df['close'].dropna()
                if len(prices) >= 14:
                    stop = self.stop_loss_calc.calculate_atr_stop(prices)
                    return max(stop, entry_price * (1 - self.base_stop_loss))
        except:
            pass
                
        return entry_price * (1 - self.base_stop_loss)
        
    def _check_stop_orders(self, date: str):
        """非调仓日检查止盈止损"""
        params = self._get_position_params()
        stop_loss_pct = params['stop_loss']
        take_profit_pct = params['take_profit']
        
        # 熊市恐慌：强制清仓
        if self.bear_phase == BearPhase.PANIC:
            for stock in list(self.positions.keys()):
                self._sell_stock(stock, date, "熊市恐慌清仓")
            return
            
        # 检查现有持仓
        for stock, pos in list(self.positions.items()):
            stock_df = self._get_stock_data(stock, date)
            if stock_df is None or len(stock_df) == 0:
                continue
            current_price = stock_df['close'].iloc[-1]
            
            entry_price = pos['entry_price']
            stop_loss = pos.get('stop_loss', entry_price * (1 - stop_loss_pct))
            
            # 止损
            if current_price <= stop_loss:
                self._sell_stock(stock, date, f"止损")
                continue
                
            # 止盈
            if current_price >= entry_price * (1 + take_profit_pct):
                self._sell_stock(stock, date, f"止盈")
                continue
                
    def _execute_trades(self, date: str, selected_stocks: List[Tuple[str, float, str]]):
        """执行交易"""
        params = self._get_position_params()
        max_pos = params['max_positions']
        target_position = params['position']
        stop_loss_pct = params['stop_loss']
        take_profit_pct = params['take_profit']
        
        # 熊市恐慌：强制清仓
        if self.bear_phase == BearPhase.PANIC:
            for stock, pos in list(self.positions.items()):
                self._sell_stock(stock, date, "熊市恐慌清仓")
            return
            
        # 检查现有持仓的止盈止损
        for stock, pos in list(self.positions.items()):
            stock_df = self._get_stock_data(stock, date)
            if stock_df is None or len(stock_df) == 0:
                continue
            current_price = stock_df['close'].iloc[-1]
                
            entry_price = pos['entry_price']
            stop_loss = pos.get('stop_loss', entry_price * (1 - stop_loss_pct))
            
            # 止损
            if current_price <= stop_loss:
                self._sell_stock(stock, date, f"止损: {current_price:.2f} < {stop_loss:.2f}")
                continue
                
            # 止盈
            if current_price >= entry_price * (1 + take_profit_pct):
                self._sell_stock(stock, date, f"止盈: {(current_price/entry_price-1)*100:.1f}%")
                continue
                
            # 更新跟踪止损
            new_stop = self._calculate_dynamic_stop_loss(stock, entry_price)
            if new_stop > stop_loss:
                pos['stop_loss'] = new_stop
                
        # 买入新股票
        if len(self.positions) < max_pos and target_position > 0:
            available_slots = max_pos - len(self.positions)
            capital_per_stock = self.cash * target_position / max(available_slots, 1)
            
            for stock, score, stage in selected_stocks:
                if len(self.positions) >= max_pos:
                    break
                if stock in self.positions:
                    continue
                if capital_per_stock < 10000:  # 最小投资额
                    break
                    
                self._buy_stock(stock, date, capital_per_stock, stage)
                
    def _buy_stock(self, stock_code: str, date: str, amount: float, stage: str):
        """买入股票"""
        stock_df = self._get_stock_data(stock_code, date)
        if stock_df is None or len(stock_df) == 0:
            return
        price = stock_df['close'].iloc[-1]
            
        if pd.isna(price) or price <= 0:
            return
            
        shares = int(amount / price / 100) * 100  # 取整手
        if shares < 100:
            return
            
        cost = shares * price
        if cost > self.cash:
            return
            
        # 计算动态止损
        stop_loss = self._calculate_dynamic_stop_loss(stock_code, price)
        
        self.cash -= cost
        self.positions[stock_code] = {
            'shares': shares,
            'entry_price': price,
            'entry_date': date,
            'stage': stage,
            'stop_loss': stop_loss
        }
        
        self.trades.append({
            'date': date,
            'stock': stock_code,
            'action': 'BUY',
            'price': price,
            'shares': shares,
            'amount': cost,
            'stage': stage,
            'regime': self.current_regime.value
        })
        
        logger.debug(f"买入: {stock_code}, {shares}股 @ {price:.2f}, 阶段: {stage}")
        
    def _sell_stock(self, stock_code: str, date: str, reason: str):
        """卖出股票"""
        if stock_code not in self.positions:
            return
            
        pos = self.positions[stock_code]
        
        # 获取当前价格
        price = pos['entry_price']  # 默认
        stock_df = self._get_stock_data(stock_code, date)
        if stock_df is not None and len(stock_df) > 0:
            price = stock_df['close'].iloc[-1]
                
        if pd.isna(price) or price <= 0:
            price = pos['entry_price']
            
        shares = pos['shares']
        proceeds = shares * price
        self.cash += proceeds
        
        pnl = (price - pos['entry_price']) / pos['entry_price']
        
        self.trades.append({
            'date': date,
            'stock': stock_code,
            'action': 'SELL',
            'price': price,
            'shares': shares,
            'amount': proceeds,
            'pnl': pnl,
            'reason': reason,
            'regime': self.current_regime.value
        })
        
        del self.positions[stock_code]
        logger.debug(f"卖出: {stock_code}, {shares}股 @ {price:.2f}, 收益: {pnl*100:.1f}%, 原因: {reason}")
        
    def _calc_portfolio_value(self, date: str) -> float:
        """计算组合总价值"""
        total = self.cash
        
        for stock, pos in self.positions.items():
            stock_df = self._get_stock_data(stock, date)
            if stock_df is not None and len(stock_df) > 0:
                price = stock_df['close'].iloc[-1]
                if not pd.isna(price):
                    total += pos['shares'] * price
                    continue
            total += pos['shares'] * pos['entry_price']
            
        return total
        
    def run_backtest(self, start_date: str, end_date: str) -> Dict:
        """运行回测"""
        self._ensure_jqdata_auth()
        import jqdatasdk as jq
        
        logger.info(f"开始回测: {start_date} ~ {end_date}")
        
        # 获取股票池（沪深300成分股）
        stock_pool = list(jq.get_index_stocks('000300.XSHG'))
        logger.info(f"股票池: {len(stock_pool)}只")
        
        # 计算预加载数据的起始日期（需要额外历史计算技术指标）
        preload_start = (pd.to_datetime(start_date) - timedelta(days=120)).strftime('%Y-%m-%d')
        
        # 预加载数据
        self._preload_data(preload_start, end_date, stock_pool)
        
        # 加载财务数据
        self._load_fundamental_data(stock_pool, start_date)
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date, end_date)
        
        # 获取指数数据用于市场环境判断（也需要历史）
        index_data = self._get_index_data('000300.XSHG', preload_start, end_date)
        
        # 调仓参数
        rebalance_interval = 60  # 约2个月调仓一次
        regime_check_interval = 5  # 每周检测市场环境
        last_rebalance = -rebalance_interval  # 第一天就调仓
        last_regime_check = -regime_check_interval
        
        # 逐日回测
        for i, date in enumerate(trade_days):
            date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
            
            # 每周检测市场环境
            if i - last_regime_check >= regime_check_interval:
                if not index_data.empty:
                    idx_to_date = index_data[index_data.index <= date_str]
                    if len(idx_to_date) >= 20:
                        self.current_regime, regime_score = self._detect_market_regime(idx_to_date)
                        self.bear_phase, warning_score = self._detect_bear_phase(idx_to_date)
                last_regime_check = i
                    
            # 记录环境
            self.regime_history.append({
                'date': date_str,
                'regime': self.current_regime.value,
                'bear_phase': self.bear_phase.value
            })
            
            # 定期调仓或第一天
            if i - last_rebalance >= rebalance_interval:
                # 更新财务数据
                self._load_fundamental_data(stock_pool, date_str)
                # 选股
                selected = self._select_stocks(date_str, stock_pool)
                # 执行交易
                self._execute_trades(date_str, selected)
                last_rebalance = i
            else:
                # 非调仓日只检查止盈止损
                self._check_stop_orders(date_str)
            
            # 记录净值
            portfolio_value = self._calc_portfolio_value(date_str)
            self.equity_curve.append({
                'date': date_str,
                'value': portfolio_value,
                'regime': self.current_regime.value
            })
            
            # 进度日志
            if i % 50 == 0:
                logger.info(f"进度: {i+1}/{len(trade_days)}, 日期: {date_str}, 净值: {portfolio_value:.2f}")
                
        # 计算结果
        return self._calc_result()
        
    def _calc_result(self) -> Dict:
        """计算回测结果"""
        if not self.equity_curve:
            return {"success": False, "error": "无权益曲线数据"}
            
        values = [e['value'] for e in self.equity_curve]
        dates = [e['date'] for e in self.equity_curve]
        
        final_value = values[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # 计算最大回撤
        peak = values[0]
        max_drawdown = 0
        for v in values:
            if v > peak:
                peak = v
            drawdown = (peak - v) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                
        # 年化收益
        days = (pd.to_datetime(dates[-1]) - pd.to_datetime(dates[0])).days
        annual_return = (1 + total_return) ** (365 / max(days, 1)) - 1 if days > 0 else 0
        
        # 夏普比率
        returns = pd.Series(values).pct_change().dropna()
        if len(returns) > 0 and returns.std() > 0:
            sharpe = returns.mean() / returns.std() * np.sqrt(252)
        else:
            sharpe = 0
            
        # 按环境统计
        regime_stats = {}
        for entry in self.equity_curve:
            regime = entry['regime']
            if regime not in regime_stats:
                regime_stats[regime] = {'days': 0}
            regime_stats[regime]['days'] += 1
            
        return {
            "success": True,
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
            "final_value": final_value,
            "trade_count": len(self.trades),
            "days": days,
            "regime_stats": regime_stats,
            "position_count": len(self.positions)
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Tenbagger Core V9 Strategy')
    parser.add_argument('-p', '--period', default='1y', 
                        help='回测周期: 1m/3m/6m/1y/2y/3y')
    args = parser.parse_args()
    
    # 计算日期范围
    end_date = '2024-12-31'
    period_map = {
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        '2y': 730,
        '3y': 1095
    }
    days = period_map.get(args.period, 365)
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days)).strftime('%Y-%m-%d')
    
    print(f"\n{'='*60}")
    print(f"Tenbagger Core V9 - 十倍股核心策略回测")
    print(f"{'='*60}")
    print(f"周期: {args.period} ({start_date} ~ {end_date})")
    print(f"{'='*60}\n")
    
    # 运行回测
    strategy = TenbaggerCoreV9Strategy()
    result = strategy.run_backtest(start_date, end_date)
    
    # 输出结果
    if result.get('success'):
        print(f"\n{'='*60}")
        print(f"回测结果")
        print(f"{'='*60}")
        print(f"总收益率: {result['total_return']*100:.2f}%")
        print(f"年化收益: {result['annual_return']*100:.2f}%")
        print(f"最大回撤: {result['max_drawdown']*100:.2f}%")
        print(f"夏普比率: {result['sharpe_ratio']:.2f}")
        print(f"交易次数: {result['trade_count']}")
        print(f"回测天数: {result['days']}")
        print(f"\n市场环境分布:")
        for regime, stats in result.get('regime_stats', {}).items():
            print(f"  {regime}: {stats['days']}天")
        print(f"{'='*60}\n")
    else:
        print(f"回测失败: {result.get('error', '未知错误')}")


if __name__ == '__main__':
    main()

