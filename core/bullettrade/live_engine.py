"""实盘交易引擎

基于 BulletTrade 官方 `bullet-trade live` 命令
实现本地/远程实盘交易

官方命令格式:
# 本地 QMT
bullet-trade live strategies/demo_strategy.py --broker qmt

# 远程 QMT
bullet-trade live strategies/demo_strategy.py --broker qmt-remote
"""

from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime, time
import subprocess
import threading
import queue
import json
import logging
import os
import signal

logger = logging.getLogger(__name__)

# BulletTrade CLI
BT_CLI = "bullet-trade"


class BrokerType(Enum):
    """Broker 类型"""
    QMT = "qmt"              # 本地 QMT
    QMT_REMOTE = "qmt-remote"  # 远程 QMT
    SIMULATOR = "simulator"   # 模拟交易


class LiveEngineStatus(Enum):
    """实盘引擎状态"""
    STOPPED = "stopped"       # 已停止
    STARTING = "starting"     # 启动中
    RUNNING = "running"       # 运行中
    PAUSED = "paused"         # 已暂停
    STOPPING = "stopping"     # 停止中
    ERROR = "error"           # 错误


@dataclass
class LiveEngineConfig:
    """实盘引擎配置
    
    Attributes:
        strategy_path: 策略文件路径
        broker: Broker 类型
        account_id: 账户ID（可选）
        env_file: 环境配置文件路径
        log_dir: 日志目录
    """
    strategy_path: str
    broker: BrokerType = BrokerType.SIMULATOR
    account_id: Optional[str] = None
    env_file: Optional[str] = None
    log_dir: str = "live_trading/logs"
    
    def __post_init__(self):
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)


@dataclass
class Position:
    """持仓信息"""
    security: str
    amount: int
    cost_basis: float
    market_value: float
    profit: float
    profit_pct: float


@dataclass
class Trade:
    """交易记录"""
    order_id: str
    security: str
    side: str  # 'buy' or 'sell'
    amount: int
    price: float
    filled_amount: int
    filled_price: float
    status: str
    created_time: datetime
    updated_time: datetime


@dataclass
class AccountInfo:
    """账户信息"""
    cash: float
    available_cash: float
    total_value: float
    positions: List[Position] = field(default_factory=list)
    trades_today: List[Trade] = field(default_factory=list)


class LiveTradingEngine:
    """实盘交易引擎
    
    封装 BulletTrade 的实盘交易功能
    
    Example:
        >>> config = LiveEngineConfig(
        ...     strategy_path="strategies/my_strategy.py",
        ...     broker=BrokerType.QMT
        ... )
        >>> engine = LiveTradingEngine(config)
        >>> engine.start()
        >>> # ... 监控交易 ...
        >>> engine.stop()
    """
    
    def __init__(self, config: LiveEngineConfig):
        """初始化实盘引擎
        
        Args:
            config: 引擎配置
        """
        self.config = config
        self._status = LiveEngineStatus.STOPPED
        self._process: Optional[subprocess.Popen] = None
        self._log_thread: Optional[threading.Thread] = None
        self._message_queue: queue.Queue = queue.Queue()
        self._bt_available = self._check_bt()
        
        # 回调函数
        self._on_status_change: Optional[Callable[[LiveEngineStatus], None]] = None
        self._on_trade: Optional[Callable[[Trade], None]] = None
        self._on_position_update: Optional[Callable[[Position], None]] = None
        self._on_log: Optional[Callable[[str], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None
    
    @property
    def status(self) -> LiveEngineStatus:
        """获取当前状态"""
        return self._status
    
    def _check_bt(self) -> bool:
        """检查 BulletTrade CLI 是否可用"""
        try:
            result = subprocess.run(
                [BT_CLI, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def set_callbacks(
        self,
        on_status_change: Optional[Callable[[LiveEngineStatus], None]] = None,
        on_trade: Optional[Callable[[Trade], None]] = None,
        on_position_update: Optional[Callable[[Position], None]] = None,
        on_log: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ) -> None:
        """设置回调函数"""
        self._on_status_change = on_status_change
        self._on_trade = on_trade
        self._on_position_update = on_position_update
        self._on_log = on_log
        self._on_error = on_error
    
    def _set_status(self, status: LiveEngineStatus) -> None:
        """设置状态"""
        self._status = status
        if self._on_status_change:
            self._on_status_change(status)
    
    def _log(self, message: str) -> None:
        """记录日志"""
        logger.info(message)
        if self._on_log:
            self._on_log(message)
    
    def _error(self, message: str) -> None:
        """记录错误"""
        logger.error(message)
        if self._on_error:
            self._on_error(message)
    
    def start(self) -> bool:
        """启动实盘交易
        
        Returns:
            是否成功启动
        """
        if self._status == LiveEngineStatus.RUNNING:
            self._log("实盘引擎已在运行中")
            return True
        
        self._set_status(LiveEngineStatus.STARTING)
        self._log("正在启动实盘交易...")
        
        if self._bt_available:
            return self._start_with_bt()
        else:
            return self._start_simulator()
    
    def _start_with_bt(self) -> bool:
        """使用 BulletTrade CLI 启动"""
        cmd = [
            BT_CLI, "live",
            self.config.strategy_path,
            "--broker", self.config.broker.value
        ]
        
        if self.config.account_id:
            cmd.extend(["--account", self.config.account_id])
        
        self._log(f"执行命令: {' '.join(cmd)}")
        
        try:
            # 设置环境变量
            env = os.environ.copy()
            if self.config.env_file and Path(self.config.env_file).exists():
                self._load_env_file(self.config.env_file, env)
            
            # 启动进程
            log_file = Path(self.config.log_dir) / f"live_{datetime.now():%Y%m%d_%H%M%S}.log"
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                cwd=os.getcwd()
            )
            
            # 启动日志读取线程
            self._log_thread = threading.Thread(
                target=self._read_output,
                args=(log_file,),
                daemon=True
            )
            self._log_thread.start()
            
            self._set_status(LiveEngineStatus.RUNNING)
            self._log("实盘交易已启动")
            return True
            
        except Exception as e:
            self._error(f"启动失败: {e}")
            self._set_status(LiveEngineStatus.ERROR)
            return False
    
    def _start_simulator(self) -> bool:
        """启动模拟交易"""
        self._log("使用模拟模式运行")
        self._set_status(LiveEngineStatus.RUNNING)
        
        # 启动模拟线程
        self._log_thread = threading.Thread(
            target=self._run_simulator,
            daemon=True
        )
        self._log_thread.start()
        
        return True
    
    def _run_simulator(self) -> None:
        """运行模拟交易"""
        import time
        import random
        
        self._log("模拟交易开始运行")
        
        while self._status == LiveEngineStatus.RUNNING:
            # 模拟交易活动
            if random.random() < 0.1:  # 10% 概率产生交易
                trade = Trade(
                    order_id=f"SIM{datetime.now():%Y%m%d%H%M%S}",
                    security="000001.XSHE",
                    side="buy" if random.random() > 0.5 else "sell",
                    amount=100,
                    price=10.0 + random.gauss(0, 0.5),
                    filled_amount=100,
                    filled_price=10.0,
                    status="filled",
                    created_time=datetime.now(),
                    updated_time=datetime.now()
                )
                
                if self._on_trade:
                    self._on_trade(trade)
                
                self._log(f"模拟交易: {trade.side} {trade.security} {trade.amount}股 @{trade.price:.2f}")
            
            time.sleep(5)
        
        self._log("模拟交易已停止")
    
    def _read_output(self, log_file: Path) -> None:
        """读取进程输出"""
        if not self._process:
            return
        
        with open(log_file, 'w', encoding='utf-8') as f:
            while self._process and self._process.poll() is None:
                line = self._process.stdout.readline()
                if line:
                    line = line.strip()
                    f.write(f"{line}\n")
                    f.flush()
                    self._parse_output(line)
        
        if self._process and self._process.returncode != 0:
            self._error(f"进程异常退出，退出码: {self._process.returncode}")
            self._set_status(LiveEngineStatus.ERROR)
    
    def _parse_output(self, line: str) -> None:
        """解析输出日志"""
        self._log(line)
        
        # 解析交易信息
        if "ORDER" in line or "TRADE" in line:
            # TODO: 解析交易日志
            pass
        
        # 解析错误信息
        if "ERROR" in line or "Exception" in line:
            self._error(line)
    
    def _load_env_file(self, env_file: str, env: Dict[str, str]) -> None:
        """加载环境变量文件"""
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    
    def stop(self) -> bool:
        """停止实盘交易
        
        Returns:
            是否成功停止
        """
        if self._status == LiveEngineStatus.STOPPED:
            return True
        
        self._set_status(LiveEngineStatus.STOPPING)
        self._log("正在停止实盘交易...")
        
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None
        
        self._set_status(LiveEngineStatus.STOPPED)
        self._log("实盘交易已停止")
        return True
    
    def pause(self) -> bool:
        """暂停交易"""
        if self._status != LiveEngineStatus.RUNNING:
            return False
        
        self._set_status(LiveEngineStatus.PAUSED)
        self._log("实盘交易已暂停")
        return True
    
    def resume(self) -> bool:
        """恢复交易"""
        if self._status != LiveEngineStatus.PAUSED:
            return False
        
        self._set_status(LiveEngineStatus.RUNNING)
        self._log("实盘交易已恢复")
        return True
    
    def get_account_info(self) -> Optional[AccountInfo]:
        """获取账户信息"""
        # TODO: 通过 BulletTrade 获取实时账户信息
        return AccountInfo(
            cash=1000000.0,
            available_cash=800000.0,
            total_value=1200000.0
        )
    
    def get_positions(self) -> List[Position]:
        """获取持仓列表"""
        # TODO: 通过 BulletTrade 获取实时持仓
        return []
    
    def get_today_trades(self) -> List[Trade]:
        """获取今日交易记录"""
        # TODO: 通过 BulletTrade 获取交易记录
        return []


class QMTServerManager:
    """QMT 服务管理器
    
    用于管理 Windows 端的 QMT 服务
    
    官方命令:
    bullet-trade server --listen 0.0.0.0 --port 58620 --token secret --enable-data --enable-broker
    """
    
    def __init__(
        self,
        listen: str = "0.0.0.0",
        port: int = 58620,
        token: str = "secret",
        enable_data: bool = True,
        enable_broker: bool = True
    ):
        self.listen = listen
        self.port = port
        self.token = token
        self.enable_data = enable_data
        self.enable_broker = enable_broker
        self._process: Optional[subprocess.Popen] = None
    
    def start(self) -> bool:
        """启动 QMT 服务"""
        cmd = [
            BT_CLI, "server",
            "--listen", self.listen,
            "--port", str(self.port),
            "--token", self.token
        ]
        
        if self.enable_data:
            cmd.append("--enable-data")
        if self.enable_broker:
            cmd.append("--enable-broker")
        
        logger.info(f"Starting QMT server: {' '.join(cmd)}")
        
        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start QMT server: {e}")
            return False
    
    def stop(self) -> bool:
        """停止 QMT 服务"""
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=10)
            self._process = None
        return True
    
    def get_server_url(self) -> str:
        """获取服务器 URL"""
        return f"http://{self.listen}:{self.port}"


