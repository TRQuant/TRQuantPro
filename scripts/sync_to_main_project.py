#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步工作目录到主项目目录

功能：
1. 将 .local/share/trquant 中的代码同步到 /home/taotao/dev/QuantTest/TRQuant
2. 排除缓存、数据、日志等不需要同步的文件
3. 保留Git历史
"""

import os
import shutil
from pathlib import Path
from typing import List, Set
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 目录配置
WORK_DIR = Path.home() / '.local/share/trquant'
MAIN_DIR = Path('/home/taotao/dev/QuantTest/TRQuant')

# 需要同步的目录和文件
SYNC_PATTERNS = [
    'gui/',
    'markets/',
    'core/',
    'utils/',
    'jqdata/',
    'ptrade_bridge/',
    'qmt_bridge/',
    'quantconnect_bridge/',
    'bridge_common/',
    'strategies/',
    'scripts/',
    'config/',
    'docs/',
    'prompts/',
    'JQQuant.py',
    'main.py',
    'requirements.txt',
    'README.md',
    '*.md',  # 根目录的Markdown文件
]

# 排除的目录和文件
EXCLUDE_PATTERNS = [
    '__pycache__/',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.git/',
    'venv/',
    'jqdata_env/',
    'node_modules/',
    'cache/',
    'logs/',
    'data/mongodb/',
    'reports/',
    '.idea/',
    '.vscode/',
    '*.log',
    '*.db',
    '*.sqlite',
    '.DS_Store',
    'Thumbs.db',
]

# 排除的文件扩展名
EXCLUDE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.log', '.db', '.sqlite',
    '.swp', '.swo', '.tmp', '.bak', '.orig'
}


def should_exclude(path: Path, relative_path: Path) -> bool:
    """判断是否应该排除该路径"""
    
    # 检查扩展名
    if path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True
    
    # 检查排除模式
    path_str = str(relative_path).replace('\\', '/')
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith('/'):
            # 目录模式
            if path_str.startswith(pattern) or path_str.endswith('/' + pattern):
                return True
        else:
            # 文件模式
            if path_str.endswith(pattern) or pattern in path_str:
                return True
    
    return False


def should_sync(path: Path, relative_path: Path) -> bool:
    """判断是否应该同步该路径"""
    
    # 先检查排除
    if should_exclude(path, relative_path):
        return False
    
    # 检查同步模式
    path_str = str(relative_path).replace('\\', '/')
    for pattern in SYNC_PATTERNS:
        if pattern.endswith('/'):
            # 目录模式
            if path_str.startswith(pattern):
                return True
        elif pattern.startswith('*'):
            # 通配符模式
            ext = pattern[1:]
            if path_str.endswith(ext):
                return True
        else:
            # 精确匹配
            if path_str == pattern or path_str.endswith('/' + pattern):
                return True
    
    return False


def sync_file(src: Path, dst: Path) -> bool:
    """同步单个文件"""
    try:
        # 创建目标目录
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # 检查是否需要更新
        if dst.exists():
            src_mtime = src.stat().st_mtime
            dst_mtime = dst.stat().st_mtime
            if src_mtime <= dst_mtime:
                return False  # 目标文件更新，跳过
        
        # 复制文件
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        logger.error(f"同步文件失败 {src} -> {dst}: {e}")
        return False


def sync_directory(src_dir: Path, dst_dir: Path, relative_path: Path = Path('')):
    """递归同步目录"""
    synced_files = 0
    skipped_files = 0
    
    if not src_dir.exists():
        logger.warning(f"源目录不存在: {src_dir}")
        return synced_files, skipped_files
    
    for item in src_dir.iterdir():
        item_relative = relative_path / item.name
        
        # 检查是否应该排除
        if should_exclude(item, item_relative):
            continue
        
        # 检查是否应该同步
        if not should_sync(item, item_relative):
            continue
        
        src_path = src_dir / item.name
        dst_path = dst_dir / item.name
        
        if item.is_file():
            if sync_file(src_path, dst_path):
                synced_files += 1
                logger.info(f"✅ 同步: {item_relative}")
            else:
                skipped_files += 1
        elif item.is_dir():
            # 递归同步子目录
            sub_synced, sub_skipped = sync_directory(
                src_path, dst_path, item_relative
            )
            synced_files += sub_synced
            skipped_files += sub_skipped
    
    return synced_files, skipped_files


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("开始同步工作目录到主项目目录")
    logger.info("=" * 60)
    logger.info(f"工作目录: {WORK_DIR}")
    logger.info(f"主目录: {MAIN_DIR}")
    logger.info("")
    
    # 检查目录
    if not WORK_DIR.exists():
        logger.error(f"工作目录不存在: {WORK_DIR}")
        return
    
    if not MAIN_DIR.exists():
        logger.warning(f"主目录不存在，将创建: {MAIN_DIR}")
        MAIN_DIR.mkdir(parents=True, exist_ok=True)
    
    # 同步根目录文件
    logger.info("同步根目录文件...")
    root_files = [
        'JQQuant.py', 'main.py', 'requirements.txt', 'README.md'
    ]
    for filename in root_files:
        src_file = WORK_DIR / filename
        if src_file.exists():
            dst_file = MAIN_DIR / filename
            if sync_file(src_file, dst_file):
                logger.info(f"✅ 同步: {filename}")
    
    # 同步Markdown文件
    logger.info("同步Markdown文件...")
    for md_file in WORK_DIR.glob('*.md'):
        if not should_exclude(md_file, Path(md_file.name)):
            dst_file = MAIN_DIR / md_file.name
            if sync_file(md_file, dst_file):
                logger.info(f"✅ 同步: {md_file.name}")
    
    # 同步目录
    logger.info("同步目录...")
    total_synced = 0
    total_skipped = 0
    
    for pattern in SYNC_PATTERNS:
        if pattern.endswith('/'):
            dir_name = pattern.rstrip('/')
            src_dir = WORK_DIR / dir_name
            if src_dir.exists() and src_dir.is_dir():
                dst_dir = MAIN_DIR / dir_name
                synced, skipped = sync_directory(src_dir, dst_dir, Path(dir_name))
                total_synced += synced
                total_skipped += skipped
                logger.info(f"✅ 目录 {dir_name}: 同步 {synced} 个文件，跳过 {skipped} 个文件")
    
    # 总结
    logger.info("")
    logger.info("=" * 60)
    logger.info("同步完成！")
    logger.info(f"总计同步: {total_synced} 个文件")
    logger.info(f"总计跳过: {total_skipped} 个文件")
    logger.info("=" * 60)
    logger.info("")
    logger.info("下一步：")
    logger.info("1. 检查主目录的Git状态")
    logger.info("2. 审查更改")
    logger.info("3. 提交更改到Git")


if __name__ == '__main__':
    main()

