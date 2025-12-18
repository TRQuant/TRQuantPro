# -*- coding: utf-8 -*-
"""QMT回测结果"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import pandas as pd

@dataclass
class QMTResult:
    success: bool = False
    message: str = "回测未运行"
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    trading_days: int = 0
    duration_seconds: float = 0.0
    benchmark_return: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    daily_records: Optional[pd.DataFrame] = None
    trades: Optional[List[Dict[str, Any]]] = None
    equity_curve: Optional[List[float]] = None
    positions_history: Optional[List[Dict[str, Any]]] = None
    report_path: Optional[str] = None
    raw_results: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标字典"""
        return {
            "total_return": f"{self.total_return*100:.2f}%",
            "annual_return": f"{self.annual_return*100:.2f}%",
            "sharpe_ratio": f"{self.sharpe_ratio:.2f}",
            "max_drawdown": f"{self.max_drawdown*100:.2f}%",
            "win_rate": f"{self.win_rate*100:.1f}%",
            "total_trades": self.total_trades,
            "trading_days": self.trading_days,
            "benchmark_return": f"{self.benchmark_return*100:.2f}%",
        }
    
    def to_mongodb_doc(self) -> Dict[str, Any]:
        """转换为MongoDB文档"""
        return {
            "timestamp": datetime.now(),
            "success": self.success,
            "message": self.message,
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.win_rate,
            "total_trades": self.total_trades,
            "trading_days": self.trading_days,
            "benchmark_return": self.benchmark_return,
            "duration_seconds": self.duration_seconds,
            "report_path": self.report_path,
            "metrics": self.metrics,
            "trades_count": len(self.trades) if self.trades else 0,
        }

@dataclass
class QMTOptimizeResult:
    best_params: Dict[str, Any]
    best_result: Optional[QMTResult] = None
    all_results: List[Dict[str, Any]] = field(default_factory=list)
    optimization_time: float = 0.0
    iterations: int = 0
