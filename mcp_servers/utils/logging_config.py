# -*- coding: utf-8 -*-
"""
MCP 服务器日志配置
================
Phase 2 Task 2.2.2: MCP服务器监控和日志

提供:
1. 结构化日志
2. 性能日志
3. 调用链日志
4. 告警机制
"""

import os
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


# ==================== 结构化日志格式化 ====================

class StructuredFormatter(logging.Formatter):
    """
    结构化日志格式化器
    
    输出 JSON 格式日志，便于日志分析
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加额外字段
        if hasattr(record, "trace_id"):
            log_data["trace_id"] = record.trace_id
        if hasattr(record, "server"):
            log_data["server"] = record.server
        if hasattr(record, "tool"):
            log_data["tool"] = record.tool
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data
        
        # 异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class HumanReadableFormatter(logging.Formatter):
    """
    人类可读格式化器
    
    用于控制台输出
    """
    
    COLORS = {
        "DEBUG": "\033[36m",    # 青色
        "INFO": "\033[32m",     # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",    # 红色
        "CRITICAL": "\033[35m", # 紫色
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        
        # 基本格式
        timestamp = datetime.now().strftime("%H:%M:%S")
        level = f"{color}{record.levelname:8}{self.RESET}"
        
        # 构建消息
        msg = f"{timestamp} {level} [{record.name}] {record.getMessage()}"
        
        # 添加追踪信息
        extras = []
        if hasattr(record, "trace_id"):
            extras.append(f"trace={record.trace_id}")
        if hasattr(record, "duration_ms"):
            extras.append(f"time={record.duration_ms:.2f}ms")
        if hasattr(record, "server"):
            extras.append(f"server={record.server}")
        
        if extras:
            msg += f" ({', '.join(extras)})"
        
        # 异常信息
        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"
        
        return msg


# ==================== MCP 日志适配器 ====================

class MCPLoggerAdapter(logging.LoggerAdapter):
    """
    MCP 日志适配器
    
    自动添加上下文信息
    """
    
    def process(self, msg: str, kwargs: Dict) -> tuple:
        extra = kwargs.get("extra", {})
        
        # 从上下文获取 trace_id
        from mcp_servers.utils.mcp_standard import TraceManager
        trace_id = TraceManager.get()
        if trace_id:
            extra["trace_id"] = trace_id
        
        # 合并额外信息
        extra.update(self.extra)
        kwargs["extra"] = extra
        
        return msg, kwargs
    
    def tool_call(self, tool_name: str, args: Dict = None, **kwargs):
        """记录工具调用"""
        self.info(
            f"工具调用: {tool_name}",
            extra={"tool": tool_name, "args": args, **kwargs}
        )
    
    def tool_result(self, tool_name: str, success: bool, duration_ms: float, **kwargs):
        """记录工具结果"""
        level = logging.INFO if success else logging.ERROR
        self.log(
            level,
            f"工具完成: {tool_name} {'✅' if success else '❌'}",
            extra={"tool": tool_name, "duration_ms": duration_ms, "success": success, **kwargs}
        )
    
    def slow_request(self, tool_name: str, duration_ms: float, threshold_ms: float = 500):
        """记录慢请求"""
        self.warning(
            f"慢请求: {tool_name} 耗时 {duration_ms:.2f}ms (阈值: {threshold_ms}ms)",
            extra={"tool": tool_name, "duration_ms": duration_ms, "threshold_ms": threshold_ms}
        )


# ==================== 日志配置 ====================

def setup_logging(
    log_dir: str = "logs",
    level: str = "INFO",
    json_format: bool = False,
    console: bool = True,
    file: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
):
    """
    配置日志系统
    
    Args:
        log_dir: 日志目录
        level: 日志级别
        json_format: 是否使用 JSON 格式
        console: 是否输出到控制台
        file: 是否输出到文件
        max_bytes: 单文件最大字节数
        backup_count: 保留备份数量
    """
    # 创建日志目录
    if file and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            StructuredFormatter() if json_format else HumanReadableFormatter()
        )
        root_logger.addHandler(console_handler)
    
    # 文件处理器
    if file:
        # 主日志文件
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "mcp_server.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(file_handler)
        
        # 错误日志文件
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, "mcp_error.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(error_handler)
        
        # 性能日志文件
        perf_handler = RotatingFileHandler(
            os.path.join(log_dir, "mcp_performance.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        perf_handler.setLevel(logging.INFO)
        perf_handler.setFormatter(StructuredFormatter())
        perf_handler.addFilter(PerformanceLogFilter())
        root_logger.addHandler(perf_handler)
    
    return root_logger


class PerformanceLogFilter(logging.Filter):
    """性能日志过滤器"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        # 只记录包含 duration_ms 的日志
        return hasattr(record, "duration_ms")


# ==================== 获取日志器 ====================

def get_mcp_logger(name: str, server_name: str = None) -> MCPLoggerAdapter:
    """
    获取 MCP 日志器
    
    Args:
        name: 日志器名称
        server_name: 服务器名称
        
    Returns:
        MCP 日志适配器
    """
    logger = logging.getLogger(name)
    extra = {}
    if server_name:
        extra["server"] = server_name
    return MCPLoggerAdapter(logger, extra)


# ==================== 告警机制 ====================

class AlertManager:
    """
    告警管理器
    
    支持:
    - 错误告警
    - 慢请求告警
    - 阈值告警
    """
    
    _instance: Optional["AlertManager"] = None
    _handlers: list = []
    
    @classmethod
    def get_instance(cls) -> "AlertManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_handler(self, handler: callable):
        """添加告警处理器"""
        self._handlers.append(handler)
    
    def alert(self, level: str, message: str, context: Dict[str, Any] = None):
        """
        发送告警
        
        Args:
            level: 告警级别 (info, warning, error, critical)
            message: 告警消息
            context: 上下文信息
        """
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "context": context or {},
        }
        
        # 记录日志
        logger = logging.getLogger("alert")
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.log(log_level, f"[ALERT] {message}", extra={"alert": alert_data})
        
        # 调用处理器
        for handler in self._handlers:
            try:
                handler(alert_data)
            except Exception as e:
                logger.error(f"告警处理器执行失败: {e}")
    
    def error_alert(self, tool_name: str, error: str, trace_id: str = None):
        """错误告警"""
        self.alert("error", f"工具 {tool_name} 执行失败: {error}", {
            "tool": tool_name,
            "trace_id": trace_id,
        })
    
    def slow_request_alert(self, tool_name: str, duration_ms: float, threshold_ms: float = 500):
        """慢请求告警"""
        if duration_ms > threshold_ms:
            self.alert("warning", f"慢请求: {tool_name} 耗时 {duration_ms:.2f}ms", {
                "tool": tool_name,
                "duration_ms": duration_ms,
                "threshold_ms": threshold_ms,
            })
    
    def threshold_alert(self, metric_name: str, value: float, threshold: float):
        """阈值告警"""
        self.alert("warning", f"指标 {metric_name} 超过阈值: {value} > {threshold}", {
            "metric": metric_name,
            "value": value,
            "threshold": threshold,
        })


def get_alert_manager() -> AlertManager:
    """获取告警管理器"""
    return AlertManager.get_instance()


# ==================== 导出 ====================

__all__ = [
    "StructuredFormatter",
    "HumanReadableFormatter",
    "MCPLoggerAdapter",
    "setup_logging",
    "get_mcp_logger",
    "AlertManager",
    "get_alert_manager",
]
