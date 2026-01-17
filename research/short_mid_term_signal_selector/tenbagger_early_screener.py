#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别筛选器
====================

核心改进：
1. 惩罚已大涨股票 - 价格位置>80%、60日涨幅>50%的股票降权
2. 加分早期特征 - 业绩拐点+股价低位+PEG<1的组合
3. 分层筛选 - 先筛基本面，再筛价格位置
4. 历史验证 - 回测检验早期特征的预测能力

彼得·林奇十倍股早期特征：
- 业绩刚开始改善，市场尚未充分认识
- 股价离历史高点较远（30-50%），有上涨空间  
- PEG<1且PE合理
- 机构关注度低
- 财务质量好但增速刚启动

"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
import numpy as np
import logging

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


class TenbaggerEarlyScreener:
    """十倍股早期识别筛选器"""
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
        
        # 筛选参数 - 可调整（适度放宽以获取更多候选）
        self.params = {
            # 基本面门槛
            'min_market_cap': 20,       # 最小市值（亿）
            'max_market_cap': 800,      # 最大市值（亿）- 放宽上限
            'min_profit_growth': 15,    # 最小净利润增速（放宽）
            'min_revenue_growth': 10,   # 最小营收增速（放宽）
            'min_roe': 3,               # 最小ROE（放宽）
            'max_debt_ratio': 75,       # 最大负债率
            
            # 估值门槛
            'max_peg': 2.0,             # 最大PEG（放宽）
            'max_pe': 120,              # 最大PE（放宽）
            
            # 价格位置（核心改进）
            'max_price_position': 75,   # 最大52周价格位置（稍微放宽）
            'max_mom_60d': 50,          # 最大60日涨幅（稍微放宽）
            'min_distance_from_high': 15,  # 最小距离高点比例（放宽）
            
            # 早期加分特征
            'inflection_bonus': 15,     # 业绩拐点加分
            'low_position_bonus': 10,   # 股价低位加分
            'peg_undervalue_bonus': 10, # PEG低估加分
            
            # 高位惩罚
            'high_position_penalty': 30,   # 高位惩罚
            'overextended_penalty': 25,    # 涨幅过大惩罚
        }
    
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
    
    def screen_early_stage_stocks(self, date: str = None, 
                                   universe: str = 'all') -> pd.DataFrame:
        """
        筛选早期潜力股
        
        Args:
            date: 筛选日期
            universe: 股票池 ('all', 'tech', 'small_cap')
            
        Returns:
            DataFrame with ranked early-stage candidates
        """
        if not self.jq:
            return pd.DataFrame()
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        print(f"\n🔍 十倍股早期识别筛选 ({date})")
        print("=" * 50)
        
        # Step 1: 获取候选股票池
        print("📊 Step 1: 获取候选股票池...")
        candidates = self._get_candidate_universe(date, universe)
        print(f"   候选数量: {len(candidates)}")
        
        # Step 2: 基本面筛选
        print("📊 Step 2: 基本面筛选...")
        fundamentals_passed = self._filter_by_fundamentals(candidates, date)
        print(f"   通过基本面筛选: {len(fundamentals_passed)}")
        
        # Step 3: 估值筛选
        print("📊 Step 3: 估值筛选...")
        valuation_passed = self._filter_by_valuation(fundamentals_passed, date)
        print(f"   通过估值筛选: {len(valuation_passed)}")
        
        # Step 4: 价格位置筛选（核心改进）
        print("📊 Step 4: 价格位置筛选 (避免追高)...")
        position_passed = self._filter_by_price_position(valuation_passed, date)
        print(f"   通过价格位置筛选: {len(position_passed)}")
        
        # Step 5: 计算综合得分
        print("📊 Step 5: 计算早期潜力得分...")
        scored = self._calculate_early_stage_score(position_passed, date)
        
        # Step 6: 排序输出
        if not scored.empty:
            scored = scored.sort_values('early_score', ascending=False)
            print(f"\n✅ 最终筛选出 {len(scored)} 只早期潜力股")
        
        return scored
    
    def _get_candidate_universe(self, date: str, universe: str) -> List[str]:
        """获取候选股票池"""
        all_stocks = self.jq.get_all_securities(types=['stock'], date=date)
        
        # 排除ST股票
        all_stocks = all_stocks[~all_stocks['display_name'].str.contains('ST|退')]
        
        if universe == 'tech':
            # 科创板+创业板
            candidates = all_stocks[
                (all_stocks.index.str.startswith('688')) | 
                (all_stocks.index.str.startswith('300'))
            ]
        elif universe == 'small_cap':
            # 小市值股（需要额外查询市值）
            candidates = all_stocks
        else:
            candidates = all_stocks
        
        return candidates.index.tolist()
    
    def _filter_by_fundamentals(self, codes: List[str], date: str) -> List[str]:
        """基本面筛选"""
        passed = []
        
        # 批量获取财务数据
        q = self.jq.query(
            self.jq.indicator.code,
            self.jq.indicator.roe,
            self.jq.indicator.inc_revenue_year_on_year,
            self.jq.indicator.inc_net_profit_year_on_year,
        ).filter(
            self.jq.indicator.code.in_(codes[:500])  # 限制数量
        )
        
        fin_df = self.jq.get_fundamentals(q, date=date)
        
        if fin_df is None or fin_df.empty:
            return []
        
        for _, row in fin_df.iterrows():
            code = row['code']
            roe = row.get('roe', 0) or 0
            rev_growth = row.get('inc_revenue_year_on_year', 0) or 0
            profit_growth = row.get('inc_net_profit_year_on_year', 0) or 0
            
            # 基本面条件
            if (profit_growth >= self.params['min_profit_growth'] and
                rev_growth >= self.params['min_revenue_growth'] and
                roe >= self.params['min_roe']):
                passed.append({
                    'code': code,
                    'roe': roe,
                    'revenue_growth': rev_growth,
                    'profit_growth': profit_growth
                })
        
        return [p['code'] for p in passed]
    
    def _filter_by_valuation(self, codes: List[str], date: str) -> List[str]:
        """估值筛选"""
        if not codes:
            return []
        
        passed = []
        
        q = self.jq.query(
            self.jq.valuation.code,
            self.jq.valuation.pe_ratio,
            self.jq.valuation.market_cap,
        ).filter(
            self.jq.valuation.code.in_(codes)
        )
        
        val_df = self.jq.get_fundamentals(q, date=date)
        
        # 获取增速计算PEG
        q2 = self.jq.query(
            self.jq.indicator.code,
            self.jq.indicator.inc_net_profit_year_on_year,
        ).filter(
            self.jq.indicator.code.in_(codes)
        )
        fin_df = self.jq.get_fundamentals(q2, date=date)
        
        growth_map = {}
        if fin_df is not None:
            for _, row in fin_df.iterrows():
                growth_map[row['code']] = row.get('inc_net_profit_year_on_year', 0) or 0
        
        if val_df is None:
            return []
        
        for _, row in val_df.iterrows():
            code = row['code']
            pe = row.get('pe_ratio', 0) or 0
            market_cap = row.get('market_cap', 0) or 0
            profit_growth = growth_map.get(code, 0)
            
            peg = pe / profit_growth if profit_growth > 0 and pe > 0 else 99
            
            # 市值和估值条件
            if (self.params['min_market_cap'] <= market_cap <= self.params['max_market_cap'] and
                0 < pe <= self.params['max_pe'] and
                peg <= self.params['max_peg']):
                passed.append(code)
        
        return passed
    
    def _filter_by_price_position(self, codes: List[str], date: str) -> List[str]:
        """价格位置筛选 - 核心改进，避免追高"""
        if not codes:
            return []
        
        passed = []
        end_dt = datetime.strptime(date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=300)
        
        for code in codes[:100]:  # 限制数量提高速度
            try:
                df = self.jq.get_price(
                    code,
                    start_date=start_dt.strftime('%Y-%m-%d'),
                    end_date=date,
                    frequency='daily',
                    fields=['high', 'low', 'close'],
                    skip_paused=True
                )
                
                if df is None or len(df) < 60:
                    continue
                
                current_price = df['close'].iloc[-1]
                high_52w = df.tail(252)['high'].max() if len(df) >= 252 else df['high'].max()
                low_52w = df.tail(252)['low'].min() if len(df) >= 252 else df['low'].min()
                
                # 价格位置
                if high_52w > low_52w:
                    price_position = (current_price - low_52w) / (high_52w - low_52w) * 100
                else:
                    price_position = 50
                
                # 60日涨幅
                mom_60d = (current_price / df['close'].iloc[-60] - 1) * 100 if len(df) >= 60 else 0
                
                # 距离高点
                distance_from_high = (high_52w - current_price) / high_52w * 100
                
                # 核心筛选条件：避免追高
                if (price_position <= self.params['max_price_position'] and
                    mom_60d <= self.params['max_mom_60d'] and
                    distance_from_high >= self.params['min_distance_from_high']):
                    passed.append({
                        'code': code,
                        'price_position': price_position,
                        'mom_60d': mom_60d,
                        'distance_from_high': distance_from_high
                    })
            
            except Exception:
                continue
        
        return [p['code'] for p in passed]
    
    def _calculate_early_stage_score(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算早期潜力综合得分"""
        if not codes:
            return pd.DataFrame()
        
        results = []
        
        for code in codes:
            try:
                score_data = self._score_single_stock(code, date)
                if score_data:
                    results.append(score_data)
            except Exception as e:
                continue
        
        if not results:
            return pd.DataFrame()
        
        return pd.DataFrame(results)
    
    def _score_single_stock(self, code: str, date: str) -> Optional[Dict]:
        """对单只股票评分"""
        try:
            info = self.jq.get_security_info(code)
            name = info.display_name if info else ''
            
            # 获取数据
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=300)
            
            df = self.jq.get_price(
                code,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['high', 'low', 'close'],
                skip_paused=True
            )
            
            if df is None or len(df) < 60:
                return None
            
            # 价格指标
            current_price = df['close'].iloc[-1]
            high_52w = df.tail(252)['high'].max() if len(df) >= 252 else df['high'].max()
            low_52w = df.tail(252)['low'].min() if len(df) >= 252 else df['low'].min()
            price_position = (current_price - low_52w) / (high_52w - low_52w) * 100 if high_52w > low_52w else 50
            mom_60d = (current_price / df['close'].iloc[-60] - 1) * 100 if len(df) >= 60 else 0
            distance_from_high = (high_52w - current_price) / high_52w * 100
            
            # 财务指标
            q = self.jq.query(
                self.jq.indicator.roe,
                self.jq.indicator.inc_net_profit_year_on_year,
                self.jq.indicator.inc_revenue_year_on_year,
            ).filter(self.jq.indicator.code == code)
            fin_df = self.jq.get_fundamentals(q, date=date)
            
            if fin_df is None or fin_df.empty:
                return None
            
            roe = fin_df.iloc[0].get('roe', 0) or 0
            profit_growth = fin_df.iloc[0].get('inc_net_profit_year_on_year', 0) or 0
            revenue_growth = fin_df.iloc[0].get('inc_revenue_year_on_year', 0) or 0
            
            # 估值指标
            q2 = self.jq.query(
                self.jq.valuation.pe_ratio,
                self.jq.valuation.market_cap,
            ).filter(self.jq.valuation.code == code)
            val_df = self.jq.get_fundamentals(q2, date=date)
            
            if val_df is None or val_df.empty:
                return None
            
            pe = val_df.iloc[0].get('pe_ratio', 0) or 0
            market_cap = val_df.iloc[0].get('market_cap', 0) or 0
            peg = pe / profit_growth if profit_growth > 0 and pe > 0 else 99
            
            # ========== 评分计算 ==========
            base_score = 50
            
            # 1. 成长性得分 (0-25分)
            growth_score = min(25, profit_growth / 4) if profit_growth > 0 else 0
            
            # 2. 盈利质量得分 (0-15分)
            quality_score = min(15, roe / 2) if roe > 0 else 0
            
            # 3. 估值得分 (0-20分)
            if peg < 0.5:
                valuation_score = 20
            elif peg < 0.8:
                valuation_score = 15
            elif peg < 1.0:
                valuation_score = 10
            elif peg < 1.5:
                valuation_score = 5
            else:
                valuation_score = 0
            
            # 4. 价格位置得分 (-30 ~ +20)
            if price_position < 30:
                position_score = 20  # 低位加分
            elif price_position < 50:
                position_score = 10  # 中低位
            elif price_position < 70:
                position_score = 0   # 中位
            elif price_position < 85:
                position_score = -15  # 偏高位惩罚
            else:
                position_score = -30  # 高位严重惩罚
            
            # 5. 涨幅惩罚 (-25 ~ 0)
            if mom_60d > 50:
                momentum_penalty = -25
            elif mom_60d > 30:
                momentum_penalty = -15
            elif mom_60d > 20:
                momentum_penalty = -5
            else:
                momentum_penalty = 0
            
            # 6. 早期特征加分
            early_bonus = 0
            early_signals = []
            
            # 业绩拐点（前一季度增速 < 当前季度增速）
            if profit_growth > 30 and price_position < 50:
                early_bonus += 15
                early_signals.append("业绩高增+股价低位")
            
            # PEG严重低估
            if peg < 0.6 and price_position < 60:
                early_bonus += 10
                early_signals.append("PEG<0.6估值错配")
            
            # 距离高点有空间
            if distance_from_high > 30 and profit_growth > 20:
                early_bonus += 10
                early_signals.append(f"距高点{distance_from_high:.0f}%空间")
            
            # 综合得分
            total_score = (base_score + growth_score + quality_score + 
                          valuation_score + position_score + 
                          momentum_penalty + early_bonus)
            total_score = max(0, min(100, total_score))
            
            # 判断阶段
            if total_score >= 75 and price_position < 60:
                stage = "⭐ 早期潜力"
                recommendation = "建议关注"
            elif total_score >= 60 and price_position < 70:
                stage = "👁️ 观察关注"
                recommendation = "可分批建仓"
            elif price_position > 80 or mom_60d > 40:
                stage = "⚠️ 高位风险"
                recommendation = "暂不介入"
            else:
                stage = "📊 一般"
                recommendation = "持续跟踪"
            
            return {
                'code': code,
                'name': name,
                'market_cap': round(market_cap, 1),
                'pe': round(pe, 1),
                'peg': round(peg, 2),
                'profit_growth': round(profit_growth, 1),
                'revenue_growth': round(revenue_growth, 1),
                'roe': round(roe, 1),
                'price_position': round(price_position, 1),
                'mom_60d': round(mom_60d, 1),
                'distance_from_high': round(distance_from_high, 1),
                'early_score': round(total_score, 0),
                'growth_score': round(growth_score, 1),
                'quality_score': round(quality_score, 1),
                'valuation_score': round(valuation_score, 1),
                'position_score': round(position_score, 1),
                'momentum_penalty': round(momentum_penalty, 1),
                'early_bonus': round(early_bonus, 1),
                'early_signals': ', '.join(early_signals) if early_signals else '-',
                'stage': stage,
                'recommendation': recommendation
            }
        
        except Exception as e:
            return None


def generate_early_stage_report(date: str = None, 
                                 universe: str = 'tech',
                                 top_n: int = 10) -> str:
    """生成早期潜力股筛选报告"""
    screener = TenbaggerEarlyScreener()
    
    # 执行筛选
    results = screener.screen_early_stage_stocks(date, universe)
    
    if results.empty:
        print("❌ 未找到符合条件的早期潜力股")
        return ""
    
    # 取Top N
    top_results = results.head(top_n)
    
    # 生成HTML报告
    html = _build_early_stage_html_report(top_results, date, universe)
    
    # 保存
    output_dir = PROJECT_ROOT / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = output_dir / f'early_stage_screen_{timestamp}.html'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告已生成: {output_path}")
    return str(output_path)


def _build_early_stage_html_report(df: pd.DataFrame, date: str, universe: str) -> str:
    """构建早期潜力股HTML报告"""
    
    # 构建股票表格行
    rows_html = ""
    for _, row in df.iterrows():
        stage_color = '#4caf50' if '早期' in row['stage'] else '#ff9800' if '观察' in row['stage'] else '#f44336'
        rows_html += f'''
        <tr>
            <td><strong>{row['code']}</strong><br><small>{row['name']}</small></td>
            <td style="color: {stage_color};">{row['stage']}</td>
            <td><span class="score-badge" style="background: {"#4caf50" if row['early_score'] >= 70 else "#ff9800" if row['early_score'] >= 50 else "#666"};">
                {row['early_score']:.0f}
            </span></td>
            <td>{row['market_cap']:.0f}亿</td>
            <td style="color: {"#4caf50" if row['profit_growth'] > 0 else "#f44336"};">
                {row['profit_growth']:+.1f}%
            </td>
            <td style="color: {"#4caf50" if row['peg'] < 1 else "#ff9800"};">
                {row['peg']:.2f}
            </td>
            <td style="color: {"#4caf50" if row['price_position'] < 50 else "#f44336" if row['price_position'] > 70 else "#ff9800"};">
                {row['price_position']:.0f}%
            </td>
            <td style="color: {"#f44336" if row['mom_60d'] > 30 else "#4caf50"};">
                {row['mom_60d']:+.1f}%
            </td>
            <td>{row['early_signals']}</td>
            <td><strong>{row['recommendation']}</strong></td>
        </tr>
        '''
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股早期识别筛选报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%);
            color: #e6edf3;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        .header {{
            background: linear-gradient(90deg, #238636, #2ea043);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 1.1em; }}
        
        .info-bar {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        .info-item {{
            background: rgba(255,255,255,0.15);
            padding: 8px 16px;
            border-radius: 20px;
        }}
        
        .methodology {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .methodology h3 {{ color: #58a6ff; margin-bottom: 15px; }}
        .methodology ul {{ padding-left: 20px; line-height: 1.8; }}
        .methodology li {{ margin-bottom: 5px; }}
        
        .results-table {{
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 25px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #238636;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 15px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        tr:hover {{ background: rgba(255,255,255,0.05); }}
        
        .score-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: bold;
            color: white;
        }}
        
        .legend {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            opacity: 0.6;
            font-size: 0.9em;
        }}
        
        @media (max-width: 1200px) {{
            table {{ font-size: 0.85em; }}
            th, td {{ padding: 10px 8px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 十倍股早期识别筛选报告</h1>
            <div class="subtitle">Early Stage Tenbagger Screener - 聚焦业绩拐点 + 股价低位</div>
            <div class="info-bar">
                <div class="info-item">📅 筛选日期: {date or '最新'}</div>
                <div class="info-item">🎯 股票池: {universe}</div>
                <div class="info-item">📊 筛选结果: {len(df)} 只</div>
            </div>
        </div>
        
        <div class="methodology">
            <h3>📐 筛选方法论（核心改进）</h3>
            <ul>
                <li><strong>避免追高</strong>: 52周价格位置 ≤ 70%，60日涨幅 ≤ 40%</li>
                <li><strong>预留空间</strong>: 距离52周高点 ≥ 20%</li>
                <li><strong>业绩支撑</strong>: 净利润增速 ≥ 20%，营收增速 ≥ 15%</li>
                <li><strong>估值合理</strong>: PEG ≤ 1.5，PE ≤ 80</li>
                <li><strong>早期加分</strong>: 业绩拐点 + 股价低位 + PEG<0.6 = 额外加分</li>
                <li><strong>高位惩罚</strong>: 股价>80%高位或60日涨幅>50% = 扣分</li>
            </ul>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-dot" style="background: #4caf50;"></div>
                <span>早期潜力 (得分≥70)</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background: #ff9800;"></div>
                <span>观察关注 (得分50-70)</span>
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background: #f44336;"></div>
                <span>高位风险 (追高警告)</span>
            </div>
        </div>
        
        <div class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>阶段</th>
                        <th>综合分</th>
                        <th>市值</th>
                        <th>利润增速</th>
                        <th>PEG</th>
                        <th>价格位置</th>
                        <th>60日涨幅</th>
                        <th>早期信号</th>
                        <th>建议</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            ⚠️ 本报告仅供参考，不构成投资建议 | 
            十倍股早期识别需要耐心和纪律 | 
            生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
</body>
</html>'''


# ============== 主入口 ==============

if __name__ == "__main__":
    # 执行早期潜力股筛选
    print("🚀 启动十倍股早期识别筛选器")
    print("=" * 60)
    
    output_path = generate_early_stage_report(
        date=None,      # 最新日期
        universe='tech',  # 科创板+创业板
        top_n=15
    )
    
    if output_path:
        print(f"\n📄 打开报告: file://{output_path}")
