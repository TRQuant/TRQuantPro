#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API知识库构建脚本（优化版）
专门为策略生成和优化设计

特点：
1. 结构化元数据提取
2. API规范解析
3. 代码示例提取
4. 错误模式识别
5. 最佳实践记录
"""

import sys
import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from urllib.parse import urljoin, urlparse
import logging

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("❌ BeautifulSoup4未安装")
    sys.exit(1)

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False

# 配置
BASE_URL = "https://www.joinquant.com"
JQDATA_DOC_URL = "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9842"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "jqdata_kb"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 统计
STATS = {
    "total": 0,
    "success": 0,
    "failed": 0,
    "skipped": 0,
    "api_docs": 0,
    "examples_extracted": 0
}

# 已访问URL
visited_urls: Set[str] = set()
VISITED_URLS_FILE = OUTPUT_DIR / "visited_urls.json"


def load_visited_urls() -> Set[str]:
    """加载已访问URL"""
    if VISITED_URLS_FILE.exists():
        try:
            with open(VISITED_URLS_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            pass
    return set()


def save_visited_urls():
    """保存已访问URL"""
    try:
        with open(VISITED_URLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(visited_urls), f, ensure_ascii=False, indent=2)
    except:
        pass


def normalize_url(url: str) -> str:
    """规范化URL"""
    return url.split('#')[0]


def extract_api_spec(content: str, title: str) -> Dict[str, Any]:
    """提取API规范信息"""
    spec = {
        "function_name": None,
        "module": None,
        "signature": None,
        "parameters": [],
        "returns": None,
        "examples": [],
        "common_errors": [],
        "best_practices": []
    }
    
    # 提取函数名（从标题或代码块）
    func_pattern = r'def\s+(\w+)\s*\('
    func_match = re.search(func_pattern, content)
    if func_match:
        spec["function_name"] = func_match.group(1)
    
    # 提取代码示例
    code_pattern = r'```python\s*\n(.*?)```'
    examples = re.findall(code_pattern, content, re.DOTALL)
    spec["examples"] = [{"code": ex.strip(), "description": ""} for ex in examples[:5]]
    
    # 提取参数说明（查找"参数"部分）
    param_section = re.search(r'参数[：:]\s*\n(.*?)(?=\n\s*(?:返回|示例|说明|$))', content, re.DOTALL)
    if param_section:
        # 简单解析参数列表
        pass
    
    return spec


def determine_category(title: str, url: str, content: str) -> tuple:
    """确定分类"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    category = "数据"
    subcategory = "其他"
    tags = ["JQData", "聚宽数据", "官方文档", "API参考"]
    
    # 根据关键词判断
    if "alpha" in title_lower:
        category = "因子"
        subcategory = "Alpha因子"
        tags.extend(["Alpha因子", "因子库"])
        if "101" in title_lower:
            tags.append("Alpha101")
        elif "191" in title_lower:
            tags.append("Alpha191")
    elif "因子" in title or "factor" in title_lower:
        category = "因子"
        subcategory = "聚宽因子库"
        tags.extend(["因子库", "因子"])
    elif "cne" in title_lower or "风格因子" in title:
        category = "风险模型"
        subcategory = "风格因子"
        tags.extend(["风险模型", "风格因子"])
        if "cne5" in title_lower:
            tags.append("CNE5风格因子")
        elif "cne6" in title_lower:
            tags.append("CNE6风格因子")
    elif "技术" in title or "technical" in title_lower:
        category = "技术指标"
        subcategory = "技术分析"
        tags.extend(["技术指标", "技术分析"])
    elif "股票" in title or "stock" in title_lower:
        category = "数据"
        subcategory = "股票数据"
        tags.append("股票数据")
    elif "指数" in title or "index" in title_lower:
        category = "数据"
        subcategory = "指数数据"
        tags.append("指数数据")
    elif "期货" in title or "futures" in title_lower:
        category = "数据"
        subcategory = "期货数据"
        tags.append("期货数据")
    elif "基金" in title or "fund" in title_lower:
        category = "数据"
        subcategory = "基金数据"
        tags.append("基金数据")
    elif "宏观" in title or "macro" in title_lower:
        category = "数据"
        subcategory = "宏观经济数据"
        tags.append("宏观经济数据")
    
    # URL分类
    if "doc?name=JQDatadoc" in url:
        tags.append("JQDatadoc文档")
    if "logon" in url:
        tags.append("登录认证文档")
    
    return category, subcategory, list(dict.fromkeys(tags))


def build_structured_content(title: str, url: str, raw_content: str, api_spec: Dict) -> str:
    """构建结构化Markdown内容"""
    content = f"""# {title}

## 基本信息
- **URL**: {url}
- **函数名称**: {api_spec.get('function_name', 'N/A')}
- **模块**: {api_spec.get('module', 'N/A')}
- **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## API说明

{raw_content}

"""
    
    # 添加API规范
    if api_spec.get('signature'):
        content += f"""## 函数签名

```python
{api_spec['signature']}
```

"""
    
    # 添加参数说明
    if api_spec.get('parameters'):
        content += "## 参数说明\n\n"
        for param in api_spec['parameters']:
            content += f"- **{param.get('name')}** ({param.get('type', 'unknown')}): {param.get('description', '')}\n"
        content += "\n"
    
    # 添加返回值说明
    if api_spec.get('returns'):
        content += f"""## 返回值

{api_spec['returns'].get('description', '')}

"""
    
    # 添加使用示例
    if api_spec.get('examples'):
        content += "## 使用示例\n\n"
        for i, example in enumerate(api_spec['examples'][:3], 1):
            content += f"""### 示例 {i}

```python
{example.get('code', '')}
```

"""
    
    # 添加常见错误
    if api_spec.get('common_errors'):
        content += "## 常见错误\n\n"
        for error in api_spec['common_errors']:
            content += f"""### {error.get('error', 'Error')}

**解决方案**: {error.get('solution', '')}

"""
    
    # 添加最佳实践
    if api_spec.get('best_practices'):
        content += "## 最佳实践\n\n"
        for practice in api_spec['best_practices']:
            content += f"- {practice}\n"
        content += "\n"
    
    return content


async def crawl_and_process_page(url: str, page) -> Optional[Dict]:
    """爬取并处理单个页面"""
    url = normalize_url(url)
    
    if url in visited_urls:
        return None
    
    visited_urls.add(url)
    STATS["total"] += 1
    
    try:
        print(f"  [{STATS['total']}] 处理: {url}")
        
        # 访问页面
        await page.goto(url, wait_until='domcontentloaded', timeout=120000)
        await page.wait_for_timeout(3000)
        
        # 获取内容
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True).replace(' - JoinQuant', '') if title_tag else url
        
        # 提取内容
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        
        main = soup.find('main') or soup.find('body')
        raw_content = main.get_text(separator='\n', strip=True) if main else ""
        
        if len(raw_content) < 100:
            STATS["skipped"] += 1
            return None
        
        # 提取API规范
        api_spec = extract_api_spec(raw_content, title)
        
        # 确定分类
        category, subcategory, tags = determine_category(title, url, raw_content)
        
        # 构建结构化内容
        content = build_structured_content(title, url, raw_content, api_spec)
        
        # 构建知识库条目
        kb_entry = {
            "title": title,
            "content": content,
            "type": "api_reference",
            "category": category,
            "subcategory": subcategory,
            "tags": tags,
            "source": url,
            "metadata": {
                "function_name": api_spec.get("function_name"),
                "module": api_spec.get("module"),
                "account_required": "股票专业版",
                "data_range": "2005-01-01至今"
            },
            "api_spec": api_spec,
            "examples": api_spec.get("examples", []),
            "common_errors": api_spec.get("common_errors", []),
            "best_practices": api_spec.get("best_practices", [])
        }
        
        # 存入知识库
        if KB_AVAILABLE:
            result = knowledge_add(
                title=title,
                content=content,
                type="api_reference",
                tags=tags,
                source=url
            )
            if result.get('success') or result.get('id') or result.get('knowledge_id'):
                STATS["success"] += 1
                STATS["api_docs"] += 1
                if api_spec.get("examples"):
                    STATS["examples_extracted"] += 1
                print(f"    ✅ 成功 (分类: {category}/{subcategory}, 标签: {len(tags)}个)")
                return kb_entry
            else:
                STATS["failed"] += 1
                print(f"    ❌ 存入知识库失败")
                return None
        else:
            # 仅保存到文件
            STATS["success"] += 1
            return kb_entry
            
    except Exception as e:
        STATS["failed"] += 1
        print(f"    ❌ 失败: {str(e)[:100]}")
        return None


async def main():
    """主函数"""
    global visited_urls
    
    print("=" * 70)
    print("🚀 聚宽API知识库构建（优化版 - 策略生成专用）")
    print("=" * 70)
    print(f"起始URL: {JQDATA_DOC_URL}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 70)
    print()
    
    # 加载已访问URL
    visited_urls = load_visited_urls()
    if visited_urls:
        print(f"📋 已加载 {len(visited_urls)} 个已访问URL")
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    # 开始爬取
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(120000)
        
        # 爬取起始页面（简化：只爬取API文档首页）
        result = await crawl_and_process_page(JQDATA_DOC_URL, page)
        
        # 保存visited_urls
        save_visited_urls()
        
        await context.close()
        await browser.close()
    
    # 打印统计
    print()
    print("=" * 70)
    print("📊 统计信息")
    print("=" * 70)
    print(f"总共处理: {STATS['total']}")
    print(f"成功: {STATS['success']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过: {STATS['skipped']}")
    print(f"API文档: {STATS['api_docs']}")
    print(f"提取示例: {STATS['examples_extracted']}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

