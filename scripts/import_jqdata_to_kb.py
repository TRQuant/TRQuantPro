#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API文档快速导入知识库

将已爬取的233个JQData文档批量导入知识库
支持量化研究9步工作流的分类标签

Author: TRQuant Team
Date: 2026-01-01
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 知识库导入
try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False

# 文档目录
DOC_DIR = PROJECT_ROOT / "docs" / "jqdata_crawled"


def classify_document(filename: str, content: str) -> List[str]:
    """根据文件名和内容分类文档，返回标签列表"""
    tags = ['JQData', '聚宽数据', '官方文档']
    
    filename_lower = filename.lower()
    content_lower = content[:3000].lower()
    
    # === 因子相关（步骤4：因子构建）===
    if 'alpha' in filename_lower or 'alpha' in content_lower[:500]:
        tags.append('因子构建')
        tags.append('Alpha因子')
        if '101' in filename_lower or 'alpha101' in content_lower:
            tags.append('Alpha101')
        if '191' in filename_lower or 'alpha191' in content_lower:
            tags.append('Alpha191')
    
    if '因子' in filename or '因子' in content[:500]:
        tags.append('因子构建')
        tags.append('因子库')
    
    if '风险' in filename or '风险模型' in content[:500] or 'cne' in filename_lower:
        tags.append('风险模型')
        if 'cne5' in filename_lower or 'cne5' in content_lower:
            tags.append('CNE5风格因子')
        if 'cne6' in filename_lower or 'cne6' in content_lower:
            tags.append('CNE6风格因子')
    
    # === 市场数据（步骤1：市场趋势判断）===
    if '宏观' in filename or '宏观' in content[:500]:
        tags.append('市场趋势')
        tags.append('宏观经济数据')
    
    if '指数' in filename or '指数数据' in content[:500]:
        tags.append('市场趋势')
        tags.append('指数数据')
    
    if '行情' in filename or '行情数据' in content[:500]:
        tags.append('行情数据')
        tags.append('回测数据')
    
    # === 行业数据（步骤2：主线识别）===
    if '行业' in filename or '行业' in content[:500]:
        tags.append('主线识别')
        tags.append('行业数据')
    
    if '板块' in filename or '概念' in filename:
        tags.append('主线识别')
        tags.append('板块数据')
    
    # === 股票筛选（步骤3：候选池）===
    if '股票' in filename or '股票数据' in content[:500]:
        tags.append('候选池')
        tags.append('股票数据')
    
    if '财务' in filename or '财务数据' in content[:500]:
        tags.append('候选池')
        tags.append('财务数据')
    
    if '筛选' in content[:500] or 'query' in content_lower[:500]:
        tags.append('候选池')
        tags.append('数据筛选')
    
    # === 技术指标（步骤4&5：因子&策略）===
    if '技术' in filename or '技术指标' in content[:500]:
        tags.append('因子构建')
        tags.append('技术指标')
    
    # === 交易函数（步骤5：策略生成）===
    if '交易' in content[:500] or '下单' in content[:500]:
        tags.append('策略生成')
        tags.append('交易函数')
    
    # === 回测数据（步骤6：回测）===
    if '历史' in content[:500] or '分钟' in filename or 'tick' in filename_lower:
        tags.append('回测数据')
    
    if '分钟' in filename or 'tick' in filename_lower:
        tags.append('高频数据')
    
    # === 其他市场数据 ===
    if '期货' in filename or '期货' in content[:500]:
        tags.append('期货数据')
    
    if '基金' in filename or '基金' in content[:500]:
        tags.append('基金数据')
    
    if '期权' in filename or '期权' in content[:500]:
        tags.append('期权数据')
    
    if '债券' in filename or '债券' in content[:500]:
        tags.append('债券数据')
    
    # 去重并保持顺序
    return list(dict.fromkeys(tags))


def parse_document(filepath: Path) -> Dict:
    """解析文档文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析头部元数据
        lines = content.split('\n')
        url = ''
        title = filepath.stem
        
        for line in lines[:10]:
            if line.startswith('URL:'):
                url = line.replace('URL:', '').strip()
            elif line.startswith('标题:'):
                title = line.replace('标题:', '').strip()
        
        # 获取正文（跳过头部）
        body_start = content.find('=' * 70)
        if body_start > 0:
            body = content[body_start + 70:].strip()
        else:
            body = content
        
        return {
            'filepath': str(filepath),
            'filename': filepath.name,
            'title': title,
            'url': url,
            'content': body,
            'content_length': len(body)
        }
    except Exception as e:
        print(f"❌ 解析失败 {filepath}: {e}")
        return None


def import_to_knowledge_base(doc: Dict, tags: List[str]) -> bool:
    """将文档导入知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        # 构建结构化内容
        kb_content = f"""# {doc['title']}

## 基本信息
- **URL**: {doc['url']}
- **来源文件**: {doc['filename']}
- **内容长度**: {doc['content_length']} 字符
- **导入时间**: {datetime.now().isoformat()}

## 工作流标签
{', '.join(tags)}

## 内容

{doc['content']}
"""
        
        result = knowledge_add(
            title=doc['title'],
            content=kb_content,
            type='api_reference',
            tags=tags,
            source=doc['url'] or doc['filename']
        )
        
        return result.get('success') or result.get('id') or result.get('knowledge_id')
    except Exception as e:
        print(f"    ⚠️ 导入失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("聚宽API文档快速导入知识库")
    print("=" * 70)
    print(f"文档目录: {DOC_DIR}")
    print(f"知识库可用: {'✅ 是' if KB_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    # 获取所有文档
    doc_files = sorted(DOC_DIR.glob("*.txt"))
    total = len(doc_files)
    print(f"📄 发现 {total} 个文档待导入")
    print()
    
    # 统计
    stats = {
        'total': total,
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # 按工作流分类统计
    workflow_stats = {
        '市场趋势': 0,
        '主线识别': 0,
        '候选池': 0,
        '因子构建': 0,
        '策略生成': 0,
        '回测数据': 0
    }
    
    # 处理每个文档
    for i, filepath in enumerate(doc_files, 1):
        print(f"[{i}/{total}] {filepath.name[:50]}...")
        
        # 解析文档
        doc = parse_document(filepath)
        if not doc:
            stats['failed'] += 1
            continue
        
        # 分类
        tags = classify_document(filepath.name, doc['content'])
        print(f"    标签: {', '.join(tags[:5])}...")
        
        # 统计工作流覆盖
        for wf in workflow_stats:
            if wf in tags:
                workflow_stats[wf] += 1
        
        # 导入知识库
        if KB_AVAILABLE:
            if import_to_knowledge_base(doc, tags):
                stats['success'] += 1
                print(f"    ✅ 已导入")
            else:
                stats['failed'] += 1
                print(f"    ❌ 导入失败")
        else:
            stats['skipped'] += 1
    
    # 保存分类结果
    summary = {
        'timestamp': datetime.now().isoformat(),
        'stats': stats,
        'workflow_coverage': workflow_stats,
        'documents': [
            {
                'filename': f.name,
                'tags': classify_document(f.name, open(f, 'r', encoding='utf-8').read()[:3000])
            }
            for f in doc_files[:50]  # 只保存前50个示例
        ]
    }
    
    summary_file = DOC_DIR / "import_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 打印统计
    print()
    print("=" * 70)
    print("导入完成 - 统计信息")
    print("=" * 70)
    print(f"总文档数: {stats['total']}")
    print(f"成功导入: {stats['success']}")
    print(f"失败: {stats['failed']}")
    print(f"跳过: {stats['skipped']}")
    print()
    print("📊 工作流覆盖统计:")
    for wf, count in workflow_stats.items():
        print(f"  {wf}: {count} 个文档")
    print()
    print(f"📄 分类摘要: {summary_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()

