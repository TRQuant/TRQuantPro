# -*- coding: utf-8 -*-
"""
因子基类模块
============

提供因子计算的基础框架，包括：
- 数据预处理（去极值、标准化、行业中性化）
- 因子有效性评估（IC、IR、换手率）
- 缓存管理
- PTrade兼容的代码生成
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging
import hashlib
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class FactorResult:
    """因子计算结果"""
    name: str                           # 因子名称
    date: datetime                      # 计算日期
    values: pd.Series                   # 因子值（index为股票代码）
    raw_values: Optional[pd.Series] = None  # 原始因子值（未处理）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def stocks(self) -> List[str]:
        """获取股票列表"""
        return self.values.index.tolist()
    
    @property
    def valid_count(self) -> int:
        """有效值数量"""
        return self.values.notna().sum()
    
    @property
    def coverage(self) -> float:
        """覆盖率"""
        return self.valid_count / len(self.values) if len(self.values) > 0 else 0
    
    def top_n(self, n: int = 30) -> List[str]:
        """获取因子值最高的N只股票"""
        return self.values.nlargest(n).index.tolist()
    
    def bottom_n(self, n: int = 30) -> List[str]:
        """获取因子值最低的N只股票"""
        return self.values.nsmallest(n).index.tolist()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'date': self.date.isoformat() if isinstance(self.date, datetime) else str(self.date),
            'values': self.values.to_dict(),
            'valid_count': self.valid_count,
            'coverage': self.coverage,
            'metadata': self.metadata
        }


class BaseFactor(ABC):
    """
    因子基类
    
    所有因子都应继承此类，并实现calculate_raw方法。
    基类提供：
    - 数据预处理（去极值、标准化、行业中性化）
    - 缓存管理
    - 因子评估
    - PTrade代码生成
    """
    
    # 因子元信息（子类应覆盖）
    name: str = "BaseFactor"
    category: str = "base"  # value, growth, quality, momentum, flow
    description: str = "基础因子"
    direction: int = 1  # 1=越大越好, -1=越小越好
    
    def __init__(
        self,
        jq_client=None,
        cache_dir: Optional[Path] = None,
        use_cache: bool = True
    ):
        """
        初始化因子
        
        Args:
            jq_client: JQData客户端
            cache_dir: 缓存目录
            use_cache: 是否使用缓存
        """
        self.jq_client = jq_client
        self.cache_dir = cache_dir or Path(__file__).parent.parent.parent / "data" / "factors"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_cache = use_cache
        self._cache = {}
    
    @abstractmethod
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """
        计算原始因子值（子类必须实现）
        
        Args:
            stocks: 股票列表
            date: 计算日期
            **kwargs: 额外参数
        
        Returns:
            pd.Series: 因子值，index为股票代码
        """
        pass
    
    def calculate(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        winsorize: bool = True,
        standardize: bool = True,
        neutralize: bool = False,
        **kwargs
    ) -> FactorResult:
        """
        计算因子（带预处理）
        
        Args:
            stocks: 股票列表
            date: 计算日期
            winsorize: 是否去极值
            standardize: 是否标准化
            neutralize: 是否行业中性化
            **kwargs: 额外参数
        
        Returns:
            FactorResult: 因子计算结果
        """
        # 标准化日期格式
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        # 检查缓存
        cache_key = self._get_cache_key(stocks, date, winsorize, standardize, neutralize)
        if self.use_cache and cache_key in self._cache:
            logger.debug(f"使用缓存: {self.name} @ {date}")
            return self._cache[cache_key]
        
        # 计算原始因子值
        logger.info(f"计算因子: {self.name} @ {date}, 股票数: {len(stocks)}")
        raw_values = self.calculate_raw(stocks, date, **kwargs)
        
        # 数据预处理
        processed_values = raw_values.copy()
        
        if winsorize:
            processed_values = self._winsorize_mad(processed_values)
        
        if neutralize:
            processed_values = self._industry_neutralize(processed_values, stocks, date)
        
        if standardize:
            processed_values = self._standardize(processed_values)
        
        # 构建结果
        result = FactorResult(
            name=self.name,
            date=date,
            values=processed_values,
            raw_values=raw_values,
            metadata={
                'category': self.category,
                'direction': self.direction,
                'winsorize': winsorize,
                'standardize': standardize,
                'neutralize': neutralize
            }
        )
        
        # 缓存结果
        if self.use_cache:
            self._cache[cache_key] = result
        
        return result
    
    def _winsorize_mad(self, series: pd.Series, n: float = 5.0) -> pd.Series:
        """
        MAD法去极值
        
        Args:
            series: 原始数据
            n: MAD倍数阈值
        
        Returns:
            去极值后的数据
        """
        median = series.median()
        mad = (series - median).abs().median()
        
        if mad == 0:
            return series
        
        upper = median + n * 1.4826 * mad
        lower = median - n * 1.4826 * mad
        
        return series.clip(lower, upper)
    
    def _standardize(self, series: pd.Series) -> pd.Series:
        """
        Z-score标准化
        
        Args:
            series: 原始数据
        
        Returns:
            标准化后的数据
        """
        mean = series.mean()
        std = series.std()
        
        if std == 0 or pd.isna(std):
            return series - mean
        
        return (series - mean) / std
    
    def _industry_neutralize(
        self,
        series: pd.Series,
        stocks: List[str],
        date: Union[str, datetime]
    ) -> pd.Series:
        """
        行业中性化
        
        Args:
            series: 因子值
            stocks: 股票列表
            date: 日期
        
        Returns:
            行业中性化后的因子值
        """
        if self.jq_client is None:
            logger.warning("未设置JQ客户端，跳过行业中性化")
            return series
        
        try:
            import jqdatasdk as jq
            
            # 获取行业分类
            industries = jq.get_industry(stocks, date=date)
            industry_map = {}
            for stock, ind_info in industries.items():
                if 'sw_l1' in ind_info:
                    industry_map[stock] = ind_info['sw_l1']['industry_name']
                else:
                    industry_map[stock] = 'Unknown'
            
            # 构建DataFrame
            df = pd.DataFrame({
                'factor': series,
                'industry': pd.Series(industry_map)
            })
            
            # 行业内标准化
            df['factor_neutral'] = df.groupby('industry')['factor'].transform(
                lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
            )
            
            return df['factor_neutral']
        
        except Exception as e:
            logger.warning(f"行业中性化失败: {e}")
            return series
    
    def _get_cache_key(
        self,
        stocks: List[str],
        date: datetime,
        winsorize: bool,
        standardize: bool,
        neutralize: bool
    ) -> str:
        """生成缓存键"""
        stocks_hash = hashlib.md5('_'.join(sorted(stocks)).encode()).hexdigest()[:8]
        date_str = date.strftime('%Y%m%d')
        return f"{self.name}_{date_str}_{stocks_hash}_{winsorize}_{standardize}_{neutralize}"
    
    def get_ptrade_code(self) -> str:
        """
        生成PTrade兼容的因子计算代码
        
        Returns:
            str: PTrade策略代码片段
        """
        return f'''
# {self.name} - {self.description}
# 因子方向: {"越大越好" if self.direction == 1 else "越小越好"}

def calculate_{self.name.lower()}(stocks, date):
    """计算{self.description}"""
    # 此处添加因子计算逻辑
    pass
'''
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info(f"因子缓存已清空: {self.name}")
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, category={self.category})>"

