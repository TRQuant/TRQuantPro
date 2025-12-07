"""回测结果处理

解析和存储回测结果
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class BacktestMetrics:
    """回测绩效指标
    
    Attributes:
        total_return: 总收益率 (%)
        annual_return: 年化收益率 (%)
        max_drawdown: 最大回撤 (%)
        sharpe_ratio: 夏普比率
        win_rate: 胜率 (%)
        trade_count: 交易次数
        profit_factor: 盈亏比
        avg_trade_return: 平均单笔收益 (%)
        volatility: 年化波动率 (%)
        calmar_ratio: 卡玛比率
        sortino_ratio: 索提诺比率
    """
    total_return: float = 0.0
    annual_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    trade_count: int = 0
    profit_factor: float = 0.0
    avg_trade_return: float = 0.0
    volatility: float = 0.0
    calmar_ratio: float = 0.0
    sortino_ratio: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "win_rate": self.win_rate,
            "trade_count": self.trade_count,
            "profit_factor": self.profit_factor,
            "avg_trade_return": self.avg_trade_return,
            "volatility": self.volatility,
            "calmar_ratio": self.calmar_ratio,
            "sortino_ratio": self.sortino_ratio
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BacktestMetrics":
        """从字典创建"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def summary(self) -> str:
        """生成摘要文本"""
        return f"""
回测绩效摘要
============
总收益率: {self.total_return:.2f}%
年化收益: {self.annual_return:.2f}%
最大回撤: {self.max_drawdown:.2f}%
夏普比率: {self.sharpe_ratio:.2f}
胜率: {self.win_rate:.2f}%
交易次数: {self.trade_count}
盈亏比: {self.profit_factor:.2f}
波动率: {self.volatility:.2f}%
""".strip()


@dataclass
class BacktestResult:
    """回测结果
    
    Attributes:
        success: 是否成功
        mode: 运行模式 ('bullettrade', 'mock')
        metrics: 绩效指标
        equity_curve: 净值曲线
        trades: 交易记录
        config: 回测配置
        error: 错误信息
        start_time: 开始时间
        end_time: 结束时间
        report_path: 报告路径
        raw_output: 原始输出
    """
    success: bool = False
    mode: str = "unknown"
    metrics: Optional[BacktestMetrics] = None
    equity_curve: List[Dict[str, Any]] = field(default_factory=list)
    trades: List[Dict[str, Any]] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    report_path: Optional[str] = None
    raw_output: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "mode": self.mode,
            "metrics": self.metrics.to_dict() if self.metrics else {},
            "equity_curve": self.equity_curve,
            "trades": self.trades,
            "config": self.config,
            "error": self.error,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "report_path": self.report_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BacktestResult":
        """从字典创建"""
        metrics = None
        if data.get("metrics"):
            metrics = BacktestMetrics.from_dict(data["metrics"])
        
        return cls(
            success=data.get("success", False),
            mode=data.get("mode", "unknown"),
            metrics=metrics,
            equity_curve=data.get("equity_curve", []),
            trades=data.get("trades", []),
            config=data.get("config", {}),
            error=data.get("error"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            report_path=data.get("report_path")
        )
    
    def save(self, output_dir: Optional[str] = None) -> str:
        """保存结果到文件
        
        Args:
            output_dir: 输出目录
            
        Returns:
            保存的目录路径
        """
        if not output_dir:
            output_dir = self.config.get("output_dir", "backtests/default")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存结果JSON
        result_file = output_path / "result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        
        # 保存净值曲线CSV
        if self.equity_curve:
            equity_df = pd.DataFrame(self.equity_curve)
            equity_df.to_csv(output_path / "equity_curve.csv", index=False)
        
        # 保存交易记录CSV
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(output_path / "trades.csv", index=False)
        
        logger.info(f"Results saved to: {output_dir}")
        return str(output_dir)
    
    @classmethod
    def load(cls, path: str) -> "BacktestResult":
        """从文件加载结果
        
        Args:
            path: 结果目录或JSON文件路径
            
        Returns:
            BacktestResult 实例
        """
        path = Path(path)
        
        if path.is_dir():
            result_file = path / "result.json"
        else:
            result_file = path
        
        with open(result_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def get_equity_dataframe(self) -> pd.DataFrame:
        """获取净值曲线 DataFrame"""
        if not self.equity_curve:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.equity_curve)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        return df
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """获取交易记录 DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.trades)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    
    def generate_report_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        if not self.success:
            return f"# 回测失败\n\n错误: {self.error}"
        
        config = self.config
        metrics = self.metrics
        
        report = f"""# 回测报告

## 基本信息

- **策略名称**: {config.get('strategy_name', 'N/A')}
- **策略版本**: {config.get('strategy_version', 'N/A')}
- **回测区间**: {config.get('start_date')} ~ {config.get('end_date')}
- **初始资金**: ¥{config.get('initial_capital', 0):,.0f}
- **基准指数**: {config.get('benchmark', 'N/A')}
- **运行模式**: {self.mode}

## 绩效指标

| 指标 | 值 |
|------|-----|
| 总收益率 | {metrics.total_return:.2f}% |
| 年化收益 | {metrics.annual_return:.2f}% |
| 最大回撤 | {metrics.max_drawdown:.2f}% |
| 夏普比率 | {metrics.sharpe_ratio:.2f} |
| 胜率 | {metrics.win_rate:.2f}% |
| 交易次数 | {metrics.trade_count} |
| 盈亏比 | {metrics.profit_factor:.2f} |
| 波动率 | {metrics.volatility:.2f}% |

## 交易统计

- 总交易次数: {len(self.trades)}
- 买入次数: {len([t for t in self.trades if t.get('direction') == 'buy'])}
- 卖出次数: {len([t for t in self.trades if t.get('direction') == 'sell'])}

## 生成时间

- 开始时间: {self.start_time or 'N/A'}
- 结束时间: {self.end_time or 'N/A'}
"""
        return report


def parse_bt_html_report(html_path: str) -> BacktestResult:
    """解析 BulletTrade HTML 报告
    
    Args:
        html_path: HTML报告文件路径
        
    Returns:
        BacktestResult 实例
    """
    from bs4 import BeautifulSoup
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # 这里需要根据 BulletTrade HTML报告的实际结构进行解析
    # 提取指标、净值曲线、交易记录等
    
    metrics = BacktestMetrics()
    # 解析指标...
    
    return BacktestResult(
        success=True,
        mode="bullettrade",
        metrics=metrics,
        report_path=html_path
    )



