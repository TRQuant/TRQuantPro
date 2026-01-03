# -*- coding: utf-8 -*-
"""
BulletTrade 回测结果类

提供回测结果的封装和分析
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    pd = None
    np = None


@dataclass
class BTResult:
    """BulletTrade回测结果"""
    
    # 核心指标
    total_return: float = 0.0        # 总收益率 (百分比)
    annual_return: float = 0.0       # 年化收益率 (百分比)
    sharpe_ratio: float = 0.0        # 夏普比率
    max_drawdown: float = 0.0        # 最大回撤 (百分比)
    
    # 附加指标
    win_rate: float = 0.0            # 日胜率 (百分比)
    trade_win_rate: float = 0.0      # 交易胜率 (百分比)
    trading_days: int = 0            # 交易天数
    total_trades: int = 0            # 总交易次数
    
    # 资金信息
    initial_capital: float = 0.0     # 初始资金
    final_capital: float = 0.0       # 最终资金
    
    # 原始数据
    daily_records: Optional[Any] = None  # 每日记录 DataFrame
    trades: Optional[List[Any]] = None   # 交易记录
    events: Optional[List[Dict]] = None  # 事件记录 (分红/拆分)
    daily_positions: Optional[Any] = None  # 每日持仓
    
    # 元信息
    strategy_file: str = ""          # 策略文件路径
    start_date: str = ""             # 回测开始日期
    end_date: str = ""               # 回测结束日期
    runtime_seconds: float = 0.0     # 运行耗时
    
    # 报告路径
    report_path: str = ""            # HTML报告路径
    csv_path: str = ""               # CSV文件路径
    log_path: str = ""               # 日志文件路径
    
    # 原始结果
    raw_results: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 确保trades是列表
        if self.trades is None:
            self.trades = []
        
        # 确保events是列表
        if self.events is None:
            self.events = []
    
    @classmethod
    def from_engine_results(cls, results: Dict[str, Any], output_dir: str = "") -> "BTResult":
        """从BulletTrade引擎结果创建"""
        summary = results.get("summary", {})
        meta = results.get("meta", {})
        
        # 解析百分比字符串
        def parse_percent(s: str) -> float:
            if isinstance(s, (int, float)):
                return float(s)
            if isinstance(s, str):
                return float(s.replace("%", "").replace(",", ""))
            return 0.0
        
        # 解析数字字符串
        def parse_number(s: str) -> float:
            if isinstance(s, (int, float)):
                return float(s)
            if isinstance(s, str):
                return float(s.replace(",", ""))
            return 0.0
        
        return cls(
            total_return=parse_percent(summary.get("策略收益", "0")),
            annual_return=parse_percent(summary.get("策略年化收益", "0")),
            sharpe_ratio=parse_number(summary.get("夏普比率", "0")),
            max_drawdown=parse_percent(summary.get("最大回撤", "0")),
            win_rate=parse_percent(summary.get("日胜率", "0")),
            trade_win_rate=parse_percent(summary.get("交易胜率", "0")),
            trading_days=int(summary.get("交易天数", 0)),
            total_trades=len(results.get("trades", [])),
            initial_capital=parse_number(summary.get("初始资金", "0")),
            final_capital=parse_number(summary.get("最终资金", "0")),
            daily_records=results.get("daily_records"),
            trades=results.get("trades", []),
            events=results.get("events", []),
            daily_positions=results.get("daily_positions"),
            strategy_file=meta.get("strategy_file", ""),
            start_date=meta.get("start_date", ""),
            end_date=meta.get("end_date", ""),
            runtime_seconds=meta.get("runtime_seconds", 0.0),
            report_path=str(Path(output_dir) / "report.html") if output_dir else "",
            csv_path=str(Path(output_dir) / "daily_records.csv") if output_dir else "",
            log_path=str(Path(output_dir) / "backtest.log") if output_dir else "",
            raw_results=results,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 (不包含DataFrame)"""
        return {
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.win_rate,
            "trade_win_rate": self.trade_win_rate,
            "trading_days": self.trading_days,
            "total_trades": self.total_trades,
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "strategy_file": self.strategy_file,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "runtime_seconds": self.runtime_seconds,
            "report_path": self.report_path,
            "csv_path": self.csv_path,
            "log_path": self.log_path,
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def to_mongodb_doc(self) -> Dict[str, Any]:
        """转换为MongoDB文档格式"""
        doc = self.to_dict()
        doc["created_at"] = datetime.now()
        doc["trades_count"] = len(self.trades) if self.trades else 0
        doc["events_count"] = len(self.events) if self.events else 0
        return doc
    
    def get_metrics(self) -> Dict[str, float]:
        """获取核心指标"""
        return {
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.win_rate,
            "trade_win_rate": self.trade_win_rate,
        }
    
    def summary(self) -> str:
        """生成摘要文本"""
        lines = [
            "=" * 50,
            "BulletTrade 回测结果摘要",
            "=" * 50,
            f"策略文件: {self.strategy_file}",
            f"回测区间: {self.start_date} ~ {self.end_date}",
            f"交易天数: {self.trading_days}",
            "-" * 50,
            f"总收益率: {self.total_return:.2f}%",
            f"年化收益率: {self.annual_return:.2f}%",
            f"夏普比率: {self.sharpe_ratio:.2f}",
            f"最大回撤: {self.max_drawdown:.2f}%",
            f"日胜率: {self.win_rate:.2f}%",
            f"交易胜率: {self.trade_win_rate:.2f}%",
            "-" * 50,
            f"初始资金: {self.initial_capital:,.2f}",
            f"最终资金: {self.final_capital:,.2f}",
            f"总交易次数: {self.total_trades}",
            f"运行耗时: {self.runtime_seconds:.2f}秒",
            "=" * 50,
        ]
        return "\n".join(lines)
    
    def is_profitable(self) -> bool:
        """是否盈利"""
        return self.total_return > 0
    
    def meets_threshold(
        self,
        min_return: Optional[float] = None,
        min_sharpe: Optional[float] = None,
        max_drawdown: Optional[float] = None,
    ) -> bool:
        """检查是否满足阈值条件"""
        if min_return is not None and self.total_return < min_return:
            return False
        if min_sharpe is not None and self.sharpe_ratio < min_sharpe:
            return False
        if max_drawdown is not None and abs(self.max_drawdown) > abs(max_drawdown):
            return False
        return True


@dataclass
class BTOptimizeResult:
    """BulletTrade参数优化结果"""
    
    best_params: Dict[str, Any] = field(default_factory=dict)
    best_result: Optional[BTResult] = None
    all_results: List[Dict[str, Any]] = field(default_factory=list)
    
    # 优化信息
    target_metric: str = ""
    n_trials: int = 0
    runtime_seconds: float = 0.0
    
    def summary(self) -> str:
        """生成摘要"""
        if not self.best_result:
            return "无优化结果"
        
        lines = [
            "=" * 50,
            "参数优化结果",
            "=" * 50,
            f"优化目标: {self.target_metric}",
            f"试验次数: {self.n_trials}",
            f"最优参数: {self.best_params}",
            "-" * 50,
            "最优结果:",
            f"  总收益率: {self.best_result.total_return:.2f}%",
            f"  夏普比率: {self.best_result.sharpe_ratio:.2f}",
            f"  最大回撤: {self.best_result.max_drawdown:.2f}%",
            "=" * 50,
        ]
        return "\n".join(lines)


__all__ = ["BTResult", "BTOptimizeResult"]

