"""
主线识别报告生成器

生成专业的HTML报告，可在浏览器中查看
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .pro_engine import MainlineResult, ScoreBreakdown, SCORING_CONFIG


class MainlineReportGenerator:
    """主线识别报告生成器"""
    
    def __init__(self, output_dir: Optional[str] = None, report_type: str = "daily"):
        """
        初始化报告生成器
        
        Args:
            output_dir: 自定义输出目录
            report_type: 报告类型 - daily(每日), weekly(周度), archive(归档)
        """
        base_dir = Path.home() / ".local/share/trquant/reports/mainline"
        
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # 根据报告类型选择子目录
            self.output_dir = base_dir / report_type
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_type = report_type
    
    def generate_html_report(
        self,
        mainlines: List[MainlineResult],
        raw_data: Dict,
        config: Dict,
    ) -> str:
        """
        生成HTML报告
        
        Returns:
            报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mainline_report_{timestamp}.html"
        filepath = self.output_dir / filename
        
        html_content = self._build_html(mainlines, raw_data, config)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _build_html(
        self,
        mainlines: List[MainlineResult],
        raw_data: Dict,
        config: Dict,
    ) -> str:
        """构建HTML内容"""
        
        now = datetime.now()
        
        # 主线数据
        mainline_rows = ""
        for i, ml in enumerate(mainlines[:20], 1):
            score = ml.score
            signal_color = self._get_signal_color(ml.signal.value)
            change_color = "#10b981" if ml.change_pct > 0 else "#ef4444" if ml.change_pct < 0 else "#6b7280"
            flow_color = "#10b981" if ml.net_inflow > 0 else "#ef4444" if ml.net_inflow < 0 else "#6b7280"
            
            mainline_rows += f"""
            <tr>
                <td class="rank">{i}</td>
                <td class="name">
                    <span class="type-badge type-{ml.type}">{ml.type}</span>
                    {ml.name}
                </td>
                <td class="score">{score.total:.1f}</td>
                <td class="score-detail">
                    <div class="score-bar">
                        <div class="bar funds" style="width: {score.funds_score/25*100}%"></div>
                    </div>
                    <span>{score.funds_score:.1f}</span>
                </td>
                <td class="score-detail">
                    <div class="score-bar">
                        <div class="bar momentum" style="width: {score.momentum_score/20*100}%"></div>
                    </div>
                    <span>{score.momentum_score:.1f}</span>
                </td>
                <td class="score-detail">
                    <div class="score-bar">
                        <div class="bar heat" style="width: {score.heat_score/20*100}%"></div>
                    </div>
                    <span>{score.heat_score:.1f}</span>
                </td>
                <td class="score-detail">
                    <div class="score-bar">
                        <div class="bar policy" style="width: {score.policy_score/20*100}%"></div>
                    </div>
                    <span>{score.policy_score:.1f}</span>
                </td>
                <td class="score-detail">
                    <div class="score-bar">
                        <div class="bar leader" style="width: {score.leader_score/15*100}%"></div>
                    </div>
                    <span>{score.leader_score:.1f}</span>
                </td>
                <td style="color: {change_color}">{ml.change_pct:+.2f}%</td>
                <td style="color: {flow_color}">{ml.net_inflow:.2f}亿</td>
                <td class="signal" style="background-color: {signal_color}20; color: {signal_color}">{ml.signal.value}</td>
                <td class="leader">{', '.join(ml.leader_stocks[:2]) if ml.leader_stocks else '-'}</td>
            </tr>
            """
        
        # 原始数据表格
        sector_rows = self._build_data_rows(raw_data.get("sector_flow", []), "sector")
        concept_rows = self._build_data_rows(raw_data.get("concept_flow", []), "concept")
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>主线识别分析报告 - {now.strftime("%Y-%m-%d")}</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #475569;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1a2e 100%);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
        }}
        
        h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(90deg, var(--primary), #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .subtitle {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        .meta {{
            display: flex;
            gap: 24px;
            margin-top: 16px;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-secondary);
            font-size: 13px;
        }}
        
        .meta-item .icon {{
            font-size: 16px;
        }}
        
        .section {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .methodology {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }}
        
        .dimension-card {{
            background: var(--bg-tertiary);
            border-radius: 10px;
            padding: 16px;
            border-left: 4px solid var(--primary);
        }}
        
        .dimension-card.funds {{ border-left-color: #3b82f6; }}
        .dimension-card.momentum {{ border-left-color: #10b981; }}
        .dimension-card.heat {{ border-left-color: #f59e0b; }}
        .dimension-card.policy {{ border-left-color: #8b5cf6; }}
        .dimension-card.leader {{ border-left-color: #ec4899; }}
        
        .dimension-title {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .dimension-weight {{
            background: var(--bg-primary);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: var(--text-secondary);
        }}
        
        .dimension-factors {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.6;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        th {{
            background: var(--bg-tertiary);
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            color: var(--text-secondary);
            border-bottom: 2px solid var(--border);
            white-space: nowrap;
        }}
        
        td {{
            padding: 10px 8px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }}
        
        tr:hover {{
            background: var(--bg-tertiary);
        }}
        
        .rank {{
            font-weight: 700;
            color: var(--primary);
            width: 40px;
        }}
        
        .name {{
            font-weight: 500;
        }}
        
        .type-badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            margin-right: 6px;
        }}
        
        .type-行业 {{ background: #3b82f620; color: #3b82f6; }}
        .type-概念 {{ background: #8b5cf620; color: #8b5cf6; }}
        
        .score {{
            font-weight: 700;
            font-size: 15px;
        }}
        
        .score-detail {{
            width: 80px;
        }}
        
        .score-bar {{
            height: 6px;
            background: var(--bg-primary);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 2px;
        }}
        
        .score-bar .bar {{
            height: 100%;
            border-radius: 3px;
        }}
        
        .bar.funds {{ background: #3b82f6; }}
        .bar.momentum {{ background: #10b981; }}
        .bar.heat {{ background: #f59e0b; }}
        .bar.policy {{ background: #8b5cf6; }}
        .bar.leader {{ background: #ec4899; }}
        
        .score-detail span {{
            font-size: 11px;
            color: var(--text-muted);
        }}
        
        .signal {{
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 4px;
            text-align: center;
        }}
        
        .leader {{
            font-size: 12px;
            color: var(--text-secondary);
        }}
        
        .tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }}
        
        .tab {{
            padding: 8px 16px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: 6px;
            font-size: 13px;
            transition: all 0.2s;
        }}
        
        .tab:hover {{
            background: var(--bg-tertiary);
        }}
        
        .tab.active {{
            background: var(--primary);
            color: white;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .signal-rules {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-top: 16px;
        }}
        
        .signal-rule {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg-tertiary);
            border-radius: 8px;
        }}
        
        .signal-badge {{
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 12px;
        }}
        
        .signal-badge.buy {{ background: #10b98120; color: #10b981; }}
        .signal-badge.hold {{ background: #3b82f620; color: #3b82f6; }}
        .signal-badge.watch {{ background: #f59e0b20; color: #f59e0b; }}
        .signal-badge.sell {{ background: #ef444420; color: #ef4444; }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 12px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            header {{ padding: 20px; }}
            h1 {{ font-size: 22px; }}
            .section {{ padding: 16px; }}
            table {{ font-size: 11px; }}
            th, td {{ padding: 6px 4px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 A股主线识别分析报告</h1>
            <p class="subtitle">基于《A股主线识别量化流程建议书》的专业级分析</p>
            <div class="meta">
                <div class="meta-item">
                    <span class="icon">📅</span>
                    <span>报告日期: {now.strftime("%Y年%m月%d日")}</span>
                </div>
                <div class="meta-item">
                    <span class="icon">⏰</span>
                    <span>生成时间: {now.strftime("%H:%M:%S")}</span>
                </div>
                <div class="meta-item">
                    <span class="icon">📈</span>
                    <span>识别主线: {len(mainlines)} 条</span>
                </div>
                <div class="meta-item">
                    <span class="icon">🎯</span>
                    <span>强主线(≥75分): {sum(1 for m in mainlines if m.score.total >= 75)} 条</span>
                </div>
            </div>
        </header>
        
        <!-- 方法论说明 -->
        <div class="section">
            <h2 class="section-title">📐 评分方法论</h2>
            <div class="methodology">
                <div class="dimension-card funds">
                    <div class="dimension-title">
                        <span>💰 资金维度</span>
                        <span class="dimension-weight">25分</span>
                    </div>
                    <div class="dimension-factors">
                        • 当日净流入排名<br>
                        • 5日累计净流入排名<br>
                        • 流入占比强度
                    </div>
                </div>
                <div class="dimension-card momentum">
                    <div class="dimension-title">
                        <span>📈 动量维度</span>
                        <span class="dimension-weight">20分</span>
                    </div>
                    <div class="dimension-factors">
                        • 涨跌幅排名<br>
                        • 相对强度(vs沪深300)<br>
                        • 趋势得分
                    </div>
                </div>
                <div class="dimension-card heat">
                    <div class="dimension-title">
                        <span>🔥 热度维度</span>
                        <span class="dimension-weight">20分</span>
                    </div>
                    <div class="dimension-factors">
                        • 涨停股占比<br>
                        • 成交量放大<br>
                        • 关注度得分
                    </div>
                </div>
                <div class="dimension-card policy">
                    <div class="dimension-title">
                        <span>📜 政策维度</span>
                        <span class="dimension-weight">20分</span>
                    </div>
                    <div class="dimension-factors">
                        • 政策支持力度<br>
                        • 产业趋势<br>
                        • 事件催化
                    </div>
                </div>
                <div class="dimension-card leader">
                    <div class="dimension-title">
                        <span>👑 龙头维度</span>
                        <span class="dimension-weight">15分</span>
                    </div>
                    <div class="dimension-factors">
                        • 龙头强度<br>
                        • 跟风效应<br>
                        • 大市值龙头
                    </div>
                </div>
            </div>
            
            <div class="signal-rules">
                <div class="signal-rule">
                    <span class="signal-badge buy">买入</span>
                    <span>得分 ≥ 75：强主线，可重点配置</span>
                </div>
                <div class="signal-rule">
                    <span class="signal-badge hold">持有</span>
                    <span>得分 60-75：较强主线，适当参与</span>
                </div>
                <div class="signal-rule">
                    <span class="signal-badge watch">观察</span>
                    <span>得分 45-60：一般主线，观察为主</span>
                </div>
                <div class="signal-rule">
                    <span class="signal-badge sell">卖出</span>
                    <span>得分 &lt; 45：弱主线，暂不参与</span>
                </div>
            </div>
        </div>
        
        <!-- 主线排名 -->
        <div class="section">
            <h2 class="section-title">🎯 主线识别结果</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>主线名称</th>
                            <th>总分</th>
                            <th>资金(25)</th>
                            <th>动量(20)</th>
                            <th>热度(20)</th>
                            <th>政策(20)</th>
                            <th>龙头(15)</th>
                            <th>涨跌幅</th>
                            <th>净流入</th>
                            <th>信号</th>
                            <th>龙头股</th>
                        </tr>
                    </thead>
                    <tbody>
                        {mainline_rows}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 原始数据 -->
        <div class="section">
            <h2 class="section-title">📋 原始数据</h2>
            <div class="tabs">
                <button class="tab active" onclick="showTab('sector')">行业板块</button>
                <button class="tab" onclick="showTab('concept')">概念板块</button>
            </div>
            <div id="sector" class="tab-content active">
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>行业名称</th>
                                <th>涨跌幅</th>
                                <th>净流入(亿)</th>
                                <th>流入资金</th>
                                <th>流出资金</th>
                                <th>领涨股</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sector_rows}
                        </tbody>
                    </table>
                </div>
            </div>
            <div id="concept" class="tab-content">
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>概念名称</th>
                                <th>涨跌幅</th>
                                <th>净流入(亿)</th>
                                <th>流入资金</th>
                                <th>流出资金</th>
                                <th>领涨股</th>
                            </tr>
                        </thead>
                        <tbody>
                            {concept_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <footer>
            <p>报告由韬睿量化平台自动生成 | 数据来源: AKShare (同花顺/东方财富)</p>
            <p>仅供参考，不构成投资建议</p>
        </footer>
    </div>
    
    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`[onclick="showTab('${{tabId}}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }}
    </script>
</body>
</html>
        """
        
        return html
    
    def _build_data_rows(self, data: List[Dict], data_type: str) -> str:
        """构建数据行"""
        rows = ""
        
        if not data:
            return "<tr><td colspan='7' style='text-align:center;color:var(--text-muted)'>暂无数据</td></tr>"
        
        for i, item in enumerate(data[:30], 1):
            if data_type == "sector":
                name = item.get("sector_name", "") or item.get("行业", "")
            else:
                name = item.get("board_name", "") or item.get("行业", "") or item.get("概念", "")
            
            change = float(item.get("change_pct", 0) or item.get("行业-涨跌幅", 0) or 0)
            net_inflow = float(item.get("main_net_inflow", 0) or item.get("net_inflow", 0) or item.get("净额", 0) or 0)
            inflow = float(item.get("inflow", 0) or item.get("流入资金", 0) or 0)
            outflow = float(item.get("outflow", 0) or item.get("流出资金", 0) or 0)
            leader = item.get("leader_stock", "") or item.get("领涨股", "")
            
            change_color = "#10b981" if change > 0 else "#ef4444" if change < 0 else "#6b7280"
            flow_color = "#10b981" if net_inflow > 0 else "#ef4444" if net_inflow < 0 else "#6b7280"
            
            rows += f"""
            <tr>
                <td>{i}</td>
                <td>{name}</td>
                <td style="color:{change_color}">{change:+.2f}%</td>
                <td style="color:{flow_color}">{net_inflow:.2f}</td>
                <td>{inflow:.2f}</td>
                <td>{outflow:.2f}</td>
                <td>{leader}</td>
            </tr>
            """
        
        return rows
    
    def _get_signal_color(self, signal: str) -> str:
        """获取信号颜色"""
        colors = {
            "买入": "#10b981",
            "持有": "#3b82f6",
            "观察": "#f59e0b",
            "卖出": "#ef4444",
            "减仓": "#f59e0b",
        }
        return colors.get(signal, "#6b7280")


# 导出
__all__ = ["MainlineReportGenerator"]

