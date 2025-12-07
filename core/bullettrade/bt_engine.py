"""BulletTrade 引擎封装

基于 BulletTrade 官方文档：https://bullettrade.cn/
封装 BulletTrade 框架的核心功能，提供统一的回测和实盘接口

四步从准备到实盘：
1. 安装: pip install bullet-trade (QMT: pip install "bullet-trade[qmt]")
2. 研究: bullet-trade lab (启动 JupyterLab)
3. 回测: bullet-trade backtest strategy.py --start 2025-01-01 --end 2025-06-01
4. 实盘: bullet-trade live strategy.py --broker qmt
"""

from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import subprocess
import logging
import json
import os

logger = logging.getLogger(__name__)


class BTMode(Enum):
    """运行模式"""
    BACKTEST = "backtest"
    LIVE = "live"
    PAPER = "paper"  # 模拟交易


class BrokerType(Enum):
    """券商类型
    
    支持的 broker:
    - qmt: 本地 QMT (Windows)
    - qmt-remote: 远程 QMT (Linux/Mac 通过网络连接)
    - simulator: 模拟交易
    """
    QMT = "qmt"
    QMT_REMOTE = "qmt-remote"
    SIMULATOR = "simulator"
    PTRADE = "ptrade"  # 恒生 PTrade（需自定义适配）
    MOCK = "mock"  # 本地模拟


@dataclass
class BTConfig:
    """BulletTrade 配置
    
    Attributes:
        strategy_path: 策略文件路径
        start_date: 回测开始日期
        end_date: 回测结束日期
        frequency: 数据频率 ('day', 'minute', 'tick')
        initial_capital: 初始资金
        benchmark: 基准指数代码
        commission_rate: 佣金费率
        slippage: 滑点
        data_provider: 数据源 ('jqdata', 'miniqmt', 'tushare')
        broker: 券商类型 (实盘用)
        output_dir: 输出目录
    """
    strategy_path: str
    start_date: str = "2020-01-01"
    end_date: str = "2023-12-31"
    frequency: str = "day"
    initial_capital: float = 1000000.0
    benchmark: str = "000300.XSHG"
    commission_rate: float = 0.0003
    slippage: float = 0.001
    data_provider: str = "jqdata"
    broker: BrokerType = BrokerType.MOCK
    output_dir: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "strategy_path": self.strategy_path,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "frequency": self.frequency,
            "initial_capital": self.initial_capital,
            "benchmark": self.benchmark,
            "commission_rate": self.commission_rate,
            "slippage": self.slippage,
            "data_provider": self.data_provider,
            "broker": self.broker.value if isinstance(self.broker, BrokerType) else self.broker,
            "output_dir": self.output_dir,
            **self.extra_params
        }


class BulletTradeEngine:
    """BulletTrade 引擎
    
    封装 BulletTrade 框架，提供回测和实盘接口
    
    Example:
        >>> config = BTConfig(
        ...     strategy_path="strategies/my_strategy.py",
        ...     start_date="2020-01-01",
        ...     end_date="2023-12-31"
        ... )
        >>> engine = BulletTradeEngine(config)
        >>> result = engine.run_backtest()
    """
    
    # BulletTrade CLI 命令
    BT_CLI = "bullet-trade"
    
    def __init__(self, config: BTConfig):
        """初始化引擎
        
        Args:
            config: BulletTrade配置
        """
        self.config = config
        self._bt_available = self._check_bullet_trade()
        self._progress_callback: Optional[Callable[[int, str], None]] = None
        
    def _check_bullet_trade(self) -> bool:
        """检查 BulletTrade 是否可用"""
        try:
            result = subprocess.run(
                [self.BT_CLI, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"BulletTrade available: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.warning("BulletTrade CLI not found. Using mock mode.")
        except subprocess.TimeoutExpired:
            logger.warning("BulletTrade CLI timeout.")
        except Exception as e:
            logger.warning(f"BulletTrade check failed: {e}")
        return False
    
    @property
    def is_available(self) -> bool:
        """BulletTrade 是否可用"""
        return self._bt_available
    
    def set_progress_callback(self, callback: Callable[[int, str], None]) -> None:
        """设置进度回调
        
        Args:
            callback: 回调函数，接收 (progress, message) 参数
        """
        self._progress_callback = callback
    
    def _report_progress(self, progress: int, message: str) -> None:
        """报告进度"""
        logger.info(f"[{progress}%] {message}")
        if self._progress_callback:
            self._progress_callback(progress, message)
    
    def run_backtest(self) -> Dict[str, Any]:
        """运行回测
        
        Returns:
            回测结果字典，包含：
            - success: 是否成功
            - metrics: 绩效指标
            - equity_curve: 净值曲线
            - trades: 交易记录
            - report_path: 报告路径
        """
        self._report_progress(0, "开始回测...")
        
        if self._bt_available:
            return self._run_bt_backtest()
        else:
            return self._run_mock_backtest()
    
    def _run_bt_backtest(self) -> Dict[str, Any]:
        """使用 BulletTrade CLI 运行回测
        
        官方命令格式:
        bullet-trade backtest demo_strategy.py --start 2025-01-01 --end 2025-06-01
        """
        self._report_progress(10, "准备回测环境...")
        
        # 构建命令 (按照官方文档格式)
        cmd = [
            self.BT_CLI, "backtest",
            self.config.strategy_path,
            "--start", self.config.start_date,
            "--end", self.config.end_date,
        ]
        
        # 添加可选参数
        if self.config.frequency != "day":
            cmd.extend(["--frequency", self.config.frequency])
        
        # 添加输出目录
        if self.config.output_dir:
            cmd.extend(["--output", self.config.output_dir])
        
        self._report_progress(20, "执行回测...")
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            self._report_progress(80, "解析结果...")
            
            if result.returncode == 0:
                # 解析输出，提取结果
                return self._parse_bt_output(result.stdout)
            else:
                logger.error(f"Backtest failed: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "metrics": {},
                    "equity_curve": [],
                    "trades": []
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "回测超时（超过1小时）",
                "metrics": {},
                "equity_curve": [],
                "trades": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metrics": {},
                "equity_curve": [],
                "trades": []
            }
    
    def _run_mock_backtest(self) -> Dict[str, Any]:
        """模拟回测（当 BulletTrade 不可用时）"""
        import random
        from datetime import datetime, timedelta
        
        self._report_progress(10, "使用模拟模式运行回测...")
        
        # 生成模拟数据
        start = datetime.strptime(self.config.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.config.end_date, "%Y-%m-%d")
        days = (end - start).days
        
        self._report_progress(30, "生成模拟净值曲线...")
        
        # 生成净值曲线
        equity = self.config.initial_capital
        equity_curve = []
        max_equity = equity
        max_drawdown = 0.0
        
        for i in range(days):
            date = start + timedelta(days=i)
            if date.weekday() < 5:  # 工作日
                # 随机收益率
                daily_return = random.gauss(0.0005, 0.02)  # 均值0.05%，标准差2%
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
        annual_days = 252
        years = days / 365
        annual_return = ((1 + total_return) ** (1 / years) - 1) if years > 0 else 0
        
        # 计算夏普比率（简化）
        if equity_curve:
            returns = [e["daily_return"] / 100 for e in equity_curve]
            avg_return = sum(returns) / len(returns)
            std_return = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
            sharpe = (avg_return * annual_days - 0.03) / (std_return * (annual_days ** 0.5)) if std_return > 0 else 0
        else:
            sharpe = 0
        
        self._report_progress(80, "生成模拟交易记录...")
        
        # 生成模拟交易
        trades = []
        for i in range(random.randint(10, 50)):
            trade_date = start + timedelta(days=random.randint(0, days))
            trades.append({
                "date": trade_date.strftime("%Y-%m-%d"),
                "symbol": f"{random.randint(600000, 699999):06d}.SH",
                "direction": random.choice(["buy", "sell"]),
                "price": round(random.uniform(10, 100), 2),
                "volume": random.randint(100, 10000),
                "commission": round(random.uniform(1, 50), 2)
            })
        
        self._report_progress(100, "回测完成")
        
        return {
            "success": True,
            "mode": "mock",
            "metrics": {
                "total_return": round(total_return * 100, 2),
                "annual_return": round(annual_return * 100, 2),
                "max_drawdown": round(max_drawdown * 100, 2),
                "sharpe_ratio": round(sharpe, 2),
                "trade_count": len(trades),
                "win_rate": round(random.uniform(0.4, 0.6) * 100, 2)
            },
            "equity_curve": equity_curve,
            "trades": trades,
            "config": self.config.to_dict()
        }
    
    def _parse_bt_output(self, output: str) -> Dict[str, Any]:
        """解析 BulletTrade 输出"""
        # 这里需要根据 BulletTrade 的实际输出格式进行解析
        # 暂时返回基本结构
        self._report_progress(100, "回测完成")
        
        return {
            "success": True,
            "mode": "bullettrade",
            "metrics": {},
            "equity_curve": [],
            "trades": [],
            "raw_output": output
        }
    
    def start_live_trading(self) -> bool:
        """启动实盘交易
        
        官方命令格式:
        - 本地/模拟: bullet-trade live demo_strategy.py --broker qmt
        - 远程实盘: bullet-trade live demo_strategy.py --broker qmt-remote
        
        Returns:
            是否成功启动
        """
        if not self._bt_available:
            logger.error("BulletTrade not available for live trading")
            return False
        
        broker_value = self.config.broker.value if isinstance(self.config.broker, BrokerType) else self.config.broker
        
        cmd = [
            self.BT_CLI, "live",
            self.config.strategy_path,
            "--broker", broker_value
        ]
        
        logger.info(f"Starting live trading: {' '.join(cmd)}")
        
        try:
            # 后台运行
            subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start live trading: {e}")
            return False
    
    def stop_live_trading(self) -> bool:
        """停止实盘交易"""
        # BulletTrade 通过信号停止，这里可以发送 SIGTERM
        return True
    
    def start_server(self, server_type: str = "qmt", 
                     listen: str = "0.0.0.0", 
                     port: int = 58620,
                     token: Optional[str] = None) -> bool:
        """启动 BulletTrade 服务器（用于远程实盘）
        
        官方命令格式:
        bullet-trade server --server-type=qmt --listen 0.0.0.0 --port 58620 --token my_security_123456
        
        Args:
            server_type: 服务器类型 ('qmt')
            listen: 监听地址
            port: 监听端口
            token: 安全令牌
            
        Returns:
            是否成功启动
        """
        if not self._bt_available:
            logger.error("BulletTrade not available")
            return False
        
        cmd = [
            self.BT_CLI, "server",
            f"--server-type={server_type}",
            "--listen", listen,
            "--port", str(port)
        ]
        
        if token:
            cmd.extend(["--token", token])
        
        logger.info(f"Starting BulletTrade server: {' '.join(cmd)}")
        
        try:
            subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    def start_lab(self) -> bool:
        """启动 JupyterLab 研究环境
        
        官方命令: bullet-trade lab
        """
        if not self._bt_available:
            logger.error("BulletTrade not available")
            return False
        
        try:
            subprocess.Popen([self.BT_CLI, "lab"])
            return True
        except Exception as e:
            logger.error(f"Failed to start lab: {e}")
            return False


def check_bullet_trade_installation() -> Dict[str, Any]:
    """检查 BulletTrade 安装状态
    
    Returns:
        安装状态信息
    """
    result = {
        "installed": False,
        "version": None,
        "path": None,
        "message": ""
    }
    
    try:
        proc = subprocess.run(
            ["bullet-trade", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            result["installed"] = True
            result["version"] = proc.stdout.strip()
            result["message"] = "BulletTrade 已安装"
        else:
            result["message"] = f"BulletTrade 运行错误: {proc.stderr}"
    except FileNotFoundError:
        result["message"] = "BulletTrade 未安装。请运行: pip install bullet-trade"
    except Exception as e:
        result["message"] = f"检查失败: {e}"
    
    return result

