#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成PTrade策略代码脚本
==================

功能：
1. 基于当前策略配置生成PTrade格式的策略代码
2. 自动保存到strategies/ptrade目录
3. 支持自定义参数

使用方法：
    python scripts/generate_ptrade_strategy.py
    python scripts/generate_ptrade_strategy.py --max-stocks 15 --stop-loss -0.10
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.ptrade_strategy_generator import PTradeStrategyGenerator
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成PTrade策略代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认参数
  python scripts/generate_ptrade_strategy.py
  
  # 自定义参数
  python scripts/generate_ptrade_strategy.py --max-stocks 15 --stop-loss -0.10 --take-profit 0.35
        """
    )
    
    # 策略参数
    parser.add_argument('--max-stocks', type=int, default=10,
                        help='最大持股数量，默认10')
    parser.add_argument('--single-position', type=float, default=0.20,
                        help='单票最大仓位，默认0.20即20%%')
    parser.add_argument('--stop-loss', type=float, default=-0.08,
                        help='止损比例，默认-0.08即-8%%')
    parser.add_argument('--take-profit', type=float, default=0.30,
                        help='止盈比例，默认0.30即30%%')
    parser.add_argument('--min-total-score', type=float, default=30.0,
                        help='最小综合得分，默认30.0')
    
    # 输出参数
    parser.add_argument('--output-dir', type=str, default='strategies/ptrade',
                        help='输出目录，默认strategies/ptrade')
    parser.add_argument('--output-name', type=str, default=None,
                        help='输出文件名，默认自动生成')
    
    args = parser.parse_args()
    
    # 创建策略配置
    config = StrategyConfig(
        max_stocks=args.max_stocks,
        single_position_max=args.single_position,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        min_total_score=args.min_total_score
    )
    
    # 创建生成器
    generator = PTradeStrategyGenerator(config=config)
    
    # 生成策略代码
    print("=" * 70)
    print("🔧 PTrade策略代码生成器")
    print("=" * 70)
    print(f"\n📊 策略参数:")
    print(f"   最大持股: {config.max_stocks}只")
    print(f"   单票仓位: {config.single_position_max*100:.0f}%")
    print(f"   止损: {config.stop_loss*100:.0f}%")
    print(f"   止盈: {config.take_profit*100:.0f}%")
    print(f"   最小得分: {config.min_total_score}")
    
    print(f"\n🔄 正在生成策略代码...")
    code = generator.generate_strategy_code()
    
    # 保存文件
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.output_name:
        output_file = output_dir / args.output_name
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f'TRQuant_V4_PTrade_{timestamp}.py'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\n✅ 策略代码生成成功!")
    print(f"   文件位置: {output_file}")
    print(f"   文件大小: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"   代码行数: {len(code.splitlines())} 行")
    
    print(f"\n📋 下一步操作:")
    print(f"   1. 打开文件: {output_file}")
    print(f"   2. 根据PTrade实际API调整数据获取和交易函数")
    print(f"   3. 确保已安装依赖: pip install pandas numpy")
    print(f"   4. 在PTrade平台中加载并运行策略")
    
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
