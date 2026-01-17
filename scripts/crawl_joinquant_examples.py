# -*- coding: utf-8 -*-
"""
抓取聚宽投资应用例子并对比不同爬虫工具
"""

import sys
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 聚宽相关URL
JOINQUANT_URLS = [
    "https://www.joinquant.com/help/api/help?name=Strategy",
    "https://www.joinquant.com/help/api/help?name=Factor",
    "https://www.joinquant.com/help/api/help?name=Backtest",
    "https://www.joinquant.com/example",
    "https://www.joinquant.com/strategy",
]

def test_basic_crawler(url: str) -> Dict[str, Any]:
    """测试基础爬虫工具"""
    print(f"\n[基础爬虫] 抓取: {url}")
    start_time = time.time()
    
    try:
        from mcp_servers.unified_dev_server import crawler_fetch
        
        result = crawler_fetch(url, extract_text=True, extract_links=True)
        elapsed = time.time() - start_time
        
        return {
            "tool": "基础爬虫 (requests+BeautifulSoup)",
            "url": url,
            "success": result.get("success", False),
            "elapsed_time": round(elapsed, 2),
            "title": result.get("title", ""),
            "text_length": len(result.get("text", "")),
            "links_count": len(result.get("links", [])),
            "error": result.get("error"),
            "sample_text": result.get("text", "")[:500] if result.get("text") else ""
        }
    except Exception as e:
        return {
            "tool": "基础爬虫",
            "url": url,
            "success": False,
            "error": str(e),
            "elapsed_time": time.time() - start_time
        }

def test_selenium_crawler(url: str) -> Dict[str, Any]:
    """测试Selenium爬虫工具"""
    print(f"\n[Selenium] 抓取: {url}")
    start_time = time.time()
    
    try:
        from mcp_servers.unified_dev_server import crawler_selenium_fetch
        
        result = crawler_selenium_fetch(
            url=url,
            wait_time=5,
            wait_selector="body",
            headless=True
        )
        elapsed = time.time() - start_time
        
        return {
            "tool": "Selenium (浏览器自动化)",
            "url": url,
            "success": result.get("success", False),
            "elapsed_time": round(elapsed, 2),
            "title": result.get("title", ""),
            "text_length": len(result.get("text", "")),
            "html_length": len(result.get("html", "")),
            "error": result.get("error"),
            "sample_text": result.get("text", "")[:500] if result.get("text") else ""
        }
    except Exception as e:
        return {
            "tool": "Selenium",
            "url": url,
            "success": False,
            "error": str(e),
            "elapsed_time": time.time() - start_time
        }

def test_lavague_crawler(url: str) -> Dict[str, Any]:
    """测试Lavague爬虫工具"""
    print(f"\n[Lavague] 抓取: {url}")
    start_time = time.time()
    
    try:
        from mcp_servers.unified_dev_server import crawler_lavague_execute
        
        result = crawler_lavague_execute(
            url=url,
            instruction="提取页面主要内容，包括标题、策略示例和代码片段",
            max_actions=5,
            headless=True
        )
        elapsed = time.time() - start_time
        
        return {
            "tool": "Lavague (AI自动化)",
            "url": url,
            "success": result.get("success", False),
            "elapsed_time": round(elapsed, 2),
            "title": result.get("title", ""),
            "page_length": result.get("page_length", 0),
            "actions_executed": result.get("actions_executed", 0),
            "error": result.get("error"),
            "result": str(result.get("result", ""))[:500]
        }
    except Exception as e:
        return {
            "tool": "Lavague",
            "url": url,
            "success": False,
            "error": str(e),
            "elapsed_time": time.time() - start_time
        }

def generate_html_report(results: List[Dict[str, Any]]) -> str:
    """生成HTML对比报告"""
    
    # 统计信息
    total_tests = len(results)
    success_count = sum(1 for r in results if r.get("success"))
    
    # 按工具分组
    tools_stats = {}
    for result in results:
        tool = result.get("tool", "Unknown")
        if tool not in tools_stats:
            tools_stats[tool] = {
                "total": 0,
                "success": 0,
                "total_time": 0,
                "avg_time": 0,
                "total_text": 0
            }
        tools_stats[tool]["total"] += 1
        if result.get("success"):
            tools_stats[tool]["success"] += 1
            tools_stats[tool]["total_time"] += result.get("elapsed_time", 0)
            tools_stats[tool]["total_text"] += result.get("text_length", 0) or result.get("page_length", 0)
    
    for tool in tools_stats:
        if tools_stats[tool]["success"] > 0:
            tools_stats[tool]["avg_time"] = tools_stats[tool]["total_time"] / tools_stats[tool]["success"]
            tools_stats[tool]["avg_text"] = tools_stats[tool]["total_text"] / tools_stats[tool]["success"]
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>聚宽投资应用例子 - 爬虫工具对比报告</title>
    <style>
        :root {{
            --primary: #1a73e8;
            --secondary: #34a853;
            --danger: #ea4335;
            --warning: #fbbc04;
            --bg-dark: #1e1e2e;
            --bg-card: #2d2d3f;
            --text-primary: #e4e4e7;
            --text-secondary: #a1a1aa;
            --border: #3f3f5a;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            color: var(--text-primary);
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(90deg, #1a73e8, #34a853);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}
        .card h2 {{
            color: var(--primary);
            margin-bottom: 16px;
            font-size: 1.5rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #2d2d4a 0%, #1e1e35 100%);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid var(--border);
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 8px;
        }}
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: rgba(26,115,232,0.2);
            color: var(--primary);
            font-weight: 600;
        }}
        tr:hover {{
            background: rgba(255,255,255,0.03);
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .badge-success {{
            background: rgba(52,168,83,0.2);
            color: #5dd879;
        }}
        .badge-danger {{
            background: rgba(234,67,53,0.2);
            color: #ff6b6b;
        }}
        .badge-warning {{
            background: rgba(251,188,4,0.2);
            color: #ffd54f;
        }}
        .comparison-table {{
            margin-top: 20px;
        }}
        .tool-section {{
            margin-bottom: 30px;
        }}
        .result-item {{
            background: rgba(26,115,232,0.1);
            border-left: 4px solid var(--primary);
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }}
        .result-item.error {{
            border-left-color: var(--danger);
            background: rgba(234,67,53,0.1);
        }}
        .sample-text {{
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 6px;
            font-family: 'Consolas', monospace;
            font-size: 0.85rem;
            margin-top: 10px;
            max-height: 200px;
            overflow-y: auto;
        }}
        .highlight-box {{
            background: linear-gradient(135deg, rgba(26,115,232,0.2), rgba(52,168,83,0.2));
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(26,115,232,0.3);
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 聚宽投资应用例子 - 爬虫工具对比报告</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_tests}</div>
                <div class="stat-label">总测试数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{success_count}</div>
                <div class="stat-label">成功数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{round(success_count/total_tests*100, 1) if total_tests > 0 else 0}%</div>
                <div class="stat-label">成功率</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 工具性能对比</h2>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>工具</th>
                        <th>测试次数</th>
                        <th>成功次数</th>
                        <th>成功率</th>
                        <th>平均耗时(秒)</th>
                        <th>平均内容长度</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for tool, stats in tools_stats.items():
        success_rate = round(stats["success"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0
        html += f"""
                    <tr>
                        <td><strong>{tool}</strong></td>
                        <td>{stats['total']}</td>
                        <td>{stats['success']}</td>
                        <td><span class="badge {'badge-success' if success_rate > 50 else 'badge-danger'}">{success_rate}%</span></td>
                        <td>{round(stats.get('avg_time', 0), 2)}</td>
                        <td>{round(stats.get('avg_text', 0))}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>🔍 详细测试结果</h2>
"""
    
    # 按工具分组显示结果
    tools = {}
    for result in results:
        tool = result.get("tool", "Unknown")
        if tool not in tools:
            tools[tool] = []
        tools[tool].append(result)
    
    for tool, tool_results in tools.items():
        html += f"""
            <div class="tool-section">
                <h3 style="color: var(--secondary); margin-bottom: 15px;">{tool}</h3>
"""
        for result in tool_results:
            status_class = "" if result.get("success") else "error"
            status_badge = '<span class="badge badge-success">成功</span>' if result.get("success") else f'<span class="badge badge-danger">失败</span>'
            
            html += f"""
                <div class="result-item {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <strong>{result.get('url', 'N/A')}</strong>
                        {status_badge}
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.9rem; color: var(--text-secondary);">
                        <div>耗时: <strong>{result.get('elapsed_time', 0)}秒</strong></div>
"""
            if result.get("text_length"):
                html += f'<div>文本长度: <strong>{result.get("text_length")}</strong></div>'
            if result.get("html_length"):
                html += f'<div>HTML长度: <strong>{result.get("html_length")}</strong></div>'
            if result.get("links_count"):
                html += f'<div>链接数: <strong>{result.get("links_count")}</strong></div>'
            if result.get("actions_executed"):
                html += f'<div>执行动作: <strong>{result.get("actions_executed")}</strong></div>'
            
            html += """
                    </div>
"""
            if result.get("error"):
                html += f'<div style="color: var(--danger); margin-top: 10px;">❌ 错误: {result.get("error")}</div>'
            if result.get("sample_text"):
                html += f'<div class="sample-text">{result.get("sample_text")}...</div>'
            if result.get("result"):
                html += f'<div class="sample-text">{result.get("result")}...</div>'
            
            html += """
                </div>
"""
        
        html += """
            </div>
"""
    
    html += """
        </div>
        
        <div class="card">
            <h2>💡 工具选择建议</h2>
            <div class="highlight-box">
                <h3 style="color: var(--accent); margin-bottom: 15px;">📋 使用场景推荐</h3>
                <table>
                    <thead>
                        <tr>
                            <th>场景</th>
                            <th>推荐工具</th>
                            <th>原因</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>静态HTML页面</td>
                            <td><strong>基础爬虫</strong></td>
                            <td>速度快，资源占用少，适合简单页面</td>
                        </tr>
                        <tr>
                            <td>JavaScript渲染页面</td>
                            <td><strong>Selenium</strong></td>
                            <td>支持动态内容，可精确控制浏览器操作</td>
                        </tr>
                        <tr>
                            <td>复杂交互操作</td>
                            <td><strong>Lavague</strong></td>
                            <td>AI理解自然语言，自动执行多步骤操作</td>
                        </tr>
                        <tr>
                            <td>需要点击/填写表单</td>
                            <td><strong>Selenium</strong></td>
                            <td>精确的元素定位和操作控制</td>
                        </tr>
                        <tr>
                            <td>快速原型开发</td>
                            <td><strong>Lavague</strong></td>
                            <td>用自然语言描述即可，开发效率高</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="card">
            <h2>📝 聚宽投资应用示例总结</h2>
            <div class="highlight-box">
                <h3 style="color: var(--secondary); margin-bottom: 15px;">聚宽平台特点</h3>
                <ul style="line-height: 2; padding-left: 20px;">
                    <li><strong>策略研究</strong>：提供丰富的量化策略模板和因子库</li>
                    <li><strong>回测验证</strong>：强大的回测引擎，支持多周期、多市场</li>
                    <li><strong>实盘交易</strong>：支持PTrade、QMT等券商接口对接</li>
                    <li><strong>社区生态</strong>：活跃的开发者社区，策略分享和学习</li>
                    <li><strong>数据支持</strong>：完整的历史行情、财务、基本面数据</li>
                </ul>
            </div>
            
            <div class="highlight-box" style="margin-top: 20px;">
                <h3 style="color: var(--accent); margin-bottom: 15px;">聚宽投资应用典型场景</h3>
                <table>
                    <thead>
                        <tr>
                            <th>应用场景</th>
                            <th>聚宽功能</th>
                            <th>TRQuant对应</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>多因子选股</strong></td>
                            <td>get_fundamentals() 获取财务数据<br/>query() 构建查询条件</td>
                            <td>factor.recommend<br/>factor.calculate</td>
                        </tr>
                        <tr>
                            <td><strong>动量策略</strong></td>
                            <td>history() 获取历史价格<br/>pct_change() 计算收益率</td>
                            <td>strategy.generate (momentum模板)</td>
                        </tr>
                        <tr>
                            <td><strong>价值投资</strong></td>
                            <td>valuation.pe_ratio<br/>indicator.roe</td>
                            <td>strategy.generate (value模板)</td>
                        </tr>
                        <tr>
                            <td><strong>行业轮动</strong></td>
                            <td>get_industry_stocks()<br/>sector_momentum计算</td>
                            <td>market.mainlines<br/>strategy.generate (rotation模板)</td>
                        </tr>
                        <tr>
                            <td><strong>回测验证</strong></td>
                            <td>run_daily()<br/>order_target_value()</td>
                            <td>backtest.quick<br/>backtest.bullettrade</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="highlight-box" style="margin-top: 20px;">
                <h3 style="color: var(--primary); margin-bottom: 15px;">聚宽 vs TRQuant 对比</h3>
                <table>
                    <thead>
                        <tr>
                            <th>维度</th>
                            <th>聚宽</th>
                            <th>TRQuant</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>定位</strong></td>
                            <td>量化研究平台</td>
                            <td>AI辅助量化投资平台</td>
                        </tr>
                        <tr>
                            <td><strong>数据源</strong></td>
                            <td>JQData（付费）</td>
                            <td>JQData + AKShare + MongoDB</td>
                        </tr>
                        <tr>
                            <td><strong>策略开发</strong></td>
                            <td>Python代码编写</td>
                            <td>AI辅助生成 + 模板库</td>
                        </tr>
                        <tr>
                            <td><strong>工作流</strong></td>
                            <td>手动执行各步骤</td>
                            <td>9步标准化工作流</td>
                        </tr>
                        <tr>
                            <td><strong>知识积累</strong></td>
                            <td>社区分享</td>
                            <td>轩辕剑灵知识库自动学习</td>
                        </tr>
                        <tr>
                            <td><strong>实盘对接</strong></td>
                            <td>需单独开发</td>
                            <td>内置PTrade/QMT支持</td>
                        </tr>
                        <tr>
                            <td><strong>AI能力</strong></td>
                            <td>无</td>
                            <td>Cursor IDE深度集成</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="card">
            <h2>🎯 工具选择决策树</h2>
            <div class="highlight-box">
                <div style="font-family: monospace; line-height: 2; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 8px;">
                    <div>开始爬取任务</div>
                    <div>│</div>
                    <div>├─ 页面是否需要JavaScript渲染？</div>
                    <div>│  │</div>
                    <div>│  ├─ 否 → 使用 <strong style="color: var(--secondary);">crawler.fetch</strong> (最快)</div>
                    <div>│  └─ 是 → 继续判断</div>
                    <div>│     │</div>
                    <div>│     ├─ 需要精确控制元素操作？</div>
                    <div>│     │  │</div>
                    <div>│     │  ├─ 是 → 使用 <strong style="color: var(--primary);">crawler.selenium.*</strong></div>
                    <div>│     │  └─ 否 → 继续判断</div>
                    <div>│     │     │</div>
                    <div>│     │     └─ 复杂多步骤操作？</div>
                    <div>│     │        │</div>
                    <div>│     │        ├─ 是 → 使用 <strong style="color: var(--accent);">crawler.lavague.execute</strong></div>
                    <div>│     │        └─ 否 → 使用 <strong style="color: var(--primary);">crawler.selenium.fetch</strong></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """主函数"""
    print("=" * 60)
    print("聚宽投资应用例子 - 爬虫工具对比测试")
    print("=" * 60)
    
    # 测试URL（使用聚宽相关页面）
    test_urls = [
        "https://www.joinquant.com/help/api/help?name=Strategy",
        "https://www.joinquant.com/help/api/help?name=Factor",
        "https://www.joinquant.com/help/api/help?name=Backtest",
    ]
    
    # 聚宽投资应用示例页面（如果可访问）
    joinquant_example_urls = [
        "https://www.joinquant.com/example",
        "https://www.joinquant.com/strategy",
    ]
    
    # 如果无法访问，使用备用URL
    backup_urls = [
        "https://www.baidu.com",
        "https://www.example.com",
    ]
    
    all_results = []
    
    # 测试每个URL
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"测试URL: {url}")
        print('='*60)
        
        # 测试基础爬虫
        result1 = test_basic_crawler(url)
        all_results.append(result1)
        
        # 测试Selenium（如果基础爬虫失败或内容很少）
        if not result1.get("success") or result1.get("text_length", 0) < 100:
            result2 = test_selenium_crawler(url)
            all_results.append(result2)
        
        # 测试Lavague（可选，较慢）
        # result3 = test_lavague_crawler(url)
        # all_results.append(result3)
        
        time.sleep(2)  # 避免请求过快
    
    # 生成HTML报告
    html_content = generate_html_report(all_results)
    
    # 保存报告
    report_path = PROJECT_ROOT / "docs" / "reports" / f"joinquant_crawler_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n{'='*60}")
    print(f"✅ HTML报告已生成: {report_path}")
    print('='*60)
    
    return str(report_path)

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    report_path = main()
    print(f"\n报告路径: {report_path}")

