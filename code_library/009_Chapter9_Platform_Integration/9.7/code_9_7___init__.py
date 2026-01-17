"""
文件名: code_9_7___init__.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.7/code_9_7___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.7_Online_Feedback_Loop_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# core/live_feedback/feedback_loop.py
from typing import Dict, Optional
from datetime import datetime
import logging

from core.live_feedback.data_collector import LiveDataCollector
from core.live_feedback.anomaly_detector import AnomalyDetector
from core.live_feedback.trigger_manager import TriggerManager
from core.live_feedback.optimizer import OnlineOptimizer
from core.live_feedback.safety_gate import SafetyGate

logger = logging.getLogger(__name__)

class FeedbackLoopManager:
    """反馈闭环管理器"""
    
    def __init__(
        self,
        data_collector: LiveDataCollector,
        anomaly_detector: AnomalyDetector,
        trigger_manager: TriggerManager,
        optimizer: OnlineOptimizer,
        safety_gate: SafetyGate
    ):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        self.data_collector = data_collector
        self.anomaly_detector = anomaly_detector
        self.trigger_manager = trigger_manager
        self.optimizer = optimizer
        self.safety_gate = safety_gate
    
    def run_feedback_loop(
        self,
        strategy_id: str,
        date: datetime
    ) -> Dict:
        """
        运行反馈闭环
        
        Args:
            strategy_id: 策略ID
            date: 日期
        
        Returns:
            Dict: 反馈闭环结果
        """
        logger.info(f"运行反馈闭环: {strategy_id}, {date}")
        
        # 1. 收集实盘数据
        metrics = self.data_collector.collect_performance_metrics(strategy_id, date)
        if not metrics:
            return {'success': False, 'error': '无法收集性能指标'}
        
        # 2. 检测异常
        anomalies = self.anomaly_detector.detect_anomalies(strategy_id, date)
        
        # 3. 检查触发器
        triggered = self.trigger_manager.check_triggers(strategy_id, date)
        
        if not triggered:
            return {
                'success': True,
                'action': 'monitor',
                'metrics': metrics,
                'anomalies': [a.message for a in anomalies]
            }
        
        # 4. 触发再优化
        optimization_results = []
        for trigger in triggered:
            # 根据触发器类型选择优化模式
            mode = self._determine_optimization_mode(trigger, anomalies)
            
            # 执行优化（dry_run模式）
            result = self.optimizer.optimize_strategy(
                strategy_id,
                trigger,
                mode
            )
            
            optimization_results.append(result)
        
        return {
            'success': True,
            'action': 'optimize',
            'metrics': metrics,
            'anomalies': [a.message for a in anomalies],
            'triggers': [t.trigger_id for t in triggered],
            'optimization_results': [
                {
                    'optimized_strategy_id': r.optimized_strategy_id,
                    'mode': r.mode.value,
                    'recommendation': r.recommendation
                }
                for r in optimization_results
            ]
        }
    
    def deploy_optimized_strategy(
        self,
        strategy_id: str,
        optimized_strategy_id: str,
        confirm_token: str,
        operator: str,
        reason: str
    ) -> bool:
        """
        部署优化后的策略
        
        Args:
            strategy_id: 原策略ID
            optimized_strategy_id: 优化后的策略ID
            confirm_token: 确认令牌
            operator: 操作人
            reason: 原因
        
        Returns:
            bool: 是否成功
        """
        # 验证令牌
        if not self.safety_gate.validate_token(
            confirm_token,
            'deploy_strategy',
            {'strategy_id': strategy_id, 'optimized_strategy_id': optimized_strategy_id}
        ):
            logger.error("确认令牌验证失败")
            return False
        
        # 记录证据
        self.safety_gate.record_evidence(
            operation='deploy_strategy',
            operator=operator,
            reason=reason,
            scope=f"策略 {strategy_id} -> {optimized_strategy_id}",
            rollback=f"回退到策略 {strategy_id}",
            token=confirm_token
        )
        
        # 执行部署（实际实现需要调用部署系统）
        logger.info(f"部署优化后的策略: {optimized_strategy_id}")
        
        return True
    
    def _determine_optimization_mode(self, trigger, anomalies):
        """根据触发器和异常确定优化模式"""
        # 如果有严重异常，使用严重模式
        critical_anomalies = [a for a in anomalies if a.severity == "critical"]
        if critical_anomalies:
            return OptimizationMode.HEAVY
        
        # 如果触发器是数据触发器，使用中等模式
        if trigger.trigger_type == TriggerType.DATA:
            return OptimizationMode.MEDIUM
        
        # 默认使用轻量级模式
        return OptimizationMode.LIGHT