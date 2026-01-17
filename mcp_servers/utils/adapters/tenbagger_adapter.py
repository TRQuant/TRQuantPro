"""
十倍股MCP适配器

连接MCP工具调用和业务服务，实现版本路由和格式转换。

Author: TRQuant Team
Date: 2025-12-21
"""

from typing import Dict, Any, List, Optional
import logging

from core.mcp.interfaces.tenbagger_interface import (
    ITenbaggerService,
    TenbaggerRequest,
    TenbaggerResponse,
    TenbaggerBatchRequest,
    TenbaggerRankingRequest
)
from core.mcp.versioning.version_manager import get_version_manager

logger = logging.getLogger(__name__)

# 全局适配器实例
_adapter: Optional['TenbaggerMCPAdapter'] = None


class TenbaggerMCPAdapter:
    """
    十倍股MCP适配器
    
    功能:
    1. 将MCP工具调用转换为服务接口调用
    2. 路由到对应版本的服务
    3. 转换响应格式为MCP格式
    4. 处理版本兼容性
    """
    
    def __init__(self):
        self.version_manager = get_version_manager()
        self._register_services()
    
    def _register_services(self):
        """注册服务版本"""
        try:
            # 注册V2服务
            from mcp_servers.utils.services.tenbagger_service_v2 import TenbaggerServiceV2
            self.version_manager.register("v2", TenbaggerServiceV2, is_default=True)
            logger.info("已注册十倍股服务 V2")
        except ImportError as e:
            logger.warning(f"注册V2服务失败: {e}")
    
    async def handle_evaluate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理 tenbagger_v2.evaluate 工具调用
        
        Args:
            args: MCP工具参数
            
        Returns:
            MCP格式的响应
        """
        try:
            # 1. 解析请求
            version = args.get("version", "v2")
            request = TenbaggerRequest(
                symbol=args.get("symbol"),
                name=args.get("name"),
                data=args.get("data", {}),
                version=version
            )
            
            if not request.symbol:
                return {"success": False, "error": "缺少必需参数: symbol"}
            
            # 2. 获取对应版本的服务
            service: ITenbaggerService = self.version_manager.get_service(version)
            
            # 3. 调用服务
            response = service.evaluate(request)
            
            # 4. 转换为MCP响应格式
            return response.to_dict()
            
        except Exception as e:
            logger.error(f"tenbagger.evaluate 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v2")}
    
    async def handle_batch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理批量评估"""
        try:
            version = args.get("version", "v2")
            request = TenbaggerBatchRequest(
                symbols=args.get("symbols", []),
                max_count=args.get("max_count"),
                version=version
            )
            
            if not request.symbols:
                return {"success": False, "error": "缺少必需参数: symbols"}
            
            service: ITenbaggerService = self.version_manager.get_service(version)
            responses = service.batch_evaluate(request)
            
            return {
                "success": True,
                "count": len(responses),
                "reports": [r.to_dict() for r in responses],
                "version": version
            }
        except Exception as e:
            logger.error(f"tenbagger.batch 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v2")}
    
    async def handle_get_report(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理获取报告"""
        try:
            version = args.get("version", "v2")
            symbol = args.get("symbol")
            
            if not symbol:
                return {"success": False, "error": "缺少必需参数: symbol"}
            
            service: ITenbaggerService = self.version_manager.get_service(version)
            response = service.get_report(symbol)
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"tenbagger.get_report 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v2")}
    
    async def handle_get_rankings(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理获取排名"""
        try:
            version = args.get("version", "v2")
            request = TenbaggerRankingRequest(
                top_n=args.get("top_n", 20),
                min_level=args.get("min_level", "A"),
                version=version
            )
            
            service: ITenbaggerService = self.version_manager.get_service(version)
            responses = service.get_rankings(request)
            
            return {
                "success": True,
                "count": len(responses),
                "rankings": [r.to_dict() for r in responses],
                "version": version
            }
        except Exception as e:
            logger.error(f"tenbagger.get_rankings 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v2")}
    
    async def handle_generate_report(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理生成报告"""
        try:
            version = args.get("version", "v2")
            service: ITenbaggerService = self.version_manager.get_service(version)
            
            response = service.generate_report(
                format=args.get("format", "markdown"),
                min_level=args.get("min_level", "A"),
                output_path=args.get("output_path")
            )
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"tenbagger.generate_report 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v2")}
    
    def get_available_versions(self) -> List[str]:
        """获取可用版本列表"""
        return self.version_manager.list_versions()


def get_tenbagger_adapter() -> TenbaggerMCPAdapter:
    """获取全局适配器实例（单例）"""
    global _adapter
    if _adapter is None:
        _adapter = TenbaggerMCPAdapter()
    return _adapter

