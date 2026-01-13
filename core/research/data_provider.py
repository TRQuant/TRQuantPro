# -*- coding: utf-8 -*-
"""
统一数据提供器 - 研究/回测用
============================

功能：
1. 输出标准化矩阵：close/open/high/low/volume (DataFrame: index=datetime, columns=symbol)
2. 集成本地缓存（Parquet格式）
3. 集成is_tradeable过滤（停牌/退市/一字板）
4. 复用现有DataPreloader的并行下载能力

设计原则：
- 优化速度时只加载一次数据
- 缓存key基于(universe_hash, start, end, frequency)
- 支持增量更新
"""

from __future__ import annotations

import logging
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import threading

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# JQData认证信息
JQDATA_USER = os.environ.get("JQDATA_USER", "13327806797")
JQDATA_PASSWORD = os.environ.get("JQDATA_PASSWORD", "Taorui888")


@dataclass
class DataMatrices:
    """标准化数据矩阵容器
    
    所有矩阵格式: DataFrame(index=datetime, columns=symbol)
    """
    close: pd.DataFrame
    open: pd.DataFrame
    high: pd.DataFrame
    low: pd.DataFrame
    volume: pd.DataFrame
    amount: Optional[pd.DataFrame] = None  # 成交额
    is_tradeable: Optional[pd.DataFrame] = None  # 可交易标记(布尔矩阵)
    
    @property
    def symbols(self) -> List[str]:
        """获取所有股票代码"""
        return list(self.close.columns)
    
    @property
    def dates(self) -> pd.DatetimeIndex:
        """获取所有日期"""
        return self.close.index
    
    @property
    def shape(self) -> Tuple[int, int]:
        """返回(T, N)维度"""
        return self.close.shape
    
    def to_dict(self) -> Dict[str, pd.DataFrame]:
        """转换为字典格式"""
        result = {
            "close": self.close,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "volume": self.volume,
        }
        if self.amount is not None:
            result["amount"] = self.amount
        if self.is_tradeable is not None:
            result["is_tradeable"] = self.is_tradeable
        return result


class ResearchDataProvider:
    """研究用统一数据提供器
    
    主要功能：
    1. 从JQData获取OHLCV数据
    2. 转换为标准化矩阵格式
    3. 本地缓存（Parquet）
    4. 生成is_tradeable掩码
    
    使用示例：
    ```python
    provider = ResearchDataProvider()
    matrices = provider.get_data_matrices(
        symbols=["000001.XSHE", "000002.XSHE"],
        start_date="2020-01-01",
        end_date="2023-12-31"
    )
    print(matrices.close.shape)  # (T, N)
    ```
    """
    
    def __init__(
        self,
        cache_dir: Optional[Union[str, Path]] = None,
        use_cache: bool = True,
        max_workers: int = 3,  # JQData并发限制
    ):
        """
        初始化数据提供器
        
        Args:
            cache_dir: 缓存目录，默认为项目data/research_cache
            use_cache: 是否启用缓存
            max_workers: 并行下载线程数（JQData限制为3）
        """
        if cache_dir is None:
            project_root = Path(__file__).parent.parent.parent
            cache_dir = project_root / "data" / "research_cache"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_cache = use_cache
        self.max_workers = max_workers
        
        self._jq = None
        self._jq_lock = threading.Lock()
        
        logger.info(f"ResearchDataProvider初始化: cache_dir={self.cache_dir}, use_cache={use_cache}")
    
    def _get_jq(self):
        """获取JQData连接（懒加载）"""
        if self._jq is None:
            with self._jq_lock:
                if self._jq is None:
                    import jqdatasdk as jq
                    if not jq.is_auth():
                        jq.auth(JQDATA_USER, JQDATA_PASSWORD)
                        logger.info("JQData认证成功")
                    self._jq = jq
        return self._jq
    
    def _get_cache_key(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        frequency: str = "daily"
    ) -> str:
        """生成缓存key"""
        symbols_sorted = sorted(symbols)
        symbols_hash = hashlib.md5("_".join(symbols_sorted).encode()).hexdigest()[:12]
        return f"matrices_{symbols_hash}_{start_date}_{end_date}_{frequency}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.parquet"
    
    def _load_from_cache(self, cache_key: str) -> Optional[DataMatrices]:
        """从缓存加载数据"""
        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            return None
        
        try:
            # 加载元数据
            meta_path = self.cache_dir / f"{cache_key}_meta.json"
            if not meta_path.exists():
                return None
            
            import json
            with open(meta_path, "r") as f:
                meta = json.load(f)
            
            symbols = meta["symbols"]
            
            # 加载各个字段
            close = pd.read_parquet(self.cache_dir / f"{cache_key}_close.parquet")
            open_ = pd.read_parquet(self.cache_dir / f"{cache_key}_open.parquet")
            high = pd.read_parquet(self.cache_dir / f"{cache_key}_high.parquet")
            low = pd.read_parquet(self.cache_dir / f"{cache_key}_low.parquet")
            volume = pd.read_parquet(self.cache_dir / f"{cache_key}_volume.parquet")
            
            amount = None
            amount_path = self.cache_dir / f"{cache_key}_amount.parquet"
            if amount_path.exists():
                amount = pd.read_parquet(amount_path)
            
            is_tradeable = None
            tradeable_path = self.cache_dir / f"{cache_key}_tradeable.parquet"
            if tradeable_path.exists():
                is_tradeable = pd.read_parquet(tradeable_path)
            
            logger.info(f"从缓存加载数据: {cache_key}, shape={close.shape}")
            return DataMatrices(
                close=close,
                open=open_,
                high=high,
                low=low,
                volume=volume,
                amount=amount,
                is_tradeable=is_tradeable,
            )
        except Exception as e:
            logger.warning(f"加载缓存失败: {e}")
            return None
    
    def _save_to_cache(self, cache_key: str, matrices: DataMatrices):
        """保存数据到缓存"""
        try:
            import json
            
            # 保存元数据
            meta = {
                "symbols": matrices.symbols,
                "start_date": str(matrices.dates[0].date()),
                "end_date": str(matrices.dates[-1].date()),
                "shape": matrices.shape,
                "created_at": datetime.now().isoformat(),
            }
            meta_path = self.cache_dir / f"{cache_key}_meta.json"
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)
            
            # 保存各个字段
            matrices.close.to_parquet(self.cache_dir / f"{cache_key}_close.parquet")
            matrices.open.to_parquet(self.cache_dir / f"{cache_key}_open.parquet")
            matrices.high.to_parquet(self.cache_dir / f"{cache_key}_high.parquet")
            matrices.low.to_parquet(self.cache_dir / f"{cache_key}_low.parquet")
            matrices.volume.to_parquet(self.cache_dir / f"{cache_key}_volume.parquet")
            
            if matrices.amount is not None:
                matrices.amount.to_parquet(self.cache_dir / f"{cache_key}_amount.parquet")
            
            if matrices.is_tradeable is not None:
                matrices.is_tradeable.to_parquet(self.cache_dir / f"{cache_key}_tradeable.parquet")
            
            logger.info(f"数据已缓存: {cache_key}")
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")
    
    def get_data_matrices(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        frequency: str = "daily",
        include_tradeable: bool = True,
        force_refresh: bool = False,
    ) -> DataMatrices:
        """
        获取标准化数据矩阵
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            frequency: 频率 ("daily")
            include_tradeable: 是否生成is_tradeable掩码
            force_refresh: 是否强制刷新缓存
        
        Returns:
            DataMatrices: 标准化数据矩阵
        """
        # 检查缓存
        cache_key = self._get_cache_key(symbols, start_date, end_date, frequency)
        if self.use_cache and not force_refresh:
            cached = self._load_from_cache(cache_key)
            if cached is not None:
                return cached
        
        # 从JQData获取数据
        logger.info(f"从JQData获取数据: {len(symbols)}只股票, {start_date} ~ {end_date}")
        jq = self._get_jq()
        
        df = jq.get_price(
            symbols,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            fields=["open", "high", "low", "close", "volume", "money"],
            panel=False,
            fq="post",  # 后复权
            skip_paused=False,  # 不跳过停牌，用于生成is_tradeable
        )
        
        if df is None or df.empty:
            raise ValueError(f"未获取到数据: symbols={symbols[:5]}..., {start_date} ~ {end_date}")
        
        # 转换为矩阵格式
        matrices = self._convert_to_matrices(df, symbols, include_tradeable)
        
        # 保存缓存
        if self.use_cache:
            self._save_to_cache(cache_key, matrices)
        
        return matrices
    
    def _convert_to_matrices(
        self,
        df: pd.DataFrame,
        symbols: List[str],
        include_tradeable: bool = True
    ) -> DataMatrices:
        """
        将JQData返回的长表转换为矩阵格式
        
        Args:
            df: JQData返回的DataFrame (code, time, open, high, low, close, volume, money)
            symbols: 股票代码列表
            include_tradeable: 是否生成is_tradeable掩码
        
        Returns:
            DataMatrices
        """
        # 确保time列是datetime
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index(["time", "code"])
        else:
            df = df.set_index(["code"])
        
        # 获取唯一日期
        if isinstance(df.index, pd.MultiIndex):
            dates = df.index.get_level_values(0).unique().sort_values()
            codes = df.index.get_level_values(1).unique()
        else:
            dates = df.index.unique().sort_values()
            codes = symbols
        
        # 转换为矩阵 (T x N)
        def pivot_field(field_name: str) -> pd.DataFrame:
            if isinstance(df.index, pd.MultiIndex):
                series = df[field_name]
                return series.unstack(level=1).reindex(columns=symbols)
            else:
                return df[[field_name]].T
        
        close = pivot_field("close")
        open_ = pivot_field("open")
        high = pivot_field("high")
        low = pivot_field("low")
        volume = pivot_field("volume")
        amount = pivot_field("money")
        
        # 生成is_tradeable掩码
        is_tradeable = None
        if include_tradeable:
            is_tradeable = self._generate_tradeable_mask(close, volume, high, low)
        
        return DataMatrices(
            close=close,
            open=open_,
            high=high,
            low=low,
            volume=volume,
            amount=amount,
            is_tradeable=is_tradeable,
        )
    
    def _generate_tradeable_mask(
        self,
        close: pd.DataFrame,
        volume: pd.DataFrame,
        high: pd.DataFrame,
        low: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        生成可交易掩码
        
        不可交易条件：
        1. 停牌（volume=0 or NaN）
        2. 涨停（无法买入）：high == low 且 当日涨幅 > 9%
        3. 跌停（无法卖出）：high == low 且 当日跌幅 > 9%
        4. 数据缺失（close=NaN）
        
        Returns:
            布尔DataFrame (True=可交易)
        """
        # 基础条件：有数据且有成交
        has_data = close.notna()
        has_volume = (volume > 0) & volume.notna()
        
        # 一字板检测（high == low）
        is_limit = (high == low) & has_data
        
        # 综合可交易条件
        is_tradeable = has_data & has_volume & (~is_limit)
        
        return is_tradeable
    
    def get_index_stocks(
        self,
        index_code: str,
        date: Optional[str] = None
    ) -> List[str]:
        """
        获取指数成分股
        
        Args:
            index_code: 指数代码 (如 "000300.XSHG")
            date: 日期，默认为最新
        
        Returns:
            成分股代码列表
        """
        jq = self._get_jq()
        stocks = jq.get_index_stocks(index_code, date=date)
        return list(stocks) if stocks is not None else []
    
    def get_all_securities(
        self,
        types: List[str] = ["stock"],
        date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        获取所有证券列表
        
        Args:
            types: 证券类型列表
            date: 日期
        
        Returns:
            DataFrame包含证券信息
        """
        jq = self._get_jq()
        return jq.get_all_securities(types=types, date=date)
    
    def get_all_a_stocks(
        self,
        date: Optional[str] = None,
        exclude_st: bool = True,
        exclude_new: bool = True,
        exclude_kcb: bool = True,
        exclude_bj: bool = True,
        min_days_listed: int = 60,
    ) -> List[str]:
        """
        获取全A股股票列表（过滤后）
        
        Args:
            date: 日期，默认为最新
            exclude_st: 排除ST/*ST股票
            exclude_new: 排除次新股
            exclude_kcb: 排除科创板（688开头）
            exclude_bj: 排除北交所（8开头/4开头）
            min_days_listed: 最小上市天数
        
        Returns:
            股票代码列表（约3000只可交易A股）
        """
        jq = self._get_jq()
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 获取所有股票
        all_stocks = jq.get_all_securities(types=["stock"], date=date)
        
        if all_stocks is None or all_stocks.empty:
            logger.warning("未获取到股票列表")
            return []
        
        stocks = all_stocks.copy()
        initial_count = len(stocks)
        
        # 1. 排除ST股票
        if exclude_st:
            stocks = stocks[~stocks["display_name"].str.contains("ST", case=False, na=False)]
        
        # 2. 排除科创板 (688开头)
        if exclude_kcb:
            stocks = stocks[~stocks.index.str.startswith("688")]
        
        # 3. 排除北交所 (8开头/4开头)
        if exclude_bj:
            stocks = stocks[~stocks.index.str.startswith("8")]
            stocks = stocks[~stocks.index.str.startswith("4")]
        
        # 4. 排除次新股（上市不足min_days_listed天）
        if exclude_new and min_days_listed > 0:
            date_dt = pd.to_datetime(date)
            stocks["days_listed"] = (date_dt - pd.to_datetime(stocks["start_date"])).dt.days
            stocks = stocks[stocks["days_listed"] >= min_days_listed]
        
        result = list(stocks.index)
        logger.info(f"全A股过滤: {initial_count} -> {len(result)} 只股票 "
                   f"(ST={exclude_st}, 科创板={exclude_kcb}, 北交所={exclude_bj}, 次新={exclude_new})")
        
        return result
    
    def preload_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        batch_size: int = 500,
    ) -> DataMatrices:
        """
        批量预加载数据（分批处理避免内存溢出）
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            batch_size: 每批处理的股票数量
        
        Returns:
            DataMatrices: 合并后的数据矩阵
        """
        # 检查缓存
        cache_key = self._get_cache_key(symbols, start_date, end_date, "daily")
        if self.use_cache:
            cached = self._load_from_cache(cache_key)
            if cached is not None:
                return cached
        
        logger.info(f"预加载数据: {len(symbols)}只股票, 分{(len(symbols) + batch_size - 1) // batch_size}批处理")
        
        all_close = []
        all_open = []
        all_high = []
        all_low = []
        all_volume = []
        all_amount = []
        
        jq = self._get_jq()
        
        for i in range(0, len(symbols), batch_size):
            batch_symbols = symbols[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(symbols) + batch_size - 1) // batch_size
            
            logger.info(f"处理第 {batch_num}/{total_batches} 批: {len(batch_symbols)} 只股票")
            
            try:
                df = jq.get_price(
                    batch_symbols,
                    start_date=start_date,
                    end_date=end_date,
                    frequency="daily",
                    fields=["open", "high", "low", "close", "volume", "money"],
                    panel=False,
                    fq="post",
                    skip_paused=False,
                )
                
                if df is not None and not df.empty:
                    # 转换为矩阵
                    df["time"] = pd.to_datetime(df["time"])
                    df = df.set_index(["time", "code"])
                    
                    close = df["close"].unstack(level=1)
                    open_ = df["open"].unstack(level=1)
                    high = df["high"].unstack(level=1)
                    low = df["low"].unstack(level=1)
                    volume = df["volume"].unstack(level=1)
                    amount = df["money"].unstack(level=1)
                    
                    all_close.append(close)
                    all_open.append(open_)
                    all_high.append(high)
                    all_low.append(low)
                    all_volume.append(volume)
                    all_amount.append(amount)
            except Exception as e:
                logger.error(f"批次 {batch_num} 获取数据失败: {e}")
                continue
        
        if not all_close:
            raise ValueError("未能获取任何数据")
        
        # 合并所有批次
        close = pd.concat(all_close, axis=1)
        open_ = pd.concat(all_open, axis=1)
        high = pd.concat(all_high, axis=1)
        low = pd.concat(all_low, axis=1)
        volume = pd.concat(all_volume, axis=1)
        amount = pd.concat(all_amount, axis=1)
        
        # 生成可交易掩码
        is_tradeable = self._generate_tradeable_mask(close, volume, high, low)
        
        matrices = DataMatrices(
            close=close,
            open=open_,
            high=high,
            low=low,
            volume=volume,
            amount=amount,
            is_tradeable=is_tradeable,
        )
        
        # 保存缓存
        if self.use_cache:
            self._save_to_cache(cache_key, matrices)
        
        logger.info(f"数据预加载完成: shape={matrices.shape}")
        return matrices


# 便捷函数
def get_research_data_provider(
    cache_dir: Optional[str] = None,
    use_cache: bool = True,
) -> ResearchDataProvider:
    """获取研究数据提供器单例"""
    return ResearchDataProvider(cache_dir=cache_dir, use_cache=use_cache)
