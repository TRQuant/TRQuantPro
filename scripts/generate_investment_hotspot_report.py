#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用OpenManus功能抓取下周投资热点和建议报告
==========================================
使用OpenManusAgent、FinancialCollector、WorkflowEnhancer获取投资热点信息并生成报告

功能:
1. 使用FinancialCollector获取财经新闻
2. 使用WorkflowEnhancer的R2主线轮动研究获取热点主题
3. 使用R1市场趋势分析获取市场趋势
4. 整理成HTML报告

作者: TRQuant Team
日期: 2026-01-11
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


async def collect_investment_hotspots():
    """收集投资热点信息"""
    print("\n" + "=" * 70)
    print("收集投资热点信息")
    print("=" * 70)
    
    results = {
        "market_trend": None,
        "hot_topics": None,
        "news_list": None,
        "collect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        from core.workflow import WorkflowEnhancer
        from core.data_collection import FinancialCollector
        
        async with WorkflowEnhancer(headless=True) as enhancer:
            # 1. 获取市场趋势分析
            print("\n📈 获取市场趋势分析...")
            try:
                r1_result = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
                if r1_result.success:
                    results["market_trend"] = r1_result.data
                    print(f"  ✅ 市场趋势分析完成")
                    print(f"     趋势标签: {r1_result.data.get('trend_label', 'N/A')}")
                    print(f"     共振阶段: {r1_result.data.get('resonance_phase', 'N/A')}")
                else:
                    print(f"  ⚠️  市场趋势分析失败: {r1_result.error}")
            except Exception as e:
                print(f"  ❌ 市场趋势分析异常: {e}")
            
            # 2. 获取主线轮动研究（热点主题）
            print("\n🔥 获取主线轮动研究（热点主题）...")
            try:
                r2_result = await enhancer.enhance_r2_mainline()
                if r2_result.success:
                    results["hot_topics"] = r2_result.data
                    print(f"  ✅ 主线轮动研究完成")
                    hot_topics = r2_result.data.get('hot_topics', [])
                    print(f"     热点主题数量: {len(hot_topics)}")
                    for i, topic in enumerate(hot_topics[:5], 1):
                        print(f"     {i}. {topic.get('keyword', 'N/A')} (热度: {topic.get('score', 0):.1f})")
                else:
                    print(f"  ⚠️  主线轮动研究失败: {r2_result.error}")
            except Exception as e:
                print(f"  ❌ 主线轮动研究异常: {e}")
        
        # 3. 获取财经新闻（从多个数据源）
        print("\n📰 获取财经新闻（多数据源）...")
        all_news = []
        sources = ["eastmoney", "sina", "cls"]  # 支持多个数据源
        
        try:
            async with FinancialCollector(headless=True) as collector:
                for source in sources:
                    try:
                        print(f"\n  📡 正在从 {source} 抓取新闻...")
                        news_result = await collector.fetch_news(source, limit=10)
                        if news_result.success and news_result.data:
                            source_news = news_result.data
                            all_news.extend(source_news)
                            print(f"     ✅ {source}: 成功抓取 {len(source_news)} 条新闻")
                            # 显示前2条
                            for i, news in enumerate(source_news[:2], 1):
                                print(f"        {i}. {news.get('title', 'N/A')[:40]}...")
                        else:
                            error_msg = news_result.error if news_result else "无数据"
                            print(f"     ⚠️  {source}: 抓取失败或空数据 ({error_msg})")
                    except Exception as e:
                        print(f"     ❌ {source}: 抓取异常 ({str(e)[:50]})")
                    finally:
                        # 短暂延迟，避免请求过快
                        await asyncio.sleep(1)
                
                # 去重（基于标题）
                seen_titles = set()
                unique_news = []
                for news in all_news:
                    title = news.get('title', '')
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        unique_news.append(news)
                
                results["news_list"] = unique_news
                results["news_sources"] = {s: len([n for n in all_news if n.get('source') == s]) for s in sources}
                
                print(f"\n  ✅ 财经新闻获取完成")
                print(f"     总新闻数量: {len(unique_news)} (去重后)")
                print(f"     数据源分布: {results['news_sources']}")
        except Exception as e:
            print(f"  ❌ 财经新闻获取异常: {e}")
        
    except Exception as e:
        print(f"\n❌ 收集投资热点信息失败: {e}")
        import traceback
        traceback.print_exc()
    
    return results


def generate_html_report(results: Dict[str, Any], output_file: Path):
    """生成HTML报告"""
    print("\n" + "=" * 70)
    print("生成HTML报告")
    print("=" * 70)
    
    collect_time = results.get("collect_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # 获取下周日期范围
    today = datetime.now()
    next_week_start = today + timedelta(days=(7 - today.weekday()))
    next_week_end = next_week_start + timedelta(days=6)
    next_week_range = f"{next_week_start.strftime('%Y年%m月%d日')} - {next_week_end.strftime('%Y年%m月%d日')}"
    
    # 市场趋势分析
    market_trend = results.get("market_trend", {})
    trend_label = market_trend.get("trend_label", "N/A")
    resonance_phase = market_trend.get("resonance_phase", "N/A")
    hmm_state = market_trend.get("hmm_state", "N/A")
    ensemble_score = market_trend.get("ensemble_score", 0)
    
    # 热点主题
    hot_topics_data = results.get("hot_topics", {})
    hot_topics = hot_topics_data.get("hot_topics", [])
    top10_topics = hot_topics_data.get("top10_topics", [])
    
    # 财经新闻
    news_list = results.get("news_list", [])
    
    # 生成HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>下周投资热点和建议报告 - {next_week_range}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .header .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .trend-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin: 5px;
        }}
        .trend-bullish {{
            background-color: #10b981;
            color: white;
        }}
        .trend-bearish {{
            background-color: #ef4444;
            color: white;
        }}
        .trend-neutral {{
            background-color: #6b7280;
            color: white;
        }}
        .topic-list {{
            list-style: none;
            padding: 0;
        }}
        .topic-item {{
            padding: 15px;
            margin: 10px 0;
            background: #f9fafb;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .topic-item .keyword {{
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }}
        .topic-item .score {{
            float: right;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .news-list {{
            list-style: none;
            padding: 0;
        }}
        .news-item {{
            padding: 15px;
            margin: 10px 0;
            background: #f9fafb;
            border-left: 4px solid #10b981;
            border-radius: 4px;
        }}
        .news-item .title {{
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 5px;
        }}
        .news-item .meta {{
            font-size: 0.9em;
            color: #6b7280;
        }}
        .recommendations {{
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
        }}
        .recommendations h3 {{
            color: #1e40af;
            margin-top: 0;
        }}
        .recommendations ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .footer {{
            text-align: center;
            color: #6b7280;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 下周投资热点和建议报告</h1>
        <div class="subtitle">
            <strong>时间范围:</strong> {next_week_range}<br>
            <strong>生成时间:</strong> {collect_time}
        </div>
    </div>
    
    <!-- 市场趋势分析 -->
    <div class="section">
        <h2>📊 市场趋势分析</h2>
        <p><strong>趋势标签:</strong> <span class="trend-badge trend-{trend_label}">{trend_label.upper()}</span></p>
        <p><strong>共振阶段:</strong> {resonance_phase}</p>
        <p><strong>HMM状态:</strong> {hmm_state}</p>
        <p><strong>综合评分:</strong> {ensemble_score:.2f}</p>
    </div>
    
    <!-- 投资热点主题 -->
    <div class="section">
        <h2>🔥 投资热点主题</h2>
        <ul class="topic-list">
"""
    
    # 添加热点主题
    if hot_topics:
        for topic in hot_topics:
            keyword = topic.get("keyword", "N/A")
            score = topic.get("score", 0)
            count = topic.get("count", 0)
            html_content += f"""            <li class="topic-item">
                <span class="keyword">{keyword}</span>
                <span class="score">热度 {score:.1f}</span>
                <div style="margin-top: 5px; color: #6b7280; font-size: 0.9em;">出现次数: {count}</div>
            </li>
"""
    else:
        html_content += "            <li>暂无热点主题数据</li>\n"
    
    html_content += """        </ul>
    </div>
    
    <!-- 财经新闻 -->
    <div class="section">
        <h2>📰 相关财经新闻</h2>
        <ul class="news-list">
"""
    
    # 添加财经新闻
    if news_list:
        for news in news_list[:15]:  # 显示前15条
            title = news.get("title", "N/A")
            url = news.get("url", "#")
            date = news.get("date", "")
            source = news.get("source", "东方财富")
            
            html_content += f"""            <li class="news-item">
                <div class="title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="meta">{source} | {date}</div>
            </li>
"""
    else:
        html_content += "            <li>暂无财经新闻数据</li>\n"
    
    html_content += """        </ul>
    </div>
    
    <!-- 投资建议 -->
    <div class="section">
        <h2>💡 下周投资建议</h2>
        <div class="recommendations">
            <h3>基于当前市场趋势和热点主题的建议：</h3>
            <ul>
"""
    
    # 生成投资建议
    recommendations = []
    
    if trend_label == "bullish":
        recommendations.append("市场处于上涨趋势，建议关注热点主题相关的优质标的")
    elif trend_label == "bearish":
        recommendations.append("市场处于下跌趋势，建议控制仓位，关注防御性资产")
    else:
        recommendations.append("市场处于震荡状态，建议精选个股，关注热点主题轮动机会")
    
    if hot_topics:
        top_keywords = [t.get("keyword", "") for t in hot_topics[:3]]
        recommendations.append(f"重点关注热点主题: {', '.join(top_keywords)}")
    
    if resonance_phase and "共振" in resonance_phase:
        recommendations.append("多周期共振状态良好，建议适当提升仓位")
    
    recommendations.append("建议关注市场热点轮动，把握结构性机会")
    recommendations.append("严格控制风险，设置止损位")
    
    for rec in recommendations:
        html_content += f"                <li>{rec}</li>\n"
    
    html_content += """            </ul>
        </div>
    </div>
    
    <!-- 风险提示 -->
    <div class="section">
        <h2>⚠️ 风险提示</h2>
        <ul>
            <li>本报告仅供参考，不构成投资建议</li>
            <li>投资有风险，入市需谨慎</li>
            <li>市场变化较快，请及时关注最新信息</li>
            <li>建议结合自身风险承受能力进行投资决策</li>
        </ul>
    </div>
    
    <div class="footer">
        <p>报告生成时间: {collect_time} | TRQuant投资研究系统</p>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"  ✅ HTML报告已生成")
    print(f"     文件位置: {output_file}")
    print(f"     文件大小: {len(html_content)} 字节")
    
    return output_file


async def main():
    """主函数"""
    print("=" * 70)
    print("使用OpenManus功能抓取下周投资热点和建议报告")
    print("=" * 70)
    
    # 1. 收集投资热点信息
    results = await collect_investment_hotspots()
    
    # 2. 生成HTML报告
    today = datetime.now()
    report_date = today.strftime("%Y%m%d")
    output_file = PROJECT_ROOT / "reports" / f"investment_hotspot_report_{report_date}.html"
    
    html_file = generate_html_report(results, output_file)
    
    # 3. 保存JSON数据（可选）
    json_file = PROJECT_ROOT / "reports" / f"investment_hotspot_data_{report_date}.json"
    json_file.parent.mkdir(parents=True, exist_ok=True)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✅ JSON数据已保存: {json_file}")
    
    print("\n" + "=" * 70)
    print("报告生成完成")
    print("=" * 70)
    print(f"\n📄 报告文件: {html_file}")
    print(f"📊 数据文件: {json_file}")
    print("\n💡 提示:")
    print(f"  - 可以在浏览器中打开报告: {html_file}")
    print(f"  - 报告包含市场趋势分析、投资热点主题、财经新闻和投资建议")
    print(f"  - 数据已保存为JSON格式，可用于进一步分析")


if __name__ == "__main__":
    asyncio.run(main())
