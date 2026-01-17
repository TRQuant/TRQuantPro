"""
科技高成长策略综合报告
=====================================
生成包含以下内容的HTML报告：
1. 当前选股结果
2. 历史回测验证
3. 典型案例论证
4. 策略优化建议
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from jqdatasdk import auth, get_price

from tech_growth_screener import TechGrowthScreener, StockAnalysis, GrowthStage, TrendPhase
from tech_growth_backtest import TechGrowthBacktester, BacktestResult, HistoricalCase


class TechGrowthReportGenerator:
    """科技高成长策略报告生成器"""
    
    def __init__(self):
        self.screener = TechGrowthScreener()
        self.backtester = TechGrowthBacktester()
        self.selections: List[StockAnalysis] = []
        self.backtest_results: List[BacktestResult] = []
        self.cases: List[HistoricalCase] = []
    
    def generate_full_report(
        self,
        output_dir: str = 'output/reports',
        top_n: int = 5,
        run_backtest: bool = True
    ) -> str:
        """
        生成完整报告
        
        Args:
            output_dir: 输出目录
            top_n: 选股数量
            run_backtest: 是否运行回测
        
        Returns:
            报告文件路径
        """
        print(f"\n{'='*70}")
        print(f"📝 生成科技高成长策略综合报告")
        print(f"{'='*70}")
        
        # Step 1: 当前选股
        print("\n📊 Step 1: 运行当前选股...")
        df_selections = self.screener.screen(top_n=top_n)
        self.selections = self.screener.final_selection
        
        # Step 2: 历史回测（可选）
        if run_backtest:
            print("\n📈 Step 2: 运行历史回测...")
            self.backtester.run_backtest(
                start_date='2024-01-01',
                end_date='2024-11-01',
                frequency='monthly',
                top_n=5
            )
            self.backtest_results = self.backtester.results
            
            print("\n🔍 Step 3: 分析历史案例...")
            self.cases = self.backtester.analyze_historical_cases()
        
        # Step 3: 生成HTML报告
        print("\n📝 Step 4: 生成HTML报告...")
        html_content = self._generate_html()
        
        # 保存报告
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(output_dir, f'tech_growth_report_{timestamp}.html')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ 报告已生成: {report_path}")
        
        return report_path
    
    def _generate_html(self) -> str:
        """生成HTML内容"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技高成长策略研究报告</title>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--primary), #8b5cf6, #ec4899);
            padding: 60px 40px;
            border-radius: 24px;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.3;
        }}
        
        header h1 {{
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
            position: relative;
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
            position: relative;
        }}
        
        /* Tabs */
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .tab-btn {{
            padding: 12px 24px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text);
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .tab-btn:hover {{
            background: var(--primary);
            border-color: var(--primary);
        }}
        
        .tab-btn.active {{
            background: var(--primary);
            border-color: var(--primary);
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        /* Cards */
        .card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .card-title {{
            font-size: 1.4em;
            font-weight: 600;
        }}
        
        /* Stock Cards */
        .stock-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}
        
        .stock-card {{
            background: linear-gradient(145deg, var(--bg-card), #0f172a);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}
        
        .stock-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--success));
        }}
        
        .stock-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        
        .stock-name {{
            font-size: 1.5em;
            font-weight: 700;
        }}
        
        .stock-code {{
            color: var(--text-muted);
            font-size: 0.9em;
        }}
        
        .stock-sector {{
            background: linear-gradient(135deg, var(--primary), #8b5cf6);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .metric {{
            text-align: center;
            padding: 15px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 12px;
        }}
        
        .metric-value {{
            font-size: 1.4em;
            font-weight: 700;
            color: var(--success);
        }}
        
        .metric-value.negative {{
            color: var(--danger);
        }}
        
        .metric-label {{
            font-size: 0.8em;
            color: var(--text-muted);
            margin-top: 5px;
        }}
        
        .stock-reason {{
            background: rgba(16, 185, 129, 0.1);
            border-left: 4px solid var(--success);
            padding: 15px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 15px;
        }}
        
        .stock-targets {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        
        .target-box {{
            padding: 12px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .target-box.stop-loss {{
            background: rgba(239, 68, 68, 0.1);
        }}
        
        .target-box.target {{
            background: rgba(16, 185, 129, 0.1);
        }}
        
        .target-label {{
            font-size: 0.8em;
            color: var(--text-muted);
        }}
        
        .target-value {{
            font-size: 1.2em;
            font-weight: 700;
        }}
        
        .target-value.red {{
            color: var(--danger);
        }}
        
        .target-value.green {{
            color: var(--success);
        }}
        
        /* Backtest Stats */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid var(--border);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .stat-value.positive {{
            color: var(--success);
        }}
        
        .stat-label {{
            color: var(--text-muted);
        }}
        
        /* Tables */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        .data-table th {{
            background: var(--bg-dark);
            font-weight: 600;
            color: var(--primary);
        }}
        
        .data-table tr:hover {{
            background: rgba(99, 102, 241, 0.05);
        }}
        
        .positive {{
            color: var(--success);
        }}
        
        .negative {{
            color: var(--danger);
        }}
        
        /* Case Study */
        .case-card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid var(--success);
        }}
        
        .case-card.fail {{
            border-left-color: var(--danger);
        }}
        
        .case-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .case-title {{
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .case-date {{
            color: var(--text-muted);
            font-size: 0.9em;
        }}
        
        .case-returns {{
            display: flex;
            gap: 20px;
            margin: 10px 0;
        }}
        
        .case-return {{
            padding: 8px 15px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 8px;
        }}
        
        .case-lesson {{
            background: rgba(245, 158, 11, 0.1);
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            font-style: italic;
        }}
        
        /* Strategy Section */
        .strategy-box {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        
        .strategy-title {{
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--primary);
        }}
        
        .strategy-list {{
            list-style: none;
        }}
        
        .strategy-list li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
        }}
        
        .strategy-list li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success);
            font-weight: bold;
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-muted);
            margin-top: 40px;
            border-top: 1px solid var(--border);
        }}
        
        /* Animation */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate {{
            animation: fadeIn 0.5s ease-out;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 科技高成长策略研究报告</h1>
            <p>📅 生成时间: {current_date} | 策略: 早期布局 + 趋势跟随 + 波段操作</p>
        </header>
        
        <!-- Tabs -->
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('selection')">📊 当前选股</button>
            <button class="tab-btn" onclick="showTab('backtest')">📈 回测验证</button>
            <button class="tab-btn" onclick="showTab('cases')">📋 案例论证</button>
            <button class="tab-btn" onclick="showTab('strategy')">⚙️ 策略逻辑</button>
            <button class="tab-btn" onclick="showTab('optimize')">🔧 优化建议</button>
        </div>
        
        <!-- Tab 1: 当前选股 -->
        <div id="selection" class="tab-content active">
            {self._generate_selection_tab()}
        </div>
        
        <!-- Tab 2: 回测验证 -->
        <div id="backtest" class="tab-content">
            {self._generate_backtest_tab()}
        </div>
        
        <!-- Tab 3: 案例论证 -->
        <div id="cases" class="tab-content">
            {self._generate_cases_tab()}
        </div>
        
        <!-- Tab 4: 策略逻辑 -->
        <div id="strategy" class="tab-content">
            {self._generate_strategy_tab()}
        </div>
        
        <!-- Tab 5: 优化建议 -->
        <div id="optimize" class="tab-content">
            {self._generate_optimize_tab()}
        </div>
        
        <footer>
            <p>⚠️ 风险提示: 本报告仅供研究参考，不构成投资建议。投资有风险，入市需谨慎。</p>
            <p>生成时间: {current_date}</p>
        </footer>
    </div>
    
    <script>
        function showTab(tabId) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''
        
        return html
    
    def _generate_selection_tab(self) -> str:
        """生成选股结果Tab"""
        if not self.selections:
            return '<div class="card"><p>暂无选股结果</p></div>'
        
        # 汇总统计
        avg_growth = np.mean([s.profit_growth for s in self.selections])
        avg_score = np.mean([s.total_score for s in self.selections])
        sectors = set([s.sector for s in self.selections])
        
        html = f'''
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value positive">{len(self.selections)}</div>
                <div class="stat-label">选出股票数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value positive">{avg_growth:.1f}%</div>
                <div class="stat-label">平均利润增速</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_score:.1f}</div>
                <div class="stat-label">平均综合得分</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(sectors)}</div>
                <div class="stat-label">覆盖板块数</div>
            </div>
        </div>
        
        <div class="stock-grid">
        '''
        
        for i, s in enumerate(self.selections):
            growth_class = 'positive' if s.profit_growth > 0 else 'negative'
            
            html += f'''
            <div class="stock-card animate">
                <div class="stock-header">
                    <div>
                        <div class="stock-name">{i+1}. {s.name}</div>
                        <div class="stock-code">{s.code}</div>
                    </div>
                    <span class="stock-sector">{s.sector}</span>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value {growth_class}">{s.profit_growth:.1f}%</div>
                        <div class="metric-label">利润增速</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.pe:.1f}</div>
                        <div class="metric-label">PE估值</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.peg:.2f}</div>
                        <div class="metric-label">PEG</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{s.total_score:.1f}</div>
                        <div class="metric-label">综合得分</div>
                    </div>
                </div>
                
                <div class="stock-reason">
                    <strong>📌 入选理由:</strong> {s.reason}
                </div>
                
                <div class="stock-targets">
                    <div class="target-box stop-loss">
                        <div class="target-label">🛡️ 止损位</div>
                        <div class="target-value red">¥{s.stop_loss:.2f}</div>
                    </div>
                    <div class="target-box target">
                        <div class="target-label">🎯 目标位</div>
                        <div class="target-value green">¥{s.target_price:.2f}</div>
                    </div>
                </div>
                
                <div style="margin-top: 15px; display: flex; gap: 10px;">
                    <span style="background: rgba(99,102,241,0.1); padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">
                        {s.growth_stage.value}
                    </span>
                    <span style="background: rgba(99,102,241,0.1); padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">
                        {s.trend_phase.value}
                    </span>
                    <span style="background: {'rgba(16,185,129,0.2)' if s.swing_signal == 'BUY' else 'rgba(239,68,68,0.2)' if s.swing_signal == 'SELL' else 'rgba(245,158,11,0.2)'}; padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">
                        {s.swing_signal}
                    </span>
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _generate_backtest_tab(self) -> str:
        """生成回测Tab"""
        if not self.backtest_results:
            return '''
            <div class="card">
                <h3>📊 回测数据加载中...</h3>
                <p>请稍候，正在运行历史回测验证...</p>
            </div>
            '''
        
        # 计算统计数据
        returns_1w = [r.return_1w for r in self.backtest_results]
        returns_1m = [r.return_1m for r in self.backtest_results]
        returns_3m = [r.return_3m for r in self.backtest_results]
        excess_1w = [r.excess_1w for r in self.backtest_results]
        excess_1m = [r.excess_1m for r in self.backtest_results]
        excess_3m = [r.excess_3m for r in self.backtest_results]
        
        win_rate_1w = sum(1 for x in excess_1w if x > 0) / len(excess_1w) * 100 if excess_1w else 0
        win_rate_1m = sum(1 for x in excess_1m if x > 0) / len(excess_1m) * 100 if excess_1m else 0
        win_rate_3m = sum(1 for x in excess_3m if x > 0) / len(excess_3m) * 100 if excess_3m else 0
        
        html = f'''
        <div class="card">
            <div class="card-header">
                <span class="card-title">📈 回测绩效统计</span>
                <span>回测期间: 2024-01-01 ~ 2024-11-01</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value positive">{win_rate_1w:.1f}%</div>
                    <div class="stat-label">1周胜率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value positive">{win_rate_1m:.1f}%</div>
                    <div class="stat-label">1月胜率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value positive">{win_rate_3m:.1f}%</div>
                    <div class="stat-label">3月胜率</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(self.backtest_results)}</div>
                    <div class="stat-label">回测次数</div>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value {'positive' if np.mean(returns_1m) > 0 else 'negative'}">{np.mean(returns_1m):+.2f}%</div>
                    <div class="stat-label">平均1月收益</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'positive' if np.mean(excess_1m) > 0 else 'negative'}">{np.mean(excess_1m):+.2f}%</div>
                    <div class="stat-label">平均1月超额</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'positive' if np.mean(returns_3m) > 0 else 'negative'}">{np.mean(returns_3m):+.2f}%</div>
                    <div class="stat-label">平均3月收益</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'positive' if np.mean(excess_3m) > 0 else 'negative'}">{np.mean(excess_3m):+.2f}%</div>
                    <div class="stat-label">平均3月超额</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📋 每期回测明细</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>选股</th>
                        <th>1周收益</th>
                        <th>1月收益</th>
                        <th>3月收益</th>
                        <th>1月超额</th>
                        <th>3月超额</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for r in self.backtest_results[:15]:  # 显示前15条
            html += f'''
                <tr>
                    <td>{r.date}</td>
                    <td>{', '.join(r.names[:2])}...</td>
                    <td class="{'positive' if r.return_1w > 0 else 'negative'}">{r.return_1w:+.1f}%</td>
                    <td class="{'positive' if r.return_1m > 0 else 'negative'}">{r.return_1m:+.1f}%</td>
                    <td class="{'positive' if r.return_3m > 0 else 'negative'}">{r.return_3m:+.1f}%</td>
                    <td class="{'positive' if r.excess_1m > 0 else 'negative'}">{r.excess_1m:+.1f}%</td>
                    <td class="{'positive' if r.excess_3m > 0 else 'negative'}">{r.excess_3m:+.1f}%</td>
                </tr>
            '''
        
        html += '''
                </tbody>
            </table>
        </div>
        '''
        
        return html
    
    def _generate_cases_tab(self) -> str:
        """生成案例论证Tab"""
        if not self.cases:
            return '<div class="card"><p>暂无案例数据</p></div>'
        
        success_cases = [c for c in self.cases if c.is_success]
        fail_cases = [c for c in self.cases if not c.is_success]
        
        html = '''
        <div class="card">
            <div class="card-title">✅ 成功案例 - 实例论证</div>
            <p style="color: var(--text-muted); margin-bottom: 20px;">
                以下案例展示了策略选出的高成长股票在后续3个月取得超过10%收益的实例
            </p>
        '''
        
        for c in success_cases[:5]:
            html += f'''
            <div class="case-card">
                <div class="case-header">
                    <span class="case-title">{c.stock_name} ({c.stock_code})</span>
                    <span class="case-date">选股日期: {c.select_date}</span>
                </div>
                <div style="color: var(--text-muted); margin-bottom: 10px;">
                    📌 选股理由: {c.select_reason}
                </div>
                <div class="case-returns">
                    <div class="case-return">
                        <span style="color: var(--text-muted);">1周:</span>
                        <span class="{'positive' if c.return_1w > 0 else 'negative'}">{c.return_1w:+.1f}%</span>
                    </div>
                    <div class="case-return">
                        <span style="color: var(--text-muted);">1月:</span>
                        <span class="{'positive' if c.return_1m > 0 else 'negative'}">{c.return_1m:+.1f}%</span>
                    </div>
                    <div class="case-return">
                        <span style="color: var(--text-muted);">3月:</span>
                        <span class="{'positive' if c.return_3m > 0 else 'negative'}">{c.return_3m:+.1f}%</span>
                    </div>
                </div>
                <div class="case-lesson">
                    💡 经验总结: {c.lesson}
                </div>
            </div>
            '''
        
        html += '''
        </div>
        
        <div class="card">
            <div class="card-title">⚠️ 失败案例 - 教训反思</div>
            <p style="color: var(--text-muted); margin-bottom: 20px;">
                以下案例展示了策略选股后表现不佳的情况，用于反思和改进策略
            </p>
        '''
        
        for c in fail_cases[:5]:
            html += f'''
            <div class="case-card fail">
                <div class="case-header">
                    <span class="case-title">{c.stock_name} ({c.stock_code})</span>
                    <span class="case-date">选股日期: {c.select_date}</span>
                </div>
                <div style="color: var(--text-muted); margin-bottom: 10px;">
                    📌 选股理由: {c.select_reason}
                </div>
                <div class="case-returns">
                    <div class="case-return">
                        <span style="color: var(--text-muted);">1周:</span>
                        <span class="{'positive' if c.return_1w > 0 else 'negative'}">{c.return_1w:+.1f}%</span>
                    </div>
                    <div class="case-return">
                        <span style="color: var(--text-muted);">1月:</span>
                        <span class="{'positive' if c.return_1m > 0 else 'negative'}">{c.return_1m:+.1f}%</span>
                    </div>
                    <div class="case-return">
                        <span style="color: var(--text-muted);">3月:</span>
                        <span class="{'positive' if c.return_3m > 0 else 'negative'}">{c.return_3m:+.1f}%</span>
                    </div>
                    <div class="case-return">
                        <span style="color: var(--text-muted);">最大回撤:</span>
                        <span class="negative">{c.max_drawdown:.1f}%</span>
                    </div>
                </div>
                <div class="case-lesson" style="background: rgba(239, 68, 68, 0.1);">
                    ⚠️ 教训: {c.lesson}
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _generate_strategy_tab(self) -> str:
        """生成策略逻辑Tab"""
        return '''
        <div class="strategy-box">
            <div class="strategy-title">🎯 核心选股逻辑</div>
            <p>本策略聚焦<strong>科技主线板块</strong>中的<strong>高成长股票</strong>，通过多维度筛选识别具有持续上涨潜力的标的。</p>
            
            <h4 style="margin: 20px 0 10px; color: var(--primary);">1️⃣ 板块聚焦</h4>
            <ul class="strategy-list">
                <li>半导体芯片 - 国产替代核心赛道</li>
                <li>人工智能 - AI应用落地元年</li>
                <li>新能源电池 - 储能+电动化双轮驱动</li>
                <li>脑机接口 - 前沿科技蓝海</li>
                <li>人形机器人 - 具身智能爆发</li>
            </ul>
            
            <h4 style="margin: 20px 0 10px; color: var(--primary);">2️⃣ 成长性筛选</h4>
            <ul class="strategy-list">
                <li>利润增速 > 30% (核心指标)</li>
                <li>营收增速 > 20% (规模扩张)</li>
                <li>ROE > 8% (盈利质量)</li>
                <li>PEG < 2 (成长性价比)</li>
            </ul>
            
            <h4 style="margin: 20px 0 10px; color: var(--primary);">3️⃣ 趋势确认</h4>
            <ul class="strategy-list">
                <li>均线多头排列 (MA5>MA10>MA20)</li>
                <li>价格站上60日均线</li>
                <li>量价配合良好</li>
                <li>趋势阶段识别 (底部/突破/上升/加速)</li>
            </ul>
            
            <h4 style="margin: 20px 0 10px; color: var(--primary);">4️⃣ 波段信号</h4>
            <ul class="strategy-list">
                <li>RSI超卖区(<30)发出买入信号</li>
                <li>均线金叉确认入场</li>
                <li>RSI超买区(>70)提示止盈</li>
                <li>支撑/阻力位动态计算</li>
            </ul>
        </div>
        
        <div class="card">
            <div class="card-title">📊 评分体系</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>维度</th>
                        <th>权重</th>
                        <th>核心指标</th>
                        <th>满分标准</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>成长得分</td>
                        <td>40%</td>
                        <td>利润增速、营收增速、ROE</td>
                        <td>利润>100%, 营收>50%, ROE>20%</td>
                    </tr>
                    <tr>
                        <td>趋势得分</td>
                        <td>30%</td>
                        <td>均线排列、价格位置、涨幅</td>
                        <td>多头排列+20日涨>20%</td>
                    </tr>
                    <tr>
                        <td>估值得分</td>
                        <td>20%</td>
                        <td>PEG、PE相对行业</td>
                        <td>PEG<1</td>
                    </tr>
                    <tr>
                        <td>板块权重</td>
                        <td>10%</td>
                        <td>板块热度系数</td>
                        <td>脑机接口1.3x, AI/芯片1.2x</td>
                    </tr>
                </tbody>
            </table>
        </div>
        '''
    
    def _generate_optimize_tab(self) -> str:
        """生成优化建议Tab"""
        return '''
        <div class="card">
            <div class="card-title">🔧 策略优化建议</div>
            
            <div class="strategy-box">
                <h4 style="color: var(--warning);">基于回测结果的改进方向</h4>
                
                <h5 style="margin: 15px 0 10px;">1. 入场时机优化</h5>
                <ul class="strategy-list">
                    <li>增加回调买入逻辑，避免追高</li>
                    <li>结合大盘走势过滤，熊市减少开仓</li>
                    <li>加入成交量突破确认</li>
                </ul>
                
                <h5 style="margin: 15px 0 10px;">2. 止盈止损优化</h5>
                <ul class="strategy-list">
                    <li>采用移动止损，保护浮盈</li>
                    <li>分批止盈，锁定部分利润</li>
                    <li>根据波动率动态调整止损幅度</li>
                </ul>
                
                <h5 style="margin: 15px 0 10px;">3. 仓位管理优化</h5>
                <ul class="strategy-list">
                    <li>根据市场环境调整总仓位</li>
                    <li>单只股票最大仓位不超过25%</li>
                    <li>板块集中度控制</li>
                </ul>
                
                <h5 style="margin: 15px 0 10px;">4. 选股因子优化</h5>
                <ul class="strategy-list">
                    <li>加入机构持仓变化因子</li>
                    <li>考虑研发投入占比</li>
                    <li>引入分析师一致预期</li>
                </ul>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📈 下一步计划</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>优化项</th>
                        <th>预期效果</th>
                        <th>优先级</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>大盘择时模块</td>
                        <td>减少系统性风险暴露</td>
                        <td>高</td>
                        <td>待开发</td>
                    </tr>
                    <tr>
                        <td>动态止盈止损</td>
                        <td>提高收益风险比</td>
                        <td>高</td>
                        <td>待开发</td>
                    </tr>
                    <tr>
                        <td>机器学习因子挖掘</td>
                        <td>发现非线性因子</td>
                        <td>中</td>
                        <td>规划中</td>
                    </tr>
                    <tr>
                        <td>实盘模拟跟踪</td>
                        <td>验证策略稳定性</td>
                        <td>高</td>
                        <td>待启动</td>
                    </tr>
                </tbody>
            </table>
        </div>
        '''


def generate_report():
    """生成报告入口"""
    # JQData认证
    auth('18610026017', 'Tt103003!')
    
    generator = TechGrowthReportGenerator()
    report_path = generator.generate_full_report(
        output_dir='output/reports',
        top_n=5,
        run_backtest=True
    )
    
    return report_path


if __name__ == "__main__":
    generate_report()
