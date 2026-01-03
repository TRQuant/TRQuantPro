#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于知识库规律的十倍股策略

核心规律（来自东吴证券A股十倍股样本）：
1. 起步市值：17亿（78%<30亿）
2. 起步PE：47倍
3. 净利润增速：23%
4. 毛利率：30%
5. ROE：13%
6. 创十倍用时：约8年

两年5倍策略调整：
- 选择S2阶段（导入期）股票
- 聚焦超高增速（>50%）
- 小市值（<100亿）
- 高度集中（1-2只）
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


class KBBasedTenbaggerStrategy:
    """基于知识库的十倍股策略"""
    
    def __init__(self):
        self.jq = None
        self._ensure_jqdata()
        
        # 知识库规律参数
        self.criteria = {
            # 市值筛选（核心：78%十倍股<30亿）
            'market_cap_ideal': (15, 50),   # 理想区间：15-50亿（更高弹性）
            'market_cap_max': 100,          # 最大100亿
            
            # 增速要求（两年5倍需更高）
            'profit_growth_min': 50,        # 利润增速>50%（知识库建议30%，提高到50%）
            'revenue_growth_min': 30,       # 营收增速>30%（知识库建议25%）
            
            # 质量指标
            'gross_margin_min': 25,         # 毛利率>25%
            'roe_min': 10,                  # ROE>10%
            
            # 估值
            'pe_max': 80,                   # PE<80（成长股允许更高PE）
            'peg_max': 2.0,                 # PEG<2
            
            # 技术
            'momentum_min': 0.10,           # 60日动量>10%
        }
        
        # 策略参数
        self.initial_capital = 1_000_000
        self.max_holdings = 2          # 高度集中
        self.stop_loss = -0.12         # 12%止损
        self.take_profit = 0.80        # 80%分批止盈
        self.full_profit = 1.50        # 150%全止盈
        
        # 因子权重（来自知识库）
        self.factor_weights = {
            'financial': 0.40,    # 财务因子40%
            'growth': 0.25,       # 成长动量25%
            'valuation': 0.20,    # 估值因子20%
            'technical': 0.15     # 技术因子15%
        }
    
    def _ensure_jqdata(self):
        if self.jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
    
    def score_stock(self, stock: str, date: str) -> dict:
        """
        根据知识库因子体系评分
        返回: {score, stage, details}
        """
        from jqdatasdk import query, valuation, indicator
        
        try:
            # 获取财务数据
            q = query(
                valuation.pe_ratio,
                valuation.market_cap,
                indicator.roe,
                indicator.gross_profit_margin,
                indicator.net_profit_margin,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year
            ).filter(valuation.code == stock)
            
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return {'score': 0, 'stage': 'N/A', 'pass': False}
            
            row = df.iloc[0]
            
            # 获取技术数据
            price_df = self.jq.get_price(stock, end_date=date, count=60, fields=['close', 'volume'])
            momentum = 0
            ma_bullish = False
            if price_df is not None and len(price_df) >= 60:
                momentum = price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1
                ma20 = price_df['close'].tail(20).mean()
                ma60 = price_df['close'].tail(60).mean()
                ma_bullish = price_df['close'].iloc[-1] > ma20 > ma60
            
            # 提取因子值
            market_cap = row['market_cap'] / 1e8 if pd.notna(row['market_cap']) else 9999
            pe = row['pe_ratio'] if pd.notna(row['pe_ratio']) else 9999
            roe = row['roe'] if pd.notna(row['roe']) else 0
            gross_margin = row['gross_profit_margin'] if pd.notna(row['gross_profit_margin']) else 0
            profit_growth = row['inc_net_profit_year_on_year'] if pd.notna(row['inc_net_profit_year_on_year']) else 0
            revenue_growth = row['inc_revenue_year_on_year'] if pd.notna(row['inc_revenue_year_on_year']) else 0
            
            # 计算PEG
            peg = pe / profit_growth if profit_growth > 0 and pe > 0 else 999
            
            # === 评分（满分100分）===
            score = 0
            details = {}
            
            # 1. 财务因子（40分）
            # 利润增速（15分）
            if profit_growth >= 100:
                score += 15
            elif profit_growth >= 50:
                score += 12
            elif profit_growth >= 30:
                score += 8
            elif profit_growth >= 20:
                score += 5
            details['profit_growth'] = profit_growth
            
            # 营收增速（10分）
            if revenue_growth >= 50:
                score += 10
            elif revenue_growth >= 30:
                score += 7
            elif revenue_growth >= 20:
                score += 5
            details['revenue_growth'] = revenue_growth
            
            # 毛利率（8分）
            if gross_margin >= 40:
                score += 8
            elif gross_margin >= 30:
                score += 6
            elif gross_margin >= 25:
                score += 4
            details['gross_margin'] = gross_margin
            
            # ROE（7分）
            if roe >= 20:
                score += 7
            elif roe >= 15:
                score += 5
            elif roe >= 10:
                score += 3
            details['roe'] = roe
            
            # 2. 估值因子（20分）
            # 市值（10分）- 小市值优先
            if 15 <= market_cap <= 50:
                score += 10
            elif market_cap < 15:
                score += 8
            elif 50 < market_cap <= 100:
                score += 6
            elif 100 < market_cap <= 200:
                score += 3
            details['market_cap'] = market_cap
            
            # PEG（10分）
            if peg <= 1:
                score += 10
            elif peg <= 1.5:
                score += 7
            elif peg <= 2:
                score += 5
            details['peg'] = peg
            
            # 3. 成长动量（25分）
            # 增速级别加分
            growth_level = min(profit_growth, revenue_growth)
            if growth_level >= 80:
                score += 15
            elif growth_level >= 50:
                score += 10
            elif growth_level >= 30:
                score += 6
            
            # 动量（10分）
            if momentum >= 0.30:
                score += 10
            elif momentum >= 0.15:
                score += 7
            elif momentum >= 0.05:
                score += 4
            details['momentum'] = momentum
            
            # 4. 技术因子（15分）
            if ma_bullish:
                score += 8
            if momentum > 0:
                score += 7
            details['ma_bullish'] = ma_bullish
            
            # 判断阶段
            stage = self._determine_stage(profit_growth, revenue_growth, momentum)
            
            # 是否通过筛选
            passed = (
                market_cap <= self.criteria['market_cap_max'] and
                profit_growth >= self.criteria['profit_growth_min'] and
                revenue_growth >= self.criteria['revenue_growth_min'] and
                roe >= self.criteria['roe_min'] and
                score >= 60
            )
            
            return {
                'score': score,
                'stage': stage,
                'pass': passed,
                'details': details
            }
            
        except Exception as e:
            return {'score': 0, 'stage': 'ERROR', 'pass': False, 'error': str(e)}
    
    def _determine_stage(self, profit_growth, revenue_growth, momentum):
        """判断十倍股阶段"""
        if profit_growth >= 50 and revenue_growth >= 30 and momentum >= 0.15:
            return 'S2_导入期'  # 最佳买入
        elif profit_growth >= 30 and revenue_growth >= 20:
            return 'S1_验证期'  # 关注
        elif profit_growth >= 80 and momentum >= 0.30:
            return 'S3_放量期'  # 持有
        elif profit_growth < 20 or momentum < -0.10:
            return 'S4_衰退期'  # 卖出
        else:
            return 'S0_观察期'  # 排除
    
    def get_stock_pool(self, date: str) -> list:
        """获取候选股票池"""
        # 科创板 + 创业板 + 小市值成长股
        pools = []
        
        try:
            # 科创50
            pools.extend(self.jq.get_index_stocks('000688.XSHG', date=date)[:30])
        except:
            pass
        
        try:
            # 创业板50
            pools.extend(self.jq.get_index_stocks('399673.XSHE', date=date)[:30])
        except:
            pass
        
        try:
            # 中证500（部分小市值）
            pools.extend(self.jq.get_index_stocks('000905.XSHG', date=date)[:40])
        except:
            pass
        
        return list(set(pools))
    
    def run_backtest(self, start_date: str = "2023-01-01", end_date: str = "2024-12-31"):
        """运行回测"""
        print("="*70)
        print("📚 基于知识库规律的十倍股策略")
        print("="*70)
        print(f"📅 回测期间: {start_date} ~ {end_date}")
        print(f"💰 初始资金: {self.initial_capital:,}")
        print(f"📊 最大持仓: {self.max_holdings}只")
        print(f"🎯 选股标准: 利润增速>{self.criteria['profit_growth_min']}%, 市值<{self.criteria['market_cap_max']}亿")
        print()
        
        # 获取交易日
        trade_days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 获取股票池
        pool = self.get_stock_pool(start_date)
        logger.info(f"📊 候选股票池: {len(pool)}只")
        
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
        
        # 回测状态
        equity = self.initial_capital
        cash = equity
        positions = {}
        trades = []
        equity_curve = []
        
        print("\n📈 回测进度:")
        print("-"*70)
        
        for i, td in enumerate(trade_days):
            date_str = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 计算持仓市值
            portfolio_value = cash
            for stock, pos in list(positions.items()):
                if stock in price_data and date_str in price_data[stock].index:
                    price = price_data[stock].loc[date_str]
                    portfolio_value += pos['shares'] * price
                    
                    # 检查止损止盈
                    ret = price / pos['cost'] - 1
                    
                    if ret <= self.stop_loss:
                        cash += pos['shares'] * price
                        pnl = (price - pos['cost']) * pos['shares']
                        logger.info(f"⛔ [{date_str}] 止损 {stock} 亏损:{pnl:,.0f}")
                        trades.append({'date': date_str, 'action': 'stop_loss', 'pnl': pnl})
                        del positions[stock]
                    
                    elif ret >= self.full_profit:
                        cash += pos['shares'] * price
                        pnl = (price - pos['cost']) * pos['shares']
                        logger.info(f"🎯 [{date_str}] 止盈 {stock} +{ret*100:.0f}% 盈利:{pnl:,.0f}")
                        trades.append({'date': date_str, 'action': 'full_profit', 'pnl': pnl})
                        del positions[stock]
                    
                    elif ret >= self.take_profit and pos.get('partial_taken') != True:
                        # 分批止盈：卖出一半
                        sell_shares = pos['shares'] // 2
                        cash += sell_shares * price
                        pos['shares'] -= sell_shares
                        pos['partial_taken'] = True
                        pnl = (price - pos['cost']) * sell_shares
                        logger.info(f"📤 [{date_str}] 分批止盈 {stock} +{ret*100:.0f}%")
            
            # 每20天选股
            if i % 20 == 0 and i >= 20:
                # 筛选通过的股票
                candidates = []
                for stock in pool:
                    if stock in price_data:
                        result = self.score_stock(stock, date_str)
                        if result['pass']:
                            candidates.append((stock, result['score'], result['stage'], result['details']))
                
                # 排序选择
                candidates.sort(key=lambda x: x[1], reverse=True)
                top_stocks = candidates[:self.max_holdings]
                
                if top_stocks:
                    logger.info(f"\n📊 [{date_str}] 筛选结果:")
                    for s, score, stage, details in top_stocks:
                        logger.info(f"   {s} 评分:{score} {stage} 利润:{details.get('profit_growth',0):.0f}% 市值:{details.get('market_cap',0):.0f}亿")
                    
                    # 调仓
                    for stock in list(positions.keys()):
                        if stock not in [s[0] for s in top_stocks]:
                            if stock in price_data and date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                cash += positions[stock]['shares'] * price
                            del positions[stock]
                    
                    # 买入
                    per_stock = portfolio_value * 0.95 / len(top_stocks)
                    for stock, score, stage, _ in top_stocks:
                        if stock not in positions and stock in price_data:
                            if date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                shares = int(per_stock / price / 100) * 100
                                if shares > 0 and cash >= shares * price:
                                    positions[stock] = {'shares': shares, 'cost': price}
                                    cash -= shares * price
                                    logger.info(f"🔥 [{date_str}] 买入 {stock} @{price:.2f} x{shares}")
            
            # 记录净值
            equity_curve.append({'date': date_str, 'equity': portfolio_value})
            
            # 每月进度
            if i % 20 == 0:
                ret = (portfolio_value / self.initial_capital - 1) * 100
                logger.info(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret:+.1f}%")
        
        # 最终清算
        final_value = cash
        for stock, pos in positions.items():
            if stock in price_data:
                final_value += pos['shares'] * price_data[stock].iloc[-1]
        
        total_return = (final_value / self.initial_capital - 1) * 100
        years = len(trade_days) / 250
        annual_return = ((final_value / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        # 最大回撤
        eq_df = pd.DataFrame(equity_curve)
        max_dd = ((eq_df['equity'] / eq_df['equity'].cummax()) - 1).min() * 100
        
        print("\n" + "="*70)
        print("📋 回测结果")
        print("="*70)
        print(f"初始资金:     {self.initial_capital:>15,}")
        print(f"最终净值:     {final_value:>15,.0f}")
        print(f"总收益率:     {total_return:>14.1f}%")
        print(f"年化收益率:   {annual_return:>14.1f}%")
        print(f"最大回撤:     {max_dd:>14.1f}%")
        print(f"交易次数:     {len(trades):>15}")
        
        # 两年5倍评估
        factor = 1 + total_return/100
        two_year = factor ** (2/years) if years > 0 else factor
        
        print("\n🎯 两年5倍目标评估:")
        print(f"   {years:.1f}年倍数: {factor:.2f}x")
        print(f"   两年预测: {two_year:.2f}x")
        print(f"   目标: 5.0x | 进度: {two_year/5*100:.1f}%")
        
        if two_year >= 5:
            print("   ✅ 达到两年5倍目标！🎉")
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_dd,
            'two_year_factor': two_year
        }


if __name__ == "__main__":
    strategy = KBBasedTenbaggerStrategy()
    result = strategy.run_backtest()
