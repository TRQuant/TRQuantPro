# -*- coding: utf-8 -*-
"""
爬取聚宽策略回测API文档
用于V4.0系统集成聚宽回测引擎
"""

import sys
from pathlib import Path
import json
import time
from datetime import datetime
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 聚宽策略回测API关键页面
JOINQUANT_BACKTEST_API_URLS = {
    "策略设置函数": "https://www.joinquant.com/help/api/help#api:策略设置函数",
    "数据获取函数": "https://www.joinquant.com/help/api/help#api:数据获取函数",
    "交易函数": "https://www.joinquant.com/help/api/help#api:交易函数",
    "回测过程": "https://www.joinquant.com/help/api/help#api:回测过程",
    "回测环境": "https://www.joinquant.com/help/api/help#api:回测环境",
    "策略引擎介绍": "https://www.joinquant.com/help/api/help#api:策略引擎介绍",
    "对象说明": "https://www.joinquant.com/help/api/help#api:对象♠",
    "运行频率": "https://www.joinquant.com/help/api/help#api:运行频率",
    "运行时间": "https://www.joinquant.com/help/api/help#api:运行时间",
    "订单处理": "https://www.joinquant.com/help/api/help#api:订单处理",
    "滑点": "https://www.joinquant.com/help/api/help#api:滑点",
    "交易税费": "https://www.joinquant.com/help/api/help#api:交易税费",
    "风险指标": "https://www.joinquant.com/help/api/help#api:风险指标",
}

def crawl_page(url: str, title: str) -> Dict[str, Any]:
    """爬取单个页面"""
    print(f"\n[爬取] {title}: {url}")
    
    try:
        from mcp_servers.unified_dev_server import crawler_selenium_fetch
        
        # 使用Selenium爬取（因为聚宽页面是动态加载的）
        result = crawler_selenium_fetch(
            url=url,
            wait_time=5,
            wait_selector="body",
            headless=True
        )
        
        if result.get("success"):
            # 提取文本内容
            from bs4 import BeautifulSoup
            html = result.get("html", "")
            soup = BeautifulSoup(html, 'html.parser')
            
            # 移除脚本和样式
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # 提取主要内容
            main_content = soup.find("main") or soup.find("article") or soup.find("body")
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)
            
            return {
                "success": True,
                "title": title,
                "url": url,
                "content": text[:50000],  # 限制长度
                "html_length": len(html),
                "text_length": len(text)
            }
        else:
            return {
                "success": False,
                "title": title,
                "url": url,
                "error": result.get("error", "未知错误")
            }
    except Exception as e:
        return {
            "success": False,
            "title": title,
            "url": url,
            "error": str(e)
        }

def main():
    """主函数"""
    print("=" * 60)
    print("聚宽策略回测API文档爬取")
    print("=" * 60)
    
    results = []
    total = len(JOINQUANT_BACKTEST_API_URLS)
    
    for i, (title, url) in enumerate(JOINQUANT_BACKTEST_API_URLS.items(), 1):
        print(f"\n进度: {i}/{total}")
        result = crawl_page(url, title)
        results.append(result)
        
        if result.get("success"):
            print(f"✅ 成功: {title}")
        else:
            print(f"❌ 失败: {title} - {result.get('error')}")
        
        # 避免请求过快
        time.sleep(2)
    
    # 保存结果
    output_dir = PROJECT_ROOT / "docs" / "joinquant_crawled"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"backtest_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "crawl_time": datetime.now().isoformat(),
            "total_pages": total,
            "success_count": sum(1 for r in results if r.get("success")),
            "pages": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"爬取完成！结果已保存至: {output_file}")
    print(f"成功: {sum(1 for r in results if r.get('success'))}/{total}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
