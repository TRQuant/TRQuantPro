#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股策略验证与推荐报告生成器
==============================

基于彼得·林奇十倍股理论的4维评分系统：
- 基本面 (40%): ROE, 毛利率, 净利率, 负债率
- 成长性 (30%): 营收增速, 净利润增速
- 估值 (15%): PEG, PE, 市值
- 技术面 (15%): 动量, 成交量, 价格位置

输出：多Tab HTML报告 + 3-5个具体推荐标的
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
import numpy as np
import logging

# 添加项目根目录到path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


# ============== 十倍股评分系统 ==============

class TenbaggerScoringEngine:
    """十倍股4维评分引擎"""
    
    WEIGHTS = {
        'fundamental': 0.40,  # 基本面
        'growth': 0.30,       # 成长性
        'valuation': 0.15,    # 估值
        'technical': 0.15     # 技术面
    }
    
    @staticmethod
    def score_fundamental(roe: float, gross_margin: float, 
                          net_margin: float, debt_ratio: float) -> Tuple[float, Dict]:
        """基本面评分 (0-100)"""
        score = 0
        details = {}
        
        # ROE评分 (40分)
        if roe >= 0.30:
            roe_score = 40
        elif roe >= 0.20:
            roe_score = 30
        elif roe >= 0.15:
            roe_score = 20
        elif roe >= 0.10:
            roe_score = 10
        else:
            roe_score = 0
        score += roe_score
        details['roe'] = {'value': roe, 'score': roe_score, 'max': 40}
        
        # 毛利率评分 (25分)
        if gross_margin >= 0.50:
            gm_score = 25
        elif gross_margin >= 0.40:
            gm_score = 20
        elif gross_margin >= 0.30:
            gm_score = 15
        elif gross_margin >= 0.20:
            gm_score = 10
        else:
            gm_score = 0
        score += gm_score
        details['gross_margin'] = {'value': gross_margin, 'score': gm_score, 'max': 25}
        
        # 负债率评分 (20分) - 越低越好
        if debt_ratio <= 0.30:
            debt_score = 20
        elif debt_ratio <= 0.45:
            debt_score = 15
        elif debt_ratio <= 0.60:
            debt_score = 10
        elif debt_ratio <= 0.70:
            debt_score = 5
        else:
            debt_score = 0
        score += debt_score
        details['debt_ratio'] = {'value': debt_ratio, 'score': debt_score, 'max': 20}
        
        # 净利率评分 (15分)
        if net_margin >= 0.20:
            nm_score = 15
        elif net_margin >= 0.15:
            nm_score = 12
        elif net_margin >= 0.10:
            nm_score = 8
        elif net_margin >= 0.05:
            nm_score = 4
        else:
            nm_score = 0
        score += nm_score
        details['net_margin'] = {'value': net_margin, 'score': nm_score, 'max': 15}
        
        return score, details

    @staticmethod
    def score_growth(revenue_growth: float, profit_growth: float) -> Tuple[float, Dict]:
        """成长性评分 (0-100)"""
        score = 0
        details = {}
        
        # 营收增速评分 (40分)
        if revenue_growth >= 0.50:
            rg_score = 40
        elif revenue_growth >= 0.30:
            rg_score = 30
        elif revenue_growth >= 0.20:
            rg_score = 20
        elif revenue_growth >= 0.10:
            rg_score = 10
        else:
            rg_score = 0
        score += rg_score
        details['revenue_growth'] = {'value': revenue_growth, 'score': rg_score, 'max': 40}
        
        # 净利润增速评分 (60分) - 最重要
        if profit_growth >= 1.00:
            pg_score = 60
        elif profit_growth >= 0.50:
            pg_score = 50
        elif profit_growth >= 0.30:
            pg_score = 40
        elif profit_growth >= 0.20:
            pg_score = 25
        elif profit_growth >= 0.10:
            pg_score = 10
        else:
            pg_score = 0
        score += pg_score
        details['profit_growth'] = {'value': profit_growth, 'score': pg_score, 'max': 60}
        
        return score, details

    @staticmethod
    def score_valuation(peg: float, pe: float, market_cap: float) -> Tuple[float, Dict]:
        """估值评分 (0-100)"""
        score = 0
        details = {}
        
        # PEG评分 (50分) - 核心
        if 0 < peg <= 0.5:
            peg_score = 50
        elif peg <= 0.8:
            peg_score = 40
        elif peg <= 1.0:
            peg_score = 30
        elif peg <= 1.5:
            peg_score = 15
        else:
            peg_score = 0
        score += peg_score
        details['peg'] = {'value': peg, 'score': peg_score, 'max': 50}
        
        # PE评分 (25分)
        if 10 <= pe <= 25:
            pe_score = 25
        elif 25 < pe <= 35:
            pe_score = 18
        elif 35 < pe <= 50:
            pe_score = 10
        elif 5 <= pe < 10:
            pe_score = 15
        else:
            pe_score = 0
        score += pe_score
        details['pe'] = {'value': pe, 'score': pe_score, 'max': 25}
        
        # 市值评分 (25分) - 小市值加分
        if 30 <= market_cap <= 100:
            mc_score = 25
        elif 100 < market_cap <= 300:
            mc_score = 20
        elif 300 < market_cap <= 500:
            mc_score = 12
        elif 500 < market_cap <= 1000:
            mc_score = 5
        else:
            mc_score = 0
        score += mc_score
        details['market_cap'] = {'value': market_cap, 'score': mc_score, 'max': 25}
        
        return score, details

    @staticmethod
    def score_technical(momentum_20d: float, volume_ratio: float, 
                        price_position: float) -> Tuple[float, Dict]:
        """技术面评分 (0-100)"""
        score = 0
        details = {}
        
        # 动量评分 (40分)
        if momentum_20d >= 0.15:
            mom_score = 40
        elif momentum_20d >= 0.08:
            mom_score = 30
        elif momentum_20d >= 0.03:
            mom_score = 20
        elif momentum_20d >= 0:
            mom_score = 10
        else:
            mom_score = 0
        score += mom_score
        details['momentum'] = {'value': momentum_20d, 'score': mom_score, 'max': 40}
        
        # 成交量评分 (30分)
        if volume_ratio >= 2.0:
            vol_score = 30
        elif volume_ratio >= 1.5:
            vol_score = 25
        elif volume_ratio >= 1.2:
            vol_score = 20
        elif volume_ratio >= 1.0:
            vol_score = 10
        else:
            vol_score = 0
        score += vol_score
        details['volume_ratio'] = {'value': volume_ratio, 'score': vol_score, 'max': 30}
        
        # 价格位置评分 (30分)
        if 0.3 <= price_position <= 0.6:
            pos_score = 30
        elif 0.2 <= price_position < 0.3:
            pos_score = 25
        elif 0.6 < price_position <= 0.7:
            pos_score = 20
        elif price_position < 0.2:
            pos_score = 15
        else:
            pos_score = 0
        score += pos_score
        details['price_position'] = {'value': price_position, 'score': pos_score, 'max': 30}
        
        return score, details

    @classmethod
    def calculate_total(cls, fund: float, growth: float, 
                        val: float, tech: float) -> float:
        """计算加权总分"""
        return (fund * cls.WEIGHTS['fundamental'] +
                growth * cls.WEIGHTS['growth'] +
                val * cls.WEIGHTS['valuation'] +
                tech * cls.WEIGHTS['technical'])

    @staticmethod
    def determine_stage(market_cap: float, revenue_growth: float,
                        profit_growth: float, roe: float) -> str:
        """确定成长阶段"""
        if profit_growth < 0 and revenue_growth < 0.05:
            return "S5_衰退"
        if market_cap < 30:
            return "S0_种子"
        elif market_cap < 100:
            if profit_growth >= 0.50 or revenue_growth >= 0.30:
                return "S1_萌芽"
            else:
                return "S0_种子"
        elif market_cap < 300:
            if profit_growth >= 0.30 and roe >= 0.15:
                return "S2_加速 ⭐"
            else:
                return "S1_萌芽"
        elif market_cap < 1000:
            if profit_growth >= 0.20:
                return "S3_扩张"
            else:
                return "S4_成熟"
        else:
            return "S4_成熟"


# ============== 数据获取 ==============

class TenbaggerDataFetcher:
    """十倍股数据获取器"""
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
    
    def _init_jqdata(self):
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            if jq_config:
                jq.auth(jq_config['username'], jq_config['password'])
                if jq.is_auth():
                    self.jq = jq
                    print("✅ JQData 已连接")
        except Exception as e:
            logger.warning(f"JQData连接失败: {e}")
    
    def get_universe(self, date: str, min_market_cap: float = 30,
                     max_market_cap: float = 500) -> List[str]:
        """获取候选股票池"""
        if not self.jq:
            return []
        
        try:
            # 获取所有A股
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            all_codes = stocks.index.tolist()
            
            # 过滤ST
            st_list = self.jq.get_extras('is_st', all_codes, 
                                          start_date=date, end_date=date, df=True)
            if not st_list.empty:
                st_stocks = st_list.iloc[-1][st_list.iloc[-1] == True].index.tolist()
                all_codes = [c for c in all_codes if c not in st_stocks]
            
            # 过滤市值
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.market_cap
            ).filter(
                self.jq.valuation.code.in_(all_codes),
                self.jq.valuation.market_cap >= min_market_cap,
                self.jq.valuation.market_cap <= max_market_cap
            )
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is not None and not df.empty:
                return df['code'].tolist()
            return []
        except Exception as e:
            logger.warning(f"获取股票池失败: {e}")
            return []
    
    def get_financial_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """获取财务数据"""
        if not self.jq or not stocks:
            return pd.DataFrame()
        
        try:
            # 财务指标
            q = self.jq.query(
                self.jq.indicator.code,
                self.jq.indicator.roe,
                self.jq.indicator.gross_profit_margin,
                self.jq.indicator.net_profit_margin,
                self.jq.indicator.inc_revenue_year_on_year,
                self.jq.indicator.inc_net_profit_year_on_year,
            ).filter(
                self.jq.indicator.code.in_(stocks)
            )
            fin_df = self.jq.get_fundamentals(q, date=date)
            
            # 估值数据
            q2 = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.pe_ratio,
                self.jq.valuation.pb_ratio,
                self.jq.valuation.market_cap,
            ).filter(
                self.jq.valuation.code.in_(stocks)
            )
            val_df = self.jq.get_fundamentals(q2, date=date)
            
            # 负债率
            q3 = self.jq.query(
                self.jq.balance.code,
                self.jq.balance.total_liability,
                self.jq.balance.total_assets,
            ).filter(
                self.jq.balance.code.in_(stocks)
            )
            bal_df = self.jq.get_fundamentals(q3, date=date)
            
            if fin_df is None or fin_df.empty:
                return pd.DataFrame()
            
            # 合并
            df = fin_df.copy()
            if val_df is not None and not val_df.empty:
                df = df.merge(val_df, on='code', how='left')
            if bal_df is not None and not bal_df.empty:
                bal_df['debt_ratio'] = bal_df['total_liability'] / bal_df['total_assets'].replace(0, np.nan)
                df = df.merge(bal_df[['code', 'debt_ratio']], on='code', how='left')
            
            return df
        except Exception as e:
            logger.warning(f"获取财务数据失败: {e}")
            return pd.DataFrame()
    
    def get_technical_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """获取技术面数据"""
        if not self.jq or not stocks:
            return pd.DataFrame()
        
        results = []
        end_date = datetime.strptime(date, '%Y-%m-%d')
        start_date = end_date - timedelta(days=300)
        
        # 批量获取
        try:
            for code in stocks[:200]:  # 限制数量
                try:
                    df = self.jq.get_price(
                        code,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=date,
                        frequency='daily',
                        fields=['close', 'volume', 'high', 'low'],
                        skip_paused=True
                    )
                    if df is None or len(df) < 60:
                        continue
                    
                    # 20日动量
                    mom_20d = df['close'].iloc[-1] / df['close'].iloc[-20] - 1 if len(df) >= 20 else 0
                    
                    # 成交量比
                    vol_ratio = df['volume'].iloc[-5:].mean() / df['volume'].iloc[-60:].mean() \
                                if df['volume'].iloc[-60:].mean() > 0 else 1
                    
                    # 价格位置 (52周)
                    year_data = df.tail(252) if len(df) >= 252 else df
                    high_52w = year_data['high'].max()
                    low_52w = year_data['low'].min()
                    curr_price = df['close'].iloc[-1]
                    price_pos = (curr_price - low_52w) / (high_52w - low_52w) \
                                if high_52w > low_52w else 0.5
                    
                    results.append({
                        'code': code,
                        'momentum_20d': mom_20d,
                        'volume_ratio': vol_ratio,
                        'price_position': price_pos,
                        'close': curr_price
                    })
                except:
                    continue
            
            return pd.DataFrame(results)
        except Exception as e:
            logger.warning(f"获取技术数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, codes: List[str]) -> Dict[str, Dict]:
        """获取股票基本信息"""
        if not self.jq:
            return {}
        try:
            info = self.jq.get_all_securities(types=['stock'])
            result = {}
            for code in codes:
                if code in info.index:
                    result[code] = {
                        'name': info.loc[code, 'display_name'],
                        'industry': self._get_industry(code)
                    }
            return result
        except:
            return {}
    
    def _get_industry(self, code: str) -> str:
        """获取行业"""
        try:
            ind = self.jq.get_industry(code)
            if ind and code in ind:
                sw = ind[code].get('sw_l1', {})
                return sw.get('industry_name', '未知')
        except:
            pass
        return '未知'


# ============== 报告生成 ==============

class TenbaggerReportGenerator:
    """十倍股多Tab HTML报告生成器"""
    
    def __init__(self):
        self.fetcher = TenbaggerDataFetcher()
        self.engine = TenbaggerScoringEngine()
    
    def run_screening(self, date: str = None, top_n: int = 5) -> Tuple[pd.DataFrame, Dict]:
        """执行筛选"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            if self.fetcher.jq:
                # 获取最近交易日
                trade_days = self.fetcher.jq.get_trade_days(
                    end_date=date, count=5
                )
                if len(trade_days) > 0:
                    date = trade_days[-1].strftime('%Y-%m-%d')
        
        print(f"📅 分析日期: {date}")
        
        # 获取候选池
        print("🔎 筛选候选股票池 (市值30-500亿)...")
        universe = self.fetcher.get_universe(date, min_market_cap=30, max_market_cap=500)
        print(f"   候选数量: {len(universe)}")
        
        if not universe:
            return pd.DataFrame(), {}
        
        # 获取数据
        print("📊 获取财务数据...")
        fin_df = self.fetcher.get_financial_data(universe, date)
        print(f"   财务数据: {len(fin_df)} 条")
        
        print("📈 获取技术数据...")
        tech_df = self.fetcher.get_technical_data(universe[:200], date)
        print(f"   技术数据: {len(tech_df)} 条")
        
        if fin_df.empty or tech_df.empty:
            return pd.DataFrame(), {}
        
        # 合并数据
        df = fin_df.merge(tech_df, on='code', how='inner')
        df = df.dropna(subset=['roe', 'pe_ratio', 'market_cap', 'momentum_20d'])
        
        # 计算PEG
        df['profit_growth'] = df['inc_net_profit_year_on_year'].fillna(0) / 100
        df['revenue_growth'] = df['inc_revenue_year_on_year'].fillna(0) / 100
        df['peg'] = df.apply(
            lambda r: r['pe_ratio'] / (r['profit_growth'] * 100) 
            if r['profit_growth'] > 0 and r['pe_ratio'] > 0 else 99, axis=1
        )
        
        # 数据清洗
        df['roe'] = df['roe'].fillna(0) / 100
        df['gross_margin'] = df['gross_profit_margin'].fillna(0) / 100
        df['net_margin'] = df['net_profit_margin'].fillna(0) / 100
        df['debt_ratio'] = df['debt_ratio'].fillna(0.5)
        
        print("🧮 计算十倍股评分...")
        
        # 计算评分
        results = []
        for _, row in df.iterrows():
            try:
                # 基本面
                fund_score, fund_detail = self.engine.score_fundamental(
                    row['roe'], row['gross_margin'], 
                    row['net_margin'], row['debt_ratio']
                )
                # 成长性
                growth_score, growth_detail = self.engine.score_growth(
                    row['revenue_growth'], row['profit_growth']
                )
                # 估值
                val_score, val_detail = self.engine.score_valuation(
                    row['peg'], row['pe_ratio'], row['market_cap']
                )
                # 技术面
                tech_score, tech_detail = self.engine.score_technical(
                    row['momentum_20d'], row['volume_ratio'], row['price_position']
                )
                
                # 总分
                total = self.engine.calculate_total(
                    fund_score, growth_score, val_score, tech_score
                )
                
                # 阶段
                stage = self.engine.determine_stage(
                    row['market_cap'], row['revenue_growth'],
                    row['profit_growth'], row['roe']
                )
                
                results.append({
                    'code': row['code'],
                    'total_score': total,
                    'fund_score': fund_score,
                    'growth_score': growth_score,
                    'val_score': val_score,
                    'tech_score': tech_score,
                    'stage': stage,
                    'fund_detail': fund_detail,
                    'growth_detail': growth_detail,
                    'val_detail': val_detail,
                    'tech_detail': tech_detail,
                    # 原始数据
                    'roe': row['roe'],
                    'gross_margin': row['gross_margin'],
                    'net_margin': row['net_margin'],
                    'debt_ratio': row['debt_ratio'],
                    'revenue_growth': row['revenue_growth'],
                    'profit_growth': row['profit_growth'],
                    'pe': row['pe_ratio'],
                    'peg': row['peg'],
                    'market_cap': row['market_cap'],
                    'momentum_20d': row['momentum_20d'],
                    'volume_ratio': row['volume_ratio'],
                    'price_position': row['price_position'],
                    'close': row['close'],
                })
            except Exception as e:
                continue
        
        result_df = pd.DataFrame(results)
        
        # 排序，取Top N
        result_df = result_df.sort_values('total_score', ascending=False)
        
        # 基本条件过滤
        result_df = result_df[
            (result_df['growth_score'] >= 30) &
            (result_df['fund_score'] >= 25) &
            (~result_df['stage'].str.contains('衰退|成熟'))
        ]
        
        top_df = result_df.head(top_n)
        
        # 获取股票名称
        stock_info = self.fetcher.get_stock_info(top_df['code'].tolist())
        top_df['name'] = top_df['code'].map(lambda x: stock_info.get(x, {}).get('name', ''))
        top_df['industry'] = top_df['code'].map(lambda x: stock_info.get(x, {}).get('industry', ''))
        
        meta = {
            'date': date,
            'universe_count': len(universe),
            'scored_count': len(result_df),
            'weights': self.engine.WEIGHTS
        }
        
        print(f"✅ 筛选完成，推荐 {len(top_df)} 只标的")
        
        return top_df, meta
    
    def generate_html(self, df: pd.DataFrame, meta: Dict, 
                      output_path: str = None) -> str:
        """生成多Tab HTML报告"""
        if output_path is None:
            output_dir = PROJECT_ROOT / 'output' / 'reports'
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = str(output_dir / f'tenbagger_report_{timestamp}.html')
        
        # 生成HTML
        html = self._build_html(df, meta)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def _build_html(self, df: pd.DataFrame, meta: Dict) -> str:
        """构建HTML内容"""
        
        # Tab数据
        overview_html = self._build_overview_tab(df, meta)
        fundamental_html = self._build_fundamental_tab(df)
        growth_html = self._build_growth_tab(df)
        valuation_html = self._build_valuation_tab(df)
        technical_html = self._build_technical_tab(df)
        individual_html = self._build_individual_tab(df)
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股策略推荐报告 - {meta.get("date", "")}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        .header {{
            background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(233,69,96,0.3);
        }}
        .header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 1.1em; }}
        
        .tabs {{
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .tab-btn {{
            padding: 12px 24px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 8px 8px 0 0;
            color: #e8e8e8;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.2); }}
        .tab-btn.active {{
            background: linear-gradient(90deg, #e94560, #ff6b6b);
            color: white;
        }}
        
        .tab-content {{
            display: none;
            background: rgba(255,255,255,0.05);
            border-radius: 0 16px 16px 16px;
            padding: 30px;
            animation: fadeIn 0.3s ease;
        }}
        .tab-content.active {{ display: block; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .card {{
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .card-title {{
            font-size: 1.2em;
            color: #ff6b6b;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{
            background: rgba(233,69,96,0.2);
            color: #ff6b6b;
            font-weight: 600;
        }}
        tr:hover {{ background: rgba(255,255,255,0.05); }}
        
        .score-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .score-high {{ background: #4caf50; color: white; }}
        .score-mid {{ background: #ff9800; color: white; }}
        .score-low {{ background: #f44336; color: white; }}
        
        .stage-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .stage-s2 {{ background: #4caf50; color: white; }}
        .stage-s1 {{ background: #2196f3; color: white; }}
        .stage-s3 {{ background: #ff9800; color: white; }}
        .stage-other {{ background: #9e9e9e; color: white; }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .metric-item {{
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #ff6b6b;
        }}
        .metric-label {{ opacity: 0.7; margin-top: 5px; }}
        
        .progress-bar {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        .progress-green {{ background: linear-gradient(90deg, #4caf50, #8bc34a); }}
        .progress-orange {{ background: linear-gradient(90deg, #ff9800, #ffc107); }}
        .progress-red {{ background: linear-gradient(90deg, #f44336, #ff5722); }}
        
        .stock-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .stock-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .stock-name {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .stock-code {{ color: #ff6b6b; margin-left: 10px; }}
        
        .dimension-scores {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
        }}
        .dim-score {{
            text-align: center;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }}
        .dim-score-value {{ font-size: 1.5em; font-weight: bold; }}
        .dim-score-label {{ font-size: 0.9em; opacity: 0.7; margin-top: 5px; }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            opacity: 0.6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 十倍股策略推荐报告</h1>
            <div class="subtitle">
                分析日期: {meta.get("date", "")} | 
                候选池: {meta.get("universe_count", 0)} | 
                通过筛选: {meta.get("scored_count", 0)} |
                推荐: {len(df)} 只
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('overview')">📊 概览</button>
            <button class="tab-btn" onclick="showTab('fundamental')">📈 基本面</button>
            <button class="tab-btn" onclick="showTab('growth')">🚀 成长性</button>
            <button class="tab-btn" onclick="showTab('valuation')">💰 估值</button>
            <button class="tab-btn" onclick="showTab('technical')">📉 技术面</button>
            <button class="tab-btn" onclick="showTab('individual')">🔍 个股详情</button>
        </div>
        
        <div id="overview" class="tab-content active">
            {overview_html}
        </div>
        <div id="fundamental" class="tab-content">
            {fundamental_html}
        </div>
        <div id="growth" class="tab-content">
            {growth_html}
        </div>
        <div id="valuation" class="tab-content">
            {valuation_html}
        </div>
        <div id="technical" class="tab-content">
            {technical_html}
        </div>
        <div id="individual" class="tab-content">
            {individual_html}
        </div>
        
        <div class="footer">
            <p>⚠️ 本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。</p>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
    
    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''
    
    def _build_overview_tab(self, df: pd.DataFrame, meta: Dict) -> str:
        """概览Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        # 评分方法说明
        weights = meta.get('weights', {})
        
        # 推荐列表
        rows = ''
        for i, row in df.iterrows():
            score_class = 'score-high' if row['total_score'] >= 70 else 'score-mid' if row['total_score'] >= 50 else 'score-low'
            stage_class = 'stage-s2' if 'S2' in row['stage'] else 'stage-s1' if 'S1' in row['stage'] else 'stage-s3' if 'S3' in row['stage'] else 'stage-other'
            
            rows += f'''<tr>
                <td><strong>{row.get("name", "")}</strong><br><small style="color:#888">{row["code"]}</small></td>
                <td>{row.get("industry", "")}</td>
                <td><span class="score-badge {score_class}">{row["total_score"]:.1f}</span></td>
                <td><span class="stage-badge {stage_class}">{row["stage"]}</span></td>
                <td>{row["fund_score"]:.0f}</td>
                <td>{row["growth_score"]:.0f}</td>
                <td>{row["val_score"]:.0f}</td>
                <td>{row["tech_score"]:.0f}</td>
            </tr>'''
        
        return f'''
        <div class="card">
            <div class="card-title">💡 十倍股评分体系</div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-value">{weights.get("fundamental", 0.4)*100:.0f}%</div>
                    <div class="metric-label">基本面权重</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{weights.get("growth", 0.3)*100:.0f}%</div>
                    <div class="metric-label">成长性权重</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{weights.get("valuation", 0.15)*100:.0f}%</div>
                    <div class="metric-label">估值权重</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{weights.get("technical", 0.15)*100:.0f}%</div>
                    <div class="metric-label">技术面权重</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🏆 推荐标的排名</div>
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>行业</th>
                        <th>总分</th>
                        <th>阶段</th>
                        <th>基本面</th>
                        <th>成长性</th>
                        <th>估值</th>
                        <th>技术面</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📌 策略说明</div>
            <p style="line-height: 1.8;">
                本策略基于<strong>彼得·林奇十倍股理论</strong>，通过4个维度评估潜在十倍股：
            </p>
            <ul style="margin: 15px 0; padding-left: 20px; line-height: 2;">
                <li><strong>基本面 (40%)</strong>: ROE、毛利率、净利率、负债率 - 反映公司质地</li>
                <li><strong>成长性 (30%)</strong>: 营收增速、净利润增速 - 反映成长动能</li>
                <li><strong>估值 (15%)</strong>: PEG、PE、市值 - 寻找低估机会</li>
                <li><strong>技术面 (15%)</strong>: 动量、成交量、价格位置 - 把握买入时机</li>
            </ul>
            <p style="line-height: 1.8;">
                <strong>阶段说明</strong>: S2_加速期是最佳介入点，此时业绩爆发但估值尚未完全反映。
            </p>
        </div>
        '''
    
    def _build_fundamental_tab(self, df: pd.DataFrame) -> str:
        """基本面Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        rows = ''
        for _, row in df.iterrows():
            roe_pct = row['roe'] * 100
            gm_pct = row['gross_margin'] * 100
            nm_pct = row['net_margin'] * 100
            debt_pct = row['debt_ratio'] * 100
            
            rows += f'''<tr>
                <td><strong>{row.get("name", "")}</strong><br><small>{row["code"]}</small></td>
                <td>{roe_pct:.1f}%</td>
                <td>{gm_pct:.1f}%</td>
                <td>{nm_pct:.1f}%</td>
                <td>{debt_pct:.1f}%</td>
                <td><span class="score-badge score-mid">{row["fund_score"]:.0f}/100</span></td>
            </tr>'''
        
        return f'''
        <div class="card">
            <div class="card-title">📊 基本面指标详情</div>
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>ROE</th>
                        <th>毛利率</th>
                        <th>净利率</th>
                        <th>负债率</th>
                        <th>基本面得分</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📌 基本面评分规则</div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div style="font-weight: bold; color: #4caf50;">ROE (40分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥30%: 40分<br>≥20%: 30分<br>≥15%: 20分<br>≥10%: 10分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #2196f3;">毛利率 (25分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥50%: 25分<br>≥40%: 20分<br>≥30%: 15分<br>≥20%: 10分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #ff9800;">负债率 (20分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≤30%: 20分<br>≤45%: 15分<br>≤60%: 10分<br>≤70%: 5分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #e91e63;">净利率 (15分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥20%: 15分<br>≥15%: 12分<br>≥10%: 8分<br>≥5%: 4分
                    </div>
                </div>
            </div>
        </div>
        '''
    
    def _build_growth_tab(self, df: pd.DataFrame) -> str:
        """成长性Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        rows = ''
        for _, row in df.iterrows():
            rev_pct = row['revenue_growth'] * 100
            profit_pct = row['profit_growth'] * 100
            
            rows += f'''<tr>
                <td><strong>{row.get("name", "")}</strong><br><small>{row["code"]}</small></td>
                <td style="color: {"#4caf50" if rev_pct > 0 else "#f44336"}">{rev_pct:+.1f}%</td>
                <td style="color: {"#4caf50" if profit_pct > 0 else "#f44336"}">{profit_pct:+.1f}%</td>
                <td><span class="score-badge score-mid">{row["growth_score"]:.0f}/100</span></td>
            </tr>'''
        
        return f'''
        <div class="card">
            <div class="card-title">🚀 成长性指标详情</div>
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>营收增速 (YoY)</th>
                        <th>净利润增速 (YoY)</th>
                        <th>成长性得分</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📌 成长性评分规则</div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div style="font-weight: bold; color: #4caf50;">营收增速 (40分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥50%: 40分<br>≥30%: 30分<br>≥20%: 20分<br>≥10%: 10分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #e94560;">净利润增速 (60分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥100%: 60分<br>≥50%: 50分<br>≥30%: 40分<br>≥20%: 25分
                    </div>
                </div>
            </div>
            <p style="margin-top: 15px; opacity: 0.8;">
                💡 <strong>提示</strong>: 净利润增速是十倍股最重要的指标，权重占成长性维度的60%。
            </p>
        </div>
        '''
    
    def _build_valuation_tab(self, df: pd.DataFrame) -> str:
        """估值Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        rows = ''
        for _, row in df.iterrows():
            peg_color = '#4caf50' if row['peg'] <= 1 else '#ff9800' if row['peg'] <= 2 else '#f44336'
            
            rows += f'''<tr>
                <td><strong>{row.get("name", "")}</strong><br><small>{row["code"]}</small></td>
                <td style="color: {peg_color}">{row["peg"]:.2f}</td>
                <td>{row["pe"]:.1f}</td>
                <td>{row["market_cap"]:.1f} 亿</td>
                <td><span class="score-badge score-mid">{row["val_score"]:.0f}/100</span></td>
            </tr>'''
        
        return f'''
        <div class="card">
            <div class="card-title">💰 估值指标详情</div>
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>PEG</th>
                        <th>PE</th>
                        <th>市值</th>
                        <th>估值得分</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📌 估值评分规则</div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div style="font-weight: bold; color: #4caf50;">PEG (50分) - 核心</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≤0.5: 50分<br>≤0.8: 40分<br>≤1.0: 30分<br>≤1.5: 15分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #2196f3;">PE (25分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        10-25: 25分<br>25-35: 18分<br>35-50: 10分<br>5-10: 15分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #ff9800;">市值 (25分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        30-100亿: 25分<br>100-300亿: 20分<br>300-500亿: 12分
                    </div>
                </div>
            </div>
            <p style="margin-top: 15px; opacity: 0.8;">
                💡 <strong>PEG公式</strong>: PE / 净利润增速(%)。PEG≤1表示被低估，是彼得·林奇最看重的指标。
            </p>
        </div>
        '''
    
    def _build_technical_tab(self, df: pd.DataFrame) -> str:
        """技术面Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        rows = ''
        for _, row in df.iterrows():
            mom_color = '#4caf50' if row['momentum_20d'] > 0 else '#f44336'
            
            rows += f'''<tr>
                <td><strong>{row.get("name", "")}</strong><br><small>{row["code"]}</small></td>
                <td style="color: {mom_color}">{row["momentum_20d"]*100:+.1f}%</td>
                <td>{row["volume_ratio"]:.2f}x</td>
                <td>{row["price_position"]*100:.0f}%</td>
                <td>¥{row["close"]:.2f}</td>
                <td><span class="score-badge score-mid">{row["tech_score"]:.0f}/100</span></td>
            </tr>'''
        
        return f'''
        <div class="card">
            <div class="card-title">📉 技术面指标详情</div>
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>20日动量</th>
                        <th>量比</th>
                        <th>价格位置</th>
                        <th>现价</th>
                        <th>技术面得分</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📌 技术面评分规则</div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div style="font-weight: bold; color: #4caf50;">20日动量 (40分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥15%: 40分<br>≥8%: 30分<br>≥3%: 20分<br>≥0%: 10分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #2196f3;">量比 (30分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        ≥2.0x: 30分<br>≥1.5x: 25分<br>≥1.2x: 20分<br>≥1.0x: 10分
                    </div>
                </div>
                <div class="metric-item">
                    <div style="font-weight: bold; color: #ff9800;">价格位置 (30分)</div>
                    <div style="font-size: 0.9em; margin-top: 8px;">
                        30-60%: 30分 (最佳)<br>20-30%: 25分<br>60-70%: 20分
                    </div>
                </div>
            </div>
            <p style="margin-top: 15px; opacity: 0.8;">
                💡 <strong>价格位置</strong>: 相对52周高低点的位置。30-60%表示离底部有一定距离，但未追高。
            </p>
        </div>
        '''
    
    def _build_individual_tab(self, df: pd.DataFrame) -> str:
        """个股详情Tab"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        cards = ''
        for _, row in df.iterrows():
            score_class = 'score-high' if row['total_score'] >= 70 else 'score-mid'
            stage_class = 'stage-s2' if 'S2' in row['stage'] else 'stage-s1' if 'S1' in row['stage'] else 'stage-s3' if 'S3' in row['stage'] else 'stage-other'
            
            cards += f'''
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <span class="stock-name">{row.get("name", "")}</span>
                        <span class="stock-code">{row["code"]}</span>
                        <span style="margin-left: 10px; opacity: 0.7;">{row.get("industry", "")}</span>
                    </div>
                    <div>
                        <span class="score-badge {score_class}" style="font-size: 1.2em;">
                            总分: {row["total_score"]:.1f}
                        </span>
                        <span class="stage-badge {stage_class}" style="margin-left: 10px;">
                            {row["stage"]}
                        </span>
                    </div>
                </div>
                
                <div class="dimension-scores">
                    <div class="dim-score">
                        <div class="dim-score-value" style="color: #4caf50;">{row["fund_score"]:.0f}</div>
                        <div class="dim-score-label">基本面 (满分100)</div>
                        <div class="progress-bar">
                            <div class="progress-fill progress-green" style="width: {row["fund_score"]}%;"></div>
                        </div>
                    </div>
                    <div class="dim-score">
                        <div class="dim-score-value" style="color: #e94560;">{row["growth_score"]:.0f}</div>
                        <div class="dim-score-label">成长性 (满分100)</div>
                        <div class="progress-bar">
                            <div class="progress-fill progress-orange" style="width: {row["growth_score"]}%;"></div>
                        </div>
                    </div>
                    <div class="dim-score">
                        <div class="dim-score-value" style="color: #2196f3;">{row["val_score"]:.0f}</div>
                        <div class="dim-score-label">估值 (满分100)</div>
                        <div class="progress-bar">
                            <div class="progress-fill progress-green" style="width: {row["val_score"]}%;"></div>
                        </div>
                    </div>
                    <div class="dim-score">
                        <div class="dim-score-value" style="color: #ff9800;">{row["tech_score"]:.0f}</div>
                        <div class="dim-score-label">技术面 (满分100)</div>
                        <div class="progress-bar">
                            <div class="progress-fill progress-orange" style="width: {row["tech_score"]}%;"></div>
                        </div>
                    </div>
                </div>
                
                <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                        <div style="opacity: 0.7; font-size: 0.9em;">ROE</div>
                        <div style="font-size: 1.2em; font-weight: bold;">{row["roe"]*100:.1f}%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                        <div style="opacity: 0.7; font-size: 0.9em;">净利润增速</div>
                        <div style="font-size: 1.2em; font-weight: bold; color: {"#4caf50" if row["profit_growth"] > 0 else "#f44336"};">
                            {row["profit_growth"]*100:+.1f}%
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                        <div style="opacity: 0.7; font-size: 0.9em;">PEG</div>
                        <div style="font-size: 1.2em; font-weight: bold; color: {"#4caf50" if row["peg"] <= 1 else "#ff9800"};">
                            {row["peg"]:.2f}
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                        <div style="opacity: 0.7; font-size: 0.9em;">市值</div>
                        <div style="font-size: 1.2em; font-weight: bold;">{row["market_cap"]:.1f}亿</div>
                    </div>
                </div>
            </div>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">🔍 推荐标的详细分析</div>
        </div>
        {cards}
        '''


# ============== 主入口 ==============

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 十倍股策略验证与推荐报告")
    print("=" * 60)
    
    generator = TenbaggerReportGenerator()
    
    # 执行筛选
    df, meta = generator.run_screening(top_n=5)
    
    if df.empty:
        print("❌ 未找到符合条件的标的")
        return
    
    # 生成报告
    output_path = generator.generate_html(df, meta)
    print(f"\n✅ 报告已生成: {output_path}")
    
    # 打印推荐
    print("\n" + "=" * 60)
    print("🏆 十倍股推荐 TOP 5")
    print("=" * 60)
    for i, row in df.iterrows():
        print(f"\n{row.get('name', '')} ({row['code']})")
        print(f"   总分: {row['total_score']:.1f} | 阶段: {row['stage']}")
        print(f"   基本面: {row['fund_score']:.0f} | 成长性: {row['growth_score']:.0f} | 估值: {row['val_score']:.0f} | 技术: {row['tech_score']:.0f}")
        print(f"   ROE: {row['roe']*100:.1f}% | 净利润增速: {row['profit_growth']*100:+.1f}% | PEG: {row['peg']:.2f}")


if __name__ == "__main__":
    main()
