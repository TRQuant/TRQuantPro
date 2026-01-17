#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成QMT策略代码脚本
==================

功能：
1. 基于当前策略配置生成QMT格式的策略代码
2. 自动保存到strategies/qmt目录
3. 支持自定义参数

使用方法：
    python scripts/generate_qmt_strategy.py
    python scripts/generate_qmt_strategy.py --max-stocks 15 --stop-loss -0.10
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.qmt_strategy_generator import QMTStrategyGenerator
from core.advisor_v4.qmt_research_strategy_generator import QMTResearchStrategyGenerator
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成QMT策略代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认参数
  python scripts/generate_qmt_strategy.py
  
  # 自定义参数
  python scripts/generate_qmt_strategy.py --max-stocks 15 --stop-loss -0.10 --take-profit 0.35
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
    parser.add_argument('--output-dir', type=str, default='strategies/qmt',
                        help='输出目录，默认strategies/qmt')
    parser.add_argument('--output-name', type=str, default=None,
                        help='输出文件名，默认自动生成')
    parser.add_argument('--research', action='store_true',
                        help='生成研究环境版本（使用ContextInfo API，无需连接交易账户）')
    
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
    if args.research:
        generator = QMTResearchStrategyGenerator(config=config)
        version_type = "研究环境版本"
    else:
        generator = QMTStrategyGenerator(config=config)
        version_type = "连接版本"
    
    # 生成策略代码
    print("=" * 70)
    print(f"🔧 QMT策略代码生成器 - {version_type}")
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
        if args.research:
            output_file = output_dir / f'TRQuant_V4_QMT_Research_{timestamp}.py'
        else:
            output_file = output_dir / f'TRQuant_V4_QMT_{timestamp}.py'
    
    # 保存文件，使用UTF-8编码（确保Windows QMT可以正确读取）
    # 注意：Windows QMT可能需要UTF-8编码，使用二进制模式写入确保编码正确
    try:
        # 先尝试文本模式
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 验证文件编码
        with open(output_file, 'r', encoding='utf-8') as f:
            test_content = f.read()
            if len(test_content) > 0:
                print(f"✅ 文件编码验证通过（UTF-8）")
            else:
                raise ValueError("文件内容为空")
    except Exception as e:
        print(f"⚠️  文本模式保存失败: {e}")
        print(f"   尝试二进制模式保存...")
        # 使用二进制模式保存，确保UTF-8编码
        with open(output_file, 'wb') as f:
            f.write(code.encode('utf-8'))
        print(f"✅ 二进制模式保存成功（UTF-8）")
    
    print(f"\n✅ 策略代码生成成功!")
    print(f"   文件位置: {output_file}")
    print(f"   文件大小: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"   代码行数: {len(code.splitlines())} 行")
    
    print(f"\n📋 下一步操作:")
    print(f"   1. 打开文件: {output_file}")
    if args.research:
        print(f"   2. 在QMT研究环境中加载策略文件")
        print(f"   3. 设置回测参数（起始日期、结束日期、初始资金）")
        print(f"   4. 点击运行回测")
        print(f"\n💡 提示: 研究环境版本使用ContextInfo API，无需连接交易账户")
    else:
        print(f"   2. 修改QMT_PATH、SESSION_ID、ACCOUNT_ID为实际值")
        print(f"   3. 确保已安装依赖: pip install xtquant schedule")
        print(f"   4. 在QMT客户端中加载并运行策略")
    
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
