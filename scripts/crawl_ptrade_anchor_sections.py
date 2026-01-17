#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTrade API文档锚点内容提取脚本

功能：
1. 从主页面提取所有锚点链接对应的内容块
2. 将每个锚点内容作为独立的知识库条目
3. 存入RAG知识库

Author: TRQuant Team
Date: 2026-01-09
"""

import sys
import asyncio
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装")

try:
    # 优先使用MCP Client调用kb工具
    from core.mcp.client import MCPClient
    MCP_CLIENT_AVAILABLE = True
    KB_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    try:
        # 回退到直接函数调用
        from mcp_servers.unified_dev_server import knowledge_add
        KB_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ 知识库工具不可用: {e}")
        KB_AVAILABLE = False

BASE_URL = "https://ptradeapi.com"
START_URL = "https://ptradeapi.com/"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "ptrade_crawled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATS = {
    "sections_found": 0,
    "sections_saved": 0,
    "sections_failed": 0,
    "duplicates_skipped": 0,
}

content_hashes: Set[str] = set()


def load_content_hashes():
    """加载内容哈希"""
    global content_hashes
    hash_file = OUTPUT_DIR / "anchor_content_hashes.json"
    if hash_file.exists():
        try:
            content_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass


def save_content_hashes():
    """保存内容哈希"""
    hash_file = OUTPUT_DIR / "anchor_content_hashes.json"
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
    
    if '委托' in title or 'order' in anchor_id.lower():
        tags.append('委托下单')
    
    if '持仓' in title or 'position' in anchor_id.lower():
        tags.append('持仓查询')
    
    if '财务' in title or 'fundamental' in anchor_id.lower():
        tags.append('财务数据')
    
    if '历史' in title or 'history' in anchor_id.lower():
        tags.append('历史数据')
    
    if '定时' in title or 'schedule' in anchor_id.lower() or 'run_daily' in content:
        tags.append('定时任务')
    
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
                # 使用MCP Client调用kb工具
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
                        import json
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


async def extract_anchor_sections(page) -> List[Dict]:
    """提取所有锚点内容块"""
    try:
        # 等待页面完全加载
        await page.wait_for_load_state('networkidle', timeout=60000)
        await asyncio.sleep(3)
        
        # 使用JavaScript提取所有锚点内容
        sections_data = await page.evaluate('''
            () => {
                const sections = [];
                const seenIds = new Set();
                
                // 查找所有可能的锚点元素
                const anchorSelectors = [
                    '[id]',
                    '[name]',
                    'h1[id]',
                    'h2[id]',
                    'h3[id]',
                    'h4[id]',
                    '.section',
                    '.content-section',
                ];
                
                // 查找所有有ID的元素（可能是锚点目标）
                const allElements = document.querySelectorAll('[id]');
                
                allElements.forEach(elem => {
                    const id = elem.id;
                    if (!id || seenIds.has(id)) return;
                    seenIds.add(id);
                    
                    // 提取该元素及其后续内容（直到下一个同级或父级元素）
                    let content = '';
                    let codeBlocks = [];
                    
                    // 获取元素文本
                    content = elem.innerText || elem.textContent || '';
                    
                    // 如果内容太短，尝试获取后续兄弟元素
                    if (content.length < 100) {
                        let sibling = elem.nextElementSibling;
                        let depth = 0;
                        while (sibling && depth < 10) {
                            const siblingText = sibling.innerText || sibling.textContent || '';
                            if (siblingText.length > 50) {
                                content += '\\n\\n' + siblingText;
                            }
                            sibling = sibling.nextElementSibling;
                            depth++;
                        }
                    }
                    
                    // 提取代码块
                    const codeElems = elem.querySelectorAll('pre code, code');
                    codeElems.forEach(codeElem => {
                        const codeText = codeElem.innerText || codeElem.textContent || '';
                        if (codeText && codeText.length > 10) {
                            codeBlocks.push(codeText);
                        }
                    });
                    
                    // 获取标题
                    let title = '';
                    if (elem.tagName && ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'].includes(elem.tagName)) {
                        title = elem.innerText || elem.textContent || '';
                    } else {
                        // 查找最近的标题元素
                        let heading = elem.querySelector('h1, h2, h3, h4, h5, h6');
                        if (heading) {
                            title = heading.innerText || heading.textContent || '';
                        } else {
                            // 向上查找标题
                            let parent = elem.parentElement;
                            for (let i = 0; i < 3 && parent; i++) {
                                heading = parent.querySelector('h1, h2, h3, h4, h5, h6');
                                if (heading) {
                                    title = heading.innerText || heading.textContent || '';
                                    break;
                                }
                                parent = parent.parentElement;
                            }
                        }
                    }
                    
                    if (content.length > 50) {  // 至少50字符才保存
                        sections.push({
                            anchor_id: id,
                            title: title || id,
                            content: content.substring(0, 50000),  // 限制长度
                            code_blocks: codeBlocks.slice(0, 10),  // 最多10个代码块
                            content_length: content.length
                        });
                    }
                });
                
                return sections;
            }
        ''')
        
        return sections_data
    
    except Exception as e:
        print(f"⚠️ 提取锚点内容失败: {e}")
        import traceback
        traceback.print_exc()
        return []


async def main():
    """主函数"""
    print("=" * 70)
    print("📚 PTrade API文档锚点内容提取脚本")
    print("=" * 70)
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    if not KB_AVAILABLE:
        print("⚠️ 知识库工具不可用，将只保存到本地文件")
    
    # 加载内容哈希
    load_content_hashes()
    
    print(f"\n🚀 访问主页面: {START_URL}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=30000)
        
        try:
            page = await browser.new_page()
            
            print("   ⏳ 加载页面...")
            await page.goto(START_URL, wait_until='networkidle', timeout=60000)
            print("   ✅ 页面加载完成")
            
            print("   ⏳ 等待页面稳定...")
            await asyncio.sleep(5)
            
            print("   🔍 提取锚点内容块...")
            sections = await extract_anchor_sections(page)
            
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
                
                # 添加URL
                section['url'] = f"{START_URL}#{section['anchor_id']}"
                
                # 保存到知识库
                if save_to_knowledge_base(section):
                    print(f"  ✅ 已存入知识库")
                
                # 保存到本地文件（备份）
                # 清理文件名中的特殊字符
                safe_anchor_id = re.sub(r'[<>:"/\\|?*]', '_', section['anchor_id'])
                safe_anchor_id = safe_anchor_id.replace(' ', '_')[:100]  # 限制长度
                section_file = OUTPUT_DIR / f"section_{safe_anchor_id}.json"
                section_file.write_text(json.dumps(section, ensure_ascii=False, indent=2), encoding='utf-8')
            
            await page.close()
        
        finally:
            await browser.close()
    
    # 保存内容哈希
    save_content_hashes()
    
    # 打印统计
    print("\n" + "=" * 70)
    print("📊 提取统计")
    print("=" * 70)
    print(f"找到内容块: {STATS['sections_found']}")
    print(f"存入知识库: {STATS['sections_saved']}")
    print(f"失败: {STATS['sections_failed']}")
    print(f"重复跳过: {STATS['duplicates_skipped']}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
