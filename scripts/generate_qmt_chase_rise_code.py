#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成追涨策略QMT代码

Phase 4: QMT代码转换
- 从最优参数生成QMT回测代码
- 从最优参数生成QMT实盘代码
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.qmt.chase_rise_strategy_generator import ChaseRiseStrategyGenerator, ChaseRiseStrategyConfig
from scripts.evaluate_chase_rise_strategy import load_best_params

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("生成追涨策略QMT代码")
    logger.info("=" * 70)
    
    # 加载最优参数
    best_params = load_best_params()
    if not best_params:
        logger.warning("未找到最优参数，使用默认参数")
        best_params = {
            'limit_up_threshold': 0.095,
            'vol_ratio_threshold_first': 3.0,
            'mom_5d_threshold_breakout': 15.0,
            'mom_5d_threshold_volume': 10.0,
            'vol_ratio_threshold_breakout': 1.5,
            'vol_ratio_threshold_volume': 2.0,
            'min_signal_score': 55.0,
            'max_positions': 2,
            'stop_loss_pct': -10.0,
            'take_profit_pct': 25.0,
            'rebalance_days': 5,
            'warmup_bars': 22,
        }
    
    # 创建配置对象
    config = ChaseRiseStrategyConfig(**best_params)
    
    # 创建生成器
    generator = ChaseRiseStrategyGenerator(config)
    
    # 生成回测代码
    logger.info("\n生成QMT回测代码...")
    backtest_code = generator.generate_backtest_code()
    
    # 生成实盘代码
    logger.info("生成QMT实盘代码...")
    live_code = generator.generate_live_code()
    
    # 保存代码
    output_dir = PROJECT_ROOT / 'strategies' / 'qmt'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存回测代码
    backtest_path = output_dir / f'TRQuant_ChaseRise_V1_{timestamp}.py'
    with open(backtest_path, 'w', encoding='gbk') as f:
        f.write(backtest_code)
    logger.info(f"✅ 回测代码已保存: {backtest_path}")
    
    # 保存实盘代码
    live_path = output_dir / f'TRQuant_ChaseRise_V1_Live_{timestamp}.py'
    with open(live_path, 'w', encoding='gbk') as f:
        f.write(live_code)
    logger.info(f"✅ 实盘代码已保存: {live_path}")
    
    # 保存参数配置
    params_path = output_dir / f'TRQuant_ChaseRise_V1_params_{timestamp}.json'
    with open(params_path, 'w', encoding='utf-8') as f:
        json.dump(best_params, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ 参数配置已保存: {params_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("代码生成完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
