#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
归档已完成的计划文件
====================

自动检测并归档所有任务都已完成（status: completed）的计划文件到归档目录。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
from pathlib import Path
import yaml
import shutil
from datetime import datetime
from typing import List, Dict, Any

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

def parse_plan_file(plan_file: Path) -> Dict[str, Any]:
    """
    解析计划文件
    
    Args:
        plan_file: 计划文件路径
    
    Returns:
        Dict: 解析后的计划数据
    """
    try:
        content = plan_file.read_text(encoding='utf-8')
        
        # 分离frontmatter和内容
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                markdown_content = parts[2]
            else:
                frontmatter = {}
                markdown_content = content
        else:
            frontmatter = {}
            markdown_content = content
        
        return {
            'frontmatter': frontmatter or {},
            'content': markdown_content,
            'todos': frontmatter.get('todos', []) if isinstance(frontmatter, dict) else []
        }
    except Exception as e:
        print(f"⚠️ 解析计划文件失败 {plan_file.name}: {e}")
        return {'frontmatter': {}, 'content': '', 'todos': []}


def is_plan_completed(plan_data: Dict[str, Any]) -> bool:
    """
    检查计划是否全部完成
    
    Args:
        plan_data: 计划数据
    
    Returns:
        bool: 是否全部完成
    """
    todos = plan_data.get('todos', [])
    
    if not todos:
        # 如果没有todos，检查文件修改时间（超过30天未修改视为完成）
        return False
    
    # 检查所有todos是否都是completed
    all_completed = all(
        todo.get('status', '').lower() in ['completed', 'done', 'finished']
        for todo in todos
        if isinstance(todo, dict)
    )
    
    return all_completed and len(todos) > 0


def archive_plan(plan_file: Path, archive_dir: Path) -> bool:
    """
    归档计划文件
    
    Args:
        plan_file: 计划文件路径
        archive_dir: 归档目录
    
    Returns:
        bool: 是否成功
    """
    try:
        # 创建归档目录（按月份）
        now = datetime.now()
        month_dir = archive_dir / f"{now.year}-{now.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        
        # 移动文件
        dest_file = month_dir / plan_file.name
        shutil.move(str(plan_file), str(dest_file))
        
        return True
    except Exception as e:
        print(f"❌ 归档失败 {plan_file.name}: {e}")
        return False


def main(dry_run: bool = False):
    """主函数"""
    plans_dir = PROJECT_ROOT / ".cursor" / "plans"
    archive_dir = PROJECT_ROOT / ".cursor" / "archived_plans"
    
    if not plans_dir.exists():
        print(f"❌ 计划目录不存在: {plans_dir}")
        return
    
    print("=" * 80)
    print("归档已完成的计划文件")
    print("=" * 80)
    print(f"\n计划目录: {plans_dir}")
    print(f"归档目录: {archive_dir}")
    print(f"模式: {'试运行（不实际移动）' if dry_run else '实际归档'}\n")
    
    # 获取所有计划文件
    plan_files = list(plans_dir.glob("*.plan.md"))
    
    if not plan_files:
        print("✅ 没有找到计划文件")
        return
    
    print(f"📋 找到 {len(plan_files)} 个计划文件\n")
    
    # 分析每个计划文件
    completed_plans = []
    active_plans = []
    
    for plan_file in plan_files:
        # 跳过归档目录中的文件
        if 'archived' in str(plan_file):
            continue
        
        plan_data = parse_plan_file(plan_file)
        is_completed = is_plan_completed(plan_data)
        
        plan_name = plan_data.get('frontmatter', {}).get('name', plan_file.stem)
        todos_count = len(plan_data.get('todos', []))
        
        if is_completed:
            completed_plans.append({
                'file': plan_file,
                'name': plan_name,
                'todos_count': todos_count
            })
            print(f"✅ 已完成: {plan_name} ({todos_count} 个任务)")
        else:
            active_plans.append({
                'file': plan_file,
                'name': plan_name,
                'todos_count': todos_count
            })
            print(f"🔄 进行中: {plan_name} ({todos_count} 个任务)")
    
    print(f"\n📊 统计:")
    print(f"  已完成: {len(completed_plans)} 个")
    print(f"  进行中: {len(active_plans)} 个")
    
    # 归档已完成的计划
    if completed_plans:
        print(f"\n📦 准备归档 {len(completed_plans)} 个已完成的计划...")
        
        if not dry_run:
            archive_dir.mkdir(parents=True, exist_ok=True)
        
        archived_count = 0
        for plan_info in completed_plans:
            if dry_run:
                print(f"  [试运行] 将归档: {plan_info['name']}")
            else:
                if archive_plan(plan_info['file'], archive_dir):
                    archived_count += 1
                    print(f"  ✅ 已归档: {plan_info['name']}")
        
        if not dry_run:
            print(f"\n✅ 成功归档 {archived_count} 个计划文件")
        else:
            print(f"\n[试运行] 将归档 {len(completed_plans)} 个计划文件")
    else:
        print("\n✅ 没有需要归档的计划文件")
    
    print(f"\n📁 当前活动计划: {len(active_plans)} 个")
    for plan_info in active_plans:
        print(f"  - {plan_info['name']}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='归档已完成的计划文件')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式（不实际移动文件）')
    parser.add_argument('--force', action='store_true', help='强制归档（即使有未完成的任务）')
    
    args = parser.parse_args()
    
    main(dry_run=args.dry_run)
