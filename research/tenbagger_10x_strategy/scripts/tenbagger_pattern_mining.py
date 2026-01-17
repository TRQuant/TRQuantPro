#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
历史十倍股规律挖掘
目标：找出十倍股的共同特征，用于预测未来十倍股
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TenbaggerPatternMiner:
    """十倍股规律挖掘器"""
    
    def __init__(self):
        self.jq = None
        self._ensure_jqdata()
        
        # 历史十倍股案例（2019-2024年涨幅超过10倍的股票）
        self.historical_tenbaggers = [
            # 科创板
            ('688981.XSHG', '中芯国际', 2020),  # 芯片龙头
            ('688012.XSHG', '中微公司', 2020),  # 半导体设备
            ('688008.XSHG', '澜起科技', 2020),  # 内存接口芯片
            # 创业板
            ('300750.XSHE', '宁德时代', 2020),  # 新能源电池
            ('300059.XSHE', '东方财富', 2020),  # 互联网券商
            ('300124.XSHE', '汇川技术', 2021),  # 工业自动化
            ('300760.XSHE', '迈瑞医疗', 2020),  # 医疗器械
            # 主板
            ('600519.XSHG', '贵州茅台', 2019),  # 高端白酒
            ('002475.XSHE', '立讯精密', 2020),  # 消费电子
            ('000858.XSHE', '五粮液', 2019),    # 高端白酒
        ]
    
    def _ensure_jqdata(self):
        if self.jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
            logger.info(f"✅ JQData: {config['username']}")
    
    def analyze_single_stock(self, stock_code: str, name: str, start_year: int) -> dict:
        """分析单只十倍股的特征"""
        try:
            start_date = f"{start_year}-01-01"
            end_date = f"{start_year}-12-31"
            
            # 获取起涨前的财务数据
            from jqdatasdk import query, valuation, income, indicator
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.market_cap,
                income.net_profit,
                income.operating_revenue,
                indicator.roe,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year
            ).filter(
                valuation.code == stock_code
            )
            
            df = self.jq.get_fundamentals(q, date=start_date)
            
            if df is None or len(df) == 0:
                return None
            
            # 获取技术指标
            price_df = self.jq.get_price(
                stock_code, 
                start_date=start_date,
                end_date=end_date,
                fields=['close', 'volume', 'money']
            )
            
            if price_df is None or len(price_df) < 20:
                return None
            
            # 计算特征
            features = {
                'code': stock_code,
                'name': name,
                'year': start_year,
                # 估值
                'pe': df['pe_ratio'].iloc[0] if 'pe_ratio' in df.columns else None,
                'pb': df['pb_ratio'].iloc[0] if 'pb_ratio' in df.columns else None,
                'market_cap': df['market_cap'].iloc[0] if 'market_cap' in df.columns else None,
                # 成长性
                'profit_growth': df['inc_net_profit_year_on_year'].iloc[0] if 'inc_net_profit_year_on_year' in df.columns else None,
                'revenue_growth': df['inc_revenue_year_on_year'].iloc[0] if 'inc_revenue_year_on_year' in df.columns else None,
                'roe': df['roe'].iloc[0] if 'roe' in df.columns else None,
                # 技术
                'momentum_60d': (price_df['close'].iloc[-1] / price_df['close'].iloc[0] - 1) if len(price_df) > 60 else None,
                'avg_turnover': (price_df['money'].mean() / 1e8) if 'money' in price_df.columns else None,
            }
            
            return features
            
        except Exception as e:
            logger.warning(f"分析失败 {stock_code}: {e}")
            return None
    
    def mine_patterns(self) -> dict:
        """挖掘十倍股规律"""
        logger.info("\n" + "="*60)
        logger.info("📊 十倍股规律挖掘")
        logger.info("="*60)
        
        results = []
        
        # 并行分析
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.analyze_single_stock, code, name, year): (code, name)
                for code, name, year in self.historical_tenbaggers
            }
            
            for future in as_completed(futures):
                code, name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        logger.info(f"✅ {name}: PE={result['pe']:.1f}, 市值={result['market_cap']/1e8:.0f}亿")
                except Exception as e:
                    logger.warning(f"❌ {name}: {e}")
        
        # 统计共同特征
        if not results:
            return {}
        
        df = pd.DataFrame(results)
        
        patterns = {
            'pe_range': (df['pe'].quantile(0.25), df['pe'].quantile(0.75)),
            'pb_range': (df['pb'].quantile(0.25), df['pb'].quantile(0.75)),
            'market_cap_range': (df['market_cap'].quantile(0.25) / 1e8, df['market_cap'].quantile(0.75) / 1e8),
            'profit_growth_min': df['profit_growth'].quantile(0.25),
            'roe_min': df['roe'].quantile(0.25),
            'momentum_range': (df['momentum_60d'].quantile(0.25), df['momentum_60d'].quantile(0.75)),
        }
        
        logger.info("\n📈 十倍股共同特征:")
        logger.info(f"   PE范围: {patterns['pe_range'][0]:.0f} - {patterns['pe_range'][1]:.0f}")
        logger.info(f"   PB范围: {patterns['pb_range'][0]:.1f} - {patterns['pb_range'][1]:.1f}")
        logger.info(f"   市值范围: {patterns['market_cap_range'][0]:.0f} - {patterns['market_cap_range'][1]:.0f}亿")
        logger.info(f"   利润增速下限: {patterns['profit_growth_min']:.0f}%")
        logger.info(f"   ROE下限: {patterns['roe_min']:.1f}%")
        
        return patterns
    
    def screen_candidates(self, patterns: dict, date: str = None) -> list:
        """根据挖掘的规律筛选候选股"""
        logger.info("\n🔍 筛选十倍股候选...")
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        from jqdatasdk import query, valuation, indicator
        
        # 筛选条件
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap,
            indicator.roe,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year
        ).filter(
            # 科创板和创业板
            valuation.code.like('688%') | valuation.code.like('300%'),
            # PE范围
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 150,
            # 市值：小于1000亿（有成长空间）
            valuation.market_cap < 1e11,
            valuation.market_cap > 5e9,  # 大于50亿（有一定规模）
            # 高ROE
            indicator.roe > 10,
            # 高增长
            indicator.inc_net_profit_year_on_year > 30,
        ).limit(50)
        
        df = self.jq.get_fundamentals(q, date=date)
        
        if df is None or len(df) == 0:
            logger.info("   未找到符合条件的股票")
            return []
        
        # 计算综合评分
        candidates = []
        for _, row in df.iterrows():
            score = 0
            # 高增长加分
            if row['inc_net_profit_year_on_year'] > 50:
                score += 30
            elif row['inc_net_profit_year_on_year'] > 30:
                score += 20
            
            # 高ROE加分
            if row['roe'] > 20:
                score += 25
            elif row['roe'] > 15:
                score += 15
            
            # 合理PE加分
            if 20 < row['pe_ratio'] < 80:
                score += 20
            
            # 中等市值加分（100-500亿最佳）
            cap_bn = row['market_cap'] / 1e8
            if 100 < cap_bn < 500:
                score += 25
            elif 50 < cap_bn < 1000:
                score += 15
            
            candidates.append({
                'code': row['code'],
                'pe': row['pe_ratio'],
                'pb': row['pb_ratio'],
                'market_cap': row['market_cap'] / 1e8,
                'roe': row['roe'],
                'profit_growth': row['inc_net_profit_year_on_year'],
                'score': score
            })
        
        # 排序
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"   筛选出 {len(candidates)} 只候选股")
        for i, c in enumerate(candidates[:10]):
            logger.info(f"   {i+1}. {c['code']} 评分:{c['score']} PE:{c['pe']:.0f} ROE:{c['roe']:.1f}% 增速:{c['profit_growth']:.0f}%")
        
        return candidates


if __name__ == "__main__":
    miner = TenbaggerPatternMiner()
    patterns = miner.mine_patterns()
    candidates = miner.screen_candidates(patterns)
