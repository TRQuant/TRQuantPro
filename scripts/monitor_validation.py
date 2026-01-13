#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
监控长期回测验证进程
====================

实时监控验证脚本的运行状态和进度

作者: TRQuant Team
日期: 2026-01-12
"""

import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

def check_process():
    """检查验证进程是否运行"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'validate_market_type_v7_long_term'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def get_process_info():
    """获取进程信息"""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if 'validate_market_type_v7_long_term' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) >= 11:
                    return {
                        'pid': parts[1],
                        'cpu': parts[2],
                        'mem': parts[3],
                        'time': parts[9],
                        'command': ' '.join(parts[10:])
                    }
    except:
        pass
    return None

def check_output_files():
    """检查输出文件"""
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/market_type_validation")
    if output_dir.exists():
        md_files = list(output_dir.glob("*.md"))
        if md_files:
            latest = max(md_files, key=lambda p: p.stat().st_mtime)
            return {
                'exists': True,
                'latest_file': latest.name,
                'file_size': latest.stat().st_size,
                'modified_time': datetime.fromtimestamp(latest.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            }
    return {'exists': False}

def monitor():
    """监控主函数"""
    print("=" * 70)
    print("长期回测验证进程监控")
    print("=" * 70)
    print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查进程
    is_running = check_process()
    if not is_running:
        print("❌ 验证进程未运行")
        print()
        print("提示: 运行以下命令启动验证:")
        print("  cd /home/taotao/.cursor/worktrees/TRQuant/ope")
        print("  ./venv/bin/python scripts/validate_market_type_v7_long_term.py")
        return
    
    print("✅ 验证进程正在运行")
    print()
    
    # 获取进程信息
    proc_info = get_process_info()
    if proc_info:
        print("进程信息:")
        print(f"  PID: {proc_info['pid']}")
        print(f"  CPU使用率: {proc_info['cpu']}%")
        print(f"  内存使用: {proc_info['mem']}%")
        print(f"  运行时间: {proc_info['time']}")
        print()
    
    # 检查输出文件
    output_info = check_output_files()
    if output_info['exists']:
        print("✅ 验证报告已生成:")
        print(f"  文件: {output_info['latest_file']}")
        print(f"  大小: {output_info['file_size']} 字节")
        print(f"  修改时间: {output_info['modified_time']}")
        print()
        print("提示: 验证可能已完成，请查看报告文件")
    else:
        print("⏳ 验证报告尚未生成（验证进行中...）")
        print()
        print("预计完成时间:")
        print("  - 每个时间段: 约5-10分钟")
        print("  - 总共4个时间段: 约20-40分钟")
        print()
        print("提示: 验证完成后，报告将保存在:")
        print("  output/market_type_validation/validation_report_*.md")
    
    print()
    print("=" * 70)
    print("监控完成")
    print("=" * 70)
    print()
    print("继续监控命令:")
    print("  watch -n 30 python scripts/monitor_validation.py")
    print("  或")
    print("  while true; do python scripts/monitor_validation.py; sleep 30; done")

if __name__ == "__main__":
    monitor()
