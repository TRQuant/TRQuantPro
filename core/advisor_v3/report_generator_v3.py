"""
V3.0 HTML报告生成模块
=====================

生成完整的投资推荐报告，包含:
1. 市场趋势分析
2. 主线五维评分
3. 推荐股票列表
4. 交易策略建议
5. 风险提示
6. 历史表现追踪
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class ReportGeneratorV3:
    """
    V3.0 HTML报告生成器
    
    生成专业的投资推荐HTML报告
    """
    
    def __init__(self, output_dir: str = None):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir or "/home/taotao/.cursor/worktrees/TRQuant/ope/results"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self, data: Dict) -> str:
        """
        生成HTML报告
        
        Args:
            data: 报告数据，包含:
                - date: 日期
                - market_trend: 市场趋势分析
                - mainlines: 主线识别结果
                - recommendations: 推荐股票列表
                - trading_strategy: 交易策略
                - risk_warning: 风险提示
                
        Returns:
            HTML文件路径
        """
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        html_content = self._build_html(data)
        
        filepath = os.path.join(self.output_dir, f"weekly_report_{date}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"报告已生成: {filepath}")
        return filepath
    
    def _build_html(self, data: Dict) -> str:
        """构建HTML内容"""
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>韬睿量化 - 本周投资推荐报告 {date}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        {self._build_header(data)}
        
        <!-- 市场趋势 -->
        {self._build_market_trend_section(data)}
        
        <!-- 主线分析 -->
        {self._build_mainlines_section(data)}
        
        <!-- 推荐股票 -->
        {self._build_recommendations_section(data)}
        
        <!-- 交易策略 -->
        {self._build_trading_strategy_section(data)}
        
        <!-- 风险提示 -->
        {self._build_risk_warning_section(data)}
        
        <!-- 页脚 -->
        {self._build_footer(data)}
    </div>
    
    <script>
        {self._get_js()}
    </script>
</body>
</html>
"""
    
    def _get_css(self) -> str:
        """获取CSS样式"""
        return """
        :root {
            --primary: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .header .date {
            color: var(--text-muted);
            font-size: 1.1rem;
        }
        
        .section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
        }
        
        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title .icon {
            font-size: 1.5rem;
        }
        
        /* 市场趋势卡片 */
        .trend-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        
        .trend-card {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        
        .trend-card .label {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 8px;
        }
        
        .trend-card .value {
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        .trend-card .value.positive { color: var(--success); }
        .trend-card .value.negative { color: var(--danger); }
        .trend-card .value.neutral { color: var(--warning); }
        
        /* 主线表格 */
        .mainline-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .mainline-table th,
        .mainline-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        .mainline-table th {
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        
        .mainline-table tr:hover {
            background: rgba(255,255,255,0.03);
        }
        
        .score-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .score-badge.high { background: rgba(16,185,129,0.2); color: #10b981; }
        .score-badge.medium { background: rgba(245,158,11,0.2); color: #f59e0b; }
        .score-badge.low { background: rgba(239,68,68,0.2); color: #ef4444; }
        
        /* 推荐股票卡片 */
        .stock-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }
        
        .stock-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stock-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .stock-name {
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .stock-code {
            color: var(--text-muted);
            font-size: 0.85rem;
        }
        
        .stock-score {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stock-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .metric {
            padding: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 6px;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        .metric-value {
            font-size: 0.95rem;
            font-weight: 600;
        }
        
        .stock-signal {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .signal-strong-buy { background: linear-gradient(135deg, #10b981, #059669); color: white; }
        .signal-buy { background: rgba(16,185,129,0.2); color: #10b981; }
        .signal-hold { background: rgba(245,158,11,0.2); color: #f59e0b; }
        .signal-watch { background: rgba(148,163,184,0.2); color: #94a3b8; }
        
        /* 交易策略 */
        .strategy-box {
            background: linear-gradient(145deg, rgba(37,99,235,0.1), rgba(139,92,246,0.1));
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
        }
        
        .strategy-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--primary);
        }
        
        .strategy-content {
            color: var(--text);
        }
        
        .strategy-content ul {
            list-style: none;
            padding: 0;
        }
        
        .strategy-content li {
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
        }
        
        .strategy-content li::before {
            content: "▸";
            position: absolute;
            left: 0;
            color: var(--primary);
        }
        
        /* 风险提示 */
        .risk-warning {
            background: rgba(239,68,68,0.1);
            border-left: 4px solid var(--danger);
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }
        
        .risk-warning h3 {
            color: var(--danger);
            margin-bottom: 12px;
        }
        
        /* 页脚 */
        .footer {
            text-align: center;
            padding: 30px 0;
            color: var(--text-muted);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }
        
        /* 响应式 */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }
            
            .trend-cards {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .stock-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    
    def _get_js(self) -> str:
        """获取JavaScript"""
        return """
        // 数字动画
        document.querySelectorAll('.trend-card .value').forEach(el => {
            const value = parseFloat(el.textContent);
            if (!isNaN(value)) {
                let start = 0;
                const duration = 1000;
                const startTime = performance.now();
                
                function animate(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const easeOut = 1 - Math.pow(1 - progress, 3);
                    const current = start + (value - start) * easeOut;
                    el.textContent = current.toFixed(1);
                    if (progress < 1) requestAnimationFrame(animate);
                }
                
                requestAnimationFrame(animate);
            }
        });
        """
    
    def _build_header(self, data: Dict) -> str:
        """构建头部"""
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        return f"""
        <header class="header">
            <h1>📊 韬睿量化 - 本周投资推荐</h1>
            <p class="date">报告日期: {date}</p>
        </header>
        """
    
    def _build_market_trend_section(self, data: Dict) -> str:
        """构建市场趋势部分"""
        trend = data.get("market_trend", {})
        
        score = trend.get("ensemble_score", 0)
        direction = trend.get("direction", "震荡盘整")
        position_limit = trend.get("position_limit", 0.5)
        strategy_mode = trend.get("strategy_mode", "观望")
        
        score_class = "positive" if score > 20 else "negative" if score < -20 else "neutral"
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <span class="icon">📈</span>
                市场趋势分析
            </h2>
            <div class="trend-cards">
                <div class="trend-card">
                    <div class="label">综合评分</div>
                    <div class="value {score_class}">{score:.1f}</div>
                </div>
                <div class="trend-card">
                    <div class="label">趋势方向</div>
                    <div class="value neutral">{direction}</div>
                </div>
                <div class="trend-card">
                    <div class="label">建议仓位</div>
                    <div class="value">{position_limit*100:.0f}%</div>
                </div>
                <div class="trend-card">
                    <div class="label">策略模式</div>
                    <div class="value neutral">{strategy_mode}</div>
                </div>
            </div>
        </section>
        """
    
    def _build_mainlines_section(self, data: Dict) -> str:
        """构建主线分析部分"""
        mainlines = data.get("mainlines", [])[:10]  # Top 10
        
        if not mainlines:
            return """
            <section class="section">
                <h2 class="section-title">
                    <span class="icon">🎯</span>
                    市场主线分析
                </h2>
                <p style="color: var(--text-muted);">暂无主线数据</p>
            </section>
            """
        
        rows = ""
        for i, ml in enumerate(mainlines):
            name = ml.get("name", "")
            score = ml.get("total_score", 0)
            change = ml.get("change_pct", 0)
            signal = ml.get("signal", "观察")
            
            score_class = "high" if score >= 70 else "medium" if score >= 50 else "low"
            change_class = "positive" if change > 0 else "negative"
            
            rows += f"""
            <tr>
                <td>{i+1}</td>
                <td><strong>{name}</strong></td>
                <td><span class="score-badge {score_class}">{score:.1f}</span></td>
                <td class="{change_class}">{change:+.2f}%</td>
                <td>{signal}</td>
            </tr>
            """
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <span class="icon">🎯</span>
                市场主线分析 (五维评分)
            </h2>
            <table class="mainline-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>主线名称</th>
                        <th>综合得分</th>
                        <th>涨跌幅</th>
                        <th>信号</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </section>
        """
    
    def _build_recommendations_section(self, data: Dict) -> str:
        """构建推荐股票部分"""
        stocks = data.get("recommendations", {}).get("stocks", [])[:12]
        
        if not stocks:
            return """
            <section class="section">
                <h2 class="section-title">
                    <span class="icon">💎</span>
                    本周推荐股票
                </h2>
                <p style="color: var(--text-muted);">暂无推荐股票</p>
            </section>
            """
        
        cards = ""
        for stock in stocks:
            code = stock.get("code", "")
            name = stock.get("name", "")
            score = stock.get("total_score", 0)
            signal = stock.get("signal", "观察")
            
            signal_class = {
                "强买": "signal-strong-buy",
                "买入": "signal-buy",
                "持有": "signal-hold",
            }.get(signal, "signal-watch")
            
            mom_5d = stock.get("mom_5d", 0) * 100
            mom_20d = stock.get("mom_20d", 0) * 100
            market_cap = stock.get("market_cap", 0)
            pe = stock.get("pe_ratio", 0)
            
            cards += f"""
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <div class="stock-name">{name}</div>
                        <div class="stock-code">{code}</div>
                    </div>
                    <div class="stock-score">{score:.0f}</div>
                </div>
                <div class="stock-metrics">
                    <div class="metric">
                        <div class="metric-label">5日涨幅</div>
                        <div class="metric-value" style="color: {'#10b981' if mom_5d > 0 else '#ef4444'}">{mom_5d:+.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">20日涨幅</div>
                        <div class="metric-value" style="color: {'#10b981' if mom_20d > 0 else '#ef4444'}">{mom_20d:+.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">市值(亿)</div>
                        <div class="metric-value">{market_cap:.0f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">PE</div>
                        <div class="metric-value">{pe:.1f}</div>
                    </div>
                </div>
                <span class="stock-signal {signal_class}">{signal}</span>
            </div>
            """
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <span class="icon">💎</span>
                本周推荐股票
            </h2>
            <div class="stock-grid">
                {cards}
            </div>
        </section>
        """
    
    def _build_trading_strategy_section(self, data: Dict) -> str:
        """构建交易策略部分"""
        strategy = data.get("trading_strategy", {})
        
        position_advice = strategy.get("position_advice", "根据市场趋势灵活调整")
        entry_strategy = strategy.get("entry_strategy", [
            "逢低建仓，分批买入",
            "关注回调支撑位",
            "设置止损点位",
        ])
        exit_strategy = strategy.get("exit_strategy", [
            "设定目标止盈位",
            "跟踪止盈保护利润",
            "异常放量坚决离场",
        ])
        risk_control = strategy.get("risk_control", [
            "单只股票仓位不超过10%",
            "总仓位根据市场趋势调整",
            "严格执行止损纪律",
        ])
        
        entry_items = "".join([f"<li>{item}</li>" for item in entry_strategy])
        exit_items = "".join([f"<li>{item}</li>" for item in exit_strategy])
        risk_items = "".join([f"<li>{item}</li>" for item in risk_control])
        
        return f"""
        <section class="section">
            <h2 class="section-title">
                <span class="icon">📋</span>
                交易策略建议
            </h2>
            
            <div class="strategy-box">
                <div class="strategy-title">💰 仓位建议</div>
                <div class="strategy-content">
                    <p>{position_advice}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
                <div class="strategy-box">
                    <div class="strategy-title">🎯 入场策略</div>
                    <div class="strategy-content">
                        <ul>{entry_items}</ul>
                    </div>
                </div>
                
                <div class="strategy-box">
                    <div class="strategy-title">🚪 出场策略</div>
                    <div class="strategy-content">
                        <ul>{exit_items}</ul>
                    </div>
                </div>
                
                <div class="strategy-box">
                    <div class="strategy-title">🛡️ 风控策略</div>
                    <div class="strategy-content">
                        <ul>{risk_items}</ul>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _build_risk_warning_section(self, data: Dict) -> str:
        """构建风险提示部分"""
        warnings = data.get("risk_warnings", [
            "本报告仅供参考，不构成投资建议",
            "股市有风险，投资需谨慎",
            "过往业绩不代表未来表现",
            "请根据自身风险承受能力做出投资决策",
        ])
        
        warning_items = "".join([f"<li>{w}</li>" for w in warnings])
        
        return f"""
        <section class="section">
            <div class="risk-warning">
                <h3>⚠️ 风险提示</h3>
                <ul style="list-style: disc; padding-left: 20px;">
                    {warning_items}
                </ul>
            </div>
        </section>
        """
    
    def _build_footer(self, data: Dict) -> str:
        """构建页脚"""
        return f"""
        <footer class="footer">
            <p>韬睿量化 V3.0 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Powered by TRQuant</p>
        </footer>
        """


# ============ 便捷函数 ============

def generate_report(data: Dict, output_dir: str = None) -> str:
    """
    便捷函数：生成报告
    
    Args:
        data: 报告数据
        output_dir: 输出目录
        
    Returns:
        报告文件路径
    """
    generator = ReportGeneratorV3(output_dir=output_dir)
    return generator.generate(data)
