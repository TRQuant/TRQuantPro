"""
MCP服务器集成辅助函数

提供统一的集成辅助功能，简化MCP服务器集成新规范的工作。
"""

from typing import Dict, Any, Optional, List
import json
import logging
from .parameter_validator import validate_mcp_tool_params, ParameterValidationError
from .trace_manager import get_trace_id_from_args_or_context, TraceManager
from .mcp_tool_helper import get_tool_schema
from .error_handler import (
    MCPParameterError, MCPSystemError, MCPBusinessError,
    ErrorCodes, create_error_response
)

logger = logging.getLogger(__name__)


def process_mcp_tool_call(
    tool_name: str,
    arguments: Dict[str, Any],
    tools_list: List[Any],
    tool_handler_func,
    server_name: str = "mcp-server",
    version: str = "1.0.0"
) -> Dict[str, Any]:
    """
    处理MCP工具调用的统一流程
    
    包括：
    1. trace_id提取和设置
    2. 参数验证
    3. 错误处理
    4. 结果包装
    
    Args:
        tool_name: 工具名称
        arguments: 工具参数
        tools_list: 工具列表（用于获取schema）
        tool_handler_func: 工具处理函数
        server_name: 服务器名称
        version: 服务器版本
    
    Returns:
        标准化的工具调用结果
    """
    # 1. 提取和设置trace_id
    trace_id = get_trace_id_from_args_or_context(arguments)
    TraceManager.set_trace_id(trace_id)
    
    logger.info(f"[trace_id={trace_id}] 调用工具: {tool_name}")
    
    try:
        # 2. 获取工具schema
        tool_schema = get_tool_schema(tool_name, tools_list)
        
        # 3. 验证参数
        if tool_schema:
            try:
                validated_args = validate_mcp_tool_params(tool_name, tool_schema, arguments)
            except ParameterValidationError as e:
                error = MCPParameterError(
                    code=ErrorCodes.build_code("KB", ErrorCodes.PARAM_VALIDATION_FAILED),
                    message=f"参数验证失败: {e.message}",
                    details={"errors": e.errors},
                    trace_id=trace_id
                )
                return create_error_response(error, server_name, tool_name, version)
        else:
            validated_args = arguments
            logger.warning(f"[trace_id={trace_id}] 工具 '{tool_name}' 未找到schema，跳过参数验证")
        
        # 4. 调用工具处理函数
        result = tool_handler_func(validated_args)
        
        # 5. 包装结果（添加trace_id）
        if isinstance(result, dict):
            if "content" in result:
                # 标准MCP响应格式
                result["trace_id"] = trace_id
            else:
                # 普通字典，包装为标准格式
                result = {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(result, ensure_ascii=False, indent=2)
                    }],
                    "trace_id": trace_id
                }
        else:
            # 非字典结果，包装为标准格式
            result = {
                "content": [{
                    "type": "text",
                    "text": json.dumps({"result": result}, ensure_ascii=False, indent=2)
                }],
                "trace_id": trace_id
            }
        
        logger.info(f"[trace_id={trace_id}] 工具 '{tool_name}' 调用成功")
        return result
        
    except MCPParameterError as e:
        logger.error(f"[trace_id={trace_id}] 参数错误: {e.message}")
        return create_error_response(e, server_name, tool_name, version)
    except MCPSystemError as e:
        logger.error(f"[trace_id={trace_id}] 系统错误: {e.message}")
        return create_error_response(e, server_name, tool_name, version)
    except MCPBusinessError as e:
        logger.error(f"[trace_id={trace_id}] 业务错误: {e.message}")
        return create_error_response(e, server_name, tool_name, version)
    except Exception as e:
        logger.exception(f"[trace_id={trace_id}] 工具 '{tool_name}' 调用异常")
        error = MCPSystemError(
            code=ErrorCodes.build_code("KB", ErrorCodes.SYSTEM_INTERNAL),
            message=f"工具调用异常: {str(e)}",
            details={"exception_type": type(e).__name__},
            trace_id=trace_id
        )
        return create_error_response(error, server_name, tool_name, version)
