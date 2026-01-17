#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线预测因子组合

基于聚宽正式账号，实现5大类因子组合，用于预测市场主线。

因子分类：
1. 宏观因子（20%）：政策、经济、流动性
2. 资金流因子（30%）：主力资金、北向资金、两融
3. 行业景气因子（25%）：基本面、景气度
4. 技术动量因子（15%）：Alpha191、技术指标
5. 市场情绪因子（10%）：新闻、搜索、社交、龙虎榜
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# 尝试导入依赖
try:
    from core.factors.jqdata_factor_engine import JQDataFactorEngine
    FACTOR_ENGINE_AVAILABLE = True
except ImportError:
    FACTOR_ENGINE_AVAILABLE = False
    logger.warning("JQDataFactorEngine不可用")

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("AKShare不可用")


class MainlinePredictionFactorCombination:
    """
    主线预测因子组合
    
    使用聚宽正式账号获取因子数据，结合AKShare补充数据，
    计算5大类因子得分，预测市场主线强度。
    """
    
    def __init__(
        self,
        jq_client=None,
        akshare_client=None,
        factor_engine=None  # Optional[JQDataFactorEngine]
    ):
        """
        初始化因子组合
        
        Args:
            jq_client: JQData客户端
            akshare_client: AKShare客户端（可选，默认使用ak）
            factor_engine: 因子引擎（可选，自动创建）
        """
        self.jq_client = jq_client
        self.akshare_client = akshare_client if akshare_client else ak if AKSHARE_AVAILABLE else None
        
        # 初始化因子引擎
        if factor_engine:
            self.factor_engine = factor_engine
        elif FACTOR_ENGINE_AVAILABLE:
            # JQDataFactorEngine不需要jq_client参数，它自己管理连接
            self.factor_engine = JQDataFactorEngine()
        else:
            self.factor_engine = None
            logger.warning("因子引擎不可用，部分功能将受限")
        
        # 权重配置（可根据市场环境调整）
        self.weights = {
            'macro': 0.20,              # 宏观因子
            'capital_flow': 0.30,        # 资金流因子（权重最高）
            'industry_prosperity': 0.25, # 行业景气因子
            'technical_momentum': 0.15,   # 技术动量因子
            'market_sentiment': 0.10     # 市场情绪因子
        }
        
        # 不同期限的权重调整
        self.period_weights = {
            'short': {  # 短期（3-5日）
                'macro': 0.10,
                'capital_flow': 0.40,      # 短期更关注资金流
                'industry_prosperity': 0.15,
                'technical_momentum': 0.25,  # 短期更关注技术面
                'market_sentiment': 0.10
            },
            'medium': {  # 中期（15-30日）
                'macro': 0.20,
                'capital_flow': 0.30,
                'industry_prosperity': 0.25,
                'technical_momentum': 0.15,
                'market_sentiment': 0.10
            },
            'long': {  # 长期（60-180日）
                'macro': 0.30,              # 长期更关注宏观
                'capital_flow': 0.20,
                'industry_prosperity': 0.35, # 长期更关注基本面
                'technical_momentum': 0.10,
                'market_sentiment': 0.05
            }
        }
    
    def calculate_mainline_score(
        self,
        industry_code: str,
        date: str,
        period: str = 'medium'  # short/medium/long
    ) -> Dict[str, float]:
        """
        计算主线预测得分
        
        Args:
            industry_code: 行业代码（如申万一级行业代码 '801010'）
            date: 日期 'YYYY-MM-DD'
            period: 期限（short/medium/long）
        
        Returns:
            {
                'total_score': 总分（0-100）,
                'macro_score': 宏观因子得分,
                'capital_flow_score': 资金流因子得分,
                'industry_prosperity_score': 行业景气因子得分,
                'technical_momentum_score': 技术动量因子得分,
                'market_sentiment_score': 市场情绪因子得分,
                'factor_details': 各因子详细数据
            }
        """
        logger.info(f"计算主线预测得分: 行业={industry_code}, 日期={date}, 期限={period}")
        
        # 获取行业股票列表
        stocks = self._get_industry_stocks(industry_code, date)
        if not stocks:
            logger.warning(f"无法获取行业股票列表: {industry_code}")
            return self._empty_score_result()
        
        # 使用对应期限的权重
        weights = self.period_weights.get(period, self.weights)
        
        # 计算各类因子得分
        macro_score, macro_details = self._calculate_macro_score(date)
        capital_score, capital_details = self._calculate_capital_flow_score(stocks, date)
        industry_score, industry_details = self._calculate_industry_score(stocks, date)
        technical_score, technical_details = self._calculate_technical_score(stocks, date)
        sentiment_score, sentiment_details = self._calculate_sentiment_score(stocks, date)
        
        # 加权组合
        total_score = (
            macro_score * weights['macro'] +
            capital_score * weights['capital_flow'] +
            industry_score * weights['industry_prosperity'] +
            technical_score * weights['technical_momentum'] +
            sentiment_score * weights['market_sentiment']
        )
        
        # 确保得分在0-100范围内
        total_score = max(0, min(100, total_score))
        
        result = {
            'total_score': float(total_score),
            'macro_score': float(macro_score),
            'capital_flow_score': float(capital_score),
            'industry_prosperity_score': float(industry_score),
            'technical_momentum_score': float(technical_score),
            'market_sentiment_score': float(sentiment_score),
            'factor_details': {
                'macro': macro_details,
                'capital_flow': capital_details,
                'industry_prosperity': industry_details,
                'technical_momentum': technical_details,
                'market_sentiment': sentiment_details
            },
            'weights_used': weights,
            'period': period,
            'industry_code': industry_code,
            'date': date,
            'n_stocks': len(stocks)
        }
        
        logger.info(f"主线预测得分计算完成: 总分={total_score:.2f}")
        return result
    
    def _get_industry_stocks(self, industry_code: str, date: str) -> List[str]:
        """获取行业股票列表"""
        if not self.jq_client:
            logger.warning("JQData客户端不可用")
            return []
        
        try:
            # 尝试使用JQData获取行业成分股
            stocks = self.jq_client.get_industry_stocks(industry_code, date=date)
            if stocks:
                logger.info(f"✅ 获取行业成分股: {industry_code}, 共{len(stocks)}只")
                return stocks
        except Exception as e:
            logger.warning(f"JQData获取行业成分股失败: {e}")
        
        # 如果JQData失败，尝试使用AKShare
        if self.akshare_client:
            try:
                # AKShare需要行业名称，这里简化处理
                # 实际使用时需要建立行业代码到名称的映射
                logger.warning("AKShare行业股票获取需要行业名称映射")
            except Exception as e:
                logger.warning(f"AKShare获取行业成分股失败: {e}")
        
        return []
    
    def _calculate_macro_score(self, date: str) -> Tuple[float, Dict]:
        """
        计算宏观因子得分（0-100）
        
        使用AKShare获取宏观数据：
        - GDP增长率
        - PMI指数
        - M2增长率
        - 政策支持度（简化处理）
        """
        score = 50.0  # 默认中性得分
        details = {}
        
        if not self.akshare_client:
            logger.warning("AKShare不可用，使用默认宏观得分")
            return score, details
        
        try:
            # 获取PMI数据
            try:
                pmi_data = self.akshare_client.macro_china_pmi()
                if pmi_data is not None and not pmi_data.empty:
                    latest_pmi = pmi_data.iloc[-1] if len(pmi_data) > 0 else None
                    if latest_pmi is not None:
                        pmi_value = latest_pmi.get('PMI', 50)
                        # PMI > 50表示扩张，< 50表示收缩
                        pmi_score = min(100, max(0, 50 + (pmi_value - 50) * 2))
                        details['pmi'] = pmi_value
                        details['pmi_score'] = pmi_score
                        score = pmi_score * 0.5 + score * 0.5  # 部分权重
            except Exception as e:
                logger.debug(f"获取PMI数据失败: {e}")
            
            # 获取M2增长率
            try:
                m2_data = self.akshare_client.macro_china_m2()
                if m2_data is not None and not m2_data.empty:
                    latest_m2 = m2_data.iloc[-1] if len(m2_data) > 0 else None
                    if latest_m2 is not None:
                        m2_growth = latest_m2.get('M2同比增长', 0)
                        # M2增长率在8-12%之间为健康
                        if 8 <= m2_growth <= 12:
                            m2_score = 80
                        elif m2_growth > 12:
                            m2_score = min(100, 80 + (m2_growth - 12) * 2)
                        else:
                            m2_score = max(0, 80 - (8 - m2_growth) * 5)
                        details['m2_growth'] = m2_growth
                        details['m2_score'] = m2_score
                        score = m2_score * 0.3 + score * 0.7
            except Exception as e:
                logger.debug(f"获取M2数据失败: {e}")
            
        except Exception as e:
            logger.warning(f"宏观因子计算失败: {e}")
        
        return score, details
    
    def _calculate_capital_flow_score(
        self,
        stocks: List[str],
        date: str
    ) -> Tuple[float, Dict]:
        """
        计算资金流因子得分（0-100）
        
        使用JQData和AKShare获取：
        - 主力资金净流入
        - 北向资金流向
        - 两融数据
        """
        score = 50.0  # 默认中性得分
        details = {}
        
        if not stocks:
            return score, details
        
        try:
            # 使用JQData获取资金流向数据
            # 注意：聚宽股票专业版不包含分钟资金流向，需要使用其他方法
            
            # 方法1: 使用价格和成交量估算资金流
            if self.jq_client and self.factor_engine:
                try:
                    # 获取最近5日的价格和成交量数据
                    end_date = datetime.strptime(date, '%Y-%m-%d')
                    start_date = end_date - timedelta(days=10)
                    
                    prices = self.jq_client.get_price(
                        stocks[:50],  # 限制股票数量以提高性能
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=date,
                        frequency='daily',
                        fields=['close', 'volume', 'money']
                    )
                    
                    if prices is not None and not prices.empty:
                        # 计算资金流入（价格上涨且成交量放大）
                        recent_data = prices.tail(5)
                        if len(recent_data) > 0:
                            # 计算平均资金流入
                            avg_money = recent_data['money'].mean() if 'money' in recent_data.columns else 0
                            # 简化计算：资金流入得分
                            if avg_money > 0:
                                # 这里需要更复杂的计算，简化处理
                                capital_score = min(100, max(0, 50 + (avg_money / 1e8) * 10))
                                details['avg_money'] = float(avg_money)
                                details['capital_score'] = capital_score
                                score = capital_score
                except Exception as e:
                    logger.debug(f"JQData资金流计算失败: {e}")
            
            # 方法2: 使用AKShare获取北向资金数据
            if self.akshare_client:
                try:
                    # 获取北向资金流向（需要股票代码转换）
                    # 这里简化处理，实际需要将JQData代码转换为AKShare格式
                    pass
                except Exception as e:
                    logger.debug(f"AKShare北向资金获取失败: {e}")
            
        except Exception as e:
            logger.warning(f"资金流因子计算失败: {e}")
        
        return score, details
    
    def _calculate_industry_score(
        self,
        stocks: List[str],
        date: str
    ) -> Tuple[float, Dict]:
        """
        计算行业景气因子得分（0-100）
        
        使用聚宽因子库获取：
        - 营收增长率
        - 净利润增长率
        - ROE
        - ROA
        - 毛利率
        """
        score = 50.0  # 默认中性得分
        details = {}
        
        if not stocks or not self.factor_engine:
            return score, details
        
        try:
            # 使用聚宽因子库中的正确因子名称
            # 根据get_all_factors()查询结果：
            # - 成长类: operating_revenue_growth_rate (营业收入增长率), net_profit_growth_rate (净利润增长率)
            # - 质量类: roe_ttm (权益回报率TTM), roa_ttm (资产回报率TTM), gross_income_ratio (销售毛利率)
            factors = [
                'operating_revenue_growth_rate',  # 营业收入增长率
                'net_profit_growth_rate',  # 净利润增长率
                'roe_ttm',  # ROE(TTM) 权益回报率TTM
                'roa_ttm',  # ROA(TTM) 资产回报率TTM
                'gross_income_ratio'  # 销售毛利率
            ]
            
            # 调用get_factor_values，注意参数名
            try:
                # 尝试使用date参数（单日期）
                factor_data = self.factor_engine.get_factor_values(
                    stocks=stocks[:50],  # 限制股票数量
                    factors=factors,
                    date=date
                )
            except TypeError:
                # 如果失败，尝试使用start_date和end_date
                factor_data = self.factor_engine._jq.get_factor_values(
                    securities=stocks[:50],
                    factors=factors,
                    start_date=date,
                    end_date=date
                )
                if factor_data is not None and not factor_data.empty:
                    # 转换为DataFrame格式
                    result = {}
                    for factor in factors:
                        if factor in factor_data.columns:
                            result[factor] = factor_data[factor].iloc[0] if len(factor_data) > 0 else pd.Series()
                    factor_data = pd.DataFrame(result).T if result else pd.DataFrame()
            
            if factor_data is not None and not factor_data.empty:
                # 计算行业平均指标（使用正确的因子名称）
                avg_revenue_growth = factor_data['operating_revenue_growth_rate'].mean() if 'operating_revenue_growth_rate' in factor_data.columns else 0
                avg_profit_growth = factor_data['net_profit_growth_rate'].mean() if 'net_profit_growth_rate' in factor_data.columns else 0
                avg_roe = factor_data['roe_ttm'].mean() if 'roe_ttm' in factor_data.columns else 0
                avg_roa = factor_data['roa_ttm'].mean() if 'roa_ttm' in factor_data.columns else 0
                avg_gross_margin = factor_data['gross_income_ratio'].mean() if 'gross_income_ratio' in factor_data.columns else 0
                
                # 计算得分（简化算法）
                revenue_score = min(100, max(0, 50 + avg_revenue_growth * 2))  # 营收增长每1%加2分
                profit_score = min(100, max(0, 50 + avg_profit_growth * 1.5))  # 利润增长每1%加1.5分
                roe_score = min(100, max(0, avg_roe * 2))  # ROE每1%加2分
                roa_score = min(100, max(0, avg_roa * 5))  # ROA每1%加5分
                margin_score = min(100, max(0, avg_gross_margin))  # 毛利率直接作为得分
                
                # 综合得分
                score = (
                    revenue_score * 0.25 +
                    profit_score * 0.25 +
                    roe_score * 0.20 +
                    roa_score * 0.15 +
                    margin_score * 0.15
                )
                
                details = {
                    'avg_revenue_growth': float(avg_revenue_growth),
                    'avg_profit_growth': float(avg_profit_growth),
                    'avg_roe': float(avg_roe),
                    'avg_roa': float(avg_roa),
                    'avg_gross_margin': float(avg_gross_margin),
                    'revenue_score': float(revenue_score),
                    'profit_score': float(profit_score),
                    'roe_score': float(roe_score),
                    'roa_score': float(roa_score),
                    'margin_score': float(margin_score)
                }
            
        except Exception as e:
            logger.warning(f"行业景气因子计算失败: {e}")
        
        return score, details
    
    def _calculate_technical_score(
        self,
        stocks: List[str],
        date: str
    ) -> Tuple[float, Dict]:
        """
        计算技术动量因子得分（0-100）
        
        使用Alpha191因子和聚宽因子库：
        - Alpha191因子（多个）
        - RSI、MACD等技术指标
        """
        score = 50.0  # 默认中性得分
        details = {}
        
        if not stocks:
            return score, details
        
        try:
            import jqdatasdk as jq
            # get_all_alpha_191在主模块中，不在alpha191子模块
            try:
                from jqdatasdk import get_all_alpha_191
            except ImportError:
                # 备用方案：直接从jq调用
                get_all_alpha_191 = jq.get_all_alpha_191
            
            # 限制股票数量以提高性能
            limited_stocks = stocks[:50]
            
            # 获取Alpha191因子（选择几个关键因子）
            alpha_factors = ['alpha_001', 'alpha_002', 'alpha_003', 'alpha_004', 'alpha_005']
            alpha_scores = []
            
            try:
                # 批量获取Alpha191因子
                # 注意：参数顺序是 date, code=None, alpha=None
                alpha_data = get_all_alpha_191(
                    date=date,
                    code=limited_stocks,
                    alpha=alpha_factors
                )
                
                if alpha_data is not None and not alpha_data.empty:
                    # 计算每个因子的平均得分
                    for alpha_name in alpha_factors:
                        if alpha_name in alpha_data.columns:
                            alpha_values = alpha_data[alpha_name].dropna()
                            if len(alpha_values) > 0:
                                avg_alpha = float(alpha_values.mean())
                                # Alpha值转换为得分（简化处理）
                                # Alpha值通常在-1到1之间，映射到0-100
                                alpha_score = min(100, max(0, 50 + avg_alpha * 50))
                                alpha_scores.append(alpha_score)
                                details[f'{alpha_name}_score'] = alpha_score
                                details[f'{alpha_name}_avg'] = avg_alpha
                    
                    # 计算平均Alpha得分
                    if alpha_scores:
                        score = np.mean(alpha_scores)
                        details['avg_alpha_score'] = float(score)
                        details['n_alpha_factors'] = len(alpha_scores)
            except Exception as e:
                logger.debug(f"获取Alpha191因子失败: {e}")
            
            # 获取技术指标（使用聚宽因子库）
            # 注意：聚宽因子库技术类中没有RSI，只有MACDC（平滑异同移动平均线）
            if self.factor_engine:
                try:
                    tech_factors = ['MACDC']  # 使用MACDC替代MACD
                    # 使用date参数而不是start_date和end_date
                    tech_data = self.factor_engine.get_factor_values(
                        stocks=limited_stocks,
                        factors=tech_factors,
                        date=date
                    )
                    
                    if tech_data is not None and not tech_data.empty:
                        # MACDC得分（MACDC>0为看涨，<0为看跌）
                        if 'MACDC' in tech_data.columns:
                            macdc_values = tech_data['MACDC'].dropna()
                            if len(macdc_values) > 0:
                                avg_macdc = float(macdc_values.mean())
                                # MACDC转换为得分：正数映射到50-100，负数映射到0-50
                                macdc_score = min(100, max(0, 50 + avg_macdc * 100))  # 简化映射
                                details['avg_macdc'] = avg_macdc
                                details['macdc_score'] = macdc_score
                                # 如果Alpha得分可用，则加权组合；否则直接使用MACDC得分
                                if alpha_scores:
                                    score = score * 0.7 + macdc_score * 0.3
                                else:
                                    score = macdc_score
                except Exception as e:
                    logger.debug(f"获取技术指标失败: {e}")
            
        except Exception as e:
            logger.warning(f"技术动量因子计算失败: {e}")
        
        return score, details
    
    def _calculate_sentiment_score(
        self,
        stocks: List[str],
        date: str
    ) -> Tuple[float, Dict]:
        """
        计算市场情绪因子得分（0-100）
        
        使用AKShare获取：
        - 新闻热度（简化处理）
        - 龙虎榜数据
        """
        score = 50.0  # 默认中性得分
        details = {}
        
        if not stocks or not self.akshare_client:
            return score, details
        
        try:
            # 获取龙虎榜数据（需要股票代码转换）
            # 这里简化处理，实际需要将JQData代码转换为AKShare格式
            # 龙虎榜数据可以反映市场关注度
            
            # 简化实现：使用默认得分
            # 实际应该：
            # 1. 获取龙虎榜上榜次数
            # 2. 获取新闻提及次数
            # 3. 获取搜索指数
            
            details['note'] = '情绪因子需要额外数据源支持'
            
        except Exception as e:
            logger.warning(f"市场情绪因子计算失败: {e}")
        
        return score, details
    
    def _empty_score_result(self) -> Dict[str, float]:
        """返回空得分结果"""
        return {
            'total_score': 0.0,
            'macro_score': 0.0,
            'capital_flow_score': 0.0,
            'industry_prosperity_score': 0.0,
            'technical_momentum_score': 0.0,
            'market_sentiment_score': 0.0,
            'factor_details': {},
            'weights_used': self.weights,
            'period': 'medium',
            'industry_code': '',
            'date': '',
            'n_stocks': 0
        }
    
    def batch_calculate_mainline_scores(
        self,
        industry_codes: List[str],
        date: str,
        period: str = 'medium'
    ) -> Dict[str, Dict[str, float]]:
        """
        批量计算多个行业的主线预测得分
        
        Args:
            industry_codes: 行业代码列表
            date: 日期
            period: 期限
        
        Returns:
            {行业代码: 得分结果}
        """
        results = {}
        
        for industry_code in industry_codes:
            try:
                score_result = self.calculate_mainline_score(
                    industry_code=industry_code,
                    date=date,
                    period=period
                )
                results[industry_code] = score_result
            except Exception as e:
                logger.error(f"计算行业{industry_code}得分失败: {e}")
                results[industry_code] = self._empty_score_result()
        
        return results

