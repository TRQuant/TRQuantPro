"""
文件名: code_6_3_group_backtest.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3_group_backtest.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: group_backtest

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

@dataclass
class GroupBacktestResult:
    """分组回测结果"""
    factor_name: str
    start_date: datetime
    end_date: datetime
    n_groups: int
    group_returns: Dict[int, float]  # 各组平均收益
    group_sharpe: Dict[int, float]  # 各组夏普比
    long_short_return: float  # 多空收益
    is_monotonic: bool  # 是否单调
    ic_mean: float  # 平均IC
    ic_ir: float  # IC信息比

def group_backtest(
    self,
    factor_calculator,
    stocks: List[str],
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    n_groups: int = 5,
    rebalance_freq: str = "M",
) -> GroupBacktestResult:
        """
    group_backtest函数
    
    **设计原理**：
    - **核心功能**：实现group_backtest的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    if self.jq_client is None:
        raise ValueError("需要JQData客户端")
    
    import jqdatasdk as jq
    
    # 生成调仓日期
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    trade_dates = jq.get_trade_days(start_date, end_date)
    
    # 按频率筛选调仓日期
    if rebalance_freq == "M":
        dates_df = pd.DataFrame({"date": trade_dates})
        dates_df["month"] = dates_df["date"].apply(lambda x: x.strftime("%Y-%m"))
        rebalance_dates = dates_df.groupby("month")["date"].last().values
    elif rebalance_freq == "W":
        dates_df = pd.DataFrame({"date": trade_dates})
        dates_df["week"] = dates_df["date"].apply(lambda x: x.strftime("%Y-%W"))
        rebalance_dates = dates_df.groupby("week")["date"].last().values
    else:
        rebalance_dates = trade_dates
    
    # 初始化分组收益记录
    group_returns_list = {i: [] for i in range(n_groups)}
    
    # 计算IC时间序列
    ic_series = []
    
    for rebalance_date in rebalance_dates:
        try:
            # 计算因子值
            if hasattr(factor_calculator, "calculate"):
                factor_result = factor_calculator.calculate(stocks, rebalance_date)
                factor_values = factor_result.values
            else:
                factor_values = factor_calculator(stocks, rebalance_date)
            
            # 分组
            groups = self._group_by_factor(factor_values, n_groups)
            
            # 计算下一期收益
            next_date_idx = np.searchsorted(trade_dates, rebalance_date) + 20
            if next_date_idx >= len(trade_dates):
                continue
            
            next_date = trade_dates[next_date_idx]
            returns = self._get_returns(stocks, rebalance_date, next_date)
            
            if returns is None or returns.empty:
                continue
            
            # 计算各组收益
            for group_id, group_stocks in groups.items():
                group_return = returns[group_stocks].mean()
                group_returns_list[group_id].append(group_return)
            
            # 计算IC
            ic_result = self.calculate_ic(factor_values, returns)
            ic_series.append(ic_result.rank_ic)
        
        except Exception as e:
            logger.warning(f"分组回测失败 {rebalance_date}: {e}")
            continue
    
    # 计算各组平均收益和夏普比
    group_returns = {}
    group_sharpe = {}
    
    for group_id, returns_list in group_returns_list.items():
        if returns_list:
            group_returns[group_id] = np.mean(returns_list) * 252  # 年化
            group_sharpe[group_id] = (
                np.mean(returns_list) / np.std(returns_list) * np.sqrt(252)
                if np.std(returns_list) > 0 else 0
            )
    
    # 多空收益（最高组 - 最低组）
    long_short_return = (
        group_returns.get(n_groups - 1, 0) - group_returns.get(0, 0)
    )
    
    # 检查是否单调
    is_monotonic = self._check_monotonic(group_returns)
    
    # 计算IC统计
    ic_mean = np.mean(ic_series) if ic_series else 0
    ic_std = np.std(ic_series) if ic_series else 0
    ic_ir = ic_mean / ic_std if ic_std > 0 else 0
    
    return GroupBacktestResult(
        factor_name=getattr(factor_calculator, "name", ""),
        start_date=start_date,
        end_date=end_date,
        n_groups=n_groups,
        group_returns=group_returns,
        group_sharpe=group_sharpe,
        long_short_return=long_short_return,
        is_monotonic=is_monotonic,
        ic_mean=ic_mean,
        ic_ir=ic_ir,
    )

def _group_by_factor(self, factor_values: pd.Series, n_groups: int) -> Dict[int, List[str]]:
    """
    按因子值分组
    
    Args:
        factor_values: 因子值
        n_groups: 分组数量
    
    Returns:
        Dict[int, List[str]]: 分组结果 {组号: 股票列表}
    """
    # 去除缺失值
    valid_values = factor_values.dropna()
    
    if len(valid_values) < n_groups:
        # 样本不足，返回空分组
        return {i: [] for i in range(n_groups)}
    
    # 按分位数分组
    groups = {}
    for i in range(n_groups):
        lower = i / n_groups
        upper = (i + 1) / n_groups
        
        if i == 0:
            mask = valid_values <= valid_values.quantile(upper)
        elif i == n_groups - 1:
            mask = valid_values > valid_values.quantile(lower)
        else:
            mask = (valid_values > valid_values.quantile(lower)) & \
                   (valid_values <= valid_values.quantile(upper))
        
        groups[i] = valid_values[mask].index.tolist()
    
    return groups

def _check_monotonic(self, group_returns: Dict[int, float]) -> bool:
    """
    检查分组收益是否单调
    
    Args:
        group_returns: 各组收益
    
    Returns:
        bool: 是否单调
    """
    if len(group_returns) < 2:
        return False
    
    returns_list = [group_returns.get(i, 0) for i in sorted(group_returns.keys())]
    
    # 检查是否单调递增或递减
    is_increasing = all(returns_list[i] <= returns_list[i+1] 
                       for i in range(len(returns_list) - 1))
    is_decreasing = all(returns_list[i] >= returns_list[i+1] 
                       for i in range(len(returns_list) - 1))
    
    return is_increasing or is_decreasing