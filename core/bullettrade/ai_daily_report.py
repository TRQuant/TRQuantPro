"""AI 实盘日报生成器

使用 LLM 分析实盘交易数据，生成智能分析报告：
- 每日交易分析
- 持仓分析
- 风险评估
- 改进建议
- 周报/月报汇总
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging

from .snapshot_manager import SnapshotManager, DailySnapshot

logger = logging.getLogger(__name__)


@dataclass
class DailyReportData:
    """日报数据"""
    date: str
    total_value: float
    daily_pnl: float
    daily_pnl_pct: float
    total_pnl: float
    total_pnl_pct: float
    positions_count: int
    trades_count: int
    winning_trades: int
    losing_trades: int
    largest_win: float
    largest_loss: float
    risk_level: str
    positions_summary: List[Dict[str, Any]]
    trades_summary: List[Dict[str, Any]]


class AIReportGenerator:
    """AI 日报生成器
    
    生成智能实盘分析报告
    
    Example:
        >>> generator = AIReportGenerator(snapshot_manager)
        >>> 
        >>> # 生成日报
        >>> report = generator.generate_daily_report("2025-01-06")
        >>> print(report)
        >>> 
        >>> # 生成周报
        >>> report = generator.generate_weekly_report("2025-01-06")
    """
    
    DAILY_PROMPT_TEMPLATE = """你是一位专业的量化交易分析师。请根据以下交易数据生成一份专业的实盘日报。

## 交易数据

### 账户概览
- 日期: {date}
- 总资产: {total_value:,.2f}
- 当日盈亏: {daily_pnl:,.2f} ({daily_pnl_pct:+.2f}%)
- 累计盈亏: {total_pnl:,.2f} ({total_pnl_pct:+.2f}%)

### 持仓统计
- 持仓数量: {positions_count}
- 总市值: {market_value:,.2f}
- 当前仓位: {position_ratio:.1f}%

### 交易统计
- 今日交易: {trades_count} 笔
- 盈利交易: {winning_trades} 笔
- 亏损交易: {losing_trades} 笔
- 最大盈利: {largest_win:,.2f}
- 最大亏损: {largest_loss:,.2f}

### 持仓明细
{positions_detail}

### 交易明细
{trades_detail}

### 风险状态
- 当前风险等级: {risk_level}
- 当前回撤: {current_drawdown:.2f}%

---

请生成一份包含以下内容的日报：

1. **今日总结**：简要概述今日交易情况和盈亏原因
2. **持仓分析**：分析当前持仓的风险和机会
3. **交易复盘**：分析今日交易的得失
4. **风险提示**：指出需要关注的风险点
5. **明日展望**：对明日交易的建议

请用简洁专业的语言，突出重点，给出可执行的建议。"""

    WEEKLY_PROMPT_TEMPLATE = """你是一位专业的量化交易分析师。请根据以下周度交易数据生成一份专业的周报。

## 周度数据

### 基本信息
- 统计周期: {start_date} ~ {end_date}
- 交易天数: {trading_days}

### 账户概览
- 期初资产: {start_value:,.2f}
- 期末资产: {end_value:,.2f}
- 周度盈亏: {weekly_pnl:,.2f} ({weekly_pnl_pct:+.2f}%)

### 绩效指标
- 周度收益率: {weekly_return:.2f}%
- 最大回撤: {max_drawdown:.2f}%
- 胜率: {win_rate:.1f}%
- 盈亏比: {profit_factor:.2f}

### 交易统计
- 总交易次数: {total_trades}
- 盈利交易: {winning_trades}
- 亏损交易: {losing_trades}
- 平均每日交易: {avg_daily_trades:.1f}

### 每日盈亏
{daily_pnl_detail}

### 持仓变化
{position_changes}

---

请生成一份包含以下内容的周报：

1. **本周总结**：概述本周市场情况和策略表现
2. **绩效分析**：分析收益来源和风险控制情况
3. **策略评估**：评估当前策略的有效性
4. **问题与改进**：指出存在的问题和改进方向
5. **下周展望**：对下周市场和操作的预期

请用数据说话，给出具体可行的建议。"""

    def __init__(
        self,
        snapshot_manager: SnapshotManager,
        output_dir: str = "live_trading/reports"
    ):
        """初始化 AI 报告生成器
        
        Args:
            snapshot_manager: 快照管理器
            output_dir: 报告输出目录
        """
        self.snapshot_manager = snapshot_manager
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_daily_report(
        self,
        date_str: str,
        use_llm: bool = False
    ) -> str:
        """生成日报
        
        Args:
            date_str: 日期
            use_llm: 是否使用 LLM 生成（否则使用模板）
            
        Returns:
            报告内容
        """
        # 获取快照数据
        snapshot = self.snapshot_manager.get_snapshot(date_str)
        if not snapshot:
            return f"未找到 {date_str} 的数据"
        
        # 准备报告数据
        report_data = self._prepare_daily_data(snapshot)
        
        # 生成报告
        if use_llm:
            report = self._generate_with_llm(
                self.DAILY_PROMPT_TEMPLATE,
                report_data
            )
        else:
            report = self._generate_template_report(report_data)
        
        # 保存报告
        report_path = self.output_dir / f"daily_{date_str.replace('-', '')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"生成日报: {report_path}")
        return report
    
    def generate_weekly_report(
        self,
        end_date: str,
        use_llm: bool = False
    ) -> str:
        """生成周报
        
        Args:
            end_date: 截止日期
            use_llm: 是否使用 LLM
            
        Returns:
            报告内容
        """
        # 计算周期
        end = datetime.strptime(end_date, "%Y-%m-%d")
        start = end - timedelta(days=6)
        start_date = start.strftime("%Y-%m-%d")
        
        # 获取周数据
        snapshots = self.snapshot_manager.get_snapshots(start_date, end_date)
        if not snapshots:
            return f"未找到 {start_date} ~ {end_date} 的数据"
        
        # 准备周报数据
        report_data = self._prepare_weekly_data(snapshots, start_date, end_date)
        
        # 生成报告
        if use_llm:
            report = self._generate_with_llm(
                self.WEEKLY_PROMPT_TEMPLATE,
                report_data
            )
        else:
            report = self._generate_weekly_template(report_data)
        
        # 保存报告
        week_num = end.isocalendar()[1]
        report_path = self.output_dir / f"weekly_{end.year}W{week_num:02d}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"生成周报: {report_path}")
        return report
    
    def _prepare_daily_data(self, snapshot: DailySnapshot) -> Dict[str, Any]:
        """准备日报数据"""
        # 分析交易
        winning_trades = 0
        losing_trades = 0
        largest_win = 0.0
        largest_loss = 0.0
        
        for trade in snapshot.trades:
            pnl = (trade.filled_price - trade.price) * trade.filled_amount
            if trade.side == 'sell':
                pnl = -pnl
            
            if pnl > 0:
                winning_trades += 1
                largest_win = max(largest_win, pnl)
            elif pnl < 0:
                losing_trades += 1
                largest_loss = min(largest_loss, pnl)
        
        # 持仓明细
        positions_detail = ""
        for pos in snapshot.positions:
            positions_detail += f"- {pos.security} ({pos.name}): {pos.amount}股, 市值{pos.market_value:,.0f}, 盈亏{pos.profit:+,.0f}({pos.profit_pct:+.2f}%)\n"
        
        # 交易明细
        trades_detail = ""
        for trade in snapshot.trades:
            trades_detail += f"- {trade.created_time} {trade.side.upper()} {trade.security}: {trade.filled_amount}股 @{trade.filled_price:.2f}\n"
        
        return {
            "date": snapshot.date,
            "total_value": snapshot.total_value,
            "daily_pnl": snapshot.daily_pnl,
            "daily_pnl_pct": snapshot.daily_pnl_pct,
            "total_pnl": snapshot.total_pnl,
            "total_pnl_pct": snapshot.total_pnl_pct,
            "market_value": snapshot.market_value,
            "position_ratio": snapshot.market_value / snapshot.total_value * 100 if snapshot.total_value > 0 else 0,
            "positions_count": len(snapshot.positions),
            "trades_count": len(snapshot.trades),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "largest_win": largest_win,
            "largest_loss": largest_loss,
            "risk_level": "正常",  # TODO: 从风控系统获取
            "current_drawdown": 0.0,  # TODO: 计算实际回撤
            "positions_detail": positions_detail or "无持仓",
            "trades_detail": trades_detail or "无交易"
        }
    
    def _prepare_weekly_data(
        self,
        snapshots: List[DailySnapshot],
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """准备周报数据"""
        first = snapshots[0]
        last = snapshots[-1]
        
        # 周度盈亏
        weekly_pnl = last.total_value - first.total_value
        weekly_pnl_pct = weekly_pnl / first.total_value * 100 if first.total_value > 0 else 0
        
        # 计算最大回撤
        max_drawdown = 0
        peak = first.total_value
        for s in snapshots:
            if s.total_value > peak:
                peak = s.total_value
            drawdown = (peak - s.total_value) / peak * 100
            max_drawdown = max(max_drawdown, drawdown)
        
        # 统计交易
        total_trades = sum(len(s.trades) for s in snapshots)
        all_trades = []
        for s in snapshots:
            all_trades.extend(s.trades)
        
        winning_trades = sum(1 for t in all_trades if t.status == 'filled')  # 简化
        losing_trades = total_trades - winning_trades
        
        # 每日盈亏
        daily_pnl_detail = ""
        for s in snapshots:
            emoji = "🟢" if s.daily_pnl >= 0 else "🔴"
            daily_pnl_detail += f"- {s.date}: {emoji} {s.daily_pnl:+,.0f} ({s.daily_pnl_pct:+.2f}%)\n"
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "trading_days": len(snapshots),
            "start_value": first.total_value,
            "end_value": last.total_value,
            "weekly_pnl": weekly_pnl,
            "weekly_pnl_pct": weekly_pnl_pct,
            "weekly_return": weekly_pnl_pct,
            "max_drawdown": max_drawdown,
            "win_rate": winning_trades / total_trades * 100 if total_trades > 0 else 0,
            "profit_factor": 1.5,  # TODO: 计算实际值
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "avg_daily_trades": total_trades / len(snapshots),
            "daily_pnl_detail": daily_pnl_detail,
            "position_changes": "详见每日报告"
        }
    
    def _generate_with_llm(
        self,
        template: str,
        data: Dict[str, Any]
    ) -> str:
        """使用 LLM 生成报告"""
        prompt = template.format(**data)
        
        # TODO: 集成实际的 LLM API
        # 这里返回格式化后的 prompt 作为占位
        return f"""# AI 分析报告

> 此报告需要 LLM 支持，当前显示原始数据

---

{prompt}

---

*请配置 LLM API 以获得智能分析*
"""
    
    def _generate_template_report(self, data: Dict[str, Any]) -> str:
        """使用模板生成日报"""
        pnl_emoji = "🟢" if data['daily_pnl'] >= 0 else "🔴"
        total_emoji = "📈" if data['total_pnl'] >= 0 else "📉"
        
        return f"""# 📊 实盘日报 - {data['date']}

## 📈 账户概览

| 指标 | 数值 |
|------|------|
| 总资产 | ¥{data['total_value']:,.2f} |
| 当日盈亏 | {pnl_emoji} ¥{data['daily_pnl']:+,.2f} ({data['daily_pnl_pct']:+.2f}%) |
| 累计盈亏 | {total_emoji} ¥{data['total_pnl']:+,.2f} ({data['total_pnl_pct']:+.2f}%) |
| 持仓数量 | {data['positions_count']} 只 |
| 当前仓位 | {data['position_ratio']:.1f}% |

## 📋 交易统计

| 指标 | 数值 |
|------|------|
| 今日交易 | {data['trades_count']} 笔 |
| 盈利交易 | {data['winning_trades']} 笔 |
| 亏损交易 | {data['losing_trades']} 笔 |
| 最大盈利 | ¥{data['largest_win']:,.2f} |
| 最大亏损 | ¥{data['largest_loss']:,.2f} |

## 📦 持仓明细

{data['positions_detail']}

## 📝 交易明细

{data['trades_detail']}

## ⚠️ 风险状态

- 风险等级：**{data['risk_level']}**
- 当前回撤：{data['current_drawdown']:.2f}%

---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*TRQuant 量化交易系统*
"""
    
    def _generate_weekly_template(self, data: Dict[str, Any]) -> str:
        """使用模板生成周报"""
        pnl_emoji = "🟢" if data['weekly_pnl'] >= 0 else "🔴"
        
        return f"""# 📊 实盘周报

## 📅 统计周期

**{data['start_date']} ~ {data['end_date']}** (共 {data['trading_days']} 个交易日)

## 📈 绩效概览

| 指标 | 数值 |
|------|------|
| 期初资产 | ¥{data['start_value']:,.2f} |
| 期末资产 | ¥{data['end_value']:,.2f} |
| 周度盈亏 | {pnl_emoji} ¥{data['weekly_pnl']:+,.2f} ({data['weekly_pnl_pct']:+.2f}%) |
| 最大回撤 | {data['max_drawdown']:.2f}% |
| 胜率 | {data['win_rate']:.1f}% |

## 📋 交易统计

| 指标 | 数值 |
|------|------|
| 总交易次数 | {data['total_trades']} |
| 盈利交易 | {data['winning_trades']} |
| 亏损交易 | {data['losing_trades']} |
| 日均交易 | {data['avg_daily_trades']:.1f} |

## 📆 每日盈亏

{data['daily_pnl_detail']}

## 📝 本周小结

本周整体表现{'良好' if data['weekly_pnl'] >= 0 else '欠佳'}，
周度收益率为 {data['weekly_pnl_pct']:+.2f}%。

### 亮点
- 胜率保持在 {data['win_rate']:.0f}%

### 待改进
- 最大回撤 {data['max_drawdown']:.2f}% 需要关注

---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*TRQuant 量化交易系统*
"""


