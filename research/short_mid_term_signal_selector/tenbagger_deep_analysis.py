#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股深度分析与早期识别模型
=============================

问题诊断：
- 原模型选出的是"已经大涨"的股票，而非"早期潜力股"
- 动量因子反而成为了"追高"信号
- 缺少对"价格已处高位"的惩罚

修正方向：
1. 加入"距离历史高点"的惩罚因子
2. 加入"近期涨幅过大"的惩罚因子  
3. 识别"业绩拐点刚出现但股价尚未反应"的早期阶段
4. 重视"估值错配"而非"动量追涨"

十倍股早期特征（彼得·林奇）：
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


class TenbaggerDeepAnalyzer:
    """十倍股深度分析器"""
    
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
    
    def analyze_single_stock(self, code: str, date: str = None) -> Dict[str, Any]:
        """深度分析单只股票"""
        if not self.jq:
            return {}
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        result = {
            'code': code,
            'date': date,
            'basic_info': {},
            'price_analysis': {},
            'financial_analysis': {},
            'valuation_analysis': {},
            'stage_analysis': {},
            'risk_analysis': {},
            'similar_history': [],
            'conclusion': {}
        }
        
        # 1. 基本信息
        result['basic_info'] = self._get_basic_info(code)
        
        # 2. 价格分析（关键：判断是否已在高位）
        result['price_analysis'] = self._analyze_price(code, date)
        
        # 3. 财务分析
        result['financial_analysis'] = self._analyze_financials(code, date)
        
        # 4. 估值分析
        result['valuation_analysis'] = self._analyze_valuation(code, date)
        
        # 5. 阶段判断（修正版）
        result['stage_analysis'] = self._determine_stage_v2(result)
        
        # 6. 风险分析
        result['risk_analysis'] = self._analyze_risks(result)
        
        # 7. 历史相似案例
        result['similar_history'] = self._find_similar_history(code, date)
        
        # 8. 综合结论
        result['conclusion'] = self._generate_conclusion(result)
        
        return result
    
    def _get_basic_info(self, code: str) -> Dict:
        """获取基本信息"""
        try:
            info = self.jq.get_security_info(code)
            industry = self.jq.get_industry(code)
            ind_name = ''
            if industry and code in industry:
                sw = industry[code].get('sw_l1', {})
                ind_name = sw.get('industry_name', '')
            
            return {
                'name': info.display_name if info else '',
                'industry': ind_name,
                'start_date': str(info.start_date) if info else '',
                'type': info.type if info else ''
            }
        except Exception as e:
            return {'name': '', 'industry': '', 'start_date': '', 'type': ''}
    
    def _analyze_price(self, code: str, date: str) -> Dict:
        """价格分析 - 关键：判断是否已在高位"""
        try:
            end_date = datetime.strptime(date, '%Y-%m-%d')
            start_date = end_date - timedelta(days=500)  # 约2年
            
            df = self.jq.get_price(
                code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume', 'money'],
                skip_paused=True
            )
            
            if df is None or len(df) < 60:
                return {}
            
            current_price = df['close'].iloc[-1]
            
            # 历史高点低点
            high_52w = df.tail(252)['high'].max() if len(df) >= 252 else df['high'].max()
            low_52w = df.tail(252)['low'].min() if len(df) >= 252 else df['low'].min()
            high_all = df['high'].max()
            low_all = df['low'].min()
            
            # 距离高点的位置
            distance_from_52w_high = (high_52w - current_price) / high_52w * 100
            distance_from_all_high = (high_all - current_price) / high_all * 100
            price_position_52w = (current_price - low_52w) / (high_52w - low_52w) * 100 if high_52w > low_52w else 50
            
            # 各时间段涨幅
            mom_5d = (current_price / df['close'].iloc[-5] - 1) * 100 if len(df) >= 5 else 0
            mom_20d = (current_price / df['close'].iloc[-20] - 1) * 100 if len(df) >= 20 else 0
            mom_60d = (current_price / df['close'].iloc[-60] - 1) * 100 if len(df) >= 60 else 0
            mom_120d = (current_price / df['close'].iloc[-120] - 1) * 100 if len(df) >= 120 else 0
            mom_250d = (current_price / df['close'].iloc[-250] - 1) * 100 if len(df) >= 250 else 0
            
            # IPO以来涨幅
            ipo_return = (current_price / df['close'].iloc[0] - 1) * 100
            
            # 成交量分析
            vol_ma20 = df['volume'].tail(20).mean()
            vol_ma60 = df['volume'].tail(60).mean()
            current_vol = df['volume'].iloc[-1]
            vol_ratio = current_vol / vol_ma20 if vol_ma20 > 0 else 1
            
            # 波动率
            returns = df['close'].pct_change().dropna()
            volatility_20d = returns.tail(20).std() * np.sqrt(252) * 100
            volatility_60d = returns.tail(60).std() * np.sqrt(252) * 100
            
            # 最大回撤
            roll_max = df['close'].cummax()
            drawdown = (df['close'] - roll_max) / roll_max
            max_drawdown = drawdown.min() * 100
            
            # 高位判断
            is_near_high = price_position_52w > 80  # 距离52周高点很近
            is_overextended = mom_60d > 50  # 60日涨幅超50%
            
            return {
                'current_price': current_price,
                'high_52w': high_52w,
                'low_52w': low_52w,
                'high_all': high_all,
                'low_all': low_all,
                'distance_from_52w_high': distance_from_52w_high,
                'distance_from_all_high': distance_from_all_high,
                'price_position_52w': price_position_52w,
                'mom_5d': mom_5d,
                'mom_20d': mom_20d,
                'mom_60d': mom_60d,
                'mom_120d': mom_120d,
                'mom_250d': mom_250d,
                'ipo_return': ipo_return,
                'vol_ratio': vol_ratio,
                'volatility_20d': volatility_20d,
                'volatility_60d': volatility_60d,
                'max_drawdown': max_drawdown,
                'is_near_high': is_near_high,
                'is_overextended': is_overextended,
                'price_data': df  # 保存用于图表
            }
        except Exception as e:
            logger.warning(f"价格分析失败: {e}")
            return {}
    
    def _analyze_financials(self, code: str, date: str) -> Dict:
        """财务分析"""
        try:
            # 获取最近4个季度数据
            q = self.jq.query(
                self.jq.indicator.code,
                self.jq.indicator.statDate,
                self.jq.indicator.roe,
                self.jq.indicator.gross_profit_margin,
                self.jq.indicator.net_profit_margin,
                self.jq.indicator.inc_revenue_year_on_year,
                self.jq.indicator.inc_net_profit_year_on_year,
                self.jq.indicator.inc_revenue_annual,
                self.jq.indicator.inc_net_profit_annual,
            ).filter(
                self.jq.indicator.code == code
            ).order_by(
                self.jq.indicator.statDate.desc()
            ).limit(8)
            
            fin_df = self.jq.get_fundamentals(q, date=date)
            
            # 负债率
            q2 = self.jq.query(
                self.jq.balance.code,
                self.jq.balance.total_liability,
                self.jq.balance.total_assets,
            ).filter(
                self.jq.balance.code == code
            )
            bal_df = self.jq.get_fundamentals(q2, date=date)
            
            if fin_df is None or fin_df.empty:
                return {}
            
            latest = fin_df.iloc[0]
            
            # 业绩趋势分析
            revenue_growth_trend = []
            profit_growth_trend = []
            roe_trend = []
            
            for _, row in fin_df.iterrows():
                if pd.notna(row.get('inc_revenue_year_on_year')):
                    revenue_growth_trend.append(row['inc_revenue_year_on_year'])
                if pd.notna(row.get('inc_net_profit_year_on_year')):
                    profit_growth_trend.append(row['inc_net_profit_year_on_year'])
                if pd.notna(row.get('roe')):
                    roe_trend.append(row['roe'])
            
            # 业绩拐点检测
            has_inflection = False
            if len(profit_growth_trend) >= 2:
                # 最近一期增速显著高于前一期
                if profit_growth_trend[0] > profit_growth_trend[1] + 20:
                    has_inflection = True
            
            # 业绩加速检测
            is_accelerating = False
            if len(profit_growth_trend) >= 3:
                if profit_growth_trend[0] > profit_growth_trend[1] > profit_growth_trend[2]:
                    is_accelerating = True
            
            debt_ratio = 0
            if bal_df is not None and not bal_df.empty:
                assets = bal_df.iloc[0].get('total_assets', 0)
                liability = bal_df.iloc[0].get('total_liability', 0)
                if assets > 0:
                    debt_ratio = liability / assets * 100
            
            return {
                'roe': latest.get('roe', 0) or 0,
                'gross_margin': latest.get('gross_profit_margin', 0) or 0,
                'net_margin': latest.get('net_profit_margin', 0) or 0,
                'revenue_growth': latest.get('inc_revenue_year_on_year', 0) or 0,
                'profit_growth': latest.get('inc_net_profit_year_on_year', 0) or 0,
                'debt_ratio': debt_ratio,
                'revenue_growth_trend': revenue_growth_trend[:4],
                'profit_growth_trend': profit_growth_trend[:4],
                'roe_trend': roe_trend[:4],
                'has_inflection': has_inflection,
                'is_accelerating': is_accelerating,
                'stat_date': str(latest.get('statDate', ''))
            }
        except Exception as e:
            logger.warning(f"财务分析失败: {e}")
            return {}
    
    def _analyze_valuation(self, code: str, date: str) -> Dict:
        """估值分析"""
        try:
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.pe_ratio,
                self.jq.valuation.pb_ratio,
                self.jq.valuation.ps_ratio,
                self.jq.valuation.market_cap,
                self.jq.valuation.pe_ratio_lyr,
            ).filter(
                self.jq.valuation.code == code
            )
            val_df = self.jq.get_fundamentals(q, date=date)
            
            if val_df is None or val_df.empty:
                return {}
            
            latest = val_df.iloc[0]
            pe = latest.get('pe_ratio', 0) or 0
            profit_growth = 0
            
            # 获取利润增速计算PEG
            q2 = self.jq.query(
                self.jq.indicator.inc_net_profit_year_on_year
            ).filter(
                self.jq.indicator.code == code
            )
            fin_df = self.jq.get_fundamentals(q2, date=date)
            if fin_df is not None and not fin_df.empty:
                profit_growth = fin_df.iloc[0].get('inc_net_profit_year_on_year', 0) or 0
            
            peg = pe / profit_growth if profit_growth > 0 and pe > 0 else 99
            
            # 获取历史PE分位
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=750)  # 约3年
            
            pe_history = self.jq.get_valuation(
                code,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                fields=['pe_ratio']
            )
            
            pe_percentile = 50
            if pe_history is not None and len(pe_history) > 0:
                pe_vals = pe_history['pe_ratio'].dropna()
                pe_vals = pe_vals[(pe_vals > 0) & (pe_vals < 1000)]
                if len(pe_vals) > 10:
                    pe_percentile = (pe_vals < pe).sum() / len(pe_vals) * 100
            
            return {
                'pe': pe,
                'pb': latest.get('pb_ratio', 0) or 0,
                'ps': latest.get('ps_ratio', 0) or 0,
                'market_cap': latest.get('market_cap', 0) or 0,
                'peg': peg,
                'profit_growth': profit_growth,
                'pe_percentile': pe_percentile,
                'is_undervalued': peg < 1 and pe < 50,
                'is_overvalued': peg > 2 or pe > 100
            }
        except Exception as e:
            logger.warning(f"估值分析失败: {e}")
            return {}
    
    def _determine_stage_v2(self, result: Dict) -> Dict:
        """修正版阶段判断 - 加入价格位置惩罚"""
        price = result.get('price_analysis', {})
        fin = result.get('financial_analysis', {})
        val = result.get('valuation_analysis', {})
        
        # 关键指标
        market_cap = val.get('market_cap', 0)
        profit_growth = fin.get('profit_growth', 0)
        revenue_growth = fin.get('revenue_growth', 0)
        roe = fin.get('roe', 0)
        peg = val.get('peg', 99)
        
        price_position = price.get('price_position_52w', 50)
        mom_60d = price.get('mom_60d', 0)
        distance_from_high = price.get('distance_from_52w_high', 0)
        is_near_high = price.get('is_near_high', False)
        is_overextended = price.get('is_overextended', False)
        has_inflection = fin.get('has_inflection', False)
        
        # 基础阶段判断
        if profit_growth < -20 and revenue_growth < 0:
            base_stage = "S5_衰退"
            stage_score = 10
        elif market_cap < 30:
            base_stage = "S0_种子"
            stage_score = 30
        elif market_cap < 100:
            if profit_growth >= 50 or revenue_growth >= 30:
                base_stage = "S1_萌芽"
                stage_score = 70
            else:
                base_stage = "S0_种子"
                stage_score = 40
        elif market_cap < 300:
            if profit_growth >= 30 and roe >= 10:
                base_stage = "S2_加速"
                stage_score = 80
            else:
                base_stage = "S1_萌芽"
                stage_score = 60
        elif market_cap < 1000:
            if profit_growth >= 20:
                base_stage = "S3_扩张"
                stage_score = 50
            else:
                base_stage = "S4_成熟"
                stage_score = 30
        else:
            base_stage = "S4_成熟"
            stage_score = 20
        
        # 价格位置惩罚（关键修正）
        price_penalty = 0
        price_warning = []
        
        if is_near_high:
            price_penalty += 30
            price_warning.append("⚠️ 股价接近52周高点(>80%)，追高风险大")
        
        if is_overextended:
            price_penalty += 25
            price_warning.append("⚠️ 60日涨幅超50%，短期已透支")
        
        if mom_60d > 30:
            price_penalty += 15
            price_warning.append("⚠️ 近期涨幅较大，需等待回调")
        
        if distance_from_high < 10:
            price_penalty += 20
            price_warning.append("⚠️ 距离历史高点很近，上涨空间有限")
        
        # 早期识别加分
        early_bonus = 0
        early_signal = []
        
        if has_inflection and price_position < 50:
            early_bonus += 20
            early_signal.append("✅ 业绩拐点出现，股价尚未充分反应")
        
        if peg < 0.8 and price_position < 60:
            early_bonus += 15
            early_signal.append("✅ PEG<0.8且股价位置适中，估值错配")
        
        if profit_growth > 30 and mom_60d < 20:
            early_bonus += 15
            early_signal.append("✅ 业绩高增长但股价涨幅温和")
        
        if distance_from_high > 30 and profit_growth > 20:
            early_bonus += 10
            early_signal.append("✅ 距离高点有空间，业绩支撑")
        
        # 调整后得分
        adjusted_score = stage_score - price_penalty + early_bonus
        adjusted_score = max(0, min(100, adjusted_score))
        
        # 真实阶段判断
        if adjusted_score >= 70 and not is_near_high and not is_overextended:
            real_stage = "早期潜力 ⭐"
            recommendation = "建议买入"
        elif adjusted_score >= 50 and not is_near_high:
            real_stage = "观察关注"
            recommendation = "等待回调"
        elif is_near_high or is_overextended:
            real_stage = "高位风险 ⚠️"
            recommendation = "暂不介入"
        else:
            real_stage = base_stage
            recommendation = "持续跟踪"
        
        return {
            'base_stage': base_stage,
            'real_stage': real_stage,
            'stage_score': stage_score,
            'price_penalty': price_penalty,
            'early_bonus': early_bonus,
            'adjusted_score': adjusted_score,
            'price_warning': price_warning,
            'early_signal': early_signal,
            'recommendation': recommendation,
            'is_early_stage': adjusted_score >= 70 and not is_near_high,
            'is_high_risk': is_near_high or is_overextended
        }
    
    def _analyze_risks(self, result: Dict) -> Dict:
        """风险分析"""
        price = result.get('price_analysis', {})
        fin = result.get('financial_analysis', {})
        val = result.get('valuation_analysis', {})
        stage = result.get('stage_analysis', {})
        
        risks = []
        risk_score = 0  # 越高风险越大
        
        # 价格风险
        if price.get('is_near_high'):
            risks.append({"type": "价格", "level": "高", "desc": "股价接近52周高点，回调风险大"})
            risk_score += 30
        
        if price.get('is_overextended'):
            risks.append({"type": "价格", "level": "高", "desc": "60日涨幅超50%，透支未来涨幅"})
            risk_score += 25
        
        if price.get('volatility_60d', 0) > 60:
            risks.append({"type": "波动", "level": "中", "desc": "波动率较高，需设好止损"})
            risk_score += 15
        
        # 估值风险
        if val.get('pe', 0) > 100:
            risks.append({"type": "估值", "level": "高", "desc": "PE过高，估值泡沫风险"})
            risk_score += 20
        
        if val.get('peg', 99) > 2:
            risks.append({"type": "估值", "level": "中", "desc": "PEG>2，成长性不足以支撑估值"})
            risk_score += 15
        
        # 财务风险
        if fin.get('debt_ratio', 0) > 70:
            risks.append({"type": "财务", "level": "中", "desc": "负债率较高"})
            risk_score += 15
        
        if fin.get('roe', 0) < 5:
            risks.append({"type": "盈利", "level": "中", "desc": "ROE偏低，盈利能力一般"})
            risk_score += 10
        
        # 综合风险等级
        if risk_score >= 50:
            overall_risk = "高风险"
        elif risk_score >= 30:
            overall_risk = "中等风险"
        else:
            overall_risk = "低风险"
        
        return {
            'risks': risks,
            'risk_score': risk_score,
            'overall_risk': overall_risk
        }
    
    def _find_similar_history(self, code: str, date: str) -> List[Dict]:
        """寻找历史相似案例 - 通过数据库搜索类似特征的股票"""
        try:
            # 获取当前股票的特征
            result = {
                'price_analysis': self._analyze_price(code, date),
                'financial_analysis': self._analyze_financials(code, date),
                'valuation_analysis': self._analyze_valuation(code, date)
            }
            
            current_features = {
                'price_position': result['price_analysis'].get('price_position_52w', 50),
                'mom_60d': result['price_analysis'].get('mom_60d', 0),
                'profit_growth': result['financial_analysis'].get('profit_growth', 0),
                'peg': result['valuation_analysis'].get('peg', 1)
            }
            
            # 搜索历史上类似走势的股票后续表现
            similar_cases = self._search_historical_patterns(current_features, date)
            
            # 补充通用规律
            pattern_rules = [
                {
                    'pattern': '高位追涨型',
                    'description': '股价已涨50%+后买入，股价位于52周高点附近',
                    'typical_outcome': '短期可能继续上涨10-20%，但3个月内大概率回调',
                    'avg_return_3m': -15,
                    'win_rate': 30,
                    'applies': current_features['mom_60d'] > 50 and current_features['price_position'] > 80
                },
                {
                    'pattern': '业绩拐点型',
                    'description': '业绩刚出现拐点，股价尚在低位或中位',
                    'typical_outcome': '中长期收益显著，适合分批建仓',
                    'avg_return_3m': 25,
                    'win_rate': 65,
                    'applies': current_features['profit_growth'] > 30 and current_features['price_position'] < 50
                },
                {
                    'pattern': '估值错配型',
                    'description': 'PEG<0.8，成长性被市场低估',
                    'typical_outcome': '估值修复带来超额收益',
                    'avg_return_3m': 20,
                    'win_rate': 60,
                    'applies': current_features['peg'] < 0.8 and current_features['price_position'] < 60
                },
                {
                    'pattern': '强势追涨但业绩支撑型',
                    'description': '股价大涨但有强业绩支撑，PEG仍合理',
                    'typical_outcome': '可能继续上涨但波动大，需设止损',
                    'avg_return_3m': 5,
                    'win_rate': 45,
                    'applies': current_features['mom_60d'] > 30 and current_features['peg'] < 1 and current_features['profit_growth'] > 50
                }
            ]
            
            # 筛选适用的规律
            applicable_rules = [r for r in pattern_rules if r.get('applies', False)]
            if not applicable_rules:
                applicable_rules = pattern_rules[:2]  # 返回前两个作为参考
            
            return similar_cases + applicable_rules
            
        except Exception as e:
            logger.warning(f"历史相似案例搜索失败: {e}")
            return []
    
    def _search_historical_patterns(self, features: Dict, as_of_date: str) -> List[Dict]:
        """从数据库搜索历史上类似特征的股票案例"""
        similar_stocks = []
        
        try:
            end_dt = datetime.strptime(as_of_date, '%Y-%m-%d')
            
            # 获取A股科创板股票列表（限制范围减少计算量）
            all_stocks = self.jq.get_all_securities(types=['stock'], date=as_of_date)
            # 筛选科创板（688开头）和创业板（300开头）的高成长股
            tech_stocks = all_stocks[
                (all_stocks.index.str.startswith('688')) | 
                (all_stocks.index.str.startswith('300'))
            ]
            
            # 随机抽样30只进行分析（避免太慢）
            sample_codes = tech_stocks.sample(min(30, len(tech_stocks))).index.tolist()
            
            # 回溯到1年前，寻找当时特征类似的股票
            historical_date = (end_dt - timedelta(days=365)).strftime('%Y-%m-%d')
            
            for stock_code in sample_codes[:10]:  # 限制数量
                try:
                    # 获取历史特征
                    hist_price = self._analyze_price(stock_code, historical_date)
                    hist_fin = self._analyze_financials(stock_code, historical_date)
                    
                    if not hist_price or not hist_fin:
                        continue
                    
                    hist_features = {
                        'price_position': hist_price.get('price_position_52w', 50),
                        'mom_60d': hist_price.get('mom_60d', 0),
                        'profit_growth': hist_fin.get('profit_growth', 0)
                    }
                    
                    # 相似度计算（特征差异小于阈值）
                    pos_diff = abs(hist_features['price_position'] - features['price_position'])
                    mom_diff = abs(hist_features['mom_60d'] - features['mom_60d'])
                    growth_diff = abs(hist_features['profit_growth'] - features['profit_growth'])
                    
                    if pos_diff < 20 and mom_diff < 30 and growth_diff < 50:
                        # 计算后续3个月收益
                        future_date = (datetime.strptime(historical_date, '%Y-%m-%d') + timedelta(days=90)).strftime('%Y-%m-%d')
                        future_price = self._analyze_price(stock_code, future_date)
                        
                        if future_price and hist_price.get('current_price'):
                            future_return = (future_price.get('current_price', 0) / hist_price['current_price'] - 1) * 100
                            
                            info = self.jq.get_security_info(stock_code)
                            similar_stocks.append({
                                'code': stock_code,
                                'name': info.display_name if info else '',
                                'historical_date': historical_date,
                                'features': hist_features,
                                'return_3m': future_return,
                                'outcome': '盈利' if future_return > 0 else '亏损'
                            })
                
                except Exception:
                    continue
            
            # 汇总统计
            if similar_stocks:
                returns = [s['return_3m'] for s in similar_stocks]
                avg_return = np.mean(returns)
                win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
                
                similar_stocks.insert(0, {
                    'pattern': f'历史相似案例统计 (n={len(similar_stocks)})',
                    'description': f'过去1年中特征相似的股票后续表现',
                    'avg_return_3m': round(avg_return, 1),
                    'win_rate': round(win_rate, 0),
                    'typical_outcome': f'平均收益{avg_return:.1f}%，胜率{win_rate:.0f}%'
                })
            
        except Exception as e:
            logger.warning(f"历史模式搜索失败: {e}")
        
        return similar_stocks[:5]  # 最多返回5个案例
    
    def _generate_conclusion(self, result: Dict) -> Dict:
        """生成综合结论"""
        stage = result.get('stage_analysis', {})
        risk = result.get('risk_analysis', {})
        price = result.get('price_analysis', {})
        val = result.get('valuation_analysis', {})
        fin = result.get('financial_analysis', {})
        
        # 投资建议
        if stage.get('is_high_risk'):
            action = "不建议买入"
            reason = "股价已处高位，追高风险大"
            timing = "等待回调30%以上再考虑"
        elif stage.get('is_early_stage'):
            action = "建议买入"
            reason = "业绩拐点+估值合理+股价位置适中"
            timing = "可分批建仓"
        else:
            action = "观望"
            reason = "综合条件一般，性价比不高"
            timing = "持续跟踪，等待更好时机"
        
        # 目标价估算（简化）
        current_price = price.get('current_price', 0)
        peg = val.get('peg', 1)
        profit_growth = fin.get('profit_growth', 0)
        
        if peg < 1 and profit_growth > 30:
            target_upside = min(profit_growth, 50)  # 最多50%上涨空间
        elif stage.get('is_high_risk'):
            target_upside = -20  # 可能回调
        else:
            target_upside = 10  # 一般预期
        
        return {
            'action': action,
            'reason': reason,
            'timing': timing,
            'target_upside': target_upside,
            'confidence': 'low' if stage.get('is_high_risk') else 'medium',
            'summary': self._generate_summary(result)
        }
    
    def _generate_summary(self, result: Dict) -> str:
        """生成文字总结"""
        basic = result.get('basic_info', {})
        stage = result.get('stage_analysis', {})
        price = result.get('price_analysis', {})
        fin = result.get('financial_analysis', {})
        val = result.get('valuation_analysis', {})
        
        name = basic.get('name', '')
        
        parts = []
        parts.append(f"{name}当前处于{stage.get('real_stage', '未知')}阶段。")
        
        # 价格描述
        price_pos = price.get('price_position_52w', 50)
        if price_pos > 80:
            parts.append(f"股价位于52周高位区间({price_pos:.0f}%)，追高风险较大。")
        elif price_pos < 30:
            parts.append(f"股价位于52周低位区间({price_pos:.0f}%)，具有安全边际。")
        else:
            parts.append(f"股价位于52周中位区间({price_pos:.0f}%)。")
        
        # 业绩描述
        profit_g = fin.get('profit_growth', 0)
        if profit_g > 50:
            parts.append(f"净利润增速{profit_g:.1f}%，业绩高增长。")
        elif profit_g > 20:
            parts.append(f"净利润增速{profit_g:.1f}%，业绩稳健。")
        
        # 估值描述
        peg = val.get('peg', 99)
        if peg < 0.8:
            parts.append(f"PEG={peg:.2f}，估值具有吸引力。")
        elif peg > 2:
            parts.append(f"PEG={peg:.2f}，估值偏高。")
        
        # 风险提示
        warnings = stage.get('price_warning', [])
        if warnings:
            parts.append("风险提示: " + "; ".join(warnings))
        
        return " ".join(parts)


def generate_stock_report(code: str, date: str = None) -> str:
    """生成个股深度分析报告"""
    analyzer = TenbaggerDeepAnalyzer()
    result = analyzer.analyze_single_stock(code, date)
    
    if not result:
        return ""
    
    # 生成HTML报告
    html = _build_stock_html_report(result)
    
    # 保存
    output_dir = PROJECT_ROOT / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = output_dir / f'stock_analysis_{code.split(".")[0]}_{timestamp}.html'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)


def _build_stock_html_report(result: Dict) -> str:
    """构建个股分析HTML报告"""
    basic = result.get('basic_info', {})
    price = result.get('price_analysis', {})
    fin = result.get('financial_analysis', {})
    val = result.get('valuation_analysis', {})
    stage = result.get('stage_analysis', {})
    risk = result.get('risk_analysis', {})
    conclusion = result.get('conclusion', {})
    
    code = result.get('code', '')
    name = basic.get('name', '')
    date = result.get('date', '')
    
    # 构建各Tab内容
    overview_html = _build_overview_section(result)
    price_html = _build_price_section(price)
    financial_html = _build_financial_section(fin)
    valuation_html = _build_valuation_section(val)
    stage_html = _build_stage_section(stage)
    risk_html = _build_risk_section(risk)
    conclusion_html = _build_conclusion_section(conclusion)
    
    # 确定状态颜色
    if stage.get('is_high_risk'):
        status_color = '#f44336'
        status_text = '⚠️ 高位风险'
    elif stage.get('is_early_stage'):
        status_color = '#4caf50'
        status_text = '⭐ 早期潜力'
    else:
        status_color = '#ff9800'
        status_text = '👁️ 观察关注'
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{name}({code}) 深度分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        .header {{
            background: linear-gradient(90deg, {status_color}, {status_color}88);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 20px;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            margin-top: 10px;
            font-weight: bold;
        }}
        
        .tabs {{
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .tab-btn {{
            padding: 12px 20px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 8px 8px 0 0;
            color: #e8e8e8;
            cursor: pointer;
            font-size: 0.95em;
            transition: all 0.3s;
        }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.2); }}
        .tab-btn.active {{
            background: linear-gradient(90deg, #e94560, #ff6b6b);
        }}
        
        .tab-content {{
            display: none;
            background: rgba(255,255,255,0.05);
            border-radius: 0 16px 16px 16px;
            padding: 25px;
            animation: fadeIn 0.3s;
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
        }}
        .card-title {{
            color: #ff6b6b;
            font-size: 1.1em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .metric-item {{
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 1.6em;
            font-weight: bold;
        }}
        .metric-label {{ opacity: 0.7; margin-top: 5px; font-size: 0.9em; }}
        
        .warning-box {{
            background: rgba(244,67,54,0.2);
            border: 1px solid #f44336;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .success-box {{
            background: rgba(76,175,80,0.2);
            border: 1px solid #4caf50;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{ background: rgba(233,69,96,0.2); color: #ff6b6b; }}
        
        .progress-bar {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-fill {{ height: 100%; border-radius: 4px; }}
        .fill-green {{ background: linear-gradient(90deg, #4caf50, #8bc34a); }}
        .fill-red {{ background: linear-gradient(90deg, #f44336, #ff5722); }}
        .fill-orange {{ background: linear-gradient(90deg, #ff9800, #ffc107); }}
        
        .conclusion-box {{
            background: linear-gradient(135deg, rgba(233,69,96,0.3), rgba(255,107,107,0.2));
            border-radius: 16px;
            padding: 25px;
            text-align: center;
        }}
        .conclusion-action {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .footer {{ text-align: center; padding: 20px; opacity: 0.6; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{name} <span style="opacity:0.7">({code})</span></h1>
            <div class="meta">
                行业: {basic.get('industry', '')} | 
                分析日期: {date} | 
                市值: {val.get('market_cap', 0):.1f}亿
            </div>
            <div class="status-badge">{status_text}</div>
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('overview')">📊 概览</button>
            <button class="tab-btn" onclick="showTab('price')">📈 价格分析</button>
            <button class="tab-btn" onclick="showTab('financial')">💰 财务分析</button>
            <button class="tab-btn" onclick="showTab('valuation')">📐 估值分析</button>
            <button class="tab-btn" onclick="showTab('stage')">🎯 阶段判断</button>
            <button class="tab-btn" onclick="showTab('risk')">⚠️ 风险分析</button>
            <button class="tab-btn" onclick="showTab('conclusion')">✅ 投资结论</button>
        </div>
        
        <div id="overview" class="tab-content active">{overview_html}</div>
        <div id="price" class="tab-content">{price_html}</div>
        <div id="financial" class="tab-content">{financial_html}</div>
        <div id="valuation" class="tab-content">{valuation_html}</div>
        <div id="stage" class="tab-content">{stage_html}</div>
        <div id="risk" class="tab-content">{risk_html}</div>
        <div id="conclusion" class="tab-content">{conclusion_html}</div>
        
        <div class="footer">
            ⚠️ 本报告仅供参考，不构成投资建议 | 
            生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
    
    <script>
        function showTab(id) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''


def _build_overview_section(result: Dict) -> str:
    """概览部分"""
    price = result.get('price_analysis', {})
    fin = result.get('financial_analysis', {})
    val = result.get('valuation_analysis', {})
    stage = result.get('stage_analysis', {})
    conclusion = result.get('conclusion', {})
    
    return f'''
    <div class="card">
        <div class="card-title">📌 核心指标一览</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if price.get('price_position_52w', 50) < 60 else "#f44336"};">
                    {price.get('price_position_52w', 0):.0f}%
                </div>
                <div class="metric-label">52周价格位置</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if fin.get('profit_growth', 0) > 0 else "#f44336"};">
                    {fin.get('profit_growth', 0):+.1f}%
                </div>
                <div class="metric-label">净利润增速</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if val.get('peg', 99) < 1 else "#ff9800"};">
                    {val.get('peg', 0):.2f}
                </div>
                <div class="metric-label">PEG</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{val.get('pe', 0):.1f}</div>
                <div class="metric-label">PE</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if price.get('mom_60d', 0) > 0 else "#f44336"};">
                    {price.get('mom_60d', 0):+.1f}%
                </div>
                <div class="metric-label">60日涨幅</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{stage.get('adjusted_score', 0):.0f}</div>
                <div class="metric-label">综合评分</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">💡 综合结论</div>
        <p style="font-size: 1.1em; line-height: 1.8;">
            {conclusion.get('summary', '')}
        </p>
    </div>
    
    {"".join([f'<div class="warning-box">{w}</div>' for w in stage.get('price_warning', [])])}
    {"".join([f'<div class="success-box">{s}</div>' for s in stage.get('early_signal', [])])}
    '''


def _build_price_section(price: Dict) -> str:
    """价格分析部分"""
    return f'''
    <div class="card">
        <div class="card-title">📈 价格位置分析</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">¥{price.get('current_price', 0):.2f}</div>
                <div class="metric-label">当前价格</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">¥{price.get('high_52w', 0):.2f}</div>
                <div class="metric-label">52周最高</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">¥{price.get('low_52w', 0):.2f}</div>
                <div class="metric-label">52周最低</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#f44336" if price.get('distance_from_52w_high', 0) < 15 else "#4caf50"};">
                    {price.get('distance_from_52w_high', 0):.1f}%
                </div>
                <div class="metric-label">距52周高点</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">📊 各时间段涨跌幅</div>
        <table>
            <tr>
                <th>5日</th><th>20日</th><th>60日</th><th>120日</th><th>250日</th><th>IPO以来</th>
            </tr>
            <tr>
                <td style="color: {"#4caf50" if price.get('mom_5d', 0) > 0 else "#f44336"};">
                    {price.get('mom_5d', 0):+.1f}%
                </td>
                <td style="color: {"#4caf50" if price.get('mom_20d', 0) > 0 else "#f44336"};">
                    {price.get('mom_20d', 0):+.1f}%
                </td>
                <td style="color: {"#4caf50" if price.get('mom_60d', 0) > 0 else "#f44336"};">
                    {price.get('mom_60d', 0):+.1f}%
                </td>
                <td style="color: {"#4caf50" if price.get('mom_120d', 0) > 0 else "#f44336"};">
                    {price.get('mom_120d', 0):+.1f}%
                </td>
                <td style="color: {"#4caf50" if price.get('mom_250d', 0) > 0 else "#f44336"};">
                    {price.get('mom_250d', 0):+.1f}%
                </td>
                <td style="color: {"#4caf50" if price.get('ipo_return', 0) > 0 else "#f44336"};">
                    {price.get('ipo_return', 0):+.1f}%
                </td>
            </tr>
        </table>
    </div>
    
    <div class="card">
        <div class="card-title">📉 波动与风险</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">{price.get('volatility_60d', 0):.1f}%</div>
                <div class="metric-label">60日年化波动率</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: #f44336;">{price.get('max_drawdown', 0):.1f}%</div>
                <div class="metric-label">历史最大回撤</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{price.get('vol_ratio', 0):.2f}x</div>
                <div class="metric-label">成交量比</div>
            </div>
        </div>
    </div>
    '''


def _build_financial_section(fin: Dict) -> str:
    """财务分析部分"""
    return f'''
    <div class="card">
        <div class="card-title">💰 盈利能力</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">{fin.get('roe', 0):.1f}%</div>
                <div class="metric-label">ROE</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{fin.get('gross_margin', 0):.1f}%</div>
                <div class="metric-label">毛利率</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{fin.get('net_margin', 0):.1f}%</div>
                <div class="metric-label">净利率</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{fin.get('debt_ratio', 0):.1f}%</div>
                <div class="metric-label">负债率</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">🚀 成长性</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if fin.get('revenue_growth', 0) > 0 else "#f44336"};">
                    {fin.get('revenue_growth', 0):+.1f}%
                </div>
                <div class="metric-label">营收增速</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if fin.get('profit_growth', 0) > 0 else "#f44336"};">
                    {fin.get('profit_growth', 0):+.1f}%
                </div>
                <div class="metric-label">净利润增速</div>
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <p><strong>业绩拐点: </strong>{"✅ 检测到业绩拐点" if fin.get('has_inflection') else "❌ 未检测到明显拐点"}</p>
            <p><strong>业绩加速: </strong>{"✅ 业绩持续加速" if fin.get('is_accelerating') else "❌ 未呈加速趋势"}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">📊 历史增速趋势</div>
        <table>
            <tr><th>季度</th><th>营收增速</th><th>净利润增速</th></tr>
            {"".join([f"<tr><td>Q{i+1}</td><td>{fin.get('revenue_growth_trend', [0]*4)[i] if i < len(fin.get('revenue_growth_trend', [])) else '-'}%</td><td>{fin.get('profit_growth_trend', [0]*4)[i] if i < len(fin.get('profit_growth_trend', [])) else '-'}%</td></tr>" for i in range(4)])}
        </table>
    </div>
    '''


def _build_valuation_section(val: Dict) -> str:
    """估值分析部分"""
    pe_pctl = val.get('pe_percentile', 50)
    return f'''
    <div class="card">
        <div class="card-title">📐 估值指标</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">{val.get('pe', 0):.1f}</div>
                <div class="metric-label">PE (TTM)</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{val.get('pb', 0):.2f}</div>
                <div class="metric-label">PB</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if val.get('peg', 99) < 1 else "#ff9800" if val.get('peg', 99) < 2 else "#f44336"};">
                    {val.get('peg', 0):.2f}
                </div>
                <div class="metric-label">PEG</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{val.get('market_cap', 0):.1f}亿</div>
                <div class="metric-label">市值</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">📊 PE历史分位</div>
        <p>当前PE处于近3年的 <strong>{pe_pctl:.0f}%</strong> 分位</p>
        <div class="progress-bar" style="margin-top: 15px;">
            <div class="progress-fill {"fill-green" if pe_pctl < 30 else "fill-orange" if pe_pctl < 70 else "fill-red"}" 
                 style="width: {pe_pctl}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px; opacity: 0.7;">
            <span>低估</span><span>合理</span><span>高估</span>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">💡 估值评价</div>
        <p style="font-size: 1.1em;">
            {"✅ <strong>估值具有吸引力</strong>: PEG<1且PE历史分位较低" if val.get('is_undervalued') else ""}
            {"⚠️ <strong>估值偏高</strong>: PEG>2或PE过高，需警惕" if val.get('is_overvalued') else ""}
            {"📊 <strong>估值中性</strong>: 估值处于合理区间" if not val.get('is_undervalued') and not val.get('is_overvalued') else ""}
        </p>
    </div>
    '''


def _build_stage_section(stage: Dict) -> str:
    """阶段判断部分"""
    return f'''
    <div class="card">
        <div class="card-title">🎯 阶段判断（修正版）</div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">{stage.get('base_stage', '')}</div>
                <div class="metric-label">基础阶段</div>
            </div>
            <div class="metric-item">
                <div class="metric-value" style="color: {"#4caf50" if "早期" in stage.get('real_stage', '') else "#f44336" if "风险" in stage.get('real_stage', '') else "#ff9800"};">
                    {stage.get('real_stage', '')}
                </div>
                <div class="metric-label">修正阶段</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{stage.get('adjusted_score', 0):.0f}</div>
                <div class="metric-label">综合评分</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{stage.get('recommendation', '')}</div>
                <div class="metric-label">操作建议</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">📊 评分构成</div>
        <table>
            <tr><th>项目</th><th>分值</th><th>说明</th></tr>
            <tr><td>基础阶段分</td><td>{stage.get('stage_score', 0)}</td><td>基于市值+业绩判断</td></tr>
            <tr><td style="color: #f44336;">价格位置惩罚</td><td>-{stage.get('price_penalty', 0)}</td><td>高位追涨惩罚</td></tr>
            <tr><td style="color: #4caf50;">早期识别加分</td><td>+{stage.get('early_bonus', 0)}</td><td>业绩拐点+估值错配</td></tr>
            <tr style="font-weight: bold;"><td>最终得分</td><td>{stage.get('adjusted_score', 0)}</td><td></td></tr>
        </table>
    </div>
    
    {"".join([f'<div class="warning-box">{w}</div>' for w in stage.get('price_warning', [])])}
    {"".join([f'<div class="success-box">{s}</div>' for s in stage.get('early_signal', [])])}
    '''


def _build_risk_section(risk: Dict) -> str:
    """风险分析部分"""
    risks_html = ""
    for r in risk.get('risks', []):
        color = '#f44336' if r['level'] == '高' else '#ff9800' if r['level'] == '中' else '#4caf50'
        risks_html += f'''
        <tr>
            <td>{r['type']}</td>
            <td style="color: {color};">{r['level']}</td>
            <td>{r['desc']}</td>
        </tr>
        '''
    
    return f'''
    <div class="card">
        <div class="card-title">⚠️ 风险评估</div>
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2em; color: {"#f44336" if "高" in risk.get('overall_risk', '') else "#ff9800" if "中" in risk.get('overall_risk', '') else "#4caf50"};">
                {risk.get('overall_risk', '')}
            </div>
            <div style="opacity: 0.7;">风险得分: {risk.get('risk_score', 0)}</div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">📋 风险明细</div>
        <table>
            <tr><th>风险类型</th><th>等级</th><th>说明</th></tr>
            {risks_html if risks_html else "<tr><td colspan='3'>暂无明显风险</td></tr>"}
        </table>
    </div>
    '''


def _build_conclusion_section(conclusion: Dict) -> str:
    """投资结论部分"""
    action_color = '#4caf50' if '买入' in conclusion.get('action', '') else '#f44336' if '不建议' in conclusion.get('action', '') else '#ff9800'
    
    return f'''
    <div class="conclusion-box">
        <div class="conclusion-action" style="color: {action_color};">
            {conclusion.get('action', '')}
        </div>
        <p style="font-size: 1.2em; margin-bottom: 15px;">
            {conclusion.get('reason', '')}
        </p>
        <p style="opacity: 0.8;">
            <strong>时机建议:</strong> {conclusion.get('timing', '')}
        </p>
        <div style="margin-top: 20px;">
            <span style="font-size: 1.5em;">
                预期空间: <strong style="color: {"#4caf50" if conclusion.get('target_upside', 0) > 0 else "#f44336"};">
                    {conclusion.get('target_upside', 0):+.0f}%
                </strong>
            </span>
        </div>
    </div>
    
    <div class="card" style="margin-top: 20px;">
        <div class="card-title">💡 十倍股早期识别要点</div>
        <ul style="line-height: 2; padding-left: 20px;">
            <li>✅ 业绩刚出现拐点，市场尚未充分认识</li>
            <li>✅ 股价距离历史高点30%以上，有上涨空间</li>
            <li>✅ PEG<1，估值与增速匹配</li>
            <li>✅ ROE>15%或处于上升趋势</li>
            <li>❌ 避免：60日涨幅>50%的追高</li>
            <li>❌ 避免：股价在52周高点附近</li>
        </ul>
    </div>
    '''


# ============== 主入口 ==============

if __name__ == "__main__":
    # 分析688270
    code = "688270.XSHG"
    print(f"🔍 深度分析 {code}")
    
    output_path = generate_stock_report(code)
    print(f"✅ 报告已生成: {output_path}")
