# -*- coding: utf-8 -*-
"""
TRQuant MCP客户端模块
===================

提供统一的MCP工具调用接口，供GUI使用
"""

from .client import MCPClient, get_mcp_client

__all__ = ["MCPClient", "get_mcp_client"]
