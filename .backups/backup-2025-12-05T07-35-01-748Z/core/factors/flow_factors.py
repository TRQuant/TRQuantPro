# -*- coding: utf-8 -*-
"""
资金流因子模块（A股特色）
========================

包含以下因子：
- NorthboundFlow: 北向资金流入
- MainForceFlow: 主力资金流入
- MarginBalance: 融资余额变化

A股特点：
- 北向资金是最重要的"聪明钱"指标
- 主力资金反映机构行为
- 融资融券反映杠杆资金情绪
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime, timedelta
import logging

from .base_factor import BaseFactor

logger = logging.getLogger(__name__)


class NorthboundFlowFactor(BaseFactor):
    """
    北向资金因子
    
    经济学逻辑：
    - 北向资金代表外资的投资偏好
    - 通常被认为是"聪明钱"
    - 偏好高ROE、低估值的龙头股
    
    A股实证：
    - IC可达0.045，是A股最有效的因子之一
    - 在蓝筹股中效果尤其显著
    """
    
    name = "NorthboundFlow"
    category = "flow"
    description = "北向资金因子"
    direction = 1
    
    def __init__(self, jq_client=None, lookback_days: int = 20, **kwargs):
        """
        初始化
        
        Args:
            lookback_days: 回看天数（默认20天，约1个月）
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """
        计算北向资金因子
        
        注意：JQData的北向资金数据可能需要特殊权限
        这里提供一个基于持股变化的近似计算
        """
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算北向资金因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import finance
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 尝试获取沪深港通持股数据
            # 注意：这需要JQData的高级权限
            try:
                # 获取当前持股
                q_current = jq.query(
                    finance.STK_HK_HOLD_INFO.code,
                    finance.STK_HK_HOLD_INFO.share_ratio
                ).filter(
                    finance.STK_HK_HOLD_INFO.code.in_(stocks),
                    finance.STK_HK_HOLD_INFO.day == date.strftime('%Y-%m-%d')
                )
                
                df_current = finance.run_query(q_current)
                
                # 获取N天前持股
                past_date = date - timedelta(days=self.lookback_days)
                q_past = jq.query(
                    finance.STK_HK_HOLD_INFO.code,
                    finance.STK_HK_HOLD_INFO.share_ratio
                ).filter(
                    finance.STK_HK_HOLD_INFO.code.in_(stocks),
                    finance.STK_HK_HOLD_INFO.day == past_date.strftime('%Y-%m-%d')
                )
                
                df_past = finance.run_query(q_past)
                
                if not df_current.empty and not df_past.empty:
                    df_current = df_current.set_index('code')
                    df_past = df_past.set_index('code')
                    
                    # 计算持股比例变化
                    flow = df_current['share_ratio'] - df_past['share_ratio'].reindex(df_current.index).fillna(0)
                    
                    result = flow.reindex(stocks)
                    logger.info(f"北向资金因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
                    return result
                    
            except Exception as e:
                logger.warning(f"获取北向资金数据失败，使用替代方法: {e}")
            
            # 替代方法：使用成交量和价格变化的综合指标
            # 这是一个近似，实际应该使用真实的北向资金数据
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 5,
                fields=['close', 'volume', 'money'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            flow_dict = {}
            
            for stock in stocks:
                stock_data = prices[prices['code'] == stock]
                
                if len(stock_data) < self.lookback_days:
                    flow_dict[stock] = np.nan
                    continue
                
                # 计算资金流入指标：价格上涨时的成交额 - 价格下跌时的成交额
                stock_data = stock_data.copy()
                stock_data['return'] = stock_data['close'].pct_change()
                stock_data['signed_money'] = np.where(
                    stock_data['return'] > 0,
                    stock_data['money'],
                    -stock_data['money']
                )
                
                # 近期资金流入
                recent_flow = stock_data['signed_money'].iloc[-self.lookback_days:].sum()
                avg_money = stock_data['money'].iloc[-self.lookback_days:].mean()
                
                if avg_money > 0:
                    flow_dict[stock] = recent_flow / (avg_money * self.lookback_days)
                else:
                    flow_dict[stock] = np.nan
            
            result = pd.Series(flow_dict)
            result = result.clip(-2, 2)
            
            logger.info(f"北向资金因子（替代）计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"北向资金因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return f'''
# 北向资金因子
def calculate_northbound_flow_factor(stocks, date, lookback_days={self.lookback_days}):
    """
    计算北向资金因子
    
    使用资金流向作为替代指标
    """
    from jqdatasdk import get_price
    import numpy as np
    import pandas as pd
    
    prices = get_price(
        stocks,
        end_date=date,
        count=lookback_days + 5,
        fields=['close', 'volume', 'money'],
        panel=False
    )
    
    flow_dict = {{}}
    
    for stock in stocks:
        stock_data = prices[prices['code'] == stock].copy()
        
        if len(stock_data) < lookback_days:
            flow_dict[stock] = np.nan
            continue
        
        stock_data['return'] = stock_data['close'].pct_change()
        stock_data['signed_money'] = np.where(
            stock_data['return'] > 0,
            stock_data['money'],
            -stock_data['money']
        )
        
        recent_flow = stock_data['signed_money'].iloc[-lookback_days:].sum()
        avg_money = stock_data['money'].iloc[-lookback_days:].mean()
        
        if avg_money > 0:
            flow_dict[stock] = recent_flow / (avg_money * lookback_days)
        else:
            flow_dict[stock] = np.nan
    
    return pd.Series(flow_dict).clip(-2, 2)
'''


class MainForceFlowFactor(BaseFactor):
    """
    主力资金因子
    
    公式: 主力净流入 = 大单买入 - 大单卖出
    
    经济学逻辑：
    - 大单通常代表机构或大户行为
    - 主力资金流入预示股价上涨
    
    A股实证：
    - 短期效果明显
    - 需要结合成交量判断
    """
    
    name = "MainForceFlow"
    category = "flow"
    description = "主力资金因子"
    direction = 1
    
    def __init__(self, jq_client=None, lookback_days: int = 10, **kwargs):
        """
        初始化
        
        Args:
            lookback_days: 回看天数
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算主力资金因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算主力资金因子")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 获取成交数据
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 5,
                fields=['close', 'volume', 'money', 'high', 'low'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            flow_dict = {}
            
            for stock in stocks:
                stock_data = prices[prices['code'] == stock].copy()
                
                if len(stock_data) < self.lookback_days:
                    flow_dict[stock] = np.nan
                    continue
                
                # 使用价格位置和成交量估算主力行为
                # 高位放量买入 vs 低位放量卖出
                stock_data['price_position'] = (
                    (stock_data['close'] - stock_data['low']) / 
                    (stock_data['high'] - stock_data['low'] + 0.0001)
                )
                
                # 价格位置高+成交量大 = 主力买入
                stock_data['main_flow'] = (
                    (stock_data['price_position'] - 0.5) * 
                    stock_data['money']
                )
                
                recent_flow = stock_data['main_flow'].iloc[-self.lookback_days:].sum()
                avg_money = stock_data['money'].iloc[-self.lookback_days:].mean()
                
                if avg_money > 0:
                    flow_dict[stock] = recent_flow / (avg_money * self.lookback_days)
                else:
                    flow_dict[stock] = np.nan
            
            result = pd.Series(flow_dict)
            result = result.clip(-2, 2)
            
            logger.info(f"主力资金因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"主力资金因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return f'''
# 主力资金因子
def calculate_main_force_flow_factor(stocks, date, lookback_days={self.lookback_days}):
    """
    计算主力资金因子
    
    使用价格位置和成交量估算主力行为
    """
    from jqdatasdk import get_price
    import numpy as np
    import pandas as pd
    
    prices = get_price(
        stocks,
        end_date=date,
        count=lookback_days + 5,
        fields=['close', 'volume', 'money', 'high', 'low'],
        panel=False
    )
    
    flow_dict = {{}}
    
    for stock in stocks:
        stock_data = prices[prices['code'] == stock].copy()
        
        if len(stock_data) < lookback_days:
            flow_dict[stock] = np.nan
            continue
        
        # 价格位置
        stock_data['price_position'] = (
            (stock_data['close'] - stock_data['low']) / 
            (stock_data['high'] - stock_data['low'] + 0.0001)
        )
        
        # 主力资金流
        stock_data['main_flow'] = (
            (stock_data['price_position'] - 0.5) * 
            stock_data['money']
        )
        
        recent_flow = stock_data['main_flow'].iloc[-lookback_days:].sum()
        avg_money = stock_data['money'].iloc[-lookback_days:].mean()
        
        if avg_money > 0:
            flow_dict[stock] = recent_flow / (avg_money * lookback_days)
        else:
            flow_dict[stock] = np.nan
    
    return pd.Series(flow_dict).clip(-2, 2)
'''


class MarginBalanceFactor(BaseFactor):
    """
    融资余额变化因子
    
    公式: 融资变化 = (融资余额_t - 融资余额_t-N) / 融资余额_t-N
    
    经济学逻辑：
    - 融资余额增加表示杠杆资金看多
    - 反映市场情绪和风险偏好
    
    A股实证：
    - 短期有一定预测能力
    - 需要注意过度杠杆的风险
    """
    
    name = "MarginBalance"
    category = "flow"
    description = "融资余额变化因子"
    direction = 1
    
    def __init__(self, jq_client=None, lookback_days: int = 20, **kwargs):
        """
        初始化
        
        Args:
            lookback_days: 回看天数
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算融资余额变化因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算融资余额因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import finance
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 尝试获取融资融券数据
            try:
                # 当前融资余额
                q_current = jq.query(
                    finance.STK_MT_TOTAL.sec_code,
                    finance.STK_MT_TOTAL.fin_balance
                ).filter(
                    finance.STK_MT_TOTAL.sec_code.in_(stocks),
                    finance.STK_MT_TOTAL.date == date.strftime('%Y-%m-%d')
                )
                
                df_current = finance.run_query(q_current)
                
                # N天前融资余额
                past_date = date - timedelta(days=self.lookback_days)
                q_past = jq.query(
                    finance.STK_MT_TOTAL.sec_code,
                    finance.STK_MT_TOTAL.fin_balance
                ).filter(
                    finance.STK_MT_TOTAL.sec_code.in_(stocks),
                    finance.STK_MT_TOTAL.date == past_date.strftime('%Y-%m-%d')
                )
                
                df_past = finance.run_query(q_past)
                
                if not df_current.empty and not df_past.empty:
                    df_current = df_current.set_index('sec_code')
                    df_past = df_past.set_index('sec_code')
                    
                    # 计算变化率
                    past_balance = df_past['fin_balance'].reindex(df_current.index)
                    change = (df_current['fin_balance'] - past_balance) / (past_balance.abs() + 1)
                    
                    result = change.clip(-1, 1)
                    result.index = result.index.map(lambda x: x if '.X' in x else x + '.XSHE')
                    result = result.reindex(stocks)
                    
                    logger.info(f"融资余额因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
                    return result
                    
            except Exception as e:
                logger.warning(f"获取融资融券数据失败: {e}")
            
            # 返回空值
            return pd.Series(index=stocks, dtype=float)
            
        except Exception as e:
            logger.error(f"融资余额因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return f'''
# 融资余额变化因子
def calculate_margin_balance_factor(stocks, date, lookback_days={self.lookback_days}):
    """
    计算融资余额变化因子
    
    需要融资融券数据权限
    """
    from jqdatasdk import query, finance
    from datetime import datetime, timedelta
    import pandas as pd
    
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    
    try:
        # 当前融资余额
        q_current = query(
            finance.STK_MT_TOTAL.sec_code,
            finance.STK_MT_TOTAL.fin_balance
        ).filter(
            finance.STK_MT_TOTAL.sec_code.in_(stocks),
            finance.STK_MT_TOTAL.date == date.strftime('%Y-%m-%d')
        )
        df_current = finance.run_query(q_current)
        
        # N天前
        past_date = date - timedelta(days=lookback_days)
        q_past = query(
            finance.STK_MT_TOTAL.sec_code,
            finance.STK_MT_TOTAL.fin_balance
        ).filter(
            finance.STK_MT_TOTAL.sec_code.in_(stocks),
            finance.STK_MT_TOTAL.date == past_date.strftime('%Y-%m-%d')
        )
        df_past = finance.run_query(q_past)
        
        if not df_current.empty and not df_past.empty:
            df_current = df_current.set_index('sec_code')
            df_past = df_past.set_index('sec_code')
            
            past_balance = df_past['fin_balance'].reindex(df_current.index)
            change = (df_current['fin_balance'] - past_balance) / (past_balance.abs() + 1)
            
            return change.clip(-1, 1)
    except:
        pass
    
    return pd.Series(index=stocks, dtype=float)
'''


class CompositeFlowFactor(BaseFactor):
    """
    复合资金流因子
    
    综合北向资金、主力资金、融资余额三个因子。
    """
    
    name = "CompositeFlow"
    category = "flow"
    description = "复合资金流因子"
    direction = 1
    
    def __init__(self, jq_client=None, weights: Optional[dict] = None, **kwargs):
        """
        初始化
        
        Args:
            weights: 因子权重
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.weights = weights or {
            'NorthboundFlow': 0.5,  # 北向资金权重最高
            'MainForceFlow': 0.3,
            'MarginBalance': 0.2
        }
        
        self.northbound_factor = NorthboundFlowFactor(jq_client=jq_client, **kwargs)
        self.mainforce_factor = MainForceFlowFactor(jq_client=jq_client, **kwargs)
        self.margin_factor = MarginBalanceFactor(jq_client=jq_client, **kwargs)
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算复合资金流因子"""
        factors = {}
        
        if self.weights.get('NorthboundFlow', 0) > 0:
            factors['NorthboundFlow'] = self.northbound_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('MainForceFlow', 0) > 0:
            factors['MainForceFlow'] = self.mainforce_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('MarginBalance', 0) > 0:
            factors['MarginBalance'] = self.margin_factor.calculate(stocks, date, **kwargs).values
        
        df = pd.DataFrame(factors)
        
        # 加权平均
        composite = pd.Series(0, index=df.index)
        total_weight = 0
        
        for name, weight in self.weights.items():
            if name in df.columns:
                factor_values = df[name].fillna(0)
                composite += factor_values * weight
                total_weight += weight
        
        if total_weight > 0:
            composite /= total_weight
        
        composite.index = stocks
        
        logger.info(f"复合资金流因子计算完成: 有效值 {composite.notna().sum()}/{len(stocks)}")
        return composite
    
    def get_ptrade_code(self) -> str:
        return '''
# 复合资金流因子
def calculate_composite_flow_factor(stocks, date, weights=None):
    """计算复合资金流因子"""
    if weights is None:
        weights = {'NorthboundFlow': 0.5, 'MainForceFlow': 0.3, 'MarginBalance': 0.2}
    
    northbound = calculate_northbound_flow_factor(stocks, date)
    mainforce = calculate_main_force_flow_factor(stocks, date)
    margin = calculate_margin_balance_factor(stocks, date)
    
    def zscore(s):
        return (s - s.mean()) / s.std() if s.std() > 0 else s - s.mean()
    
    composite = (
        zscore(northbound.fillna(0)) * weights['NorthboundFlow'] +
        zscore(mainforce.fillna(0)) * weights['MainForceFlow'] +
        zscore(margin.fillna(0)) * weights['MarginBalance']
    )
    
    return zscore(composite)
'''

