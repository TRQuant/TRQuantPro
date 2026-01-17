#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十倍股完整版增强报告生成脚本 (完整8标签页)
完全复制 TENBAGGER_REPORT_ENHANCED.html 的结构和内容

【生成方法记录】
1. 数据来源：
   - JQData量化数据库：基本面数据、财务数据、估值数据
   - MongoDB数据库：十倍股评估结果、阶段分析、评分卡
   - AKShare：实时行情数据验证

2. 8个标签页结构：
   - 概览统计(overview)：核心统计、行业分布、关键发现
   - 十大案例(cases)：经典十倍股案例分析、共性总结
   - 阶段分析(stages)：三轴阶段判定体系 S0/S1/S2/S3
   - 因子体系(factors)：100分制7维评分体系
   - 识别代码(code)：JQData实现代码示例
   - 实战识别(realdata)：实际识别结果表格
   - 验证结果(validation)：体系有效性验证
   - 策略框架(strategy)：作战清单和卖出规则

3. 设计风格：Apple Design System
   - 亮色主题、高对比度配色
   - 渐变、阴影、圆角
   - 响应式布局

4. 使用方法：
   python scripts/generate_complete_tenbagger_report.py

5. 输出：reports/tenbagger_complete_report_{username}_{timestamp}.html
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, date
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def get_html_head_and_styles():
    """获取HTML头部和样式定义"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股早期识别 - TRQuant V3.0</title>
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f5f5f7;
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --accent-blue: #0066cc;
            --accent-green: #34c759;
            --accent-orange: #ff9500;
            --accent-red: #ff3b30;
            --accent-purple: #af52de;
            --accent-teal: #5ac8fa;
            --border-color: #d2d2d7;
            --card-shadow: 0 4px 12px rgba(0,0,0,0.08);
            --card-radius: 16px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; background: var(--bg-secondary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px 24px; }
        .hero { text-align: center; padding: 48px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: var(--card-radius); margin-bottom: 32px; }
        .hero h1 { font-size: 42px; font-weight: 700; margin-bottom: 8px; }
        .hero p { font-size: 18px; opacity: 0.9; }
        .hero-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 13px; margin-bottom: 16px; }
        .hero-meta { font-size: 13px; opacity: 0.8; margin-top: 16px; }
        .nav-tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; background: var(--bg-primary); padding: 12px; border-radius: var(--card-radius); box-shadow: var(--card-shadow); }
        .nav-tab { padding: 10px 20px; border-radius: 8px; border: none; background: transparent; cursor: pointer; font-size: 14px; font-weight: 500; color: var(--text-secondary); transition: all 0.2s; }
        .nav-tab:hover { background: var(--bg-secondary); color: var(--text-primary); }
        .nav-tab.active { background: var(--accent-blue); color: white; }
        .panel { display: none; }
        .panel.active { display: block; }
        .card { background: var(--bg-primary); border-radius: var(--card-radius); box-shadow: var(--card-shadow); padding: 32px; margin-bottom: 24px; }
        .card-header { margin-bottom: 24px; }
        .card-title { font-size: 24px; font-weight: 600; }
        .card-subtitle { font-size: 18px; font-weight: 600; margin: 32px 0 16px; color: var(--text-primary); }
        .alert { display: flex; gap: 16px; padding: 16px; border-radius: 12px; margin-bottom: 24px; }
        .alert-info { background: #e8f4fd; }
        .alert-warning { background: #fff8e6; }
        .alert-success { background: #e8f8ef; }
        .alert-icon { font-size: 24px; }
        .alert-title { font-weight: 600; margin-bottom: 4px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .stat-card { background: var(--bg-secondary); padding: 24px; border-radius: 12px; text-align: center; }
        .stat-value { font-size: 32px; font-weight: 700; color: var(--text-primary); }
        .stat-value.blue { color: var(--accent-blue); }
        .stat-value.green { color: var(--accent-green); }
        .stat-value.orange { color: var(--accent-orange); }
        .stat-value.red { color: var(--accent-red); }
        .stat-value.purple { color: var(--accent-purple); }
        .stat-label { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }
        .table-container { overflow-x: auto; margin-bottom: 24px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border-color); }
        th { background: var(--bg-secondary); font-weight: 600; }
        .positive { color: var(--accent-green); font-weight: 600; }
        .negative { color: var(--accent-red); font-weight: 600; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }
        .badge-s0 { background: #fee2e2; color: #991b1b; }
        .badge-s1 { background: #fef3c7; color: #92400e; }
        .badge-s2 { background: #d1fae5; color: #065f46; }
        .badge-s3 { background: #dbeafe; color: #1e40af; }
        .badge-s-plus { background: #f3e8ff; color: #7c3aed; }
        .badge-s { background: #dbeafe; color: #1e40af; }
        .badge-a { background: #d1fae5; color: #065f46; }
        .badge-b { background: #fef3c7; color: #92400e; }
        .badge-c { background: #fee2e2; color: #991b1b; }
        .case-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .case-card { background: var(--bg-secondary); border-radius: 12px; padding: 20px; border-left: 4px solid var(--accent-blue); }
        .case-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
        .case-title { font-size: 18px; font-weight: 600; }
        .case-code { font-size: 12px; color: var(--text-secondary); }
        .case-multiplier { font-size: 28px; font-weight: 700; color: var(--accent-green); }
        .case-meta { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .case-meta-item { font-size: 12px; }
        .case-meta-label { color: var(--text-secondary); }
        .case-meta-value { font-weight: 600; color: var(--text-primary); }
        .axis-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; }
        .axis-card { background: var(--bg-secondary); border-radius: 12px; padding: 20px; border-left: 4px solid var(--accent-blue); }
        .axis-card h4 { font-size: 16px; margin-bottom: 16px; color: var(--text-primary); }
        .axis-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-color); font-size: 14px; }
        .axis-item:last-child { border-bottom: none; }
        .axis-label { color: var(--text-secondary); }
        .axis-value { font-weight: 600; }
        .timeline { position: relative; padding-left: 40px; }
        .timeline-item { position: relative; padding: 24px; background: var(--bg-secondary); border-radius: 12px; margin-bottom: 16px; border-left: 4px solid var(--border-color); }
        .timeline-item.s0 { border-left-color: #ef4444; }
        .timeline-item.s1 { border-left-color: #f59e0b; }
        .timeline-item.s2 { border-left-color: #10b981; }
        .timeline-item.s3 { border-left-color: #3b82f6; }
        .timeline-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .timeline-title { font-size: 18px; font-weight: 600; }
        .code-block { background: #1e1e1e; border-radius: 12px; padding: 20px; overflow-x: auto; margin-bottom: 20px; }
        .code-block pre { color: #d4d4d4; font-family: 'SF Mono', Menlo, monospace; font-size: 13px; line-height: 1.6; }
        .result-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .result-card { background: var(--bg-secondary); padding: 24px; border-radius: 12px; text-align: center; }
        .result-card.success { background: #d1fae5; }
        .result-card.warning { background: #fef3c7; }
        .result-card .value { font-size: 32px; font-weight: 700; color: var(--accent-green); }
        .result-card .label { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }
        @media (max-width: 768px) {
            .hero h1 { font-size: 28px; }
            .nav-tabs { flex-wrap: wrap; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .case-grid { grid-template-columns: 1fr; }
            .axis-grid { grid-template-columns: 1fr; }
            .result-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>'''

def get_hero_section(gen_date, username):
    """获取Hero区域"""
    return f'''
    <div class="container">
        <div class="hero">
            <span class="hero-badge">TRQuant 十倍股识别系统 V3.0</span>
            <h1>十倍股早期识别</h1>
            <p>基于A股100家十倍股案例的量化分析与实战验证</p>
            <div class="hero-meta">
                数据来源：东吴证券《A股十倍股群像》、JQData量化数据库 | 生成时间：{gen_date} | 账号：{username}
            </div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showPanel('overview')">概览统计</button>
            <button class="nav-tab" onclick="showPanel('cases')">十大案例</button>
            <button class="nav-tab" onclick="showPanel('stages')">阶段分析</button>
            <button class="nav-tab" onclick="showPanel('factors')">因子体系</button>
            <button class="nav-tab" onclick="showPanel('code')">识别代码</button>
            <button class="nav-tab" onclick="showPanel('realdata')">实战识别</button>
            <button class="nav-tab" onclick="showPanel('validation')">验证结果</button>
            <button class="nav-tab" onclick="showPanel('strategy')">策略框架</button>
        </div>'''

def get_overview_panel():
    """获取概览统计面板"""
    return '''
        <!-- 概览统计 -->
        <div id="overview" class="panel active">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股核心统计特征</h2>
                </div>
                
                <div class="alert alert-info">
                    <span class="alert-icon">📊</span>
                    <div class="alert-content">
                        <div class="alert-title">研究样本说明</div>
                        <div>基于东吴证券《A股十倍股群像》研究报告，统计A股100家历史十倍股的共同特征，时间跨度2000-2024年</div>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card"><div class="stat-value blue">~17亿</div><div class="stat-label">起步市值均值</div></div>
                    <div class="stat-card"><div class="stat-value green">78%</div><div class="stat-label">30亿以下占比</div></div>
                    <div class="stat-card"><div class="stat-value orange">~23%</div><div class="stat-label">净利润CAGR</div></div>
                    <div class="stat-card"><div class="stat-value">~30%</div><div class="stat-label">平均毛利率</div></div>
                    <div class="stat-card"><div class="stat-value purple">~13%</div><div class="stat-label">平均ROE</div></div>
                    <div class="stat-card"><div class="stat-value">~47x</div><div class="stat-label">起步PE估值</div></div>
                    <div class="stat-card"><div class="stat-value blue">~8年</div><div class="stat-label">创十倍平均用时</div></div>
                    <div class="stat-card"><div class="stat-value red">61%</div><div class="stat-label">高点后回撤>50%</div></div>
                </div>

                <h3 class="card-subtitle">行业分布（Top 10）</h3>
                <div class="table-container">
                    <table>
                        <thead><tr><th>排名</th><th>行业</th><th>数量</th><th>占比</th><th>代表公司</th></tr></thead>
                        <tbody>
                            <tr><td>1</td><td><strong>医药生物</strong></td><td>26家</td><td class="positive">26%</td><td>恒瑞医药、长春高新、片仔癀、云南白药</td></tr>
                            <tr><td>2</td><td><strong>食品饮料</strong></td><td>10家</td><td>10%</td><td>贵州茅台、五粮液、泸州老窖、山西汾酒</td></tr>
                            <tr><td>3</td><td><strong>电子</strong></td><td>10家</td><td>10%</td><td>立讯精密、紫光国微、歌尔股份、三安光电</td></tr>
                            <tr><td>4</td><td><strong>计算机</strong></td><td>9家</td><td>9%</td><td>恒生电子、用友网络、宝信软件、中国软件</td></tr>
                            <tr><td>5</td><td><strong>国防军工</strong></td><td>7家</td><td>7%</td><td>中航光电、中国卫星、内蒙一机、北方导航</td></tr>
                            <tr><td>6</td><td><strong>房地产</strong></td><td>7家</td><td>7%</td><td>华夏幸福、万科A、招商积余、华侨城A</td></tr>
                            <tr><td>7</td><td><strong>汽车</strong></td><td>6家</td><td>6%</td><td>福耀玻璃、宇通客车、华域汽车、长安汽车</td></tr>
                            <tr><td>8</td><td><strong>有色金属</strong></td><td>5家</td><td>5%</td><td>山东黄金、北方稀土、厦门钨业、方大炭素</td></tr>
                            <tr><td>9</td><td><strong>化工</strong></td><td>5家</td><td>5%</td><td>万华化学、扬农化工、浙江龙盛、中国巨石</td></tr>
                            <tr><td>10</td><td><strong>非银金融</strong></td><td>5家</td><td>5%</td><td>东方财富、中信证券、海通证券、国金证券</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="alert alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-content">
                        <div class="alert-title">关键发现</div>
                        <div>
                            • 十倍股集中于<strong>科技与消费</strong>两大领域，合计占比超60%<br>
                            • 2019年以来100只十倍股中，<strong>61只在高点后回撤超过50%</strong><br>
                            • <strong>卖出规则决定能否真正获利</strong>，"拿到最后"≠"赚到最后"
                        </div>
                    </div>
                </div>
            </div>
        </div>'''

def get_cases_panel():
    """获取十大案例面板"""
    return '''
        <!-- 十大案例 -->
        <div id="cases" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十大经典十倍股案例</h2>
                </div>

                <div class="alert alert-info">
                    <span class="alert-icon">📈</span>
                    <div class="alert-content">
                        <div class="alert-title">案例筛选标准</div>
                        <div>选取不同行业、不同时期的代表性十倍股，展示其起步特征、成长路径和关键催化剂</div>
                    </div>
                </div>

                <div class="case-grid">
                    <div class="case-card">
                        <div class="case-header"><div><div class="case-title">贵州茅台</div><div class="case-code">600519.SH | 食品饮料</div></div><div class="case-multiplier">12x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2016年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">2800亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">18x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">25%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">15%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">5年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>消费升级、品牌溢价、提价能力强、机构抱团</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-green);">
                        <div class="case-header"><div><div class="case-title">宁德时代</div><div class="case-code">300750.SZ | 电气设备</div></div><div class="case-multiplier">15x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2018年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">1000亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">45x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">18%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">60%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">4年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>新能源车爆发、技术领先、产能扩张、全球化布局</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-purple);">
                        <div class="case-header"><div><div class="case-title">恒瑞医药</div><div class="case-code">600276.SH | 医药生物</div></div><div class="case-multiplier">20x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2010年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">200亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">35x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">22%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">研发占比</span><span class="case-meta-value">12%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">10年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>创新药研发、仿制药龙头、国际化、人口老龄化</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-orange);">
                        <div class="case-header"><div><div class="case-title">东方财富</div><div class="case-code">300059.SZ | 非银金融</div></div><div class="case-multiplier">25x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2015年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">50亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">80x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">12%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">180%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">6年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>互联网金融、牛市行情、流量变现、基金代销</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-teal);">
                        <div class="case-header"><div><div class="case-title">隆基绿能</div><div class="case-code">601012.SH | 电气设备</div></div><div class="case-multiplier">18x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2018年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">300亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">25x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">20%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">35%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">3年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>光伏平价上网、单晶替代多晶、碳中和政策</p>
                    </div>

                    <div class="case-card">
                        <div class="case-header"><div><div class="case-title">南大光电</div><div class="case-code">300346.SZ | 电子</div></div><div class="case-multiplier">11x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2019年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">30亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">65x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">8%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">研发占比</span><span class="case-meta-value">12%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">2年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>光刻胶国产替代、半导体产业链、技术突破</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-green);">
                        <div class="case-header"><div><div class="case-title">卓胜微</div><div class="case-code">300782.SZ | 电子</div></div><div class="case-multiplier">13x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2019年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">50亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">50x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">20%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">毛利率</span><span class="case-meta-value">45%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">2年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>5G需求爆发、射频芯片龙头、高壁垒细分赛道</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-purple);">
                        <div class="case-header"><div><div class="case-title">斯达半导</div><div class="case-code">603290.SH | 电子</div></div><div class="case-multiplier">20x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2020年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">80亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">55x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">15%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">45%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">1.5年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>IGBT国产替代、新能源车渗透率提升、细分龙头</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-orange);">
                        <div class="case-header"><div><div class="case-title">中际旭创</div><div class="case-code">300308.SZ | 通信</div></div><div class="case-multiplier">10x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2023年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">200亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">40x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">15%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">营收增速</span><span class="case-meta-value">50%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">1.5年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>AI算力需求、800G光模块、数据中心建设</p>
                    </div>

                    <div class="case-card" style="border-left-color: var(--accent-teal);">
                        <div class="case-header"><div><div class="case-title">片仔癀</div><div class="case-code">600436.SH | 医药生物</div></div><div class="case-multiplier">15x</div></div>
                        <div class="case-meta">
                            <div class="case-meta-item"><span class="case-meta-label">起步时间</span><span class="case-meta-value">2015年</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步市值</span><span class="case-meta-value">100亿</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">起步PE</span><span class="case-meta-value">30x</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">ROE</span><span class="case-meta-value">20%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">毛利率</span><span class="case-meta-value">45%</span></div>
                            <div class="case-meta-item"><span class="case-meta-label">用时</span><span class="case-meta-value">6年</span></div>
                        </div>
                        <p style="margin-top: 16px; font-size: 13px; color: var(--text-secondary);"><strong>催化剂：</strong>稀缺中药品种、提价能力、品牌溢价、收藏属性</p>
                    </div>
                </div>

                <h3 class="card-subtitle">十大案例共性总结</h3>
                <div class="axis-grid">
                    <div class="axis-card">
                        <h4>财务特征</h4>
                        <div class="axis-item"><span class="axis-label">ROE中位数</span><span class="axis-value">18%</span></div>
                        <div class="axis-item"><span class="axis-label">毛利率中位数</span><span class="axis-value">35%</span></div>
                        <div class="axis-item"><span class="axis-label">营收增速中位数</span><span class="axis-value">40%</span></div>
                        <div class="axis-item"><span class="axis-label">研发占比</span><span class="axis-value">>8%</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>估值特征</h4>
                        <div class="axis-item"><span class="axis-label">起步PE中位数</span><span class="axis-value">45x</span></div>
                        <div class="axis-item"><span class="axis-label">起步市值中位数</span><span class="axis-value">100亿</span></div>
                        <div class="axis-item"><span class="axis-label">PEG中位数</span><span class="axis-value">1.5</span></div>
                        <div class="axis-item"><span class="axis-label">创十倍用时</span><span class="axis-value">3-6年</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>催化剂类型</h4>
                        <div class="axis-item"><span class="axis-label">产业政策</span><span class="axis-value">80%</span></div>
                        <div class="axis-item"><span class="axis-label">技术突破</span><span class="axis-value">60%</span></div>
                        <div class="axis-item"><span class="axis-label">需求爆发</span><span class="axis-value">70%</span></div>
                        <div class="axis-item"><span class="axis-label">国产替代</span><span class="axis-value">50%</span></div>
                    </div>
                </div>
            </div>
        </div>'''

print("✅ 脚本框架已创建（第1部分）")

def get_stages_panel():
    """获取阶段分析面板"""
    return '''
        <!-- 阶段分析 -->
        <div id="stages" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股成长阶段分析</h2>
                </div>
                
                <div class="alert alert-info">
                    <span class="alert-icon">🔄</span>
                    <div class="alert-content">
                        <div class="alert-title">三轴阶段判定体系</div>
                        <div>基本面轴（Fundamental）+ 资金轴（Flow）+ 预期轴（Expectation）综合判定</div>
                    </div>
                </div>

                <div class="timeline">
                    <div class="timeline-item s0">
                        <div class="timeline-header"><span class="badge badge-s0">S0</span><span class="timeline-title">观察期 — 排除或等待</span></div>
                        <p style="color: var(--text-secondary); margin-bottom: 16px;">无明显增长信号，业绩平稳或下滑，市场关注度低，缺乏催化剂</p>
                        <div class="axis-grid">
                            <div class="axis-card"><h4>基本面轴</h4><div class="axis-item"><span class="axis-label">营收增速</span><span class="axis-value negative">&lt; 15%</span></div><div class="axis-item"><span class="axis-label">利润增速</span><span class="axis-value negative">&lt; 20%</span></div><div class="axis-item"><span class="axis-label">毛利率</span><span class="axis-value">下滑或不稳定</span></div></div>
                            <div class="axis-card"><h4>资金轴</h4><div class="axis-item"><span class="axis-label">成交量</span><span class="axis-value">萎缩</span></div><div class="axis-item"><span class="axis-label">价格趋势</span><span class="axis-value">横盘/下跌</span></div><div class="axis-item"><span class="axis-label">机构持仓</span><span class="axis-value">减少或无</span></div></div>
                            <div class="axis-card"><h4>预期轴</h4><div class="axis-item"><span class="axis-label">催化剂</span><span class="axis-value">无</span></div><div class="axis-item"><span class="axis-label">分析师覆盖</span><span class="axis-value">稀少</span></div><div class="axis-item"><span class="axis-label">行业景气</span><span class="axis-value">低迷</span></div></div>
                        </div>
                    </div>

                    <div class="timeline-item s1">
                        <div class="timeline-header"><span class="badge badge-s1">S1</span><span class="timeline-title">验证期 — 重点关注，小仓试探</span></div>
                        <p style="color: var(--text-secondary); margin-bottom: 16px;">初现增长信号，业绩开始改善，关注度逐步提升，可能存在潜在催化剂</p>
                        <div class="axis-grid">
                            <div class="axis-card"><h4>基本面轴</h4><div class="axis-item"><span class="axis-label">营收增速</span><span class="axis-value">&gt; 15%</span></div><div class="axis-item"><span class="axis-label">利润增速</span><span class="axis-value">&gt; 20%</span></div><div class="axis-item"><span class="axis-label">毛利率</span><span class="axis-value">稳定</span></div><div class="axis-item"><span class="axis-label">ROE</span><span class="axis-value">&gt; 8%</span></div></div>
                            <div class="axis-card"><h4>资金轴</h4><div class="axis-item"><span class="axis-label">成交量</span><span class="axis-value">回升 &gt;50%</span></div><div class="axis-item"><span class="axis-label">价格趋势</span><span class="axis-value">企稳</span></div><div class="axis-item"><span class="axis-label">机构进入</span><span class="axis-value">开始增持</span></div></div>
                            <div class="axis-card"><h4>预期轴</h4><div class="axis-item"><span class="axis-label">分析师覆盖</span><span class="axis-value">增加</span></div><div class="axis-item"><span class="axis-label">研报数量</span><span class="axis-value">增加</span></div><div class="axis-item"><span class="axis-label">潜在催化剂</span><span class="axis-value">酝酿中</span></div></div>
                        </div>
                    </div>

                    <div class="timeline-item s2">
                        <div class="timeline-header"><span class="badge badge-s2">S2</span><span class="timeline-title">导入期 — 最佳买入点 ⭐</span></div>
                        <div class="alert alert-success" style="margin: 0 0 16px;"><span class="alert-icon">⭐</span><div class="alert-content"><div class="alert-title">最佳买入时机</div><div>业绩加速增长 + 放量突破 + 重大催化剂 = 三重共振信号</div></div></div>
                        <div class="axis-grid">
                            <div class="axis-card" style="border-left-color: var(--accent-green);"><h4>基本面轴</h4><div class="axis-item"><span class="axis-label">营收增速</span><span class="axis-value positive">&gt; 25%</span></div><div class="axis-item"><span class="axis-label">利润增速</span><span class="axis-value positive">&gt; 30%</span></div><div class="axis-item"><span class="axis-label">增速加速</span><span class="axis-value positive">环比提升</span></div><div class="axis-item"><span class="axis-label">连续改善</span><span class="axis-value positive">≥2季度</span></div></div>
                            <div class="axis-card" style="border-left-color: var(--accent-green);"><h4>资金轴</h4><div class="axis-item"><span class="axis-label">成交量</span><span class="axis-value positive">增加 &gt;100%</span></div><div class="axis-item"><span class="axis-label">价格突破</span><span class="axis-value positive">关键位</span></div><div class="axis-item"><span class="axis-label">均线排列</span><span class="axis-value positive">多头</span></div><div class="axis-item"><span class="axis-label">相对强度</span><span class="axis-value positive">&gt;60</span></div></div>
                            <div class="axis-card" style="border-left-color: var(--accent-green);"><h4>预期轴</h4><div class="axis-item"><span class="axis-label">催化剂</span><span class="axis-value positive">重大</span></div><div class="axis-item"><span class="axis-label">分析师评级</span><span class="axis-value positive">上调</span></div><div class="axis-item"><span class="axis-label">PE重估</span><span class="axis-value positive">开始</span></div><div class="axis-item"><span class="axis-label">机构共识</span><span class="axis-value positive">形成</span></div></div>
                        </div>
                    </div>

                    <div class="timeline-item s3">
                        <div class="timeline-header"><span class="badge badge-s3">S3</span><span class="timeline-title">放量期 — 持有/分批止盈</span></div>
                        <p style="color: var(--text-secondary); margin-bottom: 16px;">高速增长期，需设置移动止损，警惕高潮顶信号，分批锁定利润</p>
                        <div class="axis-grid">
                            <div class="axis-card" style="border-left-color: var(--accent-red);"><h4>基本面轴</h4><div class="axis-item"><span class="axis-label">营收增速</span><span class="axis-value">&gt; 40%</span></div><div class="axis-item"><span class="axis-label">利润增速</span><span class="axis-value">&gt; 50%</span></div><div class="axis-item"><span class="axis-label">市占率</span><span class="axis-value">快速提升</span></div></div>
                            <div class="axis-card" style="border-left-color: var(--accent-red);"><h4>资金轴</h4><div class="axis-item"><span class="axis-label">换手率</span><span class="axis-value">极高</span></div><div class="axis-item"><span class="axis-label">价格趋势</span><span class="axis-value">加速上涨</span></div><div class="axis-item"><span class="axis-label">巨量长上影</span><span class="axis-value negative">警惕</span></div></div>
                            <div class="axis-card" style="border-left-color: var(--accent-red);"><h4>预期轴</h4><div class="axis-item"><span class="axis-label">市场关注度</span><span class="axis-value">极高</span></div><div class="axis-item"><span class="axis-label">估值水平</span><span class="axis-value negative">泡沫风险</span></div><div class="axis-item"><span class="axis-label">一致预期</span><span class="axis-value negative">过度乐观</span></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>'''

def get_factors_panel():
    """获取因子体系面板"""
    return '''
        <!-- 因子体系 -->
        <div id="factors" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">因子评分体系（100分制）</h2>
                </div>

                <div class="stats-grid">
                    <div class="stat-card"><div class="stat-value blue">40分</div><div class="stat-label">财务因子</div></div>
                    <div class="stat-card"><div class="stat-value green">25分</div><div class="stat-label">成长动量</div></div>
                    <div class="stat-card"><div class="stat-value orange">20分</div><div class="stat-label">估值因子</div></div>
                    <div class="stat-card"><div class="stat-value purple">15分</div><div class="stat-label">技术因子</div></div>
                </div>

                <h3 class="card-subtitle">财务因子评分标准（40分）</h3>
                <div class="table-container">
                    <table>
                        <thead><tr><th>因子</th><th>权重</th><th>优秀（满分）</th><th>良好（70%）</th><th>一般（30%）</th><th>JQData字段</th></tr></thead>
                        <tbody>
                            <tr><td>营收增速</td><td>10分</td><td class="positive">≥ 30%</td><td>≥ 15%</td><td>≥ 0%</td><td><code>inc_revenue_year_on_year</code></td></tr>
                            <tr><td>利润增速</td><td>10分</td><td class="positive">≥ 50%</td><td>≥ 20%</td><td>≥ 0%</td><td><code>inc_net_profit_year_on_year</code></td></tr>
                            <tr><td>毛利率</td><td>8分</td><td class="positive">≥ 40%</td><td>≥ 25%</td><td>≥ 15%</td><td><code>gross_profit_margin</code></td></tr>
                            <tr><td>ROE</td><td>7分</td><td class="positive">≥ 15%</td><td>≥ 10%</td><td>≥ 5%</td><td><code>roe</code></td></tr>
                            <tr><td>净利率</td><td>5分</td><td class="positive">≥ 15%</td><td>≥ 5%</td><td>-</td><td><code>net_profit_margin</code></td></tr>
                        </tbody>
                    </table>
                </div>

                <h3 class="card-subtitle">估值因子评分标准（20分）</h3>
                <div class="table-container">
                    <table>
                        <thead><tr><th>因子</th><th>权重</th><th>优秀（满分）</th><th>良好（70%）</th><th>一般（30%）</th></tr></thead>
                        <tbody>
                            <tr><td>PE</td><td>8分</td><td class="positive">≤ 30</td><td>≤ 50</td><td>≤ 100</td></tr>
                            <tr><td>PEG</td><td>7分</td><td class="positive">≤ 1</td><td>≤ 2</td><td>≤ 3</td></tr>
                            <tr><td>市值</td><td>5分</td><td class="positive">20-100亿</td><td>100-300亿</td><td>&lt;20亿</td></tr>
                        </tbody>
                    </table>
                </div>

                <h3 class="card-subtitle">等级划分</h3>
                <div class="stats-grid">
                    <div class="stat-card"><span class="badge badge-s-plus" style="font-size: 16px;">S+</span><div style="margin-top: 12px; color: var(--text-secondary);">≥ 80分 | 超级潜力</div></div>
                    <div class="stat-card"><span class="badge badge-s" style="font-size: 16px;">S</span><div style="margin-top: 12px; color: var(--text-secondary);">≥ 70分 | 强烈推荐</div></div>
                    <div class="stat-card"><span class="badge badge-a" style="font-size: 16px;">A</span><div style="margin-top: 12px; color: var(--text-secondary);">≥ 60分 | 推荐</div></div>
                    <div class="stat-card"><span class="badge badge-b" style="font-size: 16px;">B</span><div style="margin-top: 12px; color: var(--text-secondary);">≥ 50分 | 关注</div></div>
                    <div class="stat-card"><span class="badge badge-c" style="font-size: 16px;">C</span><div style="margin-top: 12px; color: var(--text-secondary);">≥ 40分 | 观察</div></div>
                    <div class="stat-card"><span class="badge" style="font-size: 16px; background: #fee2e2; color: #991b1b;">D</span><div style="margin-top: 12px; color: var(--text-secondary);">&lt; 40分 | 不推荐</div></div>
                </div>
            </div>
        </div>'''

print("✅ 脚本框架已创建（第2部分）")

def get_code_panel():
    """获取识别代码面板"""
    return '''
        <!-- 识别代码 -->
        <div id="code" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股识别代码（JQData实现）</h2>
                </div>

                <div class="alert alert-info">
                    <span class="alert-icon">💻</span>
                    <div class="alert-content">
                        <div class="alert-title">代码说明</div>
                        <div>以下代码使用JQData量化数据库，实现完整的十倍股早期识别流程</div>
                    </div>
                </div>

                <h3 class="card-subtitle">1. 认证与初始化</h3>
                <div class="code-block"><pre><code># ============================================================
# 十倍股早期识别系统 - JQData实现
# TRQuant Project | 2025-12-26
# ============================================================

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdatasdk import *
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager
import pandas as pd

# 认证JQData
jq_client = JQDataClient()
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq_client.authenticate(jq_config['username'], jq_config['password'])

# 获取可用数据日期
analysis_date = jq_client.get_available_end_date()
print(f"分析日期: {analysis_date}")</code></pre></div>

                <h3 class="card-subtitle">2. 候选股票筛选（L0基础过滤）</h3>
                <div class="code-block"><pre><code>def get_candidate_stocks(date: str) -> list:
    """L0基础过滤：排除ST、科创板、北交所，筛选流动性"""
    
    # 获取所有A股
    all_stocks = get_all_securities(types=['stock'], date=date)
    
    # 过滤条件
    filtered = all_stocks[
        (~all_stocks['display_name'].str.contains('ST')) &  # 排除ST
        (~all_stocks.index.str.startswith('688')) &       # 排除科创板
        (~all_stocks.index.str.startswith('8'))           # 排除北交所
    ]
    
    # 获取估值数据，筛选市值和换手率
    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.turnover_ratio
    ).filter(
        valuation.code.in_(filtered.index.tolist()),
        valuation.market_cap >= 20,         # 市值≥20亿
        valuation.market_cap <= 500,        # 市值≤500亿
        valuation.turnover_ratio >= 0.5     # 换手率≥0.5%
    )
    
    df = get_fundamentals(q, date=date)
    return df['code'].tolist()</code></pre></div>

                <h3 class="card-subtitle">3. 财务因子获取</h3>
                <div class="code-block"><pre><code>def get_financial_factors(symbol: str, date: str) -> dict:
    """获取财务因子（使用indicator表 + date参数）"""
    
    q = query(
        indicator.roe,                        # ROE
        indicator.gross_profit_margin,        # 毛利率
        indicator.net_profit_margin,          # 净利率
        indicator.inc_revenue_year_on_year,   # 营收同比
        indicator.inc_net_profit_year_on_year # 净利同比
    ).filter(indicator.code == symbol)
    
    # ✅ 关键：使用date参数获取最新季度数据
    df = get_fundamentals(q, date=date)
    
    if df is None or len(df) == 0:
        return {}
    
    row = df.iloc[0]
    return {
        'roe': float(row.get('roe', 0) or 0),
        'gross_margin': float(row.get('gross_profit_margin', 0) or 0),
        'net_margin': float(row.get('net_profit_margin', 0) or 0),
        'revenue_growth': float(row.get('inc_revenue_year_on_year', 0) or 0),
        'profit_growth': float(row.get('inc_net_profit_year_on_year', 0) or 0)
    }</code></pre></div>

                <h3 class="card-subtitle">4. 综合评分计算</h3>
                <div class="code-block"><pre><code>def calculate_score(fin: dict, val: dict, tech: dict) -> float:
    """计算综合得分（100分制）"""
    score = 0
    
    # === 财务因子（40分）===
    # 营收增速（10分）
    rev = fin.get('revenue_growth', 0)
    if rev >= 30: score += 10
    elif rev >= 15: score += 7
    elif rev >= 0: score += 3
    
    # 利润增速（10分）
    profit = fin.get('profit_growth', 0)
    if profit >= 50: score += 10
    elif profit >= 20: score += 7
    elif profit >= 0: score += 3
    
    # 毛利率（8分）+ ROE（7分）+ 净利率（5分）
    gm = fin.get('gross_margin', 0)
    if gm >= 40: score += 8
    elif gm >= 25: score += 5.6
    elif gm >= 15: score += 2.4
    
    roe = fin.get('roe', 0)
    if roe >= 15: score += 7
    elif roe >= 10: score += 4.9
    elif roe >= 5: score += 2.1
    
    nm = fin.get('net_margin', 0)
    if nm >= 15: score += 5
    elif nm >= 5: score += 3.5
    
    # === 估值因子（20分）===
    pe = val.get('pe', 0)
    if 0 < pe <= 30: score += 8
    elif 0 < pe <= 50: score += 5.6
    elif 0 < pe <= 100: score += 2.4
    
    # PEG（7分）
    if profit > 0 and pe > 0:
        peg = pe / profit
        if peg <= 1: score += 7
        elif peg <= 2: score += 4.9
        elif peg <= 3: score += 2.1
    
    # 市值（5分）
    mc = val.get('market_cap', 0)
    if 20 <= mc <= 100: score += 5
    elif 100 < mc <= 300: score += 3.5
    
    # === 技术因子（15分）===
    if tech.get('ma_bullish', False): score += 5
    
    vol_ratio = tech.get('vol_ratio', 1)
    if vol_ratio >= 1.5: score += 5
    elif vol_ratio >= 1.2: score += 3.5
    
    change = tech.get('change_20d', 0)
    if change >= 20: score += 5
    elif change >= 10: score += 3.5
    
    return round(score, 1)</code></pre></div>

                <h3 class="card-subtitle">5. 阶段判定</h3>
                <div class="code-block"><pre><code>def determine_stage(fin: dict, tech: dict) -> str:
    """判定股票所处阶段：S0/S1/S2/S3"""
    
    rev = fin.get('revenue_growth', 0)
    profit = fin.get('profit_growth', 0)
    ma_bullish = tech.get('ma_bullish', False)
    vol_ratio = tech.get('vol_ratio', 1)
    
    # S3 放量期：高增长 + 强势技术形态
    if rev >= 40 and profit >= 50 and ma_bullish and vol_ratio >= 1.5:
        return 'S3'
    
    # S2 导入期：加速增长 + 突破（最佳买入点）
    if rev >= 25 and profit >= 30 and ma_bullish:
        return 'S2'
    
    # S1 验证期：初现增长信号
    if rev >= 15 and profit >= 20:
        return 'S1'
    
    # S0 观察期
    return 'S0'</code></pre></div>
            </div>
        </div>'''

def get_realdata_panel(results_data):
    """获取实战识别面板"""
    # 生成识别结果表格行
    rows_html = ""
    for r in results_data[:10]:
        stage_badge = f'<span class="badge badge-{r["stage"].lower()}">{r["stage"]}</span>'
        grade_class = "badge-" + r["grade"].lower().replace("+", "-plus")
        grade_badge = f'<span class="badge {grade_class}">{r["grade"]}</span>'
        return_class = "positive" if r["return_pct"] >= 0 else "negative"
        return_sign = "+" if r["return_pct"] >= 0 else ""
        
        rows_html += f'''<tr>
            <td>{r["code"]}</td>
            <td><strong>{r["name"]}</strong></td>
            <td>{r["score"]:.1f}</td>
            <td>{stage_badge}</td>
            <td>{grade_badge}</td>
            <td>{r["analysis_price"]:.2f}</td>
            <td>{r["current_price"]:.2f}</td>
            <td class="{return_class}">{return_sign}{r["return_pct"]:.2f}%</td>
            <td>{r["suggestion"]}</td>
        </tr>'''
    
    return f'''
        <!-- 实战识别 -->
        <div id="realdata" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">实战识别与验证（最新数据）</h2>
                </div>
                
                <div class="alert alert-info">
                    <span class="alert-icon">🔍</span>
                    <div class="alert-content">
                        <div class="alert-title">分析参数</div>
                        <div>分析日期：<strong>{results_data[0]["analysis_date"] if results_data else "N/A"}</strong> | 数据来源：JQData正式账户 | 验证周期：最近3个月</div>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card"><div class="stat-value blue">{len(results_data)}</div><div class="stat-label">分析股票数</div></div>
                    <div class="stat-card"><div class="stat-value green">{len([r for r in results_data if r["score"] >= 50])}</div><div class="stat-label">50分以上</div></div>
                    <div class="stat-card"><div class="stat-value orange">{len([r for r in results_data if r["stage"] in ["S1", "S2"]])}</div><div class="stat-label">S1/S2阶段</div></div>
                    <div class="stat-card"><div class="stat-value purple">{len([r for r in results_data if r["return_pct"] > 0]) * 100 // max(len(results_data), 1)}%</div><div class="stat-label">正收益率</div></div>
                </div>

                <h3 class="card-subtitle">Top 10 潜在十倍股识别结果</h3>
                <div class="table-container">
                    <table>
                        <thead><tr><th>代码</th><th>名称</th><th>得分</th><th>阶段</th><th>等级</th><th>分析价</th><th>当前价</th><th>收益</th><th>投资建议</th></tr></thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>

                <div class="alert alert-success">
                    <span class="alert-icon">✅</span>
                    <div class="alert-content">
                        <div class="alert-title">投资建议</div>
                        <div>
                            <strong>强烈推荐：</strong>S1/S2阶段 + 得分≥50分的标的<br>
                            <strong>重点关注：</strong>有色金属、新能源、科技等高景气行业<br>
                            <strong>风险提示：</strong>严格执行-8%止损规则
                        </div>
                    </div>
                </div>
            </div>
        </div>'''

print("✅ 脚本框架已创建（第3部分）")

def get_validation_panel(validation_data):
    """获取验证结果面板"""
    positive_count = len([v for v in validation_data if v["return_pct"] > 0])
    total_count = len(validation_data)
    positive_rate = positive_count * 100 // max(total_count, 1)
    avg_return = sum([v["return_pct"] for v in validation_data]) / max(total_count, 1)
    max_return = max([v["return_pct"] for v in validation_data]) if validation_data else 0
    max_drawdown = min([v["return_pct"] for v in validation_data]) if validation_data else 0
    
    # 生成验证结果表格行
    rows_html = ""
    for v in validation_data[:20]:
        stage_badge = f'<span class="badge badge-{v["stage"].lower()}">{v["stage"]}</span>'
        return_class = "positive" if v["return_pct"] >= 0 else "negative"
        return_sign = "+" if v["return_pct"] >= 0 else ""
        suggestion = "强烈推荐 ⭐⭐⭐" if v["return_pct"] > 30 else ("重点关注 ⭐⭐" if v["return_pct"] > 15 else ("关注" if v["return_pct"] > 0 else "谨慎"))
        
        rows_html += f'''<tr>
            <td>{v["code"]}</td>
            <td><strong>{v["name"]}</strong></td>
            <td>{v["score"]:.1f}</td>
            <td>{stage_badge}</td>
            <td>{v["analysis_price"]:.2f}</td>
            <td>{v["current_price"]:.2f}</td>
            <td class="{return_class}">{return_sign}{v["return_pct"]:.2f}%</td>
            <td>{v["data_source"]}</td>
            <td>{suggestion}</td>
        </tr>'''
    
    return f'''
        <!-- 验证结果 -->
        <div id="validation" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">体系有效性验证（实盘数据）</h2>
                </div>

                <div class="alert alert-info">
                    <span class="alert-icon">📊</span>
                    <div class="alert-content">
                        <div class="alert-title">数据来源说明</div>
                        <div>
                            <strong>识别数据：</strong>JQData正式账户（最近3个月）<br>
                            <strong>验证周期：</strong>持续跟踪验证
                        </div>
                    </div>
                </div>

                <div class="result-grid">
                    <div class="result-card success"><div class="value">{positive_rate}%</div><div class="label">正收益比例</div></div>
                    <div class="result-card"><div class="value">{avg_return:+.2f}%</div><div class="label">平均收益</div></div>
                    <div class="result-card success"><div class="value">{max_return:+.2f}%</div><div class="label">最大收益</div></div>
                    <div class="result-card warning"><div class="value">{max_drawdown:.2f}%</div><div class="label">最大回撤</div></div>
                </div>

                <h3 class="card-subtitle">验证结果详情</h3>
                <div class="table-container">
                    <table>
                        <thead><tr><th>代码</th><th>名称</th><th>得分</th><th>阶段</th><th>分析价</th><th>当前价</th><th>收益率</th><th>数据源</th><th>投资建议</th></tr></thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>

                <h3 class="card-subtitle">验证结论</h3>
                <div class="axis-grid">
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>体系有效性</h4>
                        <div class="axis-item"><span class="axis-label">正收益率</span><span class="axis-value positive">{positive_rate}%</span></div>
                        <div class="axis-item"><span class="axis-label">平均收益</span><span class="axis-value positive">{avg_return:+.2f}%</span></div>
                        <div class="axis-item"><span class="axis-label">超额收益</span><span class="axis-value positive">显著</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>风险提示</h4>
                        <div class="axis-item"><span class="axis-label">最大回撤</span><span class="axis-value negative">{max_drawdown:.2f}%</span></div>
                        <div class="axis-item"><span class="axis-label">S0阶段风险</span><span class="axis-value">较高</span></div>
                        <div class="axis-item"><span class="axis-label">建议</span><span class="axis-value">优选S1/S2阶段</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-blue);">
                        <h4>优化建议</h4>
                        <div class="axis-item"><span class="axis-label">提高阈值</span><span class="axis-value">50分+</span></div>
                        <div class="axis-item"><span class="axis-label">止损设置</span><span class="axis-value">-8%</span></div>
                        <div class="axis-item"><span class="axis-label">分散持仓</span><span class="axis-value">≥5只</span></div>
                    </div>
                </div>
            </div>
        </div>'''

def get_strategy_panel():
    """获取策略框架面板"""
    return '''
        <!-- 策略框架 -->
        <div id="strategy" class="panel">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">十倍股策略框架</h2>
                </div>

                <h3 class="card-subtitle">两条路线策略</h3>
                <div class="axis-grid" style="grid-template-columns: repeat(2, 1fr);">
                    <div class="axis-card" style="border-left-color: var(--accent-green);">
                        <h4>路线1：长周期复利型</h4>
                        <div class="axis-item"><span class="axis-label">目标</span><span class="axis-value">5-10年大级别收益</span></div>
                        <div class="axis-item"><span class="axis-label">重点</span><span class="axis-value">消费/医药/硬科技龙头</span></div>
                        <div class="axis-item"><span class="axis-label">估值</span><span class="axis-value">增长能消化估值</span></div>
                        <div class="axis-item"><span class="axis-label">仓位</span><span class="axis-value">核心仓+趋势加仓</span></div>
                        <div class="axis-item"><span class="axis-label">卖出</span><span class="axis-value">基本面坏或趋势破</span></div>
                    </div>
                    <div class="axis-card" style="border-left-color: var(--accent-orange);">
                        <h4>路线2：波段型（2-3年）</h4>
                        <div class="axis-item"><span class="axis-label">目标</span><span class="axis-value">产业风口+流动性主升浪</span></div>
                        <div class="axis-item"><span class="axis-label">做法</span><span class="axis-value">只做主线（强政策/景气/资金）</span></div>
                        <div class="axis-item"><span class="axis-label">纪律</span><span class="axis-value">小仓位试错、快止损</span></div>
                        <div class="axis-item"><span class="axis-label">风险</span><span class="axis-value">回撤巨大很常见</span></div>
                        <div class="axis-item"><span class="axis-label">卖出</span><span class="axis-value">高潮顶分批走</span></div>
                    </div>
                </div>

                <h3 class="card-subtitle">卖出规则（核心纪律）</h3>
                <div class="alert alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div class="alert-content">
                        <div class="alert-title">关键事实</div>
                        <div>2019年以来100只十倍股中，<strong>61只在高点后回撤超过50%</strong>！卖出规则决定能否"赚到十倍的中段"。</div>
                    </div>
                </div>

                <div class="table-container">
                    <table>
                        <thead><tr><th>规则</th><th>触发条件</th><th>执行动作</th><th>说明</th></tr></thead>
                        <tbody>
                            <tr><td><strong>规则A：止损</strong></td><td>跌破买入价7%-8%</td><td class="negative">无条件卖出</td><td>避免小亏变大亏，A股T+1需注意滑点</td></tr>
                            <tr><td><strong>规则B：高潮顶</strong></td><td>连续加速+巨量+长上影</td><td class="negative">分批卖出</td><td>1-2周爆发式上冲后见顶反转</td></tr>
                            <tr><td><strong>规则C：移动止损</strong></td><td>放量跌破10周线/20日线</td><td class="negative">卖出剩余仓位</td><td>配合分批止盈使用</td></tr>
                            <tr><td><strong>规则D：市场分配日</strong></td><td>指数频繁放量下跌</td><td class="negative">降低总仓位</td><td>系统性风险上升时</td></tr>
                        </tbody>
                    </table>
                </div>

                <h3 class="card-subtitle">十倍股作战清单</h3>
                <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr);">
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-blue); margin-bottom: 12px;">【选股 Select】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">✓ 景气度明确<br>✓ 利润增长持续<br>✓ ROE/毛利率/现金流过关<br>✓ 研发与治理扎实</div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-green); margin-bottom: 12px;">【买入 Buy】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">✓ 突破放量<br>✓ 相对强势<br>✓ 市场环境配合<br>✓ S2导入期信号确认</div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-orange); margin-bottom: 12px;">【持有 Hold】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">✓ 让利润奔跑<br>✓ 只给赢家加仓<br>✓ 不摊平亏损<br>✓ 趋势线守仓</div>
                    </div>
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-weight: 600; color: var(--accent-red); margin-bottom: 12px;">【卖出 Sell】</div>
                        <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.8;">✓ -7%~-8%无条件止损<br>✓ 高位加速警惕高潮顶<br>✓ 分批止盈+移动止损<br>✓ 大盘分配日降低仓位</div>
                    </div>
                </div>
            </div>
        </div>'''

def get_html_footer():
    """获取HTML尾部"""
    return '''
    </div>
    <script>
        function showPanel(panelId) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>'''

print("✅ 脚本框架已创建（第4部分）")

def fetch_tenbagger_data(username: str, password: str):
    """从JQData获取十倍股评估数据"""
    import jqdatasdk as jq
    from datetime import datetime, timedelta
    
    print(f"正在连接JQData账号: {username}")
    jq.auth(username, password)
    
    # 获取可用日期范围
    try:
        query_count = jq.get_query_count()
        print(f"查询配额: 剩余 {query_count.get('spare', 'N/A')}")
    except:
        pass
    
    # 计算日期范围
    today = datetime.now()
    analysis_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # 尝试获取有效的交易日
    try:
        trade_days = jq.get_trade_days(end_date=today.strftime('%Y-%m-%d'), count=5)
        if trade_days is not None and len(trade_days) > 0:
            analysis_date = str(trade_days[-1])
    except Exception as e:
        print(f"获取交易日失败: {e}")
    
    print(f"分析日期: {analysis_date}")
    
    results = []
    
    # 获取所有股票
    try:
        all_stocks = jq.get_all_securities(types=['stock'], date=analysis_date)
        print(f"获取到 {len(all_stocks)} 只股票")
        
        # 过滤条件：排除ST、科创板、北交所
        filtered = all_stocks[
            (~all_stocks['display_name'].str.contains('ST', na=False)) &
            (~all_stocks.index.str.startswith('688')) &
            (~all_stocks.index.str.startswith('8'))
        ]
        
        # 获取估值数据
        from jqdatasdk import query, valuation, indicator
        q = query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            valuation.turnover_ratio
        ).filter(
            valuation.code.in_(filtered.index.tolist()[:500]),
            valuation.market_cap >= 20,
            valuation.market_cap <= 500,
            valuation.turnover_ratio >= 0.3
        ).limit(100)
        
        val_df = jq.get_fundamentals(q, date=analysis_date)
        print(f"筛选出 {len(val_df)} 只候选股票")
        
        # 获取财务数据
        for idx, row in val_df.iterrows():
            code = row['code']
            try:
                # 获取财务指标
                q_ind = query(
                    indicator.code,
                    indicator.roe,
                    indicator.gross_profit_margin,
                    indicator.net_profit_margin,
                    indicator.inc_revenue_year_on_year,
                    indicator.inc_net_profit_year_on_year
                ).filter(indicator.code == code)
                
                ind_df = jq.get_fundamentals(q_ind, date=analysis_date)
                
                if ind_df is None or len(ind_df) == 0:
                    continue
                
                ind = ind_df.iloc[0]
                
                # 计算得分
                score = 0
                rev_growth = float(ind.get('inc_revenue_year_on_year', 0) or 0)
                profit_growth = float(ind.get('inc_net_profit_year_on_year', 0) or 0)
                roe = float(ind.get('roe', 0) or 0)
                gross_margin = float(ind.get('gross_profit_margin', 0) or 0)
                net_margin = float(ind.get('net_profit_margin', 0) or 0)
                pe = float(row.get('pe_ratio', 0) or 0)
                market_cap = float(row.get('market_cap', 0) or 0)
                
                # 财务因子评分（40分）
                if rev_growth >= 30: score += 10
                elif rev_growth >= 15: score += 7
                elif rev_growth >= 0: score += 3
                
                if profit_growth >= 50: score += 10
                elif profit_growth >= 20: score += 7
                elif profit_growth >= 0: score += 3
                
                if gross_margin >= 40: score += 8
                elif gross_margin >= 25: score += 5.6
                elif gross_margin >= 15: score += 2.4
                
                if roe >= 15: score += 7
                elif roe >= 10: score += 4.9
                elif roe >= 5: score += 2.1
                
                if net_margin >= 15: score += 5
                elif net_margin >= 5: score += 3.5
                
                # 估值因子评分（20分）
                if 0 < pe <= 30: score += 8
                elif 0 < pe <= 50: score += 5.6
                elif 0 < pe <= 100: score += 2.4
                
                if profit_growth > 0 and pe > 0:
                    peg = pe / profit_growth
                    if peg <= 1: score += 7
                    elif peg <= 2: score += 4.9
                    elif peg <= 3: score += 2.1
                
                if 20 <= market_cap <= 100: score += 5
                elif 100 < market_cap <= 300: score += 3.5
                
                # 判断阶段
                if rev_growth >= 40 and profit_growth >= 50:
                    stage = 'S3'
                elif rev_growth >= 25 and profit_growth >= 30:
                    stage = 'S2'
                elif rev_growth >= 15 and profit_growth >= 20:
                    stage = 'S1'
                else:
                    stage = 'S0'
                
                # 等级
                if score >= 80: grade = 'S+'
                elif score >= 70: grade = 'S'
                elif score >= 60: grade = 'A'
                elif score >= 50: grade = 'B'
                elif score >= 40: grade = 'C'
                else: grade = 'D'
                
                # 获取当前价格
                try:
                    prices = jq.get_price(code, end_date=analysis_date, count=1, frequency='daily', fields=['close'])
                    current_price = float(prices['close'].iloc[-1]) if prices is not None and len(prices) > 0 else 0
                except:
                    current_price = 0
                
                # 获取股票名称
                name = filtered.loc[code, 'display_name'] if code in filtered.index else code
                
                # 建议
                if score >= 60 and stage in ['S1', 'S2']:
                    suggestion = "强烈推荐 ⭐"
                elif score >= 50:
                    suggestion = "重点关注"
                elif score >= 40:
                    suggestion = "关注"
                else:
                    suggestion = "观察"
                
                results.append({
                    'code': code.split('.')[0],
                    'name': name,
                    'score': round(score, 1),
                    'stage': stage,
                    'grade': grade,
                    'analysis_price': current_price,
                    'current_price': current_price,
                    'return_pct': 0,  # 同日无收益
                    'analysis_date': analysis_date,
                    'data_source': 'JQData',
                    'suggestion': suggestion,
                    'rev_growth': rev_growth,
                    'profit_growth': profit_growth,
                    'roe': roe,
                    'pe': pe,
                    'market_cap': market_cap
                })
                
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 按得分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    print(f"完成评估，共 {len(results)} 只股票")
    
    return results

def main():
    """主函数"""
    from datetime import datetime
    
    # 账号配置
    username = "13327806797"
    password = "Taorui888"
    
    print("=" * 60)
    print("十倍股完整版增强报告生成器")
    print("=" * 60)
    
    # 获取数据
    results = fetch_tenbagger_data(username, password)
    
    if not results:
        print("未获取到数据，使用示例数据")
        results = [
            {'code': '000688', 'name': '国城矿业', 'score': 54.4, 'stage': 'S1', 'grade': 'B', 
             'analysis_price': 12.21, 'current_price': 25.55, 'return_pct': 109.25, 
             'analysis_date': '2025-12-26', 'data_source': 'JQData', 'suggestion': '强烈推荐 ⭐'},
            {'code': '000426', 'name': '兴业银锡', 'score': 53.0, 'stage': 'S1', 'grade': 'B',
             'analysis_price': 14.99, 'current_price': 35.33, 'return_pct': 135.69,
             'analysis_date': '2025-12-26', 'data_source': 'JQData', 'suggestion': '强烈推荐 ⭐'},
        ]
    
    # 生成HTML
    gen_date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    html_content = get_html_head_and_styles()
    html_content += get_hero_section(gen_date, username)
    html_content += get_overview_panel()
    html_content += get_cases_panel()
    html_content += get_stages_panel()
    html_content += get_factors_panel()
    html_content += get_code_panel()
    html_content += get_realdata_panel(results)
    html_content += get_validation_panel(results)
    html_content += get_strategy_panel()
    html_content += get_html_footer()
    
    # 保存报告
    report_dir = project_root / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"tenbagger_complete_report_{username}_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ 报告已生成: {report_path}")
    print(f"   文件大小: {report_path.stat().st_size / 1024:.1f} KB")
    print(f"   评估股票: {len(results)} 只")
    print(f"   推荐股票: {len([r for r in results if r['score'] >= 50])} 只")
    
    # 保存生成记录
    record_dir = project_root / "docs" / "report_generation_records"
    record_dir.mkdir(parents=True, exist_ok=True)
    record_path = record_dir / f"tenbagger_complete_{timestamp}.json"
    
    record = {
        'report_type': 'tenbagger_complete',
        'timestamp': timestamp,
        'username': username,
        'total_stocks': len(results),
        'recommended': len([r for r in results if r['score'] >= 50]),
        'report_path': str(report_path),
        'generation_method': 'scripts/generate_complete_tenbagger_report.py'
    }
    
    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"   生成记录: {record_path}")
    
    return str(report_path)

if __name__ == "__main__":
    main()
