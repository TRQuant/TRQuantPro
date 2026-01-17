#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 标准开发流程自动化工具

使用方法:
    python scripts/dev_workflow.py start "任务名称" "任务描述"
    python scripts/dev_workflow.py check
    python scripts/dev_workflow.py log "开发内容" --tags development
    python scripts/dev_workflow.py complete "task_id"
    python scripts/dev_workflow.py status
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT / "mcp_servers"))

from dev_task_server import call_tool

PROJECT = "trquant"


async def check_status():
    """检查当前开发状态"""
    print("\n" + "=" * 60)
    print("TRQuant 开发状态检查")
    print("=" * 60)
    
    # 检查进行中的任务
    print("\n【进行中的任务】")
    result = await call_tool("task.list", {"project": PROJECT, "status": "in_progress"})
    if hasattr(result, 'text'):
        data = json.loads(result.text)
        tasks = data.get('tasks', [])
        if tasks:
            for task in tasks[:5]:
                print(f"  - [{task.get('id')}] {task.get('title')}")
        else:
            print("  (无)")
    
    # 检查最近日志
    print("\n【最近开发日志】")
    result = await call_tool("devlog.list", {"project": PROJECT, "limit": 3})
    if hasattr(result, 'text'):
        data = json.loads(result.text)
        logs = data.get('logs', [])
        for log in logs:
            content = log.get('content', '')[:50]
            tags = log.get('tags', [])
            print(f"  - [{', '.join(tags[:2])}] {content}...")
    
    print("\n✅ 状态检查完成")


async def start_task(title: str, description: str):
    """开始新任务"""
    print(f"\n【开始新任务】: {title}")
    
    # 创建任务
    result = await call_tool("task.create", {
        "title": title,
        "description": description,
        "status": "in_progress",
        "project": PROJECT
    })
    
    if hasattr(result, 'text'):
        data = json.loads(result.text)
        task_id = data.get('task', {}).get('id', 'N/A')
    else:
        task_id = 'N/A'
    
    print(f"  ✅ 任务已创建: {task_id}")
    
    # 记录规划日志
    await call_tool("devlog.add", {
        "content": f"【规划】{title}\n\n{description}",
        "tags": ["planning", title.split(':')[0].lower().replace(' ', '_')],
        "project": PROJECT
    })
    print("  ✅ 规划日志已记录")
    
    return task_id


async def add_log(content: str, tags: list):
    """添加开发日志"""
    await call_tool("devlog.add", {
        "content": content,
        "tags": tags,
        "project": PROJECT
    })
    print(f"✅ 日志已记录: {content[:50]}...")


async def complete_task(task_id: str, summary: str = None):
    """完成任务"""
    print(f"\n【完成任务】: {task_id}")
    
    # 更新任务状态
    await call_tool("task.update", {
        "task_id": task_id,
        "status": "completed",
        "project": PROJECT
    })
    print("  ✅ 任务状态已更新")
    
    # 记录完成日志
    if summary:
        await call_tool("devlog.add", {
            "content": f"【完成】{summary}",
            "tags": ["completed"],
            "project": PROJECT
        })
        print("  ✅ 完成日志已记录")


async def record_issue(title: str, description: str):
    """记录问题"""
    await call_tool("issue.create", {
        "title": title,
        "description": description,
        "project": PROJECT
    })
    print(f"✅ 问题已记录: {title}")


async def search_experience(query: str):
    """搜索经验"""
    result = await call_tool("experience.search", {
        "query": query,
        "project": PROJECT
    })
    if hasattr(result, 'text'):
        data = json.loads(result.text)
        experiences = data.get('experiences', [])
        print(f"\n找到 {len(experiences)} 条相关经验:")
        for exp in experiences[:5]:
            print(f"  - {exp.get('content', '')[:80]}...")
    else:
        print("未找到相关经验")


def main():
    parser = argparse.ArgumentParser(description='TRQuant 标准开发流程工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # check 命令
    subparsers.add_parser('check', help='检查当前开发状态')
    subparsers.add_parser('status', help='检查当前开发状态')
    
    # start 命令
    start_parser = subparsers.add_parser('start', help='开始新任务')
    start_parser.add_argument('title', help='任务标题')
    start_parser.add_argument('description', help='任务描述')
    
    # log 命令
    log_parser = subparsers.add_parser('log', help='添加开发日志')
    log_parser.add_argument('content', help='日志内容')
    log_parser.add_argument('--tags', nargs='+', default=['development'], help='标签')
    
    # complete 命令
    complete_parser = subparsers.add_parser('complete', help='完成任务')
    complete_parser.add_argument('task_id', help='任务ID')
    complete_parser.add_argument('--summary', help='完成总结')
    
    # issue 命令
    issue_parser = subparsers.add_parser('issue', help='记录问题')
    issue_parser.add_argument('title', help='问题标题')
    issue_parser.add_argument('description', help='问题描述')
    
    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索经验')
    search_parser.add_argument('query', help='搜索关键词')
    
    args = parser.parse_args()
    
    if args.command in ['check', 'status'] or args.command is None:
        asyncio.run(check_status())
    elif args.command == 'start':
        asyncio.run(start_task(args.title, args.description))
    elif args.command == 'log':
        asyncio.run(add_log(args.content, args.tags))
    elif args.command == 'complete':
        asyncio.run(complete_task(args.task_id, args.summary))
    elif args.command == 'issue':
        asyncio.run(record_issue(args.title, args.description))
    elif args.command == 'search':
        asyncio.run(search_experience(args.query))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
