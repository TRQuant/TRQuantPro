"""
多因子高收益预测系统
目标：提前一周预测可能获得10%+收益的股票

核心理念：
1. 构建预测模型，而非描述模型
2. 多维度因子：基本面+技术面+资金面+情绪面
3. 完整的买卖规则和风控机制
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from config.config_manager import get_config_manager


class SignalStrength(Enum):
    STRONG_BUY = "强烈买入"
    BUY = "买入"
    HOLD = "持有"
    SELL = "卖出"
    STRONG_SELL = "强烈卖出"


@dataclass
class FactorScore:
    """因子评分"""
    fundamental: float = 0.0  # 基本面
    technical: float = 0.0    # 技术面
    sentiment: float = 0.0    # 情绪面/资金面
    event: float = 0.0        # 事件驱动
    total: float = 0.0        # 综合得分


@dataclass
class StockRecommendation:
    """股票推荐"""
    code: str
    name: str
    score: FactorScore
    signal: SignalStrength
    entry_price: float
    target_price: float
    stop_loss: float
    expected_return: float
    holding_days: int
    factors: Dict = field(default_factory=dict)


class MultiFactorPredictor:
    """多因子高收益预测器"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self._init_jqdata()
        
        # 因子权重配置
        self.factor_weights = {
            'fundamental': 0.20,
            'technical': 0.35,
            'sentiment': 0.30,
            'event': 0.15,
        }
        
        # 买卖规则配置
        self.trading_rules = {
            'target_return': 0.10,      # 目标收益10%
            'stop_loss': -0.05,         # 止损5%
            'trailing_stop': 0.03,      # 移动止损3%
            'max_holding_days': 5,      # 最大持有5天
            'position_size': 0.10,      # 单票仓位10%
            'max_positions': 10,        # 最多10只
        }
        
        # 风控规则
        self.risk_rules = {
            'max_industry_exposure': 0.30,  # 单行业最大30%
            'max_drawdown': 0.08,           # 最大回撤8%
            'min_liquidity': 1000,          # 最小成交额(万)
        }
    
    def _init_jqdata(self):
        """初始化JQData"""
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config.get('username'), jq_config.get('password'))
        if self.verbose:
            print("JQData连接成功")
    
    def get_stock_pool(self, date: str, min_cap: float = 30, max_cap: float = 500) -> List[str]:
        """获取股票池"""
        stocks = jq.get_all_securities(types=['stock'], date=date)
        # 排除ST和科创板
        stocks = stocks[~stocks.index.str.startswith('688')]
        stocks = stocks[~stocks['display_name'].str.contains('ST')]
        
        # 市值筛选
        q = jq.query(
            jq.valuation.code
        ).filter(
            jq.valuation.code.in_(stocks.index.tolist()),
            jq.valuation.market_cap.between(min_cap, max_cap),
        )
        df = jq.get_fundamentals(q, date=date)
        
        return df['code'].tolist() if df is not None else []
    
    def calculate_fundamental_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算基本面因子"""
        q = jq.query(
            jq.valuation.code,
            jq.valuation.market_cap,
            jq.valuation.pe_ratio,
            jq.valuation.pb_ratio,
            jq.valuation.ps_ratio,
            jq.indicator.roe,
            jq.indicator.inc_net_profit_year_on_year,
            jq.indicator.inc_revenue_year_on_year,
            jq.indicator.gross_profit_margin,
        ).filter(
            jq.valuation.code.in_(codes)
        )
        
        df = jq.get_fundamentals(q, date=date)
        if df is None or df.empty:
            return pd.DataFrame()
        
        # 计算PEG
        df['peg'] = df['pe_ratio'] / df['inc_net_profit_year_on_year'].replace(0, np.nan)
        df['peg'] = df['peg'].clip(-10, 10)
        
        # 基本面得分
        df['f_roe_score'] = df['roe'].clip(-20, 50).rank(pct=True) * 100
        df['f_growth_score'] = df['inc_net_profit_year_on_year'].clip(-100, 500).rank(pct=True) * 100
        df['f_rev_score'] = df['inc_revenue_year_on_year'].clip(-50, 200).rank(pct=True) * 100
        df['f_peg_score'] = (2 - df['peg'].clip(0, 2)).rank(pct=True) * 100  # PEG越低越好
        
        df['fundamental_score'] = (
            df['f_roe_score'] * 0.30 +
            df['f_growth_score'] * 0.35 +
            df['f_rev_score'] * 0.20 +
            df['f_peg_score'] * 0.15
        )
        
        return df
    
    def calculate_technical_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算技术面因子"""
        start_dt = datetime.strptime(date, '%Y-%m-%d')
        hist_start = start_dt - timedelta(days=60)
        
        prices = jq.get_price(
            codes,
            start_date=hist_start.strftime('%Y-%m-%d'),
            end_date=date,
            frequency='daily',
            fields=['close', 'high', 'low', 'volume', 'money'],
            panel=False,
            skip_paused=True,
            fq='post'
        )
        
        if prices is None or prices.empty:
            return pd.DataFrame()
        
        results = []
        for code in codes:
            code_df = prices[prices['code'] == code].reset_index(drop=True)
            if len(code_df) < 20:
                continue
            
            close = code_df['close']
            high = code_df['high']
            low = code_df['low']
            volume = code_df['volume']
            money = code_df['money']
            
            # 动量因子
            mom_5d = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
            mom_10d = (close.iloc[-1] / close.iloc[-10] - 1) * 100 if len(close) >= 10 else 0
            mom_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
            
            # 相对强度（vs 近期高低点）
            high_20 = high.tail(20).max()
            low_20 = low.tail(20).min()
            rel_strength = (close.iloc[-1] - low_20) / (high_20 - low_20) * 100 if high_20 != low_20 else 50
            
            # 突破因子
            high_60 = high.max()
            is_near_high = close.iloc[-1] >= high_60 * 0.95  # 距离60日高点5%以内
            
            # 放量因子
            avg_volume_5 = volume.tail(5).mean()
            avg_volume_20 = volume.tail(20).mean()
            volume_ratio = avg_volume_5 / avg_volume_20 if avg_volume_20 > 0 else 1
            
            # 成交额（流动性）
            avg_money = money.tail(5).mean() / 10000  # 万元
            
            # 波动率
            returns = close.pct_change().dropna()
            volatility = returns.tail(20).std() * np.sqrt(252) * 100
            
            # RSI
            delta = close.diff()
            gain = delta.where(delta > 0, 0).tail(14).mean()
            loss = (-delta.where(delta < 0, 0)).tail(14).mean()
            rsi = 100 - (100 / (1 + gain / loss)) if loss != 0 else 50
            
            results.append({
                'code': code,
                'mom_5d': mom_5d,
                'mom_10d': mom_10d,
                'mom_20d': mom_20d,
                'rel_strength': rel_strength,
                'is_near_high': is_near_high,
                'volume_ratio': volume_ratio,
                'avg_money': avg_money,
                'volatility': volatility,
                'rsi': rsi,
            })
        
        df = pd.DataFrame(results)
        if df.empty:
            return df
        
        # 技术面得分
        # 动量得分：适度动量最佳（5~25%）
        df['t_mom_score'] = 100 - np.abs(df['mom_20d'] - 15).clip(0, 50) * 2
        
        # 相对强度得分：中等位置（30~70%）最佳
        df['t_rs_score'] = 100 - np.abs(df['rel_strength'] - 50).clip(0, 50) * 2
        
        # 放量得分
        df['t_vol_score'] = df['volume_ratio'].clip(0.5, 3).rank(pct=True) * 100
        
        # RSI得分：40~60最佳
        df['t_rsi_score'] = 100 - np.abs(df['rsi'] - 50).clip(0, 30) * 3
        
        df['technical_score'] = (
            df['t_mom_score'] * 0.35 +
            df['t_rs_score'] * 0.25 +
            df['t_vol_score'] * 0.25 +
            df['t_rsi_score'] * 0.15
        )
        
        return df
    
    def calculate_sentiment_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算情绪/资金面因子"""
        results = []
        
        # 获取融资融券数据
        start_dt = datetime.strptime(date, '%Y-%m-%d')
        mtss_start = start_dt - timedelta(days=10)
        
        try:
            mtss = jq.get_mtss(codes, start_date=mtss_start.strftime('%Y-%m-%d'), end_date=date)
        except:
            mtss = None
        
        # 获取龙虎榜数据
        try:
            billboard = jq.get_billboard_list(stock_list=codes, end_date=date, count=10)
        except:
            billboard = None
        
        for code in codes:
            result = {'code': code}
            
            # 融资融券分析
            if mtss is not None and not mtss.empty:
                code_mtss = mtss[mtss['sec_code'] == code]
                if len(code_mtss) >= 2:
                    # 融资余额变化
                    fin_change = (code_mtss['fin_value'].iloc[-1] / code_mtss['fin_value'].iloc[0] - 1) * 100
                    result['fin_change'] = fin_change
                else:
                    result['fin_change'] = 0
            else:
                result['fin_change'] = 0
            
            # 龙虎榜分析
            if billboard is not None and not billboard.empty:
                code_bill = billboard[billboard['code'] == code]
                if len(code_bill) > 0:
                    result['billboard_count'] = len(code_bill)
                    result['on_billboard'] = 1
                else:
                    result['billboard_count'] = 0
                    result['on_billboard'] = 0
            else:
                result['billboard_count'] = 0
                result['on_billboard'] = 0
            
            results.append(result)
        
        df = pd.DataFrame(results)
        if df.empty:
            return df
        
        # 情绪得分
        df['s_fin_score'] = df['fin_change'].clip(-20, 20).rank(pct=True) * 100
        df['s_billboard_score'] = df['on_billboard'] * 50 + df['billboard_count'].clip(0, 5) * 10
        
        df['sentiment_score'] = (
            df['s_fin_score'] * 0.60 +
            df['s_billboard_score'] * 0.40
        )
        
        return df
    
    def calculate_event_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算事件驱动因子"""
        results = []
        
        # 获取股票所属概念
        for code in codes:
            try:
                concepts = jq.get_concept(code, date)
                concept_count = len(concepts) if concepts is not None else 0
                
                # 获取行业
                industry = jq.get_industry(code, date)
                industry_name = list(industry.get(code, {}).get('sw_l1', {}).values())[0] if industry else '未知'
            except:
                concept_count = 0
                industry_name = '未知'
            
            results.append({
                'code': code,
                'concept_count': concept_count,
                'industry': industry_name,
            })
        
        df = pd.DataFrame(results)
        if df.empty:
            return df
        
        # 概念热度得分
        df['e_concept_score'] = df['concept_count'].clip(0, 20).rank(pct=True) * 100
        
        df['event_score'] = df['e_concept_score']
        
        return df
    
    def get_recommendations(self, date: str, top_n: int = 10) -> List[StockRecommendation]:
        """获取推荐股票"""
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"【多因子选股】日期: {date}")
            print(f"{'='*60}")
        
        # 获取股票池
        codes = self.get_stock_pool(date)
        if self.verbose:
            print(f"股票池: {len(codes)} 只")
        
        if len(codes) == 0:
            return []
        
        # 分批处理
        batch_size = 300
        all_results = []
        
        for i in range(0, len(codes), batch_size):
            batch_codes = codes[i:i+batch_size]
            
            # 计算各维度因子
            fundamental_df = self.calculate_fundamental_factors(batch_codes, date)
            technical_df = self.calculate_technical_factors(batch_codes, date)
            sentiment_df = self.calculate_sentiment_factors(batch_codes, date)
            event_df = self.calculate_event_factors(batch_codes, date)
            
            # 合并
            if fundamental_df.empty or technical_df.empty:
                continue
            
            df = fundamental_df[['code', 'market_cap', 'roe', 'inc_net_profit_year_on_year', 'fundamental_score']]
            df = df.merge(technical_df[['code', 'mom_5d', 'mom_20d', 'rel_strength', 'avg_money', 'technical_score']], on='code', how='inner')
            
            if not sentiment_df.empty:
                df = df.merge(sentiment_df[['code', 'fin_change', 'on_billboard', 'sentiment_score']], on='code', how='left')
                df['sentiment_score'] = df['sentiment_score'].fillna(50)
            else:
                df['sentiment_score'] = 50
            
            if not event_df.empty:
                df = df.merge(event_df[['code', 'concept_count', 'industry', 'event_score']], on='code', how='left')
                df['event_score'] = df['event_score'].fillna(50)
            else:
                df['event_score'] = 50
            
            all_results.append(df)
        
        if not all_results:
            return []
        
        df = pd.concat(all_results, ignore_index=True)
        
        # 计算综合得分
        df['total_score'] = (
            df['fundamental_score'] * self.factor_weights['fundamental'] +
            df['technical_score'] * self.factor_weights['technical'] +
            df['sentiment_score'] * self.factor_weights['sentiment'] +
            df['event_score'] * self.factor_weights['event']
        )
        
        # 流动性过滤
        df = df[df['avg_money'] >= self.risk_rules['min_liquidity']]
        
        # 排序选取TOP N
        df = df.nlargest(top_n * 2, 'total_score')
        
        # 行业分散
        if 'industry' in df.columns:
            industry_count = df.groupby('industry').cumcount()
            df = df[industry_count < 3]  # 每个行业最多3只
        
        df = df.head(top_n)
        
        if self.verbose:
            print(f"筛选结果: {len(df)} 只")
        
        # 生成推荐
        recommendations = []
        for _, row in df.iterrows():
            try:
                sec_info = jq.get_security_info(row['code'])
                name = sec_info.display_name if sec_info else row['code']
            except:
                name = row['code']
            
            # 获取当前价格
            current_price = jq.get_price(row['code'], end_date=date, count=1, fields=['close'])
            entry_price = current_price['close'].iloc[0] if current_price is not None and len(current_price) > 0 else 0
            
            score = FactorScore(
                fundamental=row['fundamental_score'],
                technical=row['technical_score'],
                sentiment=row['sentiment_score'],
                event=row['event_score'],
                total=row['total_score'],
            )
            
            # 确定信号强度
            if row['total_score'] >= 75:
                signal = SignalStrength.STRONG_BUY
            elif row['total_score'] >= 60:
                signal = SignalStrength.BUY
            else:
                signal = SignalStrength.HOLD
            
            rec = StockRecommendation(
                code=row['code'],
                name=name,
                score=score,
                signal=signal,
                entry_price=entry_price,
                target_price=entry_price * (1 + self.trading_rules['target_return']),
                stop_loss=entry_price * (1 + self.trading_rules['stop_loss']),
                expected_return=self.trading_rules['target_return'] * 100,
                holding_days=self.trading_rules['max_holding_days'],
                factors={
                    'roe': row.get('roe', 0),
                    'growth': row.get('inc_net_profit_year_on_year', 0),
                    'mom_20d': row.get('mom_20d', 0),
                    'rel_strength': row.get('rel_strength', 0),
                    'industry': row.get('industry', '未知'),
                }
            )
            recommendations.append(rec)
        
        return recommendations
    
    def backtest(self, start_date: str, end_date: str, top_n: int = 10) -> pd.DataFrame:
        """回测验证"""
        print(f"\n{'='*80}")
        print(f"【多因子策略回测】")
        print(f"回测期间: {start_date} ~ {end_date}")
        print(f"{'='*80}")
        
        # 生成回测日期（每周一）
        dates = pd.date_range(start=start_date, end=end_date, freq='W-MON').strftime('%Y-%m-%d').tolist()
        print(f"回测周期: {len(dates)} 周")
        
        all_trades = []
        
        for date in dates:
            print(f"\n回测日期: {date}")
            
            # 获取推荐
            recommendations = self.get_recommendations(date, top_n=top_n)
            
            if not recommendations:
                print("  无推荐")
                continue
            
            # 计算实际收益
            start_dt = datetime.strptime(date, '%Y-%m-%d')
            end_dt = start_dt + timedelta(days=8)
            
            for rec in recommendations:
                try:
                    prices = jq.get_price(
                        rec.code,
                        start_date=date,
                        end_date=end_dt.strftime('%Y-%m-%d'),
                        frequency='daily',
                        fields=['close', 'high', 'low'],
                        skip_paused=True,
                        fq='post'
                    )
                    
                    if prices is None or len(prices) < 2:
                        continue
                    
                    entry_price = prices['close'].iloc[0]
                    
                    # 模拟交易（含止盈止损）
                    exit_price = None
                    exit_day = None
                    exit_reason = 'hold'
                    
                    for day in range(1, min(6, len(prices))):
                        high = prices['high'].iloc[day]
                        low = prices['low'].iloc[day]
                        close = prices['close'].iloc[day]
                        
                        # 检查止损
                        if low <= entry_price * (1 + self.trading_rules['stop_loss']):
                            exit_price = entry_price * (1 + self.trading_rules['stop_loss'])
                            exit_day = day
                            exit_reason = 'stop_loss'
                            break
                        
                        # 检查止盈
                        if high >= entry_price * (1 + self.trading_rules['target_return']):
                            exit_price = entry_price * (1 + self.trading_rules['target_return'])
                            exit_day = day
                            exit_reason = 'take_profit'
                            break
                    
                    # 如果没有触发止盈止损，按第5天收盘价退出
                    if exit_price is None:
                        exit_day = min(5, len(prices) - 1)
                        exit_price = prices['close'].iloc[exit_day]
                        exit_reason = 'time_exit'
                    
                    ret = (exit_price / entry_price - 1) * 100
                    
                    # 获取基准收益
                    bench = jq.get_price('000300.XSHG', start_date=date, end_date=end_dt.strftime('%Y-%m-%d'),
                                        frequency='daily', fields=['close'], fq='post')
                    bench_ret = (bench['close'].iloc[min(5, len(bench)-1)] / bench['close'].iloc[0] - 1) * 100 if len(bench) > 1 else 0
                    
                    all_trades.append({
                        'date': date,
                        'code': rec.code,
                        'name': rec.name,
                        'total_score': rec.score.total,
                        'fundamental_score': rec.score.fundamental,
                        'technical_score': rec.score.technical,
                        'sentiment_score': rec.score.sentiment,
                        'event_score': rec.score.event,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'exit_day': exit_day,
                        'exit_reason': exit_reason,
                        'return': ret,
                        'bench_return': bench_ret,
                        'alpha': ret - bench_ret,
                        'industry': rec.factors.get('industry', '未知'),
                    })
                    
                except Exception as e:
                    continue
            
            print(f"  完成: {len([t for t in all_trades if t['date'] == date])} 笔交易")
        
        if not all_trades:
            print("无交易记录")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_trades)
        
        # 统计结果
        print(f"\n{'='*80}")
        print(f"【回测结果汇总】")
        print(f"{'='*80}")
        
        total_trades = len(df)
        avg_return = df['return'].mean()
        avg_alpha = df['alpha'].mean()
        win_rate = (df['return'] > 0).mean()
        alpha_rate = (df['alpha'] > 0).mean()
        hit_10 = (df['return'] >= 10).mean()
        hit_5 = (df['return'] >= 5).mean()
        
        print(f"\n总交易数: {total_trades}")
        print(f"平均收益: {avg_return:.2f}%")
        print(f"平均超额收益: {avg_alpha:.2f}%")
        print(f"盈利率: {win_rate:.1%}")
        print(f"超额盈利率: {alpha_rate:.1%}")
        print(f"10%+命中率: {hit_10:.1%}")
        print(f"5%+命中率: {hit_5:.1%}")
        
        # 按退出原因统计
        print(f"\n【按退出原因】")
        for reason in df['exit_reason'].unique():
            reason_df = df[df['exit_reason'] == reason]
            print(f"  {reason}: {len(reason_df)}笔 ({len(reason_df)/total_trades:.1%}) | 平均收益: {reason_df['return'].mean():.2f}%")
        
        # 按因子得分分组分析
        print(f"\n【按总得分分组】")
        df['score_group'] = pd.cut(df['total_score'], bins=[0, 60, 70, 80, 100], labels=['<60', '60-70', '70-80', '>80'])
        for group in df['score_group'].unique():
            if pd.isna(group):
                continue
            group_df = df[df['score_group'] == group]
            print(f"  {group}: {len(group_df)}笔 | 平均收益: {group_df['return'].mean():.2f}% | 10%+率: {(group_df['return']>=10).mean():.1%}")
        
        # 夏普比率
        vol = df['return'].std()
        sharpe = (avg_return - 0.1) / vol if vol > 0 else 0
        print(f"\n夏普比率: {sharpe:.3f}")
        
        return df


def main():
    """主函数"""
    predictor = MultiFactorPredictor(verbose=True)
    
    # 回测验证
    results = predictor.backtest(
        start_date='2025-09-30',
        end_date='2025-12-31',
        top_n=10
    )
    
    if not results.empty:
        results.to_csv('results/multi_factor_backtest.csv', index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: results/multi_factor_backtest.csv")


if __name__ == '__main__':
    main()
