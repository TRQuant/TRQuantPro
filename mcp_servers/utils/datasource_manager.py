"""
Phase 2.1: 数据源集成管理器

统一管理JQData/AKShare等数据源，为Tenbagger系统提供数据接口

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """数据源类型"""
    JQDATA = "jqdata"           # JQData (财务/行情)
    AKSHARE = "akshare"         # AKShare (公告/新闻)
    EASTMONEY = "eastmoney"     # 东方财富 (互动易)
    BIDDING = "bidding"         # 招投标网站
    RECRUITMENT = "recruitment" # 招聘网站
    MOCK = "mock"               # 模拟数据
    ALLTICK = "alltick"         # AllTick (实时行情/历史数据)


class DataCategory(Enum):
    """数据类别"""
    PRICE = "price"             # 行情数据
    FINANCIAL = "financial"     # 财务数据
    ANNOUNCEMENT = "announcement"  # 公告
    EVENT = "event"             # 事件
    BIDDING = "bidding"         # 招投标
    RECRUITMENT = "recruitment" # 招聘
    NEWS = "news"               # 新闻
    INTERACTIVE = "interactive" # 互动易


@dataclass
class DataRequest:
    """数据请求"""
    category: DataCategory
    symbols: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    fields: List[str] = field(default_factory=list)
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataResponse:
    """数据响应"""
    success: bool
    data: Any = None
    source: DataSourceType = DataSourceType.MOCK
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    cached: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "source": self.source.value,
            "timestamp": self.timestamp.isoformat(),
            "error": self.error,
            "cached": self.cached
        }


class BaseDataProvider(ABC):
    """数据提供者基类"""
    
    @property
    @abstractmethod
    def source_type(self) -> DataSourceType:
        pass
    
    @property
    @abstractmethod
    def supported_categories(self) -> List[DataCategory]:
        pass
    
    @abstractmethod
    def fetch(self, request: DataRequest) -> DataResponse:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass


class MockDataProvider(BaseDataProvider):
    """模拟数据提供者"""
    
    @property
    def source_type(self) -> DataSourceType:
        return DataSourceType.MOCK
    
    @property
    def supported_categories(self) -> List[DataCategory]:
        return list(DataCategory)
    
    def is_available(self) -> bool:
        return True
    
    def fetch(self, request: DataRequest) -> DataResponse:
        """生成模拟数据"""
        if request.category == DataCategory.FINANCIAL:
            data = self._mock_financial(request.symbols)
        elif request.category == DataCategory.PRICE:
            data = self._mock_price(request.symbols)
        elif request.category == DataCategory.ANNOUNCEMENT:
            data = self._mock_announcements(request.symbols)
        elif request.category == DataCategory.EVENT:
            data = self._mock_events(request.symbols)
        elif request.category == DataCategory.BIDDING:
            data = self._mock_bidding(request.symbols)
        elif request.category == DataCategory.RECRUITMENT:
            data = self._mock_recruitment(request.symbols)
        else:
            data = {}
        
        return DataResponse(success=True, data=data, source=self.source_type)
    
    def _mock_financial(self, symbols: List[str]) -> Dict[str, Dict]:
        """模拟财务数据"""
        import random
        result = {}
        for symbol in symbols:
            result[symbol] = {
                "roe": random.uniform(5, 25),
                "revenue_growth": random.uniform(-10, 80),
                "profit_growth": random.uniform(-20, 100),
                "debt_ratio": random.uniform(20, 70),
                "pe_ratio": random.uniform(10, 100),
                "pb_ratio": random.uniform(1, 10),
                "market_cap": random.uniform(50, 5000),  # 亿
                "gross_margin": random.uniform(15, 60)
            }
        return result
    
    def _mock_price(self, symbols: List[str]) -> Dict[str, Dict]:
        """模拟行情数据"""
        import random
        result = {}
        for symbol in symbols:
            base_price = random.uniform(10, 200)
            result[symbol] = {
                "current_price": base_price,
                "open": base_price * random.uniform(0.98, 1.02),
                "high": base_price * random.uniform(1.0, 1.05),
                "low": base_price * random.uniform(0.95, 1.0),
                "volume": random.randint(100000, 10000000),
                "turnover": random.uniform(0.5, 10),
                "change_pct": random.uniform(-5, 5),
                "ma5": base_price * random.uniform(0.95, 1.05),
                "ma20": base_price * random.uniform(0.9, 1.1)
            }
        return result
    
    def _mock_announcements(self, symbols: List[str]) -> Dict[str, List]:
        """模拟公告数据"""
        import random
        titles = [
            "关于签订重大合同的公告",
            "关于获得政府补贴的公告",
            "关于投资建设新项目的公告",
            "关于子公司增资的公告",
            "关于回购股份的公告",
            "关于高管增持的公告"
        ]
        result = {}
        for symbol in symbols:
            count = random.randint(0, 5)
            result[symbol] = [
                {
                    "title": random.choice(titles),
                    "date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                    "type": "positive" if random.random() > 0.3 else "neutral"
                }
                for _ in range(count)
            ]
        return result
    
    def _mock_events(self, symbols: List[str]) -> Dict[str, List]:
        """模拟事件数据"""
        import random
        events = [
            {"type": "contract", "desc": "签订大额订单"},
            {"type": "expansion", "desc": "产能扩张"},
            {"type": "rd", "desc": "研发突破"},
            {"type": "policy", "desc": "政策利好"},
            {"type": "market", "desc": "市场份额提升"}
        ]
        result = {}
        for symbol in symbols:
            count = random.randint(0, 3)
            result[symbol] = [
                {
                    **random.choice(events),
                    "date": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                    "impact": random.choice(["high", "medium", "low"])
                }
                for _ in range(count)
            ]
        return result
    
    def _mock_bidding(self, symbols: List[str]) -> Dict[str, List]:
        """模拟招投标数据"""
        import random
        result = {}
        for symbol in symbols:
            count = random.randint(0, 5)
            result[symbol] = [
                {
                    "title": f"项目招标{i+1}",
                    "amount": random.randint(100, 10000),
                    "date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()
                }
                for i in range(count)
            ]
        return result
    
    def _mock_recruitment(self, symbols: List[str]) -> Dict[str, List]:
        """模拟招聘数据"""
        import random
        jobs = ["研发工程师", "算法工程师", "产品经理", "销售经理", "运营专员"]
        result = {}
        for symbol in symbols:
            count = random.randint(0, 10)
            result[symbol] = [
                {
                    "title": random.choice(jobs),
                    "salary_range": f"{random.randint(10, 30)}-{random.randint(30, 60)}K",
                    "location": random.choice(["北京", "上海", "深圳", "杭州"]),
                    "date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
                }
                for _ in range(count)
            ]
        return result


class JQDataProvider(BaseDataProvider):
    """JQData数据提供者"""
    
    def __init__(self):
        self._authenticated = False
        self._jq = None
    
    @property
    def source_type(self) -> DataSourceType:
        return DataSourceType.JQDATA
    
    @property
    def supported_categories(self) -> List[DataCategory]:
        return [DataCategory.PRICE, DataCategory.FINANCIAL]
    
    def is_available(self) -> bool:
        if self._authenticated:
            return True
        try:
            import jqdatasdk as jq
            self._jq = jq
            return True
        except ImportError:
            return False
    
    def authenticate(self, username: str, password: str) -> bool:
        """认证JQData"""
        if not self.is_available():
            return False
        try:
            # 禁用认证提示
            if hasattr(self._jq, 'JQDataClient'):
                self._jq.JQDataClient.enable_auth_prompt = False
            self._jq.auth(username, password)
            self._authenticated = True
            logger.info("JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"JQData认证失败: {e}")
            return False
    
    def fetch(self, request: DataRequest) -> DataResponse:
        if not self._authenticated:
            return DataResponse(success=False, error="JQData未认证")
        
        try:
            if request.category == DataCategory.FINANCIAL:
                data = self._fetch_financial(request)
            elif request.category == DataCategory.PRICE:
                data = self._fetch_price(request)
            else:
                return DataResponse(success=False, error=f"不支持的数据类别: {request.category}")
            
            return DataResponse(success=True, data=data, source=self.source_type)
        except Exception as e:
            return DataResponse(success=False, error=str(e))
    
    def _fetch_financial(self, request: DataRequest) -> Dict:
        """获取财务数据"""
        from jqdatasdk import get_fundamentals, query, valuation, indicator
        
        result = {}
        for symbol in request.symbols:
            try:
                q = query(
                    valuation.code,
                    valuation.pe_ratio,
                    valuation.pb_ratio,
                    valuation.market_cap,
                    indicator.roe,
                    indicator.inc_revenue_year_on_year,
                    indicator.inc_net_profit_year_on_year
                ).filter(valuation.code == symbol)
                
                df = get_fundamentals(q)
                if not df.empty:
                    row = df.iloc[0]
                    result[symbol] = {
                        "pe_ratio": float(row.get('pe_ratio', 0) or 0),
                        "pb_ratio": float(row.get('pb_ratio', 0) or 0),
                        "market_cap": float(row.get('market_cap', 0) or 0) / 100000000,  # 转为亿
                        "roe": float(row.get('roe', 0) or 0),
                        "revenue_growth": float(row.get('inc_revenue_year_on_year', 0) or 0),
                        "profit_growth": float(row.get('inc_net_profit_year_on_year', 0) or 0)
                    }
            except Exception as e:
                logger.warning(f"获取{symbol}财务数据失败: {e}")
        
        return result
    
    def _fetch_price(self, request: DataRequest) -> Dict:
        """获取行情数据"""
        from jqdatasdk import get_price
        
        end_date = request.end_date or datetime.now()
        start_date = request.start_date or (end_date - timedelta(days=30))
        
        result = {}
        for symbol in request.symbols:
            try:
                df = get_price(symbol, start_date=start_date, end_date=end_date, 
                              frequency='daily', fields=['open', 'close', 'high', 'low', 'volume'])
                if not df.empty:
                    latest = df.iloc[-1]
                    result[symbol] = {
                        "current_price": float(latest['close']),
                        "open": float(latest['open']),
                        "high": float(latest['high']),
                        "low": float(latest['low']),
                        "volume": int(latest['volume']),
                        "change_pct": float((latest['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100) if len(df) > 1 else 0
                    }
            except Exception as e:
                logger.warning(f"获取{symbol}行情数据失败: {e}")
        
        return result


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self._providers: Dict[DataSourceType, BaseDataProvider] = {}
        self._cache: Dict[str, DataResponse] = {}
        self._cache_ttl = 300  # 5分钟缓存
        
        # 注册默认提供者
        self.register_provider(MockDataProvider())
    
    def register_provider(self, provider: BaseDataProvider):
        """注册数据提供者"""
        self._providers[provider.source_type] = provider
        logger.info(f"注册数据提供者: {provider.source_type.value}")
    
    def get_provider(self, source: DataSourceType) -> Optional[BaseDataProvider]:
        """获取数据提供者"""
        return self._providers.get(source)
    
    def fetch(self, request: DataRequest, 
              preferred_source: Optional[DataSourceType] = None,
              use_cache: bool = True) -> DataResponse:
        """获取数据"""
        # 生成缓存键
        cache_key = f"{request.category.value}_{','.join(request.symbols)}_{preferred_source}"
        
        # 检查缓存
        if use_cache and cache_key in self._cache:
            cached = self._cache[cache_key]
            if (datetime.now() - cached.timestamp).seconds < self._cache_ttl:
                cached.cached = True
                return cached
        
        # 确定数据源
        if preferred_source and preferred_source in self._providers:
            provider = self._providers[preferred_source]
            if provider.is_available() and request.category in provider.supported_categories:
                response = provider.fetch(request)
                if response.success:
                    self._cache[cache_key] = response
                    return response
        
        # 遍历可用提供者
        for source, provider in self._providers.items():
            if source == DataSourceType.MOCK:
                continue  # Mock作为最后备选
            if provider.is_available() and request.category in provider.supported_categories:
                response = provider.fetch(request)
                if response.success:
                    self._cache[cache_key] = response
                    return response
        
        # 使用Mock数据
        if DataSourceType.MOCK in self._providers:
            response = self._providers[DataSourceType.MOCK].fetch(request)
            self._cache[cache_key] = response
            return response
        
        return DataResponse(success=False, error="无可用数据源")
    
    def fetch_for_tenbagger(self, symbols: List[str]) -> Dict[str, Any]:
        """为Tenbagger系统获取完整数据"""
        result = {
            "financials": {},
            "prices": {},
            "events": {},
            "announcements": {},
            "altdata": {
                "bidding": {},
                "recruitment": {}
            }
        }
        
        # 财务数据
        resp = self.fetch(DataRequest(category=DataCategory.FINANCIAL, symbols=symbols))
        if resp.success:
            result["financials"] = resp.data
        
        # 行情数据
        resp = self.fetch(DataRequest(category=DataCategory.PRICE, symbols=symbols))
        if resp.success:
            result["prices"] = resp.data
        
        # 事件数据
        resp = self.fetch(DataRequest(category=DataCategory.EVENT, symbols=symbols))
        if resp.success:
            result["events"] = resp.data
        
        # 公告数据
        resp = self.fetch(DataRequest(category=DataCategory.ANNOUNCEMENT, symbols=symbols))
        if resp.success:
            result["announcements"] = resp.data
        
        # 另类数据
        resp = self.fetch(DataRequest(category=DataCategory.BIDDING, symbols=symbols))
        if resp.success:
            result["altdata"]["bidding"] = resp.data
        
        resp = self.fetch(DataRequest(category=DataCategory.RECRUITMENT, symbols=symbols))
        if resp.success:
            result["altdata"]["recruitment"] = resp.data
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "providers": {
                source.value: {
                    "available": provider.is_available(),
                    "categories": [c.value for c in provider.supported_categories]
                }
                for source, provider in self._providers.items()
            },
            "cache_size": len(self._cache),
            "cache_ttl": self._cache_ttl
        }
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()


# 全局实例
_datasource_manager: Optional[DataSourceManager] = None


def get_datasource_manager() -> DataSourceManager:
    global _datasource_manager
    if _datasource_manager is None:
        _datasource_manager = DataSourceManager()
    # 自动注册AllTick
    try:
        from .datasource_manager import register_alltick_provider
        register_alltick_provider(_datasource_manager)
    except Exception as e:
        logger.warning(f"自动注册AllTick失败: {e}")
    return _datasource_manager
    def __init__(self):
        self._jq = None
    
    @property
    def source_type(self) -> DataSourceType:
        return DataSourceType.JQDATA
    
    @property
    def supported_categories(self) -> List[DataCategory]:
        return [DataCategory.PRICE, DataCategory.FINANCIAL]
    
    def is_available(self) -> bool:
        try:
            from .jqdata_enhanced import get_jqdata_enhanced
            self._jq = get_jqdata_enhanced()
            return self._jq.authenticate()
        except:
            return False
    
    def fetch(self, request: DataRequest) -> DataResponse:
        if not self.is_available():
            return DataResponse(success=False, error="JQData未认证", source=self.source_type)
        
        try:
            if request.category == DataCategory.FINANCIAL:
                data = self._jq.get_fundamentals(request.symbols)
            elif request.category == DataCategory.PRICE:
                data = self._jq.get_price(request.symbols)
            else:
                return DataResponse(success=False, error=f"不支持的数据类别: {request.category}")
            
            return DataResponse(success=True, data=data, source=self.source_type)
        except Exception as e:
            return DataResponse(success=False, error=str(e), source=self.source_type)


def register_jqdata_provider(manager: DataSourceManager) -> bool:
    """注册JQData增强版到数据源管理器"""
    try:
        provider = JQDataEnhancedProvider()
        if provider.is_available():
            manager.register_provider(provider)
            return True
    except Exception as e:
        logger.warning(f"注册JQData失败: {e}")
    return False

# ==================== AllTick集成 ====================

class AllTickProvider(BaseDataProvider):
    """AllTick数据提供者（实时行情和历史数据）"""
    
    def __init__(self, api_token: str = None):
        self._alltick = None
        self._api_token = api_token or "e194fd5add8cf29b303c858939d25b59-c-app"
    
    @property
    def source_type(self) -> DataSourceType:
        return DataSourceType.ALLTICK
    
    @property
    def supported_categories(self) -> List[DataCategory]:
        return [DataCategory.PRICE]  # AllTick主要提供行情数据
    
    def is_available(self) -> bool:
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from data_sources.alltick_source import AllTickSource
            self._alltick = AllTickSource(api_token=self._api_token)
            return self._alltick.connect()
        except Exception as e:
            logger.warning(f"AllTick不可用: {e}")
            return False
    
    def fetch(self, request: DataRequest) -> DataResponse:
        if not self.is_available():
            return DataResponse(success=False, error="AllTick未连接", source=self.source_type)
        
        try:
            if request.category == DataCategory.PRICE:
                # 获取价格数据
                result = {}
                for symbol in request.symbols:
                    if request.start_date and request.end_date:
                        # 历史数据
                        df = self._alltick.get_historical_prices(
                            symbol,
                            request.start_date.strftime('%Y-%m-%d'),
                            request.end_date.strftime('%Y-%m-%d'),
                            frequency='daily'
                        )
                        if df is not None and len(df) > 0:
                            result[symbol] = {
                                'prices': df.to_dict('records'),
                                'latest_price': float(df['close'].iloc[-1])
                            }
                    else:
                        # 实时数据
                        price_info = self._alltick.get_realtime_price(symbol)
                        if price_info:
                            result[symbol] = {
                                'price': price_info['price'],
                                'volume': price_info.get('volume', 0),
                                'timestamp': price_info['timestamp'].isoformat()
                            }
                
                return DataResponse(success=True, data=result, source=self.source_type)
            else:
                return DataResponse(success=False, error=f"AllTick不支持的数据类别: {request.category}", source=self.source_type)
        except Exception as e:
            return DataResponse(success=False, error=str(e), source=self.source_type)


def register_alltick_provider(manager: DataSourceManager, api_token: str = None) -> bool:
    """注册AllTick到数据源管理器"""
    try:
        provider = AllTickProvider(api_token=api_token)
        if provider.is_available():
            manager.register_provider(provider)
            logger.info("✅ AllTick数据源已注册")
            return True
        else:
            logger.warning("⚠️ AllTick数据源不可用")
            return False
    except Exception as e:
        logger.warning(f"注册AllTick失败: {e}")
        return False
