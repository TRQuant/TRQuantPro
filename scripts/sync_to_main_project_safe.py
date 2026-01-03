#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全同步工作目录到主项目目录

特点：
1. 只复制文件，不删除目标文件
2. 保留目标目录的Git历史
3. 显示详细同步日志
4. 支持备份
"""

import os
import shutil
from pathlib import Path
from typing import List, Set, Tuple
import logging
from datetime import datetime

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
            if path_str.startswith(pattern) or path_str.endswith('/' + pattern):
                return True
        else:
            if path_str.endswith(pattern) or pattern in path_str:
                return True
    
    return False


def should_sync(path: Path, relative_path: Path) -> bool:
    """判断是否应该同步该路径"""
    
    if should_exclude(path, relative_path):
        return False
    
    path_str = str(relative_path).replace('\\', '/')
    for pattern in SYNC_PATTERNS:
        if pattern.endswith('/'):
            if path_str.startswith(pattern):
                return True
        elif pattern.startswith('*'):
            ext = pattern[1:]
            if path_str.endswith(ext):
                return True
        else:
            if path_str == pattern or path_str.endswith('/' + pattern):
                return True
    
    return False


def safe_copy_file(src: Path, dst: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    安全复制文件（不覆盖较新的文件）
    
    Returns:
        (copied, message)
    """
    try:
        # 检查源文件
        if not src.exists():
            return False, f"源文件不存在: {src}"
        
        # 创建目标目录
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
        
        # 检查目标文件
        if dst.exists():
            src_mtime = src.stat().st_mtime
            dst_mtime = dst.stat().st_mtime
            
            # 如果目标文件更新，询问是否覆盖
            if src_mtime <= dst_mtime:
                return False, f"目标文件较新，跳过: {dst.name}"
            
            # 备份目标文件
            if not dry_run:
                backup_path = dst.with_suffix(dst.suffix + '.backup')
                shutil.copy2(dst, backup_path)
        
        # 复制文件
        if not dry_run:
            shutil.copy2(src, dst)
        
        return True, f"已复制: {dst.name}"
    
    except Exception as e:
        return False, f"错误: {e}"


def sync_directory(src_dir: Path, dst_dir: Path, relative_path: Path = Path(''), dry_run: bool = False):
    """递归同步目录"""
    synced_files = 0
    skipped_files = 0
    errors = []
    
    if not src_dir.exists():
        logger.warning(f"源目录不存在: {src_dir}")
        return synced_files, skipped_files, errors
    
    for item in src_dir.iterdir():
        item_relative = relative_path / item.name
        
        if should_exclude(item, item_relative):
            continue
        
        if not should_sync(item, item_relative):
            continue
        
        src_path = src_dir / item.name
        dst_path = dst_dir / item.name
        
        if item.is_file():
            copied, message = safe_copy_file(src_path, dst_path, dry_run)
            if copied:
                synced_files += 1
                logger.info(f"✅ {message}")
            else:
                skipped_files += 1
                logger.debug(f"⏭️  {message}")
        elif item.is_dir():
            sub_synced, sub_skipped, sub_errors = sync_directory(
                src_path, dst_path, item_relative, dry_run
            )
            synced_files += sub_synced
            skipped_files += sub_skipped
            errors.extend(sub_errors)
    
    return synced_files, skipped_files, errors


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='安全同步工作目录到主项目')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要执行的操作，不实际复制')
    parser.add_argument('--backup', action='store_true', help='同步前备份主目录')
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("安全同步工作目录到主项目目录")
    logger.info("=" * 60)
    logger.info(f"工作目录: {WORK_DIR}")
    logger.info(f"主目录: {MAIN_DIR}")
    if args.dry_run:
        logger.info("⚠️  干运行模式（不会实际复制文件）")
    logger.info("")
    
    # 检查目录
    if not WORK_DIR.exists():
        logger.error(f"工作目录不存在: {WORK_DIR}")
        return
    
    if not MAIN_DIR.exists():
        logger.warning(f"主目录不存在，将创建: {MAIN_DIR}")
        if not args.dry_run:
            MAIN_DIR.mkdir(parents=True, exist_ok=True)
    
    # 备份（可选）
    if args.backup and not args.dry_run:
        backup_dir = MAIN_DIR.parent / f"{MAIN_DIR.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"创建备份: {backup_dir}")
        shutil.copytree(MAIN_DIR, backup_dir, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
    
    # 同步根目录文件
    logger.info("同步根目录文件...")
    root_files = ['JQQuant.py', 'main.py', 'requirements.txt', 'README.md']
    for filename in root_files:
        src_file = WORK_DIR / filename
        if src_file.exists():
            dst_file = MAIN_DIR / filename
            copied, message = safe_copy_file(src_file, dst_file, args.dry_run)
            if copied:
                logger.info(f"✅ {message}")
            else:
                logger.debug(f"⏭️  {message}")
    
    # 同步Markdown文件
    logger.info("同步Markdown文件...")
    for md_file in WORK_DIR.glob('*.md'):
        if not should_exclude(md_file, Path(md_file.name)):
            dst_file = MAIN_DIR / md_file.name
            copied, message = safe_copy_file(md_file, dst_file, args.dry_run)
            if copied:
                logger.info(f"✅ {message}")
    
    # 同步目录
    logger.info("同步目录...")
    total_synced = 0
    total_skipped = 0
    errors = []
    
    for pattern in SYNC_PATTERNS:
        if pattern.endswith('/'):
            dir_name = pattern.rstrip('/')
            src_dir = WORK_DIR / dir_name
            if src_dir.exists() and src_dir.is_dir():
                dst_dir = MAIN_DIR / dir_name
                synced, skipped, dir_errors = sync_directory(src_dir, dst_dir, Path(dir_name), args.dry_run)
                total_synced += synced
                total_skipped += skipped
                errors.extend(dir_errors)
                logger.info(f"📁 目录 {dir_name}: 同步 {synced} 个文件，跳过 {skipped} 个文件")
    
    # 总结
    logger.info("")
    logger.info("=" * 60)
    if args.dry_run:
        logger.info("干运行完成（未实际复制文件）")
    else:
        logger.info("同步完成！")
    logger.info(f"总计同步: {total_synced} 个文件")
    logger.info(f"总计跳过: {total_skipped} 个文件")
    if errors:
        logger.warning(f"错误: {len(errors)} 个")
        for error in errors[:10]:  # 只显示前10个错误
            logger.error(f"  - {error}")
    logger.info("=" * 60)
    
    if not args.dry_run:
        logger.info("")
        logger.info("下一步：")
        logger.info("1. 检查主目录的Git状态")
        logger.info("2. 审查更改")
        logger.info("3. 提交更改到Git")


if __name__ == '__main__':
    main()

