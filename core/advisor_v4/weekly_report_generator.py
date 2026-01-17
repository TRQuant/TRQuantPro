#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Report Generator (phase7)
=================================

生成“提前一周布局系统”的周度HTML报告（多Tab格式）。

Tab结构：
1. 首页：本周投资标的和布局计划总览
2. 市场展望：市场趋势和仓位建议
3. 投资标的：每只股票一个Tab，详细分析
4. 交易策略：入场/出场/仓位/风控规则
5. 风险提示：风险控制和注意事项

注意：
- 深色主题，交互式Tab切换
- 报告内容基于 WeeklyLayoutPlan 数据结构
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

from .weekly_layout_planner import WeeklyLayoutPlan, LayoutTarget, EntryPlan, ExitPlan
from core.utils.output_manager import get_output_manager, OutputCategory

logger = logging.getLogger(__name__)


class WeeklyReportGenerator:
    """周度HTML报告生成器"""

    def __init__(self, output_dir: Optional[str] = None, verbose: bool = True):
        """
        Args:
            output_dir: 输出目录（默认: 使用OutputManager统一管理）
            verbose: 是否输出日志
        """
        self.verbose = verbose
        
        # 使用OutputManager统一管理输出路径
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            output_manager = get_output_manager()
            self.output_dir = output_manager.get_path(
                category=OutputCategory.ADVISOR_V4,
                output_type="reports",
                create_dirs=True
            )
        
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, plan: WeeklyLayoutPlan, output_filename: Optional[str] = None) -> str:
        """
        生成周度HTML报告

        Args:
            plan: WeeklyLayoutPlan 数据
            output_filename: 输出文件名（默认: weekly_layout_{week_start}.html）

        Returns:
            HTML文件路径
        """
        if output_filename is None:
            output_filename = f"weekly_layout_{plan.week_start}.html"

        filepath = self.output_dir / output_filename
        html_content = self._build_html(plan)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        if self.verbose:
            logger.info(f"✅ 周度报告已生成: {filepath}")

        return str(filepath)

    def _build_html(self, plan: WeeklyLayoutPlan) -> str:
        """构建完整HTML内容"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>韬睿量化 - 周度布局计划 {plan.week_start} ~ {plan.week_end}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        {self._build_header(plan)}
        {self._build_tabs(plan)}
        {self._build_tab_content(plan)}
        {self._build_footer(plan)}
    </div>
    <script>
        {self._get_js()}
    </script>
</body>
</html>
"""

    def _get_css(self) -> str:
        """获取CSS样式（深色主题 + Tab切换）"""
        return """
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --border: #475569;
            --accent: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid var(--border);
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: var(--accent);
        }

        .header .meta {
            color: var(--text-secondary);
            font-size: 0.95em;
        }

        .tabs {
            display: flex;
            gap: 5px;
            border-bottom: 2px solid var(--border);
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .tab {
            padding: 12px 24px;
            background: var(--bg-secondary);
            border: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            cursor: pointer;
            color: var(--text-secondary);
            font-size: 0.95em;
            font-weight: 500;
            transition: all 0.3s;
        }

        .tab:hover {
            background: var(--bg-card);
            color: var(--text-primary);
        }

        .tab.active {
            background: var(--bg-card);
            color: var(--accent);
            border-bottom: 2px solid var(--accent);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }

        .card h2 {
            color: var(--accent);
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .card h3 {
            color: var(--text-primary);
            margin: 20px 0 10px 0;
            font-size: 1.2em;
        }

        .targets-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .target-card {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 20px;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .target-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }

        .target-card .code {
            font-size: 1.3em;
            font-weight: bold;
            color: var(--accent);
            margin-bottom: 5px;
        }

        .target-card .name {
            color: var(--text-secondary);
            margin-bottom: 15px;
        }

        .target-card .score {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .score-high {
            background: var(--success);
            color: white;
        }

        .score-medium {
            background: var(--warning);
            color: white;
        }

        .score-low {
            background: var(--border);
            color: var(--text-primary);
        }

        .entry-plan {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid var(--accent);
        }

        .entry-plan h4 {
            color: var(--accent);
            margin-bottom: 10px;
        }

        .entry-stage {
            margin: 10px 0;
            padding: 10px;
            background: var(--bg-secondary);
            border-radius: 6px;
        }

        .exit-plan {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid var(--warning);
        }

        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        .table th {
            background: var(--bg-card);
            color: var(--accent);
            font-weight: 600;
        }

        .table tr:hover {
            background: var(--bg-card);
        }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
        }

        .badge-success {
            background: var(--success);
            color: white;
        }

        .badge-warning {
            background: var(--warning);
            color: white;
        }

        .badge-danger {
            background: var(--danger);
            color: white;
        }

        .footer {
            text-align: center;
            padding: 30px 0;
            margin-top: 50px;
            border-top: 2px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .risk-controls {
            list-style: none;
            padding: 0;
        }

        .risk-controls li {
            padding: 10px;
            margin: 8px 0;
            background: var(--bg-card);
            border-radius: 6px;
            border-left: 4px solid var(--warning);
        }

        .highlight {
            color: var(--accent);
            font-weight: 600;
        }
        """

    def _get_js(self) -> str:
        """获取JavaScript（Tab切换逻辑）"""
        return """
        function switchTab(tabName) {
            // 隐藏所有tab内容
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // 移除所有tab按钮的active状态
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // 显示选中的tab内容
            document.getElementById(`tab-${tabName}`).classList.add('active');
            
            // 激活选中的tab按钮
            event.target.classList.add('active');
        }

        // 默认显示首页
        document.addEventListener('DOMContentLoaded', function() {
            if (document.querySelectorAll('.tab').length > 0) {
                document.querySelectorAll('.tab')[0].click();
            }
        });
        """

    def _build_header(self, plan: WeeklyLayoutPlan) -> str:
        """构建报告头部"""
        return f"""
        <div class="header">
            <h1>📊 韬睿量化 - 周度布局计划</h1>
            <div class="meta">
                <strong>周期范围</strong>: {plan.week_start} ~ {plan.week_end} |
                <strong>生成时间</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """

    def _build_tabs(self, plan: WeeklyLayoutPlan) -> str:
        """构建Tab导航"""
        tabs = ['overview', 'market', 'strategy', 'risk']
        tab_names = ['首页总览', '市场展望', '交易策略', '风险提示']
        
        # 为每只股票添加Tab
        for target in plan.targets:
            tabs.append(f"target_{target.code}")
            tab_names.append(f"{target.code} {target.name or ''}")

        tab_buttons = []
        for i, (tab_id, tab_name) in enumerate(zip(tabs, tab_names)):
            active = "active" if i == 0 else ""
            tab_buttons.append(
                f'<button class="tab {active}" onclick="switchTab(\'{tab_id}\')">{tab_name}</button>'
            )

        return f'<div class="tabs">{"".join(tab_buttons)}</div>'

    def _build_tab_content(self, plan: WeeklyLayoutPlan) -> str:
        """构建Tab内容"""
        contents = []

        # 首页总览
        contents.append(self._build_overview_tab(plan))

        # 市场展望
        contents.append(self._build_market_tab(plan))

        # 交易策略
        contents.append(self._build_strategy_tab(plan))

        # 风险提示
        contents.append(self._build_risk_tab(plan))

        # 每只股票的详细Tab
        for target in plan.targets:
            contents.append(self._build_target_tab(plan, target))

        return "\n".join(contents)

    def _build_overview_tab(self, plan: WeeklyLayoutPlan) -> str:
        """构建首页总览Tab"""
        targets_html = []
        for target in plan.targets:
            score_class = "score-high" if target.score >= 70 else ("score-medium" if target.score >= 50 else "score-low")
            entry = plan.entry_plan.get(target.code, EntryPlan())
            exit_plan = plan.exit_plan.get(target.code, ExitPlan())

            targets_html.append(f"""
            <div class="target-card">
                <div class="code">{target.code}</div>
                <div class="name">{target.name or 'N/A'}</div>
                <div class="score {score_class}">综合得分: {target.score:.1f}</div>
                <div style="margin-top: 10px;">
                    <strong>目标仓位</strong>: {target.weight:.1%}<br>
                    <strong>推荐理由</strong>: {target.reason or 'N/A'}<br>
                    <strong>止盈</strong>: {exit_plan.take_profit:+.0%} |
                    <strong>止损</strong>: {exit_plan.stop_loss:+.0%}
                </div>
            </div>
            """)

        return f"""
        <div id="tab-overview" class="tab-content active">
            <div class="card">
                <h2>📋 本周投资标的总览</h2>
                <div class="targets-grid">
                    {"".join(targets_html)}
                </div>
            </div>

            <div class="card">
                <h2>💼 仓位建议</h2>
                <p style="font-size: 1.1em; margin: 20px 0;">
                    建议总仓位: <span class="highlight">{plan.position_advice:.1%}</span>
                </p>
                <p style="color: var(--text-secondary);">
                    基于当前市场环境（{plan.market_outlook}），建议采用{'积极' if plan.position_advice > 0.7 else '稳健' if plan.position_advice > 0.5 else '保守'}的仓位策略。
                </p>
            </div>

            <div class="card">
                <h2>📅 本周布局时间表</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>时间窗口</th>
                            <th>操作建议</th>
                            <th>注意事项</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>周一~周二</strong></td>
                            <td>分批试仓，观察市场反应</td>
                            <td>避免追高，关注开盘和分时量能</td>
                        </tr>
                        <tr>
                            <td><strong>周三~周四</strong></td>
                            <td>根据回踩/突破情况加仓或调整</td>
                            <td>回踩不破支撑可加仓，跌破关键位减仓</td>
                        </tr>
                        <tr>
                            <td><strong>周五收盘后</strong></td>
                            <td>复盘总结，评估下周持仓计划</td>
                            <td>记录关键事件和价格行为，用于迭代优化</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """

    def _build_market_tab(self, plan: WeeklyLayoutPlan) -> str:
        """构建市场展望Tab"""
        outlook_desc = {
            "bullish": "积极乐观 - 市场处于上升趋势，适合积极布局",
            "neutral": "中性观望 - 市场震荡，保持稳健仓位",
            "bearish": "谨慎保守 - 市场疲弱，建议降低仓位",
        }.get(plan.market_outlook.lower(), "中性观望")

        return f"""
        <div id="tab-market" class="tab-content">
            <div class="card">
                <h2>📈 市场展望</h2>
                <h3>当前市场环境</h3>
                <p style="font-size: 1.1em; margin: 15px 0;">
                    <span class="highlight">{plan.market_outlook.upper()}</span> - {outlook_desc}
                </p>

                <h3>仓位建议</h3>
                <p style="margin: 15px 0;">
                    建议总仓位: <span class="highlight">{plan.position_advice:.1%}</span>
                </p>
                <p style="color: var(--text-secondary);">
                    根据当前市场环境和风险控制要求，建议将{'{plan.position_advice:.1%}'}的资金配置到本布局计划中。
                </p>
            </div>

            <div class="card">
                <h2>🔍 市场观察要点</h2>
                <ul style="list-style-position: inside; padding: 0; margin: 15px 0;">
                    <li>关注大盘指数（沪深300/中证1000）的走势和成交量</li>
                    <li>观察行业轮动和主线板块的资金流向</li>
                    <li>监控政策面和消息面的变化对市场情绪的影响</li>
                    <li>跟踪个股异动和流动性变化</li>
                </ul>
            </div>
        </div>
        """

    def _build_strategy_tab(self, plan: WeeklyLayoutPlan) -> str:
        """构建交易策略Tab"""
        strategy_html = []

        for target in plan.targets:
            entry = plan.entry_plan.get(target.code, EntryPlan())
            exit_plan = plan.exit_plan.get(target.code, ExitPlan())

            stages_html = []
            if entry.stages:
                for stage in entry.stages:
                    stages_html.append(f"""
                    <div class="entry-stage">
                        <strong>{stage.get('stage', 'N/A')}</strong><br>
                        仓位: {stage.get('weight', 0):.1%} |
                        价格区间: {stage.get('price_low', 0):.2f} ~ {stage.get('price_high', 0):.2f}<br>
                        触发条件: {stage.get('trigger', 'N/A')}<br>
                        时间窗口: {stage.get('time_window', 'N/A')}
                    </div>
                    """)

            strategy_html.append(f"""
            <div class="card">
                <h3>{target.code} {target.name or ''}</h3>

                <div class="entry-plan">
                    <h4>📥 入场计划</h4>
                    {"".join(stages_html) if stages_html else "<p>暂无详细入场计划</p>"}
                    {f'<p style="margin-top: 10px; color: var(--text-secondary);"><em>{entry.notes}</em></p>' if entry.notes else ''}
                </div>

                <div class="exit-plan">
                    <h4>📤 出场计划</h4>
                    <p>
                        <strong>目标止盈</strong>: {exit_plan.take_profit:+.0%}<br>
                        <strong>固定止损</strong>: {exit_plan.stop_loss:+.0%}<br>
                        <strong>移动止盈回撤</strong>: {exit_plan.trailing_stop:.0%}<br>
                        <strong>时间止损</strong>: 持有超过 {exit_plan.time_stop_days} 天无表现则考虑退出
                    </p>
                    {f'<p style="margin-top: 10px; color: var(--text-secondary);"><em>{exit_plan.notes}</em></p>' if exit_plan.notes else ''}
                </div>
            </div>
            """)

        return f"""
        <div id="tab-strategy" class="tab-content">
            <div class="card">
                <h2>📋 交易策略总览</h2>
                <p style="margin-bottom: 20px;">
                    本布局计划采用<strong>分批建仓</strong>策略，根据市场情况和个股表现动态调整仓位。
                </p>
            </div>
            {"".join(strategy_html)}
        </div>
        """

    def _build_risk_tab(self, plan: WeeklyLayoutPlan) -> str:
        """构建风险提示Tab"""
        risk_items = []
        for risk in plan.risk_controls:
            risk_items.append(f'<li>{risk}</li>')

        return f"""
        <div id="tab-risk" class="tab-content">
            <div class="card">
                <h2>⚠️ 风险提示</h2>
                <ul class="risk-controls">
                    {"".join(risk_items) if risk_items else "<li>暂无特殊风险提示</li>"}
                </ul>
            </div>

            <div class="card">
                <h2>🛡️ 风险控制措施</h2>
                <ul style="list-style-position: inside; padding: 0; margin: 15px 0;">
                    <li>单票仓位限制：单只股票最大仓位不超过 20%</li>
                    <li>止损机制：严格执行止损规则，保护本金</li>
                    <li>仓位管理：根据市场环境动态调整总仓位</li>
                    <li>流动性要求：优先选择流动性良好的标的</li>
                    <li>分散投资：避免过度集中在单一行业或概念</li>
                </ul>
            </div>

            <div class="card">
                <h2>📝 免责声明</h2>
                <p style="color: var(--text-secondary); line-height: 1.8;">
                    本报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
                    本报告基于历史数据和量化模型生成，过往表现不代表未来收益。
                    投资者应根据自身风险承受能力，审慎决策，并自行承担投资风险。
                </p>
            </div>
        </div>
        """

    def _build_target_tab(self, plan: WeeklyLayoutPlan, target: LayoutTarget) -> str:
        """构建单个标的的详细Tab"""
        entry = plan.entry_plan.get(target.code, EntryPlan())
        exit_plan = plan.exit_plan.get(target.code, ExitPlan())

        stages_html = []
        if entry.stages:
            for stage in entry.stages:
                stages_html.append(f"""
                <tr>
                    <td>{stage.get('stage', 'N/A')}</td>
                    <td>{stage.get('weight', 0):.1%}</td>
                    <td>{stage.get('price_low', 0):.2f} ~ {stage.get('price_high', 0):.2f}</td>
                    <td>{stage.get('trigger', 'N/A')}</td>
                    <td>{stage.get('time_window', 'N/A')}</td>
                </tr>
                """)

        return f"""
        <div id="tab-target_{target.code}" class="tab-content">
            <div class="card">
                <h2>{target.code} {target.name or 'N/A'}</h2>
                <p style="margin-bottom: 20px;">
                    <span class="badge {'badge-success' if target.score >= 70 else 'badge-warning'}">
                        综合得分: {target.score:.1f}
                    </span>
                </p>

                <h3>📊 推荐理由</h3>
                <p style="margin: 15px 0; color: var(--text-secondary);">
                    {target.reason or '暂无推荐理由'}
                </p>

                <h3>💼 仓位配置</h3>
                <p style="margin: 15px 0;">
                    目标仓位: <span class="highlight">{target.weight:.1%}</span>
                </p>

                <h3>📥 入场计划</h3>
                {"".join(stages_html) if stages_html else "<p>暂无详细入场计划</p>"}
                {f'<p style="margin-top: 10px; color: var(--text-secondary);"><em>{entry.notes}</em></p>' if entry.notes else ''}

                <h3>📤 出场计划</h3>
                <div class="exit-plan">
                    <p>
                        <strong>目标止盈</strong>: {exit_plan.take_profit:+.0%}<br>
                        <strong>固定止损</strong>: {exit_plan.stop_loss:+.0%}<br>
                        <strong>移动止盈回撤</strong>: {exit_plan.trailing_stop:.0%}<br>
                        <strong>时间止损</strong>: {exit_plan.time_stop_days} 天
                    </p>
                    {f'<p style="margin-top: 10px; color: var(--text-secondary);"><em>{exit_plan.notes}</em></p>' if exit_plan.notes else ''}
                </div>

                <h3>🏷️ 标签</h3>
                <p style="margin: 15px 0;">
                    {', '.join(target.tags) if target.tags else '无标签'}
                </p>
            </div>
        </div>
        """

    def _build_footer(self, plan: WeeklyLayoutPlan) -> str:
        """构建页脚"""
        return f"""
        <div class="footer">
            <p>韬睿量化系统 (TRQuant) - Investment Advisor V4.0 提前一周布局系统</p>
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px; color: var(--text-secondary);">
                本报告基于量化模型和历史数据生成，仅供参考，不构成投资建议。
            </p>
        </div>
        """
