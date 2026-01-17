#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
动态主线选股模块 V1.0
=====================

功能:
1. 五维主线识别（资金/热度/动量/政策/龙头）
2. 动态获取主线成分股
3. 加权融合主线股票与信号股票

数据源:
- 主源: JQData (聚宽正式账号)
- 辅助: AKShare (资金流向补充)

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

from __future__ import annotations

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

class MainlineSignal(Enum):
    """主线信号"""
    STRONG_BUY = "强买入"   # >= 75
    BUY = "买入"            # 65-75
    HOLD = "持有"           # 50-65
    WATCH = "观察"          # 35-50
    SELL = "卖出"           # < 35


@dataclass
class DimensionScore:
    """单维度评分"""
    name: str               # 维度名称
    score: float = 0.0      # 评分 (0-100)
    weight: float = 0.2     # 权重
    factors: Dict[str, float] = field(default_factory=dict)  # 因子明细
    remark: str = ""        # 备注
    
    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class MainlineResult:
    """主线识别结果"""
    name: str                           # 主线名称
    code: str = ""                      # 主线代码
    mainline_type: str = "industry"     # industry/concept
    
    # 五维评分
    funds_score: Optional[DimensionScore] = None     # 资金维度
    heat_score: Optional[DimensionScore] = None      # 热度维度
    momentum_score: Optional[DimensionScore] = None  # 动量维度
    policy_score: Optional[DimensionScore] = None    # 政策维度
    leader_score: Optional[DimensionScore] = None    # 龙头维度
    
    # 综合评分
    total_score: float = 0.0
    rank: int = 0
    signal: MainlineSignal = MainlineSignal.WATCH
    
    # 成分股
    stocks: List[str] = field(default_factory=list)
    
    # 原始数据
    change_pct: float = 0.0     # 涨跌幅
    net_inflow: float = 0.0     # 净流入
    leader_stock: str = ""      # 龙头股
    leader_change: float = 0.0  # 龙头涨幅
    
    def get_signal(self) -> MainlineSignal:
        """根据得分获取信号"""
        if self.total_score >= 75:
            return MainlineSignal.STRONG_BUY
        elif self.total_score >= 65:
            return MainlineSignal.BUY
        elif self.total_score >= 50:
            return MainlineSignal.HOLD
        elif self.total_score >= 35:
            return MainlineSignal.WATCH
        else:
            return MainlineSignal.SELL
    
    def is_investable(self) -> bool:
        """是否可投资"""
        return self.signal in [MainlineSignal.STRONG_BUY, MainlineSignal.BUY, MainlineSignal.HOLD]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "code": self.code,
            "type": self.mainline_type,
            "total_score": self.total_score,
            "signal": self.signal.value,
            "rank": self.rank,
            "change_pct": self.change_pct,
            "net_inflow": self.net_inflow,
            "stocks_count": len(self.stocks),
            "leader_stock": self.leader_stock,
            "dimensions": {
                "funds": self.funds_score.score if self.funds_score else 0,
                "heat": self.heat_score.score if self.heat_score else 0,
                "momentum": self.momentum_score.score if self.momentum_score else 0,
                "policy": self.policy_score.score if self.policy_score else 0,
                "leader": self.leader_score.score if self.leader_score else 0,
            }
        }


@dataclass
class SelectorConfig:
    """选股器配置"""
    # 主线参数
    top_n_mainlines: int = 5              # 关注前N个主线
    min_mainline_score: float = 50.0      # 最低主线得分
    
    # 权重配置
    mainline_weight: float = 0.7          # 主线股票权重
    signal_weight: float = 0.3            # 信号股票权重
    
    # 五维权重 (总和=1.0)
    funds_weight: float = 0.30            # 资金维度权重
    heat_weight: float = 0.20             # 热度维度权重
    momentum_weight: float = 0.20         # 动量维度权重
    policy_weight: float = 0.15           # 政策维度权重
    leader_weight: float = 0.15           # 龙头维度权重
    
    # 数据源
    use_jqdata: bool = True               # 使用JQData
    use_akshare: bool = True              # 使用AKShare补充


# ============== 动态主线选股器 ==============

class DynamicMainlineSelector:
    """
    动态主线选股器
    
    核心功能:
    1. 五维主线识别（资金/热度/动量/政策/龙头）
    2. 动态获取主线成分股
    3. 加权融合主线股票与信号股票
    
    数据源优先级:
    1. JQData (正式账号，行业/概念成分股)
    2. AKShare (资金流向、龙虎榜补充)
    """
    
    def __init__(self, config: Optional[SelectorConfig] = None):
        """
        初始化选股器
        
        Args:
            config: 选股器配置
        """
        self.config = config if config else SelectorConfig()
        self.jq = None
        self._ensure_jqdata()
        self._cache: Dict[str, Any] = {}
        self._cache_time: Dict[str, datetime] = {}
        logger.info("DynamicMainlineSelector 初始化完成")
        logger.info(f"  - 主线权重: {self.config.mainline_weight:.0%}")
        logger.info(f"  - 信号权重: {self.config.signal_weight:.0%}")
        logger.info(f"  - TopN主线: {self.config.top_n_mainlines}")
    
    def _ensure_jqdata(self):
        """确保JQData已认证"""
        if self.jq is None:
            try:
                import jqdatasdk as jq
                with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self.jq = jq
                logger.info("JQData认证成功")
            except Exception as e:
                logger.error(f"JQData认证失败: {e}")
                self.jq = None
    
    def identify_mainlines(self, as_of_date: str) -> List[MainlineResult]:
        """
        识别当前市场主线
        
        使用五维评分系统:
        1. 资金维度 (30%): 主力净流入、北向资金
        2. 热度维度 (20%): 涨跌幅强度、涨停板
        3. 动量维度 (20%): 价格动量、相对强度
        4. 政策维度 (15%): 政策关联度
        5. 龙头维度 (15%): 龙头涨幅、连板高度
        
        Args:
            as_of_date: 日期 (YYYY-MM-DD)
        
        Returns:
            主线结果列表（按总分降序）
        """
        logger.info(f"开始识别市场主线: {as_of_date}")
        
        # 检查缓存
        cache_key = f"mainlines_{as_of_date}"
        if cache_key in self._cache:
            cache_age = (datetime.now() - self._cache_time.get(cache_key, datetime.min)).seconds
            if cache_age < 1800:  # 30分钟缓存
                logger.info("使用缓存的主线数据")
                return self._cache[cache_key]
        
        mainlines = []
        
        # 1. 获取行业板块数据（使用JQData）
        industry_results = self._analyze_industries(as_of_date)
        mainlines.extend(industry_results)
        
        # 2. 获取概念板块数据（使用JQData）
        concept_results = self._analyze_concepts(as_of_date)
        mainlines.extend(concept_results)
        
        # 3. 排序并计算排名
        mainlines.sort(key=lambda x: x.total_score, reverse=True)
        for i, ml in enumerate(mainlines):
            ml.rank = i + 1
            ml.signal = ml.get_signal()
        
        # 4. 更新缓存
        self._cache[cache_key] = mainlines
        self._cache_time[cache_key] = datetime.now()
        
        logger.info(f"主线识别完成: 共{len(mainlines)}条，Top3: "
                   f"{', '.join([f'{ml.name}({ml.total_score:.1f})' for ml in mainlines[:3]])}")
        
        return mainlines
    
    def _analyze_industries(self, as_of_date: str) -> List[MainlineResult]:
        """分析行业板块"""
        results = []
        
        if self.jq is None:
            logger.warning("JQData未初始化，跳过行业分析")
            return results
        
        try:
            # 获取申万一级行业列表
            industries = self.jq.get_industries(name='sw_l1')
            
            if industries is None or industries.empty:
                logger.warning("无法获取行业列表")
                return results
            
            logger.info(f"获取到 {len(industries)} 个行业")
            
            # 分析每个行业
            for idx, row in industries.iterrows():
                industry_code = idx
                industry_name = row.get('name', str(idx))
                
                try:
                    # 获取行业成分股
                    stocks = self.jq.get_industry_stocks(industry_code, date=as_of_date)
                    
                    if not stocks:
                        continue
                    
                    # 计算行业指标
                    metrics = self._calculate_industry_metrics(stocks, as_of_date)
                    
                    # 计算五维评分
                    mainline = self._calculate_five_dim_score(
                        name=industry_name,
                        code=industry_code,
                        mainline_type="industry",
                        stocks=stocks,
                        metrics=metrics,
                    )
                    
                    results.append(mainline)
                    
                except Exception as e:
                    logger.debug(f"分析行业 {industry_name} 失败: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"行业分析失败: {e}")
        
        return results
    
    def _analyze_concepts(self, as_of_date: str) -> List[MainlineResult]:
        """分析概念板块"""
        results = []
        
        if self.jq is None:
            logger.warning("JQData未初始化，跳过概念分析")
            return results
        
        try:
            # 获取概念列表
            concepts = self.jq.get_concepts()
            
            if concepts is None or concepts.empty:
                logger.warning("无法获取概念列表")
                return results
            
            logger.info(f"获取到 {len(concepts)} 个概念")
            
            # 限制分析数量（概念太多会很慢）
            max_concepts = 50
            concepts_to_analyze = concepts.head(max_concepts)
            
            for idx, row in concepts_to_analyze.iterrows():
                concept_code = idx
                concept_name = row.get('name', str(idx))
                
                try:
                    # 获取概念成分股
                    stocks = self.jq.get_concept_stocks(concept_code, date=as_of_date)
                    
                    if not stocks or len(stocks) < 5:  # 至少5只股票
                        continue
                    
                    # 计算概念指标
                    metrics = self._calculate_industry_metrics(stocks[:50], as_of_date)  # 限制股票数
                    
                    # 计算五维评分
                    mainline = self._calculate_five_dim_score(
                        name=concept_name,
                        code=concept_code,
                        mainline_type="concept",
                        stocks=stocks,
                        metrics=metrics,
                    )
                    
                    results.append(mainline)
                    
                except Exception as e:
                    logger.debug(f"分析概念 {concept_name} 失败: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"概念分析失败: {e}")
        
        return results
    
    def _calculate_industry_metrics(
        self,
        stocks: List[str],
        as_of_date: str,
    ) -> Dict[str, float]:
        """
        计算行业/概念的核心指标
        
        使用JQData获取:
        - 价格数据 (用于计算动量、涨跌幅)
        - 成交量数据 (用于计算量比)
        """
        metrics = {
            "avg_change_pct": 0.0,       # 平均涨跌幅
            "up_ratio": 0.0,             # 上涨股票比例
            "limit_up_count": 0,         # 涨停数
            "momentum_5d": 0.0,          # 5日动量
            "momentum_20d": 0.0,         # 20日动量
            "vol_ratio_avg": 0.0,        # 平均量比
            "leader_change": 0.0,        # 龙头涨幅
            "leader_stock": "",          # 龙头股
        }
        
        if self.jq is None or not stocks:
            return metrics
        
        try:
            # 计算日期范围
            end_date = as_of_date
            start_date_5d = (datetime.strptime(as_of_date, "%Y-%m-%d") - timedelta(days=10)).strftime("%Y-%m-%d")
            start_date_20d = (datetime.strptime(as_of_date, "%Y-%m-%d") - timedelta(days=40)).strftime("%Y-%m-%d")
            
            # 获取价格数据（限制股票数量提高速度）
            sample_stocks = stocks[:30] if len(stocks) > 30 else stocks
            
            df = self.jq.get_price(
                sample_stocks,
                start_date=start_date_20d,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                panel=False,
                skip_paused=True,
            )
            
            if df is None or df.empty:
                return metrics
            
            # 按股票分组计算
            changes = []
            momentums_5d = []
            momentums_20d = []
            vol_ratios = []
            
            for stock in sample_stocks:
                stock_df = df[df['code'] == stock] if 'code' in df.columns else df
                
                if len(stock_df) < 5:
                    continue
                
                # 当日涨跌幅
                if len(stock_df) >= 2:
                    daily_change = (stock_df['close'].iloc[-1] / stock_df['close'].iloc[-2] - 1) * 100
                    changes.append(daily_change)
                    
                    # 涨停判断 (>9.5%)
                    if daily_change > 9.5:
                        metrics["limit_up_count"] += 1
                
                # 5日动量
                if len(stock_df) >= 6:
                    mom_5d = (stock_df['close'].iloc[-1] / stock_df['close'].iloc[-6] - 1) * 100
                    momentums_5d.append(mom_5d)
                
                # 20日动量
                if len(stock_df) >= 21:
                    mom_20d = (stock_df['close'].iloc[-1] / stock_df['close'].iloc[-21] - 1) * 100
                    momentums_20d.append(mom_20d)
                
                # 量比
                if len(stock_df) >= 10:
                    vol_5d = stock_df['volume'].iloc[-5:].mean()
                    vol_20d = stock_df['volume'].iloc[-20:].mean()
                    if vol_20d > 0:
                        vol_ratios.append(vol_5d / vol_20d)
            
            # 计算汇总指标
            if changes:
                metrics["avg_change_pct"] = np.mean(changes)
                metrics["up_ratio"] = sum(1 for c in changes if c > 0) / len(changes) * 100
                
                # 龙头股
                max_idx = np.argmax(changes)
                metrics["leader_change"] = changes[max_idx]
                metrics["leader_stock"] = sample_stocks[max_idx] if max_idx < len(sample_stocks) else ""
            
            if momentums_5d:
                metrics["momentum_5d"] = np.mean(momentums_5d)
            
            if momentums_20d:
                metrics["momentum_20d"] = np.mean(momentums_20d)
            
            if vol_ratios:
                metrics["vol_ratio_avg"] = np.mean(vol_ratios)
            
        except Exception as e:
            logger.warning(f"计算行业指标失败: {e}")
        
        return metrics
    
    def _calculate_five_dim_score(
        self,
        name: str,
        code: str,
        mainline_type: str,
        stocks: List[str],
        metrics: Dict[str, float],
    ) -> MainlineResult:
        """
        计算五维评分
        
        五维权重:
        - 资金维度 (30%): 基于量比、资金流向
        - 热度维度 (20%): 基于涨跌幅、涨停数
        - 动量维度 (20%): 基于5日/20日动量
        - 政策维度 (15%): 基于概念类型（暂用固定值）
        - 龙头维度 (15%): 基于龙头涨幅
        """
        result = MainlineResult(
            name=name,
            code=code,
            mainline_type=mainline_type,
            stocks=stocks[:100],  # 只保留前100只
            change_pct=metrics.get("avg_change_pct", 0),
            leader_stock=metrics.get("leader_stock", ""),
            leader_change=metrics.get("leader_change", 0),
        )
        
        # 1. 资金维度 (30%)
        vol_ratio = metrics.get("vol_ratio_avg", 1.0)
        funds_raw = min(100, max(0, 50 + (vol_ratio - 1) * 30))  # 量比>1加分
        result.funds_score = DimensionScore(
            name="资金维度",
            score=funds_raw,
            weight=self.config.funds_weight,
            factors={"vol_ratio": vol_ratio},
        )
        
        # 2. 热度维度 (20%)
        avg_change = metrics.get("avg_change_pct", 0)
        up_ratio = metrics.get("up_ratio", 50)
        limit_up = metrics.get("limit_up_count", 0)
        heat_raw = min(100, max(0, 
            40 + avg_change * 5 +     # 涨幅加分
            (up_ratio - 50) * 0.5 +   # 上涨比例加分
            limit_up * 5              # 涨停加分
        ))
        result.heat_score = DimensionScore(
            name="热度维度",
            score=heat_raw,
            weight=self.config.heat_weight,
            factors={"avg_change": avg_change, "up_ratio": up_ratio, "limit_up": limit_up},
        )
        
        # 3. 动量维度 (20%)
        mom_5d = metrics.get("momentum_5d", 0)
        mom_20d = metrics.get("momentum_20d", 0)
        momentum_raw = min(100, max(0, 50 + mom_5d * 2 + mom_20d * 0.5))
        result.momentum_score = DimensionScore(
            name="动量维度",
            score=momentum_raw,
            weight=self.config.momentum_weight,
            factors={"momentum_5d": mom_5d, "momentum_20d": mom_20d},
        )
        
        # 4. 政策维度 (15%) - 基于概念类型给予基础分
        policy_raw = 50  # 默认中性
        if mainline_type == "concept":
            # AI/新能源/半导体等热门概念加分
            hot_keywords = ["人工智能", "AI", "芯片", "半导体", "新能源", "光伏", "储能", "机器人"]
            for kw in hot_keywords:
                if kw in name:
                    policy_raw = 70
                    break
        result.policy_score = DimensionScore(
            name="政策维度",
            score=policy_raw,
            weight=self.config.policy_weight,
            factors={"type": mainline_type},
        )
        
        # 5. 龙头维度 (15%)
        leader_change = metrics.get("leader_change", 0)
        leader_raw = min(100, max(0, 50 + leader_change * 3))
        if leader_change > 9.5:  # 龙头涨停
            leader_raw = min(100, leader_raw + 20)
        result.leader_score = DimensionScore(
            name="龙头维度",
            score=leader_raw,
            weight=self.config.leader_weight,
            factors={"leader_change": leader_change},
        )
        
        # 计算总分
        result.total_score = (
            result.funds_score.weighted_score +
            result.heat_score.weighted_score +
            result.momentum_score.weighted_score +
            result.policy_score.weighted_score +
            result.leader_score.weighted_score
        )
        
        return result
    
    def get_mainline_stocks(
        self,
        as_of_date: str,
        top_n: Optional[int] = None,
    ) -> Tuple[Dict[str, List[str]], List[MainlineResult]]:
        """
        获取主线成分股
        
        Args:
            as_of_date: 日期
            top_n: 返回前N个主线，默认使用配置
        
        Returns:
            (主线股票字典, 主线结果列表)
            - 主线股票字典: {mainline_name: [stocks]}
            - 主线结果列表: 用于显示详情
        """
        if top_n is None:
            top_n = self.config.top_n_mainlines
        
        # 识别主线
        mainlines = self.identify_mainlines(as_of_date)
        
        # 筛选可投资主线
        investable = [ml for ml in mainlines if ml.is_investable()]
        top_mainlines = investable[:top_n]
        
        # 构建股票字典
        stocks_dict = {}
        for ml in top_mainlines:
            stocks_dict[ml.name] = ml.stocks
        
        logger.info(f"获取主线成分股: {len(top_mainlines)}条主线，共{sum(len(s) for s in stocks_dict.values())}只股票")
        
        return stocks_dict, top_mainlines
    
    def build_weighted_targets(
        self,
        mainline_stocks: Dict[str, List[str]],
        signal_stocks: List[str],
        max_stocks: int = 100,
    ) -> List[Tuple[str, float, str]]:
        """
        构建加权标的池
        
        融合主线股票与信号股票:
        - 主线股票权重: 0.7 (默认)
        - 信号股票权重: 0.3 (默认)
        
        Args:
            mainline_stocks: 主线股票字典 {mainline_name: [stocks]}
            signal_stocks: 信号股票列表
            max_stocks: 最大返回数量
        
        Returns:
            [(stock_code, weight, source), ...]
            - stock_code: 股票代码
            - weight: 权重 (0-1)
            - source: 来源 (mainline/signal/both)
        """
        stock_scores: Dict[str, Dict] = {}
        
        # 1. 处理主线股票
        mainline_weight = self.config.mainline_weight
        for mainline_name, stocks in mainline_stocks.items():
            for i, stock in enumerate(stocks):
                if stock not in stock_scores:
                    stock_scores[stock] = {"weight": 0.0, "sources": []}
                
                # 主线内排名靠前的股票权重更高
                rank_factor = max(0.5, 1 - i / len(stocks) * 0.5) if stocks else 1
                stock_scores[stock]["weight"] += mainline_weight * rank_factor
                stock_scores[stock]["sources"].append(f"主线:{mainline_name}")
        
        # 2. 处理信号股票
        signal_weight = self.config.signal_weight
        for i, stock in enumerate(signal_stocks):
            if stock not in stock_scores:
                stock_scores[stock] = {"weight": 0.0, "sources": []}
            
            rank_factor = max(0.5, 1 - i / len(signal_stocks) * 0.5) if signal_stocks else 1
            stock_scores[stock]["weight"] += signal_weight * rank_factor
            stock_scores[stock]["sources"].append("信号")
        
        # 3. 归一化并排序
        results = []
        for stock, info in stock_scores.items():
            source = "both" if len(set(info["sources"])) > 1 else (
                "mainline" if "主线" in info["sources"][0] else "signal"
            )
            results.append((stock, info["weight"], source))
        
        # 按权重降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 限制数量
        results = results[:max_stocks]
        
        logger.info(f"加权标的池构建完成: {len(results)}只股票")
        logger.info(f"  - 纯主线: {sum(1 for r in results if r[2] == 'mainline')}")
        logger.info(f"  - 纯信号: {sum(1 for r in results if r[2] == 'signal')}")
        logger.info(f"  - 两者兼有: {sum(1 for r in results if r[2] == 'both')}")
        
        return results
    
    def get_summary(self, mainlines: List[MainlineResult]) -> str:
        """生成主线摘要"""
        lines = [
            "=" * 60,
            "市场主线分析报告",
            "=" * 60,
            f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"主线数量: {len(mainlines)}",
            "",
            "【Top 10 主线】",
        ]
        
        for ml in mainlines[:10]:
            lines.append(
                f"  {ml.rank}. {ml.name} ({ml.mainline_type}): "
                f"得分={ml.total_score:.1f}, 信号={ml.signal.value}, "
                f"涨幅={ml.change_pct:.2f}%, 龙头={ml.leader_stock}"
            )
        
        lines.append("")
        lines.append("【五维评分明细 (Top 3)】")
        
        for ml in mainlines[:3]:
            lines.append(f"\n  >> {ml.name}")
            lines.append(f"     资金={ml.funds_score.score:.1f} x {ml.funds_score.weight:.0%}")
            lines.append(f"     热度={ml.heat_score.score:.1f} x {ml.heat_score.weight:.0%}")
            lines.append(f"     动量={ml.momentum_score.score:.1f} x {ml.momentum_score.weight:.0%}")
            lines.append(f"     政策={ml.policy_score.score:.1f} x {ml.policy_score.weight:.0%}")
            lines.append(f"     龙头={ml.leader_score.score:.1f} x {ml.leader_score.weight:.0%}")
        
        return "\n".join(lines)


# ============== 测试函数 ==============

def test_dynamic_mainline_selector():
    """测试动态主线选股器"""
    print("=" * 60)
    print("测试: DynamicMainlineSelector")
    print("=" * 60)
    
    # 初始化选股器
    selector = DynamicMainlineSelector()
    
    # 测试日期
    test_date = "2024-09-25"  # 2024政策牛期间
    
    # 1. 识别主线
    print(f"\n1. 识别市场主线 ({test_date})...")
    mainlines = selector.identify_mainlines(test_date)
    print(f"   识别到 {len(mainlines)} 条主线")
    
    # 2. 获取主线成分股
    print("\n2. 获取Top5主线成分股...")
    stocks_dict, top_mainlines = selector.get_mainline_stocks(test_date, top_n=5)
    for name, stocks in stocks_dict.items():
        print(f"   - {name}: {len(stocks)}只股票")
    
    # 3. 构建加权标的池
    print("\n3. 构建加权标的池...")
    # 模拟信号股票
    signal_stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG"]
    all_mainline_stocks = []
    for stocks in stocks_dict.values():
        all_mainline_stocks.extend(stocks[:20])
    
    weighted = selector.build_weighted_targets(stocks_dict, signal_stocks, max_stocks=50)
    print(f"   加权标的: {len(weighted)}只")
    for stock, weight, source in weighted[:10]:
        print(f"   - {stock}: 权重={weight:.3f}, 来源={source}")
    
    # 4. 打印摘要
    print("\n4. 主线摘要:")
    print(selector.get_summary(mainlines))
    
    print("\n✅ 测试完成!")
    return mainlines, stocks_dict, weighted


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    test_dynamic_mainline_selector()
