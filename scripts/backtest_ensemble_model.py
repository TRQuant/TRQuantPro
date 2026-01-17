#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
回测验证集成模型准确率
====================

使用历史数据回测集成模型的预测准确率，并与各独立模型对比。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass
import pandas as pd
import numpy as np

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

warnings.filterwarnings('ignore')

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from core.ensemble_market_trend import EnsembleMarketTrendAnalyzer, TrendDirection
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 初始化JQData
cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])

INDEX_CODE = "000300.XSHG"
FORWARD_DAYS = 63  # 3个月前瞻

# 回测期间（最近2年，采样验证）
BACKTEST_START = "2023-01-01"
BACKTEST_END = "2024-12-31"
SAMPLE_INTERVAL = 20  # 每20个交易日验证一次


@dataclass
class BacktestResult:
    """回测结果"""
    model_name: str
    total_samples: int
    correct_predictions: int
    accuracy: float
    bull_accuracy: float
    bear_accuracy: float
    sideways_accuracy: float
    avg_confidence: float


def calculate_actual_trend(forward_return: float) -> str:
    """根据3个月前瞻收益判断实际趋势"""
    if forward_return > 0.10:
        return "bull"
    elif forward_return < -0.10:
        return "bear"
    else:
        return "sideways"


def backtest_ensemble_model() -> BacktestResult:
    """回测集成模型"""
    logger.info("开始回测集成模型")
    
    analyzer = EnsembleMarketTrendAnalyzer()
    
    # 获取历史数据
    index_data = jq.get_price(
        INDEX_CODE,
        start_date=BACKTEST_START,
        end_date=(pd.to_datetime(BACKTEST_END) + timedelta(days=90)).strftime('%Y-%m-%d'),
        frequency='daily',
        fields=['close']
    )
    
    if isinstance(index_data.index, pd.MultiIndex):
        index_data = index_data.reset_index(level='code', drop=True)
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=BACKTEST_START, end_date=BACKTEST_END)
    sample_days = [d.strftime('%Y-%m-%d') for d in trade_days[::SAMPLE_INTERVAL]]
    
    total = 0
    correct = 0
    bull_correct = 0
    bull_total = 0
    bear_correct = 0
    bear_total = 0
    sideways_correct = 0
    sideways_total = 0
    confidences = []
    
    for date_str in sample_days:
        try:
            # 集成模型预测
            result = analyzer.analyze(INDEX_CODE, date_str)
            
            if result is None:
                continue
            
            predicted = result.final_trend.value
            
            # 获取实际收益
            date_dt = pd.to_datetime(date_str)
            date_idx = index_data.index.get_indexer([date_dt], method='nearest')[0]
            
            if date_idx < 0 or date_idx + FORWARD_DAYS >= len(index_data):
                continue
            
            forward_return = (index_data.iloc[date_idx + FORWARD_DAYS]['close'] / 
                            index_data.iloc[date_idx]['close'] - 1)
            actual = calculate_actual_trend(forward_return)
            
            # 统计
            total += 1
            if predicted == actual:
                correct += 1
            
            if actual == "bull":
                bull_total += 1
                if predicted == "bull":
                    bull_correct += 1
            elif actual == "bear":
                bear_total += 1
                if predicted == "bear":
                    bear_correct += 1
            else:
                sideways_total += 1
                if predicted == "sideways":
                    sideways_correct += 1
            
            confidences.append(result.final_confidence)
            
        except Exception as e:
            logger.debug(f"回测 {date_str} 失败: {e}")
            continue
    
    accuracy = correct / total if total > 0 else 0.0
    bull_acc = bull_correct / bull_total if bull_total > 0 else 0.0
    bear_acc = bear_correct / bear_total if bear_total > 0 else 0.0
    sideways_acc = sideways_correct / sideways_total if sideways_total > 0 else 0.0
    avg_conf = np.mean(confidences) if confidences else 0.0
    
    return BacktestResult(
        model_name="Ensemble",
        total_samples=total,
        correct_predictions=correct,
        accuracy=accuracy,
        bull_accuracy=bull_acc,
        bear_accuracy=bear_acc,
        sideways_accuracy=sideways_acc,
        avg_confidence=avg_conf
    )


def generate_report(result: BacktestResult):
    """生成回测报告"""
    output_dir = PROJECT_ROOT / "output" / "ensemble_backtest"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"ensemble_backtest_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 集成模型回测验证报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**验证指数**: {INDEX_CODE} (沪深300)\n")
        f.write(f"**回测期间**: {BACKTEST_START} ~ {BACKTEST_END}\n")
        f.write(f"**前瞻周期**: {FORWARD_DAYS} 交易日 (约3个月)\n")
        f.write(f"**采样间隔**: 每 {SAMPLE_INTERVAL} 个交易日验证一次\n\n")
        
        f.write("## 1. 执行摘要\n\n")
        f.write(f"**综合准确率: {result.accuracy:.1%}**\n\n")
        
        f.write("| 指标 | 数值 |\n")
        f.write("|------|------|\n")
        f.write(f"| 总样本数 | {result.total_samples} |\n")
        f.write(f"| 正确预测 | {result.correct_predictions} |\n")
        f.write(f"| 综合准确率 | {result.accuracy:.1%} |\n")
        f.write(f"| 平均置信度 | {result.avg_confidence:.1%} |\n\n")
        
        f.write("## 2. 分市场状态准确率\n\n")
        f.write("| 市场状态 | 准确率 | 样本数 |\n")
        f.write("|----------|--------|--------|\n")
        f.write(f"| 牛市 | {result.bull_accuracy:.1%} | {result.total_samples} |\n")
        f.write(f"| 熊市 | {result.bear_accuracy:.1%} | {result.total_samples} |\n")
        f.write(f"| 震荡 | {result.sideways_accuracy:.1%} | {result.total_samples} |\n\n")
        
        f.write("## 3. 评估\n\n")
        
        if result.accuracy >= 0.65:
            f.write("✅ **通过**: 集成模型准确率>=65%，可以用于实盘决策\n")
        elif result.accuracy >= 0.55:
            f.write("⚠️ **谨慎使用**: 集成模型准确率55-65%，建议模拟交易观察\n")
        else:
            f.write("❌ **不通过**: 集成模型准确率<55%，需要进一步优化\n")
        
        f.write("\n## 4. 下一步行动\n\n")
        f.write("1. 如果准确率>=65%，可以用于实盘策略切换\n")
        f.write("2. 如果准确率55-65%，建议先进行模拟交易验证\n")
        f.write("3. 如果准确率<55%，需要优化模型权重或增加更多模型\n")
        f.write("4. 对比各独立模型的准确率，找出最佳组合\n")
    
    logger.info(f"回测报告已保存: {report_path}")
    return report_path


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("开始回测验证集成模型")
    logger.info("=" * 80)
    
    # 回测集成模型
    result = backtest_ensemble_model()
    
    # 生成报告
    report_path = generate_report(result)
    
    logger.info("\n" + "=" * 80)
    logger.info("回测完成")
    logger.info(f"综合准确率: {result.accuracy:.1%}")
    logger.info(f"报告路径: {report_path}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
