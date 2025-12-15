#!/usr/bin/env python3
"""
通用文件恢复脚本 - 从Cursor历史恢复被git restore覆盖的文件
用法: python3 recover_from_cursor.py [文件路径] [目标日期] [目标时间范围]
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

CURSOR_HISTORY_DIR = Path.home() / ".config/Cursor/User/History"
PROJECT_ROOT = Path("/home/taotao/dev/QuantTest/TRQuant")

def find_history_dir(file_path):
    """查找文件对应的Cursor历史目录"""
    file_uri = f"file://{file_path.resolve()}"
    
    for entries_file in CURSOR_HISTORY_DIR.rglob("entries.json"):
        try:
            with open(entries_file) as f:
                data = json.load(f)
                if data.get("resource") == file_uri:
                    return entries_file.parent
        except:
            continue
    return None

def find_target_version(history_dir, target_date=None, target_hour_start=None, target_hour_end=None):
    """在历史目录中查找目标版本"""
    if not history_dir or not history_dir.exists():
        return None, None
    
    hist_files = list(history_dir.glob("*.*"))
    target_file = None
    target_time = None
    
    for hist_file in hist_files:
        if not hist_file.is_file():
            continue
        
        file_stat = hist_file.stat()
        file_time = datetime.fromtimestamp(file_stat.st_mtime)
        
        # 如果指定了目标日期和时间范围
        if target_date:
            date_str = file_time.strftime("%Y-%m-%d")
            if date_str != target_date:
                continue
            
            if target_hour_start is not None and target_hour_end is not None:
                hour = file_time.hour
                if not (target_hour_start <= hour <= target_hour_end):
                    continue
        
        # 选择最新的匹配版本
        if target_file is None or file_stat.st_mtime > target_file.stat().st_mtime:
            target_file = hist_file
            target_time = file_time
    
    return target_file, target_time

def recover_file(file_path, target_date=None, target_hour_start=None, target_hour_end=None, backup=True):
    """恢复单个文件"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"⚠️  文件不存在: {file_path}")
        return False
    
    # 查找历史目录
    history_dir = find_history_dir(file_path)
    if not history_dir:
        print(f"⚠️  未找到历史: {file_path.name}")
        return False
    
    # 查找目标版本
    target_file, target_time = find_target_version(history_dir, target_date, target_hour_start, target_hour_end)
    
    if not target_file:
        print(f"⚠️  未找到目标版本: {file_path.name}")
        return False
    
    # 创建备份
    if backup:
        backup_file = file_path.with_suffix(file_path.suffix + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(file_path, backup_file)
        print(f"📋 已备份: {backup_file.name}")
    
    # 恢复文件
    shutil.copy2(target_file, file_path)
    print(f"✅ 已恢复: {file_path.name} ({target_time})")
    return True

def recover_directory(dir_path, target_date=None, target_hour_start=None, target_hour_end=None, pattern="*"):
    """批量恢复目录中的文件"""
    dir_path = Path(dir_path)
    if not dir_path.exists():
        print(f"❌ 目录不存在: {dir_path}")
        return
    
    files = list(dir_path.rglob(pattern))
    recovered = 0
    not_found = 0
    
    for file in files:
        if file.is_file():
            if recover_file(file, target_date, target_hour_start, target_hour_end):
                recovered += 1
            else:
                not_found += 1
    
    print(f"\n=== 恢复完成 ===")
    print(f"✅ 已恢复: {recovered} 个文件")
    print(f"⚠️  未找到: {not_found} 个文件")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 recover_from_cursor.py <文件路径> [目标日期] [开始小时] [结束小时]")
        print("  python3 recover_from_cursor.py <目录路径> --dir [目标日期] [开始小时] [结束小时]")
        print("")
        print("示例:")
        print("  python3 recover_from_cursor.py extension/AShare-manual/src/pages/index.astro")
        print("  python3 recover_from_cursor.py extension/AShare-manual/src/pages/index.astro 2025-12-13 6 9")
        print("  python3 recover_from_cursor.py extension/AShare-manual/src/pages/ashare-book6 --dir 2025-12-13 6 9")
        sys.exit(1)
    
    target_path = Path(sys.argv[1])
    target_date = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "--dir" else None
    target_hour_start = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] != "--dir" else None
    target_hour_end = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[2] != "--dir" else None
    
    if "--dir" in sys.argv:
        idx = sys.argv.index("--dir")
        target_date = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else None
        target_hour_start = int(sys.argv[idx + 2]) if len(sys.argv) > idx + 2 else None
        target_hour_end = int(sys.argv[idx + 3]) if len(sys.argv) > idx + 3 else None
        recover_directory(target_path, target_date, target_hour_start, target_hour_end)
    else:
        recover_file(target_path, target_date, target_hour_start, target_hour_end)
