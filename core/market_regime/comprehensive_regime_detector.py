#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
综合市场环境判断模块
====================

多维度综合判断市场环境：
1. 宏观层面：PMI/CPI/M2/社融
2. 资金层面：北向资金/融资融券/主力资金流
3. 技术层面：指数趋势/波动率/成交量
4. 情绪层面：涨跌比/涨停跌停/连板

数据源：
- JQData（聚宽）：专业版数据
- AKShare：实时数据补充

作者：TRQuant Team
创建：2024-12-26
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np
import pandas as pd
import json
import os

logger = logging.getLogger(__name__)

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"


class MarketRegime(Enum):
    """市场环境类型"""
    BULL = "BULL"           # 牛市：趋势向上，资金充裕
    BEAR = "BEAR"           # 熊市：趋势向下，资金流出
    VOLATILE = "VOLATILE"   # 震荡市：方向不明，高波动
    RECOVERY = "RECOVERY"   # 复苏期：底部企稳，资金试探
    DISTRIBUTION = "DISTRIBUTION"  # 派发期：顶部震荡，资金撤离


class DimensionSignal(Enum):
    """维度信号"""
    STRONG_BULLISH = 2      # 强烈看多
    BULLISH = 1             # 看多
    NEUTRAL = 0             # 中性
    BEARISH = -1            # 看空
    STRONG_BEARISH = -2     # 强烈看空


@dataclass
class DimensionScore:
    """维度评分"""
    name: str
    score: float           # -100 到 100
    signal: DimensionSignal
    weight: float          # 权重
    indicators: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    data_source: str = ""
    updated_at: str = ""


@dataclass
class RegimeResult:
    """环境判断结果"""
    regime: MarketRegime
    confidence: float       # 置信度 0-100
    composite_score: float  # 综合得分 -100到100
    
    # 各维度评分
    macro_score: Optional[DimensionScore] = None
    capital_score: Optional[DimensionScore] = None
    technical_score: Optional[DimensionScore] = None
    sentiment_score: Optional[DimensionScore] = None
    
    # 元数据
    analysis_date: str = ""
    previous_regime: Optional[MarketRegime] = None
    regime_duration: int = 0  # 当前环境持续天数
    
    # 建议
    recommended_strategy: str = ""
    recommended_position: float = 0.5  # 建议仓位 0-1
    risk_level: str = "medium"
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "regime": self.regime.value,
            "confidence": self.confidence,
            "composite_score": self.composite_score,
            "dimensions": {
                "macro": self._dim_to_dict(self.macro_score),
                "capital": self._dim_to_dict(self.capital_score),
                "technical": self._dim_to_dict(self.technical_score),
                "sentiment": self._dim_to_dict(self.sentiment_score),
            },
            "analysis_date": self.analysis_date,
            "recommended_strategy": self.recommended_strategy,
            "recommended_position": self.recommended_position,
            "risk_level": self.risk_level,
            "notes": self.notes,
        }
    
    def _dim_to_dict(self, dim: Optional[DimensionScore]) -> Optional[Dict]:
        if dim is None:
            return None
        return {
            "name": dim.name,
            "score": dim.score,
            "signal": dim.signal.name,
            "weight": dim.weight,
            "indicators": dim.indicators,
            "description": dim.description,
        }


class ComprehensiveRegimeDetector:
    """
    综合市场环境检测器
    
    整合多数据源，多维度判断市场环境
    """
    
    def __init__(self):
        self._jq = None
        self._ak = None
        self._config = self._load_config()
        
        # 权重配置
        # 权重配置（优化版：提高技术权重，降低情绪权重）
        self.weights = {
            "macro": 0.25,      # 宏观权重（提高5%）
            "capital": 0.20,    # 资金权重（降低5%，数据不稳定）
            "technical": 0.45,  # 技术权重（提高10%，核心指标）
            "sentiment": 0.10,  # 情绪权重（降低10%，容易异常）
        }
        
        # 环境阈值（基于华泰证券方法和历史回测优化）
        self.thresholds = {
            "BULL": 8,         # 综合得分 > 15 为牛市（降低阈值，提高灵敏度）
            "BEAR": -12,        # 综合得分 < -12 为熊市（提高阈值，减少误判）
            "RECOVERY": -8,    # -12 < 得分 < -8 且趋势向上（复苏期）
            "DISTRIBUTION": 6, # 10 < 得分 < 15 且趋势向下（派发期）
        }
        
        # 历史状态
        self._history: List[RegimeResult] = []
        self._current_regime = MarketRegime.VOLATILE
        self._regime_start_date = None
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_path = f"{PROJECT_ROOT}/config/jqdata_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _ensure_jqdata(self):
        """确保JQData已认证"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                if self._config:
                    jq.auth(self._config.get('username', ''), 
                           self._config.get('password', ''))
                    self._jq = jq
                    logger.info(f"JQData认证成功: {self._config.get('username')}")
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def _ensure_akshare(self):
        """确保AKShare可用"""
        if self._ak is None:
            try:
                import akshare as ak
                self._ak = ak
            except ImportError:
                logger.warning("AKShare未安装")
    
    # ================================================================
    # 宏观维度
    # ================================================================
    
    def analyze_macro(self, date: str = None) -> DimensionScore:
        """
        分析宏观经济环境
        
        指标：
        - PMI：制造业景气度（>50扩张，<50收缩）
        - CPI：通胀水平（2-3%健康）
        - M2：货币供应增速
        - 社融：社会融资规模
        """
        indicators = {}
        score = 0
        descriptions = []
        
        self._ensure_akshare()
        
        try:
            if self._ak:
                # PMI数据
                try:
                    df_pmi = self._ak.macro_china_pmi_yearly()
                    if df_pmi is not None and len(df_pmi) > 0:
                        latest_pmi = float(df_pmi.iloc[-1].get('今值', 50))
                        indicators['pmi'] = latest_pmi
                        
                        if latest_pmi >= 52:
                            score += 30
                            descriptions.append(f"PMI={latest_pmi:.1f}，制造业强劲扩张")
                        elif latest_pmi >= 50:
                            score += 15
                            descriptions.append(f"PMI={latest_pmi:.1f}，制造业温和扩张")
                        elif latest_pmi >= 48:
                            score -= 10
                            descriptions.append(f"PMI={latest_pmi:.1f}，制造业轻微收缩")
                        else:
                            score -= 25
                            descriptions.append(f"PMI={latest_pmi:.1f}，制造业明显收缩")
                except Exception as e:
                    logger.debug(f"获取PMI失败: {e}")
                
                # M2增速
                try:
                    df_m2 = self._ak.macro_china_money_supply()
                    if df_m2 is not None and len(df_m2) > 0:
                        m2_growth = float(df_m2.iloc[-1].get('M2-同比增长', 8))
                        indicators['m2_growth'] = m2_growth
                        
                        if m2_growth > 12:
                            score += 20
                            descriptions.append(f"M2增速{m2_growth:.1f}%，货币宽松")
                        elif m2_growth > 8:
                            score += 10
                            descriptions.append(f"M2增速{m2_growth:.1f}%，货币适度")
                        else:
                            score -= 10
                            descriptions.append(f"M2增速{m2_growth:.1f}%，货币偏紧")
                except Exception as e:
                    logger.debug(f"获取M2失败: {e}")
                
                # CPI
                try:
                    df_cpi = self._ak.macro_china_cpi_yearly()
                    if df_cpi is not None and len(df_cpi) > 0:
                        cpi = float(df_cpi.iloc[-1].get('今值', 2))
                        indicators['cpi'] = cpi
                        
                        if 1 <= cpi <= 3:
                            score += 10
                            descriptions.append(f"CPI={cpi:.1f}%，通胀温和")
                        elif cpi > 5:
                            score -= 20
                            descriptions.append(f"CPI={cpi:.1f}%，通胀过热")
                        elif cpi < 0:
                            score -= 15
                            descriptions.append(f"CPI={cpi:.1f}%，通缩风险")
                except Exception as e:
                    logger.debug(f"获取CPI失败: {e}")
                    
        except Exception as e:
            logger.warning(f"宏观分析失败: {e}")
        
        # 限制得分范围
        score = max(-100, min(100, score))
        
        # 确定信号
        if score >= 30:
            signal = DimensionSignal.STRONG_BULLISH
        elif score >= 10:
            signal = DimensionSignal.BULLISH
        elif score <= -30:
            signal = DimensionSignal.STRONG_BEARISH
        elif score <= -10:
            signal = DimensionSignal.BEARISH
        else:
            signal = DimensionSignal.NEUTRAL
        
        return DimensionScore(
            name="宏观经济",
            score=score,
            signal=signal,
            weight=self.weights['macro'],
            indicators=indicators,
            description="；".join(descriptions) if descriptions else "数据获取中",
            data_source="AKShare",
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
    
    # ================================================================
    # 资金维度
    # ================================================================
    
    def analyze_capital(self, date: str = None) -> DimensionScore:
        """
        分析资金流向
        
        指标：
        - 北向资金：外资流向
        - 融资融券：杠杆资金
        - 主力资金：大单资金流
        """
        indicators = {}
        score = 0
        descriptions = []
        
        self._ensure_akshare()
        self._ensure_jqdata()
        
        try:
            if self._ak:
                # 北向资金
                try:
                    df_north = self._ak.stock_hsgt_north_net_flow_in_em()
                    if df_north is not None and len(df_north) > 0:
                        # 取近5日累计
                        recent = df_north.tail(5)
                        if '当日净买入' in recent.columns:
                            net_flow_5d = recent['当日净买入'].sum() / 1e8
                        else:
                            net_flow_5d = 0
                        indicators['north_flow_5d'] = net_flow_5d
                        
                        if net_flow_5d > 100:
                            score += 25
                            descriptions.append(f"北向资金5日净流入{net_flow_5d:.0f}亿，外资积极")
                        elif net_flow_5d > 0:
                            score += 10
                            descriptions.append(f"北向资金5日净流入{net_flow_5d:.0f}亿")
                        elif net_flow_5d > -100:
                            score -= 10
                            descriptions.append(f"北向资金5日净流出{-net_flow_5d:.0f}亿")
                        else:
                            score -= 25
                            descriptions.append(f"北向资金5日净流出{-net_flow_5d:.0f}亿，外资撤离")
                except Exception as e:
                    logger.debug(f"获取北向资金失败: {e}")
                
                # 融资融券
                try:
                    df_margin = self._ak.stock_margin_sz_sh_summary_em()
                    if df_margin is not None and len(df_margin) > 0:
                        latest = df_margin.iloc[-1]
                        margin_balance = float(latest.get('融资余额', 0)) / 1e8
                        indicators['margin_balance'] = margin_balance
                        
                        # 计算融资余额变化
                        if len(df_margin) > 5:
                            prev = df_margin.iloc[-6]
                            margin_change = (margin_balance - float(prev.get('融资余额', 0)) / 1e8)
                            indicators['margin_change_5d'] = margin_change
                            
                            if margin_change > 100:
                                score += 20
                                descriptions.append(f"融资余额5日增加{margin_change:.0f}亿")
                            elif margin_change < -100:
                                score -= 20
                                descriptions.append(f"融资余额5日减少{-margin_change:.0f}亿")
                except Exception as e:
                    logger.debug(f"获取融资融券失败: {e}")
                    
        except Exception as e:
            logger.warning(f"资金分析失败: {e}")
        
        score = max(-100, min(100, score))
        
        if score >= 30:
            signal = DimensionSignal.STRONG_BULLISH
        elif score >= 10:
            signal = DimensionSignal.BULLISH
        elif score <= -30:
            signal = DimensionSignal.STRONG_BEARISH
        elif score <= -10:
            signal = DimensionSignal.BEARISH
        else:
            signal = DimensionSignal.NEUTRAL
        
        return DimensionScore(
            name="资金流向",
            score=score,
            signal=signal,
            weight=self.weights['capital'],
            indicators=indicators,
            description="；".join(descriptions) if descriptions else "数据获取中",
            data_source="AKShare",
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
    
    # ================================================================
    # 技术维度
    # ================================================================
    
    def analyze_technical(self, date: str = None) -> DimensionScore:
        """
        分析技术指标
        
        指标：
        - 指数趋势：上证/深证/创业板
        - 波动率：市场波动程度
        - 成交量：市场活跃度
        - 均线系统：MA20/MA60/MA250
        """
        indicators = {}
        score = 0
        descriptions = []
        
        self._ensure_jqdata()
        
        try:
            if self._jq:
                jq = self._jq
                end_date = date or datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=300)).strftime("%Y-%m-%d")
                
                # 上证指数分析
                df = jq.get_price("000001.XSHG", start_date=start_date, 
                                 end_date=end_date, frequency='daily',
                                 fields=['close', 'volume'])
                
                if df is not None and len(df) > 60:
                    close = df['close'].values
                    volume = df['volume'].values
                    
                    current = close[-1]
                    ma20 = np.mean(close[-20:])
                    ma60 = np.mean(close[-60:])
                    ma250 = np.mean(close[-250:]) if len(close) >= 250 else np.mean(close)
                    
                    indicators['sh_close'] = current
                    indicators['sh_ma20'] = ma20
                    indicators['sh_ma60'] = ma60
                    indicators['sh_ma250'] = ma250
                    
                    # 趋势判断
                    if current > ma20 > ma60 > ma250:
                        score += 40
                        descriptions.append("多头排列，趋势向上")
                    elif current > ma20 > ma60:
                        score += 25
                        descriptions.append("中期趋势向上")
                    elif current > ma20:
                        score += 10
                        descriptions.append("短期趋势向上")
                    elif current < ma20 < ma60 < ma250:
                        score -= 40
                        descriptions.append("空头排列，趋势向下")
                    elif current < ma20 < ma60:
                        score -= 25
                        descriptions.append("中期趋势向下")
                    elif current < ma20:
                        score -= 10
                        descriptions.append("短期趋势向下")
                    
                    # 波动率分析（基于华泰证券方法）
                    returns = np.diff(np.log(close[-60:]))
                    volatility = np.std(returns) * np.sqrt(252) * 100
                    volatility_20 = np.std(returns[-20:]) * np.sqrt(252) * 100 if len(returns) >= 20 else volatility
                    vol_change = (volatility - volatility_20) / volatility_20 if volatility_20 > 0 else 0
                    indicators['volatility'] = volatility
                    indicators['volatility_change'] = vol_change
                    
                    # 换手率分析（计算市场整体换手率趋势）
                    # 使用成交量相对变化作为换手率代理指标
                    vol_ma20 = np.mean(volume[-20:])
                    vol_ma60 = np.mean(volume[-60:]) if len(volume) >= 60 else vol_ma20
                    turnover_trend = (vol_ma20 - vol_ma60) / vol_ma60 if vol_ma60 > 0 else 0
                    indicators['turnover_trend'] = turnover_trend
                    
                    # 波动率+换手率组合判断（华泰证券方法）
                    # 规则：
                    # 1. 波动率↑+换手率↑ = 牛市（快速上涨伴随高波动和高换手）
                    # 2. 波动率↓+换手率↓ = 震荡市（方向不明朗，小幅涨跌）
                    # 3. 波动率↑+换手率↓ = 熊市（下跌放大波动，成交低迷）
                    # 4. 波动率↓+换手率↑ = 牛市初期或熊市末段反弹
                    
                    vol_rising = vol_change > 0.1  # 波动率上升超过10%
                    vol_falling = vol_change < -0.1  # 波动率下降超过10%
                    turnover_rising = turnover_trend > 0.1  # 换手率上升
                    turnover_falling = turnover_trend < -0.1  # 换手率下降
                    
                    if vol_rising and turnover_rising:
                        # 波动率↑+换手率↑ = 牛市特征
                        score += 30
                        descriptions.append(f"波动率↑+换手率↑，牛市特征（波动{volatility:.1f}%，换手↑{turnover_trend*100:.1f}%）")
                    elif vol_falling and turnover_falling:
                        # 波动率↓+换手率↓ = 震荡市
                        score += 0  # 中性
                        descriptions.append(f"波动率↓+换手率↓，震荡市特征（波动{volatility:.1f}%，换手↓{abs(turnover_trend)*100:.1f}%）")
                    elif vol_rising and turnover_falling:
                        # 波动率↑+换手率↓ = 典型熊市
                        score -= 30
                        descriptions.append(f"波动率↑+换手率↓，熊市特征（波动{volatility:.1f}%，换手↓{abs(turnover_trend)*100:.1f}%）")
                    elif vol_falling and turnover_rising:
                        # 波动率↓+换手率↑ = 牛市初期或熊市末段
                        score += 20
                        descriptions.append(f"波动率↓+换手率↑，可能为牛市初期/熊市末段（波动{volatility:.1f}%，换手↑{turnover_trend*100:.1f}%）")
                    else:
                        # 其他情况，根据波动率绝对值判断
                        if volatility < 15:
                            score += 10
                            descriptions.append(f"波动率{volatility:.1f}%，市场平稳")
                        elif volatility > 30:
                            score -= 15
                            descriptions.append(f"波动率{volatility:.1f}%，市场剧烈波动")
                    
                    # 成交量比率分析（作为补充）
                    vol_ma5 = np.mean(volume[-5:])
                    vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
                    indicators['volume_ratio'] = vol_ratio
                    
                    if vol_ratio > 1.5 and close[-1] > close[-5]:
                        score += 10
                        descriptions.append("放量上涨")
                    elif vol_ratio > 1.5 and close[-1] < close[-5]:
                        score -= 10
                        descriptions.append("放量下跌")
                    elif vol_ratio < 0.7:
                        descriptions.append("成交萎缩")
                        
        except Exception as e:
            logger.warning(f"技术分析失败: {e}")
        
        score = max(-100, min(100, score))
        
        if score >= 30:
            signal = DimensionSignal.STRONG_BULLISH
        elif score >= 10:
            signal = DimensionSignal.BULLISH
        elif score <= -30:
            signal = DimensionSignal.STRONG_BEARISH
        elif score <= -10:
            signal = DimensionSignal.BEARISH
        else:
            signal = DimensionSignal.NEUTRAL
        
        return DimensionScore(
            name="技术分析",
            score=score,
            signal=signal,
            weight=self.weights['technical'],
            indicators=indicators,
            description="；".join(descriptions) if descriptions else "数据获取中",
            data_source="JQData",
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
    
    # ================================================================
    # 情绪维度
    # ================================================================
    
    def analyze_sentiment(self, date: str = None) -> DimensionScore:
        """
        分析市场情绪
        
        指标：
        - 涨跌家数比
        - 涨停跌停比
        - 连板数分布
        - 换手率
        """
        indicators = {}
        score = 0
        descriptions = []
        
        self._ensure_akshare()
        self._ensure_jqdata()
        
        try:
            if self._ak:
                today = datetime.now().strftime("%Y%m%d")
                
                # 涨停数据
                try:
                    df_zt = self._ak.stock_zt_pool_em(date=today)
                    up_limit = len(df_zt) if df_zt is not None else 0
                    indicators['up_limit'] = up_limit
                    
                    # 连板统计
                    if df_zt is not None and '连板数' in df_zt.columns:
                        continuous = df_zt['连板数'].value_counts().to_dict()
                        indicators['continuous_limit'] = continuous
                        high_board = sum(v for k, v in continuous.items() if int(k) >= 3)
                        if high_board > 10:
                            score += 15
                            descriptions.append(f"3板以上{high_board}只，市场活跃")
                except Exception as e:
                    logger.debug(f"获取涨停数据失败: {e}")
                    up_limit = 50
                
                # 跌停数据
                try:
                    df_dt = self._ak.stock_zt_pool_dtgc_em(date=today)
                    down_limit = len(df_dt) if df_dt is not None else 0
                    indicators['down_limit'] = down_limit
                except Exception as e:
                    logger.debug(f"获取跌停数据失败: {e}")
                    down_limit = 10
                
                # 涨跌停比
                if down_limit > 0:
                    zt_ratio = up_limit / (up_limit + down_limit)
                    indicators['zt_ratio'] = zt_ratio
                    
                    if zt_ratio > 0.85:
                        score += 30
                        descriptions.append(f"涨停{up_limit}只/跌停{down_limit}只，情绪高涨")
                    elif zt_ratio > 0.7:
                        score += 15
                        descriptions.append(f"涨停{up_limit}只/跌停{down_limit}只，情绪偏多")
                    elif zt_ratio < 0.3:
                        score -= 30
                        descriptions.append(f"涨停{up_limit}只/跌停{down_limit}只，情绪恐慌")
                    elif zt_ratio < 0.5:
                        score -= 15
                        descriptions.append(f"涨停{up_limit}只/跌停{down_limit}只，情绪偏空")
                        
        except Exception as e:
            logger.warning(f"情绪分析失败: {e}")
        
        # 使用JQData获取涨跌家数
        try:
            if self._jq:
                jq = self._jq
                target_date = date or datetime.now().strftime("%Y-%m-%d")
                
                all_stocks = jq.get_all_securities(types=['stock'], date=target_date)
                if all_stocks is not None and len(all_stocks) > 0:
                    stock_list = all_stocks.index.tolist()[:1000]
                    
                    prices = jq.get_price(stock_list, end_date=target_date, count=2,
                                         frequency='daily', fields=['close'])
                    
                    if prices is not None:
                        advances = declines = 0
                        for stock in stock_list:
                            try:
                                stock_data = prices.loc[:, stock, 'close'].values
                                if len(stock_data) >= 2:
                                    if stock_data[-1] > stock_data[-2]:
                                        advances += 1
                                    else:
                                        declines += 1
                            except:
                                pass
                        
                        total = advances + declines
                        if total > 0:
                            ad_ratio = advances / total
                            indicators['advances'] = advances
                            indicators['declines'] = declines
                            indicators['ad_ratio'] = ad_ratio
                            
                            if ad_ratio > 0.7:
                                score += 20
                                descriptions.append(f"上涨{advances}/下跌{declines}，市场普涨")
                            elif ad_ratio < 0.3:
                                score -= 20
                                descriptions.append(f"上涨{advances}/下跌{declines}，市场普跌")
        except Exception as e:
            logger.debug(f"获取涨跌家数失败: {e}")
        
        score = max(-100, min(100, score))
        
        if score >= 30:
            signal = DimensionSignal.STRONG_BULLISH
        elif score >= 10:
            signal = DimensionSignal.BULLISH
        elif score <= -30:
            signal = DimensionSignal.STRONG_BEARISH
        elif score <= -10:
            signal = DimensionSignal.BEARISH
        else:
            signal = DimensionSignal.NEUTRAL
        
        return DimensionScore(
            name="市场情绪",
            score=score,
            signal=signal,
            weight=self.weights['sentiment'],
            indicators=indicators,
            description="；".join(descriptions) if descriptions else "数据获取中",
            data_source="AKShare+JQData",
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
    
    # ================================================================
    # 综合判断
    # ================================================================
    
    def detect(self, date: str = None) -> RegimeResult:
        """
        综合检测市场环境
        """
        analysis_date = date or datetime.now().strftime("%Y-%m-%d")
        
        # 获取各维度评分
        macro = self.analyze_macro(date)
        capital = self.analyze_capital(date)
        technical = self.analyze_technical(date)
        sentiment = self.analyze_sentiment(date)
        
        # 计算综合得分（增加异常值限制和趋势确认）
        # 限制单维度最大贡献，避免极端值影响
        def clamp_contribution(score, weight, max_contrib=15):
            contrib = score * weight
            return max(-max_contrib, min(max_contrib, contrib))
        
        macro_contrib = clamp_contribution(macro.score, macro.weight)
        capital_contrib = clamp_contribution(capital.score, capital.weight)
        technical_contrib = clamp_contribution(technical.score, technical.weight, max_contrib=20)  # 技术允许更大贡献
        sentiment_contrib = clamp_contribution(sentiment.score, sentiment.weight, max_contrib=8)   # 情绪限制更严格
        
        composite_score = macro_contrib + capital_contrib + technical_contrib + sentiment_contrib
        
        # 趋势确认：技术和宏观同向时加强信号
        if (technical.score > 0 and macro.score > 0) or (technical.score < 0 and macro.score < 0):
            # 技术和宏观同向，增强信号
            composite_score *= 1.2
        
        # 判断市场环境
        regime = self._determine_regime(composite_score, technical)
        
        # 计算置信度
        confidence = self._calculate_confidence(macro, capital, technical, sentiment)
        
        # 生成建议
        strategy, position, risk = self._generate_recommendation(regime, confidence)
        
        # 检查环境变化
        previous = self._current_regime
        if regime != self._current_regime:
            self._current_regime = regime
            self._regime_start_date = analysis_date
        
        duration = 0
        if self._regime_start_date:
            try:
                start = datetime.strptime(self._regime_start_date, "%Y-%m-%d")
                end = datetime.strptime(analysis_date, "%Y-%m-%d")
                duration = (end - start).days
            except:
                pass
        
        notes = []
        if previous != regime:
            notes.append(f"环境变化: {previous.value} -> {regime.value}")
        
        result = RegimeResult(
            regime=regime,
            confidence=confidence,
            composite_score=composite_score,
            macro_score=macro,
            capital_score=capital,
            technical_score=technical,
            sentiment_score=sentiment,
            analysis_date=analysis_date,
            previous_regime=previous if previous != regime else None,
            regime_duration=duration,
            recommended_strategy=strategy,
            recommended_position=position,
            risk_level=risk,
            notes=notes,
        )
        
        self._history.append(result)
        
        return result
    
    def _determine_regime(self, score: float, technical: DimensionScore) -> MarketRegime:
        """根据综合得分和趋势判断环境"""
        
        # 技术趋势判断
        trend_up = technical.signal in [DimensionSignal.BULLISH, DimensionSignal.STRONG_BULLISH]
        trend_down = technical.signal in [DimensionSignal.BEARISH, DimensionSignal.STRONG_BEARISH]
        
        if score > self.thresholds['BULL']:
            return MarketRegime.BULL
        elif score < self.thresholds['BEAR']:
            return MarketRegime.BEAR
        elif self.thresholds['DISTRIBUTION'] < score < self.thresholds['BULL']:
            if trend_down:
                return MarketRegime.DISTRIBUTION
            return MarketRegime.BULL
        elif self.thresholds['BEAR'] < score < self.thresholds['RECOVERY']:
            if trend_up:
                return MarketRegime.RECOVERY
            return MarketRegime.BEAR
        else:
            return MarketRegime.VOLATILE
    
    def _calculate_confidence(self, *dimensions: DimensionScore) -> float:
        """计算判断置信度"""
        signals = [d.signal for d in dimensions if d]
        
        if not signals:
            return 50.0
        
        # 信号一致性
        positive = sum(1 for s in signals if s in [DimensionSignal.BULLISH, DimensionSignal.STRONG_BULLISH])
        negative = sum(1 for s in signals if s in [DimensionSignal.BEARISH, DimensionSignal.STRONG_BEARISH])
        
        consistency = max(positive, negative) / len(signals)
        
        # 基础置信度
        base_confidence = 50 + consistency * 40
        
        # 强信号加成
        strong_signals = sum(1 for s in signals if s in [DimensionSignal.STRONG_BULLISH, DimensionSignal.STRONG_BEARISH])
        base_confidence += strong_signals * 5
        
        return min(95, base_confidence)
    
    def _generate_recommendation(self, regime: MarketRegime, confidence: float) -> Tuple[str, float, str]:
        """生成投资建议"""
        recommendations = {
            MarketRegime.BULL: ("趋势跟踪策略", 0.85, "low"),
            MarketRegime.BEAR: ("防守型策略", 0.15, "high"),
            MarketRegime.VOLATILE: ("网格交易策略", 0.50, "medium"),
            MarketRegime.RECOVERY: ("价值投资策略", 0.60, "medium"),
            MarketRegime.DISTRIBUTION: ("减仓观望策略", 0.35, "high"),
        }
        
        strategy, position, risk = recommendations.get(regime, ("均衡策略", 0.5, "medium"))
        
        # 根据置信度调整仓位
        if confidence < 60:
            position *= 0.8
        elif confidence > 80:
            position = min(0.95, position * 1.1)
        
        return strategy, round(position, 2), risk


# 单例实例
_detector = None

def get_detector() -> ComprehensiveRegimeDetector:
    """获取检测器单例"""
    global _detector
    if _detector is None:
        _detector = ComprehensiveRegimeDetector()
    return _detector


def detect_market_regime(date: str = None) -> Dict:
    """
    便捷函数：检测市场环境
    
    返回字典格式的结果，适合MCP工具调用
    """
    detector = get_detector()
    result = detector.detect(date)
    return result.to_dict()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    detector = ComprehensiveRegimeDetector()
    result = detector.detect()
    
    print("\n" + "="*60)
    print("市场环境综合分析报告")
    print("="*60)
    print(f"分析日期: {result.analysis_date}")
    print(f"市场环境: {result.regime.value}")
    print(f"置信度: {result.confidence:.1f}%")
    print(f"综合得分: {result.composite_score:.1f}")
    print()
    print("各维度评分:")
    for dim in [result.macro_score, result.capital_score, result.technical_score, result.sentiment_score]:
        if dim:
            print(f"  {dim.name}: {dim.score:.1f} ({dim.signal.name})")
            print(f"    {dim.description}")
    print()
    print(f"建议策略: {result.recommended_strategy}")
    print(f"建议仓位: {result.recommended_position*100:.0f}%")
    print(f"风险等级: {result.risk_level}")
