#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股主线板块筛选器
====================

核心理念：
1. 遵循主线板块 - 国家政策支持的热门行业
2. 龙头企业优先
3. 优先早期布局，但上升趋势也可
4. 利用聚宽行业/概念数据挖掘

热门主线板块：
- 脑机接口 (Brain-Computer Interface)
- 钙钛矿/固态电池 (New Energy Storage)
- 人工智能应用 (AI Applications)
- 半导体/芯片 (Semiconductor)
- 新材料 (New Materials)
- 国产替代 (Domestic Substitution)
- 新质生产力 (New Productivity)
- 低空经济 (Low-Altitude Economy)
- 人形机器人 (Humanoid Robot)
- 卫星互联网 (Satellite Internet)

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


# ==================== 热门主线板块定义 ====================

# 使用聚宽精确概念代码
MAINLINE_SECTORS = {
    # ===== 核心主线 - 使用精确概念代码 =====
    '人工智能': {
        'concept_codes': ['SC0022', 'SC0408', 'SC0423', 'SC0350'],  # 人工智能, AIGC, AI智能体, AI语料
        'industry_codes': [],
        'keywords': ['智能', 'AI', '算法', '大模型', '算力'],
        'weight': 1.25,  # 核心赛道高权重
    },
    '半导体芯片': {
        'concept_codes': ['SC0363', 'SC0174', 'SC0311', 'SC0255'],  # 芯片概念, 第三代半导体, MCU芯片, 汽车芯片
        'industry_codes': ['HY007'],  # 聚宽电子行业
        'keywords': ['半导体', '芯片', '晶圆', '封测', '集成电路'],
        'weight': 1.25,
    },
    '新能源电池': {
        'concept_codes': ['SC0318', 'SC0223', 'SC0297', 'SC0390', 'SC0232', 'SC0056'],  
        # 固态电池, 钠离子电池, 钙钛矿电池, 锂电池概念, 储能, 燃料电池
        'industry_codes': [],
        'keywords': ['电池', '储能', '钙钛矿', '固态', '锂电'],
        'weight': 1.15,
    },
    '新材料': {
        'concept_codes': ['SC0131'],  # 新材料
        'industry_codes': [],
        'keywords': ['材料', '碳纤维', '石墨', '稀土', '永磁'],
        'weight': 1.0,
    },
    '脑机接口': {
        # 聚宽暂无专门的脑机接口概念，使用医疗器械+关键词搜索
        'concept_codes': ['SC0371'],  # 医疗器械概念
        'industry_codes': [],
        'keywords': ['脑科学', '神经', '脑机', '脑电', '植入', '神经调控'],
        'weight': 1.3,  # 新兴赛道高权重
    },
    '人形机器人': {
        'concept_codes': ['SC0346', 'SC0361'],  # 人形机器人, 机器人概念
        'industry_codes': [],
        'keywords': ['机器人', '减速器', '伺服', '控制器'],
        'weight': 1.25,  # 热门赛道
    },
    '低空经济': {
        'concept_codes': ['SC0348', 'SC0058'],  # 低空经济, 无人机
        'industry_codes': [],
        'keywords': ['无人机', '低空', '飞行', 'eVTOL'],
        'weight': 1.2,
    },
    '卫星互联网': {
        'concept_codes': [],  # 暂无精确代码
        'industry_codes': [],
        'keywords': ['卫星', '航天', '北斗', '遥感', '星网'],
        'weight': 1.15,
    },
    '信创国产替代': {
        'concept_codes': ['SC0302'],  # 信创
        'industry_codes': [],
        'keywords': ['国产', '自主', '替代', '信创', '华为'],
        'weight': 1.15,
    },
    '医药创新': {
        'concept_codes': ['SC0303'],  # 创新药
        'industry_codes': [],
        'keywords': ['创新药', '生物', '医药', 'ADC', 'GLP'],
        'weight': 1.0,
    },
    '算力': {
        'concept_codes': ['SC0331'],  # 算力租赁
        'industry_codes': [],
        'keywords': ['算力', 'GPU', 'HBM', '服务器'],
        'weight': 1.2,
    },
    '光伏新能源': {
        'concept_codes': ['SC0368', 'SC0216', 'SC0335'],  # 光伏概念, 新能源, BC电池
        'industry_codes': [],
        'keywords': ['光伏', '太阳能', 'BC电池', 'TOPCon'],
        'weight': 1.0,
    },
}


class MainlineScreener:
    """热门主线板块筛选器"""
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
        
        # 筛选参数
        self.params = {
            # 市值范围（亿）
            'min_market_cap': 30,
            'max_market_cap': 2000,
            
            # 基本面
            'min_profit_growth': 10,     # 放宽，主线板块有增速即可
            'min_revenue_growth': 5,     # 放宽
            'min_roe': 0,                # 放宽，新兴产业ROE可能不高
            
            # 估值
            'max_pe': 150,               # 放宽，高成长板块可接受高PE
            'max_peg': 3.0,              # 放宽
            
            # 价格位置 - 适度放宽
            'max_price_position': 85,    # 放宽到85%，允许上升趋势
            'max_mom_60d': 60,           # 放宽到60%
            
            # 上升趋势判断
            'trend_ma_periods': [5, 10, 20, 60],  # 均线周期
        }
    
    def _init_jqdata(self):
        """初始化聚宽数据"""
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
    
    def get_mainline_stocks(self, sectors: List[str] = None, 
                            date: str = None) -> Dict[str, List[str]]:
        """
        获取主线板块股票
        
        Args:
            sectors: 板块列表，None则获取所有主线板块
            date: 日期
            
        Returns:
            {板块名: [股票代码列表]}
        """
        if not self.jq:
            return {}
        
        if sectors is None:
            sectors = list(MAINLINE_SECTORS.keys())
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        result = {}
        
        print(f"\n📊 获取主线板块股票 ({date})")
        print("=" * 50)
        
        for sector_name in sectors:
            if sector_name not in MAINLINE_SECTORS:
                continue
            
            sector_info = MAINLINE_SECTORS[sector_name]
            stocks = set()
            
            # 1. 使用精确概念代码获取股票（最准确）
            for concept_code in sector_info.get('concept_codes', []):
                try:
                    concept_stocks = self.jq.get_concept_stocks(concept_code, date=date)
                    if concept_stocks:
                        stocks.update(concept_stocks)
                except Exception:
                    continue
            
            # 2. 通过行业代码获取
            for industry_code in sector_info.get('industry_codes', []):
                try:
                    industry_stocks = self.jq.get_industry_stocks(industry_code, date=date)
                    if industry_stocks:
                        stocks.update(industry_stocks)
                except Exception:
                    continue
            
            # 3. 通过关键字匹配公司名称（备选方案，仅当前两步获取数量太少时）
            if len(stocks) < 20:
                keywords = sector_info.get('keywords', [])
                keyword_stocks = self._search_by_keywords(keywords, date)
                stocks.update(keyword_stocks)
            
            result[sector_name] = list(stocks)
            count = len(stocks)
            print(f"   {sector_name}: {count} 只{'✅' if count > 50 else '⚠️' if count > 20 else '📝'}")
        
        return result
    
    def _search_by_keywords(self, keywords: List[str], date: str) -> List[str]:
        """通过关键字搜索股票 - 仅作为概念代码获取不到时的补充"""
        result = []
        try:
            all_stocks = self.jq.get_all_securities(types=['stock'], date=date)
            # 排除明显不相关的行业（券商、银行、保险等）
            exclude_keywords = ['证券', '银行', '保险', '信托', '基金', '期货', '租赁', '控股']
            
            for idx, row in all_stocks.iterrows():
                name = row.get('display_name', '')
                
                # 排除金融类股票
                if any(ex in name for ex in exclude_keywords):
                    continue
                
                # 关键词匹配
                for keyword in keywords:
                    if keyword in name:
                        result.append(idx)
                        break
        except Exception:
            pass
        return result
    
    def screen_mainline_stocks(self, 
                               sectors: List[str] = None,
                               date: str = None,
                               include_uptrend: bool = True) -> pd.DataFrame:
        """
        筛选主线板块股票
        
        Args:
            sectors: 指定板块，None则全部
            date: 筛选日期
            include_uptrend: 是否包含非早期但处于上升趋势的股票
            
        Returns:
            筛选结果DataFrame
        """
        if not self.jq:
            return pd.DataFrame()
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        print(f"\n🔍 主线板块十倍股筛选 ({date})")
        print("=" * 60)
        
        # Step 1: 获取主线板块股票
        print("\n📊 Step 1: 获取主线板块股票池...")
        sector_stocks = self.get_mainline_stocks(sectors, date)
        
        # 合并所有板块股票
        all_candidates = {}
        for sector_name, stocks in sector_stocks.items():
            for stock in stocks:
                if stock not in all_candidates:
                    all_candidates[stock] = {
                        'sectors': [sector_name],
                        'weight': MAINLINE_SECTORS.get(sector_name, {}).get('weight', 1.0)
                    }
                else:
                    all_candidates[stock]['sectors'].append(sector_name)
                    # 多板块加权
                    all_candidates[stock]['weight'] = max(
                        all_candidates[stock]['weight'],
                        MAINLINE_SECTORS.get(sector_name, {}).get('weight', 1.0)
                    )
        
        candidate_codes = list(all_candidates.keys())
        print(f"   总候选: {len(candidate_codes)} 只 (去重后)")
        
        if not candidate_codes:
            print("❌ 未找到主线板块股票")
            return pd.DataFrame()
        
        # Step 2: 基本面筛选
        print("\n📊 Step 2: 基本面筛选...")
        fundamentals_passed = self._filter_by_fundamentals(candidate_codes, date)
        print(f"   通过: {len(fundamentals_passed)}")
        
        # Step 3: 估值筛选
        print("\n📊 Step 3: 估值筛选...")
        valuation_passed = self._filter_by_valuation(fundamentals_passed, date)
        print(f"   通过: {len(valuation_passed)}")
        
        # Step 4: 技术面筛选（价格位置 + 趋势）
        print("\n📊 Step 4: 技术面筛选...")
        technical_passed = self._filter_by_technical(
            valuation_passed, date, include_uptrend
        )
        print(f"   通过: {len(technical_passed)}")
        
        # Step 5: 综合评分
        print("\n📊 Step 5: 综合评分...")
        results = self._score_candidates(technical_passed, date, all_candidates)
        
        if not results.empty:
            results = results.sort_values('total_score', ascending=False)
            print(f"\n✅ 最终筛选出 {len(results)} 只主线板块潜力股")
        
        return results
    
    def _filter_by_fundamentals(self, codes: List[str], date: str) -> List[str]:
        """基本面筛选"""
        passed = []
        
        # 分批查询（避免超出限制）
        batch_size = 300
        for i in range(0, len(codes), batch_size):
            batch_codes = codes[i:i+batch_size]
            
            q = self.jq.query(
                self.jq.indicator.code,
                self.jq.indicator.roe,
                self.jq.indicator.inc_revenue_year_on_year,
                self.jq.indicator.inc_net_profit_year_on_year,
            ).filter(
                self.jq.indicator.code.in_(batch_codes)
            )
            
            fin_df = self.jq.get_fundamentals(q, date=date)
            
            if fin_df is None or fin_df.empty:
                continue
            
            for _, row in fin_df.iterrows():
                code = row['code']
                roe = row.get('roe', 0) or 0
                rev_growth = row.get('inc_revenue_year_on_year', 0) or 0
                profit_growth = row.get('inc_net_profit_year_on_year', 0) or 0
                
                # 放宽条件：主线板块有增速即可
                if (profit_growth >= self.params['min_profit_growth'] and
                    rev_growth >= self.params['min_revenue_growth']):
                    passed.append(code)
        
        return passed
    
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
        
        if val_df is None or val_df.empty:
            return []
        
        for _, row in val_df.iterrows():
            code = row['code']
            pe = row.get('pe_ratio', 0) or 0
            market_cap = row.get('market_cap', 0) or 0
            
            if (self.params['min_market_cap'] <= market_cap <= self.params['max_market_cap'] and
                0 < pe <= self.params['max_pe']):
                passed.append(code)
        
        return passed
    
    def _filter_by_technical(self, codes: List[str], date: str, 
                             include_uptrend: bool) -> List[str]:
        """技术面筛选"""
        if not codes:
            return []
        
        passed = []
        end_dt = datetime.strptime(date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=300)
        
        for code in codes[:150]:  # 限制数量
            try:
                df = self.jq.get_price(
                    code,
                    start_date=start_dt.strftime('%Y-%m-%d'),
                    end_date=date,
                    frequency='daily',
                    fields=['high', 'low', 'close', 'volume'],
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
                
                # 均线判断
                ma5 = df['close'].rolling(5).mean().iloc[-1]
                ma10 = df['close'].rolling(10).mean().iloc[-1]
                ma20 = df['close'].rolling(20).mean().iloc[-1]
                ma60 = df['close'].rolling(60).mean().iloc[-1] if len(df) >= 60 else ma20
                
                # 上升趋势判断
                is_uptrend = (ma5 > ma10 > ma20) and (current_price > ma20)
                is_strong_uptrend = is_uptrend and (ma20 > ma60) and (current_price > ma5)
                
                # 筛选条件
                # 1. 早期阶段（价格位置低，涨幅小）
                is_early_stage = price_position <= 60 and mom_60d <= 30
                
                # 2. 上升趋势阶段（允许高位但趋势明确）
                is_trending = is_uptrend and price_position <= 85 and mom_60d <= 60
                
                if is_early_stage:
                    passed.append({
                        'code': code,
                        'price_position': price_position,
                        'mom_60d': mom_60d,
                        'is_uptrend': is_uptrend,
                        'is_strong_uptrend': is_strong_uptrend,
                        'stage': 'early'
                    })
                elif include_uptrend and is_trending:
                    passed.append({
                        'code': code,
                        'price_position': price_position,
                        'mom_60d': mom_60d,
                        'is_uptrend': is_uptrend,
                        'is_strong_uptrend': is_strong_uptrend,
                        'stage': 'trending'
                    })
            
            except Exception:
                continue
        
        return [p['code'] for p in passed]
    
    def _score_candidates(self, codes: List[str], date: str, 
                          all_candidates: Dict) -> pd.DataFrame:
        """综合评分"""
        if not codes:
            return pd.DataFrame()
        
        results = []
        
        for code in codes:
            try:
                score_data = self._score_single_stock(code, date, all_candidates)
                if score_data:
                    results.append(score_data)
            except Exception:
                continue
        
        return pd.DataFrame(results) if results else pd.DataFrame()
    
    def _score_single_stock(self, code: str, date: str, 
                            all_candidates: Dict) -> Optional[Dict]:
        """单只股票评分"""
        try:
            info = self.jq.get_security_info(code)
            name = info.display_name if info else ''
            
            # 获取板块信息
            candidate_info = all_candidates.get(code, {})
            sectors = candidate_info.get('sectors', [])
            sector_weight = candidate_info.get('weight', 1.0)
            
            # 获取价格数据
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=300)
            
            df = self.jq.get_price(
                code,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['high', 'low', 'close', 'volume'],
                skip_paused=True
            )
            
            if df is None or len(df) < 60:
                return None
            
            current_price = df['close'].iloc[-1]
            high_52w = df.tail(252)['high'].max() if len(df) >= 252 else df['high'].max()
            low_52w = df.tail(252)['low'].min() if len(df) >= 252 else df['low'].min()
            price_position = (current_price - low_52w) / (high_52w - low_52w) * 100 if high_52w > low_52w else 50
            mom_60d = (current_price / df['close'].iloc[-60] - 1) * 100 if len(df) >= 60 else 0
            mom_20d = (current_price / df['close'].iloc[-20] - 1) * 100 if len(df) >= 20 else 0
            distance_from_high = (high_52w - current_price) / high_52w * 100
            
            # 均线和趋势
            ma5 = df['close'].rolling(5).mean().iloc[-1]
            ma10 = df['close'].rolling(10).mean().iloc[-1]
            ma20 = df['close'].rolling(20).mean().iloc[-1]
            ma60 = df['close'].rolling(60).mean().iloc[-1] if len(df) >= 60 else ma20
            
            is_uptrend = (ma5 > ma10 > ma20) and (current_price > ma20)
            is_strong_uptrend = is_uptrend and (ma20 > ma60)
            
            # 财务数据
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
            
            # 估值数据
            q2 = self.jq.query(
                self.jq.valuation.pe_ratio,
                self.jq.valuation.market_cap,
                self.jq.valuation.pb_ratio,
            ).filter(self.jq.valuation.code == code)
            val_df = self.jq.get_fundamentals(q2, date=date)
            
            if val_df is None or val_df.empty:
                return None
            
            pe = val_df.iloc[0].get('pe_ratio', 0) or 0
            pb = val_df.iloc[0].get('pb_ratio', 0) or 0
            market_cap = val_df.iloc[0].get('market_cap', 0) or 0
            peg = pe / profit_growth if profit_growth > 0 and pe > 0 else 99
            
            # ========== 评分计算 ==========
            base_score = 40
            
            # 1. 成长性得分 (0-25分)
            growth_score = min(25, profit_growth / 4) if profit_growth > 0 else 0
            
            # 2. 估值得分 (0-15分)
            if peg < 0.8:
                valuation_score = 15
            elif peg < 1.2:
                valuation_score = 10
            elif peg < 2.0:
                valuation_score = 5
            else:
                valuation_score = 0
            
            # 3. 趋势得分 (0-20分)
            if is_strong_uptrend:
                trend_score = 20
            elif is_uptrend:
                trend_score = 12
            elif current_price > ma20:
                trend_score = 5
            else:
                trend_score = 0
            
            # 4. 价格位置得分 (-20 ~ +15)
            if price_position < 40:
                position_score = 15  # 早期低位
            elif price_position < 60:
                position_score = 8   # 中低位
            elif price_position < 75:
                position_score = 0   # 中位
            else:
                position_score = -10  # 高位
            
            # 5. 板块加权 (0-15分)
            sector_score = len(sectors) * 5  # 多板块加分
            sector_score = min(15, sector_score)
            
            # 6. 龙头加分（市值大但仍在成长）
            if market_cap > 300 and profit_growth > 20:
                leader_bonus = 10
            elif market_cap > 100 and profit_growth > 30:
                leader_bonus = 5
            else:
                leader_bonus = 0
            
            # 综合得分（应用板块权重）
            raw_score = (base_score + growth_score + valuation_score + 
                        trend_score + position_score + sector_score + leader_bonus)
            total_score = raw_score * sector_weight
            total_score = max(0, min(100, total_score))
            
            # 阶段判断
            if price_position < 50 and profit_growth > 20:
                stage = "🌱 早期潜力"
                recommendation = "重点关注"
            elif is_strong_uptrend and price_position < 80:
                stage = "📈 主升趋势"
                recommendation = "可择机介入"
            elif is_uptrend:
                stage = "⬆️ 上升趋势"
                recommendation = "观察跟踪"
            else:
                stage = "📊 震荡整理"
                recommendation = "等待信号"
            
            return {
                'code': code,
                'name': name,
                'sectors': ', '.join(sectors[:3]),  # 最多显示3个板块
                'market_cap': round(market_cap, 1),
                'pe': round(pe, 1),
                'pb': round(pb, 2),
                'peg': round(peg, 2),
                'profit_growth': round(profit_growth, 1),
                'revenue_growth': round(revenue_growth, 1),
                'roe': round(roe, 1),
                'price_position': round(price_position, 1),
                'mom_60d': round(mom_60d, 1),
                'mom_20d': round(mom_20d, 1),
                'distance_from_high': round(distance_from_high, 1),
                'is_uptrend': is_uptrend,
                'is_strong_uptrend': is_strong_uptrend,
                'total_score': round(total_score, 0),
                'growth_score': round(growth_score, 1),
                'valuation_score': round(valuation_score, 1),
                'trend_score': round(trend_score, 1),
                'position_score': round(position_score, 1),
                'sector_score': round(sector_score, 1),
                'stage': stage,
                'recommendation': recommendation
            }
        
        except Exception as e:
            return None


def generate_mainline_report(sectors: List[str] = None,
                             date: str = None,
                             top_n: int = 20) -> str:
    """生成主线板块筛选报告"""
    screener = MainlineScreener()
    
    # 执行筛选
    results = screener.screen_mainline_stocks(
        sectors=sectors,
        date=date,
        include_uptrend=True
    )
    
    if results.empty:
        print("❌ 未找到符合条件的主线板块股票")
        return ""
    
    # 取Top N
    top_results = results.head(top_n)
    
    # 生成HTML报告
    html = _build_mainline_html_report(top_results, date, sectors)
    
    # 保存
    output_dir = PROJECT_ROOT / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = output_dir / f'mainline_screen_{timestamp}.html'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告已生成: {output_path}")
    return str(output_path)


def _build_mainline_html_report(df: pd.DataFrame, date: str, 
                                sectors: List[str]) -> str:
    """构建主线板块HTML报告（多Tab页面）"""
    
    # 统计各板块数量
    sector_counts = {}
    for _, row in df.iterrows():
        for sector in row['sectors'].split(', '):
            if sector:
                sector_counts[sector] = sector_counts.get(sector, 0) + 1
    
    sector_stats = ' | '.join([f"{k}: {v}" for k, v in 
                               sorted(sector_counts.items(), key=lambda x: -x[1])[:5]])
    
    # 构建板块分布统计
    sector_dist_html = ""
    for sector, count in sorted(sector_counts.items(), key=lambda x: -x[1]):
        pct = count / len(df) * 100
        sector_dist_html += f'''
        <div class="sector-bar">
            <div class="sector-label">{sector}</div>
            <div class="sector-progress">
                <div class="sector-fill" style="width: {pct}%;"></div>
            </div>
            <div class="sector-count">{count}只 ({pct:.1f}%)</div>
        </div>'''
    
    # 构建股票表格行
    rows_html = ""
    for idx, row in df.iterrows():
        stage_color = '#4caf50' if '早期' in row['stage'] else \
                     '#2196f3' if '主升' in row['stage'] else \
                     '#ff9800' if '上升' in row['stage'] else '#666'
        
        trend_icon = '🔥' if row['is_strong_uptrend'] else \
                    '📈' if row['is_uptrend'] else '➖'
        
        # 过滤异常增速（扭亏为盈导致的极端值）
        profit_growth_display = row['profit_growth']
        if profit_growth_display > 1000:
            profit_growth_display = 999.9
        
        rows_html += f'''
        <tr>
            <td>
                <strong>{row['code']}</strong><br>
                <small>{row['name']}</small>
            </td>
            <td style="font-size: 0.85em; color: #58a6ff;">{row['sectors']}</td>
            <td style="color: {stage_color};">{row['stage']}</td>
            <td>
                <span class="score-badge" style="background: {'#4caf50' if row['total_score'] >= 70 else '#ff9800' if row['total_score'] >= 50 else '#666'};">
                    {row['total_score']:.0f}
                </span>
            </td>
            <td>{row['market_cap']:.0f}亿</td>
            <td style="color: {'#4caf50' if profit_growth_display > 0 else '#f44336'};">
                {profit_growth_display:+.1f}%
            </td>
            <td style="color: {'#4caf50' if row['peg'] < 1 else '#ff9800' if row['peg'] < 2 else '#f44336'};">
                {row['peg']:.2f}
            </td>
            <td style="color: {'#4caf50' if row['price_position'] < 50 else '#ff9800' if row['price_position'] < 75 else '#f44336'};">
                {row['price_position']:.0f}%
            </td>
            <td>{trend_icon}</td>
            <td style="color: {'#f44336' if row['mom_60d'] > 40 else '#4caf50' if row['mom_60d'] < 20 else '#ff9800'};">
                {row['mom_60d']:+.1f}%
            </td>
            <td><strong>{row['recommendation']}</strong></td>
        </tr>
        '''
    
    sectors_display = ', '.join(sectors) if sectors else '全部主线板块'
    
    # 聚宽概念代码说明
    concept_codes_html = ""
    for sector_name, sector_info in MAINLINE_SECTORS.items():
        codes = sector_info.get('concept_codes', [])
        keywords = sector_info.get('keywords', [])
        weight = sector_info.get('weight', 1.0)
        concept_codes_html += f'''
        <tr>
            <td><strong>{sector_name}</strong></td>
            <td style="color: #58a6ff;">{', '.join(codes) if codes else '无(使用关键词)'}</td>
            <td style="color: #a78bfa;">{', '.join(keywords[:3])}</td>
            <td style="color: {'#4caf50' if weight > 1.1 else '#fff'};">{weight:.2f}x</td>
        </tr>'''
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>主线板块十倍股筛选报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%);
            color: #e6edf3;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        .header {{
            background: linear-gradient(90deg, #7c3aed, #2563eb);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 1.1em; }}
        
        .info-bar {{
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        .info-item {{
            background: rgba(255,255,255,0.15);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.95em;
        }}
        
        /* Tab 样式 */
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
            color: #e6edf3;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.2); }}
        .tab-btn.active {{
            background: #7c3aed;
            color: white;
        }}
        .tab-content {{
            display: none;
            background: rgba(255,255,255,0.03);
            border-radius: 0 12px 12px 12px;
            padding: 20px;
        }}
        .tab-content.active {{ display: block; }}
        
        /* 板块分布 */
        .sector-bar {{
            display: flex;
            align-items: center;
            margin: 10px 0;
            gap: 15px;
        }}
        .sector-label {{
            width: 120px;
            font-weight: bold;
        }}
        .sector-progress {{
            flex: 1;
            height: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        .sector-fill {{
            height: 100%;
            background: linear-gradient(90deg, #7c3aed, #2563eb);
            border-radius: 10px;
        }}
        .sector-count {{
            width: 100px;
            text-align: right;
        }}
        
        /* 代码块样式 */
        .code-block {{
            background: #161b22;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            line-height: 1.6;
        }}
        .code-block .comment {{ color: #8b949e; }}
        .code-block .keyword {{ color: #ff7b72; }}
        .code-block .string {{ color: #a5d6ff; }}
        .code-block .function {{ color: #d2a8ff; }}
        
        .results-table {{
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            overflow-x: auto;
            margin-bottom: 25px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 1000px;
        }}
        th {{
            background: #7c3aed;
            padding: 14px 10px;
            text-align: left;
            font-weight: 600;
            white-space: nowrap;
        }}
        td {{
            padding: 14px 10px;
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
        
        .section-title {{
            color: #a78bfa;
            font-size: 1.3em;
            margin: 20px 0 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
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
            <h1>🚀 主线板块十倍股筛选</h1>
            <div class="subtitle">Mainline Sector Tenbagger Screener - 国家战略 + 产业升级</div>
            <div class="info-bar">
                <div class="info-item">📅 {date or '最新'}</div>
                <div class="info-item">📊 {len(df)} 只</div>
                <div class="info-item">🎯 {sectors_display}</div>
            </div>
        </div>
        
        <!-- Tab 导航 -->
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('overview')">📊 筛选结果</button>
            <button class="tab-btn" onclick="showTab('distribution')">📈 板块分布</button>
            <button class="tab-btn" onclick="showTab('concept-codes')">🔢 概念代码</button>
            <button class="tab-btn" onclick="showTab('implementation')">💻 代码实现</button>
        </div>
        
        <!-- Tab 1: 筛选结果 -->
        <div id="overview" class="tab-content active">
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-dot" style="background: #4caf50;"></div>
                    <span>🌱 早期潜力</span>
                </div>
                <div class="legend-item">
                    <div class="legend-dot" style="background: #2196f3;"></div>
                    <span>📈 主升趋势</span>
                </div>
                <div class="legend-item">
                    <div class="legend-dot" style="background: #ff9800;"></div>
                    <span>⬆️ 上升趋势</span>
                </div>
                <div class="legend-item">
                    <span>🔥 = 强势趋势</span>
                </div>
            </div>
            
            <div class="results-table">
                <table>
                    <thead>
                        <tr>
                            <th>股票</th>
                            <th>所属板块</th>
                            <th>阶段</th>
                            <th>综合分</th>
                            <th>市值</th>
                            <th>利润增速</th>
                            <th>PEG</th>
                            <th>价格位置</th>
                            <th>趋势</th>
                            <th>60日涨幅</th>
                            <th>建议</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Tab 2: 板块分布 -->
        <div id="distribution" class="tab-content">
            <h3 class="section-title">📊 板块分布统计</h3>
            <div style="max-width: 800px;">
                {sector_dist_html}
            </div>
            
            <h3 class="section-title">📐 筛选方法论</h3>
            <ul style="padding-left: 20px; line-height: 2;">
                <li><strong>主线聚焦</strong>: 国家政策支持的热门行业</li>
                <li><strong>龙头优先</strong>: 板块内市值较大、业绩优良的龙头企业</li>
                <li><strong>早期识别</strong>: 优先布局价格位置&lt;60%、业绩高增长的早期标的</li>
                <li><strong>趋势兼顾</strong>: 非早期但处于上升趋势的标的也纳入</li>
                <li><strong>多板块加分</strong>: 横跨多个主线板块的标的获得额外权重</li>
            </ul>
        </div>
        
        <!-- Tab 3: 概念代码 -->
        <div id="concept-codes" class="tab-content">
            <h3 class="section-title">🔢 聚宽概念代码映射</h3>
            <p style="margin-bottom: 15px; color: #8b949e;">
                使用聚宽(JQData)精确概念代码获取板块成分股，避免关键词匹配导致的错误分类。
            </p>
            
            <div class="results-table">
                <table style="min-width: 600px;">
                    <thead>
                        <tr>
                            <th>板块名称</th>
                            <th>聚宽概念代码</th>
                            <th>备选关键词</th>
                            <th>权重</th>
                        </tr>
                    </thead>
                    <tbody>
                        {concept_codes_html}
                    </tbody>
                </table>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: rgba(255,165,0,0.1); border-radius: 8px; border-left: 4px solid #ff9800;">
                <strong>⚠️ 注意事项：</strong>
                <ul style="margin-top: 10px; padding-left: 20px;">
                    <li><strong>脑机接口</strong>：聚宽暂无专门概念代码，使用医疗器械(SC0371)+关键词搜索</li>
                    <li><strong>卫星互联网</strong>：使用关键词匹配（卫星、航天、北斗等）</li>
                    <li>关键词匹配已排除金融类股票（券商、银行、保险等）</li>
                </ul>
            </div>
        </div>
        
        <!-- Tab 4: 代码实现 -->
        <div id="implementation" class="tab-content">
            <h3 class="section-title">💻 代码实现说明</h3>
            
            <h4 style="color: #58a6ff; margin: 20px 0 10px;">1. 获取主线板块股票</h4>
            <div class="code-block">
<span class="comment"># 使用聚宽精确概念代码获取股票</span>
<span class="keyword">for</span> concept_code <span class="keyword">in</span> sector_info.get(<span class="string">'concept_codes'</span>, []):
    concept_stocks = jq.<span class="function">get_concept_stocks</span>(concept_code, date=date)
    stocks.update(concept_stocks)

<span class="comment"># 示例：获取人工智能板块</span>
ai_stocks = jq.<span class="function">get_concept_stocks</span>(<span class="string">'SC0022'</span>, date=<span class="string">'2026-01-05'</span>)
            </div>
            
            <h4 style="color: #58a6ff; margin: 20px 0 10px;">2. 基本面筛选</h4>
            <div class="code-block">
<span class="comment"># 查询财务指标</span>
q = jq.<span class="function">query</span>(
    jq.indicator.code,
    jq.indicator.roe,
    jq.indicator.inc_revenue_year_on_year,
    jq.indicator.inc_net_profit_year_on_year,
).<span class="function">filter</span>(
    jq.indicator.code.<span class="function">in_</span>(codes)
)

<span class="comment"># 筛选条件</span>
<span class="keyword">if</span> profit_growth >= <span class="string">10</span> <span class="keyword">and</span> rev_growth >= <span class="string">5</span>:
    passed.append(code)
            </div>
            
            <h4 style="color: #58a6ff; margin: 20px 0 10px;">3. 技术面筛选（趋势判断）</h4>
            <div class="code-block">
<span class="comment"># 均线趋势判断</span>
ma5 = df[<span class="string">'close'</span>].<span class="function">rolling</span>(5).<span class="function">mean</span>().<span class="function">iloc</span>[-1]
ma10 = df[<span class="string">'close'</span>].<span class="function">rolling</span>(10).<span class="function">mean</span>().<span class="function">iloc</span>[-1]
ma20 = df[<span class="string">'close'</span>].<span class="function">rolling</span>(20).<span class="function">mean</span>().<span class="function">iloc</span>[-1]

<span class="comment"># 上升趋势：MA5 > MA10 > MA20 且价格在MA20上方</span>
is_uptrend = (ma5 > ma10 > ma20) <span class="keyword">and</span> (current_price > ma20)

<span class="comment"># 早期阶段：价格位置低 + 涨幅小</span>
is_early_stage = price_position <= <span class="string">60</span> <span class="keyword">and</span> mom_60d <= <span class="string">30</span>
            </div>
            
            <h4 style="color: #58a6ff; margin: 20px 0 10px;">4. 综合评分模型</h4>
            <div class="code-block">
<span class="comment"># 评分维度</span>
growth_score = <span class="function">min</span>(25, profit_growth / 4)     <span class="comment"># 成长性 0-25分</span>
valuation_score = <span class="function">calc_peg_score</span>(peg)          <span class="comment"># 估值 0-15分</span>
trend_score = 20 <span class="keyword">if</span> is_strong_uptrend <span class="keyword">else</span> 12  <span class="comment"># 趋势 0-20分</span>
position_score = 15 <span class="keyword">if</span> price_position < 40 <span class="keyword">else</span> ...  <span class="comment"># 位置 -20~+15分</span>
sector_score = <span class="function">len</span>(sectors) * 5               <span class="comment"># 多板块 0-15分</span>

<span class="comment"># 板块权重加成</span>
total_score = raw_score * sector_weight  <span class="comment"># 人工智能/半导体 = 1.25x</span>
            </div>
            
            <h4 style="color: #58a6ff; margin: 20px 0 10px;">5. 关键词排除逻辑（避免错误分类）</h4>
            <div class="code-block">
<span class="comment"># 排除金融类股票（券商、银行等不会属于半导体板块）</span>
exclude_keywords = [<span class="string">'证券'</span>, <span class="string">'银行'</span>, <span class="string">'保险'</span>, <span class="string">'信托'</span>, <span class="string">'基金'</span>, <span class="string">'期货'</span>]

<span class="keyword">for</span> idx, row <span class="keyword">in</span> all_stocks.<span class="function">iterrows</span>():
    name = row.get(<span class="string">'display_name'</span>, <span class="string">''</span>)
    <span class="keyword">if</span> <span class="function">any</span>(ex <span class="keyword">in</span> name <span class="keyword">for</span> ex <span class="keyword">in</span> exclude_keywords):
        <span class="keyword">continue</span>  <span class="comment"># 跳过金融股</span>
            </div>
        </div>
        
        <div class="footer">
            ⚠️ 本报告仅供参考，不构成投资建议 | 
            主线板块具有政策催化，但波动也较大 | 
            生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
    
    <script>
        function showTab(tabId) {{
            // 隐藏所有tab内容
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            // 移除所有按钮active状态
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            // 显示选中的tab
            document.getElementById(tabId).classList.add('active');
            // 激活对应按钮
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''


# ============== 主入口 ==============

if __name__ == "__main__":
    print("🚀 启动主线板块十倍股筛选器")
    print("=" * 60)
    print("聚焦板块: 人工智能、半导体、新能源电池、新材料、")
    print("         脑机接口、人形机器人、低空经济、卫星互联网")
    print("=" * 60)
    
    # 可以指定特定板块筛选
    # sectors = ['人工智能', '半导体芯片', '人形机器人']
    
    output_path = generate_mainline_report(
        sectors=None,  # None = 全部主线板块
        date=None,     # 最新日期
        top_n=30       # Top 30
    )
    
    if output_path:
        print(f"\n📄 打开报告: file://{output_path}")
