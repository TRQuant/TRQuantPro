"""
trace_id追踪管理器

提供trace_id的生成、传递和管理功能，用于关联和追踪整个调用链。
"""

import uuid
import threading
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def generate_trace_id() -> str:
    """
    生成新的trace_id（UUID v4格式）
    
    Returns:
        trace_id字符串
    """
    return str(uuid.uuid4())


class TraceManager:
    """trace_id管理器（线程本地存储）"""
    
    _local = threading.local()
    
    @classmethod
    def set_trace_id(cls, trace_id: str):
        """
        设置当前线程的trace_id
        
        Args:
            trace_id: 追踪ID
        """
        cls._local.trace_id = trace_id
        logger.debug(f"设置trace_id: {trace_id}")
    
    @classmethod
    def get_trace_id(cls) -> Optional[str]:
        """
        获取当前线程的trace_id
        
        Returns:
            当前trace_id，如果未设置则返回None
        """
        return getattr(cls._local, 'trace_id', None)
    
    @classmethod
    def generate_and_set(cls) -> str:
        """
        生成并设置新的trace_id
        
        Returns:
            新生成的trace_id
        """
        trace_id = generate_trace_id()
        cls.set_trace_id(trace_id)
        return trace_id
    
    @classmethod
    def clear_trace_id(cls):
        """清除当前线程的trace_id"""
        if hasattr(cls._local, 'trace_id'):
            delattr(cls._local, 'trace_id')


def extract_trace_id_from_args(args: Dict[str, Any]) -> Optional[str]:
    """
    从参数中提取trace_id
    
    Args:
        args: 工具参数
    
    Returns:
        trace_id，如果不存在则返回None
    """
    trace_id = args.get('trace_id')
    if trace_id:
        # 验证trace_id格式（UUID格式）
        try:
            uuid.UUID(trace_id)
            return trace_id
        except ValueError:
            logger.warning(f"无效的trace_id格式: {trace_id}")
            return None
    return None


def add_trace_id_to_args(args: Dict[str, Any], trace_id: Optional[str] = None) -> Dict[str, Any]:
    """
    向参数中添加trace_id
    
    Args:
        args: 工具参数
        trace_id: 追踪ID，如果为None则从当前上下文获取或生成新的
    
    Returns:
        包含trace_id的参数
    """
    if trace_id is None:
        trace_id = TraceManager.get_trace_id()
        if trace_id is None:
            trace_id = TraceManager.generate_and_set()
    
    args_with_trace = args.copy()
    args_with_trace['trace_id'] = trace_id
    return args_with_trace


def get_trace_id_from_args_or_context(args: Dict[str, Any]) -> str:
    """
    从参数或上下文中获取trace_id，如果不存在则生成新的
    
    Args:
        args: 工具参数
    
    Returns:
        trace_id
    """
    trace_id = extract_trace_id_from_args(args)
    if trace_id:
        TraceManager.set_trace_id(trace_id)
        return trace_id
    
    trace_id = TraceManager.get_trace_id()
    if trace_id:
        return trace_id
    
    return TraceManager.generate_and_set()


class TraceContext:
    """trace_id上下文管理器"""
    
    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or generate_trace_id()
        self.old_trace_id = None
    
    def __enter__(self):
        self.old_trace_id = TraceManager.get_trace_id()
        TraceManager.set_trace_id(self.trace_id)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.old_trace_id:
            TraceManager.set_trace_id(self.old_trace_id)
        else:
            TraceManager.clear_trace_id()
        return False
