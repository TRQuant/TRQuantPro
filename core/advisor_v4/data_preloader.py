#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据预加载器 - 并行下载数据到本地缓存
======================================

功能：
1. 利用聚宽3个并发连接并行下载数据
2. 支持增量更新（只下载缺失数据）
3. 数据本地缓存（Parquet格式，高效读写）
4. 下载进度显示和断点续传
"""

from __future__ import annotations

import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
import threading

import pandas as pd
import numpy as np
from tqdm import tqdm

# 导入MongoDB存储模块
try:
    from core.advisor_v4.jqdata_mongodb_storage import JQDataMongoDBStorage
    MONGODB_STORAGE_AVAILABLE = True
except ImportError:
    MONGODB_STORAGE_AVAILABLE = False

logger = logging.getLogger(__name__)

# JQData认证信息
JQDATA_USER = os.environ.get("JQDATA_USER", "13327806797")
JQDATA_PASSWORD = os.environ.get("JQDATA_PASSWORD", "Taorui888")


def _init_jqdata_in_worker():
    """在工作进程中初始化JQData"""
    import jqdatasdk as jq
    if not jq.is_auth():
        jq.auth(JQDATA_USER, JQDATA_PASSWORD)


def _fetch_price_data_worker(args: Dict) -> Optional[pd.DataFrame]:
    """
    工作进程：获取价格数据
    
    Args:
        args: {
            "codes": List[str],
            "start_date": str,
            "end_date": str,
            "fields": List[str]
        }
    
    Returns:
        DataFrame or None
    """
    try:
        _init_jqdata_in_worker()
        import jqdatasdk as jq
        
        codes = args["codes"]
        start_date = args["start_date"]
        end_date = args["end_date"]
        fields = args.get("fields", ["open", "high", "low", "close", "volume", "money"])
        
        if not codes:
            return None
        
        df = jq.get_price(
            codes,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            fields=fields,
            panel=False,
            fq="post"
        )
        
        return df
    except Exception as e:
        logger.error(f"获取价格数据失败: {e}")
        return None


def _fetch_fundamentals_worker(args: Dict) -> Optional[pd.DataFrame]:
    """
    工作进程：获取基本面数据
    
    Args:
        args: {
            "codes": List[str],
            "date": str,
            "data_type": str  # "valuation" or "indicator"
        }
    
    Returns:
        DataFrame or None
    """
    try:
        _init_jqdata_in_worker()
        import jqdatasdk as jq
        from jqdatasdk import query, valuation, indicator
        
        codes = args["codes"]
        date = args["date"]
        data_type = args.get("data_type", "valuation")
        
        if not codes:
            return None
        
        if data_type == "valuation":
            # 市值、换手率等
            q = query(
                valuation.code,
                valuation.market_cap,
                valuation.turnover_ratio,
                valuation.pe_ratio,
                valuation.pb_ratio,
            ).filter(valuation.code.in_(codes))
        elif data_type == "indicator":
            # ROE、净利润增长率等
            q = query(
                indicator.code,
                indicator.roe,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year,
            ).filter(indicator.code.in_(codes))
        else:
            return None
        
        df = jq.get_fundamentals(q, date=date)
        return df
    except Exception as e:
        logger.error(f"获取基本面数据失败: {e}")
        return None


def _fetch_index_data_worker(args: Dict) -> Optional[pd.DataFrame]:
    """
    工作进程：获取指数数据
    
    Args:
        args: {
            "index_code": str,
            "start_date": str,
            "end_date": str
        }
    
    Returns:
        DataFrame or None
    """
    try:
        _init_jqdata_in_worker()
        import jqdatasdk as jq
        
        index_code = args["index_code"]
        start_date = args["start_date"]
        end_date = args["end_date"]
        
        df = jq.get_price(
            index_code,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            fields=["open", "high", "low", "close", "volume", "money"],
            panel=False,
            fq="post"
        )
        
        return df
    except Exception as e:
        logger.error(f"获取指数数据失败: {e}")
        return None


@dataclass
class PreloadProgress:
    """预加载进度"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    current_task: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def progress(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.completed_tasks / self.total_tasks
    
    @property
    def elapsed_seconds(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def eta_seconds(self) -> float:
        if self.completed_tasks == 0:
            return 0.0
        rate = self.completed_tasks / self.elapsed_seconds
        remaining = self.total_tasks - self.completed_tasks
        return remaining / rate if rate > 0 else 0.0


@dataclass
class PreloadResult:
    """预加载结果"""
    success: bool = True
    cache_paths: Dict[str, Path] = field(default_factory=dict)
    total_stocks: int = 0
    total_trading_days: int = 0
    data_size_mb: float = 0.0
    duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)


class DataPreloader:
    """数据预加载器 - 并行下载数据到本地缓存"""
    
    def __init__(
        self,
        max_workers: int = 3,
        cache_dir: str = "data/cache",
        verbose: bool = True,
        use_mongodb: bool = True
    ):
        """
        初始化数据预加载器
        
        Args:
            max_workers: 最大并行工作数（聚宽最大3个连接）
            cache_dir: 缓存目录
            verbose: 是否显示详细输出
            use_mongodb: 是否使用MongoDB存储（默认True）
        """
        self.max_workers = min(max_workers, 3)  # 聚宽限制最大3个连接
        self.cache_dir = Path(cache_dir)
        self.verbose = verbose
        self.use_mongodb = use_mongodb and MONGODB_STORAGE_AVAILABLE
        
        # 初始化MongoDB存储（如果可用）
        self.mongodb_storage = None
        if self.use_mongodb:
            try:
                self.mongodb_storage = JQDataMongoDBStorage()
                if self.verbose:
                    print(f"✅ MongoDB存储已启用: {self.mongodb_storage.db_name}")
            except Exception as e:
                logger.warning(f"MongoDB存储初始化失败: {e}，将使用文件存储")
                self.mongodb_storage = None
                self.use_mongodb = False
        
        # 创建缓存目录结构
        self._init_cache_dirs()
        
        # 进度追踪
        self.progress = PreloadProgress()
        self._progress_lock = threading.Lock()
        
        # 元数据文件
        self.metadata_file = self.cache_dir / "metadata.json"
        self._metadata = self._load_metadata()
    
    def _init_cache_dirs(self):
        """初始化缓存目录结构"""
        subdirs = [
            "daily_prices",
            "fundamentals/valuation",
            "fundamentals/indicator",
            "indices",
            "stock_lists",
            "trade_days"  # 交易日缓存
        ]
        for subdir in subdirs:
            (self.cache_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def _load_metadata(self) -> Dict:
        """加载缓存元数据"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "cached_periods": {},
            "last_update": None
        }
    
    def _save_metadata(self):
        """保存缓存元数据"""
        self._metadata["last_update"] = datetime.now().isoformat()
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, indent=2, ensure_ascii=False)
    
    def _get_period_key(self, start_date: str, end_date: str) -> str:
        """生成时间段的缓存键"""
        # 按半年分区: 2024H1, 2024H2
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        year = start_dt.year
        half = "H1" if start_dt.month <= 6 else "H2"
        return f"{year}{half}"
    
    def _get_all_stocks(self, date: str = None) -> List[str]:
        """获取全A股列表"""
        try:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(JQDATA_USER, JQDATA_PASSWORD)
            
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            # 获取所有A股
            stocks = jq.get_all_securities(types=["stock"], date=date)
            all_codes = stocks.index.tolist()
            
            # 过滤ST和退市股票
            filtered_codes = [
                code for code in all_codes
                if not stocks.loc[code, "display_name"].startswith("ST")
                and not stocks.loc[code, "display_name"].startswith("*ST")
            ]
            
            return filtered_codes
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return []
    
    def _chunk_list(self, lst: List, chunk_size: int) -> List[List]:
        """将列表分成多个块"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    def _update_progress(self, task_name: str, increment: int = 1, failed: bool = False):
        """更新进度"""
        with self._progress_lock:
            self.progress.completed_tasks += increment
            if failed:
                self.progress.failed_tasks += increment
            self.progress.current_task = task_name
    
    def preload_market_data(
        self,
        start_date: str,
        end_date: str,
        stock_pool: List[str] = None,
        force_refresh: bool = False
    ) -> PreloadResult:
        """
        并行预加载市场数据
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            stock_pool: 股票池（None表示全A股）
            force_refresh: 强制刷新（忽略缓存）
        
        Returns:
            PreloadResult
        """
        result = PreloadResult()
        start_time = datetime.now()
        
        period_key = self._get_period_key(start_date, end_date)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"📦 数据预加载器 - 开始下载")
            print(f"{'='*60}")
            print(f"   时间段: {start_date} ~ {end_date}")
            print(f"   缓存目录: {self.cache_dir}")
            print(f"   并行连接数: {self.max_workers}")
        
        # 1. 获取股票列表
        if stock_pool is None:
            if self.verbose:
                print(f"\n📋 获取全A股列表...")
            stock_pool = self._get_all_stocks(end_date)
        
        if not stock_pool:
            result.success = False
            result.errors.append("无法获取股票列表")
            return result
        
        result.total_stocks = len(stock_pool)
        if self.verbose:
            print(f"   共 {result.total_stocks} 只股票")
        
        # 保存股票列表
        stock_list_path = self.cache_dir / "stock_lists" / f"{period_key}_stocks.json"
        with open(stock_list_path, "w", encoding="utf-8") as f:
            json.dump(stock_pool, f)
        result.cache_paths["stock_list"] = stock_list_path
        
        # 2. 下载/加载价格数据（优先MongoDB）
        prices_df = None
        if self.use_mongodb and self.mongodb_storage:
            # 优先从MongoDB加载
            if not force_refresh:
                prices_df = self.mongodb_storage.load_daily_prices(period_key=period_key)
                if prices_df is not None and not prices_df.empty:
                    if self.verbose:
                        print(f"\n✅ 价格数据已从MongoDB加载: {len(prices_df)}条")
                    result.cache_paths["prices"] = "mongodb"
            
            # 如果MongoDB中没有，则下载并保存
            if prices_df is None or prices_df.empty:
                prices_df = self._download_prices_parallel(
                    stock_pool, start_date, end_date, period_key
                )
                if prices_df is not None and not prices_df.empty:
                    # 保存到MongoDB
                    self.mongodb_storage.save_daily_prices(prices_df, period_key, start_date, end_date)
                    result.cache_paths["prices"] = "mongodb"
                    if self.verbose:
                        print(f"   ✅ 价格数据已保存到MongoDB: {len(prices_df)}条")
        else:
            # 使用文件存储
            prices_cache_path = self.cache_dir / "daily_prices" / f"{period_key}_prices.parquet"
            if prices_cache_path.exists() and not force_refresh:
                if self.verbose:
                    print(f"\n✅ 价格数据缓存已存在: {prices_cache_path}")
                prices_df = pd.read_parquet(prices_cache_path)
                result.cache_paths["prices"] = prices_cache_path
            else:
                # 下载价格数据
                prices_df = self._download_prices_parallel(
                    stock_pool, start_date, end_date, period_key
                )
                if prices_df is not None and not prices_df.empty:
                    prices_df.to_parquet(prices_cache_path, index=False)
                    result.cache_paths["prices"] = prices_cache_path
                    if self.verbose:
                        print(f"   ✅ 价格数据已保存: {prices_cache_path}")
        
        if prices_df is not None and not prices_df.empty:
            result.total_trading_days = prices_df["time"].nunique() if "time" in prices_df.columns else 0
            if self.verbose and result.total_trading_days > 0:
                print(f"   交易日数: {result.total_trading_days}")
        else:
            result.errors.append("价格数据下载失败")
        
        # 3. 下载基本面数据（按日期下载）
        fundamentals_result = self._download_fundamentals_parallel(
            stock_pool, start_date, end_date, period_key, force_refresh
        )
        result.cache_paths.update(fundamentals_result)
        
        # 4. 缓存交易日数据（避免BulletTrade引擎调用get_trade_days API）
        trade_days_result = self._cache_trade_days(start_date, end_date, period_key, force_refresh)
        result.cache_paths.update(trade_days_result)
        if trade_days_result:
            result.total_trading_days = len(trade_days_result.get('trade_days', []))
        
        # 5. 计算总大小
        total_size = 0
        for path in result.cache_paths.values():
            if isinstance(path, Path) and path.exists():
                total_size += path.stat().st_size
        result.data_size_mb = total_size / (1024 * 1024)
        
        # 6. 更新元数据
        self._metadata["cached_periods"][period_key] = {
            "start_date": start_date,
            "end_date": end_date,
            "total_stocks": result.total_stocks,
            "total_trading_days": result.total_trading_days,
            "cached_at": datetime.now().isoformat()
        }
        self._save_metadata()
        
        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        result.success = len(result.errors) == 0
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"📦 预加载完成")
            print(f"{'='*60}")
            print(f"   耗时: {result.duration_seconds:.1f} 秒")
            print(f"   数据大小: {result.data_size_mb:.1f} MB")
            print(f"   缓存文件数: {len(result.cache_paths)}")
            if result.errors:
                print(f"   ⚠️  错误: {len(result.errors)}")
                for err in result.errors[:3]:
                    print(f"      - {err}")
        
        return result
    
    def _download_prices_parallel(
        self,
        stock_pool: List[str],
        start_date: str,
        end_date: str,
        period_key: str
    ) -> Optional[pd.DataFrame]:
        """并行下载价格数据"""
        if self.verbose:
            print(f"\n📈 下载价格数据...")
        
        # 分块
        chunk_size = max(100, len(stock_pool) // self.max_workers)
        chunks = self._chunk_list(stock_pool, chunk_size)
        
        if self.verbose:
            print(f"   分 {len(chunks)} 批下载，每批约 {chunk_size} 只股票")
        
        all_dfs = []
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    _fetch_price_data_worker,
                    {
                        "codes": chunk,
                        "start_date": start_date,
                        "end_date": end_date,
                        "fields": ["open", "high", "low", "close", "volume", "money"]
                    }
                ): i for i, chunk in enumerate(chunks)
            }
            
            with tqdm(total=len(chunks), desc="下载价格数据", disable=not self.verbose) as pbar:
                for future in as_completed(futures):
                    try:
                        df = future.result()
                        if df is not None and not df.empty:
                            all_dfs.append(df)
                    except Exception as e:
                        logger.warning(f"批次下载失败: {e}")
                    pbar.update(1)
        
        if not all_dfs:
            return None
        
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df
    
    def _download_fundamentals_parallel(
        self,
        stock_pool: List[str],
        start_date: str,
        end_date: str,
        period_key: str,
        force_refresh: bool = False
    ) -> Dict[str, Path]:
        """并行下载基本面数据"""
        cache_paths = {}
        
        # 获取交易日列表
        try:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(JQDATA_USER, JQDATA_PASSWORD)
            trading_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        except Exception as e:
            logger.error(f"获取交易日失败: {e}")
            return cache_paths
        
        if self.verbose:
            print(f"\n📊 下载基本面数据...")
            print(f"   交易日数: {len(trading_days)}")
        
        # 每周下载一次基本面数据（减少API调用）
        sample_dates = [trading_days[i] for i in range(0, len(trading_days), 5)]
        
        # 分块股票
        chunk_size = max(500, len(stock_pool) // self.max_workers)
        chunks = self._chunk_list(stock_pool, chunk_size)
        
        # 下载估值数据（优先MongoDB）
        valuation_df = None
        if self.use_mongodb and self.mongodb_storage:
            # 检查MongoDB中是否已有数据
            if not force_refresh:
                # 尝试加载所有日期的数据
                for date in sample_dates[:1]:  # 只检查第一个日期
                    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
                    df = self.mongodb_storage.load_fundamentals("valuation", period_key=period_key, date=date_str)
                    if df is not None and not df.empty:
                        valuation_df = df
                        break
                if valuation_df is not None and not valuation_df.empty:
                    if self.verbose:
                        print(f"   ✅ 估值数据已从MongoDB加载")
                    cache_paths["valuation"] = "mongodb"
        
        if valuation_df is None or valuation_df.empty:
            # 从文件检查
            valuation_cache = self.cache_dir / "fundamentals/valuation" / f"{period_key}_valuation.parquet"
            if valuation_cache.exists() and not force_refresh:
                if self.verbose:
                    print(f"   ✅ 估值数据缓存已存在")
                cache_paths["valuation"] = valuation_cache
            else:
                # 下载数据
                valuation_dfs = []
                tasks = []
                for date in sample_dates:
                    for chunk in chunks:
                        tasks.append({
                            "codes": chunk,
                            "date": date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date),
                            "data_type": "valuation"
                        })
                
                with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(_fetch_fundamentals_worker, task) for task in tasks]
                    with tqdm(total=len(futures), desc="下载估值数据", disable=not self.verbose) as pbar:
                        for future in as_completed(futures):
                            try:
                                df = future.result()
                                if df is not None and not df.empty:
                                    valuation_dfs.append(df)
                            except Exception as e:
                                logger.warning(f"估值数据下载失败: {e}")
                            pbar.update(1)
                
                if valuation_dfs:
                    valuation_df = pd.concat(valuation_dfs, ignore_index=True).drop_duplicates()
                    
                    # 保存到MongoDB
                    if self.use_mongodb and self.mongodb_storage:
                        # 按日期保存
                        for date in sample_dates:
                            date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
                            date_df = valuation_df[valuation_df.get("date", pd.Series()).astype(str) == date_str] if "date" in valuation_df.columns else valuation_df
                            if not date_df.empty:
                                self.mongodb_storage.save_fundamentals(date_df, "valuation", period_key, date_str)
                        cache_paths["valuation"] = "mongodb"
                        if self.verbose:
                            print(f"   ✅ 估值数据已保存到MongoDB: {len(valuation_df)}条")
                    else:
                        # 文件存储
                        valuation_df.to_parquet(valuation_cache, index=False)
                        cache_paths["valuation"] = valuation_cache
                        if self.verbose:
                            print(f"   ✅ 估值数据已保存: {valuation_cache}")
        
        # 下载财务指标数据（优先MongoDB）
        indicator_df = None
        if self.use_mongodb and self.mongodb_storage:
            # 检查MongoDB中是否已有数据
            if not force_refresh:
                # 尝试加载所有日期的数据
                for date in sample_dates[:1]:  # 只检查第一个日期
                    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
                    df = self.mongodb_storage.load_fundamentals("indicator", period_key=period_key, date=date_str)
                    if df is not None and not df.empty:
                        indicator_df = df
                        break
                if indicator_df is not None and not indicator_df.empty:
                    if self.verbose:
                        print(f"   ✅ 财务指标已从MongoDB加载")
                    cache_paths["indicator"] = "mongodb"
        
        if indicator_df is None or indicator_df.empty:
            # 从文件检查
            indicator_cache = self.cache_dir / "fundamentals/indicator" / f"{period_key}_indicator.parquet"
            if indicator_cache.exists() and not force_refresh:
                if self.verbose:
                    print(f"   ✅ 财务指标缓存已存在")
                cache_paths["indicator"] = indicator_cache
            else:
                # 下载数据
                indicator_dfs = []
                tasks = []
                for date in sample_dates:
                    for chunk in chunks:
                        tasks.append({
                            "codes": chunk,
                            "date": date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date),
                            "data_type": "indicator"
                        })
                
                with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(_fetch_fundamentals_worker, task) for task in tasks]
                    with tqdm(total=len(futures), desc="下载财务指标", disable=not self.verbose) as pbar:
                        for future in as_completed(futures):
                            try:
                                df = future.result()
                                if df is not None and not df.empty:
                                    indicator_dfs.append(df)
                            except Exception as e:
                                logger.warning(f"财务指标下载失败: {e}")
                            pbar.update(1)
                
                if indicator_dfs:
                    indicator_df = pd.concat(indicator_dfs, ignore_index=True).drop_duplicates()
                    
                    # 保存到MongoDB
                    if self.use_mongodb and self.mongodb_storage:
                        # 按日期保存
                        for date in sample_dates:
                            date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
                            date_df = indicator_df[indicator_df.get("date", pd.Series()).astype(str) == date_str] if "date" in indicator_df.columns else indicator_df
                            if not date_df.empty:
                                self.mongodb_storage.save_fundamentals(date_df, "indicator", period_key, date_str)
                        cache_paths["indicator"] = "mongodb"
                        if self.verbose:
                            print(f"   ✅ 财务指标已保存到MongoDB: {len(indicator_df)}条")
                    else:
                        # 文件存储
                        indicator_df.to_parquet(indicator_cache, index=False)
                        cache_paths["indicator"] = indicator_cache
                        if self.verbose:
                            print(f"   ✅ 财务指标已保存: {indicator_cache}")
        
        return cache_paths
    
    def preload_index_data(
        self,
        start_date: str,
        end_date: str,
        indices: List[str] = None,
        force_refresh: bool = False
    ) -> Dict[str, Path]:
        """
        预加载指数数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            indices: 指数列表（默认沪深300、中证500）
            force_refresh: 强制刷新
        
        Returns:
            缓存路径字典
        """
        if indices is None:
            indices = ["000300.XSHG", "000905.XSHG", "000001.XSHG"]  # 沪深300、中证500、上证指数
        
        if self.verbose:
            print(f"\n📊 下载指数数据...")
        
        cache_paths = {}
        period_key = self._get_period_key(start_date, end_date)
        
        with ProcessPoolExecutor(max_workers=min(self.max_workers, len(indices))) as executor:
            futures = {
                executor.submit(
                    _fetch_index_data_worker,
                    {
                        "index_code": index_code,
                        "start_date": start_date,
                        "end_date": end_date
                    }
                ): index_code for index_code in indices
            }
            
            for future in as_completed(futures):
                index_code = futures[future]
                try:
                    df = future.result()
                    if df is not None and not df.empty:
                        cache_path = self.cache_dir / "indices" / f"{period_key}_{index_code.replace('.', '_')}.parquet"
                        df.to_parquet(cache_path, index=False)
                        cache_paths[index_code] = cache_path
                        if self.verbose:
                            print(f"   ✅ {index_code} 已保存")
                except Exception as e:
                    logger.warning(f"指数 {index_code} 下载失败: {e}")
        
        return cache_paths
    
    def load_cached_prices(self, period_key: str) -> Optional[pd.DataFrame]:
        """从缓存加载价格数据（优先MongoDB）"""
        # 优先从MongoDB加载
        if self.use_mongodb and self.mongodb_storage:
            df = self.mongodb_storage.load_daily_prices(period_key=period_key)
            if df is not None and not df.empty:
                return df
        
        # 从文件加载
        cache_path = self.cache_dir / "daily_prices" / f"{period_key}_prices.parquet"
        if cache_path.exists():
            return pd.read_parquet(cache_path)
        return None
    
    def load_cached_fundamentals(self, period_key: str, data_type: str = "valuation") -> Optional[pd.DataFrame]:
        """从缓存加载基本面数据"""
        cache_path = self.cache_dir / f"fundamentals/{data_type}" / f"{period_key}_{data_type}.parquet"
        if cache_path.exists():
            return pd.read_parquet(cache_path)
        return None
    
    def load_cached_index(self, period_key: str, index_code: str) -> Optional[pd.DataFrame]:
        """从缓存加载指数数据"""
        cache_path = self.cache_dir / "indices" / f"{period_key}_{index_code.replace('.', '_')}.parquet"
        if cache_path.exists():
            return pd.read_parquet(cache_path)
        return None
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        info = {
            "cache_dir": str(self.cache_dir),
            "metadata": self._metadata,
            "cached_files": {}
        }
        
        # 统计各类型缓存
        for subdir in ["daily_prices", "fundamentals", "indices"]:
            subdir_path = self.cache_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.rglob("*.parquet"))
                total_size = sum(f.stat().st_size for f in files)
                info["cached_files"][subdir] = {
                    "count": len(files),
                    "size_mb": total_size / (1024 * 1024)
                }
        
        return info
    
    def _cache_trade_days(
        self,
        start_date: str,
        end_date: str,
        period_key: str,
        force_refresh: bool = False
    ) -> Dict[str, Union[Path, str]]:
        """缓存交易日数据（避免BulletTrade引擎调用get_trade_days API）"""
        # 优先从MongoDB加载
        if self.use_mongodb and self.mongodb_storage:
            if not force_refresh:
                trade_days_str = self.mongodb_storage.load_trade_days(period_key=period_key)
                if trade_days_str:
                    if self.verbose:
                        print(f"   ✅ 交易日数据已从MongoDB加载: {len(trade_days_str)}天")
                    return {"trade_days": "mongodb", "trade_days_list": trade_days_str}
        
        # 获取交易日数据
        try:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(JQDATA_USER, JQDATA_PASSWORD)
            
            trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
            trade_days_str = [d.strftime('%Y-%m-%d') if isinstance(d, datetime) else str(d) for d in trade_days]
            
            # 保存到MongoDB
            if self.use_mongodb and self.mongodb_storage:
                self.mongodb_storage.save_trade_days(trade_days, period_key, start_date, end_date)
                if self.verbose:
                    print(f"   ✅ 交易日数据已保存到MongoDB: {len(trade_days)}天")
                return {"trade_days": "mongodb", "trade_days_list": trade_days_str}
            else:
                # 文件存储
                cache_file = self.cache_dir / "trade_days" / f"{period_key}_trade_days.parquet"
                trade_days_df = pd.DataFrame({
                    'date': trade_days_str,
                    'datetime': trade_days
                })
                trade_days_df.to_parquet(cache_file, index=False)
                if self.verbose:
                    print(f"   ✅ 交易日数据已缓存: {len(trade_days)}天 -> {cache_file.name}")
                return {"trade_days": cache_file, "trade_days_list": trade_days_str}
        except Exception as e:
            logger.warning(f"缓存交易日数据失败: {e}")
            return {}
    
    def clear_cache(self, period_key: str = None):
        """清除缓存"""
        if period_key:
            # 清除指定时间段的缓存
            for path in self.cache_dir.rglob(f"*{period_key}*"):
                if path.is_file():
                    path.unlink()
            if period_key in self._metadata["cached_periods"]:
                del self._metadata["cached_periods"][period_key]
            self._save_metadata()
        else:
            # 清除所有缓存
            import shutil
            for subdir in ["daily_prices", "fundamentals", "indices"]:
                subdir_path = self.cache_dir / subdir
                if subdir_path.exists():
                    shutil.rmtree(subdir_path)
            self._init_cache_dirs()
            self._metadata = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "cached_periods": {},
                "last_update": None
            }
            self._save_metadata()


# 便捷函数
def preload_6month_data(
    start_date: str = "2024-07-01",
    end_date: str = "2024-12-31",
    cache_dir: str = "data/cache",
    force_refresh: bool = False
) -> PreloadResult:
    """
    预加载半年数据的便捷函数
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        cache_dir: 缓存目录
        force_refresh: 强制刷新
    
    Returns:
        PreloadResult
    """
    preloader = DataPreloader(max_workers=3, cache_dir=cache_dir, verbose=True)
    
    # 预加载市场数据
    result = preloader.preload_market_data(
        start_date=start_date,
        end_date=end_date,
        force_refresh=force_refresh
    )
    
    # 预加载指数数据
    index_paths = preloader.preload_index_data(
        start_date=start_date,
        end_date=end_date,
        force_refresh=force_refresh
    )
    result.cache_paths.update(index_paths)
    
    return result


if __name__ == "__main__":
    # 测试
    result = preload_6month_data(
        start_date="2024-07-01",
        end_date="2024-12-31",
        cache_dir="data/cache",
        force_refresh=False
    )
    
    print(f"\n预加载结果:")
    print(f"  成功: {result.success}")
    print(f"  股票数: {result.total_stocks}")
    print(f"  数据大小: {result.data_size_mb:.1f} MB")
    print(f"  耗时: {result.duration_seconds:.1f} 秒")
