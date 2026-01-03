#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
终极两年5倍策略系统
核心思路：
1. 市场环境判断 - 只在牛市执行激进策略
2. 知识库规律选股 - 小市值+高增速
3. 极端集中 - 只持1-2只最强股
4. 完美择时 - 牛市满仓，熊市空仓
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Ultimate5XStrategy:
    """终极两年5倍策略"""
    
    def __init__(self):
        self.jq = None
        self._ensure_jqdata()
        
        # 策略参数
        self.initial_capital = 1_000_000
        self.max_holdings = 2  # 极端集中
        self.stop_loss = -0.15
        self.take_profit = 2.0  # 200%止盈
        
        # 知识库规律参数
        self.tenbagger_criteria = {
            'market_cap_max': 50,   # 小市值<50亿
            'market_cap_min': 10,
            'profit_growth_min': 50,  # 利润增速>50%
            'revenue_growth_min': 30,  # 营收增速>30%
        }
    
    def _ensure_jqdata(self):
        if self.jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
    
    def detect_market_regime(self, date: str) -> str:
        """检测市场环境"""
        try:
            # 获取沪深300指数数据
            prices = self.jq.get_price('000300.XSHG', end_date=date, count=120, fields=['close'])
            if prices is None or len(prices) < 60:
                return 'UNKNOWN'
            
            close = prices['close']
            ma20 = close.tail(20).mean()
            ma60 = close.tail(60).mean()
            current = close.iloc[-1]
            
            # 计算动量
            momentum_60d = current / close.iloc[-60] - 1 if len(close) >= 60 else 0
            momentum_20d = current / close.iloc[-20] - 1 if len(close) >= 20 else 0
            
            # 判断市场环境
            if current > ma20 > ma60 and momentum_60d > 0.15:
                return 'BULL'
            elif current < ma20 < ma60 and momentum_60d < -0.10:
                return 'BEAR'
            elif momentum_20d > 0.05 and current > ma20:
                return 'RECOVERY'
            else:
                return 'VOLATILE'
                
        except Exception as e:
            return 'UNKNOWN'
    
    def screen_stocks(self, date: str) -> list:
        """根据知识库规律筛选股票"""
        from jqdatasdk import query, valuation, indicator
        
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year,
            indicator.roe
        ).filter(
            # 科创板+创业板+主板小盘
            valuation.market_cap < self.tenbagger_criteria['market_cap_max'],
            valuation.market_cap > self.tenbagger_criteria['market_cap_min'],
            indicator.inc_net_profit_year_on_year > self.tenbagger_criteria['profit_growth_min'],
            indicator.inc_revenue_year_on_year > self.tenbagger_criteria['revenue_growth_min'],
            indicator.roe > 5
        ).limit(50)
        
        df = self.jq.get_fundamentals(q, date=date)
        
        if df is None or len(df) == 0:
            return []
        
        # 评分
        df['score'] = (
            df['inc_net_profit_year_on_year'].clip(0, 200).fillna(0) * 0.5 +
            df['inc_revenue_year_on_year'].clip(0, 100).fillna(0) * 0.3 +
            (50 - df['market_cap']).clip(0, 50) * 0.4  # 市值越小分越高
        )
        
        df = df.sort_values('score', ascending=False)
        return df['code'].head(10).tolist()
    
    def run_backtest(self, start_date: str, end_date: str):
        """运行回测"""
        print("="*70)
        print("🎯 终极两年5倍策略")
        print("="*70)
        print(f"📅 回测期间: {start_date} ~ {end_date}")
        print(f"💰 初始资金: {self.initial_capital:,}")
        print(f"📊 最大持仓: {self.max_holdings}只（极端集中）")
        print(f"🔄 策略: 牛市满仓，熊市空仓")
        print()
        
        trade_days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 状态
        cash = self.initial_capital
        positions = {}
        equity_curve = []
        current_regime = 'UNKNOWN'
        regime_count = {'BULL': 0, 'BEAR': 0, 'RECOVERY': 0, 'VOLATILE': 0}
        
        # 预加载候选股价格
        print("📈 预加载数据...")
        candidates = self.screen_stocks(start_date)
        print(f"   候选股: {len(candidates)}")
        
        if len(candidates) == 0:
            print("❌ 无候选股票")
            return
        
        price_data = {}
        for stock in candidates:
            try:
                df = self.jq.get_price(stock, start_date=start_date, end_date=end_date, 
                                      fields=['close'], skip_paused=True)
                if df is not None and len(df) > 200:
                    price_data[stock] = df['close']
            except:
                pass
        print(f"   成功加载 {len(price_data)} 只")
        
        selected = [s for s in candidates if s in price_data][:self.max_holdings]
        print(f"   选中: {selected}")
        
        print("\n📊 回测进度:")
        print("-"*70)
        
        for i, td in enumerate(trade_days):
            date_str = str(td)
            
            # 每20天检查市场环境
            if i % 20 == 0:
                new_regime = self.detect_market_regime(date_str)
                if new_regime != current_regime:
                    print(f"📊 [{date_str}] 市场环境: {current_regime} → {new_regime}")
                    current_regime = new_regime
                regime_count[new_regime] = regime_count.get(new_regime, 0) + 1
            
            # 计算持仓市值
            portfolio_value = cash
            for stock, pos in list(positions.items()):
                if stock in price_data and date_str in price_data[stock].index:
                    price = price_data[stock].loc[date_str]
                    if pd.isna(price):
                        continue
                    portfolio_value += pos['shares'] * price
                    
                    # 检查止损止盈
                    ret = price / pos['cost'] - 1
                    if ret <= self.stop_loss:
                        cash += pos['shares'] * price
                        print(f"⛔ [{date_str}] 止损 {stock} 亏损:{ret*100:.1f}%")
                        del positions[stock]
                    elif ret >= self.take_profit:
                        cash += pos['shares'] * price
                        print(f"🎯 [{date_str}] 止盈 {stock} 盈利:{ret*100:.1f}%")
                        del positions[stock]
            
            # 根据市场环境决策
            if current_regime == 'BULL':
                # 牛市：满仓
                if len(positions) < self.max_holdings:
                    available = portfolio_value * 0.95 / self.max_holdings
                    for stock in selected:
                        if stock not in positions and stock in price_data:
                            if date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                if pd.isna(price) or price <= 0:
                                    continue
                                shares = int(available / price / 100) * 100
                                if shares > 0 and cash >= shares * price:
                                    positions[stock] = {'shares': shares, 'cost': price}
                                    cash -= shares * price
                                    print(f"🔥 [{date_str}] 牛市买入 {stock} @{price:.2f}")
            
            elif current_regime == 'BEAR':
                # 熊市：清仓
                for stock in list(positions.keys()):
                    if stock in price_data and date_str in price_data[stock].index:
                        price = price_data[stock].loc[date_str]
                        if pd.isna(price):
                            continue
                        cash += positions[stock]['shares'] * price
                        ret = price / positions[stock]['cost'] - 1
                        print(f"📉 [{date_str}] 熊市清仓 {stock} 收益:{ret*100:.1f}%")
                        del positions[stock]
            
            elif current_regime == 'RECOVERY':
                # 恢复期：半仓
                if len(positions) < 1:
                    if selected and selected[0] in price_data:
                        if date_str in price_data[selected[0]].index:
                            price = price_data[selected[0]].loc[date_str]
                            if not pd.isna(price) and price > 0:
                                shares = int(portfolio_value * 0.5 / price / 100) * 100
                                if shares > 0 and cash >= shares * price:
                                    positions[selected[0]] = {'shares': shares, 'cost': price}
                                    cash -= shares * price
                                    print(f"📈 [{date_str}] 恢复期买入 {selected[0]} @{price:.2f}")
            
            equity_curve.append({'date': date_str, 'equity': portfolio_value})
            
            if i % 40 == 0:
                ret_pct = (portfolio_value / self.initial_capital - 1) * 100
                print(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}% 环境:{current_regime} 持仓:{len(positions)}只")
        
        # 最终清算
        final_value = cash
        for stock, pos in positions.items():
            if stock in price_data:
                last_price = price_data[stock].iloc[-1]
                if not pd.isna(last_price):
                    final_value += pos['shares'] * last_price
        
        total_ret = (final_value / self.initial_capital - 1) * 100
        years = len(trade_days) / 250
        annual_ret = ((final_value / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        eq_df = pd.DataFrame(equity_curve)
        eq_df['equity'] = eq_df['equity'].replace([np.inf, -np.inf], np.nan).ffill()
        max_dd = ((eq_df['equity'] / eq_df['equity'].cummax()) - 1).min() * 100
        
        print("\n" + "="*70)
        print("📋 回测结果")
        print("="*70)
        print(f"初始资金:     {self.initial_capital:>15,}")
        print(f"最终净值:     {final_value:>15,.0f}")
        print(f"总收益率:     {total_ret:>14.1f}%")
        print(f"年化收益率:   {annual_ret:>14.1f}%")
        print(f"最大回撤:     {max_dd:>14.1f}%")
        
        print("\n📊 市场环境统计:")
        for k, v in regime_count.items():
            print(f"   {k}: {v}次")
        
        factor = 1 + total_ret/100
        two_year = factor ** (2/years) if years > 0 else factor
        
        print("\n🎯 两年5倍目标评估:")
        print(f"   {years:.1f}年倍数: {factor:.2f}x")
        print(f"   两年预测: {two_year:.2f}x")
        print(f"   目标: 5.0x | 进度: {two_year/5*100:.1f}%")
        
        if two_year >= 5:
            print("   ✅ 达到两年5倍目标！🎉")
        elif two_year >= 3:
            print("   📈 表现优秀，接近目标")
        
        return {'total_return': total_ret, 'annual_return': annual_ret, 'two_year_factor': two_year}


if __name__ == "__main__":
    strategy = Ultimate5XStrategy()
    
    # 在2014-2015大牛市测试
    print("\n" + "🔵"*35)
    print("测试1: 2014-2015大牛市")
    print("🔵"*35 + "\n")
    strategy.run_backtest("2014-01-01", "2015-12-31")
    
    print("\n\n" + "🔵"*35)
    print("测试2: 2020-2021牛市")
    print("🔵"*35 + "\n")
    strategy.run_backtest("2020-01-01", "2021-12-31")
