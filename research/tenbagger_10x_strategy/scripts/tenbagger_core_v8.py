#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股核心策略 V8.0 - 市场环境感知 + 早期识别
==============================================

V8相对V7的改进：
1. 整合市场环境判断（熊市减仓/空仓）
2. 熊市寻找超跌反弹机会
3. 牛市加大仓位
4. 更严格的止损机制

核心思想：
- 熊市：减少仓位到20%，等待反转信号
- 震荡：保持50%仓位，精选个股
- 牛市：加大仓位到80%，追逐主线

创建时间：2025-12-27
"""

import sys
import os
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np

sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from research.tenbagger_10x_strategy.knowledge.tenbagger_core_strategy_kb import (
    HISTORICAL_TENBAGGERS,
    TenbaggerEarlySignals,
    TENBAGGER_BUY_RULES,
    TENBAGGER_SELL_RULES,
    STAGE_POSITION_STRATEGY,
    EarlyEntryAlgorithm,
)
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerStage,
    TenbaggerIdentifier,
    TenbaggerScorer,
)
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime,
    AStockRegimeDetectorV2,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 市场环境下的仓位控制
MARKET_REGIME_POSITION = {
    'BULL_EARLY': 0.70,
    'BULL_MID': 0.80,
    'BULL_LATE': 0.60,
    'BEAR_PANIC': 0.10,
    'BEAR_GRINDING': 0.15,
    'VOLATILE_UP': 0.50,
    'VOLATILE_DOWN': 0.25,
    'VOLATILE_RANGE': 0.40,
    'RECOVERY': 0.60,
    'DISTRIBUTION': 0.30,
}


class TenbaggerCoreStrategyV8:
    """十倍股核心策略 V8 - 市场环境感知版
    
    核心改进：
    1. 每周检测市场环境
    2. 根据环境调整总仓位上限
    3. 熊市不开新仓，只持有已有仓位
    4. 牛市积极加仓优质标的
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.daily_values = []
        
        # 知识库
        self.early_signals = TenbaggerEarlySignals()
        self.identifier = TenbaggerIdentifier()
        self.regime_detector = AStockRegimeDetectorV2()
        
        # 当前市场环境
        self.current_regime = 'VOLATILE_RANGE'
        self.regime_position_limit = 0.40
        
        # JQData认证
        self._ensure_jqdata_auth()
        
        # 数据
        self.price_data = None
        self.fundamental_data = None
        
    def _ensure_jqdata_auth(self):
        """确保JQData认证"""
        try:
            import jqdatasdk as jq
            jq.auth('13327806797', 'Taorui888')
            logger.info("JQData认证成功")
        except Exception as e:
            logger.error(f"JQData认证失败: {e}")
            raise
    
    def _detect_market_regime(self, date: str) -> str:
        """检测市场环境
        
        使用简化版判断：基于指数均线和波动率
        """
        import jqdatasdk as jq
        
        try:
            # 获取沪深300近60日数据
            end_date = pd.to_datetime(date)
            start_date = end_date - timedelta(days=100)
            
            index_data = jq.get_price(
                '000300.XSHG',
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['close']
            )
            
            if index_data is None or len(index_data) < 40:
                return 'VOLATILE_RANGE'
            
            close = index_data['close']
            
            # 计算指标
            ma20 = close.rolling(20).mean().iloc[-1]
            ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20
            current = close.iloc[-1]
            
            # 计算动量
            momentum_20d = (current / close.iloc[-21] - 1) if len(close) > 21 else 0
            
            # 计算波动率
            returns = close.pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) if len(returns) > 5 else 0.2
            
            # 判断环境
            if current > ma20 > ma60 and momentum_20d > 0.05:
                if momentum_20d > 0.15:
                    regime = 'BULL_MID'
                elif volatility > 0.25:
                    regime = 'BULL_LATE'
                else:
                    regime = 'BULL_EARLY'
            elif current < ma20 < ma60 and momentum_20d < -0.05:
                if momentum_20d < -0.15 or volatility > 0.35:
                    regime = 'BEAR_PANIC'
                else:
                    regime = 'BEAR_GRINDING'
            elif momentum_20d > 0.03:
                regime = 'VOLATILE_UP'
            elif momentum_20d < -0.03:
                regime = 'VOLATILE_DOWN'
            else:
                regime = 'VOLATILE_RANGE'
            
            return regime
            
        except Exception as e:
            logger.warning(f"市场环境检测失败: {e}")
            return 'VOLATILE_RANGE'
    
    def _preload_data(self, start_date: str, end_date: str):
        """预加载数据"""
        import jqdatasdk as jq
        
        logger.info(f"预加载数据: {start_date} ~ {end_date}")
        
        self.trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 获取股票列表
        all_stocks = jq.get_all_securities(types=['stock'], date=start_date)
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST') &
            (all_stocks['start_date'] < pd.to_datetime(start_date) - timedelta(days=365))
        ].index.tolist()
        
        logger.info(f"候选股票数: {len(valid_stocks)}")
        
        # 获取价格数据
        self.price_data = jq.get_price(
            valid_stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            panel=False
        )
        
        if self.price_data is not None:
            self.price_data['date'] = pd.to_datetime(self.price_data['time']).dt.date
            logger.info(f"价格数据加载: {len(self.price_data)} 条")
    
    def _load_fundamental_data(self, stocks: List[str], date: str):
        """加载财务数据"""
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
            
            self.fundamental_data = jq.get_fundamentals(q, date=date)
            
            if self.fundamental_data is not None:
                self.fundamental_data = self.fundamental_data.set_index('code')
                
        except Exception as e:
            logger.warning(f"财务数据加载失败: {e}")
            self.fundamental_data = pd.DataFrame()
    
    def _screen_candidates(self, date: str) -> List[Dict]:
        """筛选候选股票"""
        if self.fundamental_data is None or len(self.fundamental_data) == 0:
            return []
        
        candidates = []
        
        for code, row in self.fundamental_data.iterrows():
            try:
                market_cap = row.get('market_cap', 0) or 0
                pe = row.get('pe_ratio', 0) or 0
                roe = row.get('roe', 0) or 0
                revenue_growth = (row.get('inc_revenue_year_on_year', 0) or 0) / 100
                profit_growth = (row.get('inc_net_profit_year_on_year', 0) or 0) / 100
                gross_margin = (row.get('gross_profit_margin', 0) or 0) / 100
                
                # 基础筛选
                if not (20 <= market_cap <= 500):
                    continue
                if profit_growth < 0.15:
                    continue
                if revenue_growth < 0.10:
                    continue
                
                # 识别阶段
                stage = self.identifier.identify_stage(
                    market_cap=market_cap,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    roe=roe / 100 if roe > 1 else roe
                )
                
                # 排除成熟期和衰退期
                if stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                    continue
                
                # 计算得分
                is_potential, score, _, details = self.identifier.is_potential_tenbagger(
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
                    'pe': pe,
                    'roe': roe,
                    'revenue_growth': revenue_growth,
                    'profit_growth': profit_growth,
                    'gross_margin': gross_margin,
                    'stage': stage.value,
                    'score': score,
                    'is_potential': is_potential,
                })
                
            except Exception:
                continue
        
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates
    
    def _calculate_entry_score(self, candidate: Dict) -> Tuple[float, str]:
        """计算进入得分"""
        score, details, advice = EarlyEntryAlgorithm.calculate_entry_score(
            stage=candidate['stage'].split('_')[0] if '_' in candidate['stage'] else candidate['stage'][:2],
            market_cap=candidate['market_cap'],
            revenue_growth=candidate['revenue_growth'],
            profit_growth=candidate['profit_growth'],
            prev_profit_growth=candidate['profit_growth'] * 0.8,
            mainline_score=70,
            research_report_count=5,
            institution_ratio=0.15,
            has_catalyst=candidate['profit_growth'] > 0.5,
            technical_breakout=False,
        )
        return score, advice
    
    def _get_position_limit(self, stage: str) -> float:
        """获取阶段仓位限制，同时考虑市场环境"""
        stage_key = stage.split('_')[0] if '_' in stage else stage[:2]
        base_limit = STAGE_POSITION_STRATEGY.get(stage_key, {}).get('max_position', 0.08)
        
        # 根据市场环境调整
        adjusted = base_limit * (self.regime_position_limit / 0.50)  # 以50%为基准
        return min(adjusted, base_limit)  # 不超过阶段上限
    
    def _execute_trades(self, date, candidates: List[Dict]):
        """执行交易"""
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
        
        # 卖出检查
        positions_to_sell = []
        for code, pos in list(self.positions.items()):
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    continue
                current_price = price_row['close'].values[0]
            except:
                continue
            
            return_rate = (current_price - pos['avg_cost']) / pos['avg_cost']
            
            should_sell = False
            sell_ratio = 0
            sell_reason = ""
            
            # 规则1：止损（根据市场环境调整）
            stop_loss = -0.15 if 'BULL' in self.current_regime else -0.10
            if return_rate < stop_loss:
                should_sell = True
                sell_ratio = 1.0
                sell_reason = f"止损{stop_loss*100:.0f}%"
            
            # 规则2：目标止盈
            elif return_rate >= 3.0:
                sell_ratio = 0.30
                sell_reason = "涨3倍-卖30%"
                should_sell = True
            elif return_rate >= 2.0:
                sell_ratio = 0.20
                sell_reason = "涨2倍-卖20%"
                should_sell = True
            elif return_rate >= 1.0:
                sell_ratio = 0.15
                sell_reason = "翻倍-卖15%"
                should_sell = True
            
            # 规则3：熊市强制减仓
            if 'BEAR' in self.current_regime and return_rate > 0.10:
                sell_ratio = max(sell_ratio, 0.50)
                sell_reason = "熊市-逢高减仓"
                should_sell = True
            
            if should_sell and sell_ratio > 0:
                positions_to_sell.append((code, sell_ratio, current_price, sell_reason))
        
        # 执行卖出
        for code, ratio, price, reason in positions_to_sell:
            pos = self.positions[code]
            shares_to_sell = int(pos['shares'] * ratio)
            if shares_to_sell > 0:
                sell_value = shares_to_sell * price
                self.capital += sell_value
                pos['shares'] -= shares_to_sell
                
                self.trades.append({
                    'date': date_str,
                    'code': code,
                    'action': 'SELL',
                    'shares': shares_to_sell,
                    'price': price,
                    'value': sell_value,
                    'reason': reason,
                })
                
                logger.debug(f"[{date_str}] 卖出 {code}: {shares_to_sell}股, 原因: {reason}")
                
                if pos['shares'] <= 0:
                    del self.positions[code]
        
        # 买入检查 - 熊市不开新仓
        if 'BEAR_PANIC' in self.current_regime:
            return  # 熊市恐慌期不买
        
        # 计算当前仓位
        total_position_value = sum(
            pos['shares'] * pos['avg_cost'] for pos in self.positions.values()
        )
        current_position_ratio = total_position_value / self.initial_capital
        
        # 仓位上限控制
        if current_position_ratio >= self.regime_position_limit:
            return
        
        available_capital = min(
            self.capital * 0.9,
            self.initial_capital * (self.regime_position_limit - current_position_ratio)
        )
        
        max_positions = 10
        if len(self.positions) >= max_positions:
            return
        
        # 筛选候选
        buy_candidates = []
        for c in candidates[:30]:
            entry_score, advice = self._calculate_entry_score(c)
            threshold = 60 if 'BULL' in self.current_regime else 70  # 牛市降低门槛
            if entry_score >= threshold and c['code'] not in self.positions:
                buy_candidates.append({
                    **c,
                    'entry_score': entry_score,
                    'advice': advice,
                })
        
        # 执行买入
        for c in buy_candidates[:3]:  # 每次最多买3只
            if len(self.positions) >= max_positions:
                break
            
            code = c['code']
            stage = c['stage']
            
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    continue
                price = price_row['close'].values[0]
            except:
                continue
            
            # 计算买入金额
            position_limit = self._get_position_limit(stage)
            target_value = self.initial_capital * position_limit
            actual_value = min(target_value, available_capital / 3)
            
            if actual_value < 10000:
                continue
            
            shares = int(actual_value / price / 100) * 100
            if shares <= 0:
                continue
            
            cost = shares * price
            if cost > self.capital:
                continue
            
            self.capital -= cost
            available_capital -= cost
            
            self.positions[code] = {
                'shares': shares,
                'avg_cost': price,
                'entry_date': date_str,
                'stage': stage,
                'entry_score': c['entry_score'],
            }
            
            self.trades.append({
                'date': date_str,
                'code': code,
                'action': 'BUY',
                'shares': shares,
                'price': price,
                'value': cost,
                'reason': f"S{c['entry_score']:.0f}-{self.current_regime}",
            })
            
            logger.debug(f"[{date_str}] 买入 {code}: {shares}股, 阶段:{stage}, 环境:{self.current_regime}")
    
    def _calculate_portfolio_value(self, date) -> float:
        """计算组合价值"""
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
        
        total_value = self.capital
        
        for code, pos in self.positions.items():
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    price = pos['avg_cost']
                else:
                    price = price_row['close'].values[0]
                
                total_value += pos['shares'] * price
            except:
                total_value += pos['shares'] * pos['avg_cost']
        
        return total_value
    
    def run_backtest(self, start_date: str, end_date: str) -> Dict:
        """运行回测"""
        logger.info(f"V8回测: {start_date} ~ {end_date}")
        
        self._preload_data(start_date, end_date)
        
        if self.price_data is None or len(self.price_data) == 0:
            return {"success": False, "error": "数据加载失败"}
        
        rebalance_interval = 60  # 季度调仓
        regime_check_interval = 5  # 每周检测市场环境
        last_rebalance = 0
        last_regime_check = 0
        
        for i, date in enumerate(self.trade_days):
            date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
            
            # 每周检测市场环境
            if i - last_regime_check >= regime_check_interval:
                self.current_regime = self._detect_market_regime(date_str)
                self.regime_position_limit = MARKET_REGIME_POSITION.get(self.current_regime, 0.40)
                last_regime_check = i
                
                if i % 50 == 0:
                    logger.info(f"[{date_str}] 市场环境: {self.current_regime}, 仓位上限: {self.regime_position_limit:.0%}")
            
            # 季度调仓
            if i - last_rebalance >= rebalance_interval or i == 0:
                valid_stocks = self.price_data['code'].unique().tolist()
                self._load_fundamental_data(valid_stocks[:500], date_str)
                candidates = self._screen_candidates(date_str)
                self._execute_trades(date, candidates)
                last_rebalance = i
            else:
                self._execute_trades(date, [])
            
            # 记录净值
            daily_value = self._calculate_portfolio_value(date)
            self.daily_values.append({
                'date': date_str,
                'value': daily_value,
                'positions': len(self.positions),
                'regime': self.current_regime,
            })
            
            if i % 50 == 0:
                logger.info(f"进度: {i+1}/{len(self.trade_days)}, 净值: {daily_value/self.initial_capital:.2%}")
        
        return self._calc_result()
    
    def _calc_result(self) -> Dict:
        """计算结果"""
        if not self.daily_values:
            return {"success": False, "error": "无交易数据"}
        
        df = pd.DataFrame(self.daily_values)
        df['return'] = df['value'] / self.initial_capital - 1
        
        final_value = df['value'].iloc[-1]
        total_return = (final_value / self.initial_capital - 1) * 100
        
        days = len(df)
        annual_return = ((final_value / self.initial_capital) ** (252 / days) - 1) * 100 if days > 0 else 0
        
        df['cummax'] = df['value'].cummax()
        df['drawdown'] = (df['cummax'] - df['value']) / df['cummax']
        max_drawdown = df['drawdown'].max() * 100
        
        df['daily_return'] = df['value'].pct_change()
        sharpe = df['daily_return'].mean() / df['daily_return'].std() * np.sqrt(252) if df['daily_return'].std() > 0 else 0
        
        # 按市场环境统计
        regime_stats = df.groupby('regime').agg({
            'value': ['count', 'first', 'last']
        }).round(2)
        
        result = {
            "success": True,
            "initial_capital": self.initial_capital,
            "final_value": final_value,
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
            "total_trades": len(self.trades),
            "final_positions": len(self.positions),
        }
        
        logger.info("=" * 60)
        logger.info(f"V8回测结果:")
        logger.info(f"  总收益率: {total_return:.2f}%")
        logger.info(f"  年化收益: {annual_return:.2f}%")
        logger.info(f"  最大回撤: {max_drawdown:.2f}%")
        logger.info(f"  夏普比率: {sharpe:.2f}")
        logger.info(f"  交易次数: {len(self.trades)}")
        logger.info("=" * 60)
        
        return result


def main():
    parser = argparse.ArgumentParser(description='十倍股核心策略V8回测')
    parser.add_argument('-p', '--period', type=str, default='1y',
                        help='回测周期: 1m/3m/6m/1y/2y/3y')
    parser.add_argument('--start', type=str, help='开始日期')
    parser.add_argument('--end', type=str, help='结束日期')
    args = parser.parse_args()
    
    end_date = args.end or '2024-12-20'
    
    period_days = {
        '1m': 30, '3m': 90, '6m': 180,
        '1y': 365, '2y': 730, '3y': 1095,
    }
    
    days = period_days.get(args.period, 365)
    start_date = args.start or (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days)).strftime('%Y-%m-%d')
    
    logger.info(f"十倍股核心策略V8 ({args.period})")
    
    strategy = TenbaggerCoreStrategyV8(initial_capital=1_000_000)
    result = strategy.run_backtest(start_date, end_date)
    
    if result['success']:
        print(f"\n{'='*60}")
        print(f"十倍股核心策略V8 结果 ({args.period})")
        print(f"{'='*60}")
        print(f"总收益率:   {result['total_return']:.2f}%")
        print(f"年化收益:   {result['annual_return']:.2f}%")
        print(f"最大回撤:   {result['max_drawdown']:.2f}%")
        print(f"夏普比率:   {result['sharpe_ratio']:.2f}")
        print(f"交易次数:   {result['total_trades']}")
        print(f"{'='*60}")


if __name__ == '__main__':
    main()

