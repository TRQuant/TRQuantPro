#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HTML报告生成器
================================================================================

功能说明：
1. 生成多Tab的专业HTML投资报告
2. 支持Prism.js代码高亮（Plasma主题）
3. 响应式布局，支持移动端
4. 包含图表、表格、代码等多种元素

Tab结构：
1. 概览 - 策略基本信息和关键指标
2. 策略架构 - 模块结构和功能说明
3. 详情描述 - 策略详细说明
4. 代码详解 - Plasma格式化的Python代码
5. 回测结果 - 收益曲线和绩效指标
6. 交易记录 - 详细交易历史
7. 风险分析 - 风控指标和回撤分析
8. 趋势分析 - 市场趋势预测
9. 投资建议 - 每周操作建议

作者: TRQuant Team
日期: 2026-01-10
================================================================================
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class HTMLReportGenerator:
    """HTML报告生成器"""
    
    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        if output_dir is None:
            output_dir = Path('output/reports')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_bull_market_report(
        self,
        report_id: str,
        overview_data: Dict,
        backtest_data: Dict = None,
        architecture_data: Dict = None,
        code_data: Dict = None,
        trades_data: List[Dict] = None,
        risk_data: Dict = None,
        trend_data: Dict = None,
        advice_data: Dict = None
    ) -> Path:
        """
        生成牛市策略报告
        
        Args:
            report_id: 报告ID
            overview_data: 概览数据
            backtest_data: 回测数据
            architecture_data: 架构数据
            code_data: 代码数据
            trades_data: 交易数据
            risk_data: 风险数据
            trend_data: 趋势数据
            advice_data: 建议数据
            
        Returns:
            Path: 报告文件路径
        """
        html = self._build_html(
            report_id=report_id,
            overview_data=overview_data,
            backtest_data=backtest_data or {},
            architecture_data=architecture_data or {},
            code_data=code_data or {},
            trades_data=trades_data or [],
            risk_data=risk_data or {},
            trend_data=trend_data or {},
            advice_data=advice_data or {}
        )
        
        output_path = self.output_dir / f"bull_market_report_{report_id}.html"
        output_path.write_text(html, encoding='utf-8')
        
        logger.info(f"报告已生成: {output_path}")
        return output_path
    
    def _build_html(
        self,
        report_id: str,
        overview_data: Dict,
        backtest_data: Dict,
        architecture_data: Dict,
        code_data: Dict,
        trades_data: List[Dict],
        risk_data: Dict,
        trend_data: Dict,
        advice_data: Dict
    ) -> str:
        """构建完整HTML"""
        
        # 生成各Tab内容
        overview_content = self._generate_overview_tab(overview_data)
        architecture_content = self._generate_architecture_tab(architecture_data)
        detail_content = self._generate_detail_tab(overview_data)
        code_content = self._generate_code_tab(code_data)
        backtest_content = self._generate_backtest_tab(backtest_data)
        trades_content = self._generate_trades_tab(trades_data)
        risk_content = self._generate_risk_tab(risk_data)
        trend_content = self._generate_trend_tab(trend_data)
        advice_content = self._generate_advice_tab(advice_data)
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>牛市极端高收益策略 - 投资报告</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-primary: #58a6ff;
            --accent-success: #3fb950;
            --accent-warning: #d29922;
            --accent-danger: #f85149;
            --border-color: #30363d;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 30px 0;
            margin-bottom: 30px;
        }}
        
        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .header-title h1 {{
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        
        .header-title .subtitle {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}
        
        .header-stats {{
            display: flex;
            gap: 30px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.8rem;
            font-weight: 700;
        }}
        
        .stat-value.positive {{
            color: var(--accent-success);
        }}
        
        .stat-value.negative {{
            color: var(--accent-danger);
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        /* Tabs */
        .tabs {{
            display: flex;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}
        
        .tab-btn {{
            padding: 12px 20px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.95rem;
            white-space: nowrap;
            transition: all 0.2s;
            border-bottom: 2px solid transparent;
        }}
        
        .tab-btn:hover {{
            color: var(--text-primary);
            background: var(--bg-secondary);
        }}
        
        .tab-btn.active {{
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Cards */
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Tables */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .data-table th {{
            background: var(--bg-tertiary);
            font-weight: 600;
            color: var(--text-secondary);
        }}
        
        .data-table tr:hover {{
            background: var(--bg-tertiary);
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .metric-card {{
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        .metric-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        /* Code Block */
        .code-block {{
            background: #1a1d21;
            border-radius: 8px;
            padding: 16px;
            overflow-x: auto;
            margin: 16px 0;
        }}
        
        .code-block pre {{
            margin: 0;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }}
        
        .code-section {{
            margin-bottom: 24px;
        }}
        
        .code-section-title {{
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--accent-primary);
        }}
        
        .code-section-desc {{
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-size: 0.9rem;
        }}
        
        /* Architecture Diagram */
        .arch-module {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        
        .arch-module-name {{
            font-weight: 600;
            color: var(--accent-primary);
            margin-bottom: 8px;
        }}
        
        .arch-module-desc {{
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-size: 0.9rem;
        }}
        
        .arch-features {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .arch-feature {{
            background: var(--bg-primary);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        /* Advice Cards */
        .advice-card {{
            background: var(--bg-tertiary);
            border-left: 4px solid var(--accent-primary);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        
        .advice-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .advice-week {{
            font-weight: 600;
            color: var(--accent-primary);
        }}
        
        .advice-period {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .advice-summary {{
            margin-bottom: 12px;
            padding: 12px;
            background: var(--bg-secondary);
            border-radius: 6px;
        }}
        
        .advice-operations {{
            list-style: none;
        }}
        
        .advice-operations li {{
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
        }}
        
        .advice-operations li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--accent-success);
        }}
        
        .advice-sectors {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }}
        
        .advice-sector {{
            background: rgba(88, 166, 255, 0.15);
            color: var(--accent-primary);
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85rem;
        }}
        
        .risk-warning {{
            background: rgba(248, 81, 73, 0.1);
            border-left: 3px solid var(--accent-danger);
            padding: 12px;
            margin-top: 12px;
            border-radius: 0 6px 6px 0;
            font-size: 0.9rem;
        }}
        
        /* Chart Container */
        .chart-container {{
            position: relative;
            height: 300px;
            margin: 20px 0;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .badge-success {{
            background: rgba(63, 185, 80, 0.15);
            color: var(--accent-success);
        }}
        
        .badge-danger {{
            background: rgba(248, 81, 73, 0.15);
            color: var(--accent-danger);
        }}
        
        .badge-warning {{
            background: rgba(210, 153, 34, 0.15);
            color: var(--accent-warning);
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                text-align: center;
            }}
            
            .header-stats {{
                flex-wrap: wrap;
                justify-content: center;
            }}
            
            .tabs {{
                padding-bottom: 8px;
            }}
            
            .tab-btn {{
                padding: 10px 14px;
                font-size: 0.85rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container header-content">
            <div class="header-title">
                <h1>🚀 牛市极端高收益策略</h1>
                <div class="subtitle">回测报告 | {overview_data.get('backtest_period', 'N/A')} | 报告ID: {report_id}</div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-value {'positive' if overview_data.get('total_return', 0) >= 0 else 'negative'}">
                        {overview_data.get('total_return', 0)*100:.2f}%
                    </div>
                    <div class="stat-label">总收益率</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value negative">{abs(overview_data.get('max_drawdown', 0))*100:.2f}%</div>
                    <div class="stat-label">最大回撤</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{overview_data.get('sharpe_ratio', 0):.2f}</div>
                    <div class="stat-label">夏普比率</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value positive">{overview_data.get('win_rate', 0)*100:.1f}%</div>
                    <div class="stat-label">胜率</div>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="tabs">
            <button class="tab-btn active" data-tab="overview">📊 概览</button>
            <button class="tab-btn" data-tab="architecture">🏛️ 策略架构</button>
            <button class="tab-btn" data-tab="detail">📝 详情描述</button>
            <button class="tab-btn" data-tab="code">💻 代码详解</button>
            <button class="tab-btn" data-tab="backtest">📈 回测结果</button>
            <button class="tab-btn" data-tab="trades">💹 交易记录</button>
            <button class="tab-btn" data-tab="risk">🛡️ 风险分析</button>
            <button class="tab-btn" data-tab="trend">🌐 趋势分析</button>
            <button class="tab-btn" data-tab="advice">💡 投资建议</button>
        </div>
        
        <div id="overview" class="tab-content active">
            {overview_content}
        </div>
        
        <div id="architecture" class="tab-content">
            {architecture_content}
        </div>
        
        <div id="detail" class="tab-content">
            {detail_content}
        </div>
        
        <div id="code" class="tab-content">
            {code_content}
        </div>
        
        <div id="backtest" class="tab-content">
            {backtest_content}
        </div>
        
        <div id="trades" class="tab-content">
            {trades_content}
        </div>
        
        <div id="risk" class="tab-content">
            {risk_content}
        </div>
        
        <div id="trend" class="tab-content">
            {trend_content}
        </div>
        
        <div id="advice" class="tab-content">
            {advice_content}
        </div>
    </div>
    
    <footer>
        <p>TRQuant 韬睿量化系统 | 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p style="margin-top: 8px;">⚠️ 本报告仅供研究参考，不构成任何投资建议</p>
    </footer>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>
        // Tab切换逻辑
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                // 移除所有active
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // 添加active
                btn.classList.add('active');
                document.getElementById(btn.dataset.tab).classList.add('active');
            }});
        }});
        
        // 初始化代码高亮
        if (typeof Prism !== 'undefined') {{
            Prism.highlightAll();
        }}
    </script>
</body>
</html>'''
        
        return html
    
    def _generate_overview_tab(self, data: Dict) -> str:
        """生成概览Tab内容"""
        return f'''
        <div class="card">
            <div class="card-title">📊 策略概况</div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">¥{data.get('initial_capital', 0):,.0f}</div>
                    <div class="metric-label">初始资金</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">¥{data.get('final_value', 0):,.0f}</div>
                    <div class="metric-label">期末资产</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{data.get('total_trades', 0)}</div>
                    <div class="metric-label">总交易次数</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{data.get('annual_return', 0)*100:.1f}%</div>
                    <div class="metric-label">年化收益率</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🎯 目标达成情况</div>
            <p style="margin-bottom: 16px;">
                目标月收益率: <strong>30%</strong> | 
                实际收益率: <strong class="{'positive' if data.get('total_return', 0) >= 0.1 else ''}">{data.get('total_return', 0)*100:.2f}%</strong> |
                达成状态: <span class="badge {'badge-success' if data.get('reached_target') else 'badge-warning'}">
                    {'✅ 已达成' if data.get('reached_target') else '⏳ 进行中'}
                </span>
            </p>
        </div>
        
        <div class="card">
            <div class="card-title">📈 策略特点</div>
            <ul style="list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
                <li>✅ <strong>市场自适应</strong>: 牛市追涨、熊市低吸</li>
                <li>✅ <strong>极端信号</strong>: 首板/连板/强势突破</li>
                <li>✅ <strong>快速轮动</strong>: 周频调仓、捕捉短期机会</li>
                <li>✅ <strong>严格风控</strong>: 止损-10%、止盈+25%</li>
            </ul>
        </div>
        '''
    
    def _generate_architecture_tab(self, data: Dict) -> str:
        """生成策略架构Tab内容"""
        modules_html = ''
        for module in data.get('modules', []):
            features_html = ''.join([
                f'<span class="arch-feature">{f}</span>' 
                for f in module.get('features', [])
            ])
            modules_html += f'''
            <div class="arch-module">
                <div class="arch-module-name">📦 {module.get('name', '')}</div>
                <div class="arch-module-desc">{module.get('description', '')}</div>
                <div class="arch-features">{features_html}</div>
            </div>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">🏛️ 策略架构图</div>
            <div style="text-align: center; padding: 20px; background: var(--bg-tertiary); border-radius: 8px; margin-bottom: 20px;">
                <pre style="font-family: monospace; color: var(--accent-primary);">
┌────────────────────────────────────────────────────────────┐
│                    牛市极端高收益策略                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  市场状态     │ → │  信号评分     │ → │  选股排序     │ │
│  │  检测模块     │    │  引擎         │    │  模块        │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         ↑                   ↑                   ↓          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  指数数据     │    │  因子计算     │    │  仓位管理     │ │
│  │  获取         │    │  器           │    │  模块        │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         ↑                                       ↓          │
│  ┌──────────────┐                       ┌──────────────┐ │
│  │  JQData      │                       │  风控模块     │ │
│  │  数据源       │                       │  止损止盈     │ │
│  └──────────────┘                       └──────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
                </pre>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📦 核心模块说明</div>
            {modules_html}
        </div>
        '''
    
    def _generate_detail_tab(self, data: Dict) -> str:
        """生成详情描述Tab内容"""
        return f'''
        <div class="card">
            <div class="card-title">📝 策略详情</div>
            
            <h3 style="margin: 20px 0 12px;">1. 策略核心思想</h3>
            <p style="color: var(--text-secondary);">
                牛市极端高收益策略基于"追涨杀跌"的核心逻辑，在市场处于牛市状态时，
                积极追踪强势股的极端信号（如首板启动、连板加速、强势突破），
                利用周频调仓快速捕捉短期爆发机会。策略目标是在牛市环境下实现30%+月收益。
            </p>
            
            <h3 style="margin: 20px 0 12px;">2. 信号类型</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>信号类型</th>
                        <th>触发条件</th>
                        <th>基础分值</th>
                        <th>风险等级</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>🔥 首板启动</td>
                        <td>当日涨停且近期无涨停</td>
                        <td>50分</td>
                        <td><span class="badge badge-danger">高</span></td>
                    </tr>
                    <tr>
                        <td>⚡ 连板加速</td>
                        <td>连续2天以上涨停</td>
                        <td>60分</td>
                        <td><span class="badge badge-danger">极高</span></td>
                    </tr>
                    <tr>
                        <td>📈 强势突破</td>
                        <td>5日动量>15%且突破60日高点</td>
                        <td>40分</td>
                        <td><span class="badge badge-warning">中高</span></td>
                    </tr>
                    <tr>
                        <td>📊 量价齐升</td>
                        <td>量比>2且涨幅>5%</td>
                        <td>35分</td>
                        <td><span class="badge badge-warning">中</span></td>
                    </tr>
                </tbody>
            </table>
            
            <h3 style="margin: 20px 0 12px;">3. 风控机制</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-danger);">-10%</div>
                    <div class="metric-label">止损线</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-success);">+25%</div>
                    <div class="metric-label">止盈线</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">2只</div>
                    <div class="metric-label">最大持仓</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">50%</div>
                    <div class="metric-label">单票仓位</div>
                </div>
            </div>
        </div>
        '''
    
    def _generate_code_tab(self, data: Dict) -> str:
        """生成代码详解Tab内容"""
        sections_html = ''
        for section in data.get('sections', []):
            code = section.get('code', '').replace('<', '&lt;').replace('>', '&gt;')
            sections_html += f'''
            <div class="code-section">
                <div class="code-section-title">📌 {section.get('name', '')}</div>
                <div class="code-section-desc">{section.get('description', '')}</div>
                <div class="code-block">
                    <pre><code class="language-python">{code}</code></pre>
                </div>
            </div>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">💻 核心代码详解（Plasma格式化）</div>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                以下是策略核心代码段，包含详细注释说明。代码使用Python语法高亮显示。
            </p>
            {sections_html}
        </div>
        '''
    
    def _generate_backtest_tab(self, data: Dict) -> str:
        """生成回测结果Tab内容"""
        metrics = data.get('metrics', {})
        
        return f'''
        <div class="card">
            <div class="card-title">📈 绩效指标</div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value {'positive' if metrics.get('total_return', 0) >= 0 else 'negative'}">{metrics.get('total_return', 0):.2f}%</div>
                    <div class="metric-label">总收益率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('annual_return', 0):.2f}%</div>
                    <div class="metric-label">年化收益率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-danger);">{abs(metrics.get('max_drawdown', 0)):.2f}%</div>
                    <div class="metric-label">最大回撤</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('sharpe_ratio', 0):.2f}</div>
                    <div class="metric-label">夏普比率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-success);">{metrics.get('win_rate', 0):.1f}%</div>
                    <div class="metric-label">胜率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('profit_loss_ratio', 1):.2f}</div>
                    <div class="metric-label">盈亏比</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 收益曲线</div>
            <div class="chart-container">
                <canvas id="returnChart"></canvas>
            </div>
        </div>
        
        <script>
            // 收益曲线图
            const returnCtx = document.getElementById('returnChart').getContext('2d');
            const returns = {json.dumps(data.get('cumulative_returns', [1]))};
            new Chart(returnCtx, {{
                type: 'line',
                data: {{
                    labels: returns.map((_, i) => '日' + (i + 1)),
                    datasets: [{{
                        label: '累计收益',
                        data: returns.map(r => (r - 1) * 100),
                        borderColor: '#58a6ff',
                        backgroundColor: 'rgba(88, 166, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: ctx => ctx.parsed.y.toFixed(2) + '%'
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: value => value + '%',
                                color: '#8b949e'
                            }},
                            grid: {{ color: '#30363d' }}
                        }},
                        x: {{
                            ticks: {{ color: '#8b949e' }},
                            grid: {{ color: '#30363d' }}
                        }}
                    }}
                }}
            }});
        </script>
        '''
    
    def _generate_trades_tab(self, data: List[Dict]) -> str:
        """生成交易记录Tab内容"""
        rows = ''
        for trade in data:
            direction = trade.get('direction', '')
            pnl = trade.get('pnl', 0)
            pnl_pct = trade.get('pnl_pct', 0)
            
            if direction == 'BUY':
                direction_badge = '<span class="badge badge-success">买入</span>'
                pnl_cell = '-'
            else:
                direction_badge = '<span class="badge badge-danger">卖出</span>'
                pnl_class = 'positive' if pnl >= 0 else 'negative'
                pnl_cell = f'<span class="{pnl_class}">¥{pnl:,.0f} ({pnl_pct:+.2f}%)</span>'
            
            rows += f'''
            <tr>
                <td>{trade.get('date', '')}</td>
                <td>{trade.get('code', '')}</td>
                <td>{trade.get('name', '')}</td>
                <td>{direction_badge}</td>
                <td>¥{trade.get('price', 0):.2f}</td>
                <td>{trade.get('shares', 0)}</td>
                <td>¥{trade.get('amount', 0):,.0f}</td>
                <td>{pnl_cell}</td>
                <td>{trade.get('signal_type', '') or trade.get('reason', '')}</td>
            </tr>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">💹 交易记录明细</div>
            <div style="overflow-x: auto;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>代码</th>
                            <th>名称</th>
                            <th>方向</th>
                            <th>价格</th>
                            <th>数量</th>
                            <th>金额</th>
                            <th>盈亏</th>
                            <th>备注</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''
    
    def _generate_risk_tab(self, data: Dict) -> str:
        """生成风险分析Tab内容"""
        drawdowns = data.get('drawdown_history', [])
        drawdown_rows = ''
        for dd in drawdowns:
            drawdown_rows += f'''
            <tr>
                <td>{dd.get('start_date', '')}</td>
                <td>{dd.get('end_date', '')}</td>
                <td style="color: var(--accent-danger);">{dd.get('drawdown', 0):.2f}%</td>
                <td>{dd.get('recovery_days', 0)}天</td>
            </tr>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">🛡️ 风险指标</div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-danger);">{abs(data.get('max_drawdown', 0)):.2f}%</div>
                    <div class="metric-label">最大回撤</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{data.get('volatility', 0):.2f}%</div>
                    <div class="metric-label">年化波动率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{data.get('sharpe_ratio', 0):.2f}</div>
                    <div class="metric-label">夏普比率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: var(--accent-danger);">{data.get('var_95', 0):.2f}%</div>
                    <div class="metric-label">VaR (95%)</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📉 回撤历史</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>开始日期</th>
                        <th>结束日期</th>
                        <th>回撤幅度</th>
                        <th>恢复时间</th>
                    </tr>
                </thead>
                <tbody>
                    {drawdown_rows}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">⚠️ 风险提示</div>
            <div class="risk-warning">
                <strong>策略风险等级：高</strong><br>
                本策略采用激进的追涨策略，在牛市环境下可能获得高收益，但在市场震荡或下跌时可能遭受较大损失。
                请投资者根据自身风险承受能力谨慎参与。
            </div>
        </div>
        '''
    
    def _generate_trend_tab(self, data: Dict) -> str:
        """生成趋势分析Tab内容"""
        summary = data.get('summary', {})
        trend_analysis = data.get('trend_analysis', {})
        csi300 = trend_analysis.get('csi300', {})
        
        return f'''
        <div class="card">
            <div class="card-title">🌐 市场趋势分析</div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{summary.get('market_outlook', '中性')}</div>
                    <div class="metric-label">市场展望</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.get('ma_status', '震荡')}</div>
                    <div class="metric-label">均线状态</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.get('volume_status', '平稳')}</div>
                    <div class="metric-label">量能状态</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.get('technical_status', '中性')}</div>
                    <div class="metric-label">技术状态</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 沪深300技术指标</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>指标</th>
                        <th>数值</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>收盘价</td>
                        <td>{csi300.get('close', 0):.2f}</td>
                        <td>最新收盘价</td>
                    </tr>
                    <tr>
                        <td>MA5</td>
                        <td>{csi300.get('ma5', 0):.2f}</td>
                        <td>5日均线</td>
                    </tr>
                    <tr>
                        <td>MA20</td>
                        <td>{csi300.get('ma20', 0):.2f}</td>
                        <td>20日均线</td>
                    </tr>
                    <tr>
                        <td>MA60</td>
                        <td>{csi300.get('ma60', 0):.2f}</td>
                        <td>60日均线</td>
                    </tr>
                    <tr>
                        <td>5日动量</td>
                        <td class="{'positive' if csi300.get('mom_5d', 0) >= 0 else 'negative'}">{csi300.get('mom_5d', 0):.2f}%</td>
                        <td>5日涨跌幅</td>
                    </tr>
                    <tr>
                        <td>20日动量</td>
                        <td class="{'positive' if csi300.get('mom_20d', 0) >= 0 else 'negative'}">{csi300.get('mom_20d', 0):.2f}%</td>
                        <td>20日涨跌幅</td>
                    </tr>
                    <tr>
                        <td>RSI</td>
                        <td>{csi300.get('rsi', 50):.1f}</td>
                        <td>相对强弱指数</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📝 综合分析</div>
            <p style="color: var(--text-secondary);">
                {summary.get('recommendation', '暂无分析结论')}
            </p>
        </div>
        '''
    
    def _generate_advice_tab(self, data: Dict) -> str:
        """生成投资建议Tab内容"""
        weekly_advice = data.get('weekly_advice', [])
        
        advice_html = ''
        for advice in weekly_advice:
            operations_html = ''.join([f'<li>{op}</li>' for op in advice.get('operations', [])])
            sectors_html = ''.join([f'<span class="advice-sector">{s}</span>' for s in advice.get('key_sectors', [])])
            
            advice_html += f'''
            <div class="advice-card">
                <div class="advice-header">
                    <span class="advice-week">📅 第{advice.get('week_number', 1)}周</span>
                    <span class="advice-period">{advice.get('period', '')}</span>
                </div>
                <div class="advice-summary">
                    <strong>市场判断：</strong>{advice.get('summary', '')}
                </div>
                <div style="display: flex; gap: 20px; margin-bottom: 12px;">
                    <div>
                        <span style="color: var(--text-secondary);">风险等级：</span>
                        <strong>{advice.get('risk_level', '平衡型')}</strong>
                    </div>
                    <div>
                        <span style="color: var(--text-secondary);">建议仓位：</span>
                        <strong>{advice.get('position_suggestion', '50%')}</strong>
                    </div>
                </div>
                <div style="margin-bottom: 12px;">
                    <strong>操作建议：</strong>
                    <ul class="advice-operations">{operations_html}</ul>
                </div>
                <div>
                    <strong>重点板块：</strong>
                    <div class="advice-sectors">{sectors_html}</div>
                </div>
                <div class="risk-warning">
                    <strong>⚠️ 风险提示：</strong>{advice.get('risk_warning', '市场有风险，投资需谨慎')}
                </div>
            </div>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">💡 未来一个月投资建议</div>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                以下是基于当前市场趋势分析生成的每周投资建议，仅供参考。
            </p>
            {advice_html}
        </div>
        '''
