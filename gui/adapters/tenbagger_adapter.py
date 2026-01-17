"""
十倍股GUI适配器（PyQt6）

连接PyQt6 GUI和MCP服务，实现版本路由和格式转换。

Author: TRQuant Team
Date: 2025-12-21
"""

from typing import Dict, Any, List, Optional
import logging

from core.mcp.client import MCPClient
from core.mcp.interfaces.tenbagger_interface import (
    TenbaggerRequest,
    TenbaggerResponse
)

logger = logging.getLogger(__name__)

# 全局适配器实例
_gui_adapter: Optional['TenbaggerGUIAdapter'] = None


class TenbaggerGUIAdapter:
    """
    十倍股GUI适配器（PyQt6）
    
    功能:
    1. 将GUI调用转换为MCP工具调用
    2. 版本路由
    3. 格式转换
    """
    
    def __init__(self, mcp_client: Optional[MCPClient] = None):
        self.mcp_client = mcp_client
        self.default_version = "v2"
    
    def _get_mcp_client(self) -> MCPClient:
        """获取MCP客户端（延迟加载）"""
        if self.mcp_client is None:
            from core.mcp.client import MCPClient
            self.mcp_client = MCPClient()
        return self.mcp_client
    
    def evaluate(
        self,
        symbol: str,
        name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        评估单个股票
        
        Args:
            symbol: 股票代码
            name: 股票名称
            data: 数据（可选）
            version: 版本（可选，默认v2）
            
        Returns:
            评估结果
        """
        version = version or self.default_version
        tool_name = f"tenbagger_{version}.evaluate"
        
        try:
            client = self._get_mcp_client()
            result = client.call_tool(tool_name, {
                "symbol": symbol,
                "name": name,
                "data": data or {},
                "version": version
            })
            return result
        except Exception as e:
            logger.error(f"评估 {symbol} 失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "version": version
            }
    
    def batch_evaluate(
        self,
        symbols: List[str],
        max_count: Optional[int] = None,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """批量评估"""
        version = version or self.default_version
        tool_name = f"tenbagger_{version}.batch"
        
        try:
            client = self._get_mcp_client()
            result = client.call_tool(tool_name, {
                "symbols": symbols,
                "max_count": max_count,
                "version": version
            })
            return result
        except Exception as e:
            logger.error(f"批量评估失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "version": version
            }
    
    def get_rankings(
        self,
        top_n: int = 20,
        min_level: str = "A",
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取排名"""
        version = version or self.default_version
        tool_name = f"tenbagger_{version}.recommendations"
        
        try:
            client = self._get_mcp_client()
            result = client.call_tool(tool_name, {
                "top_n": top_n,
                "min_level": min_level,
                "version": version
            })
            return result
        except Exception as e:
            logger.error(f"获取排名失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "version": version
            }
    
    def generate_report(
        self,
        format: str = "markdown",
        min_level: str = "A",
        output_path: Optional[str] = None,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """生成报告"""
        version = version or self.default_version
        tool_name = f"tenbagger_{version}.generate_report"
        
        try:
            client = self._get_mcp_client()
            result = client.call_tool(tool_name, {
                "format": format,
                "min_level": min_level,
                "output_path": output_path,
                "version": version
            })
            return result
        except Exception as e:
            logger.error(f"生成报告失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "version": version
            }
    
    def get_available_versions(self) -> List[str]:
        """获取可用版本列表"""
        try:
            client = self._get_mcp_client()
            result = client.call_tool("registry.list", {
                "module_type": "tenbagger"
            })
            return result.get("versions", [self.default_version])
        except Exception as e:
            logger.warning(f"获取版本列表失败: {e}")
            return [self.default_version]
    
    def set_default_version(self, version: str):
        """设置默认版本"""
        self.default_version = version


def get_tenbagger_gui_adapter(mcp_client: Optional[MCPClient] = None) -> TenbaggerGUIAdapter:
    """获取全局GUI适配器实例（单例）"""
    global _gui_adapter
    if _gui_adapter is None:
        _gui_adapter = TenbaggerGUIAdapter(mcp_client)
    return _gui_adapter
