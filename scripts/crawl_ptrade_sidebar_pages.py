#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取PTrade API文档侧栏中的所有页面

功能：
1. 读取侧栏链接列表
2. 使用Playwright逐一爬取每个锚点页面
3. 提取内容并存入知识库

Author: TRQuant Team
Date: 2026-01-09
"""

import sys
import json
import asyncio
import hashlib
import re
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

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False

BASE_URL = "https://ptradeapi.com"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "ptrade_crawled" / "mcp_crawl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATS = {
    "total_links": 0,
    "crawled": 0,
    "saved_to_kb": 0,
    "failed": 0,
    "skipped": 0,
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
    url = section_data.get('url', '')
    
    # 根据标题和内容分类
    if '策略' in title or 'strategy' in url.lower():
        tags.append('策略开发')
    
    if '回测' in title or 'backtest' in url.lower():
        tags.append('回测')
    
    if '交易' in title or 'trade' in url.lower() or 'order' in content:
        tags.append('交易')
    
    if '数据' in title or 'data' in url.lower() or 'get_' in content:
        tags.append('数据')
    
    if 'API' in title or 'api' in url.lower():
        tags.append('API接口')
    
    if '入门' in title or '快速' in title:
        tags.append('快速入门')
    
    return list(dict.fromkeys(tags))


def save_to_knowledge_base(section_data: Dict) -> bool:
    """保存到知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        # 计算内容哈希
        content_hash = hashlib.md5(section_data['content'].encode('utf-8')).hexdigest()
        if content_hash in content_hashes:
            STATS['skipped'] += 1
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
            STATS['saved_to_kb'] += 1
            kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
            print(f"  ✅ 已存入知识库 (ID: {kb_id})")
            return True
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No result'
            print(f"  ❌ 知识库存储失败: {error_msg}")
            STATS['failed'] += 1
            return False
    
    except Exception as e:
        print(f"  ❌ 知识库存储异常: {e}")
        STATS['failed'] += 1
        return False


async def crawl_anchor_page(url: str, anchor_id: Optional[str] = None) -> Optional[Dict]:
    """爬取锚点页面"""
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, timeout=30000)
            page = await browser.new_page()
            
            try:
                # 访问页面
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(3000)  # 等待3秒
                
                # 提取锚点内容
                if anchor_id:
                    # 等待锚点元素加载
                    try:
                        await page.wait_for_selector(f'#{anchor_id}', timeout=5000)
                    except:
                        pass
                    
                    # 提取锚点内容
                    anchor_content = await page.evaluate(f'''
                        () => {{
                            const elem = document.getElementById('{anchor_id}');
                            if (!elem) return null;
                            
                            let content = '';
                            let codeBlocks = [];
                            
                            // 获取元素文本
                            content = elem.innerText || elem.textContent || '';
                            
                            // 如果内容太短，尝试获取后续兄弟元素
                            if (content.length < 100) {{
                                let sibling = elem.nextElementSibling;
                                let depth = 0;
                                while (sibling && depth < 20) {{
                                    const siblingText = sibling.innerText || sibling.textContent || '';
                                    if (siblingText.length > 50) {{
                                        content += '\\n\\n' + siblingText;
                                    }}
                                    sibling = sibling.nextElementSibling;
                                    depth++;
                                }}
                            }}
                            
                            // 提取代码块
                            const codeElems = elem.querySelectorAll('pre, code');
                            codeElems.forEach(code => {{
                                const codeText = code.innerText || code.textContent || '';
                                if (codeText.length > 10) {{
                                    codeBlocks.push(codeText);
                                }}
                            }});
                            
                            return {{
                                title: elem.innerText?.split('\\n')[0] || '{anchor_id}',
                                content: content,
                                codeBlocks: codeBlocks.slice(0, 10),
                                contentLength: content.length
                            }};
                        }}
                    ''')
                else:
                    # 提取整个页面主要内容
                    anchor_content = await page.evaluate('''
                        () => {
                            const mainContent = document.querySelector('main, .content, #content, .main-content');
                            if (!mainContent) return null;
                            
                            let content = mainContent.innerText || mainContent.textContent || '';
                            let codeBlocks = [];
                            
                            // 提取代码块
                            const codeElems = mainContent.querySelectorAll('pre, code');
                            codeElems.forEach(code => {
                                const codeText = code.innerText || code.textContent || '';
                                if (codeText.length > 10) {
                                    codeBlocks.push(codeText);
                                }
                            });
                            
                            return {
                                title: document.title || 'PTrade API',
                                content: content,
                                codeBlocks: codeBlocks.slice(0, 10),
                                contentLength: content.length
                            };
                        }
                    ''')
                
                html = await page.content()
                title = await page.title()
                
                await browser.close()
                
                if anchor_content:
                    return {
                        'success': True,
                        'url': url,
                        'title': title,
                        'html': html,
                        'anchor_content': anchor_content,
                        'anchor_id': anchor_id
                    }
                else:
                    return {
                        'success': True,
                        'url': url,
                        'title': title,
                        'html': html,
                        'anchor_content': None,
                        'anchor_id': anchor_id
                    }
                    
            except Exception as e:
                await browser.close()
                return {
                    'success': False,
                    'url': url,
                    'error': str(e)
                }
    
    except ImportError:
        return {
            'success': False,
            'url': url,
            'error': 'Playwright未安装'
        }
    except Exception as e:
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }


def main():
    """主函数"""
    print("=" * 70)
    print("🕷️ 爬取PTrade API文档侧栏页面")
    print("=" * 70)
    
    if not KB_AVAILABLE:
        print("⚠️ 知识库工具不可用，将只保存到本地文件")
    
    # 加载内容哈希
    load_content_hashes()
    
    STATS['start_time'] = datetime.now()
    
    # 读取侧栏链接列表
    links_file = OUTPUT_DIR / "sidebar_links.json"
    if not links_file.exists():
        print(f"❌ 链接列表文件不存在: {links_file}")
        print(f"   请先运行提取侧栏链接的脚本")
        return
    
    links = json.loads(links_file.read_text(encoding='utf-8'))
    
    # 过滤出锚点链接（以#开头的）
    anchor_links = [l for l in links if l['href'].startswith('#')]
    
    # 过滤掉已经爬取过的（从文件名判断）
    existing_files = {f.stem for f in OUTPUT_DIR.glob("section_*.json")}
    
    new_links = []
    for link in anchor_links:
        anchor_id = link['href'][1:]  # 去掉#
        safe_id = re.sub(r'[<>:"/\\|?*]', '_', anchor_id)
        file_stem = f"section_{safe_id}"
        
        if file_stem not in existing_files:
            new_links.append(link)
        else:
            print(f"⏭️  跳过已爬取: {link['text']} ({link['url']})")
    
    STATS['total_links'] = len(new_links)
    
    print(f"\n📋 待爬取链接: {len(new_links)} 个")
    print(f"⏭️  已跳过: {len(anchor_links) - len(new_links)} 个")
    
    if not new_links:
        print("\n✅ 所有链接已爬取完成！")
        return
    
    print(f"\n🚀 开始爬取...")
    print("=" * 70)
    
    # 逐一爬取
    for i, link in enumerate(new_links, 1):
        anchor_id = link['href'][1:]  # 去掉#
        url = link['url']
        text = link['text']
        
        print(f"\n[{i}/{len(new_links)}] {text}")
        print(f"   URL: {url}")
        print(f"   锚点ID: {anchor_id}")
        
        try:
            # 爬取页面
            data = asyncio.run(crawl_anchor_page(url, anchor_id))
            
            if not data or not data.get('success'):
                error = data.get('error', 'Unknown error') if data else 'No data'
                print(f"   ❌ 爬取失败: {error}")
                STATS['failed'] += 1
                continue
            
            STATS['crawled'] += 1
            
            # 保存页面
            safe_anchor_id = re.sub(r'[<>:"/\\|?*]', '_', anchor_id)
            safe_anchor_id = safe_anchor_id.replace(' ', '_')[:100]
            page_file = OUTPUT_DIR / f"anchor_page_{safe_anchor_id}.json"
            page_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            
            # 处理锚点内容
            anchor_content = data.get('anchor_content')
            if anchor_content:
                section_data = {
                    'anchor_id': anchor_id,
                    'title': anchor_content.get('title', text),
                    'content': anchor_content.get('content', '')[:50000],
                    'code_blocks': anchor_content.get('codeBlocks', []),
                    'content_length': anchor_content.get('contentLength', 0),
                    'url': url
                }
                
                # 保存内容块
                section_file = OUTPUT_DIR / f"section_{safe_anchor_id}.json"
                section_file.write_text(json.dumps(section_data, ensure_ascii=False, indent=2), encoding='utf-8')
                
                print(f"   ✅ 内容长度: {section_data['content_length']} 字符")
                
                # 存入知识库
                if save_to_knowledge_base(section_data):
                    pass  # 已在函数中打印
            else:
                print(f"   ⚠️ 未找到锚点内容")
        
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            STATS['failed'] += 1
            import traceback
            traceback.print_exc()
    
    # 保存内容哈希
    save_content_hashes()
    
    # 打印统计
    print("\n" + "=" * 70)
    print("📊 爬取统计")
    print("=" * 70)
    print(f"总链接数: {STATS['total_links']}")
    print(f"成功爬取: {STATS['crawled']}")
    print(f"存入知识库: {STATS['saved_to_kb']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过（重复）: {STATS['skipped']}")
    elapsed = datetime.now() - STATS['start_time']
    print(f"总耗时: {elapsed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
