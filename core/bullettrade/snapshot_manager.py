"""持仓快照管理器

实现实盘交易的持仓和交易记录管理：
- 每日持仓快照
- 交易流水记录
- 历史数据查询
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, date
import json
import logging
import csv

logger = logging.getLogger(__name__)


@dataclass
class PositionRecord:
    """持仓记录"""
    security: str
    name: str
    amount: int
    available_amount: int
    cost_basis: float
    market_price: float
    market_value: float
    profit: float
    profit_pct: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TradeRecord:
    """交易记录"""
    order_id: str
    security: str
    name: str
    side: str  # 'buy' or 'sell'
    amount: int
    price: float
    filled_amount: int
    filled_price: float
    commission: float
    status: str
    created_time: str
    filled_time: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DailySnapshot:
    """每日快照"""
    date: str
    total_value: float
    cash: float
    market_value: float
    daily_pnl: float
    daily_pnl_pct: float
    total_pnl: float
    total_pnl_pct: float
    positions: List[PositionRecord] = field(default_factory=list)
    trades: List[TradeRecord] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "total_value": self.total_value,
            "cash": self.cash,
            "market_value": self.market_value,
            "daily_pnl": self.daily_pnl,
            "daily_pnl_pct": self.daily_pnl_pct,
            "total_pnl": self.total_pnl,
            "total_pnl_pct": self.total_pnl_pct,
            "positions": [p.to_dict() for p in self.positions],
            "trades": [t.to_dict() for t in self.trades]
        }


class SnapshotManager:
    """持仓快照管理器
    
    管理实盘交易的持仓快照和交易记录
    
    目录结构:
    live_trading/
    ├── snapshots/
    │   ├── 2025/
    │   │   ├── 01/
    │   │   │   ├── 20250101_snapshot.json
    │   │   │   └── 20250102_snapshot.json
    │   └── latest.json
    ├── trades/
    │   ├── trades_202501.csv
    │   └── trades_202502.csv
    └── positions/
        ├── positions_20250101.csv
        └── positions_20250102.csv
    
    Example:
        >>> manager = SnapshotManager("live_trading")
        >>> 
        >>> # 保存每日快照
        >>> snapshot = DailySnapshot(...)
        >>> manager.save_snapshot(snapshot)
        >>> 
        >>> # 查询历史
        >>> snapshots = manager.get_snapshots("2025-01-01", "2025-01-31")
    """
    
    def __init__(self, base_dir: str = "live_trading"):
        """初始化快照管理器
        
        Args:
            base_dir: 基础目录
        """
        self.base_dir = Path(base_dir)
        self._init_dirs()
    
    def _init_dirs(self) -> None:
        """初始化目录结构"""
        (self.base_dir / "snapshots").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "trades").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "positions").mkdir(parents=True, exist_ok=True)
    
    def save_snapshot(self, snapshot: DailySnapshot) -> str:
        """保存每日快照
        
        Args:
            snapshot: 快照数据
            
        Returns:
            保存路径
        """
        # 解析日期
        dt = datetime.strptime(snapshot.date, "%Y-%m-%d")
        year_month_dir = self.base_dir / "snapshots" / dt.strftime("%Y") / dt.strftime("%m")
        year_month_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存快照 JSON
        snapshot_path = year_month_dir / f"{dt.strftime('%Y%m%d')}_snapshot.json"
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新 latest.json
        latest_path = self.base_dir / "snapshots" / "latest.json"
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 保存持仓 CSV
        self._save_positions_csv(snapshot)
        
        # 保存交易 CSV
        self._save_trades_csv(snapshot)
        
        logger.info(f"保存快照: {snapshot_path}")
        return str(snapshot_path)
    
    def _save_positions_csv(self, snapshot: DailySnapshot) -> None:
        """保存持仓 CSV"""
        if not snapshot.positions:
            return
        
        dt = datetime.strptime(snapshot.date, "%Y-%m-%d")
        csv_path = self.base_dir / "positions" / f"positions_{dt.strftime('%Y%m%d')}.csv"
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(snapshot.positions[0].to_dict().keys()))
            writer.writeheader()
            for pos in snapshot.positions:
                writer.writerow(pos.to_dict())
    
    def _save_trades_csv(self, snapshot: DailySnapshot) -> None:
        """保存交易 CSV（追加模式）"""
        if not snapshot.trades:
            return
        
        dt = datetime.strptime(snapshot.date, "%Y-%m-%d")
        csv_path = self.base_dir / "trades" / f"trades_{dt.strftime('%Y%m')}.csv"
        
        file_exists = csv_path.exists()
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(snapshot.trades[0].to_dict().keys()))
            if not file_exists:
                writer.writeheader()
            for trade in snapshot.trades:
                writer.writerow(trade.to_dict())
    
    def get_latest_snapshot(self) -> Optional[DailySnapshot]:
        """获取最新快照"""
        latest_path = self.base_dir / "snapshots" / "latest.json"
        if not latest_path.exists():
            return None
        
        with open(latest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return self._dict_to_snapshot(data)
    
    def get_snapshot(self, date_str: str) -> Optional[DailySnapshot]:
        """获取指定日期快照
        
        Args:
            date_str: 日期字符串 (YYYY-MM-DD)
        """
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        snapshot_path = (
            self.base_dir / "snapshots" / dt.strftime("%Y") / 
            dt.strftime("%m") / f"{dt.strftime('%Y%m%d')}_snapshot.json"
        )
        
        if not snapshot_path.exists():
            return None
        
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return self._dict_to_snapshot(data)
    
    def get_snapshots(
        self,
        start_date: str,
        end_date: str
    ) -> List[DailySnapshot]:
        """获取日期范围内的快照
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            快照列表
        """
        from datetime import timedelta
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        snapshots = []
        current = start
        while current <= end:
            snapshot = self.get_snapshot(current.strftime("%Y-%m-%d"))
            if snapshot:
                snapshots.append(snapshot)
            current += timedelta(days=1)
        
        return snapshots
    
    def get_trades(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        security: Optional[str] = None
    ) -> List[TradeRecord]:
        """查询交易记录
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            security: 证券代码（筛选）
            
        Returns:
            交易记录列表
        """
        trades = []
        
        for csv_file in (self.base_dir / "trades").glob("trades_*.csv"):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 日期筛选
                    trade_date = row.get('created_time', '')[:10]
                    if start_date and trade_date < start_date:
                        continue
                    if end_date and trade_date > end_date:
                        continue
                    
                    # 证券筛选
                    if security and row.get('security') != security:
                        continue
                    
                    trades.append(TradeRecord(
                        order_id=row.get('order_id', ''),
                        security=row.get('security', ''),
                        name=row.get('name', ''),
                        side=row.get('side', ''),
                        amount=int(row.get('amount', 0)),
                        price=float(row.get('price', 0)),
                        filled_amount=int(row.get('filled_amount', 0)),
                        filled_price=float(row.get('filled_price', 0)),
                        commission=float(row.get('commission', 0)),
                        status=row.get('status', ''),
                        created_time=row.get('created_time', ''),
                        filled_time=row.get('filled_time', '')
                    ))
        
        return sorted(trades, key=lambda x: x.created_time)
    
    def get_performance_summary(
        self,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """获取绩效摘要
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            绩效摘要
        """
        snapshots = self.get_snapshots(start_date, end_date)
        
        if not snapshots:
            return {}
        
        first = snapshots[0]
        last = snapshots[-1]
        
        # 计算统计指标
        daily_returns = []
        for i in range(1, len(snapshots)):
            if snapshots[i-1].total_value > 0:
                daily_ret = (snapshots[i].total_value - snapshots[i-1].total_value) / snapshots[i-1].total_value
                daily_returns.append(daily_ret)
        
        # 计算最大回撤
        max_drawdown = 0
        peak = first.total_value
        for s in snapshots:
            if s.total_value > peak:
                peak = s.total_value
            drawdown = (peak - s.total_value) / peak * 100
            max_drawdown = max(max_drawdown, drawdown)
        
        # 计算夏普比率
        import statistics
        if len(daily_returns) > 1:
            avg_return = statistics.mean(daily_returns) * 252  # 年化
            std_return = statistics.stdev(daily_returns) * (252 ** 0.5)
            sharpe = avg_return / std_return if std_return > 0 else 0
        else:
            sharpe = 0
        
        # 统计交易
        trades = self.get_trades(start_date, end_date)
        winning_trades = sum(1 for t in trades if t.side == 'sell' and t.filled_price > t.price)
        win_rate = winning_trades / len(trades) * 100 if trades else 0
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "days": len(snapshots),
            "initial_value": first.total_value,
            "final_value": last.total_value,
            "total_return": last.total_pnl,
            "total_return_pct": last.total_pnl_pct,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
            "total_trades": len(trades),
            "win_rate": win_rate
        }
    
    def _dict_to_snapshot(self, data: Dict[str, Any]) -> DailySnapshot:
        """字典转换为快照对象"""
        positions = [
            PositionRecord(**p) for p in data.get('positions', [])
        ]
        trades = [
            TradeRecord(**t) for t in data.get('trades', [])
        ]
        
        return DailySnapshot(
            date=data['date'],
            total_value=data['total_value'],
            cash=data['cash'],
            market_value=data['market_value'],
            daily_pnl=data['daily_pnl'],
            daily_pnl_pct=data['daily_pnl_pct'],
            total_pnl=data['total_pnl'],
            total_pnl_pct=data['total_pnl_pct'],
            positions=positions,
            trades=trades
        )


def create_snapshot(
    date_str: str,
    account_info: Dict[str, Any],
    positions: List[Dict[str, Any]],
    trades: List[Dict[str, Any]],
    initial_value: float = 1000000.0
) -> DailySnapshot:
    """创建每日快照便捷函数
    
    Args:
        date_str: 日期
        account_info: 账户信息
        positions: 持仓列表
        trades: 交易列表
        initial_value: 初始资金
        
    Returns:
        快照对象
    """
    total_value = account_info.get('total_value', 0)
    yesterday_value = account_info.get('yesterday_value', total_value)
    
    daily_pnl = total_value - yesterday_value
    daily_pnl_pct = daily_pnl / yesterday_value * 100 if yesterday_value > 0 else 0
    total_pnl = total_value - initial_value
    total_pnl_pct = total_pnl / initial_value * 100
    
    return DailySnapshot(
        date=date_str,
        total_value=total_value,
        cash=account_info.get('cash', 0),
        market_value=account_info.get('market_value', 0),
        daily_pnl=daily_pnl,
        daily_pnl_pct=daily_pnl_pct,
        total_pnl=total_pnl,
        total_pnl_pct=total_pnl_pct,
        positions=[PositionRecord(**p) for p in positions],
        trades=[TradeRecord(**t) for t in trades]
    )


