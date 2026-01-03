"""
错误处理模块
============

提供统一的错误处理机制，包括：
- 装饰器：自动捕获和记录异常
- 重试机制：API调用失败时自动重试
- 降级方案：提供备用数据或默认值
- 友好提示：将技术错误转换为用户友好的消息

使用方式:
    from notebooks.lib.error_handling import safe_call, retry_on_failure, with_fallback
    
    @safe_call(default=None)
    def risky_operation():
        ...
        
    @retry_on_failure(max_retries=3)
    def api_call():
        ...
"""

import logging
import functools
import time
import traceback
from typing import Any, Callable, Optional, TypeVar, Union, Dict
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class ErrorInfo:
    """错误信息记录"""
    error_type: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    traceback: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback,
            "context": self.context
        }


# 错误历史记录
_error_history: list = []


def record_error(error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
    """记录错误到历史"""
    info = ErrorInfo(
        error_type=type(error).__name__,
        message=str(error),
        traceback=traceback.format_exc(),
        context=context or {}
    )
    _error_history.append(info)
    
    # 限制历史记录数量
    if len(_error_history) > 100:
        _error_history.pop(0)
    
    return info


def get_error_history() -> list:
    """获取错误历史"""
    return _error_history.copy()


def clear_error_history():
    """清空错误历史"""
    _error_history.clear()


def safe_call(
    default: Any = None,
    log_error: bool = True,
    raise_on_error: bool = False,
    error_message: str = None
) -> Callable:
    """
    安全调用装饰器 - 捕获异常并返回默认值
    
    Args:
        default: 发生异常时返回的默认值
        log_error: 是否记录错误日志
        raise_on_error: 是否重新抛出异常
        error_message: 自定义错误消息
        
    使用示例:
        @safe_call(default=[])
        def get_stock_list():
            return jq.get_all_securities()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = error_message or f"{func.__name__} 执行失败"
                
                if log_error:
                    logger.error(f"❌ {msg}: {e}")
                    record_error(e, {"function": func.__name__, "args": str(args)[:100]})
                
                if raise_on_error:
                    raise
                
                return default
        return wrapper
    return decorator


def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Callable = None
) -> Callable:
    """
    重试装饰器 - API调用失败时自动重试
    
    Args:
        max_retries: 最大重试次数
        delay: 初始延迟时间（秒）
        backoff: 延迟倍增因子
        exceptions: 需要重试的异常类型
        on_retry: 重试时的回调函数
        
    使用示例:
        @retry_on_failure(max_retries=3, delay=1.0)
        def fetch_data_from_api():
            return api.get_data()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        logger.warning(
                            f"⚠️ {func.__name__} 失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}"
                        )
                        
                        if on_retry:
                            on_retry(attempt, e)
                        
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"❌ {func.__name__} 重试 {max_retries} 次后仍然失败")
                        record_error(e, {"function": func.__name__, "retries": max_retries})
            
            raise last_exception
        return wrapper
    return decorator


def with_fallback(
    fallback_func: Callable = None,
    fallback_value: Any = None,
    log_fallback: bool = True
) -> Callable:
    """
    降级装饰器 - 提供备用方案
    
    Args:
        fallback_func: 备用函数
        fallback_value: 备用值（如果没有备用函数）
        log_fallback: 是否记录降级日志
        
    使用示例:
        def get_local_data():
            return load_from_cache()
            
        @with_fallback(fallback_func=get_local_data)
        def get_remote_data():
            return api.fetch()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_fallback:
                    logger.warning(f"⚠️ {func.__name__} 失败，使用降级方案: {e}")
                
                if fallback_func:
                    try:
                        return fallback_func(*args, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"❌ 降级方案也失败: {fallback_error}")
                        if fallback_value is not None:
                            return fallback_value
                        raise
                elif fallback_value is not None:
                    return fallback_value
                else:
                    raise
        return wrapper
    return decorator


@contextmanager
def error_context(operation_name: str, default_value: Any = None, suppress: bool = True):
    """
    错误上下文管理器 - 用于 with 语句
    
    Args:
        operation_name: 操作名称（用于日志）
        default_value: 发生异常时的默认值
        suppress: 是否抑制异常
        
    使用示例:
        with error_context("获取市场数据", default_value=[]):
            data = jq.get_price(...)
    """
    try:
        yield
    except Exception as e:
        logger.error(f"❌ {operation_name} 失败: {e}")
        record_error(e, {"operation": operation_name})
        
        if not suppress:
            raise


class ErrorBoundary:
    """
    错误边界类 - 用于包装可能出错的操作
    
    使用示例:
        with ErrorBoundary("数据获取") as eb:
            data = fetch_data()
            
        if eb.has_error:
            print(f"发生错误: {eb.error_message}")
            data = eb.default_value or []
    """
    
    def __init__(
        self,
        operation_name: str,
        default_value: Any = None,
        suppress: bool = True,
        on_error: Callable = None
    ):
        self.operation_name = operation_name
        self.default_value = default_value
        self.suppress = suppress
        self.on_error = on_error
        
        self.has_error = False
        self.error: Optional[Exception] = None
        self.error_message: str = ""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.has_error = True
            self.error = exc_val
            self.error_message = str(exc_val)
            
            logger.error(f"❌ {self.operation_name} 失败: {exc_val}")
            record_error(exc_val, {"operation": self.operation_name})
            
            if self.on_error:
                self.on_error(exc_val)
            
            return self.suppress
        return False


# 常用错误类型的友好消息映射
ERROR_MESSAGES = {
    "ConnectionError": "网络连接失败，请检查网络状态",
    "TimeoutError": "请求超时，服务器响应过慢",
    "AuthenticationError": "认证失败，请检查账号密码",
    "PermissionError": "权限不足，无法执行此操作",
    "FileNotFoundError": "文件不存在",
    "ValueError": "参数值无效",
    "KeyError": "找不到指定的键",
    "TypeError": "类型错误",
    "ImportError": "模块导入失败，请检查依赖是否已安装",
}


def get_friendly_message(error: Exception) -> str:
    """将技术错误转换为用户友好的消息"""
    error_type = type(error).__name__
    
    if error_type in ERROR_MESSAGES:
        return f"{ERROR_MESSAGES[error_type]}: {error}"
    
    # JQData 特定错误
    error_str = str(error).lower()
    if 'auth' in error_str or '认证' in error_str:
        return "JQData 认证失败，请检查用户名和密码"
    if 'quota' in error_str or '配额' in error_str:
        return "API 调用配额已用尽，请稍后再试"
    if 'connection' in error_str or '连接' in error_str:
        return "连接服务器失败，请检查网络"
    
    return f"操作失败: {error}"


def print_error_summary():
    """打印错误摘要"""
    if not _error_history:
        print("✅ 没有记录到错误")
        return
    
    print("\n" + "=" * 60)
    print(f"错误摘要 (共 {len(_error_history)} 个错误)")
    print("=" * 60)
    
    # 按类型分组
    error_types = {}
    for info in _error_history:
        error_types.setdefault(info.error_type, []).append(info)
    
    for error_type, errors in error_types.items():
        print(f"\n{error_type}: {len(errors)} 次")
        # 显示最近一次
        latest = errors[-1]
        print(f"  最近: {latest.message[:80]}...")
        print(f"  时间: {latest.timestamp.strftime('%H:%M:%S')}")
    
    print("=" * 60)


# 用于数据获取的特定装饰器
def safe_data_fetch(default_empty_df: bool = True):
    """
    安全数据获取装饰器 - 专门用于数据获取函数
    
    Args:
        default_empty_df: 失败时是否返回空 DataFrame
    """
    import pandas as pd
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @retry_on_failure(max_retries=2, delay=0.5)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if result is None or (hasattr(result, 'empty') and result.empty):
                    logger.warning(f"⚠️ {func.__name__} 返回空数据")
                return result
            except Exception as e:
                logger.error(f"❌ 数据获取失败 ({func.__name__}): {e}")
                if default_empty_df:
                    return pd.DataFrame()
                return None
        return wrapper
    return decorator


if __name__ == '__main__':
    # 测试装饰器
    @safe_call(default="默认值")
    def test_safe_call():
        raise ValueError("测试错误")
    
    @retry_on_failure(max_retries=2, delay=0.1)
    def test_retry():
        raise ConnectionError("连接失败")
    
    print("测试 safe_call:")
    result = test_safe_call()
    print(f"结果: {result}")
    
    print("\n测试 retry_on_failure:")
    try:
        test_retry()
    except ConnectionError:
        print("重试后仍然失败")
    
    print("\n错误摘要:")
    print_error_summary()

