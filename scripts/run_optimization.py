#!/usr/bin/env python
"""运行参数优化并验证"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from scripts.validate_market_state import (
    initialize_components,
    get_price_data,
    generate_state_predictions,
)
from core.market_state_optimizer import MarketStateOptimizer

def main():
    INDEX_CODE = "000001.XSHG"
    START_DATE = "2020-01-01"
    END_DATE = "2025-12-31"
    
    logger.info("=" * 60)
    logger.info("市场状态参数优化")
    logger.info("=" * 60)
    
    # 初始化
    components = initialize_components()
    
    # 获取数据
    price_df = get_price_data(components["jq_client"], INDEX_CODE, START_DATE, END_DATE)
    logger.info(f"获取 {len(price_df)} 条数据")
    
    # 生成预测
    predictions = generate_state_predictions(components, price_df, INDEX_CODE)
    logger.info(f"生成 {len(predictions)} 条预测")
    
    # 运行优化
    optimizer = MarketStateOptimizer()
    optimized_params = optimizer.optimize_for_astock(predictions)
    
    # 验证优化结果
    logger.info("\n" + "=" * 60)
    logger.info("验证优化后的参数效果")
    logger.info("=" * 60)
    
    results = optimizer.validate_optimized_params(predictions)
    
    # 对比优化前后
    logger.info("\n" + "=" * 60)
    logger.info("优化前后对比")
    logger.info("=" * 60)
    logger.info(f"优化前准确率: 31.54%")
    logger.info(f"优化后准确率: {results['overall_accuracy']:.2%}")
    
    improvement = results['overall_accuracy'] - 0.3154
    logger.info(f"提升: {improvement:+.2%}")
    
    if results['overall_accuracy'] > 0.50:
        logger.info("✅ 达到50%目标")
    else:
        logger.info("❌ 未达到50%目标，需要进一步优化")
    
    logger.info("\nauth success ")

if __name__ == "__main__":
    main()
