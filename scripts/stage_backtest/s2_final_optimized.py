#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期策略 - 最终优化版

核心优化：
1. 市场择时：熊市不开仓，牛市满仓
2. PEG阈值：<1（原<2）
3. 利润增速：>30%（原>20%）
4. 默认2年持有期
5. -20%止损保护
6. 排除周期性行业
"""

import sys
import os

PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate


# ============================================================
# 配置
# ============================================================

class MarketRegime(Enum):
    BULL = "BULL"
    VOLATILE = "VOLATILE"  
    BEAR = "BEAR"


# 周期性行业（排除）
CYCLICAL_INDUSTRIES = [
    '有色金属', '钢铁', '化工', '采掘', '建筑材料',
    '建筑装饰', '房地产', '交通运输', '公用事业'
]

# 策略参数
CONFIG = {
    # 筛选条件
    'min_mcap': 30,           # 最小市值（亿）
    'max_mcap': 500,          # 最大市值（亿）
    'min_profit_growth': 0.30, # 最小利润增速（优化：从0.20提高到0.30）
    'min_roe': 0.12,          # 最小ROE
    'max_peg': 1.0,           # 最大PEG（优化：从2.0降到1.0）
    'max_pe': 100,            # 最大PE
    
    # 仓位管理
    'bull_position': 1.0,     # 牛市满仓
    'volatile_position': 0.5, # 震荡半仓
    'bear_position': 0.0,     # 熊市空仓（核心优化）
    
    # 止损
    'stop_loss': -0.20,       # -20%止损
    
    # 持有期
    'hold_days': 504,         # 默认2年（约504个交易日）
}


# ============================================================
# 市场环境判断
# ============================================================

def get_market_regime(date_str: str) -> MarketRegime:
    """判断市场环境
    
    使用沪深300的均线系统判断：
    - 牛市：价格>MA20>MA60
    - 熊市：价格<MA20<MA60
    - 震荡：其他
    """
    try:
        end_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=100)
        
        price = jq.get_price(
            '000300.XSHG',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=date_str,
            frequency='daily',
            fields=['close'],
            panel=False
        )
        
        if price is None or len(price) < 60:
            return MarketRegime.VOLATILE
        
        close = price['close']
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        current = close.iloc[-1]
        
        if current > ma20 > ma60:
            return MarketRegime.BULL
        elif current < ma20 < ma60:
            return MarketRegime.BEAR
        else:
            return MarketRegime.VOLATILE
            
    except Exception:
        return MarketRegime.VOLATILE


# ============================================================
# S2识别器（优化版）
# ============================================================

class OptimizedS2Identifier:
    """优化后的S2识别器"""
    
    def __init__(self):
        self.config = CONFIG
    
    def identify(self, market_cap: float, profit_growth: float, 
                 roe: float, pe: float, industry: str = '') -> Tuple[bool, float, str]:
        """识别S2阶段"""
        
        # 市值过滤
        if not (self.config['min_mcap'] <= market_cap <= self.config['max_mcap']):
            return False, 0, "市值不符"
        
        # 利润增速（核心条件）
        if profit_growth < self.config['min_profit_growth']:
            return False, 0, "利润增速不足"
        
        # ROE
        if roe < self.config['min_roe']:
            return False, 0, "ROE不足"
        
        # PE
        if pe <= 0 or pe > self.config['max_pe']:
            return False, 0, "PE不符"
        
        # PEG（核心优化）
        peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 99
        if peg > self.config['max_peg']:
            return False, 0, f"PEG过高({peg:.2f})"
        
        # 周期行业排除
        if industry and any(ind in industry for ind in CYCLICAL_INDUSTRIES):
            return False, 0, "周期行业"
        
        # 计算得分
        score = 50
        
        # 利润增速得分
        if profit_growth >= 0.50:
            score += 25
        elif profit_growth >= 0.40:
            score += 20
        else:
            score += 15
        
        # ROE得分
        if roe >= 0.20:
            score += 15
        elif roe >= 0.15:
            score += 10
        else:
            score += 5
        
        # PEG得分
        if peg < 0.5:
            score += 15
        elif peg < 0.8:
            score += 10
        else:
            score += 5
        
        # 市值得分（小市值加分）
        if market_cap < 100:
            score += 5
        
        reason = f"利润+{profit_growth*100:.0f}%, ROE{roe*100:.0f}%, PEG{peg:.2f}"
        return True, min(score, 100), reason


# ============================================================
# 数据获取
# ============================================================

def get_stocks_with_industry(date_str: str) -> pd.DataFrame:
    """获取股票及行业"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &
        ~all_stocks.index.str.startswith('8')
    ]
    
    codes = valid.index.tolist()
    industries = jq.get_industry(codes, date=date_str)
    
    valid = valid.copy()
    valid['industry'] = ''
    for code in codes:
        if code in industries:
            ind_info = industries[code]
            if 'sw_l1' in ind_info and 'industry_name' in ind_info['sw_l1']:
                valid.loc[code, 'industry'] = ind_info['sw_l1']['industry_name']
    
    return valid


def get_fundamentals(codes: List[str], date_str: str) -> pd.DataFrame:
    """获取基本面数据"""
    batch_size = 1000
    all_dfs = []
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i+batch_size]
        q = jq.query(
            jq.valuation.code,
            jq.valuation.market_cap,
            jq.valuation.pe_ratio,
            jq.indicator.roe,
            jq.indicator.inc_revenue_year_on_year,
            jq.indicator.inc_net_profit_year_on_year,
        ).filter(jq.valuation.code.in_(batch))
        
        df = jq.get_fundamentals(q, date=date_str)
        if df is not None and not df.empty:
            all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True).set_index('code')
    return pd.DataFrame()


def get_price_series(code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """获取价格序列"""
    try:
        price = jq.get_price(
            code,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False
        )
        if price is not None and len(price) > 0:
            # 确保有日期列
            price = price.reset_index()
            if 'index' in price.columns:
                price = price.rename(columns={'index': 'date'})
            return price
        return None
    except:
        return None


# ============================================================
# 回测引擎（带止损）
# ============================================================

@dataclass
class Position:
    code: str
    name: str
    entry_price: float
    entry_date: str
    shares: float
    industry: str
    score: float


@dataclass
class Trade:
    code: str
    name: str
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    return_pct: float
    reason: str
    hold_days: int


class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, initial_capital: float = 1000000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_curve = []
    
    def run(self, screen_date: str, candidates: List[dict], regime: MarketRegime) -> Dict:
        """运行回测"""
        
        # 根据市场环境决定仓位
        if regime == MarketRegime.BEAR:
            position_pct = CONFIG['bear_position']
            print(f"  熊市环境，空仓（仓位{position_pct*100:.0f}%）")
            return self._generate_summary()
        elif regime == MarketRegime.VOLATILE:
            position_pct = CONFIG['volatile_position']
            print(f"  震荡环境，半仓（仓位{position_pct*100:.0f}%）")
        else:
            position_pct = CONFIG['bull_position']
            print(f"  牛市环境，满仓（仓位{position_pct*100:.0f}%）")
        
        if not candidates or position_pct == 0:
            return self._generate_summary()
        
        # 选股：按得分排序，取前10只
        candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)[:10]
        
        # 分配资金
        invest_amount = self.capital * position_pct
        per_stock = invest_amount / len(candidates)
        
        # 开仓
        entry_date = self._get_next_trading_day(screen_date)
        
        for c in candidates:
            price = self._get_price_on_date(c['code'], entry_date)
            if price and price > 0:
                shares = per_stock / price
                self.positions[c['code']] = Position(
                    code=c['code'],
                    name=c['name'],
                    entry_price=price,
                    entry_date=entry_date,
                    shares=shares,
                    industry=c.get('industry', ''),
                    score=c['score']
                )
                self.capital -= shares * price
        
        print(f"  开仓{len(self.positions)}只股票，日期{entry_date}")
        
        # 模拟持有期（每日检查止损）
        hold_days = CONFIG['hold_days']
        current_date = datetime.strptime(entry_date, '%Y-%m-%d')
        end_date = current_date + timedelta(days=hold_days + 60)
        
        # 获取所有持仓的价格数据
        price_data = {}
        for code in list(self.positions.keys()):
            price_df = get_price_series(code, entry_date, end_date.strftime('%Y-%m-%d'))
            if price_df is not None:
                price_data[code] = price_df
        
        # 逐日检查止损
        check_days = 0
        while check_days < hold_days and self.positions:
            check_days += 1
            check_date = current_date + timedelta(days=check_days)
            check_date_str = check_date.strftime('%Y-%m-%d')
            
            for code in list(self.positions.keys()):
                if code not in self.positions:
                    continue
                
                pos = self.positions[code]
                
                if code in price_data:
                    df = price_data[code]
                    # 获取日期列（可能是'time', 'date', 或index）
                    date_col = 'time' if 'time' in df.columns else 'date' if 'date' in df.columns else df.index.name
                    if date_col and date_col in df.columns:
                        current_prices = df[df[date_col].astype(str).str[:10] <= check_date_str]
                    else:
                        # 使用index
                        df_copy = df.copy()
                        df_copy['_date'] = df_copy.index.astype(str).str[:10]
                        current_prices = df_copy[df_copy['_date'] <= check_date_str]
                    
                    if len(current_prices) > 0:
                        current_price = current_prices['close'].iloc[-1]
                        ret = (current_price - pos.entry_price) / pos.entry_price
                        
                        # 止损检查
                        if ret <= CONFIG['stop_loss']:
                            self._close_position(code, current_price, check_date_str, "止损")
        
        # 到期平仓
        final_date = (current_date + timedelta(days=hold_days)).strftime('%Y-%m-%d')
        for code in list(self.positions.keys()):
            if code in price_data:
                df = price_data[code]
                # 获取日期列
                date_col = 'time' if 'time' in df.columns else 'date' if 'date' in df.columns else None
                if date_col:
                    final_prices = df[df[date_col].astype(str).str[:10] <= final_date]
                else:
                    df_copy = df.copy()
                    df_copy['_date'] = df_copy.index.astype(str).str[:10]
                    final_prices = df_copy[df_copy['_date'] <= final_date]
                
                if len(final_prices) > 0:
                    final_price = final_prices['close'].iloc[-1]
                    self._close_position(code, final_price, final_date, "到期")
        
        return self._generate_summary()
    
    def _close_position(self, code: str, price: float, date: str, reason: str):
        """平仓"""
        if code not in self.positions:
            return
        
        pos = self.positions[code]
        ret = (price - pos.entry_price) / pos.entry_price
        
        entry_dt = datetime.strptime(pos.entry_date, '%Y-%m-%d')
        exit_dt = datetime.strptime(date, '%Y-%m-%d')
        hold_days = (exit_dt - entry_dt).days
        
        self.trades.append(Trade(
            code=pos.code,
            name=pos.name,
            entry_date=pos.entry_date,
            exit_date=date,
            entry_price=pos.entry_price,
            exit_price=price,
            return_pct=ret,
            reason=reason,
            hold_days=hold_days
        ))
        
        self.capital += pos.shares * price
        del self.positions[code]
    
    def _get_next_trading_day(self, date_str: str) -> str:
        """获取下一个交易日"""
        try:
            dates = jq.get_trade_days(start_date=date_str, count=5)
            if len(dates) > 1:
                return str(dates[1])
            return date_str
        except:
            return date_str
    
    def _get_price_on_date(self, code: str, date_str: str) -> Optional[float]:
        """获取某日收盘价"""
        try:
            price = jq.get_price(code, start_date=date_str, end_date=date_str, 
                                 frequency='daily', fields=['close'], panel=False)
            if price is not None and len(price) > 0:
                return price['close'].iloc[0]
            return None
        except:
            return None
    
    def _generate_summary(self) -> Dict:
        """生成回测摘要"""
        if not self.trades:
            return {
                'total_return': 0,
                'win_rate': 0,
                'avg_return': 0,
                'max_return': 0,
                'min_return': 0,
                'trade_count': 0,
                'stop_loss_count': 0,
                'trades': []
            }
        
        returns = [t.return_pct for t in self.trades]
        stop_loss_trades = [t for t in self.trades if t.reason == "止损"]
        
        return {
            'total_return': np.mean(returns),
            'win_rate': sum(1 for r in returns if r > 0) / len(returns),
            'avg_return': np.mean(returns),
            'max_return': np.max(returns),
            'min_return': np.min(returns),
            'trade_count': len(self.trades),
            'stop_loss_count': len(stop_loss_trades),
            'trades': self.trades
        }


# ============================================================
# 主回测流程
# ============================================================

def screen_stocks(date_str: str, stocks_df: pd.DataFrame) -> List[dict]:
    """筛选S2阶段股票"""
    identifier = OptimizedS2Identifier()
    
    codes = stocks_df.index.tolist()
    fundamentals = get_fundamentals(codes, date_str)
    
    results = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            
            industry = stocks_df.loc[code, 'industry'] if code in stocks_df.index else ''
            
            is_s2, score, reason = identifier.identify(market_cap, profit_growth, roe, pe, industry)
            
            if is_s2:
                name = stocks_df.loc[code, 'display_name'] if code in stocks_df.index else code
                peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 99
                
                results.append({
                    'code': code,
                    'name': name,
                    'industry': industry,
                    'market_cap': market_cap,
                    'profit_growth': profit_growth,
                    'roe': roe,
                    'pe': pe,
                    'peg': peg,
                    'score': score,
                    'reason': reason
                })
        except:
            continue
    
    return sorted(results, key=lambda x: x['score'], reverse=True)


def run_final_backtest():
    """运行最终优化版回测"""
    
    print("="*80)
    print("S2加速期策略 - 最终优化版回测")
    print("="*80)
    print("\n核心优化：")
    print(f"  1. 市场择时：熊市空仓({CONFIG['bear_position']*100:.0f}%), 牛市满仓({CONFIG['bull_position']*100:.0f}%)")
    print(f"  2. PEG阈值：<{CONFIG['max_peg']} (原<2)")
    print(f"  3. 利润增速：>{CONFIG['min_profit_growth']*100:.0f}% (原>20%)")
    print(f"  4. 默认持有期：{CONFIG['hold_days']}天（约2年）")
    print(f"  5. 止损：{CONFIG['stop_loss']*100:.0f}%")
    print()
    
    authenticate()
    
    screen_dates = ['2020-06-01', '2021-06-01', '2022-06-01', '2023-06-01', '2024-06-01']
    
    all_stats = []
    all_trades = []
    
    for screen_date in screen_dates:
        print(f"\n{'='*70}")
        print(f"筛选日期: {screen_date}")
        
        # 市场环境
        regime = get_market_regime(screen_date)
        print(f"市场环境: {regime.value}")
        print("="*70)
        
        # 获取股票
        stocks_df = get_stocks_with_industry(screen_date)
        print(f"有效股票: {len(stocks_df)} 只")
        
        # 筛选
        candidates = screen_stocks(screen_date, stocks_df)
        print(f"S2阶段股票: {len(candidates)} 只")
        
        if candidates:
            print(f"Top3候选:")
            for c in candidates[:3]:
                print(f"  {c['code']} {c['name']}: 得分{c['score']}, {c['reason']}")
        
        # 回测
        engine = BacktestEngine()
        result = engine.run(screen_date, candidates, regime)
        
        # 统计
        stats = {
            'year': screen_date[:4],
            'regime': regime.value,
            'candidates': len(candidates),
            'trades': result['trade_count'],
            'avg_return': result['avg_return'],
            'win_rate': result['win_rate'],
            'max_return': result['max_return'],
            'min_return': result['min_return'],
            'stop_loss_count': result['stop_loss_count']
        }
        all_stats.append(stats)
        
        if result['trade_count'] > 0:
            print(f"\n  回测结果:")
            print(f"    平均收益: {result['avg_return']*100:.2f}%")
            print(f"    胜率: {result['win_rate']*100:.1f}%")
            print(f"    止损次数: {result['stop_loss_count']}")
            
            all_trades.extend(result['trades'])
    
    # ============================================================
    # 汇总
    # ============================================================
    
    print("\n" + "="*80)
    print("5年汇总统计（最终优化版）")
    print("="*80)
    
    print("\n年度表现:")
    print("-"*90)
    print(f"{'年份':<6} {'环境':<10} {'候选':<8} {'交易':<8} {'平均收益':<12} {'胜率':<10} {'止损':<8}")
    print("-"*90)
    
    for stat in all_stats:
        if stat['trades'] > 0:
            print(f"{stat['year']:<6} {stat['regime']:<10} {stat['candidates']:<8} {stat['trades']:<8} "
                  f"{stat['avg_return']*100:>8.1f}%    {stat['win_rate']*100:>6.1f}%    {stat['stop_loss_count']:<8}")
        else:
            print(f"{stat['year']:<6} {stat['regime']:<10} {stat['candidates']:<8} {'空仓':<8} "
                  f"{'N/A':>8}     {'N/A':>6}     {0:<8}")
    
    # 高回报股票
    print("\n" + "="*80)
    print("交易明细")
    print("="*80)
    
    if all_trades:
        # 按收益排序
        all_trades_sorted = sorted(all_trades, key=lambda x: x.return_pct, reverse=True)
        
        # 翻倍股
        double_trades = [t for t in all_trades_sorted if t.return_pct > 1.0]
        print(f"\n翻倍股票（收益>100%）: {len(double_trades)} 只")
        for t in double_trades:
            print(f"  {t.code} {t.name}: +{t.return_pct*100:.1f}% ({t.entry_date}→{t.exit_date}, {t.hold_days}天)")
        
        # 高回报
        high_trades = [t for t in all_trades_sorted if t.return_pct > 0.5]
        print(f"\n高回报（>50%）: {len(high_trades)} 只")
        
        # 止损统计
        stop_loss_trades = [t for t in all_trades if t.reason == "止损"]
        print(f"\n止损次数: {len(stop_loss_trades)} 次")
        for t in stop_loss_trades[:5]:
            print(f"  {t.code} {t.name}: {t.return_pct*100:.1f}% ({t.entry_date}→{t.exit_date})")
        
        # 整体统计
        returns = [t.return_pct for t in all_trades]
        print(f"\n整体统计:")
        print(f"  总交易: {len(returns)} 笔")
        print(f"  平均收益: {np.mean(returns)*100:.2f}%")
        print(f"  胜率: {sum(1 for r in returns if r>0)/len(returns)*100:.1f}%")
        print(f"  最高收益: {np.max(returns)*100:.1f}%")
        print(f"  最低收益: {np.min(returns)*100:.1f}%")
    
    # 保存结果
    if all_trades:
        trades_df = pd.DataFrame([{
            'code': t.code,
            'name': t.name,
            'entry_date': t.entry_date,
            'exit_date': t.exit_date,
            'entry_price': t.entry_price,
            'exit_price': t.exit_price,
            'return_pct': t.return_pct,
            'reason': t.reason,
            'hold_days': t.hold_days
        } for t in all_trades])
        
        output_path = f'{PROJECT_ROOT}/results'
        os.makedirs(output_path, exist_ok=True)
        trades_df.to_csv(f'{output_path}/s2_final_optimized_trades.csv', index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {output_path}/s2_final_optimized_trades.csv")
    
    return all_stats, all_trades


if __name__ == '__main__':
    run_final_backtest()
