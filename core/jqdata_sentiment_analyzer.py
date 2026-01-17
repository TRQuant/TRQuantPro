"""
JQData 市场情绪分析器（优化版）

使用JQData的价格数据计算情绪类因子，并进行市场情绪分析。

数据源:
1. get_price - 价格数据（用于计算情绪因子）
   - PSY: 心理线（12日）
   - ARBR: AR/BR人气意愿指标（26日）
   - VR: 成交量变异率（26日）
   - WVAD: 威廉变异离散量（24日）
   
2. finance.CCTV_NEWS - 新闻联播文本 (2009年至今)
   - 用于政策情绪分析

注意:
- 聚宽因子看板（get_factor_kanban_values）提供情绪因子的历史表现数据，
  但不提供当前因子值，因此需要手动计算
- 已优化：添加价格数据缓存，减少API调用，提升性能

Author: TRQuant Team
Date: 2026-01-12 (优化版)
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class SentimentLevel(Enum):
    """情绪级别"""
    EXTREME_FEAR = "极度恐慌"
    FEAR = "恐慌"
    NEUTRAL = "中性"
    GREED = "贪婪"
    EXTREME_GREED = "极度贪婪"


@dataclass
class SentimentResult:
    """情绪分析结果"""
    date: str
    
    # 综合情绪得分 (-100 ~ +100)
    composite_score: float
    sentiment_level: SentimentLevel
    
    # 技术情绪指标
    psy_score: float = 0.0      # 心理线得分
    arbr_score: float = 0.0     # AR/BR得分
    vr_score: float = 0.0       # 成交量变异率得分
    wvad_score: float = 0.0     # 威廉变异离散量得分
    
    # 原始指标值
    psy_value: float = 0.0
    ar_value: float = 0.0
    br_value: float = 0.0
    vr_value: float = 0.0
    
    # 舆情分析
    news_sentiment: float = 0.0  # 新闻情绪 (-1 ~ +1)
    policy_keywords: List[str] = None
    
    # 建议
    signal: str = "neutral"  # bullish/bearish/neutral
    description: str = ""
    
    def __post_init__(self):
        if self.policy_keywords is None:
            self.policy_keywords = []
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['sentiment_level'] = self.sentiment_level.value
        return d


class JQDataSentimentAnalyzer:
    """
    JQData市场情绪分析器
    
    使用JQData的情绪因子和舆情数据分析市场情绪。
    """
    
    # 情绪因子阈值
    THRESHOLDS = {
        'psy': {
            'overbought': 75,      # 超买
            'bullish': 55,         # 偏多
            'oversold': 25,        # 超卖
            'bearish': 45,         # 偏空
        },
        'ar': {
            'overbought': 150,
            'bullish': 110,
            'oversold': 50,
            'bearish': 80,
        },
        'br': {
            'overbought': 200,
            'bullish': 120,
            'oversold': 40,
            'bearish': 80,
        },
        'vr': {
            'overbought': 350,
            'bullish': 150,
            'oversold': 40,
            'bearish': 80,
        }
    }
    
    # 政策关键词 (正面/负面)
    POSITIVE_KEYWORDS = [
        '稳增长', '降准', '降息', '刺激', '扩大内需', '积极财政',
        '改革开放', '科技创新', '战略性新兴产业', '高质量发展',
        '减税降费', '稳就业', '稳预期', '保民生'
    ]
    
    NEGATIVE_KEYWORDS = [
        '风险', '严监管', '去杠杆', '房住不炒', '防范化解',
        '处置不良', '清理整顿', '严厉打击', '违规违法'
    ]
    
    def __init__(self, jq_client=None):
        """
        初始化情绪分析器
        
        Args:
            jq_client: JQData客户端实例
        """
        self._jq_client = jq_client
        self._jq = None
        self._cache: Dict[str, Any] = {}
        
        # 价格数据缓存（避免重复获取）
        self._price_cache: Dict[str, pd.DataFrame] = {}
        self._cache_max_size = 50  # 最多缓存50个日期的数据
        
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                from jqdatasdk import finance, query
                
                # 如果有客户端，使用客户端的认证
                if self._jq_client is not None and hasattr(self._jq_client, 'is_authenticated'):
                    if self._jq_client.is_authenticated():
                        self._jq = jq
                        return
                
                # 否则从配置加载
                import json
                config_path = "/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json"
                with open(config_path, 'r') as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info("JQData情绪分析器认证成功")
            except Exception as e:
                logger.error(f"JQData认证失败: {e}")
                raise
    
    def analyze(self, date: str = None, index_code: str = "000001.XSHG") -> SentimentResult:
        """
        分析市场情绪
        
        Args:
            date: 分析日期 (YYYY-MM-DD格式)，默认最新
            index_code: 指数代码
            
        Returns:
            SentimentResult: 情绪分析结果
        """
        self._ensure_jqdata()
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取情绪因子
        psy_score, psy_value = self._calc_psy_score(date, index_code)
        arbr_score, ar_value, br_value = self._calc_arbr_score(date, index_code)
        vr_score, vr_value = self._calc_vr_score(date, index_code)
        wvad_score = self._calc_wvad_score(date, index_code)
        
        # 获取舆情分析
        news_sentiment, keywords = self._analyze_news(date)
        
        # 计算综合得分 (加权平均)
        composite_score = (
            psy_score * 0.25 +      # 心理线权重25%
            arbr_score * 0.25 +     # AR/BR权重25%
            vr_score * 0.20 +       # VR权重20%
            wvad_score * 0.15 +     # WVAD权重15%
            news_sentiment * 15     # 舆情权重15% (转换为-15~+15)
        )
        
        # 确定情绪级别
        if composite_score >= 50:
            sentiment_level = SentimentLevel.EXTREME_GREED
            signal = "bearish"  # 极度贪婪时反向
            desc = "市场极度贪婪，建议谨慎，可能见顶"
        elif composite_score >= 25:
            sentiment_level = SentimentLevel.GREED
            signal = "neutral"
            desc = "市场情绪偏乐观，保持警惕"
        elif composite_score >= -25:
            sentiment_level = SentimentLevel.NEUTRAL
            signal = "neutral"
            desc = "市场情绪中性，可正常操作"
        elif composite_score >= -50:
            sentiment_level = SentimentLevel.FEAR
            signal = "neutral"
            desc = "市场情绪偏悲观，可逢低关注"
        else:
            sentiment_level = SentimentLevel.EXTREME_FEAR
            signal = "bullish"  # 极度恐慌时反向
            desc = "市场极度恐慌，可能是底部机会"
        
        return SentimentResult(
            date=date,
            composite_score=composite_score,
            sentiment_level=sentiment_level,
            psy_score=psy_score,
            arbr_score=arbr_score,
            vr_score=vr_score,
            wvad_score=wvad_score,
            psy_value=psy_value,
            ar_value=ar_value,
            br_value=br_value,
            vr_value=vr_value,
            news_sentiment=news_sentiment,
            policy_keywords=keywords,
            signal=signal,
            description=desc
        )
    
    def _get_price_data_cached(self, index_code: str, start_date: str, end_date: str, fields: List[str]) -> Optional[pd.DataFrame]:
        """获取价格数据（带缓存）"""
        cache_key = f"{index_code}_{start_date}_{end_date}_{'_'.join(fields)}"
        
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        try:
            df = self._jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=fields
            )
            
            # 处理MultiIndex
            if isinstance(df.index, pd.MultiIndex):
                df = df.reset_index(level='code', drop=True)
            
            # 缓存数据
            if len(self._price_cache) >= self._cache_max_size:
                # 删除最旧的缓存
                oldest_key = next(iter(self._price_cache))
                del self._price_cache[oldest_key]
            
            self._price_cache[cache_key] = df
            return df
        except Exception as e:
            logger.debug(f"获取价格数据失败: {e}")
            return None
    
    def _calc_psy_score(self, date: str, index_code: str) -> tuple:
        """计算心理线得分（优化版：使用缓存）"""
        try:
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=30)
            
            df = self._get_price_data_cached(
                index_code,
                start_dt.strftime('%Y-%m-%d'),
                date,
                ['close']
            )
            
            if df is None or df.empty or len(df) < 12:
                return 0.0, 50.0
            
            # PSY = N日内上涨天数 / N × 100
            close = df['close']
            returns = close.pct_change()
            up_days = (returns > 0).rolling(12).sum().iloc[-1]
            psy = (up_days / 12) * 100
            
            # 转换为得分
            thresh = self.THRESHOLDS['psy']
            if psy > thresh['overbought']:
                score = 30 + (psy - thresh['overbought']) * 0.5  # 超买区，但不过度扣分
            elif psy > thresh['bullish']:
                score = 20
            elif psy > thresh['bearish']:
                score = 0
            elif psy > thresh['oversold']:
                score = -20
            else:
                score = -30 + (thresh['oversold'] - psy) * 0.5  # 超卖区，可能反弹
            
            return np.clip(score, -50, 50), psy
            
        except Exception as e:
            logger.debug(f"PSY计算失败: {e}")
            return 0.0, 50.0
    
    def _calc_arbr_score(self, date: str, index_code: str) -> tuple:
        """计算AR/BR人气意愿指标得分（优化版：使用缓存）"""
        try:
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=40)
            
            df = self._get_price_data_cached(
                index_code,
                start_dt.strftime('%Y-%m-%d'),
                date,
                ['open', 'high', 'low', 'close']
            )
            
            if df is None or df.empty or len(df) < 26:
                return 0.0, 100.0, 100.0
            
            # AR = Σ(H-O) / Σ(O-L) × 100  (26日)
            ho = (df['high'] - df['open']).rolling(26).sum()
            ol = (df['open'] - df['low']).rolling(26).sum()
            ar = (ho / ol * 100).iloc[-1] if ol.iloc[-1] != 0 else 100
            
            # BR = Σ(H-YC) / Σ(YC-L) × 100  (26日)
            yc = df['close'].shift(1)
            hy = (df['high'] - yc).clip(lower=0).rolling(26).sum()
            yl = (yc - df['low']).clip(lower=0).rolling(26).sum()
            br = (hy / yl * 100).iloc[-1] if yl.iloc[-1] != 0 else 100
            
            # 综合AR/BR得分
            ar_thresh = self.THRESHOLDS['ar']
            br_thresh = self.THRESHOLDS['br']
            
            ar_score = 0
            if ar > ar_thresh['overbought']:
                ar_score = 25
            elif ar > ar_thresh['bullish']:
                ar_score = 15
            elif ar > ar_thresh['bearish']:
                ar_score = 0
            elif ar > ar_thresh['oversold']:
                ar_score = -15
            else:
                ar_score = -25
            
            br_score = 0
            if br > br_thresh['overbought']:
                br_score = 25
            elif br > br_thresh['bullish']:
                br_score = 15
            elif br > br_thresh['bearish']:
                br_score = 0
            elif br > br_thresh['oversold']:
                br_score = -15
            else:
                br_score = -25
            
            combined_score = (ar_score + br_score) / 2
            return combined_score, ar, br
            
        except Exception as e:
            logger.debug(f"AR/BR计算失败: {e}")
            return 0.0, 100.0, 100.0
    
    def _calc_vr_score(self, date: str, index_code: str) -> tuple:
        """计算成交量变异率得分（优化版：使用缓存）"""
        try:
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=40)
            
            df = self._get_price_data_cached(
                index_code,
                start_dt.strftime('%Y-%m-%d'),
                date,
                ['close', 'volume']
            )
            
            if df is None or df.empty or len(df) < 26:
                return 0.0, 150.0
            
            close = df['close']
            volume = df['volume']
            returns = close.pct_change()
            
            # VR = Σ(上涨日成交量) / Σ(下跌日成交量) × 100
            up_vol = volume[returns > 0].rolling(26, min_periods=1).sum()
            down_vol = volume[returns < 0].rolling(26, min_periods=1).sum()
            
            # 简化计算
            up_total = volume[returns > 0].sum()
            down_total = volume[returns < 0].sum()
            vr = (up_total / down_total * 100) if down_total > 0 else 150
            
            thresh = self.THRESHOLDS['vr']
            if vr > thresh['overbought']:
                score = 30
            elif vr > thresh['bullish']:
                score = 15
            elif vr > thresh['bearish']:
                score = 0
            elif vr > thresh['oversold']:
                score = -15
            else:
                score = -30
            
            return score, vr
            
        except Exception as e:
            logger.debug(f"VR计算失败: {e}")
            return 0.0, 150.0
    
    def _calc_wvad_score(self, date: str, index_code: str) -> float:
        """计算威廉变异离散量得分（优化版：使用缓存）"""
        try:
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=30)
            
            df = self._get_price_data_cached(
                index_code,
                start_dt.strftime('%Y-%m-%d'),
                date,
                ['open', 'high', 'low', 'close', 'volume']
            )
            
            if df is None or df.empty or len(df) < 24:
                return 0.0
            
            # WVAD = Σ((C-O)/(H-L) × V)
            hl = df['high'] - df['low']
            hl = hl.replace(0, 0.001)  # 避免除零
            wvad_daily = ((df['close'] - df['open']) / hl) * df['volume']
            wvad = wvad_daily.rolling(24).sum().iloc[-1]
            
            # 标准化得分
            if wvad > 0:
                score = min(30, wvad / 1e10 * 10)  # 正向资金流入
            else:
                score = max(-30, wvad / 1e10 * 10)  # 负向资金流出
            
            return score
            
        except Exception as e:
            logger.debug(f"WVAD计算失败: {e}")
            return 0.0
    
    def _analyze_news(self, date: str) -> tuple:
        """分析新闻联播舆情"""
        try:
            from jqdatasdk import finance, query
            
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=7)  # 最近7天新闻
            
            q = query(finance.CCTV_NEWS).filter(
                finance.CCTV_NEWS.day >= start_dt.strftime('%Y-%m-%d'),
                finance.CCTV_NEWS.day <= date
            )
            
            df = self._jq.run_query(q)
            
            if df is None or df.empty:
                return 0.0, []
            
            # 分析关键词
            all_text = ' '.join(df['title'].tolist() + df['content'].tolist())
            
            positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in all_text)
            negative_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in all_text)
            
            # 提取出现的关键词
            found_keywords = []
            for kw in self.POSITIVE_KEYWORDS:
                if kw in all_text:
                    found_keywords.append(f"+{kw}")
            for kw in self.NEGATIVE_KEYWORDS:
                if kw in all_text:
                    found_keywords.append(f"-{kw}")
            
            # 计算情绪得分 (-1 ~ +1)
            total = positive_count + negative_count
            if total > 0:
                sentiment = (positive_count - negative_count) / total
            else:
                sentiment = 0.0
            
            return sentiment, found_keywords[:5]  # 最多返回5个关键词
            
        except Exception as e:
            logger.debug(f"新闻分析失败: {e}")
            return 0.0, []
    
    def get_historical_sentiment(self, start_date: str, end_date: str, 
                                  index_code: str = "000001.XSHG",
                                  sample_interval: int = 5) -> pd.DataFrame:
        """
        获取历史情绪数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            index_code: 指数代码
            sample_interval: 采样间隔 (天)
            
        Returns:
            DataFrame: 历史情绪数据
        """
        self._ensure_jqdata()
        
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        sampled_days = [d.strftime('%Y-%m-%d') for d in trade_days[::sample_interval]]
        
        results = []
        for date in sampled_days:
            try:
                result = self.analyze(date, index_code)
                results.append({
                    'date': result.date,
                    'composite_score': result.composite_score,
                    'sentiment_level': result.sentiment_level.value,
                    'psy_score': result.psy_score,
                    'arbr_score': result.arbr_score,
                    'vr_score': result.vr_score,
                    'news_sentiment': result.news_sentiment,
                    'signal': result.signal
                })
            except Exception as e:
                logger.debug(f"分析 {date} 失败: {e}")
                continue
        
        return pd.DataFrame(results)


# 便捷函数
def get_market_sentiment(date: str = None, index_code: str = "000001.XSHG") -> SentimentResult:
    """
    获取市场情绪 (便捷函数)
    
    Args:
        date: 日期 (YYYY-MM-DD)
        index_code: 指数代码
        
    Returns:
        SentimentResult: 情绪分析结果
    """
    analyzer = JQDataSentimentAnalyzer()
    return analyzer.analyze(date, index_code)

