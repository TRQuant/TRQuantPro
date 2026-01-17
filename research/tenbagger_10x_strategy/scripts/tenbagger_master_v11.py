#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Master Strategy V11 - 十倍股大师增强策略
==================================================

重新设计：大师知识库用于增强评分，而非风格切换

核心改进（吸取V10教训）:
1. 保持V9的十倍股识别系统为核心（不变）
2. 大师知识库作为"评分增强因子"
3. 根据股票特征自动匹配最适合的大师评分
4. 市场环境只用于仓位控制，不影响选股逻辑

大师评分增强方案:
- 消费类股票: +林园评分×20%
- 科技成长股: +葛卫东评分×20%
- 低估值股票: +逆向抄底评分×20%
- 高ROE股票: +段永平评分×20%

Author: TRQuant Team
Date: 2025-12-27
"""

import sys
import os
import argparse
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 导入知识库
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerIdentifier, TenbaggerStage, TenbaggerScorer, STAGE_POSITION_STRATEGY
)
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegimeDetectorV2, AStockRegime, ASTOCK_REGIME_STRATEGY
)
from research.tenbagger_10x_strategy.knowledge.investment_master_kb import (
    MasterStyle, MasterScorer, MasterStrategyIntegrator
)


class TenbaggerMasterV11:
    """十倍股大师增强策略V11
    
    核心理念（吸取V10教训）：
    - 保持十倍股识别系统为核心（V9成功因子）
    - 大师知识库作为评分增强因子，而非风格切换
    - 根据股票特征自动匹配最适合的大师评分
    - 市场环境只用于仓位控制
    """
    
    # 行业分类（简化）
    CONSUMER_SECTORS = ['白酒', '食品', '医药', '家电', '零售', '餐饮']
    TECH_SECTORS = ['AI', '芯片', '半导体', '软件', '电子', '通信', '计算机']
    
    def __init__(
        self,
        initial_capital: float = 1_000_000,
        max_position_per_stock: float = 0.10,
        max_total_position: float = 0.80,
        stop_loss_pct: float = 0.10,
        take_profit_pct: float = 0.30,
        rebalance_interval: int = 60,
        regime_check_interval: int = 5,
    ):
        self.initial_capital = initial_capital
        self.max_position_per_stock = max_position_per_stock
        self.max_total_position = max_total_position
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.rebalance_interval = rebalance_interval
        self.regime_check_interval = regime_check_interval
        
        # 核心组件
        self.tenbagger_identifier = TenbaggerIdentifier()
        self.regime_detector = AStockRegimeDetectorV2()
        self.master_scorer = MasterScorer()
        
        # 状态变量
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.positions = {}
        self.trade_history = []
        self.equity_curve = []
        
        # JQData认证
        self._ensure_jqdata_auth()
    
    def _ensure_jqdata_auth(self):
        """确保JQData认证"""
        try:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth('13327806797', 'Taorui888')
            print(f"✅ JQData认证成功")
        except Exception as e:
            print(f"⚠️ JQData认证失败: {e}")
    
    def _load_price_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """加载价格数据"""
        import jqdatasdk as jq
        
        # 获取股票池 - 扩大到800只
        all_stocks = jq.get_all_securities(types=['stock'], date=end_date)
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|\\*|退') &
            ~all_stocks.index.str.startswith('688')
        ].index.tolist()[:800]
        
        ext_start = (pd.to_datetime(start_date) - timedelta(days=180)).strftime('%Y-%m-%d')
        
        price_data = jq.get_price(
            valid_stocks,
            start_date=ext_start,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=True,
            fq='pre',
            panel=False
        )
        
        if 'time' in price_data.columns:
            price_data = price_data.rename(columns={'time': 'date'})
        if 'date' not in price_data.columns:
            price_data = price_data.reset_index()
        
        price_data['date'] = pd.to_datetime(price_data['date']).dt.strftime('%Y-%m-%d')
        
        print(f"✅ 加载价格数据: {len(valid_stocks)}只股票, {len(price_data)}条记录")
        return price_data
    
    def _load_index_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """加载指数数据"""
        import jqdatasdk as jq
        
        ext_start = (pd.to_datetime(start_date) - timedelta(days=180)).strftime('%Y-%m-%d')
        
        index_data = jq.get_price(
            '000001.XSHG',
            start_date=ext_start,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            skip_paused=False,
            fq=None
        )
        
        print(f"✅ 加载指数数据: {len(index_data)}条记录")
        return index_data
    
    def _load_fundamental_data(self, date: str) -> pd.DataFrame:
        """加载基本面数据"""
        import jqdatasdk as jq
        
        q = jq.query(
            jq.valuation.code,
            jq.valuation.market_cap,
            jq.valuation.pe_ratio,
            jq.valuation.pb_ratio,
            jq.indicator.roe,
            jq.indicator.gross_profit_margin,
            jq.indicator.net_profit_margin,
            jq.indicator.inc_revenue_year_on_year,
            jq.indicator.inc_net_profit_year_on_year,
        ).filter(
            jq.valuation.market_cap > 20,
            jq.valuation.market_cap < 500,
            jq.valuation.pe_ratio > 0,
            jq.valuation.pe_ratio < 100,
        )
        
        df = jq.get_fundamentals(q, date=date)
        df.columns = ['code', 'market_cap', 'pe', 'pb', 'roe', 'gross_margin',
                      'net_margin', 'revenue_growth', 'profit_growth']
        
        print(f"✅ 加载基本面数据: {len(df)}只股票")
        return df
    
    def _get_stock_industry(self, code: str) -> str:
        """获取股票行业（简化判断）"""
        import jqdatasdk as jq
        try:
            industry = jq.get_industry(code)
            if industry and code in industry:
                return industry[code].get('sw_l1', {}).get('industry_name', '其他')
        except:
            pass
        return '其他'
    
    def _detect_market_regime(self, index_data: pd.DataFrame) -> AStockRegime:
        """检测市场环境（与V9相同）"""
        if len(index_data) < 60:
            return AStockRegime.VOLATILE_RANGE
        
        recent = index_data.tail(60)
        close = recent['close'].values
        
        ma20 = np.mean(close[-20:])
        ma60 = np.mean(close)
        current_price = close[-1]
        
        change_20d = (close[-1] / close[-20] - 1) * 100
        change_60d = (close[-1] / close[0] - 1) * 100
        
        returns = np.diff(close) / close[:-1]
        volatility = np.std(returns) * np.sqrt(252) * 100
        
        trend_score = 0
        if current_price > ma20:
            trend_score += 30
        if current_price > ma60:
            trend_score += 20
        if change_20d > 5:
            trend_score += 25
        elif change_20d > 0:
            trend_score += 10
        elif change_20d < -5:
            trend_score -= 25
        else:
            trend_score -= 10
        
        if change_60d > 10:
            trend_score += 25
        elif change_60d < -10:
            trend_score -= 25
        
        if trend_score >= 50:
            if change_20d > 10:
                return AStockRegime.BULL_EARLY
            elif volatility > 25:
                return AStockRegime.BULL_LATE
            else:
                return AStockRegime.BULL_MID
        elif trend_score <= -50:
            if volatility > 30:
                return AStockRegime.BEAR_PANIC
            else:
                return AStockRegime.BEAR_GRINDING
        else:
            if change_20d > 3:
                return AStockRegime.VOLATILE_UP
            elif change_20d < -3:
                return AStockRegime.VOLATILE_DOWN
            else:
                return AStockRegime.VOLATILE_RANGE
    
    def _calculate_master_enhanced_score(
        self,
        stock_data: Dict,
        tb_score: float
    ) -> float:
        """计算大师增强评分
        
        核心改进：根据股票特征自动选择最适合的大师评分
        - 消费类: 林园评分
        - 科技成长: 葛卫东评分
        - 低估值: 逆向抄底评分
        - 高ROE: 长期价值评分
        """
        roe = stock_data.get('roe', 0)
        gross_margin = stock_data.get('gross_margin', 0)
        net_margin = stock_data.get('net_margin', 0)
        profit_growth = stock_data.get('profit_growth', 0)
        revenue_growth = stock_data.get('revenue_growth', 0)
        debt_ratio = stock_data.get('debt_ratio', 50)
        pe = stock_data.get('pe', 20)
        pb = stock_data.get('pb', 2)
        market_cap = stock_data.get('market_cap', 100)
        price_position = stock_data.get('price_position', 0.5)
        momentum_20d = stock_data.get('momentum_20d', 0)
        
        # 计算各种大师评分
        linyuan_score = self.master_scorer.calculate_linyuan_score(
            roe, gross_margin, net_margin, profit_growth, debt_ratio, pe,
            stock_data.get('is_consumer', False),
            stock_data.get('is_pharma', False)
        )
        
        contrarian_score = self.master_scorer.calculate_contrarian_score(
            price_position, pe, 30, 0.15, profit_growth
        )
        
        growth_score = self.master_scorer.calculate_growth_score(
            profit_growth, revenue_growth, market_cap, 5, momentum_20d,
            stock_data.get('is_tech', False)
        )
        
        value_score = self.master_scorer.calculate_value_score(
            pe, pb, 2, roe, debt_ratio, stock_data.get('is_soe', False)
        )
        
        # 根据股票特征选择最适合的大师评分
        master_weight = 0.0
        best_master_score = 0.0
        
        # 消费类高毛利 -> 林园
        if gross_margin > 50 or stock_data.get('is_consumer'):
            master_weight = 0.20
            best_master_score = linyuan_score
        
        # 高增长科技 -> 葛卫东
        elif profit_growth > 30 and stock_data.get('is_tech'):
            master_weight = 0.20
            best_master_score = growth_score
        
        # 低估值低位 -> 逆向抄底
        elif pe < 15 and price_position < 0.3:
            master_weight = 0.20
            best_master_score = contrarian_score
        
        # 高ROE稳定 -> 长期价值
        elif roe > 15:
            master_weight = 0.15
            best_master_score = value_score
        
        # 默认：取最高分加权
        else:
            master_weight = 0.10
            best_master_score = max(linyuan_score, contrarian_score, growth_score, value_score)
        
        # 十倍股评分为核心，大师评分为增强
        # 公式: 最终得分 = 十倍股得分×(1-权重) + 大师得分×权重
        enhanced_score = tb_score * (1 - master_weight) + best_master_score * master_weight
        
        return enhanced_score
    
    def _screen_candidates(
        self,
        fundamental_df: pd.DataFrame,
        price_df: pd.DataFrame,
        current_date: str,
        regime: AStockRegime
    ) -> List[Dict]:
        """筛选候选股票（V9核心逻辑 + 大师增强）"""
        candidates = []
        
        for _, row in fundamental_df.iterrows():
            code = row['code']
            
            # 基本面底线筛选（V9成功关键）
            profit_growth = row.get('profit_growth', 0) or 0
            revenue_growth = row.get('revenue_growth', 0) or 0
            roe = row.get('roe', 0) or 0
            market_cap = row.get('market_cap', 100) or 100
            
            # 严格基本面筛选（V9核心）
            if profit_growth < 15 or revenue_growth < 10:
                continue
            if roe < 8:
                continue
            if market_cap < 20 or market_cap > 500:
                continue
            
            # 获取价格数据
            stock_prices = price_df[price_df['code'] == code]
            if len(stock_prices) < 60:
                continue
            
            recent_prices = stock_prices[stock_prices['date'] <= current_date].tail(60)
            if len(recent_prices) < 20:
                continue
            
            close_prices = recent_prices['close'].values
            current_price = close_prices[-1]
            
            momentum_20d = (current_price / close_prices[-20] - 1) if len(close_prices) >= 20 else 0
            
            high_252 = close_prices.max()
            low_252 = close_prices.min()
            price_position = (current_price - low_252) / (high_252 - low_252) if high_252 != low_252 else 0.5
            
            # 构建股票数据
            stock_data = {
                'code': code,
                'roe': roe,
                'gross_margin': row.get('gross_margin', 0) or 0,
                'net_margin': row.get('net_margin', 0) or 0,
                'profit_growth': profit_growth,
                'revenue_growth': revenue_growth,
                'market_cap': market_cap,
                'pe': row.get('pe', 20) or 20,
                'pb': row.get('pb', 2) or 2,
                'debt_ratio': 50,
                'price_position': price_position,
                'momentum_20d': momentum_20d,
                'current_price': current_price,
                # 行业判断（简化）
                'is_consumer': False,
                'is_tech': False,
                'is_pharma': False,
                'is_soe': False,
            }
            
            # === 十倍股评分（V9核心）===
            is_tenbagger, tb_score, stage, details = self.tenbagger_identifier.is_potential_tenbagger(
                roe=stock_data['roe'],
                gross_margin=stock_data['gross_margin'],
                net_margin=stock_data['net_margin'],
                debt_ratio=stock_data['debt_ratio'],
                revenue_growth=stock_data['revenue_growth'],
                profit_growth=stock_data['profit_growth'],
                peg=stock_data['pe'] / max(stock_data['profit_growth'], 1) if stock_data['profit_growth'] > 0 else 10,
                pe=stock_data['pe'],
                market_cap=stock_data['market_cap'],
                momentum_20d=stock_data['momentum_20d'],
                volume_ratio=1.0,
                price_position=stock_data['price_position'],
            )
            
            # 排除成熟期和衰退期（V9核心）
            if stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                continue
            
            # === 大师增强评分 ===
            enhanced_score = self._calculate_master_enhanced_score(stock_data, tb_score)
            
            # 阈值筛选
            min_score = 50
            if regime in [AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING]:
                min_score = 55  # 熊市更严格
            
            if enhanced_score >= min_score:
                candidates.append({
                    'code': code,
                    'tb_score': tb_score,
                    'enhanced_score': enhanced_score,
                    'stage': stage,
                    'price': current_price,
                    'market_cap': market_cap,
                    'profit_growth': profit_growth,
                    'roe': roe,
                })
        
        # 按增强得分排序
        candidates.sort(key=lambda x: x['enhanced_score'], reverse=True)
        
        return candidates[:15]
    
    def _get_position_limit(
        self,
        regime: AStockRegime,
        stage: TenbaggerStage
    ) -> float:
        """获取仓位限制（V9逻辑）"""
        regime_config = ASTOCK_REGIME_STRATEGY.get(regime.name, {})
        base_position = regime_config.get('position', 0.50)
        
        stage_config = STAGE_POSITION_STRATEGY.get(stage.name, {})
        stage_multiplier = stage_config.get('position_pct', 0.10) / 0.10
        
        final_position = min(
            base_position * stage_multiplier,
            self.max_position_per_stock
        )
        
        return max(final_position, 0.05)
    
    def _execute_trades(
        self,
        candidates: List[Dict],
        current_date: str,
        capital: float,
        regime: AStockRegime
    ) -> Tuple[Dict, List]:
        """执行交易"""
        new_positions = {}
        trades = []
        
        if regime == AStockRegime.BEAR_PANIC:
            return {}, []
        
        available_capital = capital * self.max_total_position
        position_used = 0
        
        for candidate in candidates:
            if position_used >= available_capital:
                break
            
            code = candidate['code']
            price = candidate['price']
            stage = candidate['stage']
            
            position_limit = self._get_position_limit(regime, stage)
            target_value = capital * position_limit
            
            # 熊市额外过滤（V9核心）
            if regime in [AStockRegime.BEAR_GRINDING, AStockRegime.VOLATILE_DOWN]:
                if candidate['profit_growth'] < 20 or candidate['enhanced_score'] < 55:
                    continue
            
            if target_value + position_used <= available_capital:
                shares = int(target_value / price / 100) * 100
                if shares >= 100:
                    actual_value = shares * price
                    new_positions[code] = {
                        'shares': shares,
                        'cost': price,
                        'value': actual_value,
                        'stage': stage,
                    }
                    position_used += actual_value
                    
                    trades.append({
                        'date': current_date,
                        'code': code,
                        'action': 'BUY',
                        'shares': shares,
                        'price': price,
                        'value': actual_value,
                        'reason': f'增强评分{candidate["enhanced_score"]:.0f}',
                    })
        
        return new_positions, trades
    
    def _check_stop_loss_take_profit(
        self,
        positions: Dict,
        price_df: pd.DataFrame,
        current_date: str,
        regime: AStockRegime
    ) -> Tuple[Dict, List]:
        """检查止盈止损"""
        remaining_positions = {}
        trades = []
        
        regime_config = ASTOCK_REGIME_STRATEGY.get(regime.name, {})
        stop_loss = regime_config.get('stop_loss', self.stop_loss_pct)
        take_profit = regime_config.get('take_profit', self.take_profit_pct)
        
        for code, pos in positions.items():
            stock_prices = price_df[(price_df['code'] == code) & (price_df['date'] == current_date)]
            if len(stock_prices) == 0:
                remaining_positions[code] = pos
                continue
            
            current_price = stock_prices.iloc[0]['close']
            cost = pos['cost']
            change = (current_price - cost) / cost
            
            if change <= -stop_loss:
                trades.append({
                    'date': current_date,
                    'code': code,
                    'action': 'SELL',
                    'shares': pos['shares'],
                    'price': current_price,
                    'value': pos['shares'] * current_price,
                    'reason': f'止损({change*100:.1f}%)',
                })
            elif change >= take_profit:
                trades.append({
                    'date': current_date,
                    'code': code,
                    'action': 'SELL',
                    'shares': pos['shares'],
                    'price': current_price,
                    'value': pos['shares'] * current_price,
                    'reason': f'止盈({change*100:.1f}%)',
                })
            else:
                remaining_positions[code] = pos
                remaining_positions[code]['current_price'] = current_price
        
        return remaining_positions, trades
    
    def run_backtest(self, start_date: str, end_date: str) -> Dict:
        """运行回测"""
        import jqdatasdk as jq
        
        print(f"\n{'='*60}")
        print(f"🚀 十倍股大师增强策略V11 回测")
        print(f"📅 周期: {start_date} -> {end_date}")
        print(f"💰 初始资金: {self.initial_capital:,.0f}")
        print(f"{'='*60}")
        
        self.price_data = self._load_price_data(start_date, end_date)
        self.index_data = self._load_index_data(start_date, end_date)
        self.fundamental_data = self._load_fundamental_data(start_date)
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        capital = self.initial_capital
        self.positions = {}
        self.trade_history = []
        self.equity_curve = []
        
        days_since_rebalance = 0
        days_since_regime_check = 0
        
        print(f"\n📊 开始回测，共{len(trade_days)}个交易日...")
        
        for i, date in enumerate(trade_days):
            date_str = str(date)
            
            # 每5天检查市场环境
            days_since_regime_check += 1
            if days_since_regime_check >= self.regime_check_interval:
                idx_to_date = self.index_data[self.index_data.index <= date_str]
                if len(idx_to_date) >= 60:
                    new_regime = self._detect_market_regime(idx_to_date)
                    if new_regime != self.current_regime:
                        print(f"[{date_str}] 市场环境: {self.current_regime.name} -> {new_regime.name}")
                        self.current_regime = new_regime
                days_since_regime_check = 0
            
            # 每60天调仓
            days_since_rebalance += 1
            if days_since_rebalance >= self.rebalance_interval or i == 0:
                # 清空旧仓位
                for code, pos in self.positions.items():
                    stock_prices = self.price_data[
                        (self.price_data['code'] == code) &
                        (self.price_data['date'] == date_str)
                    ]
                    if len(stock_prices) > 0:
                        sell_price = stock_prices.iloc[0]['close']
                        capital += pos['shares'] * sell_price
                        self.trade_history.append({
                            'date': date_str,
                            'code': code,
                            'action': 'SELL',
                            'shares': pos['shares'],
                            'price': sell_price,
                            'value': pos['shares'] * sell_price,
                            'reason': '调仓',
                        })
                
                self.positions = {}
                
                # 更新基本面数据
                self.fundamental_data = self._load_fundamental_data(date_str)
                
                # 筛选候选
                candidates = self._screen_candidates(
                    self.fundamental_data,
                    self.price_data,
                    date_str,
                    self.current_regime
                )
                
                if candidates:
                    print(f"[{date_str}] 筛选出{len(candidates)}只候选，环境:{self.current_regime.name}")
                    
                    self.positions, trades = self._execute_trades(
                        candidates, date_str, capital, self.current_regime
                    )
                    self.trade_history.extend(trades)
                    
                    for pos in self.positions.values():
                        capital -= pos['value']
                
                days_since_rebalance = 0
            
            else:
                # 非调仓日: 只执行止盈止损
                self.positions, trades = self._check_stop_loss_take_profit(
                    self.positions, self.price_data, date_str, self.current_regime
                )
                self.trade_history.extend(trades)
                
                for trade in trades:
                    if trade['action'] == 'SELL':
                        capital += trade['value']
            
            # 计算当日净值
            position_value = 0
            for code, pos in self.positions.items():
                stock_prices = self.price_data[
                    (self.price_data['code'] == code) &
                    (self.price_data['date'] == date_str)
                ]
                if len(stock_prices) > 0:
                    position_value += pos['shares'] * stock_prices.iloc[0]['close']
            
            total_value = capital + position_value
            self.equity_curve.append({
                'date': date_str,
                'capital': capital,
                'position_value': position_value,
                'total_value': total_value,
                'nav': total_value / self.initial_capital,
            })
        
        return self._calc_result()
    
    def _calc_result(self) -> Dict:
        """计算回测结果"""
        if not self.equity_curve:
            return {'total_return': 0, 'annual_return': 0, 'max_drawdown': 0, 'sharpe': 0}
        
        nav_series = pd.Series([e['nav'] for e in self.equity_curve])
        
        total_return = (nav_series.iloc[-1] - 1) * 100
        
        days = len(self.equity_curve)
        annual_return = ((nav_series.iloc[-1]) ** (252 / days) - 1) * 100 if days > 0 else 0
        
        rolling_max = nav_series.cummax()
        drawdown = (nav_series - rolling_max) / rolling_max
        max_drawdown = abs(drawdown.min()) * 100
        
        returns = nav_series.pct_change().dropna()
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        num_trades = len(self.trade_history)
        buy_trades = len([t for t in self.trade_history if t['action'] == 'BUY'])
        sell_trades = len([t for t in self.trade_history if t['action'] == 'SELL'])
        
        result = {
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe': sharpe,
            'num_trades': num_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'final_nav': nav_series.iloc[-1],
            'final_value': self.equity_curve[-1]['total_value'],
        }
        
        print(f"\n{'='*60}")
        print("📊 回测结果")
        print(f"{'='*60}")
        print(f"总收益率: {total_return:+.2f}%")
        print(f"年化收益: {annual_return:+.2f}%")
        print(f"最大回撤: {max_drawdown:.2f}%")
        print(f"夏普比率: {sharpe:.2f}")
        print(f"交易次数: {num_trades} (买入:{buy_trades}, 卖出:{sell_trades})")
        print(f"最终净值: {nav_series.iloc[-1]:.4f}")
        print(f"最终资产: {self.equity_curve[-1]['total_value']:,.0f}")
        print(f"{'='*60}")
        
        return result


def main():
    parser = argparse.ArgumentParser(description='十倍股大师增强策略V11')
    parser.add_argument('-p', '--period', type=str, default='3m',
                        choices=['1m', '3m', '6m', '1y', '2y', '3y'],
                        help='回测周期')
    args = parser.parse_args()
    
    end_date = '2024-12-31'
    period_mapping = {
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        '2y': 730,
        '3y': 1095,
    }
    days = period_mapping.get(args.period, 90)
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days)).strftime('%Y-%m-%d')
    
    strategy = TenbaggerMasterV11()
    result = strategy.run_backtest(start_date, end_date)
    
    return result


if __name__ == '__main__':
    main()







































