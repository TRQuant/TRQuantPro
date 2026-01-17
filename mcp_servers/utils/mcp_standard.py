# -*- coding: utf-8 -*-
"""
MCP 标准化工具库
================
Phase 2 Task 2.1: MCP服务器优化

统一所有 MCP 服务器的：
1. 命名规范
2. 参数验证
3. trace_id 追踪
4. 错误码处理
5. 响应格式

使用方式:
    from mcp_servers.utils.mcp_standard import (
        MCPStandard,
        create_tool_handler,
        validate_params,
        wrap_response,
    )
"""

import uuid
import json
import time
import logging
import threading
import functools
from enum import Enum
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple, TypeVar
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


# ==================== 错误码定义 ====================

class ErrorCode(Enum):
    """统一错误码（模块_类型_编号）"""
    
    # 成功
    SUCCESS = "SUCCESS"
    
    # 参数错误 (1xx)
    PARAM_MISSING = "PARAM_101"           # 缺少必填参数
    PARAM_TYPE_ERROR = "PARAM_102"        # 参数类型错误
    PARAM_FORMAT_ERROR = "PARAM_103"      # 参数格式错误
    PARAM_RANGE_ERROR = "PARAM_104"       # 参数范围错误
    PARAM_VALIDATION = "PARAM_105"        # 参数验证失败
    
    # 数据错误 (2xx)
    DATA_NOT_FOUND = "DATA_201"           # 数据不存在
    DATA_FORMAT_ERROR = "DATA_202"        # 数据格式错误
    DATA_ACCESS_ERROR = "DATA_203"        # 数据访问失败
    DATA_SOURCE_ERROR = "DATA_204"        # 数据源错误
    DATA_EXPIRED = "DATA_205"             # 数据过期
    
    # 业务错误 (3xx)
    BUSINESS_NOT_FOUND = "BIZ_301"        # 资源不存在
    BUSINESS_FORBIDDEN = "BIZ_302"        # 操作被禁止
    BUSINESS_CONFLICT = "BIZ_303"         # 操作冲突
    BUSINESS_RULE_VIOLATION = "BIZ_304"   # 违反业务规则
    BUSINESS_OPERATION_FAILED = "BIZ_305" # 操作失败
    
    # 系统错误 (5xx)
    SYSTEM_INTERNAL = "SYS_501"           # 内部错误
    SYSTEM_UNAVAILABLE = "SYS_502"        # 服务不可用
    SYSTEM_TIMEOUT = "SYS_503"            # 超时
    SYSTEM_RESOURCE = "SYS_504"           # 资源不足
    SYSTEM_DEPENDENCY = "SYS_505"         # 依赖错误
    
    def to_http_status(self) -> int:
        """转换为HTTP状态码（用于参考）"""
        if self.value.startswith("PARAM"):
            return 400
        elif self.value.startswith("DATA"):
            return 404 if "NOT_FOUND" in self.value else 422
        elif self.value.startswith("BIZ"):
            if "NOT_FOUND" in self.value:
                return 404
            elif "FORBIDDEN" in self.value:
                return 403
            elif "CONFLICT" in self.value:
                return 409
            return 422
        elif self.value.startswith("SYS"):
            if "UNAVAILABLE" in self.value:
                return 503
            elif "TIMEOUT" in self.value:
                return 504
            return 500
        return 200 if self == ErrorCode.SUCCESS else 500


# ==================== trace_id 管理 ====================

class TraceManager:
    """trace_id 管理器（增强版）"""
    
    _local = threading.local()
    _store: Dict[str, Dict[str, Any]] = {}  # trace_id -> metadata
    _lock = threading.Lock()
    
    @classmethod
    def generate(cls) -> str:
        """生成新的 trace_id"""
        return str(uuid.uuid4())[:12]  # 短格式
    
    @classmethod
    def set(cls, trace_id: str, metadata: Dict[str, Any] = None):
        """设置当前线程的 trace_id"""
        cls._local.trace_id = trace_id
        if metadata:
            with cls._lock:
                cls._store[trace_id] = {
                    **metadata,
                    "created_at": datetime.now().isoformat(),
                }
    
    @classmethod
    def get(cls) -> Optional[str]:
        """获取当前 trace_id"""
        return getattr(cls._local, 'trace_id', None)
    
    @classmethod
    def get_or_create(cls, args: Dict[str, Any] = None) -> str:
        """从参数或上下文获取 trace_id，没有则创建"""
        # 从参数获取
        if args and 'trace_id' in args:
            trace_id = args['trace_id']
            cls.set(trace_id)
            return trace_id
        
        # 从上下文获取
        trace_id = cls.get()
        if trace_id:
            return trace_id
        
        # 创建新的
        trace_id = cls.generate()
        cls.set(trace_id)
        return trace_id
    
    @classmethod
    def clear(cls):
        """清除当前 trace_id"""
        if hasattr(cls._local, 'trace_id'):
            delattr(cls._local, 'trace_id')
    
    @classmethod
    def add_span(cls, trace_id: str, span_name: str, data: Dict[str, Any] = None):
        """添加追踪 span（用于调用链跟踪）"""
        with cls._lock:
            if trace_id not in cls._store:
                cls._store[trace_id] = {"spans": [], "created_at": datetime.now().isoformat()}
            
            cls._store[trace_id].setdefault("spans", []).append({
                "name": span_name,
                "timestamp": datetime.now().isoformat(),
                "data": data or {}
            })
    
    @classmethod
    def get_trace(cls, trace_id: str) -> Optional[Dict[str, Any]]:
        """获取完整追踪信息"""
        return cls._store.get(trace_id)


class TraceContext:
    """trace_id 上下文管理器"""
    
    def __init__(self, trace_id: str = None, server_name: str = None, tool_name: str = None):
        self.trace_id = trace_id or TraceManager.generate()
        self.server_name = server_name
        self.tool_name = tool_name
        self.old_trace_id = None
        self.start_time = None
    
    def __enter__(self):
        self.old_trace_id = TraceManager.get()
        self.start_time = time.time()
        TraceManager.set(self.trace_id, {
            "server": self.server_name,
            "tool": self.tool_name,
        })
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 记录耗时
        duration = time.time() - self.start_time
        TraceManager.add_span(self.trace_id, "complete", {
            "duration_ms": round(duration * 1000, 2),
            "success": exc_type is None,
            "error": str(exc_val) if exc_val else None
        })
        
        # 恢复旧 trace_id
        if self.old_trace_id:
            TraceManager.set(self.old_trace_id)
        else:
            TraceManager.clear()
        
        return False


# ==================== 参数验证 ====================

class ParamValidator:
    """参数验证器（增强版）"""
    
    @staticmethod
    def validate(schema: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        验证参数
        
        Args:
            schema: JSON Schema
            params: 参数
            
        Returns:
            (success, validated_params, errors)
        """
        errors = []
        validated = params.copy()
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        # 检查必填参数
        for field in required:
            if field not in params or params[field] is None:
                errors.append(f"缺少必填参数: {field}")
        
        # 应用默认值和类型检查
        for field, field_schema in properties.items():
            # 应用默认值
            if field not in validated and "default" in field_schema:
                validated[field] = field_schema["default"]
            
            # 类型检查
            if field in validated:
                value = validated[field]
                expected_type = field_schema.get("type")
                
                if expected_type and not ParamValidator._check_type(value, expected_type):
                    errors.append(f"参数 {field} 类型错误，期望 {expected_type}")
                
                # 枚举检查
                if "enum" in field_schema and value not in field_schema["enum"]:
                    errors.append(f"参数 {field} 值无效，允许值: {field_schema['enum']}")
                
                # 范围检查
                if "minimum" in field_schema and isinstance(value, (int, float)):
                    if value < field_schema["minimum"]:
                        errors.append(f"参数 {field} 小于最小值 {field_schema['minimum']}")
                
                if "maximum" in field_schema and isinstance(value, (int, float)):
                    if value > field_schema["maximum"]:
                        errors.append(f"参数 {field} 大于最大值 {field_schema['maximum']}")
        
        return len(errors) == 0, validated, errors
    
    @staticmethod
    def _check_type(value: Any, expected_type: str) -> bool:
        """检查类型"""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        
        if expected_type not in type_map:
            return True
        
        expected = type_map[expected_type]
        return isinstance(value, expected)


# ==================== 响应格式 ====================

@dataclass
class MCPResponse:
    """MCP 标准响应"""
    success: bool = True
    data: Any = None
    error_code: str = None
    error_message: str = None
    error_details: Dict[str, Any] = None
    
    trace_id: str = None
    server_name: str = None
    tool_name: str = None
    version: str = "1.0.0"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_ms: float = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转为字典"""
        result = {
            "success": self.success,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
        }
        
        if self.success:
            result["data"] = self.data
        else:
            result["error"] = {
                "code": self.error_code,
                "message": self.error_message,
            }
            if self.error_details:
                result["error"]["details"] = self.error_details
        
        if self.server_name:
            result["server"] = self.server_name
        if self.tool_name:
            result["tool"] = self.tool_name
        if self.duration_ms is not None:
            result["duration_ms"] = self.duration_ms
        
        return result
    
    def to_json(self) -> str:
        """转为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def wrap_success(
    data: Any,
    trace_id: str = None,
    server_name: str = None,
    tool_name: str = None
) -> Dict[str, Any]:
    """包装成功响应"""
    return MCPResponse(
        success=True,
        data=data,
        trace_id=trace_id or TraceManager.get(),
        server_name=server_name,
        tool_name=tool_name,
    ).to_dict()


def wrap_error(
    error_code: ErrorCode,
    error_message: str,
    error_details: Dict[str, Any] = None,
    trace_id: str = None,
    server_name: str = None,
    tool_name: str = None
) -> Dict[str, Any]:
    """包装错误响应"""
    return MCPResponse(
        success=False,
        error_code=error_code.value,
        error_message=error_message,
        error_details=error_details,
        trace_id=trace_id or TraceManager.get(),
        server_name=server_name,
        tool_name=tool_name,
    ).to_dict()


# ==================== MCP 标准工具基类 ====================

class MCPStandard:
    """
    MCP 标准化工具基类
    
    提供统一的：
    - 参数验证
    - trace_id 追踪
    - 错误处理
    - 响应格式
    
    使用方式:
        class MyServer(MCPStandard):
            SERVER_NAME = "my-server"
            SERVER_VERSION = "1.0.0"
            
            TOOLS = [
                Tool(name="my.tool", ...)
            ]
            
            async def handle_my_tool(self, args: Dict) -> Dict:
                return {"result": "ok"}
    """
    
    SERVER_NAME: str = "mcp-server"
    SERVER_VERSION: str = "1.0.0"
    TOOLS: List = []
    
    def __init__(self):
        self._tool_schemas: Dict[str, Dict] = {}
        self._setup_tool_schemas()
    
    def _setup_tool_schemas(self):
        """设置工具 Schema"""
        for tool in self.TOOLS:
            self._tool_schemas[tool.name] = tool.inputSchema
    
    def get_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """获取工具 Schema"""
        return self._tool_schemas.get(tool_name)
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的工具调用入口
        
        自动处理：
        - trace_id 追踪
        - 参数验证
        - 错误处理
        - 响应格式化
        """
        start_time = time.time()
        trace_id = TraceManager.get_or_create(arguments)
        
        with TraceContext(trace_id, self.SERVER_NAME, name):
            try:
                # 1. 参数验证
                schema = self.get_schema(name)
                if schema:
                    valid, validated_args, errors = ParamValidator.validate(schema, arguments)
                    if not valid:
                        return wrap_error(
                            ErrorCode.PARAM_VALIDATION,
                            f"参数验证失败: {', '.join(errors)}",
                            {"validation_errors": errors},
                            trace_id, self.SERVER_NAME, name
                        )
                    arguments = validated_args
                
                # 2. 调用处理器
                handler_name = f"handle_{name.replace('.', '_')}"
                handler = getattr(self, handler_name, None)
                
                if handler is None:
                    return wrap_error(
                        ErrorCode.BUSINESS_NOT_FOUND,
                        f"未找到工具处理器: {name}",
                        trace_id=trace_id,
                        server_name=self.SERVER_NAME,
                        tool_name=name
                    )
                
                # 3. 执行
                result = await handler(arguments)
                
                # 4. 包装响应
                duration_ms = (time.time() - start_time) * 1000
                
                if isinstance(result, dict) and "success" in result:
                    # 已经是标准格式
                    result["trace_id"] = trace_id
                    result["duration_ms"] = round(duration_ms, 2)
                    return result
                
                return {
                    "success": True,
                    "data": result,
                    "trace_id": trace_id,
                    "server": self.SERVER_NAME,
                    "tool": name,
                    "duration_ms": round(duration_ms, 2)
                }
                
            except Exception as e:
                logger.exception(f"工具调用异常: {self.SERVER_NAME}.{name}")
                
                error_code = self._map_exception(e)
                
                return wrap_error(
                    error_code,
                    str(e),
                    {"exception_type": type(e).__name__},
                    trace_id, self.SERVER_NAME, name
                )
    
    def _map_exception(self, e: Exception) -> ErrorCode:
        """映射异常到错误码"""
        if isinstance(e, ValueError):
            return ErrorCode.PARAM_VALIDATION
        elif isinstance(e, TypeError):
            return ErrorCode.PARAM_TYPE_ERROR
        elif isinstance(e, FileNotFoundError):
            return ErrorCode.DATA_NOT_FOUND
        elif isinstance(e, PermissionError):
            return ErrorCode.BUSINESS_FORBIDDEN
        elif isinstance(e, TimeoutError):
            return ErrorCode.SYSTEM_TIMEOUT
        elif isinstance(e, ConnectionError):
            return ErrorCode.SYSTEM_UNAVAILABLE
        else:
            return ErrorCode.SYSTEM_INTERNAL


# ==================== 装饰器 ====================

def mcp_tool(
    schema: Dict[str, Any] = None,
    server_name: str = None,
    validate: bool = True
):
    """
    MCP 工具装饰器
    
    自动处理参数验证、trace_id、错误处理
    
    使用方式:
        @mcp_tool(schema=MY_SCHEMA, server_name="my-server")
        async def my_handler(args: Dict) -> Dict:
            return {"result": "ok"}
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(args: Dict[str, Any]) -> Dict[str, Any]:
            start_time = time.time()
            trace_id = TraceManager.get_or_create(args)
            tool_name = func.__name__.replace("_handle_", "").replace("handle_", "")
            
            with TraceContext(trace_id, server_name, tool_name):
                try:
                    # 参数验证
                    if validate and schema:
                        valid, validated_args, errors = ParamValidator.validate(schema, args)
                        if not valid:
                            return wrap_error(
                                ErrorCode.PARAM_VALIDATION,
                                f"参数验证失败: {', '.join(errors)}",
                                {"validation_errors": errors},
                                trace_id, server_name, tool_name
                            )
                        args = validated_args
                    
                    # 执行
                    result = await func(args)
                    
                    # 包装响应
                    duration_ms = (time.time() - start_time) * 1000
                    
                    if isinstance(result, dict):
                        result.setdefault("success", True)
                        result["trace_id"] = trace_id
                        result["duration_ms"] = round(duration_ms, 2)
                        return result
                    
                    return wrap_success(result, trace_id, server_name, tool_name)
                    
                except Exception as e:
                    logger.exception(f"工具执行异常: {tool_name}")
                    return wrap_error(
                        ErrorCode.SYSTEM_INTERNAL,
                        str(e),
                        {"exception_type": type(e).__name__},
                        trace_id, server_name, tool_name
                    )
        
        return wrapper
    return decorator


# ==================== 命名规范检查 ====================

class NamingConvention:
    """命名规范检查"""
    
    # 工具命名规范: module.action 或 module.sub_action
    TOOL_NAME_PATTERN = r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9_]*)+$'
    
    # 服务器命名规范: xxx-server
    SERVER_NAME_PATTERN = r'^[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*-server$'
    
    @staticmethod
    def validate_tool_name(name: str) -> Tuple[bool, str]:
        """验证工具名称"""
        import re
        
        if not name:
            return False, "工具名称不能为空"
        
        if not re.match(NamingConvention.TOOL_NAME_PATTERN, name):
            return False, f"工具名称格式错误，应为 'module.action' 格式，例如 'data.query'"
        
        return True, ""
    
    @staticmethod
    def validate_server_name(name: str) -> Tuple[bool, str]:
        """验证服务器名称"""
        import re
        
        if not name:
            return False, "服务器名称不能为空"
        
        if not re.match(NamingConvention.SERVER_NAME_PATTERN, name):
            return False, f"服务器名称格式错误，应为 'xxx-server' 格式"
        
        return True, ""
    
    @staticmethod
    def suggest_tool_name(description: str) -> str:
        """根据描述建议工具名称"""
        # 简单的建议逻辑
        keywords = {
            "获取": "get",
            "查询": "query",
            "列表": "list",
            "创建": "create",
            "更新": "update",
            "删除": "delete",
            "生成": "generate",
            "分析": "analyze",
            "回测": "backtest",
            "报告": "report",
            "策略": "strategy",
            "因子": "factor",
            "数据": "data",
            "市场": "market",
        }
        
        for cn, en in keywords.items():
            if cn in description:
                return f"module.{en}"
        
        return "module.action"


# ==================== 导出 ====================

__all__ = [
    # 错误码
    "ErrorCode",
    # trace_id
    "TraceManager",
    "TraceContext",
    # 参数验证
    "ParamValidator",
    # 响应格式
    "MCPResponse",
    "wrap_success",
    "wrap_error",
    # 基类
    "MCPStandard",
    # 装饰器
    "mcp_tool",
    # 命名规范
    "NamingConvention",
]
