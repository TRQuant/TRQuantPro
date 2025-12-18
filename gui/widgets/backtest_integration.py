# -*- coding: utf-8 -*-
"""
回测GUI与后端集成模块
====================
连接 GUI 组件与新的回测后端功能：
- UnifiedBacktestManager (三层回测)
- BatchBacktestManager (批量回测)
- BacktestResultAnalyzer (结果分析)
- ReportManager (报告生成)
"""

import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from PyQt6.QtCore import QThread, pyqtSignal, QObject

logger = logging.getLogger(__name__)


# ==================== 回测执行线程 ====================

class UnifiedBacktestThread(QThread):
    """统一回测执行线程"""
    
    progress = pyqtSignal(float, str)  # progress(0-1), message
    finished = pyqtSignal(dict)        # result dict
    error = pyqtSignal(str)            # error message
    
    def __init__(
        self,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_type: str = "momentum",
        strategy_params: Dict = None,
        level: str = "fast",
        use_mock: bool = True,
        initial_capital: float = 1000000,
        parent=None
    ):
        super().__init__(parent)
        self.securities = securities
        self.start_date = start_date
        self.end_date = end_date
        self.strategy_type = strategy_type
        self.strategy_params = strategy_params or {}
        self.level = level
        self.use_mock = use_mock
        self.initial_capital = initial_capital
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True
    
    def run(self):
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            
            from core.backtest import (
                UnifiedBacktestManager,
                UnifiedBacktestConfig,
                BacktestLevel,
            )
            
            self.progress.emit(0.1, "初始化回测管理器...")
            
            if self._cancelled:
                return
            
            config = UnifiedBacktestConfig(
                start_date=self.start_date,
                end_date=self.end_date,
                securities=self.securities,
                initial_capital=self.initial_capital,
                use_mock=self.use_mock,
            )
            
            manager = UnifiedBacktestManager(config)
            manager.set_progress_callback(lambda p, m: self.progress.emit(p, m))
            
            self.progress.emit(0.2, "开始回测...")
            
            if self._cancelled:
                return
            
            results = manager.run_full_pipeline(
                strategy_type=self.strategy_type,
                strategy_params=self.strategy_params,
                levels=[BacktestLevel(self.level)]
            )
            
            if self._cancelled:
                return
            
            result = results.get(self.level)
            
            if result and result.success:
                self.progress.emit(1.0, "回测完成")
                self.finished.emit(self._format_result(result))
            else:
                error_msg = result.error if result else "回测失败"
                self.error.emit(error_msg)
                
        except Exception as e:
            logger.exception("回测线程异常")
            self.error.emit(str(e))
    
    def _format_result(self, result) -> Dict:
        """格式化结果为GUI兼容格式"""
        import pandas as pd
        
        formatted = {
            "metrics": {
                "total_return": result.total_return,
                "annual_return": result.annual_return,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "calmar_ratio": result.calmar_ratio,
                "sortino_ratio": result.sortino_ratio,
                "win_rate": result.win_rate,
                "total_trades": result.total_trades,
                "profit_factor": result.profit_factor,
            },
            "equity_curve": [],
            "trades": [],
            "summary": {
                "duration_seconds": result.duration_seconds,
                "engine": result.engine_used,
                "level": result.level_used,
            }
        }
        
        # 转换权益曲线
        if result.equity_curve is not None:
            if isinstance(result.equity_curve, pd.Series):
                formatted["equity_curve"] = result.equity_curve.tolist()
            elif isinstance(result.equity_curve, list):
                formatted["equity_curve"] = result.equity_curve
        
        # 转换交易记录
        if result.trades is not None and isinstance(result.trades, pd.DataFrame):
            formatted["trades"] = result.trades.to_dict(orient="records")
        
        return formatted


class BatchBacktestThread(QThread):
    """批量回测执行线程"""
    
    progress = pyqtSignal(float, str)
    task_completed = pyqtSignal(str, dict)  # task_id, result
    all_finished = pyqtSignal(dict)          # summary
    error = pyqtSignal(str)
    
    def __init__(
        self,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_type: str,
        parameter_ranges: Dict[str, List],
        use_mock: bool = True,
        max_workers: int = 4,
        parent=None
    ):
        super().__init__(parent)
        self.securities = securities
        self.start_date = start_date
        self.end_date = end_date
        self.strategy_type = strategy_type
        self.parameter_ranges = parameter_ranges
        self.use_mock = use_mock
        self.max_workers = max_workers
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True
    
    def run(self):
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            
            from core.backtest import (
                BatchBacktestManager,
                GridSearchConfig,
            )
            
            self.progress.emit(0.1, "初始化批量回测...")
            
            if self._cancelled:
                return
            
            # 构建网格配置
            grid_config = GridSearchConfig()
            for name, values in self.parameter_ranges.items():
                grid_config.add_parameter(name, values)
            
            total = grid_config.total_combinations
            self.progress.emit(0.2, f"准备 {total} 个参数组合...")
            
            manager = BatchBacktestManager(max_workers=self.max_workers)
            
            def on_progress(p, msg):
                if not self._cancelled:
                    self.progress.emit(0.2 + p * 0.7, msg)
            
            manager.set_progress_callback(on_progress)
            
            summary = manager.run_grid_search(
                securities=self.securities,
                start_date=self.start_date,
                end_date=self.end_date,
                strategy_type=self.strategy_type,
                grid_config=grid_config,
                use_mock=self.use_mock
            )
            
            if self._cancelled:
                return
            
            # 生成对比报告
            self.progress.emit(0.95, "生成对比报告...")
            report = manager.generate_comparison_report(summary)
            
            self.progress.emit(1.0, "批量回测完成")
            
            self.all_finished.emit({
                "summary": {
                    "total_tasks": summary.total_tasks,
                    "completed_tasks": summary.completed_tasks,
                    "failed_tasks": summary.failed_tasks,
                    "total_time_seconds": summary.total_time_seconds,
                },
                "best_result": summary.best_result.to_dict() if summary.best_result else None,
                "results": [r.to_dict() for r in summary.results],
                "report": report,
            })
            
        except Exception as e:
            logger.exception("批量回测线程异常")
            self.error.emit(str(e))


class ReportGeneratorThread(QThread):
    """报告生成线程"""
    
    progress = pyqtSignal(float, str)
    finished = pyqtSignal(str)  # report_path
    error = pyqtSignal(str)
    
    def __init__(
        self,
        result: Dict,
        report_type: str = "html",
        strategy_name: str = "策略",
        output_dir: str = None,
        parent=None
    ):
        super().__init__(parent)
        self.result = result
        self.report_type = report_type
        self.strategy_name = strategy_name
        self.output_dir = output_dir
    
    def run(self):
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            
            from core.reporting import generate_report
            
            self.progress.emit(0.3, "生成报告...")
            
            result = generate_report(
                result=self.result,
                report_type="backtest",
                format=self.report_type,
                strategy_name=self.strategy_name
            )
            
            if result.get("success"):
                self.progress.emit(1.0, "报告生成完成")
                self.finished.emit(result.get("file_path", ""))
            else:
                self.error.emit(result.get("error", "报告生成失败"))
                
        except Exception as e:
            logger.exception("报告生成线程异常")
            self.error.emit(str(e))


# ==================== GUI 集成接口 ====================

class BacktestIntegration(QObject):
    """
    回测 GUI 集成接口
    
    提供给 GUI 组件调用的高级接口
    """
    
    # 信号
    backtest_started = pyqtSignal(str)           # task_id
    backtest_progress = pyqtSignal(float, str)   # progress, message
    backtest_finished = pyqtSignal(str, dict)    # task_id, result
    backtest_error = pyqtSignal(str, str)        # task_id, error
    
    batch_started = pyqtSignal(int)              # total_tasks
    batch_progress = pyqtSignal(float, str)      # progress, message
    batch_finished = pyqtSignal(dict)            # summary
    batch_error = pyqtSignal(str)                # error
    
    report_generated = pyqtSignal(str)           # report_path
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_thread: Optional[QThread] = None
        self._task_counter = 0
    
    def run_backtest(
        self,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_type: str = "momentum",
        strategy_params: Dict = None,
        level: str = "fast",
        use_mock: bool = True,
        initial_capital: float = 1000000
    ) -> str:
        """
        运行单次回测
        
        Returns:
            task_id
        """
        self._task_counter += 1
        task_id = f"bt_{datetime.now().strftime('%H%M%S')}_{self._task_counter}"
        
        thread = UnifiedBacktestThread(
            securities=securities,
            start_date=start_date,
            end_date=end_date,
            strategy_type=strategy_type,
            strategy_params=strategy_params,
            level=level,
            use_mock=use_mock,
            initial_capital=initial_capital,
            parent=self
        )
        
        thread.progress.connect(self.backtest_progress.emit)
        thread.finished.connect(lambda r: self.backtest_finished.emit(task_id, r))
        thread.error.connect(lambda e: self.backtest_error.emit(task_id, e))
        
        self._current_thread = thread
        thread.start()
        
        self.backtest_started.emit(task_id)
        return task_id
    
    def run_batch_backtest(
        self,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_type: str,
        parameter_ranges: Dict[str, List],
        use_mock: bool = True,
        max_workers: int = 4
    ):
        """运行批量回测（参数网格搜索）"""
        total = 1
        for values in parameter_ranges.values():
            total *= len(values)
        
        thread = BatchBacktestThread(
            securities=securities,
            start_date=start_date,
            end_date=end_date,
            strategy_type=strategy_type,
            parameter_ranges=parameter_ranges,
            use_mock=use_mock,
            max_workers=max_workers,
            parent=self
        )
        
        thread.progress.connect(self.batch_progress.emit)
        thread.all_finished.connect(self.batch_finished.emit)
        thread.error.connect(self.batch_error.emit)
        
        self._current_thread = thread
        thread.start()
        
        self.batch_started.emit(total)
    
    def generate_report(
        self,
        result: Dict,
        report_type: str = "html",
        strategy_name: str = "策略"
    ):
        """生成报告"""
        thread = ReportGeneratorThread(
            result=result,
            report_type=report_type,
            strategy_name=strategy_name,
            parent=self
        )
        
        thread.finished.connect(self.report_generated.emit)
        thread.error.connect(lambda e: logger.error(f"报告生成失败: {e}"))
        
        thread.start()
    
    def cancel(self):
        """取消当前任务"""
        if self._current_thread and self._current_thread.isRunning():
            if hasattr(self._current_thread, 'cancel'):
                self._current_thread.cancel()
    
    def is_running(self) -> bool:
        """是否有任务在运行"""
        return self._current_thread is not None and self._current_thread.isRunning()


# ==================== 便捷函数 ====================

_integration: Optional[BacktestIntegration] = None


def get_backtest_integration() -> BacktestIntegration:
    """获取全局集成实例"""
    global _integration
    if _integration is None:
        _integration = BacktestIntegration()
    return _integration


def quick_gui_backtest(
    securities: List[str],
    start_date: str,
    end_date: str,
    strategy_type: str = "momentum",
    on_progress: Callable = None,
    on_finished: Callable = None,
    on_error: Callable = None
) -> str:
    """
    快速 GUI 回测（便捷函数）
    
    Returns:
        task_id
    """
    integration = get_backtest_integration()
    
    if on_progress:
        integration.backtest_progress.connect(on_progress)
    if on_finished:
        integration.backtest_finished.connect(on_finished)
    if on_error:
        integration.backtest_error.connect(on_error)
    
    return integration.run_backtest(
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        strategy_type=strategy_type
    )


# ==================== 策略类型定义 ====================

STRATEGY_TYPES = {
    "momentum": {
        "name": "动量策略",
        "description": "追涨强势股，适合趋势市",
        "params": {
            "lookback": {"type": "int", "default": 20, "range": [5, 60]},
            "top_n": {"type": "int", "default": 10, "range": [3, 30]},
        }
    },
    "mean_reversion": {
        "name": "均值回归策略",
        "description": "买入超跌股票，适合震荡市",
        "params": {
            "lookback": {"type": "int", "default": 20, "range": [5, 60]},
            "std_threshold": {"type": "float", "default": 2.0, "range": [1.0, 3.0]},
            "top_n": {"type": "int", "default": 10, "range": [3, 30]},
        }
    },
    "rotation": {
        "name": "轮动策略",
        "description": "行业/风格轮动，适合结构性行情",
        "params": {
            "momentum_period": {"type": "int", "default": 20, "range": [5, 60]},
            "holding_period": {"type": "int", "default": 5, "range": [1, 20]},
        }
    },
}


def get_strategy_types() -> Dict:
    """获取支持的策略类型"""
    return STRATEGY_TYPES


def get_strategy_params(strategy_type: str) -> Dict:
    """获取策略参数定义"""
    return STRATEGY_TYPES.get(strategy_type, {}).get("params", {})


# ==================== 导出 ====================

__all__ = [
    "UnifiedBacktestThread",
    "BatchBacktestThread",
    "ReportGeneratorThread",
    "BacktestIntegration",
    "get_backtest_integration",
    "quick_gui_backtest",
    "get_strategy_types",
    "get_strategy_params",
    "STRATEGY_TYPES",
]
