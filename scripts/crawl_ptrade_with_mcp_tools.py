#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用MCP工具完整爬取PTrade API文档

功能：
1. 使用MCP爬虫工具抓取PTrade API文档
2. 提取所有锚点内容块
3. 存入RAG知识库

Author: TRQuant Team
Date: 2026-01-09
"""

import sys
import json
import asyncio
import re
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from core.mcp.client import MCPClient
    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    print("❌ MCPClient不可用")

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    print("⚠️ 知识库工具不可用")

BASE_URL = "https://ptradeapi.com"
START_URL = "https://ptradeapi.com/"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "ptrade_crawled" / "mcp_crawl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATS = {
    "pages_crawled": 0,
    "sections_found": 0,
    "sections_saved": 0,
    "sections_failed": 0,
    "duplicates_skipped": 0,
    "start_time": None,
}

content_hashes: Set[str] = set()


def load_content_hashes():
    """加载内容哈希"""
    global content_hashes
    hash_file = OUTPUT_DIR / "content_hashes.json"
    if hash_file.exists():
        try:
            content_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass


def save_content_hashes():
    """保存内容哈希"""
    hash_file = OUTPUT_DIR / "content_hashes.json"
    hash_file.write_text(json.dumps(list(content_hashes), ensure_ascii=False, indent=2), encoding='utf-8')


def classify_and_tag(section_data: Dict) -> List[str]:
    """分类和标签"""
    tags = ['PTrade', 'API文档', '量化交易']
    
    title = section_data.get('title', '')
    content = section_data.get('content', '')
    anchor_id = section_data.get('anchor_id', '')
    
    # 根据标题和内容分类
    if 'API' in title or 'api' in anchor_id.lower():
        tags.append('API接口')
    
    if '交易' in title or 'trade' in anchor_id.lower() or 'order' in content:
        tags.append('交易')
    
    if '数据' in title or 'data' in anchor_id.lower() or 'get_' in content:
        tags.append('数据')
    
    if '策略' in title or 'strategy' in anchor_id.lower():
        tags.append('策略开发')
    
    if '回测' in title or 'backtest' in anchor_id.lower():
        tags.append('回测')
    
    return list(dict.fromkeys(tags))


def save_to_knowledge_base(section_data: Dict) -> bool:
    """保存到知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        # 计算内容哈希
        content_hash = hashlib.md5(section_data['content'].encode('utf-8')).hexdigest()
        if content_hash in content_hashes:
            STATS['duplicates_skipped'] += 1
            return False
        
        content_hashes.add(content_hash)
        
        # 分类和标签
        tags = classify_and_tag(section_data)
        
        # 构建知识库内容
        kb_content = f"""# {section_data['title']}

**锚点ID**: {section_data.get('anchor_id', 'N/A')}
**URL**: {section_data.get('url', '')}

## 内容

{section_data['content']}

"""
        
        # 添加代码块
        if section_data.get('code_blocks'):
            kb_content += "\n## 代码示例\n\n"
            for i, code in enumerate(section_data['code_blocks'][:5], 1):
                kb_content += f"### 代码示例 {i}\n\n```python\n{code}\n```\n\n"
        
        # 添加到知识库（优先使用MCP工具）
        result = None
        
        if MCP_CLIENT_AVAILABLE:
            try:
                from core.mcp.client import MCPClient
                client = MCPClient()
                
                result = client.call(
                    tool_name='kb.add',
                    arguments={
                        'title': f"PTrade API: {section_data['title']}",
                        'content': kb_content,
                        'category': 'PTrade_API'
                    },
                    timeout=30.0
                )
                
                if result.success:
                    data = result.data
                    if isinstance(data, str):
                        data = json.loads(data)
                    result = {'success': True, 'knowledge_id': data.get('id') or 'unknown'}
                else:
                    result = {'success': False, 'error': result.error}
            except Exception as e:
                print(f"  ⚠️ MCP工具调用失败: {e}，回退到直接调用")
                result = None
        
        # 如果MCP工具不可用或失败，使用直接函数调用
        if result is None:
            try:
                from mcp_servers.unified_dev_server import knowledge_add
                result = knowledge_add(
                    title=f"PTrade API: {section_data['title']}",
                    content=kb_content,
                    type='reference',
                    tags=tags,
                    source=section_data.get('url', '')
                )
            except Exception as e:
                print(f"  ❌ 直接调用也失败: {e}")
                result = {'success': False, 'error': str(e)}
        
        if result and (result.get('success') or result.get('knowledge_id') or result.get('id')):
            STATS['sections_saved'] += 1
            kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
            print(f"  ✅ 已存入知识库 (ID: {kb_id})")
            return True
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No result'
            print(f"  ❌ 知识库存储失败: {error_msg}")
            STATS['sections_failed'] += 1
            return False
    
    except Exception as e:
        print(f"  ❌ 知识库存储异常: {e}")
        STATS['sections_failed'] += 1
        return False


def extract_sections_from_html(html: str) -> List[Dict]:
    """从HTML中提取所有锚点内容块"""
    try:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        sections = []
        seen_ids = set()
        
        # 查找所有有ID的元素
        for elem in soup.find_all(attrs={'id': True}):
            elem_id = elem.get('id')
            if not elem_id or elem_id in seen_ids:
                continue
            
            seen_ids.add(elem_id)
            
            # 提取内容
            content = elem.get_text(separator='\n', strip=True)
            
            # 如果内容太短，尝试获取后续兄弟元素
            if len(content) < 100:
                sibling = elem.next_sibling
                depth = 0
                while sibling and depth < 10:
                    if hasattr(sibling, 'get_text'):
                        sibling_text = sibling.get_text(separator='\n', strip=True)
                        if len(sibling_text) > 50:
                            content += '\n\n' + sibling_text
                    sibling = getattr(sibling, 'next_sibling', None)
                    depth += 1
            
            # 获取标题
            title = elem_id
            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                title = elem.get_text(strip=True)
            else:
                # 查找最近的标题元素
                heading = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if heading:
                    title = heading.get_text(strip=True)
            
            # 提取代码块
            code_blocks = []
            for code_elem in elem.find_all(['pre', 'code']):
                code_text = code_elem.get_text(strip=True)
                if len(code_text) > 10:
                    code_blocks.append(code_text)
            
            if len(content) > 50:  # 至少50字符才保存
                sections.append({
                    'anchor_id': elem_id,
                    'title': title or elem_id,
                    'content': content[:50000],  # 限制长度
                    'code_blocks': code_blocks[:10],  # 最多10个代码块
                    'content_length': len(content),
                    'url': f"{BASE_URL}#{elem_id}"
                })
        
        return sections
    
    except Exception as e:
        print(f"⚠️ 提取锚点内容失败: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """主函数"""
    print("=" * 70)
    print("🕷️ 使用MCP工具完整爬取PTrade API文档")
    print("=" * 70)
    
    if not MCP_CLIENT_AVAILABLE:
        print("❌ MCPClient不可用")
        return
    
    if not KB_AVAILABLE:
        print("⚠️ 知识库工具不可用，将只保存到本地文件")
    
    # 加载内容哈希
    load_content_hashes()
    
    STATS['start_time'] = datetime.now()
    
    client = MCPClient()
    
    print(f"\n🚀 访问主页面: {START_URL}")
    
    # 使用Playwright直接抓取（因为Selenium可能有问题）
    print("   ⏳ 使用Playwright抓取主页面...")
    
    try:
        from playwright.async_api import async_playwright
        
        async def fetch_with_playwright():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True, timeout=30000)
                page = await browser.new_page()
                
                try:
                    await page.goto(START_URL, wait_until='networkidle', timeout=60000)
                    await page.wait_for_timeout(5000)  # 额外等待5秒
                    
                    html = await page.content()
                    title = await page.title()
                    
                    await browser.close()
                    
                    return {
                        'success': True,
                        'url': START_URL,
                        'title': title,
                        'html': html,
                        'text': ''  # 稍后从HTML提取
                    }
                except Exception as e:
                    await browser.close()
                    raise e
        
        data = asyncio.run(fetch_with_playwright())
        
        if not data.get('success'):
            print(f"❌ 抓取失败: {data.get('error', 'Unknown error')}")
            return
        
        print(f"   ✅ 主页面抓取成功")
        html = data.get('html', '')
        print(f"   HTML长度: {len(html)} 字符")
        
        if not html:
            print(f"⚠️ 警告: HTML为空，可能抓取失败")
            return
        
    except ImportError:
        print(f"❌ Playwright未安装")
        print(f"   请运行: pip install playwright && playwright install chromium")
        return
    except Exception as e:
        print(f"❌ Playwright抓取失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    STATS['pages_crawled'] += 1
    
    # 保存主页面
    main_page_file = OUTPUT_DIR / "main_page.json"
    main_page_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"   💾 已保存: {main_page_file}")
    
    # 提取锚点内容
    print(f"\n🔍 提取锚点内容块...")
    html = data.get('html', '')
    sections = extract_sections_from_html(html)
    
    STATS['sections_found'] = len(sections)
    print(f"   ✅ 找到 {len(sections)} 个内容块")
    
    if sections:
        print(f"\n📋 内容块列表（前20个）:")
        for i, section in enumerate(sections[:20], 1):
            print(f"   {i}. {section['title'][:50]} (ID: {section['anchor_id']}, {section['content_length']} 字符)")
        
        # 保存到知识库
        print(f"\n💾 保存到知识库...")
        print("=" * 70)
        
        for i, section in enumerate(sections, 1):
            print(f"\n[{i}/{len(sections)}] {section['title'][:50]}")
            
            # 保存到知识库
            if save_to_knowledge_base(section):
                STATS['sections_saved'] += 1
            
            # 保存到本地文件（备份）
            safe_anchor_id = re.sub(r'[<>:"/\\|?*]', '_', section['anchor_id'])
            safe_anchor_id = safe_anchor_id.replace(' ', '_')[:100]
            section_file = OUTPUT_DIR / f"section_{safe_anchor_id}.json"
            section_file.write_text(json.dumps(section, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 保存内容哈希
    save_content_hashes()
    
    # 打印统计
    print("\n" + "=" * 70)
    print("📊 爬取统计")
    print("=" * 70)
    print(f"抓取页面: {STATS['pages_crawled']}")
    print(f"找到内容块: {STATS['sections_found']}")
    print(f"存入知识库: {STATS['sections_saved']}")
    print(f"失败: {STATS['sections_failed']}")
    print(f"重复跳过: {STATS['duplicates_skipped']}")
    elapsed = datetime.now() - STATS['start_time']
    print(f"总耗时: {elapsed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
