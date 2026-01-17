#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时监控HMM验证进度
"""
import time
import subprocess
import os
from datetime import datetime

LOG_FILE = "/tmp/hmm_validation.log"
PID_FILE = None

def get_process_info():
    """获取进程信息"""
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if 'validate_hmm_trend_accuracy' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) >= 3:
                    return {
                        'pid': parts[1],
                        'cpu': parts[2],
                        'mem': parts[3],
                        'status': parts[7] if len(parts) > 7 else 'N/A'
                    }
    except:
        pass
    return None

def get_log_tail(n=20):
    """获取日志最后N行"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                return lines[-n:] if len(lines) > n else lines
    except:
        pass
    return []

def count_validation_periods():
    """统计已完成的验证时期"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 统计"验证时期"出现的次数
                periods = content.count('验证时期:')
                # 统计"时期验证完成"出现的次数
                completed = content.count('时期验证完成')
                return periods, completed
    except:
        pass
    return 0, 0

def main():
    print("=" * 80)
    print("HMM验证进度实时监控")
    print("=" * 80)
    print(f"日志文件: {LOG_FILE}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    last_line_count = 0
    
    while True:
        # 检查进程
        proc_info = get_process_info()
        
        if proc_info:
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 进程运行中 | PID: {proc_info['pid']} | CPU: {proc_info['cpu']}% | 内存: {proc_info['mem']}%", end='', flush=True)
        else:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ⚠️  进程未找到，可能已完成或出错", end='', flush=True)
        
        # 统计进度
        total_periods, completed_periods = count_validation_periods()
        if total_periods > 0:
            progress = (completed_periods / total_periods) * 100 if total_periods > 0 else 0
            print(f" | 进度: {completed_periods}/{total_periods} ({progress:.1f}%)", end='', flush=True)
        
        # 显示最新日志
        log_lines = get_log_tail(5)
        if log_lines:
            current_line_count = len(log_lines)
            if current_line_count != last_line_count:
                print()  # 换行
                for line in log_lines[-3:]:  # 只显示最后3行
                    line = line.strip()
                    if line and ('INFO' in line or 'ERROR' in line or 'WARNING' in line):
                        # 提取关键信息
                        if '验证时期:' in line:
                            period = line.split('验证时期:')[1].strip() if '验证时期:' in line else ''
                            print(f"  📊 {period}")
                        elif '时期验证完成' in line:
                            print(f"  ✅ {line.split('INFO')[1].strip() if 'INFO' in line else line}")
                        elif 'ERROR' in line:
                            print(f"  ❌ {line.split('ERROR')[1].strip() if 'ERROR' in line else line}")
                        elif '批量分析' in line:
                            print(f"  🔄 {line.split('批量分析:')[1].strip() if '批量分析:' in line else line}")
                last_line_count = current_line_count
        
        # 检查是否完成
        if proc_info is None:
            # 检查日志中是否有完成标记
            try:
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if '验证完成' in content or '生成报告' in content:
                            print("\n\n✅ 验证已完成！")
                            print("\n最新日志:")
                            print("-" * 80)
                            tail_lines = get_log_tail(10)
                            for line in tail_lines:
                                print(line.rstrip())
                            break
            except:
                pass
        
        time.sleep(2)  # 每2秒更新一次

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n监控已停止")
    except Exception as e:
        print(f"\n\n监控出错: {e}")
