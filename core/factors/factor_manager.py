# -*- coding: utf-8 -*-
"""
因子管理器
==========

提供因子的统一管理功能：
- 因子注册和查询
- 批量计算
- 多因子组合
- PTrade策略代码生成
- 因子有效性评估
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Union, Type
from datetime import datetime, timedelta
from pathlib import Path
import logging
import json

from .base_factor import BaseFactor, FactorResult
from .value_factors import (
    EPFactor, BPFactor, SPFactor, DividendYieldFactor, CompositeValueFactor
)
from .growth_factors import (
    RevenueGrowthFactor, ProfitGrowthFactor, ROEChangeFactor, CompositeGrowthFactor
)
from .quality_factors import (
    ROEFactor, GrossMarginFactor, AssetTurnoverFactor, LeverageFactor, CompositeQualityFactor
)
from .momentum_factors import (
    PriceMomentumFactor, ReversalFactor, RelativeStrengthFactor, CompositeMomentumFactor
)
from .flow_factors import (
    NorthboundFlowFactor, MainForceFlowFactor, MarginBalanceFactor, CompositeFlowFactor
)

logger = logging.getLogger(__name__)


class FactorManager:
    """
    因子管理器
    
    提供因子的统一管理、计算和组合功能。
    """
    
    # 预定义因子类映射
    FACTOR_CLASSES: Dict[str, Type[BaseFactor]] = {
        # 价值因子
        'EP': EPFactor,
        'BP': BPFactor,
        'SP': SPFactor,
        'DividendYield': DividendYieldFactor,
        'CompositeValue': CompositeValueFactor,
        
        # 成长因子
        'RevenueGrowth': RevenueGrowthFactor,
        'ProfitGrowth': ProfitGrowthFactor,
        'ROEChange': ROEChangeFactor,
        'CompositeGrowth': CompositeGrowthFactor,
        
        # 质量因子
        'ROE': ROEFactor,
        'GrossMargin': GrossMarginFactor,
        'AssetTurnover': AssetTurnoverFactor,
        'Leverage': LeverageFactor,
        'CompositeQuality': CompositeQualityFactor,
        
        # 动量因子
        'PriceMomentum': PriceMomentumFactor,
        'Reversal': ReversalFactor,
        'RelativeStrength': RelativeStrengthFactor,
        'CompositeMomentum': CompositeMomentumFactor,
        
        # 资金流因子
        'NorthboundFlow': NorthboundFlowFactor,
        'MainForceFlow': MainForceFlowFactor,
        'MarginBalance': MarginBalanceFactor,
        'CompositeFlow': CompositeFlowFactor,
    }
    
    # 因子分类
    FACTOR_CATEGORIES = {
        'value': ['EP', 'BP', 'SP', 'DividendYield', 'CompositeValue'],
        'growth': ['RevenueGrowth', 'ProfitGrowth', 'ROEChange', 'CompositeGrowth'],
        'quality': ['ROE', 'GrossMargin', 'AssetTurnover', 'Leverage', 'CompositeQuality'],
        'momentum': ['PriceMomentum', 'Reversal', 'RelativeStrength', 'CompositeMomentum'],
        'flow': ['NorthboundFlow', 'MainForceFlow', 'MarginBalance', 'CompositeFlow'],
    }
    
    def __init__(
        self,
        jq_client=None,
        cache_dir: Optional[Path] = None,
        use_cache: bool = True
    ):
        """
        初始化因子管理器
        
        Args:
            jq_client: JQData客户端
            cache_dir: 缓存目录
            use_cache: 是否使用缓存
        """
        self.jq_client = jq_client
        self.cache_dir = cache_dir or Path(__file__).parent.parent.parent / "data" / "factors"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_cache = use_cache
        
        # 初始化因子实例
        self._factors: Dict[str, BaseFactor] = {}
        self._init_factors()
    
    def _init_factors(self):
        """初始化所有因子实例"""
        for name, factor_class in self.FACTOR_CLASSES.items():
            self._factors[name] = factor_class(
                jq_client=self.jq_client,
                cache_dir=self.cache_dir,
                use_cache=self.use_cache
            )
    
    def set_jq_client(self, jq_client):
        """设置JQData客户端"""
        self.jq_client = jq_client
        for factor in self._factors.values():
            factor.jq_client = jq_client
    
    def get_factor(self, name: str) -> Optional[BaseFactor]:
        """获取因子实例"""
        return self._factors.get(name)
    
    def list_factors(self, category: Optional[str] = None) -> List[str]:
        """
        列出所有因子
        
        Args:
            category: 因子类别（value, growth, quality, momentum）
        
        Returns:
            因子名称列表
        """
        if category:
            return self.FACTOR_CATEGORIES.get(category, [])
        return list(self._factors.keys())
    
    def get_factor_info(self, name: str) -> Optional[Dict[str, Any]]:
        """获取因子信息"""
        factor = self._factors.get(name)
        if factor:
            return {
                'name': factor.name,
                'category': factor.category,
                'description': factor.description,
                'direction': factor.direction
            }
        return None
    
    def calculate_factor(
        self,
        factor_name: str,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> Optional[FactorResult]:
        """
        计算单个因子
        
        Args:
            factor_name: 因子名称
            stocks: 股票列表
            date: 计算日期
            **kwargs: 额外参数
        
        Returns:
            FactorResult: 因子计算结果
        """
        factor = self._factors.get(factor_name)
        if factor is None:
            logger.error(f"因子不存在: {factor_name}")
            return None
        
        return factor.calculate(stocks, date, **kwargs)
    
    def calculate_factors(
        self,
        factor_names: List[str],
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> Dict[str, FactorResult]:
        """
        批量计算多个因子
        
        Args:
            factor_names: 因子名称列表
            stocks: 股票列表
            date: 计算日期
            **kwargs: 额外参数
        
        Returns:
            Dict[str, FactorResult]: 因子计算结果字典
        """
        results = {}
        for name in factor_names:
            result = self.calculate_factor(name, stocks, date, **kwargs)
            if result:
                results[name] = result
        return results
    
    def calculate_all_factors(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        categories: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, FactorResult]:
        """
        计算所有因子
        
        Args:
            stocks: 股票列表
            date: 计算日期
            categories: 因子类别列表，None表示所有类别
            **kwargs: 额外参数
        
        Returns:
            Dict[str, FactorResult]: 因子计算结果字典
        """
        if categories:
            factor_names = []
            for cat in categories:
                factor_names.extend(self.FACTOR_CATEGORIES.get(cat, []))
        else:
            factor_names = list(self._factors.keys())
        
        return self.calculate_factors(factor_names, stocks, date, **kwargs)
    
    def combine_factors(
        self,
        factor_results: Dict[str, FactorResult],
        weights: Optional[Dict[str, float]] = None,
        method: str = 'equal'
    ) -> pd.Series:
        """
        组合多个因子
        
        Args:
            factor_results: 因子计算结果字典
            weights: 因子权重
            method: 组合方法 ('equal', 'ic_weighted', 'custom')
        
        Returns:
            pd.Series: 组合因子值
        """
        if not factor_results:
            return pd.Series(dtype=float)
        
        # 收集所有因子值
        factor_df = pd.DataFrame({
            name: result.values for name, result in factor_results.items()
        })
        
        if method == 'equal' or weights is None:
            # 等权组合
            weights = {name: 1.0 / len(factor_results) for name in factor_results}
        
        # 加权组合
        combined = pd.Series(0, index=factor_df.index)
        total_weight = 0
        
        for name, weight in weights.items():
            if name in factor_df.columns:
                # 标准化
                factor_values = factor_df[name]
                mean = factor_values.mean()
                std = factor_values.std()
                if std > 0:
                    factor_values = (factor_values - mean) / std
                else:
                    factor_values = factor_values - mean
                
                combined += factor_values.fillna(0) * weight
                total_weight += weight
        
        if total_weight > 0:
            combined /= total_weight
        
        return combined
    
    def select_stocks(
        self,
        combined_factor: pd.Series,
        top_n: int = 30,
        min_score: Optional[float] = None
    ) -> List[str]:
        """
        根据组合因子选股
        
        Args:
            combined_factor: 组合因子值
            top_n: 选择前N只股票
            min_score: 最低分数阈值
        
        Returns:
            List[str]: 选中的股票列表
        """
        # 过滤无效值
        valid_factor = combined_factor.dropna()
        
        if min_score is not None:
            valid_factor = valid_factor[valid_factor >= min_score]
        
        # 选择前N只
        selected = valid_factor.nlargest(top_n).index.tolist()
        
        return selected
    
    def generate_ptrade_strategy(
        self,
        factor_names: List[str],
        weights: Optional[Dict[str, float]] = None,
        stock_pool: str = '000300.XSHG',
        hold_num: int = 30,
        rebalance_freq: str = 'monthly'
    ) -> str:
        """
        生成PTrade策略代码
        
        Args:
            factor_names: 使用的因子名称列表
            weights: 因子权重
            stock_pool: 股票池（指数代码）
            hold_num: 持仓数量
            rebalance_freq: 调仓频率
        
        Returns:
            str: PTrade策略代码
        """
        # 收集因子计算代码
        factor_codes = []
        for name in factor_names:
            factor = self._factors.get(name)
            if factor:
                factor_codes.append(factor.get_ptrade_code())
        
        # 生成权重字符串
        if weights is None:
            weights = {name: 1.0 / len(factor_names) for name in factor_names}
        weights_str = str(weights)
        
        # 生成调仓代码
        if rebalance_freq == 'monthly':
            rebalance_code = "run_monthly(rebalance, 1, time='open')"
        elif rebalance_freq == 'weekly':
            rebalance_code = "run_weekly(rebalance, 1, time='open')"
        else:
            rebalance_code = "run_daily(rebalance, time='open')"
        
        strategy_code = f'''# -*- coding: utf-8 -*-
"""
韬睿量化 - 多因子策略
======================

因子: {', '.join(factor_names)}
股票池: {stock_pool}
持仓数量: {hold_num}
调仓频率: {rebalance_freq}

由韬睿量化系统自动生成
"""

import pandas as pd
import numpy as np
from jqdatasdk import *

# ==================== 因子计算函数 ====================

{''.join(factor_codes)}

# ==================== 辅助函数 ====================

def zscore(series):
    """Z-score标准化"""
    mean = series.mean()
    std = series.std()
    if std > 0:
        return (series - mean) / std
    return series - mean

def winsorize_mad(series, n=5):
    """MAD法去极值"""
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0:
        return series
    upper = median + n * 1.4826 * mad
    lower = median - n * 1.4826 * mad
    return series.clip(lower, upper)

def filter_stocks(stocks, date):
    """过滤ST和停牌股票"""
    # 过滤ST
    st_stocks = get_extras('is_st', stocks, end_date=date, count=1).iloc[0]
    stocks = [s for s in stocks if not st_stocks.get(s, True)]
    
    # 过滤停牌
    paused = get_price(stocks, end_date=date, count=1, fields=['paused'], panel=False)
    paused_stocks = paused[paused['paused'] == 1]['code'].tolist()
    stocks = [s for s in stocks if s not in paused_stocks]
    
    return stocks

# ==================== 策略主体 ====================

def initialize(context):
    """初始化"""
    # 设置基准
    set_benchmark('{stock_pool}')
    
    # 设置滑点和手续费
    set_slippage(FixedSlippage(0.02))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    # 策略参数
    context.stock_pool = '{stock_pool}'
    context.hold_num = {hold_num}
    context.factor_weights = {weights_str}
    
    # 设置调仓
    {rebalance_code}

def calculate_composite_factor(stocks, date):
    """计算复合因子"""
    weights = {weights_str}
    
    factors = {{}}
    
    # 计算各因子
{''.join([f"    factors['{name}'] = calculate_{name.lower()}_factor(stocks, date)" + chr(10) for name in factor_names])}
    
    # 标准化并组合
    df = pd.DataFrame(factors)
    
    composite = pd.Series(0, index=df.index)
    for name, weight in weights.items():
        if name in df.columns:
            factor_values = winsorize_mad(df[name].fillna(0))
            composite += zscore(factor_values) * weight
    
    return zscore(composite)

def rebalance(context):
    """调仓"""
    date = context.current_dt.strftime('%Y-%m-%d')
    
    # 获取股票池
    stocks = get_index_stocks(context.stock_pool)
    
    # 过滤
    stocks = filter_stocks(stocks, date)
    
    if len(stocks) == 0:
        log.warning("股票池为空")
        return
    
    # 计算因子
    factor = calculate_composite_factor(stocks, date)
    
    # 选股
    target_stocks = factor.nlargest(context.hold_num).index.tolist()
    
    # 卖出不在目标中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target(stock, 0)
    
    # 买入目标股票
    if len(target_stocks) > 0:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_value(stock, context.portfolio.total_value * weight)
    
    log.info(f"调仓完成: 持仓 {{len(target_stocks)}} 只股票")
'''
        
        return strategy_code
    
    def save_strategy(
        self,
        strategy_code: str,
        filename: str,
        output_dir: Optional[Path] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        保存策略代码到文件，并创建元数据
        
        Args:
            strategy_code: 策略代码
            filename: 文件名
            output_dir: 输出目录
            metadata: 额外的元数据
        
        Returns:
            Path: 保存的文件路径
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "strategies" / "ptrade"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(strategy_code)
        
        # 创建元数据文件（用于Dashboard显示）
        meta_filename = filepath.stem + "_meta.json"
        meta_filepath = output_dir / meta_filename
        
        # 从策略代码中提取信息
        factors = []
        weights = {}
        stock_pool = "000300.XSHG"
        hold_num = 30
        
        for line in strategy_code.split('\n'):
            if '因子:' in line:
                factors = [f.strip() for f in line.split(':')[1].split(',')]
            if '股票池:' in line:
                stock_pool = line.split(':')[1].strip()
            if '持仓数量:' in line:
                try:
                    hold_num = int(line.split(':')[1].strip())
                except:
                    pass
        
        meta_data = {
            "name": filepath.stem,
            "type": "multi_factor",
            "source": "taorui_factor_library",
            "platform": "PTrade",
            "factors": factors,
            "weights": metadata.get("weights", {}) if metadata else {},
            "stock_pool": stock_pool,
            "hold_num": hold_num,
            "created_at": datetime.now().isoformat(),
            "description": f"韬睿量化因子库自动生成的多因子策略，使用{len(factors)}个因子",
            "version": "1.0"
        }
        
        if metadata:
            meta_data.update(metadata)
        
        with open(meta_filepath, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"策略已保存: {filepath}")
        logger.info(f"元数据已保存: {meta_filepath}")
        return filepath
    
    def clear_cache(self):
        """清空所有因子缓存"""
        for factor in self._factors.values():
            factor.clear_cache()
        logger.info("所有因子缓存已清空")
    
    def get_factor_summary(self) -> pd.DataFrame:
        """获取因子摘要信息"""
        data = []
        for name, factor in self._factors.items():
            data.append({
                'name': factor.name,
                'category': factor.category,
                'description': factor.description,
                'direction': '正向' if factor.direction == 1 else '负向'
            })
        
        return pd.DataFrame(data)


# 便捷函数
def create_factor_manager(jq_client=None) -> FactorManager:
    """创建因子管理器的便捷函数"""
    return FactorManager(jq_client=jq_client)

