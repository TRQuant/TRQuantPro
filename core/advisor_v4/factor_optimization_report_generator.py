#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子优化报告生成器 - 生成多Tab HTML优化报告
==========================================

功能：
1. 优化摘要（最优配置、改进幅度）
2. 因子选择分析（因子重要性、最优组合）
3. 权重优化历史（权重变化曲线、性能对比）
4. Walk-Forward验证结果（各窗口指标、稳定性分析）
5. 可靠性评估（过拟合检测、稳定性指标）
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json

import pandas as pd

logger = logging.getLogger(__name__)

# 可选导入plotly
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    logger.warning("plotly未安装，图表功能将受限")

from .factor_optimizer import OptimizationResult, ValidationResult
from core.utils.output_manager import get_output_manager, OutputCategory, OutputType

logger = logging.getLogger(__name__)


class FactorOptimizationReportGenerator:
    """因子优化报告生成器"""
    
    def __init__(self, verbose: bool = True):
        """
        初始化报告生成器
        
        Args:
            verbose: 是否输出详细信息
        """
        self.verbose = verbose
        self.output_manager = get_output_manager()
    
    def generate_report(
        self,
        optimization_result: OptimizationResult,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        生成完整的HTML优化报告
        
        Args:
            optimization_result: 优化结果
            output_path: 输出路径（如果为None，使用OutputManager生成）
        
        Returns:
            生成的报告文件路径
        """
        if output_path is None:
            output_path = self.output_manager.get_report_path(
                category=OutputCategory.ADVISOR_V4,
                filename="factor_optimization_report.html",
                add_timestamp=True,
            )
        
        if self.verbose:
            print(f"\n生成因子优化报告: {output_path}")
        
        # 构建HTML内容
        html_content = self._build_html(optimization_result)
        
        # 保存文件
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')
        
        if self.verbose:
            print(f"✅ 报告已生成: {output_path}")
        
        return output_path
    
    def _build_html(self, result: OptimizationResult) -> str:
        """构建完整HTML内容"""
        
        # 头部
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>因子优化报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    {self._get_css()}
</head>
<body>
    <div class="container">
        <header>
            <h1>因子优化报告</h1>
            <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <!-- Tab导航 -->
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('summary')">优化摘要</button>
            <button class="tab-button" onclick="showTab('factor-selection')">因子选择分析</button>
            <button class="tab-button" onclick="showTab('weight-history')">权重优化历史</button>
            <button class="tab-button" onclick="showTab('walkforward')">Walk-Forward验证</button>
            <button class="tab-button" onclick="showTab('reliability')">可靠性评估</button>
        </div>
        
        <!-- Tab内容 -->
        <div id="summary" class="tab-content active">
            {self._build_summary_tab(result)}
        </div>
        
        <div id="factor-selection" class="tab-content">
            {self._build_factor_selection_tab(result)}
        </div>
        
        <div id="weight-history" class="tab-content">
            {self._build_weight_history_tab(result)}
        </div>
        
        <div id="walkforward" class="tab-content">
            {self._build_walkforward_tab(result)}
        </div>
        
        <div id="reliability" class="tab-content">
            {self._build_reliability_tab(result)}
        </div>
        
        <footer>
            <p>TRQuant 因子优化系统 v1.0</p>
        </footer>
    </div>
    
    {self._get_javascript()}
</body>
</html>
"""
        return html
    
    def _build_summary_tab(self, result: OptimizationResult) -> str:
        """构建优化摘要Tab"""
        best = result.best_result
        
        if not best:
            return "<p>暂无优化结果</p>"
        
        # 指标对比（初始 vs 最优）
        initial_result = result.optimization_history[0] if result.optimization_history else None
        
        improvement_html = ""
        if initial_result:
            sharpe_improve = best.sharpe_ratio - initial_result.sharpe_ratio
            hit_improve = best.hit_rate - initial_result.hit_rate
            return_improve = best.total_return - initial_result.total_return
            score_improve = best.multi_objective_score - initial_result.multi_objective_score
            
            improvement_html = f"""
            <div class="improvement-section">
                <h3>优化改进</h3>
                <table class="improvement-table">
                    <tr>
                        <th>指标</th>
                        <th>初始值</th>
                        <th>最优值</th>
                        <th>改进幅度</th>
                    </tr>
                    <tr>
                        <td>综合得分</td>
                        <td>{initial_result.multi_objective_score:.2f}</td>
                        <td>{best.multi_objective_score:.2f}</td>
                        <td class="{'positive' if score_improve > 0 else 'negative'}">{score_improve:+.2f}</td>
                    </tr>
                    <tr>
                        <td>夏普比率</td>
                        <td>{initial_result.sharpe_ratio:.3f}</td>
                        <td>{best.sharpe_ratio:.3f}</td>
                        <td class="{'positive' if sharpe_improve > 0 else 'negative'}">{sharpe_improve:+.3f}</td>
                    </tr>
                    <tr>
                        <td>命中率</td>
                        <td>{initial_result.hit_rate:.2%}</td>
                        <td>{best.hit_rate:.2%}</td>
                        <td class="{'positive' if hit_improve > 0 else 'negative'}">{hit_improve:+.2%}</td>
                    </tr>
                    <tr>
                        <td>总收益率</td>
                        <td>{initial_result.total_return:.2%}</td>
                        <td>{best.total_return:.2%}</td>
                        <td class="{'positive' if return_improve > 0 else 'negative'}">{return_improve:+.2%}</td>
                    </tr>
                </table>
            </div>
            """
        
        html = f"""
        <div class="summary-section">
            <h2>优化摘要</h2>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">综合得分</div>
                    <div class="metric-value">{best.multi_objective_score:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">夏普比率</div>
                    <div class="metric-value">{best.sharpe_ratio:.3f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">命中率</div>
                    <div class="metric-value">{best.hit_rate:.2%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">总收益率</div>
                    <div class="metric-value">{best.total_return:.2%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">稳定性得分</div>
                    <div class="metric-value">{best.stability_score:.3f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">过拟合风险</div>
                    <div class="metric-value risk-{best.overfitting_risk}">{best.overfitting_risk.upper()}</div>
                </div>
            </div>
            
            <div class="config-section">
                <h3>最优配置</h3>
                <div class="config-details">
                    <p><strong>因子选择:</strong> {', '.join(best.factor_selection)} ({len(best.factor_selection)}个因子)</p>
                    <p><strong>融合权重:</strong> 已验证因子 {best.fusion_weight:.1%} / 聚宽因子 {1-best.fusion_weight:.1%}</p>
                    <p><strong>优化耗时:</strong> {result.optimization_time_seconds:.1f} 秒</p>
                </div>
            </div>
            
            {improvement_html}
        </div>
        """
        return html
    
    def _build_factor_selection_tab(self, result: OptimizationResult) -> str:
        """构建因子选择分析Tab"""
        best = result.best_result
        
        if not best:
            return "<p>暂无因子选择数据</p>"
        
        # 因子重要性表格
        importance_rows = ""
        for factor, importance in sorted(
            result.factor_importance.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            in_selection = "✅" if factor in best.factor_selection else "❌"
            importance_rows += f"""
            <tr>
                <td>{in_selection}</td>
                <td>{factor}</td>
                <td>{VALIDATED_FACTORS.get(factor, {}).get('name', factor)}</td>
                <td>{importance:.3f}</td>
                <td>{best.factor_weights.get(factor, 0.0):.3f}</td>
            </tr>
            """
        
        html = f"""
        <div class="factor-selection-section">
            <h2>因子选择分析</h2>
            
            <div class="selection-info">
                <h3>最优因子组合</h3>
                <p>从 {len(ALL_VALIDATED_FACTORS)} 个已验证因子中选择了 <strong>{len(best.factor_selection)}</strong> 个因子</p>
                <div class="factor-list">
                    {', '.join([VALIDATED_FACTORS.get(f, {}).get('name', f) for f in best.factor_selection])}
                </div>
            </div>
            
            <div class="importance-table">
                <h3>因子重要性分析</h3>
                <table>
                    <thead>
                        <tr>
                            <th>是否选择</th>
                            <th>因子代码</th>
                            <th>因子名称</th>
                            <th>重要性得分</th>
                            <th>最优权重</th>
                        </tr>
                    </thead>
                    <tbody>
                        {importance_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        return html
    
    def _build_weight_history_tab(self, result: OptimizationResult) -> str:
        """构建权重优化历史Tab"""
        if not result.optimization_history:
            return "<p>暂无权重优化历史</p>"
        
        # 构建权重变化数据
        history_data = []
        for i, val_result in enumerate(result.optimization_history):
            history_data.append({
                'iteration': i + 1,
                'score': val_result.multi_objective_score,
                'sharpe': val_result.sharpe_ratio,
                'hit_rate': val_result.hit_rate,
                'return': val_result.total_return,
            })
        
        history_df = pd.DataFrame(history_data)
        
        # 生成图表（使用Plotly，如果可用）
        if HAS_PLOTLY:
            fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('综合得分变化', '夏普比率变化', '命中率变化', '收益率变化'),
            vertical_spacing=0.15,
        )
        
        fig.add_trace(
            go.Scatter(
                x=history_df['iteration'],
                y=history_df['score'],
                mode='lines+markers',
                name='综合得分',
                line=dict(color='#1f77b4', width=2),
            ),
            row=1, col=1,
        )
        
        fig.add_trace(
            go.Scatter(
                x=history_df['iteration'],
                y=history_df['sharpe'],
                mode='lines+markers',
                name='夏普比率',
                line=dict(color='#ff7f0e', width=2),
            ),
            row=1, col=2,
        )
        
        fig.add_trace(
            go.Scatter(
                x=history_df['iteration'],
                y=history_df['hit_rate'],
                mode='lines+markers',
                name='命中率',
                line=dict(color='#2ca02c', width=2),
            ),
            row=2, col=1,
        )
        
        fig.add_trace(
            go.Scatter(
                x=history_df['iteration'],
                y=history_df['return'],
                mode='lines+markers',
                name='收益率',
                line=dict(color='#d62728', width=2),
            ),
            row=2, col=2,
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            template='plotly_dark',
        )
        
        chart_html = fig.to_html(include_plotlyjs='cdn', div_id="weight-history-chart")
        
        html = f"""
        <div class="weight-history-section">
            <h2>权重优化历史</h2>
            <p>共进行了 {len(result.optimization_history)} 次迭代优化</p>
            {chart_html}
        </div>
        """
        return html
    
    def _build_walkforward_tab(self, result: OptimizationResult) -> str:
        """构建Walk-Forward验证Tab"""
        best = result.best_result
        
        if not best or not best.cv_result:
            return "<p>暂无Walk-Forward验证结果</p>"
        
        cv_result = best.cv_result
        
        # 构建验证结果表格
        fold_rows = ""
        for fold in cv_result.fold_results:
            metrics = fold.metrics
            fold_rows += f"""
            <tr>
                <td>{fold.fold}</td>
                <td>{fold.train_period}</td>
                <td>{fold.val_period}</td>
                <td>{metrics.get('sharpe_ratio', 0.0):.3f}</td>
                <td>{metrics.get('hit_rate', 0.0):.2%}</td>
                <td>{metrics.get('total_return', 0.0):.2%}</td>
            </tr>
            """
        
        html = f"""
        <div class="walkforward-section">
            <h2>Walk-Forward验证结果</h2>
            
            <div class="cv-summary">
                <p><strong>验证周期数:</strong> {cv_result.n_folds}</p>
                <p><strong>平均夏普比率:</strong> {best.sharpe_ratio:.3f}</p>
                <p><strong>平均命中率:</strong> {best.hit_rate:.2%}</p>
                <p><strong>平均收益率:</strong> {best.total_return:.2%}</p>
            </div>
            
            <div class="cv-details">
                <h3>各窗口验证结果</h3>
                <table>
                    <thead>
                        <tr>
                            <th>窗口</th>
                            <th>训练期</th>
                            <th>测试期</th>
                            <th>夏普比率</th>
                            <th>命中率</th>
                            <th>收益率</th>
                        </tr>
                    </thead>
                    <tbody>
                        {fold_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        return html
    
    def _build_reliability_tab(self, result: OptimizationResult) -> str:
        """构建可靠性评估Tab"""
        best = result.best_result
        
        if not best:
            return "<p>暂无可靠性评估数据</p>"
        
        # 过拟合风险等级颜色
        risk_colors = {
            'low': '#2ca02c',
            'medium': '#ff7f0e',
            'high': '#d62728',
        }
        risk_color = risk_colors.get(best.overfitting_risk, '#666')
        
        # 过拟合详情
        overfitting_details_html = ""
        if best.overfitting_details:
            for key, value in best.overfitting_details.items():
                overfitting_details_html += f"<li><strong>{key}:</strong> {value:.4f}</li>"
        
        html = f"""
        <div class="reliability-section">
            <h2>可靠性评估</h2>
            
            <div class="reliability-metrics">
                <div class="metric-card">
                    <div class="metric-label">稳定性得分</div>
                    <div class="metric-value">{best.stability_score:.3f}</div>
                    <div class="metric-desc">得分越高，模型越稳定</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">过拟合风险</div>
                    <div class="metric-value" style="color: {risk_color}">{best.overfitting_risk.upper()}</div>
                    <div class="metric-desc">风险等级评估</div>
                </div>
            </div>
            
            <div class="overfitting-details">
                <h3>过拟合检测详情</h3>
                <ul>
                    {overfitting_details_html}
                </ul>
            </div>
        </div>
        """
        return html
    
    def _get_css(self) -> str:
        """获取CSS样式"""
        return """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: #1e1e1e;
                color: #e0e0e0;
                line-height: 1.6;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: #252526;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            
            header {
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #3e3e42;
                padding-bottom: 20px;
            }
            
            h1 {
                color: #4ec9b0;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #858585;
                font-size: 0.9em;
            }
            
            .tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #3e3e42;
            }
            
            .tab-button {
                background: #2d2d30;
                border: none;
                color: #cccccc;
                padding: 12px 24px;
                cursor: pointer;
                border-radius: 4px 4px 0 0;
                font-size: 1em;
                transition: all 0.3s;
            }
            
            .tab-button:hover {
                background: #3e3e42;
            }
            
            .tab-button.active {
                background: #007acc;
                color: white;
            }
            
            .tab-content {
                display: none;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .metric-card {
                background: #2d2d30;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #3e3e42;
            }
            
            .metric-label {
                color: #858585;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            
            .metric-value {
                color: #4ec9b0;
                font-size: 2em;
                font-weight: bold;
            }
            
            .risk-low { color: #2ca02c; }
            .risk-medium { color: #ff7f0e; }
            .risk-high { color: #d62728; }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: #2d2d30;
            }
            
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #3e3e42;
            }
            
            th {
                background: #1e1e1e;
                color: #4ec9b0;
                font-weight: bold;
            }
            
            tr:hover {
                background: #3e3e42;
            }
            
            .positive { color: #2ca02c; }
            .negative { color: #d62728; }
            
            footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #3e3e42;
                color: #858585;
            }
        </style>
        """
    
    def _get_javascript(self) -> str:
        """获取JavaScript代码"""
        return """
        <script>
            function showTab(tabName) {
                // 隐藏所有tab内容
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(content => {
                    content.classList.remove('active');
                });
                
                // 移除所有按钮的active类
                const buttons = document.querySelectorAll('.tab-button');
                buttons.forEach(button => {
                    button.classList.remove('active');
                });
                
                // 显示选中的tab
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }
        </script>
        """


# 导入必要的常量
from .validated_factor_calculator import VALIDATED_FACTORS, ALL_VALIDATED_FACTORS
