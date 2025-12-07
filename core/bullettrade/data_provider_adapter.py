"""数据源适配器

支持多种数据源的统一接口
- JQData (聚宽)
- MiniQMT (券商QMT免费行情)
- TuShare (免费数据)
"""

from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataProviderType(Enum):
    """数据源类型"""
    JQDATA = "jqdata"
    MINIQMT = "miniqmt"
    TUSHARE = "tushare"
    AKSHARE = "akshare"
    LOCAL = "local"
    MOCK = "mock"


class DataProviderAdapter:
    """数据源适配器
    
    提供统一的数据接口，支持多种数据源切换
    
    Example:
        >>> adapter = DataProviderAdapter(DataProviderType.JQDATA)
        >>> df = adapter.get_price('000001.XSHE', '2023-01-01', '2023-12-31')
    """
    
    def __init__(self, provider_type: DataProviderType = DataProviderType.MOCK,
                 config: Optional[Dict[str, Any]] = None):
        """初始化适配器
        
        Args:
            provider_type: 数据源类型
            config: 配置参数（如API密钥等）
        """
        self.provider_type = provider_type
        self.config = config or {}
        self._provider = self._create_provider()
    
    def _create_provider(self) -> "BaseDataProvider":
        """创建数据提供器"""
        if self.provider_type == DataProviderType.JQDATA:
            return JQDataProvider(self.config)
        elif self.provider_type == DataProviderType.MINIQMT:
            return MiniQMTProvider(self.config)
        elif self.provider_type == DataProviderType.TUSHARE:
            return TuShareProvider(self.config)
        elif self.provider_type == DataProviderType.AKSHARE:
            return AKShareProvider(self.config)
        elif self.provider_type == DataProviderType.LOCAL:
            return LocalDataProvider(self.config)
        else:
            return MockDataProvider(self.config)
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        """获取历史价格
        
        Args:
            security: 证券代码
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率
            fields: 字段列表
            fq: 复权方式
            
        Returns:
            价格数据 DataFrame
        """
        return self._provider.get_price(
            security, start_date, end_date, frequency, fields, fq
        )
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        """获取实时价格
        
        Args:
            security: 证券代码
            
        Returns:
            实时价格 DataFrame
        """
        return self._provider.get_realtime_price(security)
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """获取指数成分股
        
        Args:
            index_code: 指数代码
            
        Returns:
            成分股代码列表
        """
        return self._provider.get_index_stocks(index_code)
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        """获取所有证券信息
        
        Args:
            types: 证券类型列表
            
        Returns:
            证券信息 DataFrame
        """
        return self._provider.get_all_securities(types)


class BaseDataProvider:
    """数据提供器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        raise NotImplementedError
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        raise NotImplementedError
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        raise NotImplementedError
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        raise NotImplementedError


class JQDataProvider(BaseDataProvider):
    """聚宽数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._auth()
    
    def _auth(self) -> None:
        """认证"""
        try:
            import jqdatasdk as jq
            username = self.config.get('username')
            password = self.config.get('password')
            if username and password:
                jq.auth(username, password)
                logger.info("JQData authentication successful")
        except ImportError:
            logger.warning("jqdatasdk not installed")
        except Exception as e:
            logger.error(f"JQData auth failed: {e}")
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        try:
            import jqdatasdk as jq
            return jq.get_price(
                security,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                fields=fields,
                skip_paused=False,
                fq=fq
            )
        except Exception as e:
            logger.error(f"JQData get_price failed: {e}")
            return pd.DataFrame()
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        try:
            import jqdatasdk as jq
            return jq.get_current_data()
        except Exception as e:
            logger.error(f"JQData get_realtime_price failed: {e}")
            return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        try:
            import jqdatasdk as jq
            return jq.get_index_stocks(index_code)
        except Exception as e:
            logger.error(f"JQData get_index_stocks failed: {e}")
            return []
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        try:
            import jqdatasdk as jq
            return jq.get_all_securities(types or ['stock'])
        except Exception as e:
            logger.error(f"JQData get_all_securities failed: {e}")
            return pd.DataFrame()


class MiniQMTProvider(BaseDataProvider):
    """MiniQMT 数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._init_xtquant()
    
    def _init_xtquant(self) -> None:
        """初始化 xtquant"""
        try:
            from xtquant import xtdata
            self.xtdata = xtdata
            logger.info("xtquant initialized")
        except ImportError:
            logger.warning("xtquant not installed")
            self.xtdata = None
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        if not self.xtdata:
            return pd.DataFrame()
        
        try:
            # 转换证券代码格式
            if isinstance(security, str):
                security = [security]
            
            period = '1d' if frequency == 'daily' else '1m'
            
            data = {}
            for sec in security:
                # 转换为 xtquant 格式
                xt_code = self._convert_code(sec)
                df = self.xtdata.get_market_data(
                    stock_list=[xt_code],
                    period=period,
                    start_time=start_date.replace('-', ''),
                    end_time=end_date.replace('-', '')
                )
                if xt_code in df:
                    data[sec] = df[xt_code]
            
            if len(data) == 1:
                return list(data.values())[0]
            return pd.concat(data, axis=1)
        except Exception as e:
            logger.error(f"MiniQMT get_price failed: {e}")
            return pd.DataFrame()
    
    def _convert_code(self, code: str) -> str:
        """转换代码格式"""
        code = code.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
        return code
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        if not self.xtdata:
            return pd.DataFrame()
        # 实现实时数据获取
        return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        return []
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        return pd.DataFrame()


class TuShareProvider(BaseDataProvider):
    """TuShare 数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._init_tushare()
    
    def _init_tushare(self) -> None:
        """初始化 TuShare"""
        try:
            import tushare as ts
            token = self.config.get('token')
            if token:
                ts.set_token(token)
            self.pro = ts.pro_api()
            logger.info("TuShare initialized")
        except ImportError:
            logger.warning("tushare not installed")
            self.pro = None
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        if not self.pro:
            return pd.DataFrame()
        
        try:
            if isinstance(security, str):
                security = [security]
            
            data = {}
            for sec in security:
                ts_code = self._convert_code(sec)
                adj = 'qfq' if fq == 'pre' else ('hfq' if fq == 'post' else None)
                
                df = self.pro.daily(
                    ts_code=ts_code,
                    start_date=start_date.replace('-', ''),
                    end_date=end_date.replace('-', ''),
                    adj=adj
                )
                if not df.empty:
                    df.index = pd.to_datetime(df['trade_date'])
                    df = df.sort_index()
                    data[sec] = df
            
            if len(data) == 1:
                return list(data.values())[0]
            return pd.concat(data, axis=1)
        except Exception as e:
            logger.error(f"TuShare get_price failed: {e}")
            return pd.DataFrame()
    
    def _convert_code(self, code: str) -> str:
        """转换代码格式"""
        code = code.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
        return code
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        if not self.pro:
            return []
        try:
            ts_code = self._convert_code(index_code)
            df = self.pro.index_weight(index_code=ts_code)
            return df['con_code'].tolist()
        except Exception as e:
            logger.error(f"TuShare get_index_stocks failed: {e}")
            return []
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        if not self.pro:
            return pd.DataFrame()
        try:
            return self.pro.stock_basic(list_status='L')
        except Exception as e:
            logger.error(f"TuShare get_all_securities failed: {e}")
            return pd.DataFrame()


class AKShareProvider(BaseDataProvider):
    """AKShare 数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        try:
            import akshare as ak
            # 实现 akshare 数据获取
            return pd.DataFrame()
        except ImportError:
            logger.warning("akshare not installed")
            return pd.DataFrame()
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        return []
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        return pd.DataFrame()


class LocalDataProvider(BaseDataProvider):
    """本地数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.data_path = config.get('data_path', 'data')
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        # 从本地文件读取数据
        return pd.DataFrame()
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        return []
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        return pd.DataFrame()


class MockDataProvider(BaseDataProvider):
    """模拟数据提供器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        import numpy as np
        self.np = np
    
    def get_price(self, security: Union[str, List[str]],
                  start_date: str, end_date: str,
                  frequency: str = 'daily',
                  fields: Optional[List[str]] = None,
                  fq: str = 'pre') -> pd.DataFrame:
        if fields is None:
            fields = ['open', 'close', 'high', 'low', 'volume']
        
        if isinstance(security, str):
            security = [security]
        
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        
        data = {}
        for sec in security:
            base_price = self.np.random.uniform(10, 100)
            returns = self.np.random.normal(0, 0.02, len(dates))
            prices = base_price * (1 + returns).cumprod()
            
            df = pd.DataFrame({
                'open': prices * (1 + self.np.random.uniform(-0.01, 0.01, len(dates))),
                'close': prices,
                'high': prices * (1 + self.np.random.uniform(0, 0.02, len(dates))),
                'low': prices * (1 - self.np.random.uniform(0, 0.02, len(dates))),
                'volume': self.np.random.uniform(1000000, 10000000, len(dates))
            }, index=dates)
            data[sec] = df[fields]
        
        if len(data) == 1:
            return list(data.values())[0]
        return pd.concat(data, axis=1)
    
    def get_realtime_price(self, security: Union[str, List[str]]) -> pd.DataFrame:
        if isinstance(security, str):
            security = [security]
        
        data = []
        for sec in security:
            price = self.np.random.uniform(10, 100)
            data.append({
                'code': sec,
                'price': price,
                'open': price * 0.99,
                'high': price * 1.02,
                'low': price * 0.98,
                'volume': self.np.random.uniform(1000000, 10000000)
            })
        return pd.DataFrame(data)
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        # 返回模拟的成分股
        if '300' in index_code:
            return [f"{i:06d}.XSHE" for i in range(1, 301)]
        return [f"{i:06d}.XSHE" for i in range(1, 51)]
    
    def get_all_securities(self, types: Optional[List[str]] = None) -> pd.DataFrame:
        # 返回模拟的证券列表
        codes = [f"{i:06d}" for i in range(1, 1001)]
        names = [f"股票{i}" for i in range(1, 1001)]
        return pd.DataFrame({
            'code': codes,
            'name': names,
            'start_date': '2010-01-01',
            'end_date': '2099-12-31',
            'type': 'stock'
        })

