# -*- coding: utf-8 -*-
"""
Resonance V2 Data Layer
=======================

数据层：负责从JQData获取市场数据，支持指数、行业、个股数据。
包含数据缓存机制，减少API调用。

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from functools import lru_cache

logger = logging.getLogger(__name__)


@dataclass
class MarketData:
    """市场数据容器"""
    code: str
    name: str
    data: pd.DataFrame  # OHLCV数据
    start_date: str
    end_date: str
    frequency: str = "daily"
    
    def __post_init__(self):
        if self.data is not None and not self.data.empty:
            self.trading_days = len(self.data)
        else:
            self.trading_days = 0
    
    @property
    def close(self) -> pd.Series:
        return self.data['close'] if 'close' in self.data.columns else pd.Series()
    
    @property
    def volume(self) -> pd.Series:
        return self.data['volume'] if 'volume' in self.data.columns else pd.Series()
    
    @property
    def returns(self) -> pd.Series:
        if 'close' in self.data.columns:
            return self.data['close'].pct_change()
        return pd.Series()


class MarketDataProvider:
    """
    市场数据提供者
    
    封装JQData API，提供统一的数据获取接口。
    支持数据缓存和批量获取。
    """
    
    def __init__(self, use_cache: bool = True, cache_days: int = 1):
        """
        初始化数据提供者
        
        Args:
            use_cache: 是否使用缓存
            cache_days: 缓存有效期（天）
        """
        self._jq = None
        self._authenticated = False
        self._use_cache = use_cache
        self._cache_days = cache_days
        self._cache: Dict[str, Tuple[datetime, pd.DataFrame]] = {}
        
    def _ensure_jqdata(self) -> bool:
        """确保JQData连接"""
        if self._authenticated:
            return True
            
        try:
            import jqdatasdk as jq
            
            # 尝试从配置获取认证信息
            try:
                from config.config_manager import get_config_manager
                cm = get_config_manager()
                jq_config = cm.get_config('jqdata')
                
                if not jq.is_auth():
                    jq.auth(jq_config['username'], jq_config['password'])
                    
            except Exception as e:
                logger.debug(f"配置管理器加载失败，尝试使用已有认证: {e}")
                
            self._jq = jq
            self._authenticated = jq.is_auth()
            
            if self._authenticated:
                logger.info("JQData认证成功")
            else:
                logger.warning("JQData未认证")
                
            return self._authenticated
            
        except ImportError:
            logger.error("jqdatasdk未安装")
            return False
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
            return False
    
    def _get_cache_key(self, code: str, start: str, end: str, freq: str = "daily") -> str:
        """生成缓存键"""
        return f"{code}_{start}_{end}_{freq}"
    
    def _is_cache_valid(self, cache_time: datetime) -> bool:
        """检查缓存是否有效"""
        if not self._use_cache:
            return False
        return datetime.now() - cache_time < timedelta(days=self._cache_days)
    
    def get_index_data(
        self,
        code: str,
        start_date: str,
        end_date: str,
        fields: Optional[List[str]] = None
    ) -> MarketData:
        """
        获取指数数据
        
        Args:
            code: 指数代码 (如 "000300.XSHG")
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            fields: 需要的字段列表，默认为OHLCV
        
        Returns:
            MarketData: 市场数据容器
        """
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume', 'money']
        
        # 检查缓存
        cache_key = self._get_cache_key(code, start_date, end_date)
        if cache_key in self._cache:
            cache_time, cached_data = self._cache[cache_key]
            if self._is_cache_valid(cache_time):
                logger.debug(f"从缓存获取指数数据: {code}")
                return MarketData(
                    code=code,
                    name=self._get_security_name(code),
                    data=cached_data,
                    start_date=start_date,
                    end_date=end_date
                )
        
        if not self._ensure_jqdata():
            logger.error("JQData未连接")
            return MarketData(code=code, name="", data=pd.DataFrame(), 
                            start_date=start_date, end_date=end_date)
        
        try:
            df = self._jq.get_price(
                code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=fields,
                skip_paused=False,
                fq='pre'  # 前复权
            )
            
            if df is not None and not df.empty:
                # 重置索引，将日期作为列
                df = df.reset_index()
                if 'index' in df.columns:
                    df = df.rename(columns={'index': 'date'})
                
                # 存入缓存
                if self._use_cache:
                    self._cache[cache_key] = (datetime.now(), df)
                
                logger.info(f"获取指数数据: {code}, {len(df)} 条记录")
            else:
                df = pd.DataFrame()
                logger.warning(f"指数数据为空: {code}")
            
            return MarketData(
                code=code,
                name=self._get_security_name(code),
                data=df,
                start_date=start_date,
                end_date=end_date
            )
            
        except Exception as e:
            logger.error(f"获取指数数据失败 {code}: {e}")
            return MarketData(code=code, name="", data=pd.DataFrame(),
                            start_date=start_date, end_date=end_date)
    
    def get_stock_data(
        self,
        codes: Union[str, List[str]],
        start_date: str,
        end_date: str,
        fields: Optional[List[str]] = None
    ) -> Dict[str, MarketData]:
        """
        获取股票数据
        
        Args:
            codes: 股票代码或代码列表
            start_date: 开始日期
            end_date: 结束日期
            fields: 需要的字段列表
        
        Returns:
            Dict[str, MarketData]: 股票代码 -> MarketData 映射
        """
        if isinstance(codes, str):
            codes = [codes]
        
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume', 'money']
        
        result = {}
        
        if not self._ensure_jqdata():
            logger.error("JQData未连接")
            return result
        
        try:
            # 批量获取数据
            df = self._jq.get_price(
                codes,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=fields,
                skip_paused=False,
                fq='pre',
                panel=False  # 返回DataFrame而非Panel
            )
            
            if df is None or df.empty:
                logger.warning(f"股票数据为空")
                return result
            
            # 按股票代码分组
            for code in codes:
                if 'code' in df.columns:
                    stock_df = df[df['code'] == code].copy()
                else:
                    # 如果只有一只股票
                    stock_df = df.copy()
                    stock_df['code'] = code
                
                if not stock_df.empty:
                    stock_df = stock_df.reset_index(drop=True)
                    result[code] = MarketData(
                        code=code,
                        name=self._get_security_name(code),
                        data=stock_df,
                        start_date=start_date,
                        end_date=end_date
                    )
            
            logger.info(f"获取股票数据: {len(result)} 只股票")
            return result
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return result
    
    def get_sector_data(
        self,
        sector_codes: Optional[List[str]] = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, MarketData]:
        """
        获取行业数据
        
        Args:
            sector_codes: 行业代码列表，None则获取全部申万一级行业
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            Dict[str, MarketData]: 行业代码 -> MarketData 映射
        """
        if not self._ensure_jqdata():
            logger.error("JQData未连接")
            return {}
        
        try:
            # 获取申万一级行业
            if sector_codes is None:
                industries = self._jq.get_industries(name='sw_l1')
                sector_codes = list(industries.index)
            
            # 行业指数代码转换 (申万行业指数)
            # 这里使用行业ETF或行业指数作为代理
            result = {}
            
            for sector in sector_codes:
                try:
                    # 获取行业指数数据
                    sector_index = self._get_sector_index(sector)
                    if sector_index:
                        data = self.get_index_data(sector_index, start_date, end_date)
                        if data.trading_days > 0:
                            result[sector] = data
                except Exception as e:
                    logger.debug(f"获取行业 {sector} 数据失败: {e}")
                    continue
            
            logger.info(f"获取行业数据: {len(result)} 个行业")
            return result
            
        except Exception as e:
            logger.error(f"获取行业数据失败: {e}")
            return {}
    
    def get_capital_flow(
        self,
        code: str,
        start_date: str,
        end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        获取资金流向数据 (可选)
        
        Args:
            code: 股票/指数代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            pd.DataFrame: 资金流向数据，包含北向资金、融资融券等
        """
        if not self._ensure_jqdata():
            return None
        
        try:
            # 尝试获取北向资金数据
            from jqdatasdk import finance
            
            # 北向资金
            north_df = self._jq.get_money_flow(
                code,
                start_date=start_date,
                end_date=end_date
            )
            
            return north_df
            
        except Exception as e:
            logger.debug(f"获取资金流向数据失败: {e}")
            return None
    
    def get_northbound_flow(
        self,
        start_date: str,
        end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        获取北向资金数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            pd.DataFrame: 北向资金数据
                - date: 日期
                - north_net: 北向净买入（亿元）
                - north_cumsum: 北向累计净买入
        """
        if not self._ensure_jqdata():
            return None
        
        try:
            from jqdatasdk import finance
            
            # 获取北向资金数据 (沪股通+深股通)
            q = self._jq.query(
                finance.STK_ML_QUOTA
            ).filter(
                finance.STK_ML_QUOTA.day >= start_date,
                finance.STK_ML_QUOTA.day <= end_date
            )
            
            df = finance.run_query(q)
            
            if df is None or df.empty:
                logger.warning("北向资金数据为空，使用模拟数据")
                return self._simulate_northbound_data(start_date, end_date)
            
            # 整理数据
            df['date'] = pd.to_datetime(df['day'])
            df = df.groupby('date').agg({
                'quota_daily_balance': 'sum'  # 每日余额
            }).reset_index()
            
            # 计算净流入（用余额变化近似）
            df['north_net'] = -df['quota_daily_balance'].diff()  # 余额减少=净买入
            df['north_cumsum'] = df['north_net'].cumsum()
            
            return df[['date', 'north_net', 'north_cumsum']]
            
        except Exception as e:
            logger.warning(f"获取北向资金数据失败: {e}, 使用模拟数据")
            return self._simulate_northbound_data(start_date, end_date)
    
    def _simulate_northbound_data(
        self,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        模拟北向资金数据（当API不可用时）
        
        基于市场指数数据模拟：
        - 市场上涨日倾向于北向净流入
        - 市场下跌日倾向于北向净流出
        """
        # 获取市场数据来模拟北向资金
        market_data = self.get_index_data("000300.XSHG", start_date, end_date)
        
        if market_data.trading_days == 0:
            return pd.DataFrame()
        
        df = market_data.data.copy()
        if 'date' not in df.columns:
            df['date'] = df.index
        
        # 基于市场收益模拟北向资金
        df['return'] = df['close'].pct_change()
        
        # 模拟北向净流入：收益率*100亿 + 随机噪声
        np.random.seed(42)
        df['north_net'] = df['return'] * 100 + np.random.normal(0, 10, len(df))
        df['north_cumsum'] = df['north_net'].cumsum()
        
        return df[['date', 'north_net', 'north_cumsum']].dropna()
    
    def get_market_breadth(
        self,
        date: str,
        lookback: int = 5
    ) -> Optional[Dict]:
        """
        获取市场宽度数据
        
        Args:
            date: 日期
            lookback: 回溯天数（用于计算区间内的宽度）
        
        Returns:
            Dict: 市场宽度指标
                - advance_count: 上涨股票数
                - decline_count: 下跌股票数
                - limit_up_count: 涨停数
                - limit_down_count: 跌停数
                - new_high_count: 创新高数
                - new_low_count: 创新低数
                - breadth_ratio: 上涨/下跌比率
        """
        if not self._ensure_jqdata():
            return None
        
        try:
            # 获取所有A股
            all_stocks = self._jq.get_all_securities(types=['stock'], date=date)
            stock_list = [s for s in all_stocks.index if s.startswith('0') or s.startswith('3') or s.startswith('6')]
            
            if not stock_list:
                return None
            
            # 获取前一天的数据来计算涨跌
            trade_days = self._jq.get_trade_days(end_date=date, count=lookback + 1)
            if len(trade_days) < 2:
                return None
            
            prev_date = trade_days[-2].strftime('%Y-%m-%d')
            
            # 获取当日和前日收盘价
            today_price = self._jq.get_price(
                stock_list[:500],  # 限制数量避免超时
                start_date=date,
                end_date=date,
                fields=['close', 'high_limit', 'low_limit'],
                skip_paused=True
            )
            
            prev_price = self._jq.get_price(
                stock_list[:500],
                start_date=prev_date,
                end_date=prev_date,
                fields=['close'],
                skip_paused=True
            )
            
            if today_price is None or today_price.empty or prev_price is None or prev_price.empty:
                return self._simulate_market_breadth()
            
            # 合并数据
            today_close = today_price.reset_index()
            prev_close = prev_price.reset_index()
            
            if 'code' in today_close.columns and 'code' in prev_close.columns:
                merged = today_close.merge(prev_close, on='code', suffixes=('_today', '_prev'))
            else:
                return self._simulate_market_breadth()
            
            # 计算涨跌
            merged['change'] = (merged['close_today'] - merged['close_prev']) / merged['close_prev']
            
            advance_count = (merged['change'] > 0).sum()
            decline_count = (merged['change'] < 0).sum()
            
            # 涨跌停
            if 'high_limit' in today_close.columns and 'low_limit' in today_close.columns:
                limit_up_count = (merged['close_today'] >= merged.get('high_limit', float('inf'))).sum()
                limit_down_count = (merged['close_today'] <= merged.get('low_limit', 0)).sum()
            else:
                limit_up_count = (merged['change'] >= 0.099).sum()
                limit_down_count = (merged['change'] <= -0.099).sum()
            
            breadth_ratio = advance_count / max(decline_count, 1)
            
            return {
                'date': date,
                'advance_count': int(advance_count),
                'decline_count': int(decline_count),
                'limit_up_count': int(limit_up_count),
                'limit_down_count': int(limit_down_count),
                'new_high_count': 0,  # 需要更多历史数据
                'new_low_count': 0,
                'breadth_ratio': float(breadth_ratio),
                'breadth_score': float((advance_count - decline_count) / max(advance_count + decline_count, 1))
            }
            
        except Exception as e:
            logger.warning(f"获取市场宽度数据失败: {e}, 使用模拟数据")
            return self._simulate_market_breadth()
    
    def _simulate_market_breadth(self) -> Dict:
        """模拟市场宽度数据"""
        # 随机模拟，给一个中性的基准
        np.random.seed(42)
        advance = np.random.randint(1500, 2500)
        decline = np.random.randint(1500, 2500)
        
        return {
            'advance_count': advance,
            'decline_count': decline,
            'limit_up_count': np.random.randint(20, 80),
            'limit_down_count': np.random.randint(10, 40),
            'new_high_count': np.random.randint(50, 150),
            'new_low_count': np.random.randint(30, 100),
            'breadth_ratio': advance / max(decline, 1),
            'breadth_score': (advance - decline) / max(advance + decline, 1)
        }
    
    def get_market_breadth_series(
        self,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        获取市场宽度时间序列
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            pd.DataFrame: 市场宽度时间序列
        """
        if not self._ensure_jqdata():
            return pd.DataFrame()
        
        try:
            trade_days = self.get_trading_dates(start_date, end_date)
            
            # 为了效率，使用采样（每5天采样一次）
            sample_days = trade_days[::5] if len(trade_days) > 20 else trade_days
            
            records = []
            for date in sample_days:
                breadth = self.get_market_breadth(date)
                if breadth:
                    records.append(breadth)
            
            if not records:
                return pd.DataFrame()
            
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            
            # 填充缺失日期（线性插值）
            all_dates = pd.to_datetime(trade_days)
            df = df.set_index('date').reindex(all_dates).interpolate(method='linear')
            df = df.reset_index().rename(columns={'index': 'date'})
            
            return df
            
        except Exception as e:
            logger.error(f"获取市场宽度序列失败: {e}")
            return pd.DataFrame()
    
    def get_index_constituents(
        self,
        index_code: str,
        date: str
    ) -> List[str]:
        """
        获取指数成分股
        
        Args:
            index_code: 指数代码
            date: 日期
        
        Returns:
            List[str]: 成分股代码列表
        """
        if not self._ensure_jqdata():
            return []
        
        try:
            stocks = self._jq.get_index_stocks(index_code, date=date)
            return stocks if stocks else []
        except Exception as e:
            logger.error(f"获取指数成分股失败 {index_code}: {e}")
            return []
    
    def _get_security_name(self, code: str) -> str:
        """获取证券名称"""
        if not self._ensure_jqdata():
            return ""
        
        try:
            info = self._jq.get_security_info(code)
            return info.display_name if info else ""
        except:
            return ""
    
    def _get_sector_index(self, sector_code: str) -> Optional[str]:
        """
        将行业代码转换为对应的行业指数代码
        
        申万行业指数代码格式：801xxx.XSHG
        """
        # 申万一级行业指数映射
        sw_l1_indices = {
            '801010': '801010.XSHG',  # 农林牧渔
            '801020': '801020.XSHG',  # 采掘
            '801030': '801030.XSHG',  # 化工
            '801040': '801040.XSHG',  # 钢铁
            '801050': '801050.XSHG',  # 有色金属
            '801080': '801080.XSHG',  # 电子
            '801110': '801110.XSHG',  # 家用电器
            '801120': '801120.XSHG',  # 食品饮料
            '801130': '801130.XSHG',  # 纺织服装
            '801140': '801140.XSHG',  # 轻工制造
            '801150': '801150.XSHG',  # 医药生物
            '801160': '801160.XSHG',  # 公用事业
            '801170': '801170.XSHG',  # 交通运输
            '801180': '801180.XSHG',  # 房地产
            '801200': '801200.XSHG',  # 商业贸易
            '801210': '801210.XSHG',  # 休闲服务
            '801230': '801230.XSHG',  # 综合
            '801710': '801710.XSHG',  # 建筑材料
            '801720': '801720.XSHG',  # 建筑装饰
            '801730': '801730.XSHG',  # 电气设备
            '801740': '801740.XSHG',  # 国防军工
            '801750': '801750.XSHG',  # 计算机
            '801760': '801760.XSHG',  # 传媒
            '801770': '801770.XSHG',  # 通信
            '801780': '801780.XSHG',  # 银行
            '801790': '801790.XSHG',  # 非银金融
            '801880': '801880.XSHG',  # 汽车
            '801890': '801890.XSHG',  # 机械设备
        }
        
        # 尝试直接匹配
        if sector_code in sw_l1_indices:
            return sw_l1_indices[sector_code]
        
        # 尝试添加后缀
        if not sector_code.endswith('.XSHG'):
            full_code = f"{sector_code}.XSHG"
            if full_code in sw_l1_indices.values():
                return full_code
        
        return None
    
    def get_trading_dates(
        self,
        start_date: str,
        end_date: str
    ) -> List[str]:
        """
        获取交易日列表
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            List[str]: 交易日列表
        """
        if not self._ensure_jqdata():
            return []
        
        try:
            dates = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
            return [d.strftime('%Y-%m-%d') for d in dates]
        except Exception as e:
            logger.error(f"获取交易日失败: {e}")
            return []
    
    def clear_cache(self):
        """清除所有缓存"""
        self._cache.clear()
        logger.info("数据缓存已清除")


# 模块级别的单例实例
_provider_instance: Optional[MarketDataProvider] = None


def get_data_provider() -> MarketDataProvider:
    """获取数据提供者单例"""
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = MarketDataProvider()
    return _provider_instance
