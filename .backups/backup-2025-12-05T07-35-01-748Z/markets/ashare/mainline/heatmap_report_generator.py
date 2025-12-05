"""
热度评分报告生成器

生成专业的热度评分HTML报告，包括：
1. 方法论说明
2. 数据源状态
3. 主线热度排名
4. 热度因子分解
5. 应用建议
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class HeatmapReportGenerator:
    """热度评分报告生成器"""
    
    def __init__(self, output_dir: Optional[str] = None):
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path.home() / ".local/share/trquant/reports/heatmap"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_report(
        self,
        scores: List,
        raw_data: Dict = None,
    ) -> str:
        """
        生成HTML报告
        
        Args:
            scores: 热度评分列表（IntegratedHeatScore对象）
            raw_data: 原始数据（用于显示数据源状态）
        
        Returns:
            报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"heatmap_report_{timestamp}.html"
        filepath = self.output_dir / filename
        
        html_content = self._build_html(scores, raw_data or {})
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        logger.info(f"热度评分报告已生成: {filepath}")
        return str(filepath)
    
    def _build_html(self, scores: List, raw_data: Dict) -> str:
        """构建HTML内容"""
        
        now = datetime.now()
        
        # 统计信息
        total = len(scores)
        extreme_hot = sum(1 for s in scores if s.total_score >= 80)
        high_hot = sum(1 for s in scores if 60 <= s.total_score < 80)
        medium = sum(1 for s in scores if 40 <= s.total_score < 60)
        low = sum(1 for s in scores if s.total_score < 40)
        
        # 数据源状态
        data_source_rows = ""
        sources = [
            ("sector", "🏭 行业板块", "同花顺API"),
            ("concept", "💡 概念板块", "同花顺API"),
            ("limit_up", "📈 涨停池", "东方财富API"),
            ("lhb", "🐉 龙虎榜", "东方财富API"),
        ]
        for key, name, api in sources:
            data = raw_data.get(key, {})
            source = data.get("source", "未获取")
            count = data.get("count", 0)
            status = "✅" if count > 0 else "⚠️"
            data_source_rows += f"""
            <tr>
                <td>{name}</td>
                <td>{api}</td>
                <td>{source}</td>
                <td>{count}条</td>
                <td>{status}</td>
            </tr>
            """
        
        # 排名表格
        ranking_rows = ""
        for score in scores[:30]:  # Top 30
            score_color = self._get_score_color(score.total_score)
            type_text = "行业" if score.type == "industry" else "概念"
            
            ranking_rows += f"""
            <tr>
                <td class="rank">{score.rank}</td>
                <td class="name">{score.name}</td>
                <td class="type">{type_text}</td>
                <td class="score" style="color: {score_color}; font-weight: bold;">{score.total_score:.1f}</td>
                <td>{score.change_score:.0f}</td>
                <td>{score.flow_score:.0f}</td>
                <td>{score.limit_up_score:.0f}</td>
                <td>{score.lhb_score:.0f}</td>
                <td>{score.leader_score:.0f}</td>
                <td style="color: {score.level_color};">{score.level}</td>
            </tr>
            """
        
        # 热门主线详情
        hot_details = ""
        for score in scores[:5]:
            breakdown = score.get_factor_breakdown() if hasattr(score, 'get_factor_breakdown') else []
            factors_html = ""
            for f in breakdown:
                factors_html += f"""
                <div class="factor-item">
                    <span class="factor-name">{f['name']}</span>
                    <span class="factor-score">{f['score']:.0f}分</span>
                    <span class="factor-raw">({f['raw_value']})</span>
                </div>
                """
            
            hot_details += f"""
            <div class="hot-card">
                <div class="hot-header">
                    <span class="hot-rank">#{score.rank}</span>
                    <span class="hot-name">{score.name}</span>
                    <span class="hot-score" style="color: {score.level_color};">{score.total_score:.1f}分</span>
                    <span class="hot-level" style="background-color: {score.level_color}20; color: {score.level_color};">{score.level}</span>
                </div>
                <div class="hot-factors">
                    {factors_html}
                </div>
                <div class="hot-data">
                    <span>涨幅: {score.change_pct:+.2f}%</span>
                    <span>资金: {score.net_inflow:+.2f}亿</span>
                    <span>龙头: {score.leader_stock} {score.leader_change:+.2f}%</span>
                </div>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>热度评分报告 - {now.strftime("%Y-%m-%d %H:%M")}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 24px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        /* Header */
        .header {{
            text-align: center;
            padding: 32px 0;
            border-bottom: 1px solid #374151;
            margin-bottom: 24px;
        }}
        .header h1 {{
            font-size: 28px;
            color: #f59e0b;
            margin-bottom: 8px;
        }}
        .header .time {{ color: #9ca3af; font-size: 14px; }}
        
        /* Cards */
        .card {{
            background: #1f2937;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #374151;
        }}
        .card-title {{
            font-size: 16px;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #374151;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: #111827;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #f59e0b;
        }}
        .stat-label {{
            font-size: 12px;
            color: #9ca3af;
            margin-top: 4px;
        }}
        
        /* Methodology */
        .methodology {{
            background: #111827;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .formula {{
            background: #1f2937;
            padding: 12px;
            border-radius: 6px;
            font-family: monospace;
            color: #f59e0b;
            margin-top: 12px;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px 8px;
            text-align: left;
            border-bottom: 1px solid #374151;
        }}
        th {{
            background: #111827;
            color: #9ca3af;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
        }}
        tr:hover {{ background: #374151; }}
        .rank {{ font-weight: bold; color: #f59e0b; }}
        .name {{ font-weight: 500; }}
        .type {{ color: #9ca3af; font-size: 12px; }}
        .score {{ font-size: 16px; }}
        
        /* Hot Details */
        .hot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }}
        .hot-card {{
            background: #111827;
            border-radius: 8px;
            padding: 16px;
        }}
        .hot-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .hot-rank {{
            color: #f59e0b;
            font-weight: bold;
        }}
        .hot-name {{
            font-weight: 600;
            flex: 1;
        }}
        .hot-score {{
            font-size: 18px;
            font-weight: bold;
        }}
        .hot-level {{
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
        }}
        .hot-factors {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .factor-item {{
            background: #1f2937;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
        }}
        .factor-name {{ color: #9ca3af; }}
        .factor-score {{ color: #f59e0b; margin-left: 4px; }}
        .factor-raw {{ color: #6b7280; }}
        .hot-data {{
            display: flex;
            gap: 16px;
            color: #9ca3af;
            font-size: 12px;
        }}
        
        /* Application */
        .level-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
        }}
        .level-card {{
            text-align: center;
            padding: 12px;
            border-radius: 8px;
        }}
        .level-card h4 {{ font-size: 14px; margin-bottom: 4px; }}
        .level-card p {{ font-size: 11px; opacity: 0.8; }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 24px 0;
            color: #6b7280;
            font-size: 12px;
            border-top: 1px solid #374151;
            margin-top: 24px;
        }}
        
        /* Flow Position */
        .flow-position {{
            display: flex;
            justify-content: center;
            gap: 16px;
            padding: 16px;
            background: #111827;
            border-radius: 8px;
            margin-bottom: 16px;
        }}
        .flow-step {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
        }}
        .flow-step.active {{
            background: #f59e0b20;
            color: #f59e0b;
            font-weight: bold;
        }}
        .flow-step.inactive {{ color: #6b7280; }}
        .flow-arrow {{ color: #6b7280; align-self: center; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 热度评分报告</h1>
            <p class="time">生成时间: {now.strftime("%Y年%m月%d日 %H:%M:%S")}</p>
        </div>
        
        <!-- 流程位置 -->
        <div class="card">
            <div class="card-title">📍 在主线识别流程中的位置</div>
            <div class="flow-position">
                <span class="flow-step inactive">1️⃣ 主线识别</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step active">2️⃣ 热度评分 ← 当前</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step inactive">3️⃣ 个股筛选</span>
                <span class="flow-arrow">→</span>
                <span class="flow-step inactive">4️⃣ 回测验证</span>
            </div>
            <p style="text-align: center; color: #9ca3af; font-size: 12px;">
                热度评分用于量化主线的市场关注度，辅助判断主线持续性，与主线识别的评分可加权融合
            </p>
        </div>
        
        <!-- 统计概览 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total}</div>
                <div class="stat-label">主线总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #ef4444;">{extreme_hot}</div>
                <div class="stat-label">极热 (≥80分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #f97316;">{high_hot}</div>
                <div class="stat-label">高热 (60-80分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #eab308;">{medium}</div>
                <div class="stat-label">中等 (40-60分)</div>
            </div>
        </div>
        
        <!-- 方法论说明 -->
        <div class="card">
            <div class="card-title">📖 评分方法论 (5因子模型)</div>
            <div class="methodology">
                <table>
                    <tr>
                        <th>因子</th>
                        <th>权重</th>
                        <th>数据来源</th>
                        <th>计算方法</th>
                    </tr>
                    <tr>
                        <td>📈 涨跌幅强度</td>
                        <td>25%</td>
                        <td>同花顺API</td>
                        <td>涨跌幅排名百分位×100</td>
                    </tr>
                    <tr>
                        <td>💰 资金流入强度</td>
                        <td>25%</td>
                        <td>同花顺API</td>
                        <td>净流入排名百分位×100</td>
                    </tr>
                    <tr>
                        <td>🔥 涨停板数量</td>
                        <td>20%</td>
                        <td>东方财富API</td>
                        <td>板块涨停数/全市场涨停数×100</td>
                    </tr>
                    <tr>
                        <td>📊 龙虎榜活跃度</td>
                        <td>15%</td>
                        <td>东方财富API</td>
                        <td>板块龙虎榜数/全市场×100</td>
                    </tr>
                    <tr>
                        <td>👑 龙头股强度</td>
                        <td>15%</td>
                        <td>同花顺API</td>
                        <td>领涨股涨幅排名百分位×100</td>
                    </tr>
                </table>
                <div class="formula">
                    热度得分 = 涨跌幅强度×25% + 资金流入×25% + 涨停数×20% + 龙虎榜×15% + 龙头强度×15%
                </div>
            </div>
        </div>
        
        <!-- 数据源状态 -->
        <div class="card">
            <div class="card-title">📡 数据源状态</div>
            <table>
                <tr>
                    <th>数据类型</th>
                    <th>API接口</th>
                    <th>实际来源</th>
                    <th>数据量</th>
                    <th>状态</th>
                </tr>
                {data_source_rows}
            </table>
        </div>
        
        <!-- 热门主线详情 -->
        <div class="card">
            <div class="card-title">🔥 热门主线详情 (Top 5)</div>
            <div class="hot-grid">
                {hot_details}
            </div>
        </div>
        
        <!-- 热度排名 -->
        <div class="card">
            <div class="card-title">🏆 热度排名 (Top 30)</div>
            <table>
                <tr>
                    <th>排名</th>
                    <th>主线名称</th>
                    <th>类型</th>
                    <th>热度得分</th>
                    <th>涨幅</th>
                    <th>资金</th>
                    <th>涨停</th>
                    <th>龙虎</th>
                    <th>龙头</th>
                    <th>等级</th>
                </tr>
                {ranking_rows}
            </table>
        </div>
        
        <!-- 应用说明 -->
        <div class="card">
            <div class="card-title">💡 如何应用热度评分</div>
            <div class="level-grid">
                <div class="level-card" style="background: #ef444420;">
                    <h4 style="color: #ef4444;">🔥 极热 (≥80)</h4>
                    <p>市场焦点，注意过热风险</p>
                </div>
                <div class="level-card" style="background: #f9731620;">
                    <h4 style="color: #f97316;">📈 高热 (60-80)</h4>
                    <p>积极跟踪，择机参与</p>
                </div>
                <div class="level-card" style="background: #eab30820;">
                    <h4 style="color: #eab308;">➡️ 中等 (40-60)</h4>
                    <p>保持观察，等待催化</p>
                </div>
                <div class="level-card" style="background: #22c55e20;">
                    <h4 style="color: #22c55e;">❄️ 偏冷 (20-40)</h4>
                    <p>关注预期差，左侧布局</p>
                </div>
                <div class="level-card" style="background: #6b728020;">
                    <h4 style="color: #6b7280;">💤 冷门 (<20)</h4>
                    <p>暂不参与</p>
                </div>
            </div>
            <div style="margin-top: 16px; padding: 12px; background: #f59e0b10; border-radius: 6px; border-left: 3px solid #f59e0b;">
                <p style="color: #f59e0b; font-size: 13px;">
                    📌 与主线识别的衔接：建议综合评分 = 热度30% + 资金25% + 趋势25% + 政策20%
                </p>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>韬睿量化 - 热度评分系统</p>
            <p>报告生成时间: {now.strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _get_score_color(self, score: float) -> str:
        """获取得分颜色"""
        if score >= 80:
            return "#ef4444"
        elif score >= 60:
            return "#f97316"
        elif score >= 40:
            return "#eab308"
        elif score >= 20:
            return "#22c55e"
        else:
            return "#6b7280"
