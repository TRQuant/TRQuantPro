#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
情绪因子与资金流向PDF知识库构建
================================

读取PDF文档，作为整体专题存入知识库
主题：聚宽、AKShare、情绪因子、资金流向
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.mcp.client import MCPClient
from mcp_servers.unified_dev_server import knowledge_add

# PDF文件路径
PDF_PATH = TRQUANT_ROOT / "docs/03_modules/如何利用情绪因子与资金流向数据辅助A股交易.pdf"

# MCP客户端
MCP_CLIENT_AVAILABLE = False
try:
    client = MCPClient()
    MCP_CLIENT_AVAILABLE = True
except:
    pass


def read_pdf(pdf_path: Path) -> str:
    """
    读取PDF文件内容
    
    支持多种PDF库：
    1. PyMuPDF (fitz) - 优先
    2. pdfplumber - 备用
    3. PyPDF2 - 最后备用
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    print(f"📄 正在读取PDF: {pdf_path}")
    
    # 方法1: PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        text_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(f"=== 第 {page_num + 1} 页 ===\n{text}\n")
        
        doc.close()
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用PyMuPDF成功读取 {len(doc)} 页")
        print(f"📊 文本长度: {len(full_text)} 字符")
        return full_text
        
    except ImportError:
        print("⚠️  PyMuPDF未安装，尝试pdfplumber...")
    except Exception as e:
        print(f"⚠️  PyMuPDF读取失败: {e}，尝试pdfplumber...")
    
    # 方法2: pdfplumber
    try:
        import pdfplumber
        text_content = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(f"=== 第 {page_num} 页 ===\n{text}\n")
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用pdfplumber成功读取 {len(pdf.pages)} 页")
        print(f"📊 文本长度: {len(full_text)} 字符")
        return full_text
        
    except ImportError:
        print("⚠️  pdfplumber未安装，尝试PyPDF2...")
    except Exception as e:
        print(f"⚠️  pdfplumber读取失败: {e}，尝试PyPDF2...")
    
    # 方法3: PyPDF2
    try:
        from PyPDF2 import PdfReader
        text_content = []
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(f"=== 第 {page_num} 页 ===\n{text}\n")
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用PyPDF2成功读取 {len(pdf.pages)} 页")
        print(f"📊 文本长度: {len(full_text)} 字符")
        return full_text
        
    except ImportError:
        raise ImportError("未安装任何PDF库，请安装: pip install pymupdf 或 pip install pdfplumber 或 pip install PyPDF2")
    except Exception as e:
        raise Exception(f"所有PDF库都读取失败: {e}")


def extract_keywords(content: str) -> list:
    """从内容中提取关键词，用于标签"""
    keywords = []
    content_lower = content.lower()
    
    # 平台相关
    if '聚宽' in content or 'joinquant' in content_lower or 'jqdata' in content_lower:
        keywords.append('聚宽')
        keywords.append('JoinQuant')
        keywords.append('JQData')
    
    if 'akshare' in content_lower or 'akshare' in content:
        keywords.append('AKShare')
        keywords.append('akshare')
    
    # 主题相关
    if '情绪' in content or 'sentiment' in content_lower:
        keywords.append('情绪因子')
        keywords.append('情绪分析')
    
    if '资金流向' in content or '资金流' in content or '资金' in content:
        keywords.append('资金流向')
        keywords.append('资金流')
    
    if '因子' in content:
        keywords.append('因子')
    
    if 'a股' in content_lower or 'a股' in content:
        keywords.append('A股')
    
    if '交易' in content or 'trading' in content_lower:
        keywords.append('交易策略')
    
    # 技术相关
    if 'api' in content_lower:
        keywords.append('API')
    
    if '数据' in content:
        keywords.append('数据获取')
    
    return list(set(keywords))  # 去重


def save_to_knowledge_base(title: str, content: str, tags: list, source: str) -> bool:
    """保存到知识库"""
    try:
        # 尝试MCP工具
        if MCP_CLIENT_AVAILABLE:
            result = client.call(
                tool_name='knowledge.add',
                arguments={
                    'title': title,
                    'content': content,
                    'type': 'lesson',  # 作为经验教训/教程
                    'tags': tags,
                    'source': source
                },
                timeout=60.0  # PDF内容可能较大，增加超时时间
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    data = json.loads(data)
                if data.get('success') or data.get('knowledge_id'):
                    print(f"    ✅ [MCP工具] 成功存入知识库 (ID: {data.get('knowledge_id', 'N/A')})")
                    return True
        
        # 回退到直接函数调用
        result = knowledge_add(
            title=title,
            content=content,
            type='lesson',
            tags=tags,
            source=source
        )
        
        if result.get('success') or result.get('knowledge_id'):
            print(f"    ✅ [直接函数] 成功存入知识库 (ID: {result.get('knowledge_id', 'N/A')})")
            return True
    except Exception as e:
        print(f"    ❌ 保存失败: {e}")
        return False
    
    return False


def main():
    """主函数"""
    print("=" * 70)
    print("📚 情绪因子与资金流向PDF知识库构建")
    print("=" * 70)
    print(f"PDF文件: {PDF_PATH}")
    print(f"MCP客户端可用: {'✅ 是' if MCP_CLIENT_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    # 1. 读取PDF
    print("📄 步骤1: 读取PDF文件")
    try:
        pdf_text = read_pdf(PDF_PATH)
        print(f"✅ 读取成功")
        print()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 2. 提取关键词和标签
    print("📋 步骤2: 提取关键词和标签")
    tags = extract_keywords(pdf_text)
    print(f"✅ 提取到 {len(tags)} 个标签: {', '.join(tags[:10])}")
    if len(tags) > 10:
        print(f"   ... 还有 {len(tags) - 10} 个标签")
    print()
    
    # 3. 构建知识库条目
    print("💾 步骤3: 存入知识库（作为整体专题）")
    title = "如何利用情绪因子与资金流向数据辅助A股交易"
    
    # 添加元数据到内容开头
    full_content = f"""# {title}

**来源**: {PDF_PATH.name}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**文档类型**: PDF专题文档
**主题**: 聚宽、AKShare、情绪因子、资金流向、A股交易

---

{pdf_text}
"""
    
    source = f"PDF: {PDF_PATH.name}"
    
    print(f"   标题: {title}")
    print(f"   内容长度: {len(full_content)} 字符")
    print(f"   标签: {', '.join(tags)}")
    print()
    
    success = save_to_knowledge_base(title, full_content, tags, source)
    
    # 4. 验证
    print()
    print("=" * 70)
    if success:
        print("✅ 知识库构建完成！")
        
        # 验证搜索
        if MCP_CLIENT_AVAILABLE:
            print()
            print("🔍 验证知识库搜索...")
            try:
                result = client.call(
                    tool_name='knowledge.search',
                    arguments={
                        'query': '情绪因子 资金流向',
                        'limit': 5
                    },
                    timeout=30.0
                )
                
                if result.success:
                    data = result.data
                    if isinstance(data, str):
                        data = json.loads(data)
                    items = data.get('items', []) or data.get('results', [])
                    print(f"   ✅ 搜索测试成功，找到 {len(items)} 条相关记录")
                    if items:
                        print(f"   📋 示例记录:")
                        for i, item in enumerate(items[:3], 1):
                            print(f"      {i}. {item.get('title', 'N/A')[:60]}")
            except Exception as e:
                print(f"   ⚠️ 搜索验证异常: {e}")
    else:
        print("❌ 知识库构建失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
