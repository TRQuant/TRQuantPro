#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时监控长期回测验证进程
========================

持续监控验证脚本的运行状态、进度和输出

作者: TRQuant Team
日期: 2026-01-12
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from datetime import datetime

def clear_screen():
    """清屏"""
    os.system('clear' if os.name != 'nt' else 'cls')

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
    """获取进程详细信息"""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if 'validate_market_type_v7_long_term' in line and 'grep' not in line and 'monitor' not in line:
                parts = line.split()
                if len(parts) >= 11:
                    return {
                        'pid': parts[1],
                        'cpu': float(parts[2]),
                        'mem': float(parts[3]),
                        'time': parts[9],
                        'vsz': parts[4],  # 虚拟内存
                        'rss': parts[5],  # 物理内存
                    }
    except Exception as e:
        print(f"获取进程信息失败: {e}")
    return None

def check_output_files():
    """检查输出文件"""
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/market_type_validation")
    if output_dir.exists():
        md_files = list(output_dir.glob("validation_report_*.md"))
        if md_files:
            latest = max(md_files, key=lambda p: p.stat().st_mtime)
            try:
                content = latest.read_text(encoding='utf-8')
                return {
                    'exists': True,
                    'latest_file': latest.name,
                    'file_size': latest.stat().st_size,
                    'modified_time': datetime.fromtimestamp(latest.stat().st_mtime),
                    'content': content[:500] if len(content) > 500 else content  # 前500字符
                }
            except:
                return {
                    'exists': True,
                    'latest_file': latest.name,
                    'file_size': latest.stat().st_size,
                    'modified_time': datetime.fromtimestamp(latest.stat().st_mtime),
                }
    return {'exists': False}

def estimate_progress(proc_info):
    """估算进度"""
    if not proc_info:
        return None
    
    # 根据运行时间估算
    time_str = proc_info['time']
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
                total_seconds = minutes * 60 + seconds
            else:
                total_seconds = int(time_str)
        else:
            total_seconds = int(time_str)
        
        # 估算：每个时间段约5-10分钟，共4个时间段
        # 假设平均每个时间段7.5分钟 = 450秒
        total_estimated = 4 * 450  # 30分钟 = 1800秒
        
        if total_seconds < total_estimated:
            progress = (total_seconds / total_estimated) * 100
            return {
                'progress': min(progress, 99),  # 最多99%，避免显示100%但未完成
                'elapsed_seconds': total_seconds,
                'estimated_total': total_estimated,
                'estimated_remaining': max(0, total_estimated - total_seconds)
            }
    except:
        pass
    
    return None

def monitor_live(interval=10):
    """实时监控"""
    print("=" * 70)
    print("长期回测验证 - 实时监控")
    print("=" * 70)
    print("按 Ctrl+C 退出监控")
    print()
    
    start_time = datetime.now()
    last_status = None
    
    try:
        while True:
            clear_screen()
            current_time = datetime.now()
            elapsed = (current_time - start_time).total_seconds()
            
            print("=" * 70)
            print(f"长期回测验证 - 实时监控")
            print(f"监控开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"监控时长: {int(elapsed // 60)}分{int(elapsed % 60)}秒")
            print("=" * 70)
            print()
            
            # 检查进程
            is_running = check_process()
            if not is_running:
                print("❌ 验证进程未运行")
                print()
                output_info = check_output_files()
                if output_info.get('exists'):
                    print("✅ 但发现验证报告，可能已完成")
                    print(f"  文件: {output_info['latest_file']}")
                    print(f"  修改时间: {output_info['modified_time']}")
                else:
                    print("提示: 进程可能已结束或出错")
                print()
                print("按 Ctrl+C 退出")
                time.sleep(interval)
                continue
            
            print("✅ 验证进程正在运行")
            print()
            
            # 获取进程信息
            proc_info = get_process_info()
            if proc_info:
                print("进程信息:")
                print(f"  PID: {proc_info['pid']}")
                print(f"  CPU使用率: {proc_info['cpu']:.1f}%")
                print(f"  内存使用: {proc_info['mem']:.1f}%")
                print(f"  虚拟内存: {proc_info['vsz']} KB")
                print(f"  物理内存: {proc_info['rss']} KB")
                print(f"  运行时间: {proc_info['time']}")
                print()
                
                # 估算进度
                progress_info = estimate_progress(proc_info)
                if progress_info:
                    print("进度估算:")
                    print(f"  已完成: {progress_info['progress']:.1f}%")
                    print(f"  已运行: {int(progress_info['elapsed_seconds'] // 60)}分{int(progress_info['elapsed_seconds'] % 60)}秒")
                    remaining_min = int(progress_info['estimated_remaining'] // 60)
                    remaining_sec = int(progress_info['estimated_remaining'] % 60)
                    print(f"  预计剩余: {remaining_min}分{remaining_sec}秒")
                    print()
            
            # 检查输出文件
            output_info = check_output_files()
            if output_info.get('exists'):
                print("✅ 验证报告已生成:")
                print(f"  文件: {output_info['latest_file']}")
                print(f"  大小: {output_info['file_size']} 字节")
                print(f"  修改时间: {output_info['modified_time'].strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                if 'content' in output_info:
                    print("报告预览:")
                    print("-" * 70)
                    print(output_info['content'])
                    print("-" * 70)
                    print()
                    print("✅ 验证已完成！")
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
            print(f"下次更新: {interval}秒后 (按 Ctrl+C 退出)")
            print("=" * 70)
            
            last_status = is_running
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 70)
        print("监控已停止")
        print("=" * 70)
        
        # 最终检查
        output_info = check_output_files()
        if output_info.get('exists'):
            print()
            print("✅ 验证报告:")
            print(f"  文件: {output_info['latest_file']}")
            print(f"  路径: /home/taotao/.cursor/worktrees/TRQuant/ope/output/market_type_validation/{output_info['latest_file']}")
        else:
            print()
            print("⏳ 验证可能仍在进行中")
            print("  可稍后运行以下命令查看:")
            print("  python scripts/monitor_validation.py")

if __name__ == "__main__":
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    monitor_live(interval)
