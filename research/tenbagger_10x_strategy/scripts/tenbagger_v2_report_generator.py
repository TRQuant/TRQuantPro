#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 综合报告生成器
=====================================

HTML报告结构 (多Tab):
Tab 1: 首页 - 本周投资标的 ★
├── 当日行情概览
├── 市场趋势判断
├── TOP5投资标的
├── 具体交易策略
└── 风险提示

Tab 2: 系统概览
├── 因子体系说明
├── 筛选逻辑
└── 阶段识别

Tab 3: 回测报告
├── 收益曲线
├── 关键指标
├── 历史交易
└── 月度收益

Tab 4: 个股分析
├── 每只推荐股详细分析
├── 财务数据
├── 技术图表
└── 投资建议

Tab 5: 交易策略
├── 入场规则
├── 仓位管理
├── 止盈止损
└── 调仓计划

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_report_generator.py
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json
import logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TenbaggerV2ReportGenerator:
    """十倍股V2报告生成器"""
    
    # HTML模板
    HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股早期识别系统 V2.0 - 投资报告</title>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #1f2937;
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-blue: #3b82f6;
            --accent-yellow: #f59e0b;
            --accent-purple: #8b5cf6;
            --border-color: #374151;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card));
            padding: 24px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header-meta {
            display: flex;
            gap: 24px;
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .tabs {
            display: flex;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            overflow-x: auto;
        }
        
        .tab-btn {
            padding: 14px 24px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
            white-space: nowrap;
        }
        
        .tab-btn:hover {
            background: var(--bg-card);
            color: var(--text-primary);
        }
        
        .tab-btn.active {
            background: var(--bg-card);
            color: var(--accent-green);
            border-bottom: 2px solid var(--accent-green);
        }
        
        .tab-content {
            display: none;
            padding: 24px;
            animation: fadeIn 0.3s ease;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        
        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
        }
        
        .stat-card {
            background: var(--bg-secondary);
            padding: 16px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .positive { color: var(--accent-green); }
        .negative { color: var(--accent-red); }
        .neutral { color: var(--accent-yellow); }
        
        .stock-card {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 16px;
            border-left: 4px solid var(--accent-green);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .stock-name {
            font-size: 18px;
            font-weight: 600;
        }
        
        .stock-code {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .stock-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .badge-s0 { background: var(--accent-purple); color: white; }
        .badge-s1 { background: var(--accent-green); color: white; }
        .badge-s2 { background: var(--accent-blue); color: white; }
        .badge-s3 { background: var(--accent-yellow); color: black; }
        
        .stock-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 12px;
        }
        
        .metric {
            text-align: center;
        }
        
        .metric-value {
            font-size: 16px;
            font-weight: 600;
        }
        
        .metric-label {
            font-size: 11px;
            color: var(--text-secondary);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        th {
            background: var(--bg-secondary);
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 12px;
            text-transform: uppercase;
        }
        
        tr:hover {
            background: var(--bg-secondary);
        }
        
        .signal-buy { 
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-green);
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        .signal-sell {
            background: rgba(239, 68, 68, 0.2);
            color: var(--accent-red);
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        .signal-hold {
            background: rgba(245, 158, 11, 0.2);
            color: var(--accent-yellow);
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        .alert {
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        
        .alert-warning {
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid var(--accent-yellow);
        }
        
        .alert-danger {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid var(--accent-red);
        }
        
        .alert-info {
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid var(--accent-blue);
        }
        
        .progress-bar {
            height: 8px;
            background: var(--bg-secondary);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
            transition: width 0.5s;
        }
        
        .chart-placeholder {
            height: 300px;
            background: var(--bg-secondary);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
        }
        
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--text-secondary);
            font-size: 12px;
            border-top: 1px solid var(--border-color);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 十倍股早期识别系统 V2.0</h1>
        <div class="header-meta">
            <span>📅 报告日期: {report_date}</span>
            <span>📊 市场状态: {market_state}</span>
            <span>🎯 筛选结果: {total_picks}只</span>
        </div>
    </div>
    
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('home', this)">🏠 本周投资标的</button>
        <button class="tab-btn" onclick="showTab('system', this)">⚙️ 系统概览</button>
        <button class="tab-btn" onclick="showTab('backtest', this)">📈 回测报告</button>
        <button class="tab-btn" onclick="showTab('stocks', this)">📊 个股分析</button>
        <button class="tab-btn" onclick="showTab('strategy', this)">💹 交易策略</button>
    </div>
    
    <!-- Tab 1: 本周投资标的 -->
    <div id="home" class="tab-content active">
        {tab_home_content}
    </div>
    
    <!-- Tab 2: 系统概览 -->
    <div id="system" class="tab-content">
        {tab_system_content}
    </div>
    
    <!-- Tab 3: 回测报告 -->
    <div id="backtest" class="tab-content">
        {tab_backtest_content}
    </div>
    
    <!-- Tab 4: 个股分析 -->
    <div id="stocks" class="tab-content">
        {tab_stocks_content}
    </div>
    
    <!-- Tab 5: 交易策略 -->
    <div id="strategy" class="tab-content">
        {tab_strategy_content}
    </div>
    
    <div class="footer">
        <p>⚠️ 风险提示: 本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。</p>
        <p>Generated by TRQuant - 十倍股早期识别系统 V2.0 | {timestamp}</p>
    </div>
    
    <script>
        function showTab(tabId, btn) {
            // 隐藏所有内容
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // 移除所有按钮激活状态
            document.querySelectorAll('.tab-btn').forEach(b => {
                b.classList.remove('active');
            });
            
            // 显示选中的内容
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }
    </script>
</body>
</html>'''
    
    def __init__(self):
        self.report_date = datetime.now().strftime('%Y-%m-%d')
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_report(self, 
                        selections: List[Dict],
                        market_analysis: Dict,
                        backtest_result: Dict = None,
                        trading_plan: Dict = None) -> str:
        """生成完整报告"""
        logger.info("📝 开始生成投资报告...")
        
        # 生成各Tab内容
        tab_home = self._generate_home_tab(selections, market_analysis, trading_plan)
        tab_system = self._generate_system_tab()
        tab_backtest = self._generate_backtest_tab(backtest_result)
        tab_stocks = self._generate_stocks_tab(selections)
        tab_strategy = self._generate_strategy_tab(trading_plan)
        
        # 填充模板（使用replace避免CSS变量冲突）
        market_state_str = market_analysis.get('state', {}).value if hasattr(market_analysis.get('state', {}), 'value') else str(market_analysis.get('state', '未知'))
        
        html = self.HTML_TEMPLATE
        html = html.replace('{report_date}', self.report_date)
        html = html.replace('{market_state}', market_state_str)
        html = html.replace('{total_picks}', str(len(selections)))
        html = html.replace('{timestamp}', self.timestamp)
        html = html.replace('{tab_home_content}', tab_home)
        html = html.replace('{tab_system_content}', tab_system)
        html = html.replace('{tab_backtest_content}', tab_backtest)
        html = html.replace('{tab_stocks_content}', tab_stocks)
        html = html.replace('{tab_strategy_content}', tab_strategy)
        
        logger.info("✅ 报告生成完成")
        return html
    
    def _generate_home_tab(self, selections: List[Dict], market_analysis: Dict, trading_plan: Dict) -> str:
        """生成首页Tab内容"""
        # 市场概览
        market_state = market_analysis.get('state', {})
        state_value = market_state.value if hasattr(market_state, 'value') else str(market_state)
        confidence = market_analysis.get('confidence', 0.5)
        
        # 市场信号
        signals = market_analysis.get('signals', [])
        signals_html = ''.join([f'<li>{s}</li>' for s in signals[:5]])
        
        # TOP5投资标的
        top5 = selections[:5]
        stocks_html = ''
        for i, stock in enumerate(top5, 1):
            stage = stock.get('stage', 'S3')
            stage_class = f'badge-{stage.lower()}'
            score = stock.get('adjusted_score', stock.get('total_score', 0))
            
            stocks_html += f'''
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <span class="stock-name">{i}. {stock.get('name', stock.get('code', ''))}</span>
                        <span class="stock-code">{stock.get('code', '')}</span>
                    </div>
                    <span class="stock-badge {stage_class}">{stage}</span>
                </div>
                <div class="stock-metrics">
                    <div class="metric">
                        <div class="metric-value positive">{score:.1f}</div>
                        <div class="metric-label">综合得分</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{stock.get('market_cap', 0):.1f}亿</div>
                        <div class="metric-label">市值</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value positive">+{stock.get('inc_net_profit_year_on_year', 0):.1f}%</div>
                        <div class="metric-label">利润增速</div>
                    </div>
                </div>
                <div style="margin-top: 12px; font-size: 13px; color: var(--text-secondary);">
                    操作建议: {stock.get('action', stock.get('recommendation', '观望'))}
                </div>
            </div>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">📊 当日市场概览</div>
            <div class="grid-4">
                <div class="stat-card">
                    <div class="stat-value {'positive' if '上涨' in state_value else 'negative' if '下跌' in state_value else 'neutral'}">{state_value}</div>
                    <div class="stat-label">市场状态</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{confidence:.0%}</div>
                    <div class="stat-label">判断置信度</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value positive">{len(selections)}</div>
                    <div class="stat-label">筛选股票数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(top5)}</div>
                    <div class="stat-label">TOP推荐数</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📈 市场信号</div>
            <ul style="padding-left: 20px; color: var(--text-secondary);">
                {signals_html if signals_html else '<li>暂无明显信号</li>'}
            </ul>
        </div>
        
        <div class="card">
            <div class="card-title">🌟 本周TOP5投资标的</div>
            <div class="grid-2">
                {stocks_html}
            </div>
        </div>
        
        <div class="alert alert-warning">
            <strong>⚠️ 风险提示</strong>
            <p style="margin-top: 8px;">1. 本报告基于历史数据分析，不保证未来收益</p>
            <p>2. 投资有风险，入市需谨慎，建议分批建仓</p>
            <p>3. 市场环境变化时需重新评估，严格执行止损纪律</p>
        </div>
        '''
    
    def _generate_system_tab(self) -> str:
        """生成系统概览Tab"""
        return '''
        <div class="card">
            <div class="card-title">⚙️ 因子体系说明</div>
            <div class="grid-2">
                <div>
                    <h4 style="margin-bottom: 12px;">核心因子 (6个, 验证有效)</h4>
                    <table>
                        <tr><th>因子</th><th>权重</th><th>来源</th></tr>
                        <tr><td>成长因子</td><td>30%</td><td>营收/利润增速</td></tr>
                        <tr><td>质量因子</td><td>25%</td><td>ROE/ROA/毛利率</td></tr>
                        <tr><td>估值因子</td><td>15%</td><td>PE/PB/PEG</td></tr>
                        <tr><td>动量因子</td><td>15%</td><td>20d/60d动量</td></tr>
                        <tr><td>规模因子</td><td>10%</td><td>市值30-150亿</td></tr>
                        <tr><td>技术因子</td><td>5%</td><td>均线/量价</td></tr>
                    </table>
                </div>
                <div>
                    <h4 style="margin-bottom: 12px;">创新因子 (4个, 新增)</h4>
                    <table>
                        <tr><th>因子</th><th>权重</th><th>说明</th></tr>
                        <tr><td>营收加速度</td><td>10%</td><td>本期增速-上期增速</td></tr>
                        <tr><td>资金流向</td><td>8%</td><td>主力净流入/成交额</td></tr>
                        <tr><td>北向资金</td><td>5%</td><td>北向持仓变化率</td></tr>
                        <tr><td>舆情热度</td><td>2%</td><td>市场关注度</td></tr>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🔍 三层漏斗筛选逻辑</div>
            <div class="grid-3">
                <div class="stat-card">
                    <div class="stat-value">L0</div>
                    <div class="stat-label">基础过滤</div>
                    <p style="font-size: 12px; margin-top: 8px; color: var(--text-secondary);">
                        剔除ST、市值30-1000亿、换手率>0.5%、上市>365天
                    </p>
                </div>
                <div class="stat-card">
                    <div class="stat-value">L1</div>
                    <div class="stat-label">早期信号</div>
                    <p style="font-size: 12px; margin-top: 8px; color: var(--text-secondary);">
                        营收增速>20%、利润增速>25%、ROE>8%、得分>50
                    </p>
                </div>
                <div class="stat-card">
                    <div class="stat-value">L2</div>
                    <div class="stat-label">精选推荐</div>
                    <p style="font-size: 12px; margin-top: 8px; color: var(--text-secondary);">
                        得分>70、均线多头、量价配合、资金流入
                    </p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 成长阶段识别 (S0-S5)</div>
            <table>
                <tr><th>阶段</th><th>市值范围</th><th>增速特征</th><th>操作建议</th></tr>
                <tr><td><span class="stock-badge badge-s0">S0 种子期</span></td><td>&lt;50亿</td><td>增速显现</td><td>观望/小仓试探</td></tr>
                <tr><td><span class="stock-badge badge-s1">S1 萌芽期 ★</span></td><td>50-100亿</td><td>增速>30%</td><td>★建仓/加仓</td></tr>
                <tr><td><span class="stock-badge badge-s2">S2 加速期</span></td><td>100-300亿</td><td>增速>50%</td><td>持有/趋势加仓</td></tr>
                <tr><td><span class="stock-badge badge-s3">S3 扩张期</span></td><td>300-800亿</td><td>持续增长</td><td>持有/部分获利</td></tr>
                <tr><td style="color: var(--text-secondary);">S4 成熟期</td><td>>800亿</td><td>增速放缓</td><td>减仓/获利了结</td></tr>
                <tr><td style="color: var(--accent-red);">S5 衰退期</td><td>-</td><td>增速转负</td><td>清仓</td></tr>
            </table>
        </div>
        '''
    
    def _generate_backtest_tab(self, backtest_result: Dict = None) -> str:
        """生成回测报告Tab"""
        if backtest_result is None:
            backtest_result = {
                'total_return': 0,
                'annual_return': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'total_trades': 0,
                'win_rate': 0
            }
        
        total_return = backtest_result.get('total_return', 0)
        annual_return = backtest_result.get('annual_return', 0)
        max_drawdown = backtest_result.get('max_drawdown', 0)
        sharpe_ratio = backtest_result.get('sharpe_ratio', 0)
        
        return f'''
        <div class="card">
            <div class="card-title">📈 回测核心指标</div>
            <div class="grid-4">
                <div class="stat-card">
                    <div class="stat-value {'positive' if total_return > 0 else 'negative'}">{total_return:.1f}%</div>
                    <div class="stat-label">总收益率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'positive' if annual_return > 0 else 'negative'}">{annual_return:.1f}%</div>
                    <div class="stat-label">年化收益率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value negative">{max_drawdown:.1f}%</div>
                    <div class="stat-label">最大回撤</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{sharpe_ratio:.2f}</div>
                    <div class="stat-label">夏普比率</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 回测配置</div>
            <div class="grid-2">
                <table>
                    <tr><th>参数</th><th>值</th></tr>
                    <tr><td>回测时间</td><td>2022-01-01 ~ 2025-01-06 (3年)</td></tr>
                    <tr><td>初始资金</td><td>100万</td></tr>
                    <tr><td>目标收益</td><td>1000% (10倍)</td></tr>
                    <tr><td>佣金费率</td><td>万一 (0.01%)</td></tr>
                </table>
                <table>
                    <tr><th>参数</th><th>值</th></tr>
                    <tr><td>最大持仓</td><td>8只</td></tr>
                    <tr><td>单票上限</td><td>25%</td></tr>
                    <tr><td>调仓周期</td><td>10个交易日</td></tr>
                    <tr><td>止损比例</td><td>-15%</td></tr>
                </table>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📉 收益曲线</div>
            <div class="chart-placeholder">
                [收益曲线图表 - 需要JavaScript图表库支持]
            </div>
        </div>
        
        <div class="alert alert-info">
            <strong>📝 回测说明</strong>
            <p style="margin-top: 8px;">1. 回测采用事件驱动模式，考虑了交易成本和滑点</p>
            <p>2. 历史回测结果不代表未来收益，市场环境变化可能导致策略失效</p>
            <p>3. 10倍收益目标极具挑战性，实际操作需根据市场情况灵活调整</p>
        </div>
        '''
    
    def _generate_stocks_tab(self, selections: List[Dict]) -> str:
        """生成个股分析Tab"""
        if not selections:
            return '<div class="card"><p>暂无推荐股票</p></div>'
        
        stocks_html = ''
        for i, stock in enumerate(selections[:10], 1):
            code = stock.get('code', '')
            score = stock.get('adjusted_score', stock.get('total_score', 0))
            stage = stock.get('stage', 'S3')
            
            # 财务指标
            roe = stock.get('roe', 0)
            rev_growth = stock.get('inc_revenue_year_on_year', 0)
            profit_growth = stock.get('inc_net_profit_year_on_year', 0)
            pe = stock.get('pe_ratio', 0)
            pb = stock.get('pb_ratio', 0)
            market_cap = stock.get('market_cap', 0)
            
            stocks_html += f'''
            <div class="card">
                <div class="card-title">{i}. {stock.get('name', code)} ({code})</div>
                <div class="grid-3">
                    <div class="stat-card">
                        <div class="stat-value positive">{score:.1f}</div>
                        <div class="stat-label">综合得分</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stage}</div>
                        <div class="stat-label">成长阶段</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{market_cap:.1f}亿</div>
                        <div class="stat-label">总市值</div>
                    </div>
                </div>
                
                <h4 style="margin: 16px 0 12px;">财务指标</h4>
                <div class="grid-3">
                    <div class="metric">
                        <div class="metric-value">{roe:.1f}%</div>
                        <div class="metric-label">ROE</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value positive">+{rev_growth:.1f}%</div>
                        <div class="metric-label">营收增速</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value positive">+{profit_growth:.1f}%</div>
                        <div class="metric-label">利润增速</div>
                    </div>
                </div>
                
                <h4 style="margin: 16px 0 12px;">估值指标</h4>
                <div class="grid-3">
                    <div class="metric">
                        <div class="metric-value">{pe:.1f}</div>
                        <div class="metric-label">PE</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{pb:.1f}</div>
                        <div class="metric-label">PB</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{pe/profit_growth if profit_growth > 0 else 0:.2f}</div>
                        <div class="metric-label">PEG</div>
                    </div>
                </div>
                
                <div style="margin-top: 16px; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
                    <strong>投资建议:</strong> {stock.get('recommendation', stock.get('action', '观望'))}
                </div>
            </div>
            '''
        
        return stocks_html
    
    def _generate_strategy_tab(self, trading_plan: Dict = None) -> str:
        """生成交易策略Tab"""
        return '''
        <div class="card">
            <div class="card-title">🎯 入场策略</div>
            <table>
                <tr><th>条件</th><th>说明</th></tr>
                <tr><td>信号确认</td><td>L2精选 + 市场趋势确认</td></tr>
                <tr><td>最佳时机</td><td>S1阶段优先，量价突破确认</td></tr>
                <tr><td>建仓方式</td><td>分批建仓，首次50%，确认后加仓</td></tr>
                <tr><td>入场价位</td><td>突破20日均线或回调至支撑位</td></tr>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">💰 仓位管理</div>
            <div class="grid-2">
                <div class="stat-card">
                    <div class="stat-value">25%</div>
                    <div class="stat-label">单票上限 (激进)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">5-8只</div>
                    <div class="stat-label">持仓数量 (集中)</div>
                </div>
            </div>
            <div style="margin-top: 16px;">
                <p>• 根据市场环境动态调整现金储备</p>
                <p>• 强势市场满仓操作，弱势市场保留50%以上现金</p>
                <p>• 单一行业占比不超过40%</p>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">🛡️ 风险控制</div>
            <table>
                <tr><th>类型</th><th>条件</th><th>动作</th></tr>
                <tr><td class="negative">固定止损</td><td>亏损达到-15%</td><td>无条件卖出</td></tr>
                <tr><td class="positive">目标止盈</td><td>盈利达到100%</td><td>减仓30%</td></tr>
                <tr><td class="positive">移动止盈</td><td>盈利回撤20%</td><td>全部卖出 (利润>50%时启用)</td></tr>
                <tr><td class="neutral">时间止损</td><td>30天无表现</td><td>考虑换股</td></tr>
            </table>
        </div>
        
        <div class="card">
            <div class="card-title">📅 调仓计划</div>
            <ul style="padding-left: 20px;">
                <li>每10个交易日进行一次调仓检查</li>
                <li>市场环境变化时立即调整仓位</li>
                <li>个股基本面变化时重新评估</li>
                <li>止损止盈信号触发时立即执行</li>
            </ul>
        </div>
        
        <div class="alert alert-danger">
            <strong>⚠️ 重要提醒</strong>
            <p style="margin-top: 8px;">1. 严格执行止损纪律，宁可错过也不追高</p>
            <p>2. 分批建仓减少风险，不要一次性满仓</p>
            <p>3. 市场下跌时优先保护本金，减少操作</p>
            <p>4. 定期复盘，根据实际情况调整策略参数</p>
        </div>
        '''
    
    def save_report(self, html_content: str, output_path: str = None) -> str:
        """保存报告"""
        if output_path is None:
            output_dir = PROJECT_ROOT / "output" / "reports"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"tenbagger_v2_weekly_{datetime.now().strftime('%Y%m%d')}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"📄 报告已保存: {output_path}")
        return str(output_path)


# ============================================================
# 主入口
# ============================================================

def generate_weekly_report():
    """生成周度报告"""
    from research.tenbagger_10x_strategy.scripts.tenbagger_v2_screener import TenbaggerV2Screener
    from research.tenbagger_10x_strategy.scripts.tenbagger_v2_market_adapter import TenbaggerV2MarketAdapter
    
    logger.info("\n" + "="*70)
    logger.info("🚀 十倍股V2 - 周度投资报告生成")
    logger.info("="*70)
    
    # 1. 市场分析
    market_adapter = TenbaggerV2MarketAdapter()
    market_state, adjustment = market_adapter.analyze_and_adapt()
    market_analysis = {
        'state': market_state,
        'confidence': 0.7,  # 示例
        'signals': ['均线多头排列', '成交量放大'] if market_state.value in ['强势上涨', '上涨'] else ['市场震荡', '观望为主']
    }
    
    # 2. 股票筛选
    screener = TenbaggerV2Screener()
    selections = screener.run_full_screening()
    
    # 3. 生成报告
    generator = TenbaggerV2ReportGenerator()
    html = generator.generate_report(
        selections=selections,
        market_analysis=market_analysis,
        backtest_result=None,  # 可以传入回测结果
        trading_plan=None
    )
    
    # 4. 保存报告
    output_path = generator.save_report(html)
    
    logger.info(f"\n✅ 报告生成完成!")
    logger.info(f"📍 文件位置: {output_path}")
    
    return output_path


if __name__ == "__main__":
    generate_weekly_report()
