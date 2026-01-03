#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股多因子策略 - 基于历史特征挖掘
====================================

基于历史10倍股特征构建的多因子选股策略

核心因子（权重基于历史10倍股特征分析）:
1. 成长因子 (30%): 营收增长率、利润增长率
2. 质量因子 (25%): ROE、利润率
3. 估值因子 (15%): PE、PB
4. 动量因子 (15%): 20日/60日动量
5. 规模因子 (10%): 市值（偏好中小市值）
6. 技术因子 (5%): 均线多头、新高

代码位置: scripts/tenbagger_multifactor_strategy.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 策略配置
# ============================================================

class StrategyConfig:
    def __init__(self):
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_cash = 1000000.0
        self.benchmark = "000300.XSHG"
        self.commission_rate = 0.0003
        self.stamp_tax = 0.001
        self.slippage = 0.002
        
        # 持仓参数
        self.max_holdings = 10           # 分散持仓
        self.single_stock_max = 0.15     # 单票15%
        self.stop_loss = -0.10           # 止损10%
        self.take_profit = 0.80          # 止盈80%
        self.trailing_stop = 0.15        # 移动止损
        self.rebalance_days = 10         # 调仓频率
        
        # 因子权重（基于历史10倍股特征分析）
        self.factor_weights = {
            'growth': 0.30,      # 成长因子
            'quality': 0.25,     # 质量因子
            'value': 0.15,       # 估值因子
            'momentum': 0.15,    # 动量因子
            'size': 0.10,        # 规模因子
            'technical': 0.05,   # 技术因子
        }
        
        # 筛选阈值（基于历史10倍股特征）
        self.thresholds = {
            'min_market_cap': 20,    # 最小市值20亿
            'max_market_cap': 500,   # 最大市值500亿
            'min_roe': 5,            # ROE > 5%
            'min_revenue_growth': 10,# 营收增长 > 10%
            'max_pe': 100,           # PE < 100
            'min_volume': 3000000,   # 日成交量 > 300万股
        }

# ============================================================
# 多因子计算器
# ============================================================

class MultifactorCalculator:
    """多因子计算器"""
    
    def __init__(self, config: StrategyConfig):
        self.config = config
        self.fundamentals_cache = {}
        self.price_cache = {}
    
    def calculate_growth_score(self, fundamentals: dict) -> float:
        """计算成长因子得分"""
        score = 50.0
        
        # 营收增长率
        revenue_growth = fundamentals.get('revenue_growth', 0)
        if revenue_growth:
            if revenue_growth > 50:
                score += 25
            elif revenue_growth > 30:
                score += 20
            elif revenue_growth > 15:
                score += 10
            elif revenue_growth > 0:
                score += 5
        
        # 利润增长率
        profit_growth = fundamentals.get('profit_growth', 0)
        if profit_growth:
            if profit_growth > 50:
                score += 25
            elif profit_growth > 30:
                score += 20
            elif profit_growth > 15:
                score += 10
            elif profit_growth > 0:
                score += 5
        
        return min(score, 100)
    
    def calculate_quality_score(self, fundamentals: dict) -> float:
        """计算质量因子得分"""
        score = 50.0
        
        # ROE
        roe = fundamentals.get('roe', 0)
        if roe:
            if roe > 20:
                score += 30
            elif roe > 15:
                score += 25
            elif roe > 10:
                score += 15
            elif roe > 5:
                score += 5
        
        # ROA
        roa = fundamentals.get('roa', 0)
        if roa:
            if roa > 10:
                score += 20
            elif roa > 5:
                score += 10
        
        return min(score, 100)
    
    def calculate_value_score(self, fundamentals: dict) -> float:
        """计算估值因子得分（适度估值）"""
        score = 50.0
        
        # PE（10倍股特征：PE中位数30倍左右）
        pe = fundamentals.get('pe_ratio', 0)
        if pe and pe > 0:
            if 15 <= pe <= 35:
                score += 25  # 合理区间
            elif 10 <= pe < 15 or 35 < pe <= 50:
                score += 15
            elif pe < 10:
                score += 5   # 过低可能有问题
            elif pe > 50:
                score -= 10
        
        # PB
        pb = fundamentals.get('pb_ratio', 0)
        if pb and pb > 0:
            if 2 <= pb <= 6:
                score += 20
            elif 1 <= pb < 2 or 6 < pb <= 10:
                score += 10
        
        return max(min(score, 100), 0)
    
    def calculate_momentum_score(self, price_data: dict) -> float:
        """计算动量因子得分"""
        score = 50.0
        
        # 20日动量
        m20 = price_data.get('momentum_20d', 0)
        if m20:
            if m20 > 30:
                score += 20
            elif m20 > 15:
                score += 15
            elif m20 > 5:
                score += 10
            elif m20 < -10:
                score -= 15
        
        # 60日动量
        m60 = price_data.get('momentum_60d', 0)
        if m60:
            if m60 > 50:
                score += 15
            elif m60 > 25:
                score += 10
            elif m60 > 10:
                score += 5
        
        # 5日动量（短期）
        m5 = price_data.get('momentum_5d', 0)
        if m5:
            if m5 > 10:
                score += 10
            elif m5 > 5:
                score += 5
        
        return max(min(score, 100), 0)
    
    def calculate_size_score(self, fundamentals: dict) -> float:
        """计算规模因子得分（偏好中小市值）"""
        score = 50.0
        
        market_cap = fundamentals.get('market_cap', 0)
        if market_cap:
            if 50 <= market_cap <= 200:
                score += 30  # 最佳区间：50-200亿
            elif 30 <= market_cap < 50 or 200 < market_cap <= 300:
                score += 20
            elif 20 <= market_cap < 30 or 300 < market_cap <= 500:
                score += 10
            elif market_cap > 500:
                score -= 10  # 大市值难翻倍
        
        return max(min(score, 100), 0)
    
    def calculate_technical_score(self, price_data: dict) -> float:
        """计算技术因子得分"""
        score = 50.0
        
        # 均线多头排列
        if price_data.get('ma_trend', 0) == 1:
            score += 25
        
        # 创新高
        if price_data.get('is_new_high', 0) == 1:
            score += 20
        
        # 成交量放大
        vol_ratio = price_data.get('volume_ratio', 1)
        if vol_ratio:
            if vol_ratio > 2:
                score += 15
            elif vol_ratio > 1.5:
                score += 10
        
        return min(score, 100)
    
    def calculate_composite_score(self, fundamentals: dict, price_data: dict) -> float:
        """计算综合得分"""
        weights = self.config.factor_weights
        
        growth = self.calculate_growth_score(fundamentals)
        quality = self.calculate_quality_score(fundamentals)
        value = self.calculate_value_score(fundamentals)
        momentum = self.calculate_momentum_score(price_data)
        size = self.calculate_size_score(fundamentals)
        technical = self.calculate_technical_score(price_data)
        
        composite = (
            growth * weights['growth'] +
            quality * weights['quality'] +
            value * weights['value'] +
            momentum * weights['momentum'] +
            size * weights['size'] +
            technical * weights['technical']
        )
        
        return composite

# ============================================================
# 多因子策略引擎
# ============================================================

class MultifactorBacktest:
    def __init__(self, config: StrategyConfig):
        self.config = config
        self.calculator = MultifactorCalculator(config)
        self.cash = config.initial_cash
        self.positions = {}
        self.trade_history = []
        self.equity_history = []
        self.daily_returns = []
        self.dates = []
        self.price_cache = {}
        self.fundamentals_cache = {}
        self.all_stocks = []
        self.trade_days = []
    
    def authenticate(self) -> bool:
        try:
            config_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    password = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                password = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, password)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def preload_data(self):
        """预加载数据"""
        logger.info("📥 预加载数据...")
        
        self.trade_days = [str(d) for d in jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )]
        logger.info(f"   交易日: {len(self.trade_days)}天")
        
        # 获取中证500 + 创业板精选
        self.all_stocks = jq.get_index_stocks('000905.XSHG')  # 中证500
        self.all_stocks += jq.get_index_stocks('399006.XSHE')[:100]  # 创业板前100
        self.all_stocks = list(set(self.all_stocks))
        logger.info(f"   股票池: {len(self.all_stocks)}只")
        
        # 批量获取价格数据
        logger.info("   获取价格数据...")
        try:
            price_df = jq.get_price(
                self.all_stocks,
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                panel=False,
                skip_paused=True
            )
            
            if price_df is not None and not price_df.empty:
                for stock in self.all_stocks:
                    stock_data = price_df[price_df['code'] == stock].copy()
                    if not stock_data.empty and len(stock_data) > 60:
                        stock_data.set_index('time', inplace=True)
                        self.price_cache[stock] = stock_data
            
            logger.info(f"   价格数据: {len(self.price_cache)}只")
        except Exception as e:
            logger.error(f"   价格数据获取失败: {e}")
        
        logger.info("✅ 数据预加载完成")
    
    def get_price(self, stock: str, trade_date: str) -> dict:
        if stock not in self.price_cache:
            return None
        
        df = self.price_cache[stock]
        date_idx = pd.to_datetime(trade_date)
        
        try:
            mask = df.index <= date_idx
            if not mask.any():
                return None
            idx = mask.sum() - 1
            row = df.iloc[idx]
            
            return {
                'open': float(row['open']),
                'close': float(row['close']),
                'high': float(row['high']),
                'low': float(row['low']),
                'volume': float(row['volume']),
                'money': float(row['money'])
            }
        except:
            return None
    
    def get_fundamentals(self, stock: str, trade_date: str) -> dict:
        """获取基本面数据"""
        cache_key = f"{stock}_{trade_date}"
        if cache_key in self.fundamentals_cache:
            return self.fundamentals_cache[cache_key]
        
        fundamentals = {}
        try:
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
            ).filter(jq.valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=trade_date)
            
            if df is not None and not df.empty:
                row = df.iloc[0]
                fundamentals = {
                    'pe_ratio': float(row['pe_ratio']) if pd.notna(row['pe_ratio']) else None,
                    'pb_ratio': float(row['pb_ratio']) if pd.notna(row['pb_ratio']) else None,
                    'market_cap': float(row['market_cap']) if pd.notna(row['market_cap']) else None,
                    'roe': float(row['roe']) if pd.notna(row['roe']) else None,
                    'roa': float(row['roa']) if pd.notna(row['roa']) else None,
                    'revenue_growth': float(row['inc_revenue_year_on_year']) if pd.notna(row['inc_revenue_year_on_year']) else None,
                    'profit_growth': float(row['inc_net_profit_year_on_year']) if pd.notna(row['inc_net_profit_year_on_year']) else None,
                }
        except:
            pass
        
        self.fundamentals_cache[cache_key] = fundamentals
        return fundamentals
    
    def get_price_features(self, stock: str, trade_date: str) -> dict:
        """获取价格衍生特征"""
        if stock not in self.price_cache:
            return {}
        
        df = self.price_cache[stock]
        date_idx = pd.to_datetime(trade_date)
        
        try:
            mask = df.index <= date_idx
            if not mask.any():
                return {}
            idx = mask.sum() - 1
            
            if idx < 60:
                return {}
            
            features = {}
            closes = df['close'].values
            volumes = df['volume'].values
            
            # 动量
            features['momentum_5d'] = (closes[idx] / closes[idx-5] - 1) * 100
            features['momentum_20d'] = (closes[idx] / closes[idx-20] - 1) * 100
            features['momentum_60d'] = (closes[idx] / closes[idx-60] - 1) * 100
            
            # 均线趋势
            ma5 = np.mean(closes[idx-5:idx])
            ma20 = np.mean(closes[idx-20:idx])
            ma60 = np.mean(closes[idx-60:idx])
            features['ma_trend'] = 1.0 if closes[idx] > ma5 > ma20 > ma60 else 0.0
            
            # 新高
            features['is_new_high'] = 1 if closes[idx] >= max(closes[idx-60:idx]) * 0.98 else 0
            
            # 量比
            features['volume_ratio'] = np.mean(volumes[idx-5:idx]) / np.mean(volumes[idx-20:idx])
            
            return features
        except:
            return {}
    
    def calculate_scores(self, trade_date: str) -> dict:
        """计算所有股票评分"""
        scores = {}
        thresholds = self.config.thresholds
        
        for stock in self.price_cache.keys():
            price_data = self.get_price(stock, trade_date)
            if not price_data:
                continue
            
            # 基本过滤
            if price_data['volume'] < thresholds['min_volume']:
                continue
            
            fundamentals = self.get_fundamentals(stock, trade_date)
            if not fundamentals:
                continue
            
            # 市值过滤
            mc = fundamentals.get('market_cap', 0)
            if not mc or mc < thresholds['min_market_cap'] or mc > thresholds['max_market_cap']:
                continue
            
            # ROE过滤
            roe = fundamentals.get('roe', 0)
            if not roe or roe < thresholds['min_roe']:
                continue
            
            # PE过滤
            pe = fundamentals.get('pe_ratio', 0)
            if pe and (pe <= 0 or pe > thresholds['max_pe']):
                continue
            
            # 获取价格特征
            price_features = self.get_price_features(stock, trade_date)
            
            # 计算综合得分
            score = self.calculator.calculate_composite_score(fundamentals, price_features)
            
            if score > 60:  # 筛选高分股票
                scores[stock] = score
        
        return scores
    
    def select_stocks(self, trade_date: str) -> list:
        scores = self.calculate_scores(trade_date)
        if not scores:
            return []
        
        sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_stocks[:self.config.max_holdings]]
    
    def execute_trade(self, stock: str, action: str, shares: int, price: float, trade_date: str) -> bool:
        if action == 'buy':
            cost = shares * price * (1 + self.config.commission_rate + self.config.slippage)
            if cost <= self.cash:
                self.cash -= cost
                if stock in self.positions:
                    old = self.positions[stock]
                    total = old['shares'] + shares
                    avg = (old['shares'] * old['cost'] + shares * price) / total
                    self.positions[stock] = {
                        'shares': total, 'cost': avg,
                        'entry_date': old['entry_date'], 'highest_price': max(old.get('highest_price', price), price)
                    }
                else:
                    self.positions[stock] = {
                        'shares': shares, 'cost': price,
                        'entry_date': trade_date, 'highest_price': price
                    }
                self.trade_history.append({
                    'date': trade_date, 'stock': stock, 'action': 'buy',
                    'shares': shares, 'price': price, 'amount': cost
                })
                return True
        elif action == 'sell':
            if stock in self.positions and self.positions[stock]['shares'] >= shares:
                revenue = shares * price * (1 - self.config.commission_rate - self.config.stamp_tax - self.config.slippage)
                self.cash += revenue
                self.positions[stock]['shares'] -= shares
                if self.positions[stock]['shares'] == 0:
                    del self.positions[stock]
                self.trade_history.append({
                    'date': trade_date, 'stock': stock, 'action': 'sell',
                    'shares': shares, 'price': price, 'amount': revenue
                })
                return True
        return False
    
    def calculate_portfolio_value(self, trade_date: str) -> float:
        total = self.cash
        for stock, pos in self.positions.items():
            price_data = self.get_price(stock, trade_date)
            if price_data:
                total += pos['shares'] * price_data['close']
        return total
    
    def risk_control(self, trade_date: str):
        for stock in list(self.positions.keys()):
            pos = self.positions[stock]
            price_data = self.get_price(stock, trade_date)
            if not price_data:
                continue
            
            current = price_data['close']
            cost = pos['cost']
            highest = pos.get('highest_price', cost)
            
            if current > highest:
                self.positions[stock]['highest_price'] = current
                highest = current
            
            profit = (current - cost) / cost
            dd = (current - highest) / highest
            
            if profit < self.config.stop_loss:
                logger.info(f"🛑 [止损] {stock}: {profit*100:.1f}%")
                self.execute_trade(stock, 'sell', pos['shares'], current, trade_date)
            elif profit > self.config.take_profit:
                logger.info(f"🎯 [止盈] {stock}: {profit*100:.1f}%")
                self.execute_trade(stock, 'sell', pos['shares'], current, trade_date)
            elif profit > 0.20 and dd < -self.config.trailing_stop:
                logger.info(f"📉 [移动止损] {stock}: 回撤{dd*100:.1f}%")
                self.execute_trade(stock, 'sell', pos['shares'], current, trade_date)
    
    def rebalance(self, trade_date: str):
        target_stocks = self.select_stocks(trade_date)
        
        # 卖出非目标
        for stock in list(self.positions.keys()):
            if stock not in target_stocks:
                pos = self.positions[stock]
                price_data = self.get_price(stock, trade_date)
                if price_data:
                    self.execute_trade(stock, 'sell', pos['shares'], price_data['close'], trade_date)
        
        if not target_stocks:
            return
        
        # 买入目标
        total_value = self.calculate_portfolio_value(trade_date)
        available = self.cash
        
        for stock in target_stocks:
            if stock not in self.positions:
                price_data = self.get_price(stock, trade_date)
                if price_data and price_data['close'] > 0:
                    price = price_data['close']
                    max_invest = min(total_value * self.config.single_stock_max, available * 0.9)
                    shares = int(max_invest / price / 100) * 100
                    if shares >= 100:
                        if self.execute_trade(stock, 'buy', shares, price, trade_date):
                            available = self.cash
    
    def run(self) -> dict:
        logger.info("=" * 80)
        logger.info("🎯 十倍股多因子策略")
        logger.info("=" * 80)
        
        self.preload_data()
        
        if not self.trade_days or not self.price_cache:
            return {}
        
        logger.info(f"回测区间: {self.config.start_date} ~ {self.config.end_date}")
        logger.info(f"初始资金: {self.config.initial_cash:,.0f}")
        
        last_rebalance = -self.config.rebalance_days
        
        for idx, trade_date in enumerate(self.trade_days):
            self.dates.append(trade_date)
            self.risk_control(trade_date)
            
            if idx - last_rebalance >= self.config.rebalance_days:
                self.rebalance(trade_date)
                last_rebalance = idx
            
            pv = self.calculate_portfolio_value(trade_date)
            self.equity_history.append(pv)
            
            if len(self.equity_history) > 1:
                dr = (pv / self.equity_history[-2] - 1)
            else:
                dr = 0.0
            self.daily_returns.append(dr)
            
            if idx % 50 == 0:
                gain = (pv / self.config.initial_cash - 1) * 100
                logger.info(f"   {idx+1}/{len(self.trade_days)} | 净值: {pv:,.0f} | 收益: {gain:.1f}% | 持仓: {len(self.positions)}")
        
        results = self.calculate_performance()
        
        logger.info("=" * 80)
        logger.info("✅ 回测完成")
        logger.info(f"   总收益: {results['total_return']*100:.2f}%")
        logger.info(f"   年化收益: {results['annual_return']*100:.2f}%")
        logger.info(f"   夏普比率: {results['sharpe_ratio']:.2f}")
        logger.info(f"   最大回撤: {results['max_drawdown']*100:.2f}%")
        logger.info("=" * 80)
        
        return results
    
    def calculate_performance(self) -> dict:
        results = {
            'total_return': 0.0, 'annual_return': 0.0, 'sharpe_ratio': 0.0,
            'max_drawdown': 0.0, 'total_trades': len(self.trade_history),
            'calmar_ratio': 0.0, 'sortino_ratio': 0.0,
            'equity_curve': self.equity_history, 'daily_returns': self.daily_returns,
            'dates': self.dates, 'trade_history': self.trade_history
        }
        
        if not self.equity_history:
            return results
        
        results['total_return'] = (self.equity_history[-1] / self.config.initial_cash) - 1
        
        days = len(self.equity_history)
        if days > 1:
            results['annual_return'] = (1 + results['total_return']) ** (252 / days) - 1
        
        returns = pd.Series(self.daily_returns)
        if len(returns) > 1 and returns.std() > 0:
            results['sharpe_ratio'] = returns.mean() / returns.std() * np.sqrt(252)
        
        equity = pd.Series(self.equity_history)
        peak = equity.cummax()
        dd = (equity - peak) / peak
        results['max_drawdown'] = dd.min()
        results['drawdown_curve'] = dd.tolist()
        
        if results['max_drawdown'] != 0:
            results['calmar_ratio'] = results['annual_return'] / abs(results['max_drawdown'])
        
        neg = returns[returns < 0]
        if len(neg) > 0 and neg.std() > 0:
            results['sortino_ratio'] = returns.mean() / neg.std() * np.sqrt(252)
        
        return results

# ============================================================
# 可视化和报告
# ============================================================

def generate_chart_base64(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    return img

def generate_visualizations(results: dict, config: StrategyConfig) -> dict:
    charts = {}
    if not MATPLOTLIB_AVAILABLE or not results.get('dates'):
        return charts
    
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in results['dates']]
    equity = results['equity_curve']
    
    # 收益曲线
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(dates, equity, linewidth=2.5, color='#667eea', label='Multifactor Strategy')
    ax.axhline(y=config.initial_cash, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=config.initial_cash * 10, color='red', linestyle='--', alpha=0.7, label='10x Target')
    ax.fill_between(dates, config.initial_cash, equity, alpha=0.3, color='#667eea')
    ax.set_title('Equity Curve - Multifactor Strategy', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    charts['equity'] = generate_chart_base64(fig)
    
    # 回撤
    if results.get('drawdown_curve'):
        fig, ax = plt.subplots(figsize=(14, 4))
        dd = [d * 100 for d in results['drawdown_curve']]
        ax.fill_between(dates, dd, 0, color='#f56565', alpha=0.6)
        ax.set_title('Drawdown', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        charts['drawdown'] = generate_chart_base64(fig)
    
    return charts

def generate_html_report(results: dict, config: StrategyConfig, charts: dict) -> str:
    chart_html = ""
    for key, img in charts.items():
        chart_html += f'<div class="chart"><img src="data:image/png;base64,{img}"></div>'
    
    trade_rows = ""
    for t in results.get('trade_history', [])[-100:]:
        color = '#48bb78' if t['action'] == 'buy' else '#f56565'
        trade_rows += f"<tr><td>{t['date']}</td><td>{t['stock']}</td><td style='color:{color}'>{t['action']}</td><td>{t['shares']:,}</td><td>{t['price']:.2f}</td></tr>"
    
    target = results['total_return'] >= 9.0
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Multifactor Strategy Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; position: relative; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .status {{ position: absolute; top: 20px; right: 20px; background: {'#48bb78' if target else '#ed8936'}; padding: 10px 20px; border-radius: 30px; font-weight: bold; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); padding: 25px; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .metric .value.pos {{ color: #48bb78; }}
        .metric .value.neg {{ color: #f56565; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.05); }}
        .section h2 {{ margin-bottom: 20px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        .factor-list {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
        .factor {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; }}
        .factor-name {{ font-weight: bold; color: #667eea; }}
        .factor-weight {{ color: #aaa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="status">{'🏆 TARGET ACHIEVED!' if target else '📈 IN PROGRESS'}</div>
            <h1>🎯 多因子选股策略回测报告</h1>
            <p>基于历史10倍股特征构建的多因子模型</p>
            <p>回测区间: {config.start_date} ~ {config.end_date}</p>
            <p>初始资金: ¥{config.initial_cash:,.0f} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric"><div class="label">总收益率</div><div class="value {'pos' if results['total_return']>0 else 'neg'}">{results['total_return']*100:.1f}%</div></div>
            <div class="metric"><div class="label">年化收益</div><div class="value {'pos' if results['annual_return']>0 else 'neg'}">{results['annual_return']*100:.1f}%</div></div>
            <div class="metric"><div class="label">夏普比率</div><div class="value">{results['sharpe_ratio']:.2f}</div></div>
            <div class="metric"><div class="label">最大回撤</div><div class="value neg">{results['max_drawdown']*100:.1f}%</div></div>
            <div class="metric"><div class="label">卡玛比率</div><div class="value">{results['calmar_ratio']:.2f}</div></div>
            <div class="metric"><div class="label">索提诺</div><div class="value">{results['sortino_ratio']:.2f}</div></div>
            <div class="metric"><div class="label">交易次数</div><div class="value">{results['total_trades']}</div></div>
            <div class="metric"><div class="label">收益倍数</div><div class="value {'pos' if results['total_return']>0 else 'neg'}">{results['total_return']+1:.2f}x</div></div>
        </div>
        
        <div class="section">
            <h2>📊 收益曲线</h2>
            {chart_html}
        </div>
        
        <div class="section">
            <h2>🧮 因子权重配置</h2>
            <div class="factor-list">
                <div class="factor"><span class="factor-name">成长因子</span><span class="factor-weight"> 30%</span><p>营收增长率、利润增长率</p></div>
                <div class="factor"><span class="factor-name">质量因子</span><span class="factor-weight"> 25%</span><p>ROE、ROA</p></div>
                <div class="factor"><span class="factor-name">估值因子</span><span class="factor-weight"> 15%</span><p>PE、PB（适度估值）</p></div>
                <div class="factor"><span class="factor-name">动量因子</span><span class="factor-weight"> 15%</span><p>20日/60日动量</p></div>
                <div class="factor"><span class="factor-name">规模因子</span><span class="factor-weight"> 10%</span><p>市值50-200亿最优</p></div>
                <div class="factor"><span class="factor-name">技术因子</span><span class="factor-weight"> 5%</span><p>均线多头、新高</p></div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 交易记录（最近100笔）</h2>
            <table>
                <tr><th>日期</th><th>股票</th><th>操作</th><th>数量</th><th>价格</th></tr>
                {trade_rows}
            </table>
        </div>
    </div>
</body>
</html>"""

def main():
    print("=" * 80)
    print("🎯 十倍股多因子策略")
    print("=" * 80)
    
    config = StrategyConfig()
    
    if len(sys.argv) > 1:
        config.start_date = sys.argv[1]
    if len(sys.argv) > 2:
        config.end_date = sys.argv[2]
    
    engine = MultifactorBacktest(config)
    
    if not engine.authenticate():
        return
    
    results = engine.run()
    if not results:
        return
    
    print("\n📊 生成图表...")
    charts = generate_visualizations(results, config)
    
    print("📝 生成报告...")
    html = generate_html_report(results, config, charts)
    
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_multifactor_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("=" * 80)
    print(f"✅ 完成!")
    print(f"📄 报告: {report_path}")
    print(f"📈 总收益: {results['total_return']*100:.1f}%")
    print(f"📈 倍数: {results['total_return']+1:.2f}x")
    print("=" * 80)
    
    jq.logout()

if __name__ == "__main__":
    main()

