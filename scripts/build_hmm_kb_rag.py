#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HMM知识库RAG构建脚本
====================
将HMM知识库文档转换为RAG知识库条目，并构建向量索引
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

def parse_hmm_markdown(md_file: Path) -> List[Dict[str, Any]]:
    """
    解析HMM知识库Markdown文档，按章节切分
    
    Args:
        md_file: Markdown文件路径
        
    Returns:
        知识库条目列表
    """
    content = md_file.read_text(encoding='utf-8')
    
    # 按H2章节切分
    sections = []
    current_section = None
    current_content = []
    current_level = 0
    
    for line in content.split('\n'):
        # 检测标题层级
        if line.startswith('## '):
            # 保存上一个章节
            if current_section and current_content:
                sections.append({
                    'title': current_section,
                    'content': '\n'.join(current_content).strip(),
                    'level': current_level
                })
            # 开始新章节
            current_section = line[3:].strip()
            current_level = 2
            current_content = []
        elif line.startswith('### '):
            # H3作为子章节，追加到当前内容
            if current_section:
                current_content.append(line)
        elif current_section:
            current_content.append(line)
    
    # 保存最后一个章节
    if current_section and current_content:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip(),
            'level': current_level
        })
    
    return sections

def create_kb_items(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将章节转换为知识库条目
    
    Args:
        sections: 章节列表
        
    Returns:
        知识库条目列表
    """
    kb_items = []
    
    for i, section in enumerate(sections):
        title = section['title']
        content = section['content']
        
        # 基础标签
        tags = [
            "HMM",
            "隐马尔可夫模型",
            "市场状态识别",
            "机器学习",
            "金融模型",
            "TRQuant",
            "知识库"
        ]
        
        # 根据章节标题添加特定标签
        title_lower = title.lower()
        if '理论' in title or '基础' in title:
            tags.extend(['理论基础', '数学', '算法原理'])
        if '金融' in title or '应用' in title:
            tags.extend(['金融应用', '量化交易', '市场分析'])
        if '实现' in title or 'TRQuant' in title:
            tags.extend(['代码实现', '系统集成', 'API文档'])
        if '优化' in title or '参数' in title:
            tags.extend(['参数优化', '模型调优', '性能优化'])
        if '验证' in title or '交叉' in title:
            tags.extend(['交叉验证', '模型评估', '信号验证'])
        if '实践' in title or '最佳' in title:
            tags.extend(['最佳实践', '使用指南', '开发规范'])
        if 'Hamilton' in content or '1989' in content:
            tags.extend(['Hamilton模型', '制度转换', '经典论文'])
        
        # 创建知识库条目
        item = {
            "id": f"hmm_kb_{i+1:03d}",
            "title": f"HMM知识库: {title}",
            "content": content,
            "type": "reference",
            "tags": list(set(tags)),  # 去重
            "source": f"docs/HMM/HMM_KNOWLEDGE_BASE.md#{title}",
            "created_at": datetime.now().isoformat(),
            "useful_count": 0
        }
        
        kb_items.append(item)
    
    return kb_items

def add_to_knowledge_base(kb_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    将知识库条目添加到RAG知识库
    
    使用MCP工具或直接调用知识库API
    """
    try:
        # 尝试使用MCP工具
        from mcp_servers.unified_dev_server import knowledge_add
        
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for item in kb_items:
            try:
                result = knowledge_add(
                    title=item['title'],
                    content=item['content'],
                    type=item['type'],
                    tags=item['tags'],
                    source=item.get('source', '')
                )
                
                if result.get('success') or result.get('id') or result.get('knowledge_id'):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{item['title']}: {result.get('error', 'Unknown error')}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{item['title']}: {str(e)}")
        
        return results
        
    except ImportError:
        # 如果MCP工具不可用，返回条目数据供手动处理
        return {
            'success': False,
            'message': 'MCP工具不可用，请手动添加',
            'items': kb_items
        }

def build_vector_index(kb_items: List[Dict[str, Any]], force_rebuild: bool = False) -> Dict[str, Any]:
    """
    构建向量索引
    
    Args:
        kb_items: 知识库条目列表
        force_rebuild: 是否强制重建
        
    Returns:
        构建结果
    """
    try:
        from mcp_servers.knowledge_vector_index import build_vector_index
        
        # 创建临时知识库JSON文件
        kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "hmm_knowledge_base.json"
        kb_file.parent.mkdir(parents=True, exist_ok=True)
        
        kb_data = {
            "items": kb_items,
            "metadata": {
                "name": "HMM知识库",
                "description": "隐马尔可夫模型(HMM)在金融市场状态识别中的应用",
                "created_at": datetime.now().isoformat(),
                "source": "docs/HMM/HMM_KNOWLEDGE_BASE.md"
            }
        }
        
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        
        # 构建向量索引
        result = build_vector_index(kb_file, force_rebuild=force_rebuild)
        return result
        
    except ImportError as e:
        return {
            'success': False,
            'error': f'向量索引模块不可用: {e}'
        }

def main():
    """主函数"""
    print("=" * 70)
    print("📚 HMM知识库RAG构建")
    print("=" * 70)
    
    # 1. 解析Markdown文档
    md_file = TRQUANT_ROOT / "docs" / "HMM" / "HMM_KNOWLEDGE_BASE.md"
    if not md_file.exists():
        print(f"❌ 文件不存在: {md_file}")
        return
    
    print(f"\n📄 解析文档: {md_file}")
    sections = parse_hmm_markdown(md_file)
    print(f"✅ 共切分 {len(sections)} 个章节")
    
    # 2. 创建知识库条目
    print("\n📝 创建知识库条目...")
    kb_items = create_kb_items(sections)
    print(f"✅ 共创建 {len(kb_items)} 个知识库条目")
    
    # 3. 保存为JSON文件（备份）
    output_file = TRQUANT_ROOT / "docs" / "HMM" / "hmm_kb_items.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kb_items, f, ensure_ascii=False, indent=2)
    print(f"✅ 知识库条目已保存: {output_file}")
    
    # 4. 添加到知识库（可选）
    print("\n💾 添加到RAG知识库...")
    add_result = add_to_knowledge_base(kb_items)
    if add_result.get('success') is not False:
        print(f"✅ 成功添加: {add_result.get('success', 0)} 个")
        if add_result.get('failed', 0) > 0:
            print(f"⚠️  失败: {add_result.get('failed', 0)} 个")
            for error in add_result.get('errors', [])[:5]:
                print(f"   - {error}")
    else:
        print(f"⚠️  {add_result.get('message', '添加失败')}")
    
    # 5. 构建向量索引（可选）
    print("\n🔍 构建向量索引...")
    index_result = build_vector_index(kb_items, force_rebuild=False)
    if index_result.get('success'):
        print(f"✅ 向量索引构建成功")
        print(f"   条目数: {index_result.get('items_count', 0)}")
        print(f"   模型: {index_result.get('model', 'N/A')}")
        print(f"   维度: {index_result.get('embedding_dim', 'N/A')}")
    else:
        print(f"⚠️  向量索引构建失败: {index_result.get('error', 'Unknown error')}")
        print("   提示: 需要安装 sentence-transformers 和 chromadb")
    
    print("\n" + "=" * 70)
    print("✅ HMM知识库RAG构建完成!")
    print("=" * 70)

if __name__ == "__main__":
    main()

