# -*- coding: utf-8 -*-
"""
因子计算模块 - 研究/回测用
===========================

功能：
1. 优先使用JQData因子库（CNE5/Alpha101/基本面因子）
2. 自定义因子使用向量化计算（可GPU加速）
3. 输出标准化矩阵格式（T x N）

牛市策略核心因子：
- mom_20d: 20日动量 (close[-1] / close[-21] - 1) * 100
- mom_5d: 5日动量
- rel_position: 相对位置 (close - low_20) / (high_20 - low_20) * 100
- vol_ratio: 量比 volume / volume.rolling(20).mean()
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import os
import hashlib
from pathlib import Path
from datetime import datetime
import json

import pandas as pd
import numpy as np

from .data_provider import DataMatrices

logger = logging.getLogger(__name__)

# JQData认证信息
JQDATA_USER = os.environ.get("JQDATA_USER", "13327806797")
JQDATA_PASSWORD = os.environ.get("JQDATA_PASSWORD", "Taorui888")


@dataclass
class FactorMatrices:
    """因子矩阵容器
    
    所有矩阵格式: DataFrame(index=datetime, columns=symbol)
    """
    # 自定义动量因子
    mom_20d: Optional[pd.DataFrame] = None  # 20日动量
    mom_5d: Optional[pd.DataFrame] = None   # 5日动量
    
    # 自定义技术因子
    rel_position: Optional[pd.DataFrame] = None  # 相对位置
    vol_ratio: Optional[pd.DataFrame] = None     # 量比
    vol_ratio_5d: Optional[pd.DataFrame] = None  # 5日量比
    
    # 涨停因子（牛市策略核心）
    is_limit_up: Optional[pd.DataFrame] = None        # 当日涨停（布尔）
    limit_up_count_5d: Optional[pd.DataFrame] = None  # 近5日涨停次数
    is_first_limit_up: Optional[pd.DataFrame] = None  # 首板信号（布尔）
    limit_up_vol_ratio: Optional[pd.DataFrame] = None # 涨停当日量比
    
    # 突破因子
    breakout_60d: Optional[pd.DataFrame] = None       # 突破60日高点（布尔）
    breakout_ratio: Optional[pd.DataFrame] = None     # 突破幅度（%）
    
    # 资金流向因子
    main_flow: Optional[pd.DataFrame] = None          # 主力资金流向
    flow_strength: Optional[pd.DataFrame] = None      # 资金流向强度
    
    # JQData因子库（可选）
    size: Optional[pd.DataFrame] = None          # 市值因子
    momentum: Optional[pd.DataFrame] = None      # CNE5动量
    liquidity: Optional[pd.DataFrame] = None     # 流动性
    volatility: Optional[pd.DataFrame] = None    # 波动率
    
    # 基本面因子（可选）
    roe: Optional[pd.DataFrame] = None           # ROE
    pe: Optional[pd.DataFrame] = None            # PE
    pb: Optional[pd.DataFrame] = None            # PB
    
    def to_dict(self) -> Dict[str, pd.DataFrame]:
        """转换为字典（只包含非None的因子）"""
        result = {}
        for name, value in self.__dict__.items():
            if value is not None:
                result[name] = value
        return result
    
    @property
    def available_factors(self) -> List[str]:
        """获取可用因子列表"""
        return [name for name, value in self.__dict__.items() if value is not None]


class FactorCalculator:
    """因子计算器
    
    支持两种计算模式：
    1. 向量化计算：使用NumPy/Pandas对矩阵直接操作（默认）
    2. GPU加速：使用PyTorch批量计算（大规模数据时自动启用）
    
    使用示例：
    ```python
    calculator = FactorCalculator()
    factors = calculator.calculate_factors(
        data_matrices,
        factor_list=["mom_20d", "rel_position", "vol_ratio"]
    )
    print(factors.mom_20d.shape)  # (T, N)
    ```
    """
    
    def __init__(
        self,
        use_gpu: bool = True,
        gpu_threshold: int = 100,  # 超过此数量的股票启用GPU
        use_cache: bool = True,
        cache_dir: Optional[Path] = None,
    ):
        """
        初始化因子计算器
        
        Args:
            use_gpu: 是否启用GPU加速
            gpu_threshold: 启用GPU的股票数量阈值
            use_cache: 是否使用因子缓存
            cache_dir: 缓存目录（默认：data/research_cache/factors）
        """
        self.use_gpu = use_gpu
        self.gpu_threshold = gpu_threshold
        self.use_cache = use_cache
        
        # 设置缓存目录
        if cache_dir is None:
            project_root = Path(__file__).parent.parent.parent
            cache_dir = project_root / "data" / "research_cache" / "factors"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 检测GPU可用性
        self._gpu_available = False
        if use_gpu:
            try:
                import torch
                self._gpu_available = torch.cuda.is_available()
                if self._gpu_available:
                    logger.info(f"✅ GPU加速可用: {torch.cuda.get_device_name(0)}")
            except ImportError:
                logger.warning("PyTorch未安装，GPU加速不可用")
        
        self._jq = None
        self._jq_factor_loader = None
    
    def _get_jq(self):
        """获取JQData连接（懒加载）"""
        if self._jq is None:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(JQDATA_USER, JQDATA_PASSWORD)
            self._jq = jq
        return self._jq
    
    def _get_factor_cache_key(
        self,
        factors: List[str],
        symbols: List[str],
        start_date: str,
        end_date: str,
    ) -> str:
        """生成因子缓存键"""
        # 因子列表排序并哈希
        factors_sorted = sorted(factors)
        factors_str = "_".join(factors_sorted)
        factors_hash = hashlib.md5(factors_str.encode()).hexdigest()[:12]
        
        # 股票列表排序并哈希
        symbols_sorted = sorted(symbols)
        symbols_str = "_".join(symbols_sorted)
        symbols_hash = hashlib.md5(symbols_str.encode()).hexdigest()[:12]
        
        # 组合缓存键
        cache_key = f"factors_{factors_hash}_{symbols_hash}_{start_date}_{end_date}"
        return cache_key
    
    def _load_factor_cache(
        self,
        cache_key: str,
        factors: List[str],
    ) -> Optional[Dict[str, pd.DataFrame]]:
        """从缓存加载因子数据"""
        cache_dir = self.cache_dir / cache_key
        if not cache_dir.exists():
            return None
        
        # 检查元数据文件
        meta_path = cache_dir / "meta.json"
        if not meta_path.exists():
            return None
        
        try:
            # 加载元数据
            with open(meta_path, "r") as f:
                meta = json.load(f)
            
            # 检查因子列表是否匹配
            cached_factors = set(meta.get("factors", []))
            requested_factors = set(factors)
            if cached_factors != requested_factors:
                logger.debug(f"缓存因子列表不匹配，重新加载")
                return None
            
            # 加载各个因子
            result = {}
            for factor_name in factors:
                factor_path = cache_dir / f"{factor_name}.parquet"
                if factor_path.exists():
                    result[factor_name] = pd.read_parquet(factor_path)
                else:
                    logger.warning(f"缓存中缺少因子 {factor_name}，重新加载")
                    return None
            
            logger.info(f"✅ 从缓存加载 {len(result)} 个聚宽因子: {cache_key}")
            return result
        except Exception as e:
            logger.warning(f"加载因子缓存失败: {e}")
            return None
    
    def _save_factor_cache(
        self,
        cache_key: str,
        factor_dict: Dict[str, pd.DataFrame],
        factors: List[str],
    ):
        """保存因子数据到缓存"""
        cache_dir = self.cache_dir / cache_key
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 保存元数据
            meta = {
                "factors": factors,
                "factor_count": len(factor_dict),
                "created_at": datetime.now().isoformat(),
            }
            meta_path = cache_dir / "meta.json"
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)
            
            # 保存各个因子（Parquet格式）
            for factor_name, factor_df in factor_dict.items():
                factor_path = cache_dir / f"{factor_name}.parquet"
                factor_df.to_parquet(factor_path)
            
            logger.info(f"✅ 因子已缓存: {cache_key}, {len(factor_dict)} 个因子")
        except Exception as e:
            logger.warning(f"保存因子缓存失败: {e}")
    
    def load_jqdata_factors(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        factors: Optional[List[str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        直接从聚宽因子库加载因子（无需自己计算！）
        
        聚宽因子库有276个现成因子，包括：
        - CNE5风格因子: size, beta, momentum, liquidity, residual_volatility
        - 质量因子(71个): roe_ttm, roa_ttm, gross_income_ratio等
        - 动量因子(34个): REVS5, REVS10, REVS20等
        - 情绪因子(36个): VOL20, turnover_volatility等
        - 成长因子(9个): net_profit_growth_rate, operating_revenue_growth_rate等
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            factors: 要加载的因子列表（默认CNE5 + 常用质量/动量因子）
        
        Returns:
            因子字典 {factor_name: DataFrame(T x N)}
        """
        if factors is None:
            # 默认加载最有用的因子（276个现成因子可选）
            factors = [
                # CNE5风格因子（必选，5个）
                "size", "beta", "momentum", "liquidity", "residual_volatility",
                # 质量因子（选用）
                "roe_ttm", "roa_ttm", "gross_income_ratio",
                # 动量因子（正确名称）
                "ROC6", "ROC12", "ROC20", "ROC60",  # 变动速率
                "Price1M", "Price3M",  # 价格动量
                # 估值因子
                "PEG",
                # 成长因子
                "net_profit_growth_rate", "operating_revenue_growth_rate",
                # 技术因子
                "VOL20",  # 换手率
                "BIAS20",  # 乖离率
            ]
        
        # 检查缓存
        if self.use_cache:
            cache_key = self._get_factor_cache_key(factors, symbols, start_date, end_date)
            cached_result = self._load_factor_cache(cache_key, factors)
            if cached_result is not None:
                return cached_result
        
        # 从聚宽因子库加载
        jq = self._get_jq()
        result = {}
        
        logger.info(f"📊 从聚宽因子库加载 {len(factors)} 个因子...")
        
        # 批量获取因子值
        try:
            factor_values = jq.get_factor_values(
                securities=symbols,
                factors=factors,
                start_date=start_date,
                end_date=end_date,
            )
            
            # 转换为标准格式
            for factor_name, df in factor_values.items():
                if df is not None and not df.empty:
                    # JQData返回格式: index=日期, columns=股票代码
                    result[factor_name] = df.reindex(columns=symbols)
                    logger.debug(f"  ✅ {factor_name}: {df.shape}")
            
            logger.info(f"✅ 成功加载 {len(result)} 个聚宽因子")
            
            # 保存到缓存
            if self.use_cache and result:
                cache_key = self._get_factor_cache_key(factors, symbols, start_date, end_date)
                self._save_factor_cache(cache_key, result, factors)
        except Exception as e:
            logger.error(f"❌ 加载聚宽因子库失败: {e}")
        
        return result
    
    def calculate_factors_with_jqdata(
        self,
        data: DataMatrices,
        jq_factor_list: Optional[List[str]] = None,
        custom_factor_list: Optional[List[str]] = None,
    ) -> FactorMatrices:
        """
        混合计算因子：聚宽因子库 + 自定义因子
        
        优先使用聚宽因子库（276个现成因子），自定义因子作为补充
        
        Args:
            data: 数据矩阵
            jq_factor_list: 要从聚宽因子库加载的因子列表
            custom_factor_list: 要自己计算的自定义因子列表
        
        Returns:
            FactorMatrices: 因子矩阵
        """
        factors = FactorMatrices()
        
        # 1. 加载聚宽因子库的因子（直接获取，无需计算！）
        if jq_factor_list:
            symbols = list(data.close.columns)
            start_date = data.close.index[0].strftime('%Y-%m-%d')
            end_date = data.close.index[-1].strftime('%Y-%m-%d')
            
            jq_factors = self.load_jqdata_factors(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                factors=jq_factor_list,
            )
            
            # 将聚宽因子存入FactorMatrices（通用方式，支持所有因子）
            for factor_name, factor_df in jq_factors.items():
                # 直接映射到FactorMatrices属性（如果存在）
                if hasattr(factors, factor_name):
                    setattr(factors, factor_name, factor_df)
                # 特殊映射
                elif factor_name == "size":
                    factors.size = factor_df
                elif factor_name == "momentum":
                    factors.momentum = factor_df
                elif factor_name == "liquidity":
                    factors.liquidity = factor_df
                elif factor_name in ["residual_volatility", "volatility"]:
                    factors.volatility = factor_df
                elif factor_name == "roe_ttm":
                    factors.roe = factor_df
                elif factor_name.startswith("ROC"):
                    # ROC系列因子可以作为momentum的补充
                    if factors.momentum is None:
                        factors.momentum = factor_df
                elif factor_name.startswith("Price"):
                    # Price系列因子可以作为momentum的补充
                    if factors.momentum is None:
                        factors.momentum = factor_df
        
        # 2. 计算自定义因子（仅限聚宽没有的因子）
        if custom_factor_list:
            custom_factors = self.calculate_factors(data, factor_list=custom_factor_list)
            # 合并
            for attr in dir(custom_factors):
                if not attr.startswith('_') and attr not in ['to_dict', 'available_factors']:
                    value = getattr(custom_factors, attr)
                    if value is not None:
                        setattr(factors, attr, value)
        
        logger.info(f"✅ 混合因子计算完成: {factors.available_factors}")
        return factors
    
    def calculate_factors(
        self,
        data: DataMatrices,
        factor_list: Optional[List[str]] = None,
    ) -> FactorMatrices:
        """
        计算因子矩阵
        
        Args:
            data: 数据矩阵（DataMatrices）
            factor_list: 要计算的因子列表，默认为牛市策略完整因子
        
        Returns:
            FactorMatrices: 因子矩阵
        """
        if factor_list is None:
            # 牛市策略完整因子列表
            factor_list = [
                # 动量因子
                "mom_20d", "mom_5d", "rel_position",
                # 量价因子
                "vol_ratio", "vol_ratio_5d",
                # 涨停因子
                "is_limit_up", "limit_up_count_5d", "is_first_limit_up", "limit_up_vol_ratio",
                # 突破因子
                "breakout_60d", "breakout_ratio",
                # 资金流向因子
                "main_flow", "flow_strength",
            ]
        
        factors = FactorMatrices()
        
        # 预计算一些基础因子（供其他因子使用）
        vol_ratio = None
        is_limit_up = None
        
        for factor_name in factor_list:
            try:
                if factor_name == "mom_20d":
                    factors.mom_20d = self._calc_momentum(data.close, period=20)
                elif factor_name == "mom_5d":
                    factors.mom_5d = self._calc_momentum(data.close, period=5)
                elif factor_name == "rel_position":
                    factors.rel_position = self._calc_rel_position(data.close, period=20)
                elif factor_name == "vol_ratio":
                    vol_ratio = self._calc_vol_ratio(data.volume, period=20)
                    factors.vol_ratio = vol_ratio
                elif factor_name == "vol_ratio_5d":
                    factors.vol_ratio_5d = self._calc_vol_ratio(data.volume, period=5)
                
                # 涨停因子
                elif factor_name == "is_limit_up":
                    is_limit_up = self._calc_is_limit_up(data.close)
                    factors.is_limit_up = is_limit_up
                elif factor_name == "limit_up_count_5d":
                    if is_limit_up is None:
                        is_limit_up = self._calc_is_limit_up(data.close)
                    factors.limit_up_count_5d = self._calc_limit_up_count(is_limit_up, period=5)
                elif factor_name == "is_first_limit_up":
                    if is_limit_up is None:
                        is_limit_up = self._calc_is_limit_up(data.close)
                    factors.is_first_limit_up = self._calc_is_first_limit_up(is_limit_up, lookback=30)
                elif factor_name == "limit_up_vol_ratio":
                    if is_limit_up is None:
                        is_limit_up = self._calc_is_limit_up(data.close)
                    if vol_ratio is None:
                        vol_ratio = self._calc_vol_ratio(data.volume, period=20)
                    factors.limit_up_vol_ratio = self._calc_limit_up_vol_ratio(is_limit_up, vol_ratio)
                
                # 突破因子
                elif factor_name == "breakout_60d":
                    factors.breakout_60d = self._calc_breakout(data.close, data.high, period=60)
                elif factor_name == "breakout_ratio":
                    factors.breakout_ratio = self._calc_breakout_ratio(data.close, data.high, period=60)
                
                # 资金流向因子
                elif factor_name == "main_flow":
                    factors.main_flow = self._calc_main_flow(data.close, data.high, data.low, data.amount)
                elif factor_name == "flow_strength":
                    if factors.main_flow is None:
                        factors.main_flow = self._calc_main_flow(data.close, data.high, data.low, data.amount)
                    factors.flow_strength = self._calc_flow_strength(factors.main_flow, data.amount, period=5)
                
                elif factor_name in ["size", "momentum", "liquidity", "volatility", "residual_volatility", "beta"]:
                    # 直接使用JQData因子库 - 276个现成因子，无需自己计算
                    logger.debug(f"使用JQData因子库: {factor_name}")
                    # 在calculate_factors_with_jqdata中统一加载
                else:
                    logger.warning(f"未知因子: {factor_name}")
            except Exception as e:
                logger.error(f"计算因子 {factor_name} 失败: {e}")
        
        logger.info(f"因子计算完成: {factors.available_factors}")
        return factors
    
    def _calc_momentum(
        self,
        close: pd.DataFrame,
        period: int = 20
    ) -> pd.DataFrame:
        """
        计算动量因子
        
        公式: (close[t] / close[t-period] - 1) * 100
        
        Args:
            close: 收盘价矩阵 (T x N)
            period: 周期
        
        Returns:
            动量矩阵 (T x N)
        """
        momentum = (close / close.shift(period) - 1) * 100
        return momentum
    
    def _calc_rel_position(
        self,
        close: pd.DataFrame,
        period: int = 20
    ) -> pd.DataFrame:
        """
        计算相对位置因子
        
        公式: (close - rolling_min) / (rolling_max - rolling_min + eps) * 100
        
        Args:
            close: 收盘价矩阵 (T x N)
            period: 周期
        
        Returns:
            相对位置矩阵 (T x N)，范围 [0, 100]
        """
        rolling_min = close.rolling(window=period, min_periods=1).min()
        rolling_max = close.rolling(window=period, min_periods=1).max()
        
        eps = 1e-8
        rel_position = (close - rolling_min) / (rolling_max - rolling_min + eps) * 100
        return rel_position
    
    def _calc_vol_ratio(
        self,
        volume: pd.DataFrame,
        period: int = 20
    ) -> pd.DataFrame:
        """
        计算量比因子
        
        公式: volume / volume.rolling(period).mean()
        
        Args:
            volume: 成交量矩阵 (T x N)
            period: 周期
        
        Returns:
            量比矩阵 (T x N)
        """
        vol_ma = volume.rolling(window=period, min_periods=1).mean()
        vol_ratio = volume / (vol_ma + 1e-8)
        return vol_ratio
    
    # =========================================================================
    # 涨停因子计算
    # =========================================================================
    
    def _calc_is_limit_up(
        self,
        close: pd.DataFrame,
        threshold: float = 0.093,  # 9.3%涨停阈值（已优化）
    ) -> pd.DataFrame:
        """
        计算当日是否涨停
        
        公式: daily_return > threshold
        
        Args:
            close: 收盘价矩阵 (T x N)
            threshold: 涨停阈值（默认9.3%，已从追涨策略优化获得）
        
        Returns:
            涨停布尔矩阵 (T x N)
        """
        daily_return = close / close.shift(1) - 1
        is_limit_up = daily_return > threshold
        return is_limit_up.fillna(False)
    
    def _calc_limit_up_count(
        self,
        is_limit_up: pd.DataFrame,
        period: int = 5,
    ) -> pd.DataFrame:
        """
        计算近N日涨停次数
        
        Args:
            is_limit_up: 涨停布尔矩阵 (T x N)
            period: 统计周期
        
        Returns:
            涨停次数矩阵 (T x N)
        """
        # 将布尔转为整数后滚动求和
        limit_up_int = is_limit_up.astype(int)
        count = limit_up_int.rolling(window=period, min_periods=1).sum()
        return count
    
    def _calc_is_first_limit_up(
        self,
        is_limit_up: pd.DataFrame,
        lookback: int = 30,
    ) -> pd.DataFrame:
        """
        计算是否为首板（近N日首次涨停）
        
        条件: 当日涨停 且 前(lookback-1)日无涨停
        
        Args:
            is_limit_up: 涨停布尔矩阵 (T x N)
            lookback: 回溯周期（默认30日）
        
        Returns:
            首板布尔矩阵 (T x N)
        """
        limit_up_int = is_limit_up.astype(int)
        
        # 前N-1日涨停次数（不包含当日）
        prev_limit_count = limit_up_int.shift(1).rolling(window=lookback-1, min_periods=1).sum()
        
        # 首板条件: 当日涨停 且 前N-1日无涨停
        is_first = is_limit_up & (prev_limit_count == 0)
        return is_first.fillna(False)
    
    def _calc_limit_up_vol_ratio(
        self,
        is_limit_up: pd.DataFrame,
        vol_ratio: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        计算涨停当日量比
        
        公式: vol_ratio if is_limit_up else 0
        
        Args:
            is_limit_up: 涨停布尔矩阵 (T x N)
            vol_ratio: 量比矩阵 (T x N)
        
        Returns:
            涨停量比矩阵 (T x N)
        """
        result = vol_ratio.where(is_limit_up, 0)
        return result
    
    # =========================================================================
    # 突破因子计算
    # =========================================================================
    
    def _calc_breakout(
        self,
        close: pd.DataFrame,
        high: pd.DataFrame,
        period: int = 60,
    ) -> pd.DataFrame:
        """
        计算是否突破N日高点
        
        条件: close > max(high[t-period:t-1])
        
        Args:
            close: 收盘价矩阵 (T x N)
            high: 最高价矩阵 (T x N)
            period: 回溯周期
        
        Returns:
            突破布尔矩阵 (T x N)
        """
        # 前N日最高价（不包含当日）
        prev_high_max = high.shift(1).rolling(window=period, min_periods=1).max()
        
        # 突破条件
        is_breakout = close > prev_high_max
        return is_breakout.fillna(False)
    
    def _calc_breakout_ratio(
        self,
        close: pd.DataFrame,
        high: pd.DataFrame,
        period: int = 60,
    ) -> pd.DataFrame:
        """
        计算突破幅度
        
        公式: (close / prev_high_max - 1) * 100
        
        Args:
            close: 收盘价矩阵 (T x N)
            high: 最高价矩阵 (T x N)
            period: 回溯周期
        
        Returns:
            突破幅度矩阵 (T x N)，单位%
        """
        # 前N日最高价（不包含当日）
        prev_high_max = high.shift(1).rolling(window=period, min_periods=1).max()
        
        # 突破幅度
        breakout_ratio = (close / (prev_high_max + 1e-8) - 1) * 100
        return breakout_ratio
    
    # =========================================================================
    # 资金流向因子计算
    # =========================================================================
    
    def _calc_main_flow(
        self,
        close: pd.DataFrame,
        high: pd.DataFrame,
        low: pd.DataFrame,
        amount: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        计算主力资金流向（价量估算法）
        
        公式: main_flow = (price_position - 0.5) * amount
        其中 price_position = (close - low) / (high - low)
        
        逻辑：
        - price_position > 0.5: 收盘价偏向高位，视为资金流入
        - price_position < 0.5: 收盘价偏向低位，视为资金流出
        
        Args:
            close: 收盘价矩阵 (T x N)
            high: 最高价矩阵 (T x N)
            low: 最低价矩阵 (T x N)
            amount: 成交额矩阵 (T x N)
        
        Returns:
            主力资金流向矩阵 (T x N)
        """
        # 价格位置 [0, 1]
        price_range = high - low + 1e-8
        price_position = (close - low) / price_range
        
        # 资金流向 = (价格位置 - 0.5) * 成交额
        main_flow = (price_position - 0.5) * amount
        return main_flow
    
    def _calc_flow_strength(
        self,
        main_flow: pd.DataFrame,
        amount: pd.DataFrame,
        period: int = 5,
    ) -> pd.DataFrame:
        """
        计算资金流向强度
        
        公式: flow_strength = sum(main_flow[period]) / mean(amount[period])
        
        Args:
            main_flow: 主力资金流向矩阵 (T x N)
            amount: 成交额矩阵 (T x N)
            period: 统计周期
        
        Returns:
            资金流向强度矩阵 (T x N)
        """
        # N日主力资金流向累计
        flow_sum = main_flow.rolling(window=period, min_periods=1).sum()
        
        # N日成交额均值
        amount_mean = amount.rolling(window=period, min_periods=1).mean()
        
        # 资金流向强度
        flow_strength = flow_sum / (amount_mean + 1e-8)
        return flow_strength
    
    def calculate_composite_score(
        self,
        factors: FactorMatrices,
        weights: Optional[Dict[str, float]] = None,
    ) -> pd.DataFrame:
        """
        计算综合评分
        
        Args:
            factors: 因子矩阵
            weights: 因子权重字典，默认等权
        
        Returns:
            综合评分矩阵 (T x N)
        """
        available = factors.to_dict()
        if not available:
            raise ValueError("没有可用的因子")
        
        if weights is None:
            weights = {name: 1.0 / len(available) for name in available}
        
        # 标准化各因子（zscore）
        normalized = {}
        for name, df in available.items():
            # 按行（每天）标准化
            mean = df.mean(axis=1)
            std = df.std(axis=1)
            normalized[name] = df.sub(mean, axis=0).div(std + 1e-8, axis=0)
        
        # 加权求和
        score = pd.DataFrame(0.0, index=list(available.values())[0].index, 
                            columns=list(available.values())[0].columns)
        total_weight = 0
        
        for name, df in normalized.items():
            weight = weights.get(name, 0)
            score = score + df * weight
            total_weight += weight
        
        if total_weight > 0:
            score = score / total_weight
        
        return score


class JQFactorLoader:
    """JQData因子库加载器
    
    加载聚宽因子库中的因子，转换为矩阵格式
    """
    
    def __init__(self):
        self._jq = None
    
    def _get_jq(self):
        """获取JQData连接"""
        if self._jq is None:
            import jqdatasdk as jq
            if not jq.is_auth():
                jq.auth(JQDATA_USER, JQDATA_PASSWORD)
            self._jq = jq
        return self._jq
    
    def load_cne5_factors(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        factors: Optional[List[str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        加载CNE5风格因子
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            factors: 要加载的因子列表
        
        Returns:
            因子字典 {factor_name: DataFrame(T x N)}
        """
        if factors is None:
            factors = ["size", "beta", "momentum", "liquidity", "residual_volatility"]
        
        jq = self._get_jq()
        
        # 获取因子值
        factor_values = jq.get_factor_values(
            securities=symbols,
            factors=factors,
            start_date=start_date,
            end_date=end_date,
        )
        
        # 转换为标准格式
        result = {}
        for factor_name, df in factor_values.items():
            if df is not None and not df.empty:
                # JQData返回格式: index=日期, columns=股票代码
                result[factor_name] = df.reindex(columns=symbols)
        
        return result
    
    def load_fundamental_factors(
        self,
        symbols: List[str],
        date: str,
    ) -> Dict[str, pd.Series]:
        """
        加载基本面因子（单日截面）
        
        Args:
            symbols: 股票代码列表
            date: 日期
        
        Returns:
            因子字典 {factor_name: Series(index=symbol)}
        """
        jq = self._get_jq()
        from jqdatasdk import query, valuation, indicator
        
        result = {}
        
        # 估值因子
        try:
            q = query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                valuation.pb_ratio,
            ).filter(valuation.code.in_(symbols))
            
            df = jq.get_fundamentals(q, date=date)
            if df is not None and not df.empty:
                df = df.set_index("code")
                result["market_cap"] = df["market_cap"].reindex(symbols)
                result["pe"] = df["pe_ratio"].reindex(symbols)
                result["pb"] = df["pb_ratio"].reindex(symbols)
        except Exception as e:
            logger.warning(f"获取估值因子失败: {e}")
        
        # 质量因子
        try:
            q = query(
                indicator.code,
                indicator.roe,
            ).filter(indicator.code.in_(symbols))
            
            df = jq.get_fundamentals(q, date=date)
            if df is not None and not df.empty:
                df = df.set_index("code")
                result["roe"] = df["roe"].reindex(symbols)
        except Exception as e:
            logger.warning(f"获取质量因子失败: {e}")
        
        return result


# 便捷函数
def get_factor_calculator(use_gpu: bool = True) -> FactorCalculator:
    """获取因子计算器"""
    return FactorCalculator(use_gpu=use_gpu)
