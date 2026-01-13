#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强型错误管理器

提供：
1. 分层错误追踪（阶段 -> 操作 -> 详细）
2. 自动恢复建议
3. 错误分类和统计
4. 上下文保存
5. 日志和报告生成
"""

import sys
import traceback
from pathlib import Path
from typing import Dict, Optional, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """错误严重程度"""
    INFO = "info"           # 信息性消息
    WARNING = "warning"     # 警告，可继续执行
    ERROR = "error"         # 错误，当前操作失败但可恢复
    CRITICAL = "critical"   # 严重错误，需要中断


class ErrorCategory(Enum):
    """错误类别"""
    DATA_FETCH = "data_fetch"           # 数据获取
    DATA_PARSE = "data_parse"           # 数据解析
    CALCULATION = "calculation"         # 计算错误
    VALIDATION = "validation"           # 验证失败
    NETWORK = "network"                 # 网络错误
    DATABASE = "database"               # 数据库错误
    CONFIGURATION = "configuration"     # 配置错误
    SYSTEM = "system"                   # 系统错误
    UNKNOWN = "unknown"                 # 未知错误


@dataclass
class ErrorRecord:
    """单个错误记录"""
    timestamp: str
    phase: str              # 执行阶段
    operation: str          # 具体操作
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    traceback: Optional[str] = None
    recovery_suggestion: Optional[str] = None
    recovered: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'phase': self.phase,
            'operation': self.operation,
            'category': self.category.value,
            'severity': self.severity.value,
            'message': self.message,
            'details': self.details,
            'context': self.context,
            'traceback': self.traceback,
            'recovery_suggestion': self.recovery_suggestion,
            'recovered': self.recovered
        }


class ErrorManager:
    """增强型错误管理器"""
    
    # 错误恢复建议映射
    RECOVERY_SUGGESTIONS = {
        ErrorCategory.DATA_FETCH: [
            "检查网络连接",
            "验证数据源API可用性",
            "增加重试次数或超时时间",
            "使用本地缓存数据"
        ],
        ErrorCategory.DATA_PARSE: [
            "检查数据格式是否正确",
            "验证数据字段名称",
            "使用默认值填充缺失字段"
        ],
        ErrorCategory.CALCULATION: [
            "检查输入数据有效性",
            "验证计算参数范围",
            "使用安全的数学运算（避免除零等）"
        ],
        ErrorCategory.VALIDATION: [
            "放宽筛选条件",
            "检查阈值设置是否合理",
            "增加候选样本数量"
        ],
        ErrorCategory.NETWORK: [
            "检查网络连接",
            "尝试使用代理",
            "增加重试次数"
        ],
        ErrorCategory.DATABASE: [
            "检查数据库连接",
            "验证数据库配置",
            "清理数据库连接池"
        ],
        ErrorCategory.CONFIGURATION: [
            "检查配置文件",
            "验证必需参数",
            "使用默认配置"
        ],
        ErrorCategory.SYSTEM: [
            "检查系统资源",
            "重启服务",
            "查看系统日志"
        ]
    }
    
    def __init__(self, workflow_id: str, output_dir: Optional[Path] = None):
        """
        初始化错误管理器
        
        Args:
            workflow_id: 工作流ID
            output_dir: 输出目录
        """
        self.workflow_id = workflow_id
        self.output_dir = output_dir or Path('output/errors')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.errors: List[ErrorRecord] = []
        self.current_phase: str = "init"
        self.phase_errors: Dict[str, List[ErrorRecord]] = {}
        self.category_counts: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
        self.severity_counts: Dict[ErrorSeverity, int] = {sev: 0 for sev in ErrorSeverity}
        
        # 恢复处理器
        self.recovery_handlers: Dict[ErrorCategory, Callable] = {}
    
    def set_phase(self, phase: str):
        """设置当前执行阶段"""
        self.current_phase = phase
        if phase not in self.phase_errors:
            self.phase_errors[phase] = []
    
    def register_recovery_handler(self, category: ErrorCategory, handler: Callable):
        """注册错误恢复处理器"""
        self.recovery_handlers[category] = handler
    
    def record_error(
        self,
        operation: str,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[str] = None,
        context: Optional[Dict] = None,
        exception: Optional[Exception] = None,
        try_recovery: bool = True
    ) -> ErrorRecord:
        """
        记录错误
        
        Args:
            operation: 操作名称
            message: 错误消息
            category: 错误类别
            severity: 严重程度
            details: 详细信息
            context: 上下文数据
            exception: 异常对象
            try_recovery: 是否尝试恢复
        
        Returns:
            ErrorRecord
        """
        tb = None
        if exception:
            tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
            tb = ''.join(tb)
        
        # 获取恢复建议
        suggestions = self.RECOVERY_SUGGESTIONS.get(category, [])
        recovery_suggestion = suggestions[0] if suggestions else None
        
        record = ErrorRecord(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            phase=self.current_phase,
            operation=operation,
            category=category,
            severity=severity,
            message=message,
            details=details,
            context=context or {},
            traceback=tb,
            recovery_suggestion=recovery_suggestion
        )
        
        self.errors.append(record)
        self.phase_errors.setdefault(self.current_phase, []).append(record)
        self.category_counts[category] += 1
        self.severity_counts[severity] += 1
        
        # 尝试自动恢复
        if try_recovery and category in self.recovery_handlers:
            try:
                self.recovery_handlers[category](record)
                record.recovered = True
            except Exception as e:
                logger.warning(f"Recovery failed for {category}: {e}")
        
        # 记录日志
        log_msg = f"[{self.current_phase}:{operation}] {message}"
        if severity == ErrorSeverity.CRITICAL:
            logger.critical(log_msg)
        elif severity == ErrorSeverity.ERROR:
            logger.error(log_msg)
        elif severity == ErrorSeverity.WARNING:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
        
        return record
    
    def record_warning(self, operation: str, message: str, **kwargs) -> ErrorRecord:
        """记录警告"""
        return self.record_error(
            operation, message,
            severity=ErrorSeverity.WARNING,
            **kwargs
        )
    
    def record_info(self, operation: str, message: str, **kwargs) -> ErrorRecord:
        """记录信息"""
        return self.record_error(
            operation, message,
            severity=ErrorSeverity.INFO,
            **kwargs
        )
    
    def has_critical_errors(self) -> bool:
        """检查是否有严重错误"""
        return self.severity_counts[ErrorSeverity.CRITICAL] > 0
    
    def has_errors(self) -> bool:
        """检查是否有错误（不包括警告和信息）"""
        return self.severity_counts[ErrorSeverity.ERROR] > 0 or self.has_critical_errors()
    
    def get_phase_summary(self, phase: str) -> Dict:
        """获取阶段错误摘要"""
        phase_errors = self.phase_errors.get(phase, [])
        return {
            'phase': phase,
            'total_errors': len(phase_errors),
            'critical': sum(1 for e in phase_errors if e.severity == ErrorSeverity.CRITICAL),
            'errors': sum(1 for e in phase_errors if e.severity == ErrorSeverity.ERROR),
            'warnings': sum(1 for e in phase_errors if e.severity == ErrorSeverity.WARNING),
            'categories': {
                cat.value: sum(1 for e in phase_errors if e.category == cat)
                for cat in ErrorCategory if any(e.category == cat for e in phase_errors)
            }
        }
    
    def get_summary(self) -> Dict:
        """获取总体错误摘要"""
        return {
            'workflow_id': self.workflow_id,
            'total_errors': len(self.errors),
            'by_severity': {sev.value: count for sev, count in self.severity_counts.items() if count > 0},
            'by_category': {cat.value: count for cat, count in self.category_counts.items() if count > 0},
            'by_phase': {phase: self.get_phase_summary(phase) for phase in self.phase_errors},
            'recovered_count': sum(1 for e in self.errors if e.recovered),
            'has_critical': self.has_critical_errors()
        }
    
    def get_recovery_suggestions(self) -> List[str]:
        """获取所有恢复建议"""
        suggestions = []
        for error in self.errors:
            if error.severity in (ErrorSeverity.ERROR, ErrorSeverity.CRITICAL) and not error.recovered:
                if error.recovery_suggestion and error.recovery_suggestion not in suggestions:
                    suggestions.append(error.recovery_suggestion)
        return suggestions
    
    def export_json(self, filepath: Optional[Path] = None) -> Path:
        """导出错误记录为JSON"""
        if filepath is None:
            filepath = self.output_dir / f"errors_{self.workflow_id}.json"
        
        data = {
            'summary': self.get_summary(),
            'errors': [e.to_dict() for e in self.errors]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def print_summary(self, include_details: bool = False):
        """打印错误摘要"""
        summary = self.get_summary()
        
        print(f"\n{'='*60}")
        print(f"错误管理报告 - {self.workflow_id}")
        print(f"{'='*60}")
        
        print(f"\n总计错误: {summary['total_errors']}")
        
        if summary['by_severity']:
            print(f"\n按严重程度:")
            for sev, count in summary['by_severity'].items():
                icon = {'critical': '🔴', 'error': '🟠', 'warning': '🟡', 'info': '🔵'}.get(sev, '⚪')
                print(f"  {icon} {sev}: {count}")
        
        if summary['by_category']:
            print(f"\n按错误类别:")
            for cat, count in summary['by_category'].items():
                print(f"  • {cat}: {count}")
        
        if summary['by_phase']:
            print(f"\n按执行阶段:")
            for phase, phase_summary in summary['by_phase'].items():
                status = '✅' if phase_summary['critical'] == 0 and phase_summary['errors'] == 0 else '❌'
                print(f"  {status} {phase}: {phase_summary['total_errors']} 个问题")
        
        suggestions = self.get_recovery_suggestions()
        if suggestions:
            print(f"\n恢复建议:")
            for i, suggestion in enumerate(suggestions[:5], 1):
                print(f"  {i}. {suggestion}")
        
        print(f"\n{'='*60}")
        
        if include_details and self.errors:
            print(f"\n详细错误列表:")
            for i, error in enumerate(self.errors[-10:], 1):  # 只显示最近10个
                icon = {'critical': '🔴', 'error': '🟠', 'warning': '🟡', 'info': '🔵'}.get(
                    error.severity.value, '⚪')
                print(f"\n{i}. {icon} [{error.phase}:{error.operation}]")
                print(f"   {error.message}")
                if error.details:
                    print(f"   详情: {error.details[:100]}...")


class SafeExecutor:
    """安全执行器 - 包装函数调用，自动处理错误"""
    
    def __init__(self, error_manager: ErrorManager):
        self.error_manager = error_manager
    
    def execute(
        self,
        func: Callable,
        operation: str,
        default_value: Any = None,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        context: Optional[Dict] = None,
        max_retries: int = 0,
        *args, **kwargs
    ) -> Any:
        """
        安全执行函数
        
        Args:
            func: 要执行的函数
            operation: 操作名称
            default_value: 失败时的默认返回值
            category: 错误类别
            context: 上下文信息
            max_retries: 最大重试次数
            *args, **kwargs: 函数参数
        
        Returns:
            函数返回值或默认值
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < max_retries:
                    self.error_manager.record_warning(
                        operation=operation,
                        message=f"尝试 {attempt + 1}/{max_retries + 1} 失败: {str(e)}",
                        category=category,
                        context=context
                    )
                    continue
        
        # 所有重试都失败
        self.error_manager.record_error(
            operation=operation,
            message=f"执行失败: {str(last_exception)}",
            category=category,
            context=context,
            exception=last_exception
        )
        
        return default_value


# 工作流阶段定义
class WorkflowPhase:
    """工作流阶段常量"""
    INIT = "初始化"
    MARKET_DETECTION = "市场状态检测"
    DATA_MINING = "数据挖掘"
    PATTERN_EXTRACTION = "模式提取"
    STRATEGY_GENERATION = "策略生成"
    BACKTEST = "回测执行"
    EVOLUTION = "遗传进化"
    KNOWLEDGE_BASE = "知识库保存"
    REPORT_GENERATION = "报告生成"
