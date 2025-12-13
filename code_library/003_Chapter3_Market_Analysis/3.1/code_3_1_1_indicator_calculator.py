import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class IndicatorCalculator:
    """
    技术指标计算器
    
    **设计原理**：
    - **缓存机制**：缓存计算结果，避免重复计算
    - **统一接口**：所有指标使用相同的接口，简化调用
    - **延迟计算**：按需计算，不预计算所有指标
    
    **为什么这样设计**：
    1. **性能优化**：技术指标计算可能耗时，缓存避免重复计算
    2. **接口统一**：不同指标使用相同接口，便于扩展和维护
    3. **资源节约**：按需计算，不浪费计算资源
    
    **使用场景**：
    - 批量计算多个指标时，缓存提高效率
    - 重复计算相同指标时，直接使用缓存
    - 需要统一管理所有指标计算时
    
    **注意事项**：
    - 缓存键基于参数hash，参数变化时自动重新计算
    - 大量指标时注意内存占用，可设置缓存大小限制
    """
    
    def __init__(self):
        """
        初始化技术指标计算器
        """
        self.indicators = {}
        self._cache = {}
    
    def calculate(self, data: pd.DataFrame, indicator_name: str, **kwargs) -> pd.Series:
        """
        计算技术指标
        
        **设计原理**：
        - **缓存键生成**：使用指标名称和参数生成唯一缓存键
        - **策略模式**：根据指标名称选择相应计算方法
        - **结果缓存**：计算结果缓存，提高后续调用效率
        
        **为什么这样设计**：
        1. **性能优化**：相同参数的计算结果缓存，避免重复计算
        2. **扩展性**：新增指标只需添加一个分支，无需修改现有代码
        3. **一致性**：所有指标使用相同接口，调用方式统一
        
        **使用场景**：
        - 批量计算多个指标时，缓存提高效率
        - 重复计算相同指标时，直接使用缓存
        - 需要统一管理所有指标计算时
        
        **注意事项**：
        - 缓存键基于参数hash，参数变化时自动重新计算
        - 大量指标时注意内存占用，可设置缓存大小限制
        
        Args:
            data: 价格数据
            indicator_name: 指标名称（SMA, EMA, MACD, RSI, BB等）
            **kwargs: 指标参数
        
        Returns:
            指标序列
        """
        # 设计原理：使用指标名称和参数生成唯一缓存键
        # 原因：相同指标和参数的计算结果相同，可以复用
        # 为什么这样设计：避免重复计算，提高性能
        cache_key = f"{indicator_name}_{hash(str(kwargs))}"
        
        # 检查缓存
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 设计原理：策略模式，根据指标名称选择计算方法
        # 原因：不同指标计算逻辑不同，需要分别处理
        # 扩展性：新增指标只需添加一个分支
        # 为什么这样设计：统一接口，便于扩展和维护
        from core.market_analysis.trend_analysis import (
            calculate_sma, calculate_ema, calculate_macd,
            calculate_rsi, calculate_bollinger_bands
        )
        
        if indicator_name.upper() == 'SMA':
            result = calculate_sma(data, **kwargs)
        elif indicator_name.upper() == 'EMA':
            result = calculate_ema(data, **kwargs)
        elif indicator_name.upper() == 'MACD':
            result = calculate_macd(data, **kwargs)
        elif indicator_name.upper() == 'RSI':
            result = calculate_rsi(data, **kwargs)
        elif indicator_name.upper() == 'BB':
            result = calculate_bollinger_bands(data, **kwargs)
        else:
            raise ValueError(f"不支持的指标: {indicator_name}")
        
        # 设计原理：计算结果缓存
        # 原因：相同参数的计算结果可以复用，提高后续调用效率
        # 为什么这样设计：避免重复计算，提高性能
        self._cache[cache_key] = result
        return result
    
    def calculate_multiple(self, data: pd.DataFrame, 
                          indicators: List[Dict]) -> pd.DataFrame:
        """
        批量计算多个指标
        
        **设计原理**：
        - **批量处理**：一次性计算多个指标，提高效率
        - **结果合并**：将多个指标结果合并为DataFrame
        - **命名规范**：指标名称和列名统一规范
        
        **为什么这样设计**：
        1. **效率提升**：批量计算比逐个计算更高效
        2. **结果统一**：所有指标结果在一个DataFrame中，便于使用
        3. **命名清晰**：指标名称和列名清晰，便于识别
        
        **使用场景**：
        - 需要同时计算多个指标时
        - 指标结果需要统一管理时
        - 批量分析时
        
        Args:
            data: 价格数据
            indicators: 指标配置列表，每个元素为 {'name': 'SMA', 'period': 20}
        
        Returns:
            包含所有指标的DataFrame
        """
        # 设计原理：遍历指标配置，逐个计算
        # 原因：每个指标可能有不同的参数，需要分别处理
        # 为什么这样设计：灵活支持不同指标的参数配置
        results = {}
        for indicator in indicators:
            name = indicator['name']
            params = {k: v for k, v in indicator.items() if k != 'name'}
            result = self.calculate(data, name, **params)
            
            # 设计原理：处理DataFrame和Series两种返回类型
            # 原因：不同指标可能返回不同类型（如MACD返回DataFrame，SMA返回Series）
            # 为什么这样设计：统一处理不同类型的返回值
            if isinstance(result, pd.DataFrame):
                for col in result.columns:
                    results[f"{name}_{col}"] = result[col]
            else:
                results[name] = result
        
        return pd.DataFrame(results)

