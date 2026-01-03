"""
MCP工具辅助函数

提供统一的工具调用辅助功能，包括参数验证、错误处理等。
"""

from typing import Dict, Any, List, Optional
import json
import logging
from .parameter_validator import validate_mcp_tool_params, ParameterValidationError

logger = logging.getLogger(__name__)


def validate_and_call_tool(
    tool_name: str,
    tool_schema: Dict[str, Any],
    arguments: Dict[str, Any],
    tool_func,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """
    验证参数并调用工具函数
    
    Args:
        tool_name: 工具名称
        tool_schema: 工具的JSON Schema定义
        arguments: 工具参数
        tool_func: 工具函数
        *args, **kwargs: 传递给工具函数的额外参数
    
    Returns:
        工具调用结果，如果验证失败则返回错误响应
    """
    try:
        # 验证参数
        validated_args = validate_mcp_tool_params(tool_name, tool_schema, arguments)
        
        # 调用工具函数
        result = tool_func(validated_args, *args, **kwargs)
        
        return result
    except ParameterValidationError as e:
        logger.error(f"工具 '{tool_name}' 参数验证失败: {e.message}")
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "error": "参数验证失败",
                    "tool": tool_name,
                    "message": e.message,
                    "errors": e.errors
                }, ensure_ascii=False, indent=2)
            }],
            "isError": True
        }
    except Exception as e:
        logger.error(f"工具 '{tool_name}' 调用失败: {str(e)}")
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "error": "工具调用失败",
                    "tool": tool_name,
                    "message": str(e)
                }, ensure_ascii=False, indent=2)
            }],
            "isError": True
        }


def get_tool_schema(tool_name: str, tools_list: List[Any]) -> Optional[Dict[str, Any]]:
    """
    从工具列表中获取指定工具的Schema
    
    Args:
        tool_name: 工具名称
        tools_list: 工具列表（可以是MCPTool列表或其他格式）
    
    Returns:
        工具的Schema定义，如果未找到则返回None
    """
    for tool in tools_list:
        # 支持MCPTool对象
        if hasattr(tool, 'name') and hasattr(tool, 'input_schema'):
            if tool.name == tool_name:
                return tool.input_schema
        # 支持字典格式
        elif isinstance(tool, dict):
            if tool.get('name') == tool_name:
                return tool.get('inputSchema') or tool.get('input_schema')
    
    return None
