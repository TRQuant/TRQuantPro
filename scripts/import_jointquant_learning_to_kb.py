#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将JointQuant_Learning仓库内容导入到RAG知识库

使用方法:
    python scripts/import_jointquant_learning_to_kb.py [--repo-path /path/to/repo]
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 使用MCPClient调用MCP工具（优先）
# 如果MCP调用失败，回退到直接函数调用
from core.mcp.client import MCPClient
from mcp_servers.unified_dev_server import knowledge_add as direct_knowledge_add

def read_markdown_file(file_path: Path) -> Dict[str, Any]:
    """读取Markdown文件并解析内容"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 提取标题（第一个#标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else file_path.stem
        
        # 提取描述（第一段非标题文本）
        lines = content.split('\n')
        description = ''
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('```'):
                description = line
                break
        
        return {
            'title': title,
            'content': content,
            'description': description,
            'file_path': str(file_path),
            'file_name': file_path.name
        }
    except Exception as e:
        print(f"  ⚠️ 读取文件失败: {e}")
        return None

def determine_type_and_tags(file_name: str, content: str) -> tuple:
    """根据文件名和内容确定类型和标签"""
    file_lower = file_name.lower()
    content_lower = content.lower()
    
    # 确定类型
    if '入门' in file_name or '什么是' in file_name:
        kb_type = 'lesson'
    elif '策略' in file_name:
        kb_type = 'practice'
    elif '因子' in file_name:
        kb_type = 'reference'
    elif '数据' in file_name:
        kb_type = 'reference'
    else:
        kb_type = 'lesson'
    
    # 确定标签
    tags = ['聚宽', 'JoinQuant', '量化交易', '学习文档']
    
    if '入门' in file_name or '什么是' in file_name:
        tags.append('入门教程')
    if '策略' in file_name:
        tags.append('策略开发')
        if '轮动' in file_name:
            tags.append('轮动策略')
        if '多股票' in file_name:
            tags.append('多股票策略')
    if '因子' in file_name:
        tags.append('因子分析')
    if '数据' in file_name:
        tags.append('数据获取')
    
    # 从内容中提取更多标签
    if 'python' in content_lower or '代码' in content_lower:
        tags.append('Python')
    if '回测' in content_lower:
        tags.append('回测')
    if '实盘' in content_lower:
        tags.append('实盘交易')
    
    return kb_type, tags

def import_repo_to_kb(repo_path: Path, dry_run: bool = False) -> Dict[str, Any]:
    """将仓库内容导入到知识库"""
    print('=' * 70)
    print('📚 JointQuant_Learning 知识库导入')
    print('=' * 70)
    print(f'仓库路径: {repo_path}')
    print(f'模式: {"预览模式（不实际添加）" if dry_run else "导入模式"}')
    print()
    
    # 查找所有Markdown文件
    md_files = list(repo_path.glob('*.md'))
    md_files = [f for f in md_files if f.name != 'README.md']  # 排除README
    
    print(f'📄 找到 {len(md_files)} 个Markdown文件')
    print()
    
    results = {
        'total': len(md_files),
        'success': 0,
        'failed': 0,
        'items': []
    }
    
    for i, md_file in enumerate(md_files, 1):
        print(f'[{i}/{len(md_files)}] 处理: {md_file.name}')
        
        # 读取文件
        file_data = read_markdown_file(md_file)
        if not file_data:
            results['failed'] += 1
            continue
        
        # 确定类型和标签
        kb_type, tags = determine_type_and_tags(md_file.name, file_data['content'])
        
        # 构建知识库条目
        kb_item = {
            'title': f"聚宽学习 - {file_data['title']}",
            'content': file_data['content'],
            'type': kb_type,
            'tags': tags,
            'source': f"https://github.com/LHospitalLKY/JointQuant_Learning/blob/master/{md_file.name}"
        }
        
        if dry_run:
            print(f'  📋 标题: {kb_item["title"]}')
            print(f'  📁 类型: {kb_item["type"]}')
            print(f'  🏷️  标签: {", ".join(kb_item["tags"])}')
            print(f'  📝 内容长度: {len(kb_item["content"])} 字符')
            results['items'].append(kb_item)
        else:
            # 优先使用MCP工具调用，失败则回退到直接函数调用
            success = False
            kb_id = None
            
            # 方式1: 尝试MCP工具调用
            try:
                print(f'  📞 [MCP工具] 调用: knowledge.add')
                print(f'     参数: title="{kb_item["title"][:40]}..."')
                
                client = MCPClient()
                mcp_result = client.call(
                    tool_name='knowledge.add',
                    arguments={
                        'title': kb_item['title'],
                        'content': kb_item['content'],
                        'type': kb_item['type'],
                        'tags': kb_item['tags'],
                        'source': kb_item['source']
                    },
                    timeout=30.0
                )
                
                print(f'     Trace ID: {mcp_result.trace_id}')
                print(f'     耗时: {mcp_result.duration:.2f}秒')
                
                if mcp_result.success:
                    result_data = mcp_result.data
                    if isinstance(result_data, str):
                        import json
                        try:
                            result_data = json.loads(result_data)
                        except:
                            result_data = {'raw': result_data}
                    
                    if result_data.get('success') or result_data.get('knowledge_id'):
                        kb_id = result_data.get('knowledge_id') or result_data.get('id', 'unknown')
                        print(f'  ✅ [MCP工具] 成功 (ID: {kb_id})')
                        success = True
                    else:
                        error_msg = result_data.get('error', 'Unknown error')
                        print(f'  ⚠️  [MCP工具] 返回错误: {error_msg}，尝试直接函数调用...')
                else:
                    print(f'  ⚠️  [MCP工具] 调用失败: {mcp_result.error}，尝试直接函数调用...')
            except Exception as e:
                print(f'  ⚠️  [MCP工具] 异常: {e}，尝试直接函数调用...')
            
            # 方式2: 如果MCP调用失败，回退到直接函数调用
            if not success:
                try:
                    print(f'  📞 [直接调用] knowledge_add函数')
                    result = direct_knowledge_add(
                        title=kb_item['title'],
                        content=kb_item['content'],
                        type=kb_item['type'],
                        tags=kb_item['tags'],
                        source=kb_item['source']
                    )
                    
                    if result.get('success') or result.get('knowledge_id'):
                        kb_id = result.get('knowledge_id') or result.get('id', 'unknown')
                        print(f'  ✅ [直接调用] 成功 (ID: {kb_id})')
                        success = True
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        print(f'  ❌ [直接调用] 失败: {error_msg}')
                except Exception as e:
                    print(f'  ❌ [直接调用] 异常: {e}')
                    import traceback
                    traceback.print_exc()
            
            # 记录结果
            if success:
                results['success'] += 1
                results['items'].append(kb_item)
            else:
                results['failed'] += 1
        
        print()
    
    # 打印总结
    print('=' * 70)
    print('📊 导入结果')
    print('=' * 70)
    print(f'总计: {results["total"]} 个文件')
    print(f'成功: {results["success"]} 个')
    print(f'失败: {results["failed"]} 个')
    print('=' * 70)
    
    return results

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将JointQuant_Learning仓库导入到知识库')
    parser.add_argument('--repo-path', type=str, 
                       default='/tmp/JointQuant_Learning',
                       help='仓库路径（默认: /tmp/JointQuant_Learning）')
    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，不实际添加')
    parser.add_argument('--clone', action='store_true',
                       help='自动克隆仓库（如果不存在）')
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    
    # 如果指定了--clone且路径不存在，则克隆
    if args.clone and not repo_path.exists():
        print(f'📥 克隆仓库到: {repo_path}...')
        import subprocess
        result = subprocess.run(
            ['git', 'clone', 'https://github.com/LHospitalLKY/JointQuant_Learning.git', str(repo_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f'❌ 克隆失败: {result.stderr}')
            return
        print('✅ 克隆成功')
    
    if not repo_path.exists():
        print(f'❌ 仓库路径不存在: {repo_path}')
        print('💡 提示: 使用 --clone 参数自动克隆，或手动克隆后指定 --repo-path')
        return
    
    # 导入到知识库
    import_repo_to_kb(repo_path, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
