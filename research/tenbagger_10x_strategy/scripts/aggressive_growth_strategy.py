#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
激进版高成长策略 - 目标两年5倍
特点：
1. 聚焦科创板+创业板高成长股
2. 集中持仓1-2只
3. 更高的十倍股权重
4. 趋势跟踪+动量策略
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AggressiveGrowthStrategy:
    """激进版高成长策略"""
    
    def __init__(self):
        self.jq = None
        self._ensure_jqdata()
        
        # 激进参数
        self.initial_capital = 1_000_000
        self.max_holdings = 2  # 集中持仓
        self.stop_loss = -0.15  # 15%止损
        self.take_profit = 1.00  # 100%止盈
        
        # 十倍股规律（从挖掘结果）
        self.tenbagger_criteria = {
            'pe_range': (30, 100),      # PE 30-100（成长股特征）
            'profit_growth_min': 30,     # 利润增速>30%
            'revenue_growth_min': 20,    # 营收增速>20%
            'roe_min': 10,               # ROE>10%
            'market_cap_max': 800,       # 市值<800亿（有空间）
            'market_cap_min': 50,        # 市值>50亿（有规模）
        }
    
    def _ensure_jqdata(self):
        if self.jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
    
    def get_growth_stock_pool(self, date: str) -> list:
        """获取高成长股票池（科创板+创业板）"""
        # 科创板指数成分股
        try:
            kcb = list(self.jq.get_index_stocks('000688.XSHG', date=date))[:30]
        except:
            kcb = []
        
        # 创业板指数成分股
        try:
            cyb = list(self.jq.get_index_stocks('399006.XSHE', date=date))[:30]
        except:
            cyb = []
        
        # 合并去重
        pool = list(set(kcb + cyb))
        return pool[:50]  # 最多50只
    
    def score_stock(self, stock: str, date: str) -> tuple:
        """评分单只股票"""
        try:
            from jqdatasdk import query, valuation, indicator
            
            q = query(
                valuation.pe_ratio,
                valuation.market_cap,
                indicator.roe,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year
            ).filter(valuation.code == stock)
            
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0, {}
            
            row = df.iloc[0]
            
            # 获取动量
            price_df = self.jq.get_price(stock, end_date=date, count=60, fields=['close'])
            momentum = 0
            if price_df is not None and len(price_df) >= 60:
                momentum = price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1
            
            # 计算评分
            score = 0
            details = {}
            
            # 1. 利润增速（权重40%）
            profit_g = row['inc_net_profit_year_on_year'] if pd.notna(row['inc_net_profit_year_on_year']) else 0
            if profit_g > 100:
                score += 40
                details['profit'] = f"+100% ({profit_g:.0f}%)"
            elif profit_g > 50:
                score += 30
                details['profit'] = f"+50% ({profit_g:.0f}%)"
            elif profit_g > 30:
                score += 20
                details['profit'] = f"+30% ({profit_g:.0f}%)"
            
            # 2. ROE（权重25%）
            roe = row['roe'] if pd.notna(row['roe']) else 0
            if roe > 25:
                score += 25
                details['roe'] = f"优秀 ({roe:.1f}%)"
            elif roe > 15:
                score += 18
                details['roe'] = f"良好 ({roe:.1f}%)"
            elif roe > 10:
                score += 10
                details['roe'] = f"一般 ({roe:.1f}%)"
            
            # 3. 动量（权重25%）
            if momentum > 0.50:
                score += 25
                details['momentum'] = f"强势 ({momentum*100:.0f}%)"
            elif momentum > 0.20:
                score += 20
                details['momentum'] = f"上涨 ({momentum*100:.0f}%)"
            elif momentum > 0:
                score += 15
                details['momentum'] = f"震荡 ({momentum*100:.0f}%)"
            elif momentum > -0.10:
                score += 10
                details['momentum'] = f"回调 ({momentum*100:.0f}%)"
            # 负动量不加分
            
            # 4. 市值（权重10%）
            cap = row['market_cap'] / 1e8 if pd.notna(row['market_cap']) else 0
            if 100 < cap < 500:
                score += 10
                details['cap'] = f"中盘 ({cap:.0f}亿)"
            elif 50 < cap < 800:
                score += 6
                details['cap'] = f"成长 ({cap:.0f}亿)"
            
            return score, details
            
        except Exception as e:
            return 0, {'error': str(e)}
    
    def run_backtest(self, start_date: str = "2023-01-01", end_date: str = "2024-12-31"):
        """运行回测"""
        print("="*70)
        print("🚀 激进版高成长策略 - 目标两年5倍")
        print("="*70)
        print(f"📅 回测期间: {start_date} ~ {end_date}")
        print(f"💰 初始资金: {self.initial_capital:,}")
        print(f"📊 最大持仓: {self.max_holdings}只")
        print(f"⚠️ 止损: {self.stop_loss*100:.0f}% | 止盈: {self.take_profit*100:.0f}%")
        print()
        
        # 获取交易日
        trade_days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 状态
        equity = self.initial_capital
        cash = self.initial_capital
        positions = {}  # {stock: {'shares': n, 'cost': p, 'highest': h}}
        trades = []
        equity_curve = []
        
        # 获取股票池
        pool = self.get_growth_stock_pool(start_date)
        logger.info(f"📊 股票池: {len(pool)}只（科创板+创业板）")
        
        # 预加载价格数据
        logger.info("📥 加载价格数据...")
        price_data = {}
        for stock in pool:
            try:
                df = self.jq.get_price(stock, start_date=start_date, end_date=end_date, fields=['close'])
                if df is not None and len(df) > 0:
                    price_data[stock] = df['close']
            except:
                pass
        logger.info(f"   成功加载 {len(price_data)} 只股票")
        
        print("\n📈 回测进度:")
        print("-"*70)
        
        for i, td in enumerate(trade_days):
            date_str = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 计算当前持仓市值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_data and date_str in price_data[stock].index:
                    price = price_data[stock].loc[date_str]
                    portfolio_value += pos['shares'] * price
                    
                    # 更新最高价
                    pos['highest'] = max(pos.get('highest', price), price)
                    
                    # 检查止损止盈
                    ret = price / pos['cost'] - 1
                    
                    if ret <= self.stop_loss:
                        # 止损
                        cash += pos['shares'] * price
                        pnl = (price - pos['cost']) * pos['shares']
                        trades.append({'date': date_str, 'stock': stock, 'action': 'stop_loss', 'pnl': pnl})
                        logger.info(f"⛔ [{date_str}] 止损 {stock} @{price:.2f} 亏损:{pnl:,.0f}")
                        del positions[stock]
                    
                    elif ret >= self.take_profit:
                        # 止盈
                        cash += pos['shares'] * price
                        pnl = (price - pos['cost']) * pos['shares']
                        trades.append({'date': date_str, 'stock': stock, 'action': 'take_profit', 'pnl': pnl})
                        logger.info(f"🎯 [{date_str}] 止盈 {stock} @{price:.2f} 盈利:{pnl:,.0f}")
                        del positions[stock]
            
            # 每10天选股调仓
            if i % 10 == 0 and i >= 20:
                # 评分选股
                scored = []
                for stock in pool:
                    if stock in price_data:
                        score, details = self.score_stock(stock, date_str)
                        if score > 50:  # 只选高分股
                            scored.append((stock, score, details))
                
                scored.sort(key=lambda x: x[1], reverse=True)
                top_stocks = scored[:self.max_holdings]
                
                # 调仓
                if top_stocks:
                    # 清仓不在top中的
                    for stock in list(positions.keys()):
                        if stock not in [s[0] for s in top_stocks]:
                            if stock in price_data and date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                pnl = (price - positions[stock]['cost']) * positions[stock]['shares']
                                cash += positions[stock]['shares'] * price
                                trades.append({'date': date_str, 'stock': stock, 'action': 'rebalance', 'pnl': pnl})
                            del positions[stock]
                    
                    # 买入新股
                    per_stock = portfolio_value * 0.95 / len(top_stocks)  # 95%仓位
                    for stock, score, details in top_stocks:
                        if stock not in positions and stock in price_data:
                            if date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                shares = int(per_stock / price / 100) * 100
                                if shares > 0 and cash >= shares * price:
                                    positions[stock] = {'shares': shares, 'cost': price, 'highest': price}
                                    cash -= shares * price
                                    logger.info(f"🔥 [{date_str}] 买入 {stock} @{price:.2f} x{shares} 评分:{score}")
            
            # 记录净值
            equity_curve.append({'date': date_str, 'equity': portfolio_value})
            
            # 每月显示进度
            if i % 20 == 0:
                ret = (portfolio_value / self.initial_capital - 1) * 100
                logger.info(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret:+.1f}%")
        
        # 最终结果
        final_value = cash
        for stock, pos in positions.items():
            if stock in price_data:
                final_value += pos['shares'] * price_data[stock].iloc[-1]
        
        total_return = (final_value / self.initial_capital - 1) * 100
        years = len(trade_days) / 250
        annual_return = ((final_value / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else total_return
        
        # 计算最大回撤
        equity_df = pd.DataFrame(equity_curve)
        max_dd = ((equity_df['equity'] / equity_df['equity'].cummax()) - 1).min() * 100
        
        print("\n" + "="*70)
        print("📋 回测结果")
        print("="*70)
        print(f"初始资金:     {self.initial_capital:>15,}")
        print(f"最终净值:     {final_value:>15,.0f}")
        print(f"总收益率:     {total_return:>14.1f}%")
        print(f"年化收益率:   {annual_return:>14.1f}%")
        print(f"最大回撤:     {max_dd:>14.1f}%")
        print(f"交易次数:     {len(trades):>15}")
        
        print("\n🎯 两年5倍目标评估:")
        factor = 1 + total_return/100
        two_year_factor = factor ** (2/years) if years > 0 else factor
        print(f"   {years:.1f}年倍数: {factor:.2f}x")
        print(f"   两年预测: {two_year_factor:.2f}x")
        print(f"   目标: 5.0x")
        
        if two_year_factor >= 5:
            print("   ✅ 达到两年5倍目标！")
        else:
            print(f"   进度: {two_year_factor/5*100:.1f}%")
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_dd,
            'trades': len(trades),
            'factor': factor,
            'two_year_factor': two_year_factor
        }


if __name__ == "__main__":
    strategy = AggressiveGrowthStrategy()
    result = strategy.run_backtest()
