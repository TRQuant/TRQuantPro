#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Master Strategy V10 - 十倍股大师融合策略
==================================================

基于投资大师知识库，整合十倍股识别系统与大师策略

策略特点:
1. 林园风格: 垄断消费+医药，长期持有
2. 段永平风格: 买公司而非股票，10年尺度
3. 陈发树风格: 逆向抄底行业龙头
4. 葛卫东风格: 科技成长趋势
5. 动态环境适配: 根据市场环境选择合适的大师风格

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
    MasterStyle, MasterScorer, MasterStrategyIntegrator, MasterSelectionRules
)


class TenbaggerMasterV10:
    """十倍股大师融合策略V10
    
    核心改进:
    1. 整合10位投资大师的选股智慧
    2. 根据市场环境动态选择大师风格
    3. 综合十倍股早期识别 + 大师评分
    4. 更精细的仓位控制和风控
    """
    
    def __init__(
        self,
        initial_capital: float = 1_000_000,
        max_position_per_stock: float = 0.15,
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
        self.master_integrator = MasterStrategyIntegrator()
        self.master_scorer = MasterScorer()
        
        # 状态变量
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.current_master_style = MasterStyle.DIVERSIFIED_VALUE
        self.positions = {}
        self.trade_history = []
        self.equity_curve = []
        
        # 新增：风格切换控制
        self.style_cooldown = 20  # 风格切换冷却期（天）
        self.days_since_style_change = 0
        self.last_regime_category = "VOLATILE"  # 上次环境大类：BULL/BEAR/VOLATILE
        
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
        
        # 获取股票池
        all_stocks = jq.get_all_securities(types=['stock'], date=end_date)
        # 过滤ST和科创板
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|\\*|退') &
            ~all_stocks.index.str.startswith('688')
        ].index.tolist()[:500]  # 限制500只
        
        # 扩展起始日期以获取足够历史数据
        ext_start = (pd.to_datetime(start_date) - timedelta(days=180)).strftime('%Y-%m-%d')
        
        price_data = jq.get_price(
            valid_stocks,
            start_date=ext_start,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=True,
            fq='pre',
            panel=False  # 返回DataFrame而非Panel
        )
        
        # 确保有date和code列
        if 'time' in price_data.columns:
            price_data = price_data.rename(columns={'time': 'date'})
        if 'date' not in price_data.columns:
            price_data = price_data.reset_index()
        
        # 确保date是字符串格式
        price_data['date'] = pd.to_datetime(price_data['date']).dt.strftime('%Y-%m-%d')
        
        print(f"✅ 加载价格数据: {len(valid_stocks)}只股票, {len(price_data)}条记录")
        print(f"   列名: {list(price_data.columns)}")
        return price_data
    
    def _load_index_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """加载指数数据"""
        import jqdatasdk as jq
        
        ext_start = (pd.to_datetime(start_date) - timedelta(days=180)).strftime('%Y-%m-%d')
        
        index_data = jq.get_price(
            '000001.XSHG',  # 上证指数
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
        
        # 重命名列
        df.columns = ['code', 'market_cap', 'pe', 'pb', 'roe', 'gross_margin',
                      'net_margin', 'revenue_growth', 'profit_growth']
        
        print(f"✅ 加载基本面数据: {len(df)}只股票")
        return df
    
    def _detect_market_regime(self, index_data: pd.DataFrame) -> AStockRegime:
        """检测市场环境"""
        if len(index_data) < 60:
            return AStockRegime.VOLATILE_RANGE
        
        # 使用最近60天数据
        recent = index_data.tail(60)
        close = recent['close'].values
        
        # 计算技术指标
        ma20 = np.mean(close[-20:])
        ma60 = np.mean(close)
        current_price = close[-1]
        
        # 20日涨幅
        change_20d = (close[-1] / close[-20] - 1) * 100
        # 60日涨幅
        change_60d = (close[-1] / close[0] - 1) * 100
        
        # 波动率
        returns = np.diff(close) / close[:-1]
        volatility = np.std(returns) * np.sqrt(252) * 100
        
        # 趋势得分
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
        
        # 判断市场环境
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
    
    def _get_regime_category(self, regime: AStockRegime) -> str:
        """获取市场环境大类"""
        if regime in [AStockRegime.BULL_EARLY, AStockRegime.BULL_MID, AStockRegime.BULL_LATE]:
            return "BULL"
        elif regime in [AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING]:
            return "BEAR"
        else:
            return "VOLATILE"
    
    def _select_master_style(self, regime: AStockRegime, force: bool = False) -> MasterStyle:
        """根据市场环境选择大师风格
        
        优化：只在环境大类变化时切换风格，避免频繁切换
        """
        new_category = self._get_regime_category(regime)
        
        # 如果冷却期内且不是强制切换，保持当前风格
        if not force and self.days_since_style_change < self.style_cooldown:
            return self.current_master_style
        
        # 如果环境大类没变，保持当前风格
        if new_category == self.last_regime_category and not force:
            return self.current_master_style
        
        # 环境大类变化，选择新风格
        self.last_regime_category = new_category
        
        # 根据大类选择核心风格（简化，更稳定）
        style_mapping = {
            "BULL": MasterStyle.GROWTH_MOMENTUM,     # 牛市：成长趋势
            "BEAR": MasterStyle.DIVERSIFIED_VALUE,  # 熊市：分散价值（防守）
            "VOLATILE": MasterStyle.CONTRARIAN,     # 震荡：逆向抄底
        }
        
        return style_mapping.get(new_category, MasterStyle.DIVERSIFIED_VALUE)
    
    def _calculate_master_score(
        self, 
        stock_data: Dict, 
        style: MasterStyle
    ) -> float:
        """计算大师风格得分"""
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
        dividend_yield = stock_data.get('dividend_yield', 0)
        
        if style == MasterStyle.LONG_TERM_VALUE:
            # 林园风格评分
            return self.master_scorer.calculate_linyuan_score(
                roe, gross_margin, net_margin, profit_growth, debt_ratio, pe,
                stock_data.get('is_consumer', False),
                stock_data.get('is_pharma', False)
            )
        elif style == MasterStyle.CONTRARIAN:
            # 逆向抄底评分
            return self.master_scorer.calculate_contrarian_score(
                price_position, pe, 30, 0.15, profit_growth
            )
        elif style == MasterStyle.GROWTH_MOMENTUM:
            # 成长趋势评分
            return self.master_scorer.calculate_growth_score(
                profit_growth, revenue_growth, market_cap, 5, momentum_20d,
                stock_data.get('is_tech', False)
            )
        else:
            # 分散价值评分
            return self.master_scorer.calculate_value_score(
                pe, pb, dividend_yield, roe, debt_ratio,
                stock_data.get('is_soe', False)
            )
    
    def _screen_candidates(
        self,
        fundamental_df: pd.DataFrame,
        price_df: pd.DataFrame,
        current_date: str,
        style: MasterStyle
    ) -> List[Dict]:
        """筛选候选股票
        
        结合十倍股识别 + 大师风格筛选
        """
        candidates = []
        
        for _, row in fundamental_df.iterrows():
            code = row['code']
            
            # 获取价格数据
            stock_prices = price_df[price_df['code'] == code]
            if len(stock_prices) < 60:
                continue
            
            recent_prices = stock_prices[stock_prices['date'] <= current_date].tail(60)
            if len(recent_prices) < 20:
                continue
            
            # 计算技术指标
            close_prices = recent_prices['close'].values
            current_price = close_prices[-1]
            
            # 动量
            momentum_20d = (current_price / close_prices[-20] - 1) if len(close_prices) >= 20 else 0
            
            # 价格位置 (0-1)
            high_252 = close_prices.max()
            low_252 = close_prices.min()
            price_position = (current_price - low_252) / (high_252 - low_252) if high_252 != low_252 else 0.5
            
            # 构建股票数据
            stock_data = {
                'code': code,
                'roe': row.get('roe', 0) or 0,
                'gross_margin': row.get('gross_margin', 0) or 0,
                'net_margin': row.get('net_margin', 0) or 0,
                'profit_growth': row.get('profit_growth', 0) or 0,
                'revenue_growth': row.get('revenue_growth', 0) or 0,
                'market_cap': row.get('market_cap', 100) or 100,
                'pe': row.get('pe', 20) or 20,
                'pb': row.get('pb', 2) or 2,
                'debt_ratio': 50,  # 默认
                'price_position': price_position,
                'momentum_20d': momentum_20d,
                'dividend_yield': 2,  # 默认
                'current_price': current_price,
            }
            
            # === 十倍股评分 ===
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
            
            # 排除成熟期和衰退期
            if stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                continue
            
            # === 大师风格评分 ===
            master_score = self._calculate_master_score(stock_data, style)
            
            # === 综合评分 ===
            # 十倍股权重70% + 大师评分权重30% (十倍股为核心)
            combined_score = tb_score * 0.70 + master_score * 0.30
            
            # 根据市场环境和风格设置阈值（平衡精选与覆盖）
            min_score = 50  # 适中阈值
            
            # 基本面底线要求
            if stock_data['profit_growth'] < 10 or stock_data['revenue_growth'] < 5:
                continue
            
            if stock_data['roe'] < 5:
                continue
            
            # 风格特定要求
            if style == MasterStyle.GROWTH_MOMENTUM:
                min_score = 55
                if stock_data['profit_growth'] < 20:
                    continue
            elif style == MasterStyle.LONG_TERM_VALUE:
                if stock_data['gross_margin'] < 30:
                    continue
            elif style == MasterStyle.CONTRARIAN:
                # 逆向要求价格位置较低
                if stock_data['price_position'] > 0.6:
                    continue
            
            if combined_score >= min_score:
                candidates.append({
                    'code': code,
                    'tb_score': tb_score,
                    'master_score': master_score,
                    'combined_score': combined_score,
                    'stage': stage,
                    'style': style,
                    'price': current_price,
                    'market_cap': stock_data['market_cap'],
                    'profit_growth': stock_data['profit_growth'],
                    'roe': stock_data['roe'],
                })
        
        # 按综合得分排序
        candidates.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return candidates[:20]  # 返回前20只
    
    def _get_position_limit(
        self, 
        regime: AStockRegime, 
        stage: TenbaggerStage,
        style: MasterStyle
    ) -> float:
        """获取仓位限制"""
        # 基础仓位来自市场环境
        regime_config = ASTOCK_REGIME_STRATEGY.get(regime.name, {})
        base_position = regime_config.get('position', 0.50)
        
        # 阶段调整
        stage_config = STAGE_POSITION_STRATEGY.get(stage.name, {})
        stage_multiplier = stage_config.get('position_pct', 0.10) / 0.10
        
        # 风格调整
        style_position = self.master_integrator.get_position_limit(regime.name, style)
        
        # 综合计算
        final_position = min(
            base_position * stage_multiplier,
            style_position,
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
        
        # 熊市恐慌不买入
        if regime == AStockRegime.BEAR_PANIC:
            return {}, []
        
        # 计算可用资金
        available_capital = capital * self.max_total_position
        position_used = 0
        
        for candidate in candidates:
            if position_used >= available_capital:
                break
            
            code = candidate['code']
            price = candidate['price']
            stage = candidate['stage']
            style = candidate['style']
            
            # 获取仓位限制
            position_limit = self._get_position_limit(regime, stage, style)
            target_value = capital * position_limit
            
            # 熊市额外过滤
            if regime in [AStockRegime.BEAR_GRINDING, AStockRegime.VOLATILE_DOWN]:
                if candidate['profit_growth'] < 20 or candidate['combined_score'] < 55:
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
                        'style': style,
                    }
                    position_used += actual_value
                    
                    trades.append({
                        'date': current_date,
                        'code': code,
                        'action': 'BUY',
                        'shares': shares,
                        'price': price,
                        'value': actual_value,
                        'reason': f'{style.value}风格-{stage.name}阶段',
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
        
        # 根据市场环境调整止损/止盈参数
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
                # 止损
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
                # 止盈
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
        print(f"🚀 十倍股大师融合策略V10 回测")
        print(f"📅 周期: {start_date} -> {end_date}")
        print(f"💰 初始资金: {self.initial_capital:,.0f}")
        print(f"{'='*60}")
        
        # 加载数据
        self.price_data = self._load_price_data(start_date, end_date)
        self.index_data = self._load_index_data(start_date, end_date)
        self.fundamental_data = self._load_fundamental_data(start_date)
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 初始化
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
            self.days_since_style_change += 1
            
            if days_since_regime_check >= self.regime_check_interval:
                idx_to_date = self.index_data[self.index_data.index <= date_str]
                if len(idx_to_date) >= 60:
                    new_regime = self._detect_market_regime(idx_to_date)
                    old_category = self._get_regime_category(self.current_regime)
                    new_category = self._get_regime_category(new_regime)
                    
                    if new_regime != self.current_regime:
                        self.current_regime = new_regime
                        
                        # 只在大类变化时切换风格
                        if old_category != new_category and self.days_since_style_change >= self.style_cooldown:
                            old_style = self.current_master_style
                            self.current_master_style = self._select_master_style(new_regime, force=True)
                            if old_style != self.current_master_style:
                                print(f"[{date_str}] 环境大类变化: {old_category} -> {new_category}")
                                print(f"[{date_str}] 切换大师风格: {old_style.value} -> {self.current_master_style.value}")
                                self.days_since_style_change = 0
                
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
                    self.current_master_style
                )
                
                if candidates:
                    print(f"[{date_str}] 筛选出{len(candidates)}只候选，环境:{self.current_regime.name}, 风格:{self.current_master_style.value}")
                    
                    # 执行买入
                    self.positions, trades = self._execute_trades(
                        candidates, date_str, capital, self.current_regime
                    )
                    self.trade_history.extend(trades)
                    
                    # 更新资金
                    for pos in self.positions.values():
                        capital -= pos['value']
                
                days_since_rebalance = 0
            
            else:
                # 非调仓日: 只执行止盈止损
                self.positions, trades = self._check_stop_loss_take_profit(
                    self.positions, self.price_data, date_str, self.current_regime
                )
                self.trade_history.extend(trades)
                
                # 更新资金
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
        
        # 计算结果
        return self._calc_result()
    
    def _calc_result(self) -> Dict:
        """计算回测结果"""
        if not self.equity_curve:
            return {'total_return': 0, 'annual_return': 0, 'max_drawdown': 0, 'sharpe': 0}
        
        nav_series = pd.Series([e['nav'] for e in self.equity_curve])
        dates = [e['date'] for e in self.equity_curve]
        
        # 总收益
        total_return = (nav_series.iloc[-1] - 1) * 100
        
        # 年化收益
        days = len(self.equity_curve)
        annual_return = ((nav_series.iloc[-1]) ** (252 / days) - 1) * 100 if days > 0 else 0
        
        # 最大回撤
        rolling_max = nav_series.cummax()
        drawdown = (nav_series - rolling_max) / rolling_max
        max_drawdown = abs(drawdown.min()) * 100
        
        # 夏普比率
        returns = nav_series.pct_change().dropna()
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        # 交易统计
        num_trades = len(self.trade_history)
        buy_trades = len([t for t in self.trade_history if t['action'] == 'BUY'])
        sell_trades = len([t for t in self.trade_history if t['action'] == 'SELL'])
        
        # 环境统计
        regime_counts = {}
        for ec in self.equity_curve:
            regime = self.current_regime.name
            regime_counts[regime] = regime_counts.get(regime, 0) + 1
        
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
            'regime_counts': regime_counts,
        }
        
        # 打印结果
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
    parser = argparse.ArgumentParser(description='十倍股大师融合策略V10')
    parser.add_argument('-p', '--period', type=str, default='3m',
                        choices=['1m', '3m', '6m', '1y', '2y', '3y'],
                        help='回测周期')
    args = parser.parse_args()
    
    # 计算日期范围
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
    
    # 运行策略
    strategy = TenbaggerMasterV10()
    result = strategy.run_backtest(start_date, end_date)
    
    return result


if __name__ == '__main__':
    main()

