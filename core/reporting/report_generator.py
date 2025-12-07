"""报告生成器

生成回测和实盘分析报告
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成器
    
    生成 Markdown、HTML 格式的回测和实盘报告
    
    Example:
        >>> generator = ReportGenerator()
        >>> report = generator.generate_backtest_report(result)
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """初始化报告生成器
        
        Args:
            template_dir: 报告模板目录
        """
        self.template_dir = template_dir
    
    def generate_backtest_report(
        self,
        result: Dict[str, Any],
        output_path: Optional[str] = None,
        format: str = "markdown"
    ) -> str:
        """生成回测报告
        
        Args:
            result: 回测结果字典
            output_path: 输出路径
            format: 报告格式 ('markdown', 'html')
            
        Returns:
            报告内容
        """
        if format == "markdown":
            report = self._generate_markdown_report(result)
        elif format == "html":
            report = self._generate_html_report(result)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to: {output_path}")
        
        return report
    
    def _generate_markdown_report(self, result: Dict[str, Any]) -> str:
        """生成 Markdown 格式报告"""
        config = result.get("config", {})
        metrics = result.get("metrics", {})
        trades = result.get("trades", [])
        equity_curve = result.get("equity_curve", [])
        
        # 基本信息
        report = f"""# 📊 策略回测报告

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📌 基本信息

| 项目 | 值 |
|------|-----|
| **策略名称** | {config.get('strategy_name', 'N/A')} |
| **策略版本** | {config.get('strategy_version', 'N/A')} |
| **回测区间** | {config.get('start_date', 'N/A')} ~ {config.get('end_date', 'N/A')} |
| **初始资金** | ¥{config.get('initial_capital', 0):,.0f} |
| **基准指数** | {config.get('benchmark', 'N/A')} |
| **数据频率** | {config.get('frequency', 'N/A')} |
| **佣金费率** | {config.get('commission_rate', 0) * 100:.2f}% |
| **滑点** | {config.get('slippage', 0) * 100:.2f}% |

---

## 📈 核心指标

### 收益指标

| 指标 | 值 | 评价 |
|------|-----|------|
| **总收益率** | {metrics.get('total_return', 0):.2f}% | {self._evaluate_return(metrics.get('total_return', 0))} |
| **年化收益** | {metrics.get('annual_return', 0):.2f}% | {self._evaluate_annual_return(metrics.get('annual_return', 0))} |
| **最大回撤** | {metrics.get('max_drawdown', 0):.2f}% | {self._evaluate_drawdown(metrics.get('max_drawdown', 0))} |

### 风险调整指标

| 指标 | 值 | 评价 |
|------|-----|------|
| **夏普比率** | {metrics.get('sharpe_ratio', 0):.2f} | {self._evaluate_sharpe(metrics.get('sharpe_ratio', 0))} |
| **盈亏比** | {metrics.get('profit_factor', 0):.2f} | {self._evaluate_profit_factor(metrics.get('profit_factor', 0))} |
| **波动率** | {metrics.get('volatility', 0):.2f}% | - |

### 交易统计

| 指标 | 值 |
|------|-----|
| **交易次数** | {metrics.get('trade_count', 0)} |
| **胜率** | {metrics.get('win_rate', 0):.2f}% |
| **平均收益** | {metrics.get('avg_trade_return', 0):.2f}% |

---

## 📊 净值曲线

"""
        # 添加净值数据（如果有）
        if equity_curve:
            report += "| 日期 | 净值 | 日收益率 |\n"
            report += "|------|------|----------|\n"
            for point in equity_curve[-10:]:  # 只显示最后10个数据点
                report += f"| {point.get('date', 'N/A')} | ¥{point.get('equity', 0):,.2f} | {point.get('daily_return', 0):.2f}% |\n"
            
            if len(equity_curve) > 10:
                report += f"\n*（仅显示最后10条记录，共{len(equity_curve)}条）*\n"
        
        report += "\n---\n\n"
        
        # 交易记录
        report += "## 📝 交易记录\n\n"
        
        if trades:
            report += "| 时间 | 代码 | 方向 | 价格 | 数量 | 金额 |\n"
            report += "|------|------|------|------|------|------|\n"
            for trade in trades[-20:]:  # 只显示最后20笔
                direction = "🔴 买入" if trade.get('direction') == 'buy' else "🟢 卖出"
                report += f"| {trade.get('date', 'N/A')} | {trade.get('symbol', 'N/A')} | {direction} | ¥{trade.get('price', 0):.2f} | {trade.get('volume', 0)} | ¥{trade.get('amount', 0):,.2f} |\n"
            
            if len(trades) > 20:
                report += f"\n*（仅显示最后20条记录，共{len(trades)}条）*\n"
        else:
            report += "*暂无交易记录*\n"
        
        report += "\n---\n\n"
        
        # 总结
        report += f"""## 💡 总结

### 策略表现

- 在 {config.get('start_date', 'N/A')} 至 {config.get('end_date', 'N/A')} 期间，策略取得了 **{metrics.get('total_return', 0):.2f}%** 的总收益
- 年化收益率为 **{metrics.get('annual_return', 0):.2f}%**，最大回撤 **{metrics.get('max_drawdown', 0):.2f}%**
- 夏普比率 **{metrics.get('sharpe_ratio', 0):.2f}**，风险调整后收益{self._sharpe_comment(metrics.get('sharpe_ratio', 0))}
- 共进行了 **{metrics.get('trade_count', 0)}** 笔交易，胜率 **{metrics.get('win_rate', 0):.2f}%**

### 注意事项

- 本报告基于历史数据回测，不代表未来表现
- 建议结合市场环境和策略逻辑进行综合评估
- 实盘前请进行充分的模拟验证

---

*报告由 TRQuant 量化系统自动生成*
"""
        return report
    
    def _generate_html_report(self, result: Dict[str, Any]) -> str:
        """生成 HTML 格式报告"""
        md_report = self._generate_markdown_report(result)
        
        # 简单的 Markdown to HTML 转换
        try:
            import markdown
            html_content = markdown.markdown(md_report, extensions=['tables'])
        except ImportError:
            html_content = f"<pre>{md_report}</pre>"
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>策略回测报告</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        h1 {{
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #007bff;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        blockquote {{
            border-left: 4px solid #007bff;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
        return html
    
    def _evaluate_return(self, value: float) -> str:
        if value > 50:
            return "🌟 优秀"
        elif value > 20:
            return "✅ 良好"
        elif value > 0:
            return "➖ 一般"
        else:
            return "⚠️ 亏损"
    
    def _evaluate_annual_return(self, value: float) -> str:
        if value > 30:
            return "🌟 优秀"
        elif value > 15:
            return "✅ 良好"
        elif value > 5:
            return "➖ 一般"
        else:
            return "⚠️ 偏低"
    
    def _evaluate_drawdown(self, value: float) -> str:
        if value < 10:
            return "🌟 优秀"
        elif value < 20:
            return "✅ 可控"
        elif value < 30:
            return "⚠️ 偏高"
        else:
            return "❌ 风险高"
    
    def _evaluate_sharpe(self, value: float) -> str:
        if value > 2:
            return "🌟 优秀"
        elif value > 1:
            return "✅ 良好"
        elif value > 0.5:
            return "➖ 一般"
        else:
            return "⚠️ 偏低"
    
    def _evaluate_profit_factor(self, value: float) -> str:
        if value > 2:
            return "🌟 优秀"
        elif value > 1.5:
            return "✅ 良好"
        elif value > 1:
            return "➖ 一般"
        else:
            return "⚠️ 偏低"
    
    def _sharpe_comment(self, value: float) -> str:
        if value > 2:
            return "优秀"
        elif value > 1:
            return "良好"
        elif value > 0.5:
            return "一般"
        else:
            return "有待提升"
    
    def generate_live_daily_report(
        self,
        trading_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """生成实盘日报
        
        Args:
            trading_data: 交易数据
            output_path: 输出路径
            
        Returns:
            报告内容
        """
        date = trading_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        report = f"""# 📈 实盘日报 - {date}

## 今日概况

| 项目 | 值 |
|------|-----|
| **账户净值** | ¥{trading_data.get('total_value', 0):,.2f} |
| **可用资金** | ¥{trading_data.get('available_cash', 0):,.2f} |
| **持仓市值** | ¥{trading_data.get('positions_value', 0):,.2f} |
| **今日盈亏** | ¥{trading_data.get('daily_pnl', 0):,.2f} |
| **今日收益率** | {trading_data.get('daily_return', 0):.2f}% |

## 今日交易

"""
        trades = trading_data.get("trades", [])
        if trades:
            report += "| 时间 | 代码 | 方向 | 价格 | 数量 | 金额 |\n"
            report += "|------|------|------|------|------|------|\n"
            for trade in trades:
                direction = "买入" if trade.get('direction') == 'buy' else "卖出"
                report += f"| {trade.get('time', 'N/A')} | {trade.get('symbol', 'N/A')} | {direction} | ¥{trade.get('price', 0):.2f} | {trade.get('volume', 0)} | ¥{trade.get('amount', 0):,.2f} |\n"
        else:
            report += "*今日无交易*\n"
        
        report += "\n## 当前持仓\n\n"
        
        positions = trading_data.get("positions", [])
        if positions:
            report += "| 代码 | 名称 | 数量 | 成本 | 现价 | 盈亏 |\n"
            report += "|------|------|------|------|------|------|\n"
            for pos in positions:
                pnl = pos.get('pnl', 0)
                pnl_sign = "+" if pnl >= 0 else ""
                report += f"| {pos.get('symbol', 'N/A')} | {pos.get('name', 'N/A')} | {pos.get('volume', 0)} | ¥{pos.get('cost', 0):.2f} | ¥{pos.get('price', 0):.2f} | {pnl_sign}¥{pnl:.2f} |\n"
        else:
            report += "*当前无持仓*\n"
        
        report += f"\n---\n\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report


def generate_backtest_report(
    result: Dict[str, Any],
    output_path: Optional[str] = None,
    format: str = "markdown"
) -> str:
    """生成回测报告的便捷函数"""
    generator = ReportGenerator()
    return generator.generate_backtest_report(result, output_path, format)



