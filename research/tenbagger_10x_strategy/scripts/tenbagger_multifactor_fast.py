#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股多因子策略 - 快速版
========================

优化点:
1. 预加载所有基本面数据（每月更新一次）
2. 向量化计算因子得分
3. 减少API调用次数

代码位置: scripts/tenbagger_multifactor_fast.py
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
# 配置
# ============================================================

class Config:
    def __init__(self):
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_cash = 1000000.0
        self.benchmark = "000300.XSHG"
        self.commission = 0.0003
        self.stamp_tax = 0.001
        self.slippage = 0.002
        
        # 持仓参数
        self.max_holdings = 10
        self.single_max = 0.12
        self.stop_loss = -0.10
        self.take_profit = 0.60
        self.trailing_stop = 0.12
        self.rebalance_days = 10
        
        # 因子权重
        self.weights = {
            'growth': 0.30,
            'quality': 0.25,
            'value': 0.15,
            'momentum': 0.15,
            'size': 0.10,
            'technical': 0.05,
        }

# ============================================================
# 快速多因子引擎
# ============================================================

class FastMultifactor:
    def __init__(self, config: Config):
        self.config = config
        self.cash = config.initial_cash
        self.positions = {}
        self.trade_history = []
        self.equity_history = []
        self.daily_returns = []
        self.dates = []
        
        # 数据缓存
        self.price_cache = {}
        self.fundamentals_df = None
        self.all_stocks = []
        self.trade_days = []
        self.fund_dates = []  # 财务数据日期
    
    def auth(self) -> bool:
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, pwd)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def load_data(self):
        """预加载所有数据"""
        logger.info("📥 预加载数据...")
        
        # 交易日
        self.trade_days = [str(d) for d in jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )]
        logger.info(f"   交易日: {len(self.trade_days)}天")
        
        # 股票池：中证500 + 创业板
        self.all_stocks = jq.get_index_stocks('000905.XSHG')
        self.all_stocks += jq.get_index_stocks('399006.XSHE')[:100]
        self.all_stocks = list(set(self.all_stocks))
        logger.info(f"   股票池: {len(self.all_stocks)}只")
        
        # 价格数据
        logger.info("   获取价格数据...")
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
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty and len(sdf) > 60:
                    sdf.set_index('time', inplace=True)
                    self.price_cache[stock] = sdf
        logger.info(f"   价格数据: {len(self.price_cache)}只")
        
        # 基本面数据（按月获取）
        logger.info("   获取基本面数据...")
        self.fund_dates = []
        fund_list = []
        
        # 每月第一个交易日获取一次
        current_month = None
        for td in self.trade_days:
            month = td[:7]
            if month != current_month:
                current_month = month
                self.fund_dates.append(td)
        
        for fd in self.fund_dates:
            try:
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.valuation.market_cap,
                    jq.indicator.roe,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year,
                ).filter(jq.valuation.code.in_(list(self.price_cache.keys())))
                
                df = jq.get_fundamentals(q, date=fd)
                if df is not None and not df.empty:
                    df['fund_date'] = fd
                    fund_list.append(df)
            except Exception as e:
                logger.warning(f"   基本面数据获取失败 {fd}: {e}")
        
        if fund_list:
            self.fundamentals_df = pd.concat(fund_list, ignore_index=True)
            logger.info(f"   基本面数据: {len(self.fundamentals_df)}条")
        
        logger.info("✅ 数据预加载完成")
    
    def get_price(self, stock: str, date: str) -> dict:
        if stock not in self.price_cache:
            return None
        df = self.price_cache[stock]
        dt = pd.to_datetime(date)
        mask = df.index <= dt
        if not mask.any():
            return None
        idx = mask.sum() - 1
        r = df.iloc[idx]
        return {
            'open': float(r['open']), 'close': float(r['close']),
            'high': float(r['high']), 'low': float(r['low']),
            'volume': float(r['volume']), 'money': float(r['money'])
        }
    
    def get_fund(self, stock: str, date: str) -> dict:
        """获取最近的基本面数据"""
        if self.fundamentals_df is None:
            return {}
        
        # 找到最近的财务日期
        fund_date = None
        for fd in reversed(self.fund_dates):
            if fd <= date:
                fund_date = fd
                break
        
        if not fund_date:
            return {}
        
        row = self.fundamentals_df[
            (self.fundamentals_df['code'] == stock) & 
            (self.fundamentals_df['fund_date'] == fund_date)
        ]
        
        if row.empty:
            return {}
        
        r = row.iloc[0]
        return {
            'pe': float(r['pe_ratio']) if pd.notna(r['pe_ratio']) else None,
            'pb': float(r['pb_ratio']) if pd.notna(r['pb_ratio']) else None,
            'mc': float(r['market_cap']) if pd.notna(r['market_cap']) else None,
            'roe': float(r['roe']) if pd.notna(r['roe']) else None,
            'rev_g': float(r['inc_revenue_year_on_year']) if pd.notna(r['inc_revenue_year_on_year']) else None,
            'pft_g': float(r['inc_net_profit_year_on_year']) if pd.notna(r['inc_net_profit_year_on_year']) else None,
        }
    
    def get_price_features(self, stock: str, date: str) -> dict:
        if stock not in self.price_cache:
            return {}
        df = self.price_cache[stock]
        dt = pd.to_datetime(date)
        mask = df.index <= dt
        if not mask.any():
            return {}
        idx = mask.sum() - 1
        if idx < 60:
            return {}
        
        c = df['close'].values
        v = df['volume'].values
        
        features = {}
        features['m5'] = (c[idx] / c[idx-5] - 1) * 100
        features['m20'] = (c[idx] / c[idx-20] - 1) * 100
        features['m60'] = (c[idx] / c[idx-60] - 1) * 100
        
        ma5 = np.mean(c[idx-5:idx])
        ma20 = np.mean(c[idx-20:idx])
        ma60 = np.mean(c[idx-60:idx])
        features['trend'] = 1 if c[idx] > ma5 > ma20 > ma60 else 0
        features['new_high'] = 1 if c[idx] >= max(c[idx-60:idx]) * 0.98 else 0
        features['vol_ratio'] = np.mean(v[idx-5:idx]) / max(np.mean(v[idx-20:idx]), 1)
        
        return features
    
    def calc_score(self, stock: str, date: str) -> float:
        """计算综合得分"""
        fund = self.get_fund(stock, date)
        pf = self.get_price_features(stock, date)
        
        if not fund or not pf:
            return 0
        
        w = self.config.weights
        score = 0
        
        # 成长因子
        g = 50
        if fund.get('rev_g') and fund['rev_g'] > 30: g += 25
        elif fund.get('rev_g') and fund['rev_g'] > 15: g += 15
        if fund.get('pft_g') and fund['pft_g'] > 30: g += 25
        elif fund.get('pft_g') and fund['pft_g'] > 15: g += 15
        score += min(g, 100) * w['growth']
        
        # 质量因子
        q = 50
        if fund.get('roe') and fund['roe'] > 15: q += 30
        elif fund.get('roe') and fund['roe'] > 10: q += 20
        elif fund.get('roe') and fund['roe'] > 5: q += 10
        score += min(q, 100) * w['quality']
        
        # 估值因子
        v = 50
        pe = fund.get('pe')
        if pe and 15 <= pe <= 35: v += 25
        elif pe and 10 <= pe < 15 or 35 < pe <= 50: v += 10
        pb = fund.get('pb')
        if pb and 2 <= pb <= 6: v += 20
        score += max(min(v, 100), 0) * w['value']
        
        # 动量因子
        m = 50
        if pf.get('m20', 0) > 20: m += 20
        elif pf.get('m20', 0) > 10: m += 15
        elif pf.get('m20', 0) > 5: m += 10
        if pf.get('m60', 0) > 30: m += 15
        elif pf.get('m60', 0) > 15: m += 10
        score += max(min(m, 100), 0) * w['momentum']
        
        # 规模因子
        s = 50
        mc = fund.get('mc')
        if mc and 50 <= mc <= 200: s += 30
        elif mc and 30 <= mc < 50 or 200 < mc <= 300: s += 20
        elif mc and mc > 500: s -= 10
        score += max(min(s, 100), 0) * w['size']
        
        # 技术因子
        t = 50
        if pf.get('trend') == 1: t += 25
        if pf.get('new_high') == 1: t += 20
        if pf.get('vol_ratio', 1) > 1.5: t += 10
        score += min(t, 100) * w['technical']
        
        return score
    
    def select(self, date: str) -> list:
        """选股"""
        scores = {}
        for stock in self.price_cache.keys():
            pd_data = self.get_price(stock, date)
            if not pd_data or pd_data['volume'] < 3000000:
                continue
            
            fund = self.get_fund(stock, date)
            if not fund:
                continue
            
            mc = fund.get('mc', 0)
            if not mc or mc < 20 or mc > 500:
                continue
            
            roe = fund.get('roe', 0)
            if not roe or roe < 5:
                continue
            
            pe = fund.get('pe', 0)
            if pe and (pe <= 0 or pe > 100):
                continue
            
            sc = self.calc_score(stock, date)
            if sc > 60:
                scores[stock] = sc
        
        sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_stocks[:self.config.max_holdings]]
    
    def trade(self, stock: str, action: str, shares: int, price: float, date: str) -> bool:
        if action == 'buy':
            cost = shares * price * (1 + self.config.commission + self.config.slippage)
            if cost <= self.cash:
                self.cash -= cost
                if stock in self.positions:
                    old = self.positions[stock]
                    total = old['shares'] + shares
                    avg = (old['shares'] * old['cost'] + shares * price) / total
                    self.positions[stock] = {'shares': total, 'cost': avg, 'entry': old['entry'], 'high': max(old.get('high', price), price)}
                else:
                    self.positions[stock] = {'shares': shares, 'cost': price, 'entry': date, 'high': price}
                self.trade_history.append({'date': date, 'stock': stock, 'action': 'buy', 'shares': shares, 'price': price, 'amount': cost})
                return True
        elif action == 'sell':
            if stock in self.positions and self.positions[stock]['shares'] >= shares:
                rev = shares * price * (1 - self.config.commission - self.config.stamp_tax - self.config.slippage)
                self.cash += rev
                self.positions[stock]['shares'] -= shares
                if self.positions[stock]['shares'] == 0:
                    del self.positions[stock]
                self.trade_history.append({'date': date, 'stock': stock, 'action': 'sell', 'shares': shares, 'price': price, 'amount': rev})
                return True
        return False
    
    def portfolio_value(self, date: str) -> float:
        total = self.cash
        for stock, pos in self.positions.items():
            pd_data = self.get_price(stock, date)
            if pd_data:
                total += pos['shares'] * pd_data['close']
        return total
    
    def risk_check(self, date: str):
        for stock in list(self.positions.keys()):
            pos = self.positions[stock]
            pd_data = self.get_price(stock, date)
            if not pd_data:
                continue
            
            curr = pd_data['close']
            cost = pos['cost']
            high = pos.get('high', cost)
            
            if curr > high:
                self.positions[stock]['high'] = curr
                high = curr
            
            pft = (curr - cost) / cost
            dd = (curr - high) / high
            
            if pft < self.config.stop_loss:
                logger.info(f"🛑 止损 {stock}: {pft*100:.1f}%")
                self.trade(stock, 'sell', pos['shares'], curr, date)
            elif pft > self.config.take_profit:
                logger.info(f"🎯 止盈 {stock}: {pft*100:.1f}%")
                self.trade(stock, 'sell', pos['shares'], curr, date)
            elif pft > 0.15 and dd < -self.config.trailing_stop:
                logger.info(f"📉 移动止损 {stock}: 回撤{dd*100:.1f}%")
                self.trade(stock, 'sell', pos['shares'], curr, date)
    
    def rebalance(self, date: str):
        targets = self.select(date)
        
        # 卖出
        for stock in list(self.positions.keys()):
            if stock not in targets:
                pos = self.positions[stock]
                pd_data = self.get_price(stock, date)
                if pd_data:
                    self.trade(stock, 'sell', pos['shares'], pd_data['close'], date)
        
        if not targets:
            return
        
        # 买入
        total = self.portfolio_value(date)
        avail = self.cash
        
        for stock in targets:
            if stock not in self.positions:
                pd_data = self.get_price(stock, date)
                if pd_data and pd_data['close'] > 0:
                    price = pd_data['close']
                    max_inv = min(total * self.config.single_max, avail * 0.9)
                    shares = int(max_inv / price / 100) * 100
                    if shares >= 100:
                        if self.trade(stock, 'buy', shares, price, date):
                            avail = self.cash
    
    def run(self) -> dict:
        logger.info("=" * 80)
        logger.info("🎯 十倍股多因子策略 - 快速版")
        logger.info("=" * 80)
        
        self.load_data()
        
        if not self.trade_days or not self.price_cache:
            return {}
        
        logger.info(f"回测: {self.config.start_date} ~ {self.config.end_date}")
        logger.info(f"初始: {self.config.initial_cash:,.0f}")
        
        last_rb = -self.config.rebalance_days
        
        for idx, date in enumerate(self.trade_days):
            self.dates.append(date)
            self.risk_check(date)
            
            if idx - last_rb >= self.config.rebalance_days:
                self.rebalance(date)
                last_rb = idx
            
            pv = self.portfolio_value(date)
            self.equity_history.append(pv)
            
            dr = (pv / self.equity_history[-2] - 1) if len(self.equity_history) > 1 else 0
            self.daily_returns.append(dr)
            
            if idx % 50 == 0:
                gain = (pv / self.config.initial_cash - 1) * 100
                logger.info(f"   {idx+1}/{len(self.trade_days)} | {pv:,.0f} | {gain:.1f}% | {len(self.positions)}只")
        
        return self.calc_perf()
    
    def calc_perf(self) -> dict:
        res = {
            'total_return': 0, 'annual_return': 0, 'sharpe': 0, 'max_dd': 0,
            'calmar': 0, 'sortino': 0, 'trades': len(self.trade_history),
            'equity': self.equity_history, 'returns': self.daily_returns,
            'dates': self.dates, 'trade_history': self.trade_history
        }
        
        if not self.equity_history:
            return res
        
        res['total_return'] = self.equity_history[-1] / self.config.initial_cash - 1
        days = len(self.equity_history)
        if days > 1:
            res['annual_return'] = (1 + res['total_return']) ** (252/days) - 1
        
        ret = pd.Series(self.daily_returns)
        if len(ret) > 1 and ret.std() > 0:
            res['sharpe'] = ret.mean() / ret.std() * np.sqrt(252)
        
        eq = pd.Series(self.equity_history)
        peak = eq.cummax()
        dd = (eq - peak) / peak
        res['max_dd'] = dd.min()
        res['dd_curve'] = dd.tolist()
        
        if res['max_dd'] != 0:
            res['calmar'] = res['annual_return'] / abs(res['max_dd'])
        
        neg = ret[ret < 0]
        if len(neg) > 0 and neg.std() > 0:
            res['sortino'] = ret.mean() / neg.std() * np.sqrt(252)
        
        return res

# ============================================================
# 报告生成
# ============================================================

def make_chart(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return img

def make_charts(res, cfg):
    charts = {}
    if not MATPLOTLIB_AVAILABLE or not res.get('dates'):
        return charts
    
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in res['dates']]
    eq = res['equity']
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(dates, eq, lw=2.5, color='#667eea', label='Strategy')
    ax.axhline(y=cfg.initial_cash, color='gray', ls='--', alpha=0.5)
    ax.axhline(y=cfg.initial_cash * 10, color='red', ls='--', alpha=0.7, label='10x')
    ax.fill_between(dates, cfg.initial_cash, eq, alpha=0.3, color='#667eea')
    ax.set_title('Equity Curve', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    charts['equity'] = make_chart(fig)
    
    if res.get('dd_curve'):
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.fill_between(dates, [d*100 for d in res['dd_curve']], 0, color='#f56565', alpha=0.6)
        ax.set_title('Drawdown', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        charts['drawdown'] = make_chart(fig)
    
    return charts

def make_html(res, cfg, charts):
    chart_html = ""
    for k, img in charts.items():
        chart_html += f'<div class="chart"><img src="data:image/png;base64,{img}"></div>'
    
    rows = ""
    for t in res.get('trade_history', [])[-100:]:
        c = '#48bb78' if t['action'] == 'buy' else '#f56565'
        rows += f"<tr><td>{t['date']}</td><td>{t['stock']}</td><td style='color:{c}'>{t['action']}</td><td>{t['shares']:,}</td><td>{t['price']:.2f}</td></tr>"
    
    target = res['total_return'] >= 9.0
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>多因子策略回测报告</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; position: relative; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .status {{ position: absolute; top: 20px; right: 20px; background: {'#48bb78' if target else '#ed8936'}; padding: 10px 20px; border-radius: 30px; font-weight: bold; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }}
        .m {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .m .l {{ color: #aaa; font-size: 0.9em; }}
        .m .v {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .m .v.pos {{ color: #48bb78; }}
        .m .v.neg {{ color: #f56565; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="status">{'🏆 10X ACHIEVED!' if target else '📈 IN PROGRESS'}</div>
            <h1>🎯 多因子策略回测报告</h1>
            <p>基于历史10倍股特征的多因子选股模型</p>
            <p>{cfg.start_date} ~ {cfg.end_date} | 初始: ¥{cfg.initial_cash:,.0f}</p>
            <p>生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="m"><div class="l">总收益</div><div class="v {'pos' if res['total_return']>0 else 'neg'}">{res['total_return']*100:.1f}%</div></div>
            <div class="m"><div class="l">年化收益</div><div class="v {'pos' if res['annual_return']>0 else 'neg'}">{res['annual_return']*100:.1f}%</div></div>
            <div class="m"><div class="l">夏普比率</div><div class="v">{res['sharpe']:.2f}</div></div>
            <div class="m"><div class="l">最大回撤</div><div class="v neg">{res['max_dd']*100:.1f}%</div></div>
            <div class="m"><div class="l">卡玛比率</div><div class="v">{res['calmar']:.2f}</div></div>
            <div class="m"><div class="l">索提诺</div><div class="v">{res['sortino']:.2f}</div></div>
            <div class="m"><div class="l">交易次数</div><div class="v">{res['trades']}</div></div>
            <div class="m"><div class="l">倍数</div><div class="v {'pos' if res['total_return']>0 else 'neg'}">{res['total_return']+1:.2f}x</div></div>
        </div>
        
        <div class="section">
            <h2>📊 图表</h2>
            {chart_html}
        </div>
        
        <div class="section">
            <h2>📋 交易记录 (最近100笔)</h2>
            <table><tr><th>日期</th><th>股票</th><th>操作</th><th>数量</th><th>价格</th></tr>{rows}</table>
        </div>
    </div>
</body>
</html>"""

def main():
    print("=" * 80)
    print("🎯 十倍股多因子策略 - 快速版")
    print("=" * 80)
    
    cfg = Config()
    if len(sys.argv) > 1: cfg.start_date = sys.argv[1]
    if len(sys.argv) > 2: cfg.end_date = sys.argv[2]
    
    eng = FastMultifactor(cfg)
    if not eng.auth():
        return
    
    res = eng.run()
    if not res:
        return
    
    print("\n📊 生成图表...")
    charts = make_charts(res, cfg)
    
    print("📝 生成报告...")
    html = make_html(res, cfg, charts)
    
    rdir = PROJECT_ROOT / "reports"
    rdir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rpath = rdir / f"tenbagger_multifactor_fast_{ts}.html"
    
    with open(rpath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("=" * 80)
    print(f"✅ 完成!")
    print(f"📄 报告: {rpath}")
    print(f"📈 总收益: {res['total_return']*100:.1f}%")
    print(f"📈 倍数: {res['total_return']+1:.2f}x")
    print("=" * 80)
    
    jq.logout()

if __name__ == "__main__":
    main()

