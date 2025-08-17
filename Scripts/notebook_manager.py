#!/usr/bin/env python3
"""
Jupyter 笔记本管理器

用法:
    python notebook_manager.py [command] [options]

功能:
    - 批量转换笔记本格式
    - 添加标准配置到笔记本
    - 清理笔记本输出
    - 生成笔记本索引
    - 备份和恢复笔记本
"""

import json
import sys
import os
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import subprocess


class NotebookManager:
    def __init__(self, workspace_dir="."):
        self.workspace_dir = Path(workspace_dir)
        self.notebooks_dir = self.workspace_dir / "notebooks"
        self.backup_dir = self.workspace_dir / "notebook_backups"
        
        # 创建目录
        self.notebooks_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
    
    def find_notebooks(self, pattern="*.ipynb", recursive=True):
        """查找笔记本文件"""
        if recursive:
            notebooks = list(self.workspace_dir.rglob(pattern))
        else:
            notebooks = list(self.workspace_dir.glob(pattern))
        
        return [nb for nb in notebooks if nb.is_file()]
    
    def add_standard_config(self, notebook_path, overwrite=False):
        """添加标准配置到笔记本"""
        try:
            # 读取笔记本
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # 检查是否已有配置
            has_config = False
            if nb.cells and nb.cells[0].cell_type == 'code':
                first_cell_source = nb.cells[0].source
                if 'QuantConnect.Configuration' in first_cell_source:
                    has_config = True
            
            if has_config and not overwrite:
                print(f"⚠️  {notebook_path.name} 已有配置，跳过")
                return False
            
            # 创建标准配置单元格
            config_cell = new_code_cell(
                source="""# 标准配置 - 每个笔记本首格必备
from QuantConnect.Configuration import Config
Config.Set("data-folder", "/Lean/Data")   # 指向容器挂载点
Config.Set("log-level", "ERROR")          # 可选：安静日志

print("配置完成")""",
                metadata={}
            )
            
            # 创建导入单元格
            import_cell = new_code_cell(
                source="""# 导入必要的库
from QuantConnect.Research import QuantBook
from QuantConnect import Resolution
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置图表样式
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("库导入完成")""",
                metadata={}
            )
            
            # 创建初始化单元格
            init_cell = new_code_cell(
                source="""# 初始化 QuantBook
qb = QuantBook()
print("QuantBook 初始化完成")""",
                metadata={}
            )
            
            # 插入配置单元格
            if has_config and overwrite:
                # 替换第一个单元格
                nb.cells[0] = config_cell
                # 插入导入和初始化单元格
                nb.cells.insert(1, import_cell)
                nb.cells.insert(2, init_cell)
            else:
                # 在开头插入所有单元格
                nb.cells.insert(0, config_cell)
                nb.cells.insert(1, import_cell)
                nb.cells.insert(2, init_cell)
            
            # 保存笔记本
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            
            print(f"✅ 已添加标准配置到 {notebook_path.name}")
            return True
            
        except Exception as e:
            print(f"❌ 处理 {notebook_path.name} 失败: {e}")
            return False
    
    def clean_outputs(self, notebook_path):
        """清理笔记本输出"""
        try:
            # 读取笔记本
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # 清理所有代码单元格的输出
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.execution_count = None
                    cell.outputs = []
            
            # 保存笔记本
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            
            print(f"✅ 已清理 {notebook_path.name} 的输出")
            return True
            
        except Exception as e:
            print(f"❌ 清理 {notebook_path.name} 失败: {e}")
            return False
    
    def convert_format(self, notebook_path, output_format='py'):
        """转换笔记本格式"""
        try:
            if output_format == 'py':
                # 转换为Python脚本
                cmd = ['jupyter', 'nbconvert', '--to', 'python', str(notebook_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✅ 已转换 {notebook_path.name} 为Python脚本")
                return True
            elif output_format == 'html':
                # 转换为HTML
                cmd = ['jupyter', 'nbconvert', '--to', 'html', str(notebook_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✅ 已转换 {notebook_path.name} 为HTML")
                return True
            elif output_format == 'pdf':
                # 转换为PDF
                cmd = ['jupyter', 'nbconvert', '--to', 'pdf', str(notebook_path)]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✅ 已转换 {notebook_path.name} 为PDF")
                return True
            else:
                print(f"❌ 不支持的格式: {output_format}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 转换 {notebook_path.name} 失败: {e}")
            return False
    
    def backup_notebooks(self, backup_name=None):
        """备份笔记本"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        notebooks = self.find_notebooks()
        
        for notebook in notebooks:
            try:
                # 复制笔记本
                dest_path = backup_path / notebook.name
                shutil.copy2(notebook, dest_path)
                print(f"✅ 已备份 {notebook.name}")
            except Exception as e:
                print(f"❌ 备份 {notebook.name} 失败: {e}")
        
        print(f"📦 备份完成: {backup_path}")
        return backup_path
    
    def restore_notebooks(self, backup_name):
        """恢复笔记本"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ 备份不存在: {backup_path}")
            return False
        
        notebooks = list(backup_path.glob("*.ipynb"))
        
        for notebook in notebooks:
            try:
                # 复制回工作区
                dest_path = self.workspace_dir / notebook.name
                shutil.copy2(notebook, dest_path)
                print(f"✅ 已恢复 {notebook.name}")
            except Exception as e:
                print(f"❌ 恢复 {notebook.name} 失败: {e}")
        
        print(f"🔄 恢复完成: {len(notebooks)} 个笔记本")
        return True
    
    def generate_index(self):
        """生成笔记本索引"""
        notebooks = self.find_notebooks()
        
        if not notebooks:
            print("❌ 未找到笔记本文件")
            return
        
        # 按目录分组
        notebook_groups = {}
        for notebook in notebooks:
            rel_path = notebook.relative_to(self.workspace_dir)
            group = rel_path.parent
            if group not in notebook_groups:
                notebook_groups[group] = []
            notebook_groups[group].append(notebook)
        
        # 生成索引内容
        index_content = f"""# 笔记本索引

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**总数量**: {len(notebooks)} 个笔记本

"""
        
        for group, group_notebooks in sorted(notebook_groups.items()):
            index_content += f"\n## {group}\n\n"
            
            for notebook in sorted(group_notebooks):
                # 读取笔记本获取标题
                try:
                    with open(notebook, 'r', encoding='utf-8') as f:
                        nb = nbformat.read(f, as_version=4)
                    
                    title = notebook.stem
                    if nb.cells and nb.cells[0].cell_type == 'markdown':
                        first_line = nb.cells[0].source.strip().split('\n')[0]
                        if first_line.startswith('#'):
                            title = first_line.lstrip('#').strip()
                    
                    rel_path = notebook.relative_to(self.workspace_dir)
                    index_content += f"- [{title}]({rel_path})\n"
                    
                except Exception as e:
                    rel_path = notebook.relative_to(self.workspace_dir)
                    index_content += f"- [{notebook.stem}]({rel_path})\n"
        
        # 保存索引文件
        index_file = self.workspace_dir / "notebook_index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"📋 索引已生成: {index_file}")
        return index_file
    
    def list_backups(self):
        """列出备份"""
        if not self.backup_dir.exists():
            print("❌ 备份目录不存在")
            return
        
        backups = [d for d in self.backup_dir.iterdir() if d.is_dir()]
        
        if not backups:
            print("📦 没有找到备份")
            return
        
        print("📦 可用备份:")
        for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            notebook_count = len(list(backup.glob("*.ipynb")))
            print(f"  - {backup.name} ({mtime.strftime('%Y-%m-%d %H:%M:%S')}, {notebook_count} 个笔记本)")
    
    def batch_process(self, operation, **kwargs):
        """批量处理笔记本"""
        notebooks = self.find_notebooks()
        
        if not notebooks:
            print("❌ 未找到笔记本文件")
            return
        
        print(f"🔄 开始批量{operation} {len(notebooks)} 个笔记本...")
        
        success_count = 0
        for notebook in notebooks:
            if operation == 'add_config':
                if self.add_standard_config(notebook, **kwargs):
                    success_count += 1
            elif operation == 'clean':
                if self.clean_outputs(notebook):
                    success_count += 1
            elif operation == 'convert':
                if self.convert_format(notebook, **kwargs):
                    success_count += 1
        
        print(f"✅ 批量{operation}完成: {success_count}/{len(notebooks)} 成功")


def main():
    parser = argparse.ArgumentParser(description='Jupyter 笔记本管理器')
    parser.add_argument('command', choices=[
        'add-config', 'clean', 'convert', 'backup', 'restore', 
        'index', 'list-backups', 'batch-add-config', 'batch-clean'
    ], help='要执行的操作')
    parser.add_argument('--overwrite', action='store_true', help='覆盖现有配置')
    parser.add_argument('--format', choices=['py', 'html', 'pdf'], default='py', help='转换格式')
    parser.add_argument('--backup-name', help='备份名称')
    parser.add_argument('--workspace', default='.', help='工作区目录')
    
    args = parser.parse_args()
    
    manager = NotebookManager(args.workspace)
    
    if args.command == 'add-config':
        notebooks = manager.find_notebooks()
        if not notebooks:
            print("❌ 未找到笔记本文件")
            return
        
        for notebook in notebooks:
            manager.add_standard_config(notebook, args.overwrite)
    
    elif args.command == 'clean':
        notebooks = manager.find_notebooks()
        if not notebooks:
            print("❌ 未找到笔记本文件")
            return
        
        for notebook in notebooks:
            manager.clean_outputs(notebook)
    
    elif args.command == 'convert':
        notebooks = manager.find_notebooks()
        if not notebooks:
            print("❌ 未找到笔记本文件")
            return
        
        for notebook in notebooks:
            manager.convert_format(notebook, args.format)
    
    elif args.command == 'backup':
        manager.backup_notebooks(args.backup_name)
    
    elif args.command == 'restore':
        if not args.backup_name:
            print("❌ 请指定备份名称")
            return
        manager.restore_notebooks(args.backup_name)
    
    elif args.command == 'index':
        manager.generate_index()
    
    elif args.command == 'list-backups':
        manager.list_backups()
    
    elif args.command == 'batch-add-config':
        manager.batch_process('add_config', overwrite=args.overwrite)
    
    elif args.command == 'batch-clean':
        manager.batch_process('clean')


if __name__ == "__main__":
    main() 