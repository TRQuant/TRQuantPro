#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略测试、优化和转换流程
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
from core.comprehensive_strategy_converter import convert_strategy_comprehensive

def run_bt_backtest(strategy, start, end, output):
    """运行BulletTrade回测"""
    cmd = [
        'extension/venv/bin/bullet-trade', 'backtest', strategy,
        '--start', start, '--end', end,
        '--cash', '1000000', '--benchmark', '000300.XSHG',
        '--output', output
    ]
    
    Path(output).mkdir(parents=True, exist_ok=True)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, '', str(e)

def get_metrics(output_dir):
    """获取回测指标"""
    metrics_file = Path(output_dir) / 'metrics.json'
    if not metrics_file.exists():
        return None
    with open(metrics_file, 'r') as f:
        data = json.load(f)
    return data.get('metrics', {})

# 主流程
print("=" * 70)
print("策略测试和优化流程")
print("=" * 70)

base_strategy = 'strategies/bullettrade/TRQuant_momentum_v3_improved.py'
optimized_strategy = 'strategies/bullettrade/TRQuant_momentum_v3_optimized.py'

# 步骤1: 1周测试
print("\n[1/4] 测试1周回测")
week_output = f'backtest_results/week_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
success, stdout, stderr = run_bt_backtest(base_strategy, '2025-09-06', '2025-09-13', week_output)

if not success:
    print(f"❌ 1周回测失败: {stderr[:200]}")
    sys.exit(1)

week_metrics = get_metrics(week_output)
if week_metrics:
    print(f"✅ 1周回测完成")
    print(f"   收益: {week_metrics.get('策略收益', 0)*100:.2f}%")
    print(f"   交易: {week_metrics.get('交易盈利次数', 0) + week_metrics.get('交易亏损次数', 0)}次")

# 步骤2: 1个月测试
print("\n[2/4] 测试1个月回测")
month_output = f'backtest_results/month_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
success, stdout, stderr = run_bt_backtest(base_strategy, '2025-08-14', '2025-09-13', month_output)

if not success:
    print(f"❌ 1个月回测失败: {stderr[:200]}")
    sys.exit(1)

month_metrics = get_metrics(month_output)
if not month_metrics:
    print("❌ 无法读取回测结果")
    sys.exit(1)

annual = month_metrics.get('策略年化收益', 0)
print(f"✅ 1个月回测完成")
print(f"   收益: {month_metrics.get('策略收益', 0)*100:.2f}%")
print(f"   年化: {annual*100:.2f}%")
print(f"   夏普: {month_metrics.get('夏普比率', 0):.2f}")
print(f"   回撤: {month_metrics.get('最大回撤', 0)*100:.2f}%")

# 步骤3: 如果年化<60%，使用优化策略
if annual < 0.60 and Path(optimized_strategy).exists():
    print(f"\n[3/4] 年化{annual*100:.2f}% < 60%，使用优化策略")
    opt_output = f'backtest_results/optimized_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    success, stdout, stderr = run_bt_backtest(optimized_strategy, '2025-08-14', '2025-09-13', opt_output)
    
    if success:
        opt_metrics = get_metrics(opt_output)
        if opt_metrics:
            opt_annual = opt_metrics.get('策略年化收益', 0)
            print(f"✅ 优化策略回测完成")
            print(f"   年化: {opt_annual*100:.2f}%")
            
            if opt_annual > annual:
                annual = opt_annual
                month_metrics = opt_metrics
                base_strategy = optimized_strategy
                print(f"✅ 优化策略更优，年化提升到 {annual*100:.2f}%")
            else:
                print(f"⚠️ 优化策略未提升，保持原策略")
    else:
        print(f"⚠️ 优化策略回测失败，使用原策略")

# 步骤4: 转换为PTrade
print(f"\n[4/4] 转换为PTrade版本")
ptrade_file = base_strategy.replace('bullettrade', 'ptrade').replace('.py', '_final_ptrade.py')
result = convert_strategy_comprehensive(base_strategy, ptrade_file)

if result['success']:
    print(f"✅ PTrade版本已生成: {ptrade_file}")
    print(f"   变更: {len(result['changes'])}条")
    if result['warnings']:
        print(f"   警告: {len(result['warnings'])}条")
else:
    print(f"❌ 转换失败: {result['errors']}")

print(f"\n{'='*70}")
print("流程完成！")
print(f"{'='*70}")
print(f"最终年化收益: {annual*100:.2f}%")
print(f"BulletTrade策略: {base_strategy}")
print(f"PTrade策略: {ptrade_file}")
print(f"{'='*70}")
