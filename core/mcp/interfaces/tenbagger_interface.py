"""
十倍股服务接口定义

提供版本无关的接口定义，支持多版本并存和独立升级。

Author: TRQuant Team
Date: 2025-12-21
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class TenbaggerRequest:
    """
    十倍股评估请求（版本无关）
    
    所有版本的请求都使用此格式，内部适配器负责转换为具体版本的格式。
    """
    symbol: str
    name: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    version: str = "v2"  # 版本标识，用于路由到对应版本的服务
    
    def __post_init__(self):
        """后处理：设置默认值"""
        if self.name is None:
            self.name = self.symbol
        if self.data is None:
            self.data = {}


@dataclass
class TenbaggerResponse:
    """
    十倍股评估响应（版本无关）
    
    所有版本的响应都使用此格式，内部适配器负责转换。
    """
    success: bool
    report: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    version: str = "v2"  # 版本标识
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "report": self.report,
            "error": self.error,
            "version": self.version
        }


@dataclass
class TenbaggerBatchRequest:
    """批量评估请求"""
    symbols: List[str]
    max_count: Optional[int] = None
    version: str = "v2"
    
    def __post_init__(self):
        if self.max_count is None:
            self.max_count = len(self.symbols)


@dataclass
class TenbaggerRankingRequest:
    """排名请求"""
    top_n: int = 20
    min_level: str = "A"
    version: str = "v2"


class ITenbaggerService(ABC):
    """
    十倍股服务接口（抽象基类）
    
    所有版本的十倍股服务都必须实现此接口。
    这样可以确保：
    1. GUI层不依赖具体实现
    2. 算法升级不影响GUI
    3. 多版本可以并存
    """
    
    @abstractmethod
    def get_version(self) -> str:
        """获取服务版本"""
        pass
    
    @abstractmethod
    def evaluate(self, request: TenbaggerRequest) -> TenbaggerResponse:
        """
        评估单个股票
        
        Args:
            request: 评估请求
            
        Returns:
            评估响应
        """
        pass
    
    @abstractmethod
    def batch_evaluate(self, request: TenbaggerBatchRequest) -> List[TenbaggerResponse]:
        """
        批量评估股票
        
        Args:
            request: 批量评估请求
            
        Returns:
            评估响应列表
        """
        pass
    
    @abstractmethod
    def get_report(self, symbol: str) -> TenbaggerResponse:
        """
        获取股票评估报告
        
        Args:
            symbol: 股票代码
            
        Returns:
            报告响应
        """
        pass
    
    @abstractmethod
    def get_rankings(self, request: TenbaggerRankingRequest) -> List[TenbaggerResponse]:
        """
        获取股票排名
        
        Args:
            request: 排名请求
            
        Returns:
            排名响应列表
        """
        pass
    
    @abstractmethod
    def generate_report(
        self,
        format: str = "markdown",
        min_level: str = "A",
        output_path: Optional[str] = None
    ) -> TenbaggerResponse:
        """
        生成报告
        
        Args:
            format: 报告格式 (markdown/json/html)
            min_level: 最低等级
            output_path: 输出路径（可选）
            
        Returns:
            报告生成响应
        """
        pass

