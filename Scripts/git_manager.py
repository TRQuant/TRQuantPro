#!/usr/bin/env python3
"""
Git 管理脚本

用法:
    python git_manager.py [command] [options]

功能:
    - 自动化Git提交
    - 智能文件分类
    - 备份重要文件
    - 同步到远程仓库
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
import json


class GitManager:
    def __init__(self, workspace_dir="."):
        self.workspace_dir = Path(workspace_dir)
        self.git_dir = self.workspace_dir / ".git"
        
        if not self.git_dir.exists():
            print("❌ 当前目录不是Git仓库")
            print("请先运行: git init")
            sys.exit(1)
    
    def run_git_command(self, command, capture_output=True):
        """运行Git命令"""
        try:
            if capture_output:
                result = subprocess.run(['git'] + command, 
                                      capture_output=True, text=True, 
                                      cwd=self.workspace_dir, check=True)
                return result.stdout.strip()
            else:
                subprocess.run(['git'] + command, cwd=self.workspace_dir, check=True)
                return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Git命令失败: {' '.join(command)}")
            print(f"错误: {e.stderr}")
            return False
    
    def get_status(self):
        """获取Git状态"""
        return self.run_git_command(['status', '--porcelain'])
    
    def get_modified_files(self):
        """获取修改的文件列表"""
        status = self.get_status()
        if not status:
            return []
        
        files = []
        for line in status.split('\n'):
            if line.strip():
                status_code = line[:2]
                filename = line[3:].strip()
                files.append((status_code, filename))
        
        return files
    
    def categorize_files(self, files):
        """分类文件"""
        categories = {
            'scripts': [],
            'notebooks': [],
            'configs': [],
            'docs': [],
            'data': [],
            'other': []
        }
        
        for status, filename in files:
            file_path = Path(filename)
            
            if file_path.suffix == '.py' and 'Scripts' in str(file_path):
                categories['scripts'].append((status, filename))
            elif file_path.suffix == '.ipynb':
                categories['notebooks'].append((status, filename))
            elif file_path.name in ['config.json', 'lean.json', 'qc.code-workspace']:
                categories['configs'].append((status, filename))
            elif file_path.suffix == '.md':
                categories['docs'].append((status, filename))
            elif any(ext in str(file_path) for ext in ['.zip', '.csv', '.json']) and 'data' in str(file_path):
                categories['data'].append((status, filename))
            else:
                categories['other'].append((status, filename))
        
        return categories
    
    def add_files(self, files):
        """添加文件到暂存区"""
        if not files:
            print("📝 没有文件需要添加")
            return True
        
        file_list = [f[1] for f in files]
        print(f"📝 添加 {len(file_list)} 个文件到暂存区:")
        for filename in file_list:
            print(f"   + {filename}")
        
        return self.run_git_command(['add'] + file_list, capture_output=False)
    
    def commit_changes(self, message=None, category=None):
        """提交更改"""
        if not message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if category:
                message = f"Update {category} - {timestamp}"
            else:
                message = f"Auto commit - {timestamp}"
        
        print(f"💾 提交更改: {message}")
        return self.run_git_command(['commit', '-m', message], capture_output=False)
    
    def auto_commit(self, force=False):
        """自动提交所有更改"""
        print("🔄 检查Git状态...")
        
        # 获取修改的文件
        files = self.get_modified_files()
        if not files and not force:
            print("✅ 没有需要提交的更改")
            return True
        
        # 分类文件
        categories = self.categorize_files(files)
        
        # 显示文件分类
        print("\n📋 文件分类:")
        for category, file_list in categories.items():
            if file_list:
                print(f"  {category}: {len(file_list)} 个文件")
                for status, filename in file_list:
                    print(f"    {status} {filename}")
        
        # 询问是否继续
        if not force:
            response = input("\n是否继续提交? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("❌ 取消提交")
                return False
        
        # 添加所有文件
        all_files = []
        for file_list in categories.values():
            all_files.extend(file_list)
        
        if not self.add_files(all_files):
            return False
        
        # 提交更改
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Auto commit - {timestamp}\n\n"
        
        for category, file_list in categories.items():
            if file_list:
                message += f"{category}: {len(file_list)} files\n"
        
        return self.commit_changes(message.strip())
    
    def setup_remote(self, remote_url):
        """设置远程仓库"""
        print(f"🔗 设置远程仓库: {remote_url}")
        
        # 检查是否已有远程仓库
        remotes = self.run_git_command(['remote', '-v'])
        if 'origin' in remotes:
            print("⚠️  远程仓库已存在，更新URL...")
            self.run_git_command(['remote', 'set-url', 'origin', remote_url])
        else:
            self.run_git_command(['remote', 'add', 'origin', remote_url])
        
        print("✅ 远程仓库设置完成")
        return True
    
    def push_to_remote(self, branch='main'):
        """推送到远程仓库"""
        print(f"🚀 推送到远程仓库 (分支: {branch})")
        
        # 检查远程仓库
        remotes = self.run_git_command(['remote', '-v'])
        if 'origin' not in remotes:
            print("❌ 未设置远程仓库")
            return False
        
        # 推送
        return self.run_git_command(['push', 'origin', branch], capture_output=False)
    
    def pull_from_remote(self, branch='main'):
        """从远程仓库拉取"""
        print(f"📥 从远程仓库拉取 (分支: {branch})")
        
        # 检查远程仓库
        remotes = self.run_git_command(['remote', '-v'])
        if 'origin' not in remotes:
            print("❌ 未设置远程仓库")
            return False
        
        # 拉取
        return self.run_git_command(['pull', 'origin', branch], capture_output=False)
    
    def create_backup_branch(self, branch_name=None):
        """创建备份分支"""
        if not branch_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            branch_name = f"backup_{timestamp}"
        
        print(f"📦 创建备份分支: {branch_name}")
        
        # 确保当前更改已提交
        files = self.get_modified_files()
        if files:
            print("⚠️  有未提交的更改，先提交...")
            if not self.auto_commit(force=True):
                return False
        
        # 创建并切换到新分支
        self.run_git_command(['checkout', '-b', branch_name])
        print(f"✅ 备份分支创建完成: {branch_name}")
        return True
    
    def list_branches(self):
        """列出所有分支"""
        branches = self.run_git_command(['branch', '-a'])
        print("🌿 分支列表:")
        for branch in branches.split('\n'):
            if branch.strip():
                print(f"  {branch.strip()}")
    
    def show_log(self, count=10):
        """显示提交历史"""
        log = self.run_git_command(['log', '--oneline', f'-{count}'])
        print(f"📜 最近 {count} 次提交:")
        for line in log.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    
    def backup_important_files(self):
        """备份重要文件"""
        important_files = [
            'config.json',
            'lean.json',
            'qc.code-workspace',
            'QuantConnect_Research_Start.md',
            'Scripts/README.md'
        ]
        
        backup_dir = Path('backup_important')
        backup_dir.mkdir(exist_ok=True)
        
        print(f"💾 备份重要文件到 {backup_dir}")
        
        for file_path in important_files:
            src = Path(file_path)
            if src.exists():
                dst = backup_dir / src.name
                import shutil
                shutil.copy2(src, dst)
                print(f"  ✅ {file_path}")
            else:
                print(f"  ⚠️  {file_path} 不存在")
        
        print("✅ 重要文件备份完成")
        return True


def main():
    parser = argparse.ArgumentParser(description='Git 管理脚本')
    parser.add_argument('command', choices=[
        'status', 'commit', 'auto-commit', 'push', 'pull', 
        'setup-remote', 'backup-branch', 'list-branches', 
        'show-log', 'backup-files'
    ], help='要执行的Git操作')
    parser.add_argument('--force', action='store_true', help='强制操作')
    parser.add_argument('--message', help='提交消息')
    parser.add_argument('--remote-url', help='远程仓库URL')
    parser.add_argument('--branch', default='main', help='分支名称')
    parser.add_argument('--count', type=int, default=10, help='显示日志条数')
    
    args = parser.parse_args()
    
    manager = GitManager()
    
    if args.command == 'status':
        files = manager.get_modified_files()
        if files:
            print("📋 修改的文件:")
            categories = manager.categorize_files(files)
            for category, file_list in categories.items():
                if file_list:
                    print(f"\n{category}:")
                    for status, filename in file_list:
                        print(f"  {status} {filename}")
        else:
            print("✅ 工作区干净，没有修改")
    
    elif args.command == 'commit':
        if not manager.auto_commit(force=args.force):
            print("❌ 提交失败")
    
    elif args.command == 'auto-commit':
        if not manager.auto_commit(force=args.force):
            print("❌ 自动提交失败")
    
    elif args.command == 'push':
        if not manager.push_to_remote(args.branch):
            print("❌ 推送失败")
    
    elif args.command == 'pull':
        if not manager.pull_from_remote(args.branch):
            print("❌ 拉取失败")
    
    elif args.command == 'setup-remote':
        if not args.remote_url:
            print("❌ 请提供远程仓库URL")
            return
        if not manager.setup_remote(args.remote_url):
            print("❌ 设置远程仓库失败")
    
    elif args.command == 'backup-branch':
        if not manager.create_backup_branch(args.message):
            print("❌ 创建备份分支失败")
    
    elif args.command == 'list-branches':
        manager.list_branches()
    
    elif args.command == 'show-log':
        manager.show_log(args.count)
    
    elif args.command == 'backup-files':
        if not manager.backup_important_files():
            print("❌ 备份文件失败")


if __name__ == "__main__":
    main() 