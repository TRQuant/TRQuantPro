# -*- coding: utf-8 -*-
"""
投资标的构建器 V6.0
====================

功能:
1. 早期筛选池构建（基础过滤 + 主题过滤）
2. 动态主线筛选（五维主线识别 + 成分股）【V6新增】
3. 信号筛选（因子计算 + 信号生成 + 评分排序）
4. 最终标的输出

两阶段筛选流程:
Stage 1: 全A股 -> 基础过滤 -> 主题过滤/主线筛选 -> 初筛池
Stage 2: 初筛池 -> 因子计算 -> 信号生成 -> 目标标的

V6.0更新:
- 新增动态主线选股模式
- 支持五维主线识别
- 主线股票与信号股票加权融合

作者: TRQuant Team
版本: V6.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class FilterConfig:
    """筛选配置"""
    # 市值筛选（亿元）
    min_market_cap: float = 50.0
    max_market_cap: float = 500.0
    
    # 流动性筛选（万元）
    min_daily_amount: float = 5000.0
    
    # 排除条件
    exclude_st: bool = True
    exclude_new_days: int = 60  # 排除上市不足60天
    exclude_kcb: bool = True    # 排除科创板
    exclude_bj: bool = True     # 排除北交所
    exclude_suspended: bool = True  # 排除停牌
    
    # 主题筛选
    include_hot_themes: bool = True
    min_theme_score: float = 0.0  # 最低题材得分
    
    # 动态主线选股 (V6新增)
    use_dynamic_mainline: bool = True      # 启用动态主线选股
    mainline_weight: float = 0.7           # 主线股票权重
    signal_weight: float = 0.3             # 信号股票权重
    top_n_mainlines: int = 5               # 关注前N个主线
    min_mainline_score: float = 50.0       # 最低主线得分


@dataclass 
class TargetStock:
    """目标标的"""
    code: str
    name: str = ""
    signal_score: float = 0.0
    theme_score: float = 0.0
    signal_type: str = ""
    industry: str = ""
    market_cap: float = 0.0
    
    # 因子值
    mom_20d: float = 0.0
    vol_ratio: float = 0.0
    is_first_limit_up: bool = False
    
    # 建议
    suggested_position: float = 0.0
    entry_reason: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "signal_score": self.signal_score,
            "theme_score": self.theme_score,
            "signal_type": self.signal_type,
            "industry": self.industry,
            "market_cap": self.market_cap,
            "mom_20d": self.mom_20d,
            "vol_ratio": self.vol_ratio,
            "is_first_limit_up": self.is_first_limit_up,
            "suggested_position": self.suggested_position,
            "entry_reason": self.entry_reason,
        }


@dataclass
class BuilderResult:
    """构建结果"""
    # 阶段结果
    stage1_count: int = 0   # 早期筛选池数量
    stage2_count: int = 0   # 最终标的数量
    
    # 标的列表
    preliminary_pool: List[str] = field(default_factory=list)
    final_targets: List[TargetStock] = field(default_factory=list)
    
    # 统计信息
    total_stocks_scanned: int = 0
    filter_stats: Dict[str, int] = field(default_factory=dict)
    build_date: str = ""
    
    def summary(self) -> str:
        """生成摘要"""
        lines = [
            f"投资标的构建报告 - {self.build_date}",
            "=" * 50,
            f"扫描股票总数: {self.total_stocks_scanned}",
            f"Stage 1 初筛池: {self.stage1_count}",
            f"Stage 2 最终标的: {self.stage2_count}",
            "",
            "筛选统计:",
        ]
        
        for key, value in self.filter_stats.items():
            lines.append(f"  - {key}: {value}")
        
        if self.final_targets:
            lines.append("")
            lines.append("最终标的:")
            for i, target in enumerate(self.final_targets[:10], 1):
                lines.append(f"  {i}. {target.code} {target.name}: "
                           f"信号分={target.signal_score:.1f}, "
                           f"类型={target.signal_type}")
        
        return "\n".join(lines)


class InvestmentTargetBuilder:
    """
    投资标的构建器 V6.0
    
    两阶段筛选:
    1. 早期筛选: 基础条件 + 主题匹配/动态主线
    2. 信号筛选: 因子计算 + 信号生成
    
    V6新增:
    - 动态主线选股模式
    - 五维主线识别
    - 主线股票与信号股票加权融合
    """
    
    def __init__(
        self,
        filter_config: Optional[FilterConfig] = None,
        theme_identifier=None,
        mainline_selector=None,
    ):
        """
        初始化构建器
        
        Args:
            filter_config: 筛选配置
            theme_identifier: 题材识别器（ThemeSectorIdentifier实例）
            mainline_selector: 动态主线选股器（DynamicMainlineSelector实例）【V6新增】
        """
        self.config = filter_config or FilterConfig()
        self.theme_identifier = theme_identifier
        self.mainline_selector = mainline_selector
        
        # 尝试初始化题材识别器
        if self.theme_identifier is None:
            try:
                from .theme_sector_identifier import ThemeSectorIdentifier
                self.theme_identifier = ThemeSectorIdentifier()
            except Exception as e:
                logger.warning(f"题材识别器初始化失败: {e}")
        
        # V6: 尝试初始化动态主线选股器
        if self.mainline_selector is None and self.config.use_dynamic_mainline:
            try:
                from .dynamic_mainline_selector import DynamicMainlineSelector, SelectorConfig
                selector_config = SelectorConfig(
                    top_n_mainlines=self.config.top_n_mainlines,
                    mainline_weight=self.config.mainline_weight,
                    signal_weight=self.config.signal_weight,
                    min_mainline_score=self.config.min_mainline_score,
                )
                self.mainline_selector = DynamicMainlineSelector(config=selector_config)
                logger.info("动态主线选股器初始化成功")
            except Exception as e:
                logger.warning(f"动态主线选股器初始化失败: {e}")
                self.mainline_selector = None
        
        logger.info("InvestmentTargetBuilder V6.0 初始化完成")
        logger.info(f"  - 动态主线模式: {'启用' if self.config.use_dynamic_mainline and self.mainline_selector else '禁用'}")
    
    def build_stage1_pool(
        self,
        all_stocks: List[str],
        stock_info: pd.DataFrame,
        as_of_date: str,
    ) -> Tuple[List[str], Dict[str, int]]:
        """
        Stage 1: 构建早期筛选池
        
        V6更新: 支持动态主线选股模式
        - 动态主线模式: 基于五维主线识别筛选股票
        - 传统模式: 基于主题识别筛选股票
        
        Args:
            all_stocks: 全部股票列表
            stock_info: 股票基本信息（需包含market_cap, industry, name等）
            as_of_date: 日期
        
        Returns:
            (初筛池股票列表, 筛选统计)
        """
        stats = {
            "input": len(all_stocks),
            "after_basic": 0,
            "after_market_cap": 0,
            "after_liquidity": 0,
            "after_theme": 0,
            "after_mainline": 0,       # V6新增
            "mainline_stocks": 0,      # V6新增
            "mode": "dynamic_mainline" if (self.config.use_dynamic_mainline and self.mainline_selector) else "theme",
        }
        
        # V6: 动态主线模式
        if self.config.use_dynamic_mainline and self.mainline_selector:
            return self._build_stage1_with_mainline(all_stocks, stock_info, as_of_date, stats)
        
        # 传统主题模式
        return self._build_stage1_with_theme(all_stocks, stock_info, as_of_date, stats)
    
    def _build_stage1_with_mainline(
        self,
        all_stocks: List[str],
        stock_info: pd.DataFrame,
        as_of_date: str,
        stats: Dict[str, int],
    ) -> Tuple[List[str], Dict[str, int]]:
        """
        V6新增: 使用动态主线选股构建Stage 1
        """
        logger.info("Stage 1: 使用动态主线选股模式")
        
        pool = set()
        
        # 1. 基础过滤
        basic_filtered = []
        for stock in all_stocks:
            if self._pass_basic_filter(stock, stock_info):
                basic_filtered.append(stock)
        stats["after_basic"] = len(basic_filtered)
        
        # 2. 市值过滤
        cap_filtered = []
        for stock in basic_filtered:
            if self._pass_market_cap_filter(stock, stock_info):
                cap_filtered.append(stock)
        stats["after_market_cap"] = len(cap_filtered)
        stats["after_liquidity"] = len(cap_filtered)
        
        # 3. 动态主线筛选
        try:
            mainline_stocks_dict, mainlines = self.mainline_selector.get_mainline_stocks(
                as_of_date, 
                top_n=self.config.top_n_mainlines
            )
            
            # 收集主线成分股
            mainline_stock_set = set()
            for stocks in mainline_stocks_dict.values():
                mainline_stock_set.update(stocks)
            
            stats["mainline_stocks"] = len(mainline_stock_set)
            
            # 与基础筛选池取交集
            mainline_filtered = [s for s in cap_filtered if s in mainline_stock_set]
            stats["after_mainline"] = len(mainline_filtered)
            
            # 主线股票加入池
            pool.update(mainline_filtered)
            
            logger.info(f"主线筛选: {len(mainline_filtered)} 只股票来自主线")
            
        except Exception as e:
            logger.warning(f"动态主线筛选失败: {e}，回退到传统模式")
            stats["after_mainline"] = 0
        
        # 4. 补充非主线但有主题得分的股票
        if self.theme_identifier and self.config.include_hot_themes:
            theme_candidates = []
            for stock in cap_filtered:
                if stock in pool:
                    continue
                
                name = stock_info.loc[stock, "name"] if stock in stock_info.index else ""
                industry = stock_info.loc[stock, "industry"] if stock in stock_info.index else ""
                
                try:
                    profile = self.theme_identifier.identify_stock_themes(stock, name, industry)
                    if profile.total_theme_score >= self.config.min_theme_score:
                        theme_candidates.append((stock, profile.total_theme_score))
                except:
                    pass
            
            # 按主题得分排序，取前N只
            theme_candidates.sort(key=lambda x: x[1], reverse=True)
            for stock, _ in theme_candidates[:100]:  # 最多补充100只
                pool.add(stock)
        
        stats["after_theme"] = len(pool)
        
        logger.info(f"Stage 1 完成 (动态主线模式): {len(pool)}/{len(all_stocks)} 股票通过筛选")
        
        return list(pool), stats
    
    def _build_stage1_with_theme(
        self,
        all_stocks: List[str],
        stock_info: pd.DataFrame,
        as_of_date: str,
        stats: Dict[str, int],
    ) -> Tuple[List[str], Dict[str, int]]:
        """
        传统主题模式构建Stage 1
        """
        logger.info("Stage 1: 使用传统主题选股模式")
        
        pool = []
        
        for stock in all_stocks:
            # 基础过滤
            if not self._pass_basic_filter(stock, stock_info):
                continue
            
            stats["after_basic"] += 1
            
            # 市值过滤
            if not self._pass_market_cap_filter(stock, stock_info):
                continue
            
            stats["after_market_cap"] += 1
            
            # 流动性过滤（如果有数据）
            # 暂时跳过，需要额外数据
            stats["after_liquidity"] += 1
            
            # 主题过滤
            if self.config.include_hot_themes and self.theme_identifier:
                name = stock_info.loc[stock, "name"] if stock in stock_info.index else ""
                industry = stock_info.loc[stock, "industry"] if stock in stock_info.index else ""
                
                try:
                    profile = self.theme_identifier.identify_stock_themes(stock, name, industry)
                    
                    if profile.total_theme_score >= self.config.min_theme_score:
                        stats["after_theme"] += 1
                        pool.append(stock)
                except:
                    stats["after_theme"] += 1
                    pool.append(stock)
            else:
                stats["after_theme"] += 1
                pool.append(stock)
        
        logger.info(f"Stage 1 完成 (传统模式): {len(pool)}/{len(all_stocks)} 股票通过筛选")
        
        return pool, stats
    
    def _pass_basic_filter(self, stock: str, stock_info: pd.DataFrame) -> bool:
        """基础过滤"""
        # 排除ST
        if self.config.exclude_st:
            if stock in stock_info.index:
                name = str(stock_info.loc[stock].get("name", ""))
                if "ST" in name or "*ST" in name:
                    return False
        
        # 排除科创板
        if self.config.exclude_kcb and stock.startswith("688"):
            return False
        
        # 排除北交所
        if self.config.exclude_bj and (stock.startswith("8") or stock.startswith("4")):
            return False
        
        return True
    
    def _pass_market_cap_filter(self, stock: str, stock_info: pd.DataFrame) -> bool:
        """市值过滤"""
        if stock not in stock_info.index:
            return True  # 无数据时通过
        
        market_cap = stock_info.loc[stock].get("market_cap", 0)
        
        if market_cap <= 0:
            return True  # 无数据时通过
        
        # 转换为亿元
        if market_cap > 1e9:  # 假设是元
            market_cap = market_cap / 1e8
        
        return self.config.min_market_cap <= market_cap <= self.config.max_market_cap
    
    def build_stage2_targets(
        self,
        preliminary_pool: List[str],
        signals: pd.DataFrame,
        scores: pd.DataFrame,
        factors: Dict[str, pd.DataFrame],
        stock_info: pd.DataFrame,
        as_of_date: str,
        max_targets: int = 8,
    ) -> List[TargetStock]:
        """
        Stage 2: 构建最终标的
        
        Args:
            preliminary_pool: 初筛池
            signals: 信号矩阵
            scores: 评分矩阵
            factors: 因子字典
            stock_info: 股票信息
            as_of_date: 日期
            max_targets: 最大标的数
        
        Returns:
            最终标的列表
        """
        targets = []
        
        # 获取当日信号
        if as_of_date not in signals.index:
            logger.warning(f"日期 {as_of_date} 无信号数据")
            return targets
        
        day_signals = signals.loc[as_of_date]
        day_scores = scores.loc[as_of_date] if as_of_date in scores.index else pd.Series()
        
        # 筛选有信号的股票
        signal_stocks = day_signals[day_signals > 0].index.tolist()
        signal_stocks = [s for s in signal_stocks if s in preliminary_pool]
        
        if not signal_stocks:
            logger.info(f"日期 {as_of_date} 初筛池中无信号股票")
            return targets
        
        # 按评分排序
        stock_scores = [(s, day_scores.get(s, 0)) for s in signal_stocks]
        stock_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 取Top N
        for stock, score in stock_scores[:max_targets]:
            target = TargetStock(code=stock, signal_score=score)
            
            # 填充信息
            if stock in stock_info.index:
                target.name = str(stock_info.loc[stock].get("name", ""))
                target.industry = str(stock_info.loc[stock].get("industry", ""))
                target.market_cap = float(stock_info.loc[stock].get("market_cap", 0))
            
            # 填充因子值
            if "mom_20d" in factors and as_of_date in factors["mom_20d"].index:
                target.mom_20d = factors["mom_20d"].loc[as_of_date, stock] if stock in factors["mom_20d"].columns else 0
            
            if "vol_ratio" in factors and as_of_date in factors["vol_ratio"].index:
                target.vol_ratio = factors["vol_ratio"].loc[as_of_date, stock] if stock in factors["vol_ratio"].columns else 0
            
            if "is_first_limit_up" in factors and as_of_date in factors["is_first_limit_up"].index:
                target.is_first_limit_up = bool(factors["is_first_limit_up"].loc[as_of_date, stock]) if stock in factors["is_first_limit_up"].columns else False
            
            # 判断信号类型
            target.signal_type = self._determine_signal_type(target)
            
            # 生成入场理由
            target.entry_reason = self._generate_entry_reason(target)
            
            # 建议仓位
            target.suggested_position = min(0.2, 1.0 / max_targets)
            
            # 题材得分
            if self.theme_identifier:
                profile = self.theme_identifier.identify_stock_themes(
                    target.code, target.name, target.industry
                )
                target.theme_score = profile.total_theme_score
            
            targets.append(target)
        
        logger.info(f"Stage 2 完成: 生成 {len(targets)} 个最终标的")
        
        return targets
    
    def _determine_signal_type(self, target: TargetStock) -> str:
        """判断信号类型"""
        if target.is_first_limit_up:
            return "首板启动"
        
        if target.mom_20d > 15 and target.vol_ratio > 1.5:
            return "强势突破"
        
        if target.mom_20d > 10 and target.vol_ratio > 2.0:
            return "量价齐升"
        
        if target.mom_20d > 5:
            return "动量上涨"
        
        return "其他信号"
    
    def _generate_entry_reason(self, target: TargetStock) -> str:
        """生成入场理由"""
        reasons = []
        
        if target.is_first_limit_up:
            reasons.append("首次涨停放量")
        
        if target.mom_20d > 10:
            reasons.append(f"20日动量{target.mom_20d:.1f}%")
        
        if target.vol_ratio > 2.0:
            reasons.append(f"量比{target.vol_ratio:.1f}")
        
        if target.theme_score > 30:
            reasons.append("属于热门题材")
        
        return ", ".join(reasons) if reasons else "信号触发"
    
    def build(
        self,
        all_stocks: List[str],
        stock_info: pd.DataFrame,
        signals: pd.DataFrame,
        scores: pd.DataFrame,
        factors: Dict[str, pd.DataFrame],
        as_of_date: str,
        max_targets: int = 8,
    ) -> BuilderResult:
        """
        完整构建流程
        
        Args:
            all_stocks: 全部股票
            stock_info: 股票信息
            signals: 信号矩阵
            scores: 评分矩阵
            factors: 因子字典
            as_of_date: 日期
            max_targets: 最大标的数
        
        Returns:
            BuilderResult: 构建结果
        """
        result = BuilderResult(
            total_stocks_scanned=len(all_stocks),
            build_date=as_of_date,
        )
        
        # Stage 1
        pool, stats = self.build_stage1_pool(all_stocks, stock_info, as_of_date)
        result.preliminary_pool = pool
        result.stage1_count = len(pool)
        result.filter_stats = stats
        
        # Stage 2
        targets = self.build_stage2_targets(
            pool, signals, scores, factors, stock_info, as_of_date, max_targets
        )
        result.final_targets = targets
        result.stage2_count = len(targets)
        
        return result


# ============ 测试函数 ============

def test_investment_target_builder():
    """测试投资标的构建器"""
    print("=" * 60)
    print("InvestmentTargetBuilder 单元测试")
    print("=" * 60)
    
    builder = InvestmentTargetBuilder()
    
    # 测试1: 基础过滤
    print("\n1. 测试基础过滤...")
    all_stocks = ["000001.XSHE", "688001.XSHG", "ST股票.XSHE", "300001.XSHE"]
    
    # 创建模拟股票信息
    stock_info = pd.DataFrame({
        "name": ["平安银行", "科创板公司", "ST股票", "中小板公司"],
        "market_cap": [3000e8, 500e8, 50e8, 100e8],
        "industry": ["银行", "科技", "制造", "软件"],
    }, index=all_stocks)
    
    pool, stats = builder.build_stage1_pool(all_stocks, stock_info, "2026-01-12")
    print(f"   输入: {len(all_stocks)}")
    print(f"   输出: {len(pool)}")
    print(f"   统计: {stats}")
    print("   ✓ 通过")
    
    # 测试2: 信号筛选
    print("\n2. 测试信号筛选...")
    signals = pd.DataFrame({
        "000001.XSHE": [1, 0, 1],
        "300001.XSHE": [0, 1, 1],
    }, index=pd.to_datetime(["2026-01-10", "2026-01-11", "2026-01-12"]))
    
    scores = pd.DataFrame({
        "000001.XSHE": [70, 60, 80],
        "300001.XSHE": [65, 75, 85],
    }, index=pd.to_datetime(["2026-01-10", "2026-01-11", "2026-01-12"]))
    
    factors = {
        "mom_20d": pd.DataFrame({
            "000001.XSHE": [5, 8, 12],
            "300001.XSHE": [10, 15, 20],
        }, index=pd.to_datetime(["2026-01-10", "2026-01-11", "2026-01-12"])),
    }
    
    targets = builder.build_stage2_targets(
        ["000001.XSHE", "300001.XSHE"],
        signals, scores, factors, stock_info,
        "2026-01-12", max_targets=5
    )
    
    print(f"   最终标的数: {len(targets)}")
    for t in targets:
        print(f"   - {t.code}: 评分={t.signal_score}, 类型={t.signal_type}")
    print("   ✓ 通过")
    
    # 测试3: 完整构建
    print("\n3. 测试完整构建...")
    result = builder.build(
        all_stocks, stock_info, signals, scores, factors,
        "2026-01-12", max_targets=5
    )
    
    print(f"   Stage1: {result.stage1_count}")
    print(f"   Stage2: {result.stage2_count}")
    print(f"   摘要:\n{result.summary()[:300]}...")
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_investment_target_builder()
