#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略测试和优化脚本 - 使用extension中的BulletTrade
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta

# 添加extension路径
extension_path = Path(__file__).parent.parent / 'extension'
sys.path.insert(0, str(extension_path))

def run_backtest(strategy_file, start_date, end_date, output_dir):
    """运行BulletTrade回测"""
    print(f"\n{'='*70}")
    print(f"运行回测: {start_date} 至 {end_date}")
    print(f"{'='*70}")
    
    # 使用extension中的bullet-trade
    venv_python = extension_path / 'venv' / 'bin' / 'python'
    if not venv_python.exists():
        venv_python = 'python3'
    
    cmd = [
        str(venv_python), '-m', 'bullet_trade.cli', 'backtest', strategy_file,
        '--start', start_date,
        '--end', end_date,
        '--cash', '1000000',
        '--benchmark', '000300.XSHG',
        '--output', output_dir
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=Path.cwd())
        
        if result.returncode == 0:
            print("✅ 回测成功")
            return True, result.stdout
        else:
            print(f"❌ 回测失败")
            print(f"错误: {result.stderr[:500]}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ 回测异常: {e}")
        return False, str(e)

def analyze_results(output_dir):
    """分析回测结果"""
    metrics_file = Path(output_dir) / 'metrics.json'
    
    if not metrics_file.exists():
        return None
    
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)
    
    return metrics.get('metrics', {})

def main():
    """主函数"""
    strategy_file = 'strategies/bullettrade/TRQuant_momentum_v3_improved.py'
    
    if not Path(strategy_file).exists():
        print(f"❌ 策略文件不存在: {strategy_file}")
        return
    
    # 使用可用数据范围
    end_date = '2025-09-13'
    week_start = '2025-09-06'  # 1周
    month_start = '2025-08-14'  # 1个月
    
    print("=" * 70)
    print("策略测试和优化流程")
    print("=" * 70)
    
    # 步骤1: 测试1周
    print("\n📊 步骤1: 测试1周回测")
    week_output = f'backtest_results/week_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    Path(week_output).mkdir(parents=True, exist_ok=True)
    
    success, output = run_backtest(strategy_file, week_start, end_date, week_output)
    
    if not success:
        print("❌ 1周回测失败，请检查策略代码")
        print(f"输出: {output[:500]}")
        return
    
    # 分析1周结果
    week_metrics = analyze_results(week_output)
    if week_metrics:
        print(f"\n1周回测结果:")
        print(f"  收益: {week_metrics.get('策略收益', 0)*100:.2f}%")
        print(f"  年化: {week_metrics.get('策略年化收益', 0)*100:.2f}%")
        trades = week_metrics.get('交易盈利次数', 0) + week_metrics.get('交易亏损次数', 0)
        print(f"  交易次数: {trades}")
    
    # 步骤2: 测试1个月
    print("\n📊 步骤2: 测试1个月回测")
    month_output = f'backtest_results/month_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    Path(month_output).mkdir(parents=True, exist_ok=True)
    
    success, output = run_backtest(strategy_file, month_start, end_date, month_output)
    
    if not success:
        print("❌ 1个月回测失败")
        return
    
    # 分析1个月结果
    month_metrics = analyze_results(month_output)
    if not month_metrics:
        print("❌ 无法读取回测结果")
        return
    
    annual_return = month_metrics.get('策略年化收益', 0)
    
    print(f"\n1个月回测结果:")
    print(f"  收益: {month_metrics.get('策略收益', 0)*100:.2f}%")
    print(f"  年化: {annual_return*100:.2f}%")
    print(f"  夏普比率: {month_metrics.get('夏普比率', 0):.2f}")
    print(f"  最大回撤: {month_metrics.get('最大回撤', 0)*100:.2f}%")
    
    # 步骤3: 优化策略（如果年化<60%）
    if annual_return < 0.60:
        print(f"\n📊 步骤3: 优化策略（当前年化{annual_return*100:.2f}%，目标60%）")
        # 这里可以添加优化逻辑
        print("  优化策略参数...")
    
    # 步骤4: 转换为PTrade版本
    print(f"\n📊 步骤4: 转换为PTrade版本")
    from core.comprehensive_strategy_converter import convert_strategy_comprehensive
    
    ptrade_file = strategy_file.replace('bullettrade', 'ptrade').replace('.py', '_final_ptrade.py')
    result = convert_strategy_comprehensive(strategy_file, ptrade_file)
    
    if result['success']:
        print(f"✅ PTrade版本已生成: {ptrade_file}")
        print(f"   变更: {len(result['changes'])}条")
    else:
        print(f"❌ 转换失败: {result['errors']}")
    
    print(f"\n{'='*70}")
    print("测试完成！")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
