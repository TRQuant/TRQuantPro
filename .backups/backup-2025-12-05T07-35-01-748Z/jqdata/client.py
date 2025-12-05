"""
聚宽API客户端

支持两种数据模式：
1. historical（历史模式）：使用免费版账号，只能获取历史数据
2. realtime（实时模式）：使用付费版账号，可获取实时数据

自动检测账号权限范围，并在该范围内获取数据。
"""
import jqdatasdk as jq
import pandas as pd
from typing import List, Optional, Union, Tuple
from datetime import datetime, date, timedelta
import logging
import re
from .auth import authenticate

logger = logging.getLogger(__name__)


class DataPermission:
    """数据权限信息"""
    
    def __init__(self):
        self.start_date: Optional[str] = None  # 权限开始日期
        self.end_date: Optional[str] = None    # 权限结束日期
        self.is_realtime: bool = False         # 是否支持实时数据
        self.detected: bool = False            # 是否已检测
        
    def is_date_in_range(self, check_date: Union[str, date, datetime]) -> bool:
        """检查日期是否在权限范围内"""
        if not self.detected:
            return True  # 未检测时默认允许
        
        if isinstance(check_date, str):
            check_dt = datetime.strptime(check_date, '%Y-%m-%d').date()
        elif isinstance(check_date, datetime):
            check_dt = check_date.date()
        else:
            check_dt = check_date
            
        start_dt = datetime.strptime(self.start_date, '%Y-%m-%d').date() if self.start_date else date(2000, 1, 1)
        end_dt = datetime.strptime(self.end_date, '%Y-%m-%d').date() if self.end_date else date.today()
        
        return start_dt <= check_dt <= end_dt
    
    def get_valid_date_range(self, requested_start: str, requested_end: str) -> Tuple[str, str]:
        """获取有效的日期范围（在权限范围内）"""
        if not self.detected:
            return requested_start, requested_end
        
        req_start = datetime.strptime(requested_start, '%Y-%m-%d').date()
        req_end = datetime.strptime(requested_end, '%Y-%m-%d').date()
        perm_start = datetime.strptime(self.start_date, '%Y-%m-%d').date() if self.start_date else req_start
        perm_end = datetime.strptime(self.end_date, '%Y-%m-%d').date() if self.end_date else req_end
        
        valid_start = max(req_start, perm_start)
        valid_end = min(req_end, perm_end)
        
        return valid_start.strftime('%Y-%m-%d'), valid_end.strftime('%Y-%m-%d')
    
    def get_latest_available_date(self) -> str:
        """获取权限范围内的最新可用日期"""
        if self.is_realtime:
            return date.today().strftime('%Y-%m-%d')
        elif self.end_date:
            return self.end_date
        else:
            return date.today().strftime('%Y-%m-%d')
    
    def __str__(self):
        if not self.detected:
            return "权限未检测"
        mode = "实时" if self.is_realtime else "历史"
        return f"数据模式: {mode}, 范围: {self.start_date} 至 {self.end_date}"


class JQDataClient:
    """
    聚宽数据API客户端
    
    特性：
    1. 自动检测账号权限范围
    2. 支持历史模式和实时模式
    3. 自动调整请求日期到权限范围内
    """
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            username: 聚宽用户名
            password: 聚宽密码
        """
        self._authenticated = False
        self.permission = DataPermission()
        
        if username and password:
            self.authenticate(username, password)
    
    def authenticate(self, username: str, password: str) -> bool:
        """认证"""
        self._authenticated = authenticate(username, password)
        if self._authenticated:
            # 认证成功后自动检测权限
            self._detect_permission()
        return self._authenticated
    
    def is_authenticated(self) -> bool:
        """检查是否已认证"""
        return self._authenticated
    
    def _detect_permission(self):
        """
        自动检测账号数据权限范围
        
        通过尝试获取数据并解析错误信息来确定权限范围
        """
        logger.info("正在检测账号数据权限...")
        
        try:
            # 尝试获取今天的数据
            today = date.today().strftime('%Y-%m-%d')
            yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            try:
                # 尝试获取最近的数据
                test_data = jq.get_price(
                    '000001.XSHE',  # 平安银行，流动性好
                    start_date=yesterday,
                    end_date=today,
                    frequency='daily',
                    fields=['close']
                )
                
                if not test_data.empty:
                    # 能获取到今天或昨天的数据，说明是实时账号
                    self.permission.is_realtime = True
                    self.permission.end_date = today
                    # 尝试确定开始日期（向前推5年）
                    five_years_ago = (date.today() - timedelta(days=365*5)).strftime('%Y-%m-%d')
                    self.permission.start_date = five_years_ago
                    self.permission.detected = True
                    logger.info(f"✅ 检测到实时账号权限: {self.permission}")
                    return
                    
            except Exception as e:
                error_msg = str(e)
                # 解析错误信息中的日期范围
                if "账号权限仅能获取" in error_msg:
                    date_pattern = r'(\d{4}-\d{2}-\d{2})'
                    dates = re.findall(date_pattern, error_msg)
                    if len(dates) >= 2:
                        self.permission.start_date = dates[0]
                        self.permission.end_date = dates[1]
                        self.permission.is_realtime = False
                        self.permission.detected = True
                        logger.info(f"✅ 检测到历史账号权限: {self.permission}")
                        return
            
            # 默认设置（如果无法检测）
            self.permission.start_date = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')
            self.permission.end_date = (date.today() - timedelta(days=90)).strftime('%Y-%m-%d')
            self.permission.is_realtime = False
            self.permission.detected = True
            logger.warning(f"⚠️ 使用默认权限范围: {self.permission}")
            
        except Exception as e:
            logger.error(f"权限检测失败: {e}")
            self.permission.detected = False
    
    def get_permission(self) -> DataPermission:
        """获取当前账号的数据权限信息"""
        return self.permission
    
    def get_available_end_date(self) -> str:
        """获取可用的最新日期（用于筛选和分析）"""
        return self.permission.get_latest_available_date()
    
    def get_price(
        self,
        securities: Union[str, List[str]],
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        frequency: str = 'daily',
        fields: Optional[List[str]] = None,
        auto_adjust_date: bool = True
    ) -> pd.DataFrame:
        """
        获取价格数据
        
        Args:
            securities: 股票代码或代码列表
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率 ('daily', '1m', '5m', '15m', '30m', '60m')
            fields: 字段列表，默认 ['open', 'close', 'high', 'low', 'volume']
            auto_adjust_date: 是否自动调整日期到权限范围内
        
        Returns:
            DataFrame: 价格数据
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        if fields is None:
            fields = ['open', 'close', 'high', 'low', 'volume']
        
        # 转换日期格式
        if isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime('%Y-%m-%d')
        if isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime('%Y-%m-%d')
        
        # 自动调整日期到权限范围内
        if auto_adjust_date and self.permission.detected:
            start_date, end_date = self.permission.get_valid_date_range(start_date, end_date)
            logger.debug(f"日期已调整到权限范围: {start_date} 至 {end_date}")
        
        try:
            # 聚宽API: get_price的参数是security(单只)或count，不是securities
            # 对于多只股票，需要分别获取或使用其他方法
            if isinstance(securities, str):
                # 单只股票
                data = jq.get_price(
                    security=securities,
                    start_date=start_date,
                    end_date=end_date,
                    frequency=frequency,
                    fields=fields
                )
            else:
                # 多只股票：聚宽API需要分别获取或使用get_bars
                # 这里使用循环获取每只股票的数据，然后合并
                all_data = []
                for sec in securities:
                    sec_data = jq.get_price(
                        security=sec,
                        start_date=start_date,
                        end_date=end_date,
                        frequency=frequency,
                        fields=fields
                    )
                    # 添加股票代码列以便区分
                    sec_data['security'] = sec
                    all_data.append(sec_data)
                
                # 合并数据
                if all_data:
                    data = pd.concat(all_data, ignore_index=False)
                    # 如果索引是日期，保持日期索引；否则重置索引
                    if isinstance(all_data[0].index, pd.DatetimeIndex):
                        data = data.sort_index()
                else:
                    data = pd.DataFrame()
            
            logger.info(f"获取价格数据成功: {securities}, {start_date} to {end_date}")
            return data
        except Exception as e:
            error_msg = str(e)
            logger.error(f"获取价格数据失败: {error_msg}")
            
            # 检查是否是账号权限限制错误，并更新权限信息
            if "账号权限仅能获取" in error_msg or "权限仅能获取" in error_msg:
                date_pattern = r'(\d{4}-\d{2}-\d{2})'
                dates = re.findall(date_pattern, error_msg)
                if len(dates) >= 2:
                    # 更新权限信息
                    self.permission.start_date = dates[0]
                    self.permission.end_date = dates[1]
                    self.permission.is_realtime = False
                    self.permission.detected = True
                    logger.info(f"已更新权限范围: {self.permission}")
                    
                    allowed_start = dates[0]
                    allowed_end = dates[1]
                    raise ValueError(
                        f"账号权限限制：\n"
                        f"  您请求的日期范围: {start_date} 至 {end_date}\n"
                        f"  账号允许的日期范围: {allowed_start} 至 {allowed_end}\n"
                        f"  请调整日期参数后重试。"
                    )
            
            raise
    
    def get_all_securities(self, types: List[str] = ['stock'], date: Optional[str] = None) -> pd.DataFrame:
        """
        获取所有证券信息
        
        Args:
            types: 证券类型列表 ['stock', 'fund', 'index', 'futures', 'etf', 'lof', 'fja', 'fjb']
            date: 日期，默认为当前日期
        
        Returns:
            DataFrame: 证券信息
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            data = jq.get_all_securities(types=types, date=date)
            logger.info(f"获取证券信息成功: {types}")
            return data
        except Exception as e:
            logger.error(f"获取证券信息失败: {str(e)}")
            raise
    
    def get_index_stocks(self, index_symbol: str, date: Optional[str] = None) -> List[str]:
        """
        获取指数成分股
        
        Args:
            index_symbol: 指数代码，如 '000300.XSHG' (沪深300)
            date: 日期
        
        Returns:
            List[str]: 股票代码列表
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            stocks = jq.get_index_stocks(index_symbol, date=date)
            logger.info(f"获取指数成分股成功: {index_symbol}, 共{len(stocks)}只股票")
            return stocks
        except Exception as e:
            logger.error(f"获取指数成分股失败: {str(e)}")
            raise
    
    def get_fundamentals(
        self,
        query,
        date: Optional[Union[str, date, datetime]] = None,
        statDate: Optional[str] = None
    ) -> pd.DataFrame:
        """
        获取财务数据
        
        Args:
            query: 查询对象
            date: 日期
            statDate: 统计日期
        
        Returns:
            DataFrame: 财务数据
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            data = jq.get_fundamentals(query, date=date, statDate=statDate)
            logger.info("获取财务数据成功")
            return data
        except Exception as e:
            logger.error(f"获取财务数据失败: {str(e)}")
            raise
    
    def get_concept_stocks(self, concept_code: str, date: Optional[str] = None) -> List[str]:
        """
        获取概念板块成分股（免费版支持）
        
        Args:
            concept_code: 概念代码（如 'SC0001'）或概念名称
            date: 日期，默认使用权限范围内的最新日期
        
        Returns:
            List[str]: 股票代码列表（JQData格式，如 '000001.XSHE'）
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            # 如果没有指定日期，使用权限范围内的最新日期（免费版通常是历史日期）
            if date is None:
                # 免费版通常只能访问到某个历史日期，这里使用一个保守的日期
                date = '2025-08-28'  # 可根据实际权限调整
            
            # 如果输入的是名称，尝试查找对应的代码
            if not concept_code.startswith('SC'):
                try:
                    concepts = self.get_all_concepts()
                    if not concepts.empty:
                        # 尝试精确匹配
                        matched = concepts[concepts['name'] == concept_code]
                        if not matched.empty:
                            concept_code = matched.index[0]
                            logger.info(f"将概念名称 '{concept_code}' 转换为代码: {concept_code}")
                        else:
                            # 尝试模糊匹配
                            matched = concepts[concepts['name'].str.contains(concept_code)]
                            if not matched.empty:
                                concept_code = matched.index[0]
                                name = matched.iloc[0]['name']
                                logger.info(f"将概念名称 '{concept_code}' 模糊匹配为: {name} ({concept_code})")
                except Exception as e:
                    logger.warning(f"概念名称转换失败: {e}")
            
            stocks = jq.get_concept_stocks(concept_code, date=date)
            logger.info(f"获取概念成分股成功: {concept_code}, 共{len(stocks)}只股票")
            return stocks
        except Exception as e:
            logger.error(f"获取概念成分股失败: {str(e)}")
            raise
    
    def get_industry_stocks(self, industry_code: str, date: Optional[str] = None) -> List[str]:
        """
        获取行业板块成分股（免费版支持）
        
        Args:
            industry_code: 行业代码，如 'jq.industry_sw_l1' 或行业名称
            date: 日期，默认使用权限范围内的最新日期
        
        Returns:
            List[str]: 股票代码列表
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            if date is None:
                from datetime import datetime
                date = '2025-08-28'  # 可根据实际权限调整
            
            stocks = jq.get_industry_stocks(industry_code, date=date)
            logger.info(f"获取行业成分股成功: {industry_code}, 共{len(stocks)}只股票")
            return stocks
        except Exception as e:
            logger.error(f"获取行业成分股失败: {str(e)}")
            raise
    
    def get_price_by_count(
        self,
        security: str,
        count: int = 30,
        end_date: Optional[Union[str, date, datetime]] = None,
        frequency: str = 'daily',
        fields: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        获取指定数量的历史价格数据（免费版常用方法）
        
        Args:
            security: 股票代码
            count: 获取的数据条数
            end_date: 结束日期，默认为当前日期
            frequency: 频率 ('daily', '1m', '5m'等)
            fields: 字段列表
        
        Returns:
            DataFrame: 价格数据
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        if fields is None:
            fields = ['open', 'close', 'high', 'low', 'volume']
        
        try:
            data = jq.get_price(
                security=security,
                count=count,
                end_date=end_date,
                frequency=frequency,
                fields=fields
            )
            logger.info(f"获取价格数据成功: {security}, {count}条")
            return data
        except Exception as e:
            logger.error(f"获取价格数据失败: {str(e)}")
            raise
    
    def get_all_concepts(self) -> pd.DataFrame:
        """
        获取所有概念列表（免费版支持）
        
        Returns:
            DataFrame: 概念列表，包含code和name
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            concepts = jq.get_concepts()
            logger.info(f"获取概念列表成功: {len(concepts)}个概念")
            return concepts
        except Exception as e:
            logger.error(f"获取概念列表失败: {str(e)}")
            raise
    
    def get_all_industries(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        获取所有行业列表（免费版支持）
        
        Args:
            date: 日期
        
        Returns:
            DataFrame: 行业列表
        """
        if not self._authenticated:
            raise Exception("未认证，请先调用authenticate()")
        
        try:
            if date is None:
                date = '2025-08-28'  # 可根据实际权限调整
            
            industries = jq.get_industries(date=date)
            logger.info(f"获取行业列表成功: {len(industries)}个行业")
            return industries
        except Exception as e:
            logger.error(f"获取行业列表失败: {str(e)}")
            raise

