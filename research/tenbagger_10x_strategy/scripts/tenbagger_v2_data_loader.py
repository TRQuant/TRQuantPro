#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 数据加载器
=====================================

数据源整合:
1. 聚宽数据库(JQData): 财务指标、估值数据、历史价格、行业分类
2. AkShare补充: 当日实时行情、资金流向、舆情指数、北向资金

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_data_loader.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JQDataLoader:
    """聚宽数据加载器"""
    
    def __init__(self):
        self.jq = None
        self._auth()
    
    def _auth(self):
        """认证聚宽"""
        try:
            import jqdatasdk as jq
            config_path = PROJECT_ROOT / "config" / "jqdata_config.json"
            with open(config_path) as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
            logger.info(f"✅ JQData认证成功: {config['username']}")
        except Exception as e:
            logger.error(f"❌ JQData认证失败: {e}")
            raise
    
    def get_all_stocks(self, date: str = None) -> List[str]:
        """获取全部A股列表（剔除ST）"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        all_stocks = self.jq.get_all_securities(types=['stock'], date=date)
        
        # 剔除ST股票
        non_st = all_stocks[~all_stocks['display_name'].str.contains('ST|退')]
        
        logger.info(f"📊 全A股: {len(all_stocks)}, 剔除ST后: {len(non_st)}")
        return non_st.index.tolist()
    
    def get_financial_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """获取财务指标数据"""
        from jqdatasdk import query, indicator, valuation
        
        q = query(
            indicator.code,
            indicator.statDate,
            indicator.roe,
            indicator.roa,
            indicator.gross_profit_margin,
            indicator.net_profit_margin,
            indicator.inc_revenue_year_on_year,
            indicator.inc_net_profit_year_on_year,
            indicator.eps,
            indicator.operating_profit
        ).filter(
            indicator.code.in_(stocks)
        )
        
        df = self.jq.get_fundamentals(q, date=date)
        logger.info(f"📈 获取财务数据: {len(df)} 条")
        return df
    
    def get_valuation_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """获取估值数据"""
        from jqdatasdk import query, valuation
        
        q = query(
            valuation.code,
            valuation.day,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.ps_ratio,
            valuation.pcf_ratio,
            valuation.market_cap,
            valuation.circulating_market_cap,
            valuation.turnover_ratio
        ).filter(
            valuation.code.in_(stocks)
        )
        
        df = self.jq.get_fundamentals(q, date=date)
        logger.info(f"💰 获取估值数据: {len(df)} 条")
        return df
    
    def get_price_data(self, stocks: List[str], end_date: str, days: int = 250) -> Dict[str, pd.DataFrame]:
        """获取历史价格数据"""
        start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days*1.5)).strftime("%Y-%m-%d")
        
        price_data = {}
        batch_size = 50
        
        for i in range(0, len(stocks), batch_size):
            batch = stocks[i:i+batch_size]
            try:
                df = self.jq.get_price(
                    batch,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                    panel=False
                )
                if df is not None and len(df) > 0:
                    for code in batch:
                        stock_df = df[df['code'] == code].copy()
                        if len(stock_df) > 0:
                            stock_df = stock_df.set_index('time')
                            price_data[code] = stock_df
            except Exception as e:
                logger.warning(f"获取价格失败 {batch[:3]}...: {e}")
        
        logger.info(f"📊 获取价格数据: {len(price_data)} 只股票")
        return price_data
    
    def get_industry_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """获取行业分类"""
        industry_data = []
        
        for stock in stocks:
            try:
                info = self.jq.get_industry(stock, date=date)
                if info and stock in info:
                    sw_info = info[stock].get('sw_l1', {})
                    industry_data.append({
                        'code': stock,
                        'industry_code': sw_info.get('industry_code', ''),
                        'industry_name': sw_info.get('industry_name', '')
                    })
            except:
                pass
        
        df = pd.DataFrame(industry_data)
        logger.info(f"🏭 获取行业数据: {len(df)} 条")
        return df
    
    def get_multi_period_financial(self, stock: str, periods: int = 4) -> pd.DataFrame:
        """获取多期财务数据（用于计算加速度）"""
        from jqdatasdk import query, indicator
        
        q = query(
            indicator.code,
            indicator.statDate,
            indicator.inc_revenue_year_on_year,
            indicator.inc_net_profit_year_on_year,
            indicator.roe
        ).filter(
            indicator.code == stock
        ).order_by(
            indicator.statDate.desc()
        ).limit(periods)
        
        df = self.jq.get_fundamentals_continuously(q, count=periods)
        return df


class AkShareLoader:
    """AkShare数据加载器 - 补充数据"""
    
    def __init__(self):
        try:
            import akshare as ak
            self.ak = ak
            logger.info("✅ AkShare加载成功")
        except ImportError:
            logger.warning("⚠️ AkShare未安装，部分功能不可用")
            self.ak = None
    
    def get_realtime_quotes(self, stocks: List[str] = None) -> pd.DataFrame:
        """获取实时行情"""
        if self.ak is None:
            return pd.DataFrame()
        
        try:
            df = self.ak.stock_zh_a_spot_em()
            df = df.rename(columns={
                '代码': 'code',
                '名称': 'name',
                '最新价': 'price',
                '涨跌幅': 'change_pct',
                '涨跌额': 'change',
                '成交量': 'volume',
                '成交额': 'amount',
                '换手率': 'turnover',
                '市盈率-动态': 'pe',
                '市净率': 'pb'
            })
            
            if stocks:
                # 转换代码格式
                stock_codes = [s.split('.')[0] for s in stocks]
                df = df[df['code'].isin(stock_codes)]
            
            logger.info(f"📈 获取实时行情: {len(df)} 条")
            return df
        except Exception as e:
            logger.warning(f"获取实时行情失败: {e}")
            return pd.DataFrame()
    
    def get_money_flow(self, stock_code: str) -> pd.DataFrame:
        """获取个股资金流向"""
        if self.ak is None:
            return pd.DataFrame()
        
        try:
            # 去掉后缀
            code = stock_code.split('.')[0]
            
            # 获取资金流向
            df = self.ak.stock_individual_fund_flow(stock=code, market="sh" if code.startswith('6') else "sz")
            logger.info(f"💰 获取资金流向: {stock_code}")
            return df
        except Exception as e:
            logger.warning(f"获取资金流向失败 {stock_code}: {e}")
            return pd.DataFrame()
    
    def get_north_money_flow(self) -> pd.DataFrame:
        """获取北向资金流向"""
        if self.ak is None:
            return pd.DataFrame()
        
        try:
            df = self.ak.stock_hsgt_north_net_flow_in_em()
            logger.info(f"🌏 获取北向资金: {len(df)} 条")
            return df
        except Exception as e:
            logger.warning(f"获取北向资金失败: {e}")
            return pd.DataFrame()
    
    def get_market_sentiment(self) -> Dict:
        """获取市场情绪指标"""
        if self.ak is None:
            return {}
        
        try:
            sentiment = {}
            
            # 涨跌家数
            df = self.ak.stock_market_activity_legu()
            if len(df) > 0:
                latest = df.iloc[-1]
                sentiment['rise_count'] = latest.get('上涨家数', 0)
                sentiment['fall_count'] = latest.get('下跌家数', 0)
                sentiment['limit_up'] = latest.get('涨停家数', 0)
                sentiment['limit_down'] = latest.get('跌停家数', 0)
            
            logger.info(f"📊 获取市场情绪指标")
            return sentiment
        except Exception as e:
            logger.warning(f"获取市场情绪失败: {e}")
            return {}
    
    def get_concept_stocks(self, concept: str) -> List[str]:
        """获取概念板块成分股"""
        if self.ak is None:
            return []
        
        try:
            df = self.ak.stock_board_concept_cons_em(symbol=concept)
            codes = df['代码'].tolist()
            logger.info(f"🏷️ 获取概念{concept}成分股: {len(codes)} 只")
            return codes
        except Exception as e:
            logger.warning(f"获取概念成分股失败: {e}")
            return []


class TenbaggerV2DataLoader:
    """十倍股V2数据加载器 - 整合所有数据源"""
    
    def __init__(self):
        self.jq_loader = JQDataLoader()
        self.ak_loader = AkShareLoader()
        
        # 缓存
        self._stock_list_cache = None
        self._financial_cache = {}
        self._valuation_cache = {}
        self._price_cache = {}
    
    def load_all_data(self, date: str = None, use_cache: bool = True) -> Dict:
        """加载全部数据"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📦 加载全部数据 - 日期: {date}")
        logger.info(f"{'='*60}")
        
        # 1. 获取股票列表
        stocks = self.jq_loader.get_all_stocks(date)
        
        # 2. 获取财务数据
        financial_df = self.jq_loader.get_financial_data(stocks, date)
        
        # 3. 获取估值数据
        valuation_df = self.jq_loader.get_valuation_data(stocks, date)
        
        # 4. 获取行业数据
        industry_df = self.jq_loader.get_industry_data(stocks[:500], date)  # 限制数量
        
        # 5. 获取实时行情 (AkShare)
        realtime_df = self.ak_loader.get_realtime_quotes()
        
        # 6. 获取北向资金
        north_flow = self.ak_loader.get_north_money_flow()
        
        # 7. 获取市场情绪
        sentiment = self.ak_loader.get_market_sentiment()
        
        # 合并数据
        data = {
            'date': date,
            'stocks': stocks,
            'financial': financial_df,
            'valuation': valuation_df,
            'industry': industry_df,
            'realtime': realtime_df,
            'north_flow': north_flow,
            'sentiment': sentiment
        }
        
        logger.info(f"\n✅ 数据加载完成!")
        logger.info(f"   股票数量: {len(stocks)}")
        logger.info(f"   财务数据: {len(financial_df)}")
        logger.info(f"   估值数据: {len(valuation_df)}")
        
        return data
    
    def load_stock_detail(self, stock_code: str, end_date: str = None, days: int = 250) -> Dict:
        """加载单只股票详细数据"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        logger.info(f"📊 加载股票详情: {stock_code}")
        
        # 1. 价格数据
        price_data = self.jq_loader.get_price_data([stock_code], end_date, days)
        
        # 2. 多期财务数据（用于计算加速度）
        multi_financial = self.jq_loader.get_multi_period_financial(stock_code, 4)
        
        # 3. 资金流向
        money_flow = self.ak_loader.get_money_flow(stock_code)
        
        return {
            'code': stock_code,
            'price': price_data.get(stock_code, pd.DataFrame()),
            'multi_financial': multi_financial,
            'money_flow': money_flow
        }
    
    def calculate_technical_indicators(self, price_df: pd.DataFrame) -> Dict:
        """计算技术指标"""
        if price_df is None or len(price_df) < 20:
            return {}
        
        close = price_df['close']
        volume = price_df['volume']
        
        indicators = {}
        
        # 均线
        indicators['ma5'] = close.rolling(5).mean().iloc[-1]
        indicators['ma20'] = close.rolling(20).mean().iloc[-1]
        indicators['ma60'] = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else indicators['ma20']
        
        # 均线多头
        indicators['ma_bullish'] = close.iloc[-1] > indicators['ma5'] > indicators['ma20']
        
        # 动量
        if len(close) >= 5:
            indicators['momentum_5d'] = (close.iloc[-1] / close.iloc[-5] - 1) * 100
        if len(close) >= 20:
            indicators['momentum_20d'] = (close.iloc[-1] / close.iloc[-20] - 1) * 100
        if len(close) >= 60:
            indicators['momentum_60d'] = (close.iloc[-1] / close.iloc[-60] - 1) * 100
        
        # 波动率
        returns = close.pct_change().dropna()
        if len(returns) >= 20:
            indicators['volatility_20d'] = returns.tail(20).std() * np.sqrt(252) * 100
        
        # 成交量比率
        if len(volume) >= 20:
            vol_5 = volume.tail(5).mean()
            vol_20 = volume.tail(20).mean()
            indicators['volume_ratio'] = vol_5 / vol_20 if vol_20 > 0 else 1
        
        # RSI
        if len(close) >= 14:
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            indicators['rsi_14'] = (100 - (100 / (1 + rs))).iloc[-1]
        
        # 52周高低点位置
        if len(close) >= 250:
            high_52w = close.tail(250).max()
            low_52w = close.tail(250).min()
            indicators['price_position_52w'] = (close.iloc[-1] - low_52w) / (high_52w - low_52w) * 100
        
        # 创新高
        if len(close) >= 20:
            indicators['is_new_high_20d'] = close.iloc[-1] >= close.tail(20).max()
        
        return indicators
    
    def calculate_growth_acceleration(self, multi_financial: pd.DataFrame) -> Dict:
        """计算成长加速度"""
        if multi_financial is None or len(multi_financial) < 2:
            return {}
        
        acceleration = {}
        
        # 按时间排序
        df = multi_financial.sort_values('statDate', ascending=False)
        
        if len(df) >= 2:
            # 营收加速度 = 本期增速 - 上期增速
            rev_growth = df['inc_revenue_year_on_year'].values
            if not np.isnan(rev_growth[0]) and not np.isnan(rev_growth[1]):
                acceleration['revenue_acceleration'] = rev_growth[0] - rev_growth[1]
            
            # 利润加速度
            profit_growth = df['inc_net_profit_year_on_year'].values
            if not np.isnan(profit_growth[0]) and not np.isnan(profit_growth[1]):
                acceleration['profit_acceleration'] = profit_growth[0] - profit_growth[1]
            
            # 连续改善判断
            consecutive_improve = 0
            for i in range(len(df) - 1):
                if df['inc_net_profit_year_on_year'].iloc[i] > df['inc_net_profit_year_on_year'].iloc[i+1]:
                    consecutive_improve += 1
                else:
                    break
            acceleration['consecutive_improve'] = consecutive_improve
        
        return acceleration


# ============================================================
# 测试
# ============================================================

def test_data_loader():
    """测试数据加载器"""
    loader = TenbaggerV2DataLoader()
    
    # 测试加载全部数据
    data = loader.load_all_data()
    
    # 测试加载单股详情
    if data['stocks']:
        detail = loader.load_stock_detail(data['stocks'][0])
        
        # 测试技术指标计算
        if not detail['price'].empty:
            indicators = loader.calculate_technical_indicators(detail['price'])
            print(f"\n技术指标: {indicators}")


if __name__ == "__main__":
    test_data_loader()
