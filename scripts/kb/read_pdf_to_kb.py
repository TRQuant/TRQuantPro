#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用PDF读取工具直接读取PDF并导入到向量知识库
==============================================

功能：
1. 读取PDF文件（支持多种PDF库）
2. 智能分段
3. 直接添加到向量知识库
"""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import hashlib

# 确保可从任意工作目录运行
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


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
                text_content.append(text)
        
        doc.close()
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用PyMuPDF成功读取 {len(doc)} 页")
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
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用pdfplumber成功读取 {len(pdf.pages)} 页")
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
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        full_text = '\n\n'.join(text_content)
        print(f"✅ 使用PyPDF2成功读取 {len(pdf.pages)} 页")
        return full_text
        
    except ImportError:
        raise ImportError("未安装任何PDF库，请安装: pip install pymupdf 或 pip install pdfplumber 或 pip install PyPDF2")
    except Exception as e:
        raise Exception(f"所有PDF库都读取失败: {e}")


def parse_pdf_text(text: str) -> List[Dict[str, Any]]:
    """
    解析PDF文本内容，智能分段
    
    返回格式：
    [
        {
            "title": "段落标题",
            "content": "段落内容",
            "type": "knowledge_type",
            "tags": ["tag1", "tag2"]
        },
        ...
    ]
    """
    sections = []
    
    # 按一级标题分割
    parts = re.split(r'^#\s+(.+)$', text, flags=re.MULTILINE)
    
    # 第一部分是标题
    main_title = parts[0].strip() if parts else "PDF文档"
    
    # 处理每个主要章节
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
            
        section_title = parts[i].strip()
        section_content = parts[i + 1].strip()
        
        # 进一步按二级标题分割
        subsections = re.split(r'^##\s+(.+)$', section_content, flags=re.MULTILINE)
        
        if len(subsections) == 1:
            # 没有子标题，整个作为一个条目
            entry = _create_kb_entry(
                title=f"{main_title} - {section_title}",
                content=section_content,
                type="lesson",
                tags=_infer_tags_from_content(section_title, section_content)
            )
            sections.append(entry)
        else:
            # 有子标题，每个子标题作为一个条目
            for j in range(1, len(subsections), 2):
                if j + 1 >= len(subsections):
                    break
                    
                subsection_title = subsections[j].strip()
                subsection_content = subsections[j + 1].strip()
                
                entry = _create_kb_entry(
                    title=f"{main_title} - {section_title} - {subsection_title}",
                    content=subsection_content,
                    type=_infer_type(subsection_title),
                    tags=_infer_tags_from_content(subsection_title, subsection_content)
                )
                sections.append(entry)
    
    # 如果没有找到标题结构，按段落分割
    if not sections:
        paragraphs = re.split(r'\n\s*\n+', text)
        for i, para in enumerate(paragraphs):
            if len(para.strip()) > 100:  # 只保留较长的段落
                entry = _create_kb_entry(
                    title=f"{main_title} - 段落 {i+1}",
                    content=para.strip(),
                    type="lesson",
                    tags=_infer_tags_from_content("", para)
                )
                sections.append(entry)
    
    return sections


def _create_kb_entry(title: str, content: str, type: str, tags: List[str]) -> Dict[str, Any]:
    """创建知识库条目"""
    return {
        "title": title,
        "content": content,
        "type": type,
        "tags": tags
    }


def _infer_type(section_title: str) -> str:
    """根据章节标题推断知识类型"""
    title_lower = section_title.lower()
    
    if "风险" in section_title or "风险因素" in section_title:
        return "practice"
    elif "财务" in section_title or "数据" in section_title or "财务数据" in section_title:
        return "lesson"
    elif "估值" in section_title or "估值分析" in section_title:
        return "lesson"
    elif "投资建议" in section_title or "结论" in section_title or "建议" in section_title:
        return "practice"
    elif "行业前景" in section_title or "前景" in section_title:
        return "lesson"
    else:
        return "lesson"


def _infer_tags_from_content(section_title: str, content: str) -> List[str]:
    """根据章节标题和内容推断标签"""
    tags = []
    
    title_lower = section_title.lower()
    content_lower = content.lower()
    
    # 股票相关标签
    if "兴业银锡" in content or "000426" in content:
        tags.extend(["兴业银锡", "000426", "投资分析"])
    
    # 行业标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["有色金属", "矿业", "银", "锡", "资源"]):
        tags.extend(["有色金属", "矿业", "资源股"])
    
    # 财务标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["财务", "营收", "净利润", "现金流", "毛利率"]):
        tags.append("财务分析")
    
    # 估值标签
    if any(keyword in title_lower or keyword in content_lower 
           for keyword in ["估值", "PE", "PB", "EV/EBITDA", "市盈率", "市净率"]):
        tags.append("估值分析")
    
    # 风险标签
    if "风险" in title_lower:
        tags.append("风险分析")
    
    # 投资建议标签
    if any(keyword in title_lower 
           for keyword in ["投资建议", "结论", "建议"]):
        tags.append("投资建议")
    
    return list(dict.fromkeys(tags))  # 去重


def add_to_knowledge_base(entries: List[Dict[str, Any]], source: str = None) -> Dict[str, Any]:
    """
    直接添加到知识库JSON文件（不依赖MCP SDK）
    """
    # 知识库文件路径
    kb_dir = _PROJECT_ROOT / ".trquant" / "dev" / "knowledge"
    kb_dir.mkdir(parents=True, exist_ok=True)
    kb_file = kb_dir / "knowledge_base.json"
    
    # 加载现有知识库
    if kb_file.exists():
        try:
            kb = json.loads(kb_file.read_text(encoding='utf-8'))
        except:
            kb = {"items": [], "stats": {"total": 0, "by_type": {}}}
    else:
        kb = {"items": [], "stats": {"total": 0, "by_type": {}}}
    
    results = {
        'success': 0,
        'failed': 0,
        'errors': [],
        'knowledge_ids': []
    }
    
    for entry in entries:
        try:
            # 生成ID
            kb_id = f"kb_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(entry['title'].encode()).hexdigest()[:8]}"
            
            # 创建条目
            item = {
                "id": kb_id,
                "title": entry['title'],
                "content": entry['content'],
                "type": entry['type'],
                "tags": entry['tags'],
                "source": source or "PDF文档",
                "useful_count": 0,
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            }
            
            # 添加到知识库
            kb["items"].insert(0, item)
            kb["stats"]["total"] = len(kb["items"])
            kb["stats"]["by_type"][entry['type']] = kb["stats"]["by_type"].get(entry['type'], 0) + 1
            
            results['success'] += 1
            results['knowledge_ids'].append(kb_id)
            print(f"✅ 已添加: {entry['title'][:50]}... (ID: {kb_id})")
            
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{entry['title']}: {str(e)}")
            print(f"❌ 异常: {entry['title'][:50]}... - {str(e)}")
    
    # 保存知识库
    kb_file.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding='utf-8')
    
    return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="读取PDF文件并导入到向量知识库")
    parser.add_argument("pdf_path", type=str, help="PDF文件路径")
    parser.add_argument("--source", type=str, default=None, help="来源标识（可选）")
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_path)
    
    print("=" * 80)
    print("📚 PDF文件读取并导入到向量知识库")
    print("=" * 80)
    print()
    
    # 1. 读取PDF
    print("📄 步骤1: 读取PDF文件...")
    try:
        pdf_text = read_pdf(pdf_path)
        print(f"   读取成功，文本长度: {len(pdf_text)} 字符")
        print()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return
    
    # 2. 解析文本
    print("📋 步骤2: 解析PDF文本内容...")
    entries = parse_pdf_text(pdf_text)
    print(f"   共解析出 {len(entries)} 个知识条目")
    print()
    
    # 3. 显示条目预览
    if entries:
        print("📋 步骤3: 知识条目预览...")
        for i, entry in enumerate(entries[:5], 1):
            print(f"   {i}. {entry['title']}")
            print(f"      类型: {entry['type']}, 标签: {', '.join(entry['tags'][:5])}")
            print(f"      内容: {entry['content'][:100]}...")
            print()
        
        if len(entries) > 5:
            print(f"   ... 还有 {len(entries) - 5} 个条目")
            print()
    
    # 4. 添加到知识库
    print("💾 步骤4: 添加到向量知识库...")
    source = args.source or f"PDF: {pdf_path.name}"
    results = add_to_knowledge_base(entries, source=source)
    
    # 5. 显示结果
    print()
    print("=" * 80)
    print("📊 导入结果汇总")
    print("=" * 80)
    print(f"✅ 成功: {results.get('success', 0)} 条")
    print(f"❌ 失败: {results.get('failed', 0)} 条")
    
    if results.get('errors'):
        print()
        print("❌ 错误详情:")
        for error in results['errors'][:5]:
            print(f"   - {error}")
        if len(results['errors']) > 5:
            print(f"   ... 还有 {len(results['errors']) - 5} 个错误")
    
    if results.get('knowledge_ids'):
        print()
        print("📝 知识库ID:")
        for kid in results['knowledge_ids'][:10]:
            print(f"   - {kid}")
        if len(results['knowledge_ids']) > 10:
            print(f"   ... 还有 {len(results['knowledge_ids']) - 10} 个ID")
    
    print()
    print("=" * 80)
    print("✅ 导入完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
