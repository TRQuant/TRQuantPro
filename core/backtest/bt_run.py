"""回测执行器

封装 BulletTrade 回测执行流程
"""

from typing import Optional, Dict, Any, Callable, List
from pathlib import Path
from datetime import datetime
import subprocess
import logging
import json
import os

from .backtest_config import BacktestConfig
from .backtest_result import BacktestResult, BacktestMetrics

logger = logging.getLogger(__name__)


class BacktestRunner:
    """回测执行器
    
    封装 BulletTrade 回测执行，提供 Python API
    
    Example:
        >>> config = BacktestConfig(
        ...     strategy_path="strategies/my_strategy.py",
        ...     start_date="2020-01-01",
        ...     end_date="2023-12-31"
        ... )
        >>> runner = BacktestRunner(config)
        >>> result = runner.run()
    """
    
    BT_CLI = "bullet-trade"
    
    def __init__(self, config: BacktestConfig):
        """初始化执行器
        
        Args:
            config: 回测配置
        """
        self.config = config
        self._progress_callback: Optional[Callable[[int, str], None]] = None
        self._bt_available = self._check_bt()
    
    def _check_bt(self) -> bool:
        """检查 BulletTrade 是否可用"""
        try:
            result = subprocess.run(
                [self.BT_CLI, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def set_progress_callback(self, callback: Callable[[int, str], None]) -> None:
        """设置进度回调"""
        self._progress_callback = callback
    
    def _report_progress(self, progress: int, message: str) -> None:
        """报告进度"""
        logger.info(f"[{progress}%] {message}")
        if self._progress_callback:
            self._progress_callback(progress, message)
    
    def run(self) -> BacktestResult:
        """执行回测
        
        Returns:
            回测结果
        """
        # 验证配置
        errors = self.config.validate()
        if errors:
            return BacktestResult(
                success=False,
                error="; ".join(errors),
                config=self.config.to_dict()
            )
        
        self._report_progress(0, "开始回测...")
        
        # 保存配置
        self.config.save()
        
        if self._bt_available:
            return self._run_with_bt()
        else:
            return self._run_mock()
    
    def _run_with_bt(self) -> BacktestResult:
        """使用 BulletTrade 执行回测"""
        self._report_progress(10, "准备回测环境...")
        
        # 构建命令
        cmd = [
            self.BT_CLI, "backtest",
            self.config.strategy_path,
            "--start", self.config.start_date,
            "--end", self.config.end_date,
            "--frequency", self.config.frequency.value,
            "--capital", str(self.config.initial_capital),
        ]
        
        if self.config.output_dir:
            cmd.extend(["--output", self.config.output_dir])
        
        self._report_progress(20, "执行回测...")
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,
                cwd=os.getcwd()
            )
            
            self._report_progress(80, "解析结果...")
            
            if result.returncode == 0:
                return self._parse_bt_result(result.stdout)
            else:
                return BacktestResult(
                    success=False,
                    error=result.stderr or "回测执行失败",
                    config=self.config.to_dict()
                )
        except subprocess.TimeoutExpired:
            return BacktestResult(
                success=False,
                error="回测超时（超过1小时）",
                config=self.config.to_dict()
            )
        except Exception as e:
            return BacktestResult(
                success=False,
                error=str(e),
                config=self.config.to_dict()
            )
    
    def _run_mock(self) -> BacktestResult:
        """模拟回测"""
        import random
        from datetime import timedelta
        
        self._report_progress(10, "使用模拟模式运行回测...")
        
        start = datetime.strptime(self.config.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.config.end_date, "%Y-%m-%d")
        days = (end - start).days
        
        self._report_progress(30, "生成模拟净值曲线...")
        
        # 生成净值曲线
        equity = self.config.initial_capital
        equity_curve = []
        max_equity = equity
        max_drawdown = 0.0
        daily_returns = []
        
        for i in range(days):
            date = start + timedelta(days=i)
            if date.weekday() < 5:
                daily_return = random.gauss(0.0005, 0.02)
                daily_returns.append(daily_return)
                equity *= (1 + daily_return)
                max_equity = max(max_equity, equity)
                drawdown = (max_equity - equity) / max_equity
                max_drawdown = max(max_drawdown, drawdown)
                
                equity_curve.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "equity": round(equity, 2),
                    "daily_return": round(daily_return * 100, 4)
                })
        
        self._report_progress(60, "计算绩效指标...")
        
        # 计算指标
        total_return = (equity - self.config.initial_capital) / self.config.initial_capital
        years = days / 365
        annual_return = ((1 + total_return) ** (1 / years) - 1) if years > 0 else 0
        
        # 夏普比率
        if daily_returns:
            import statistics
            avg_return = statistics.mean(daily_returns)
            std_return = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0
            sharpe = ((avg_return * 252 - 0.03) / (std_return * (252 ** 0.5))) if std_return > 0 else 0
        else:
            sharpe = 0
        
        self._report_progress(80, "生成模拟交易记录...")
        
        # 生成交易记录
        trades = []
        for i in range(random.randint(20, 100)):
            trade_date = start + timedelta(days=random.randint(0, days))
            if trade_date.weekday() < 5:
                trades.append({
                    "date": trade_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "symbol": f"{random.randint(600000, 699999):06d}.SH",
                    "direction": random.choice(["buy", "sell"]),
                    "price": round(random.uniform(10, 100), 2),
                    "volume": random.randint(1, 100) * 100,
                    "amount": round(random.uniform(1000, 100000), 2),
                    "commission": round(random.uniform(1, 50), 2)
                })
        
        trades.sort(key=lambda x: x["date"])
        
        self._report_progress(90, "保存结果...")
        
        # 创建结果
        metrics = BacktestMetrics(
            total_return=round(total_return * 100, 2),
            annual_return=round(annual_return * 100, 2),
            max_drawdown=round(max_drawdown * 100, 2),
            sharpe_ratio=round(sharpe, 2),
            win_rate=round(random.uniform(0.4, 0.6) * 100, 2),
            trade_count=len(trades),
            profit_factor=round(random.uniform(1.0, 2.0), 2),
            avg_trade_return=round(random.uniform(-1, 3), 2),
            volatility=round(std_return * (252 ** 0.5) * 100, 2) if daily_returns else 0
        )
        
        result = BacktestResult(
            success=True,
            mode="mock",
            metrics=metrics,
            equity_curve=equity_curve,
            trades=trades,
            config=self.config.to_dict(),
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat()
        )
        
        # 保存结果
        result.save(self.config.output_dir)
        
        self._report_progress(100, "回测完成")
        
        return result
    
    def _parse_bt_result(self, output: str) -> BacktestResult:
        """解析 BulletTrade 输出"""
        self._report_progress(100, "回测完成")
        
        # 这里需要根据 BulletTrade 的实际输出格式进行解析
        return BacktestResult(
            success=True,
            mode="bullettrade",
            config=self.config.to_dict(),
            raw_output=output
        )


def run_backtest(
    strategy_path: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000.0,
    progress_callback: Optional[Callable[[int, str], None]] = None,
    **kwargs
) -> BacktestResult:
    """执行回测的便捷函数
    
    Args:
        strategy_path: 策略文件路径
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        progress_callback: 进度回调函数
        **kwargs: 其他配置参数
        
    Returns:
        回测结果
        
    Example:
        >>> result = run_backtest(
        ...     "strategies/my_strategy.py",
        ...     "2020-01-01",
        ...     "2023-12-31",
        ...     initial_capital=1000000
        ... )
        >>> print(result.metrics.total_return)
    """
    config = BacktestConfig(
        strategy_path=strategy_path,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        **kwargs
    )
    
    runner = BacktestRunner(config)
    
    if progress_callback:
        runner.set_progress_callback(progress_callback)
    
    return runner.run()



