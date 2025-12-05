"""
技术突破扫描器

功能：全市场扫描技术面强势的股票（非主线标的）

扫描信号：
- 创新高（20日/60日/250日）
- 放量突破
- 均线金叉
- 涨停突破

这些股票可能是新主线的先行者，需要纳入候选池
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from ..models import StockPoolItem, StockPool, PoolSource, Period, PoolType

logger = logging.getLogger(__name__)

try:
    from markets.ashare.utils.akshare_wrapper import get_akshare_wrapper
    import pandas as pd
    import numpy as np
    ak_wrapper = get_akshare_wrapper()
    DEPS_AVAILABLE = ak_wrapper.available
except ImportError:
    DEPS_AVAILABLE = False
    ak_wrapper = None


class TechBreakoutScanner:
    """
    技术突破扫描器
    
    全市场扫描技术面强势股票
    """
    
    # 扫描配置
    DEFAULT_CONFIG = {
        # 基础过滤
        "exclude_st": True,
        "exclude_new_stocks_days": 60,   # 排除上市不足N天的新股
        "min_market_cap": 30,            # 最低市值（亿）
        "max_market_cap": 3000,          # 最高市值（亿）
        "min_avg_amount": 5000,          # 最低日均成交额（万）
        
        # 技术信号阈值
        "volume_ratio_threshold": 2.0,   # 量比阈值
        "new_high_days": [20, 60, 250],  # 新高周期
        "ma_golden_cross": [5, 20],      # 金叉均线
        
        # 输出控制
        "max_stocks": 30,                # 最多输出N只
    }
    
    def __init__(self, config: Dict = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
    
    def scan(self, period: str = "short") -> StockPool:
        """
        执行技术扫描
        
        Args:
            period: 投资周期，影响扫描条件
                - short: 侧重涨停、放量、短期新高
                - medium: 侧重均线多头、中期新高
                - long: 侧重长期趋势突破、底部反转
        
        Returns:
            技术突破股票池
        """
        if not DEPS_AVAILABLE:
            logger.error("依赖包未安装，无法执行扫描")
            return StockPool(description="技术扫描失败：依赖包未安装")
        
        logger.info("=" * 50)
        logger.info(f"开始技术突破扫描（{period}周期）...")
        
        pool = StockPool(
            description=f"技术突破股池 - {datetime.now().strftime('%Y-%m-%d')} - {period}周期"
        )
        
        try:
            # 使用包装器获取全市场行情（带重试和缓存）
            if not ak_wrapper:
                logger.error("AKShare包装器不可用")
                return pool
            
            df = ak_wrapper.get_stock_spot()
            if df is None or df.empty:
                logger.error("获取市场行情失败")
                return pool
            
            logger.info(f"获取到 {len(df)} 只股票行情")
            
            # 基础过滤
            df_filtered = self._basic_filter(df)
            logger.info(f"基础过滤后：{len(df_filtered)} 只")
            
            # 扫描技术信号
            if period == "short":
                candidates = self._scan_short_term(df_filtered)
            elif period == "medium":
                candidates = self._scan_medium_term(df_filtered)
            else:
                candidates = self._scan_long_term(df_filtered)
            
            logger.info(f"技术信号筛选：{len(candidates)} 只")
            
            # 转换为股票池条目
            for stock in candidates[:self.config["max_stocks"]]:
                item = StockPoolItem(
                    code=stock["code"],
                    name=stock["name"],
                    
                    source=PoolSource.TECH_BREAKOUT.value,
                    entry_reason=f"技术突破：{', '.join(stock['signals'])}",
                    
                    period=period,
                    pool_type=self._determine_pool_type(stock),
                    priority=self._calculate_priority(stock),
                    
                    current_price=stock.get("price", 0),
                    change_pct=stock.get("change_pct", 0),
                    tech_signals=stock["signals"]
                )
                pool.add_stock(item)
            
        except Exception as e:
            logger.error(f"技术扫描失败: {e}")
        
        logger.info(f"技术突破扫描完成，共 {len(pool.stocks)} 只股票")
        return pool
    
    def _basic_filter(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """基础过滤"""
        result = df.copy()
        
        # 排除ST
        if self.config["exclude_st"]:
            result = result[~result['名称'].str.contains('ST', na=False)]
        
        # 市值过滤
        result['市值_亿'] = result['总市值'].fillna(0) / 100000000
        result = result[result['市值_亿'] >= self.config["min_market_cap"]]
        result = result[result['市值_亿'] <= self.config["max_market_cap"]]
        
        # 成交额过滤
        result['成交额_万'] = result['成交额'].fillna(0) / 10000
        result = result[result['成交额_万'] >= self.config["min_avg_amount"]]
        
        return result
    
    def _scan_short_term(self, df: 'pd.DataFrame') -> List[Dict]:
        """短期技术扫描"""
        candidates = []
        
        for _, row in df.iterrows():
            signals = []
            score = 0
            
            code = row['代码']
            name = row['名称']
            change_pct = float(row.get('涨跌幅', 0) or 0)
            volume_ratio = float(row.get('量比', 1) or 1)
            turnover = float(row.get('换手率', 0) or 0)
            
            # 涨停信号
            if change_pct >= 9.9:
                signals.append("涨停")
                score += 30
            elif change_pct >= 7:
                signals.append("大涨7%+")
                score += 20
            elif change_pct >= 5:
                signals.append("上涨5%+")
                score += 10
            
            # 放量信号
            if volume_ratio >= 3:
                signals.append("放量3倍+")
                score += 25
            elif volume_ratio >= 2:
                signals.append("放量2倍+")
                score += 15
            
            # 换手率信号
            if 5 <= turnover <= 15:
                signals.append("活跃换手")
                score += 10
            
            # 只保留有信号的股票
            if signals and score >= 20:
                candidates.append({
                    "code": code,
                    "name": name,
                    "signals": signals,
                    "score": score,
                    "price": float(row.get('最新价', 0) or 0),
                    "change_pct": change_pct,
                    "volume_ratio": volume_ratio
                })
        
        # 按评分排序
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates
    
    def _scan_medium_term(self, df: 'pd.DataFrame') -> List[Dict]:
        """中期技术扫描"""
        candidates = []
        
        for _, row in df.iterrows():
            signals = []
            score = 0
            
            code = row['代码']
            name = row['名称']
            change_pct = float(row.get('涨跌幅', 0) or 0)
            
            # 中期涨幅信号（需要获取历史数据，这里简化处理）
            if change_pct >= 3:
                signals.append("日涨幅强势")
                score += 15
            
            # 60日涨幅（需要额外数据）
            pct_60d = float(row.get('60日涨跌幅', 0) or 0)
            if pct_60d >= 30:
                signals.append("60日涨幅30%+")
                score += 25
            elif pct_60d >= 15:
                signals.append("60日涨幅15%+")
                score += 15
            
            # 年涨幅
            pct_year = float(row.get('年初至今涨跌幅', 0) or 0)
            if pct_year >= 50:
                signals.append("年涨幅50%+")
                score += 20
            
            if signals and score >= 15:
                candidates.append({
                    "code": code,
                    "name": name,
                    "signals": signals,
                    "score": score,
                    "price": float(row.get('最新价', 0) or 0),
                    "change_pct": change_pct
                })
        
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates
    
    def _scan_long_term(self, df: 'pd.DataFrame') -> List[Dict]:
        """长期技术扫描"""
        candidates = []
        
        for _, row in df.iterrows():
            signals = []
            score = 0
            
            code = row['代码']
            name = row['名称']
            
            # 市盈率（估值）
            pe = float(row.get('市盈率-动态', 0) or 0)
            if 0 < pe < 20:
                signals.append("低估值PE<20")
                score += 20
            
            # 市净率
            pb = float(row.get('市净率', 0) or 0)
            if 0 < pb < 2:
                signals.append("低PB<2")
                score += 15
            
            # 年涨幅适中（不追高）
            pct_year = float(row.get('年初至今涨跌幅', 0) or 0)
            if -20 < pct_year < 30:
                signals.append("年涨幅适中")
                score += 10
            
            if signals and score >= 20:
                candidates.append({
                    "code": code,
                    "name": name,
                    "signals": signals,
                    "score": score,
                    "price": float(row.get('最新价', 0) or 0),
                    "change_pct": float(row.get('涨跌幅', 0) or 0)
                })
        
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates
    
    def _determine_pool_type(self, stock: Dict) -> str:
        """确定持仓类型"""
        score = stock.get("score", 0)
        if score >= 50:
            return PoolType.SATELLITE.value  # 技术股放卫星仓位
        else:
            return PoolType.WATCH.value
    
    def _calculate_priority(self, stock: Dict) -> int:
        """计算优先级"""
        score = stock.get("score", 0)
        if score >= 60:
            return 2
        elif score >= 40:
            return 3
        elif score >= 20:
            return 4
        else:
            return 5

