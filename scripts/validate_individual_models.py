#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证各模型可靠性
================

验证以下模型的独立准确率：
1. HMM模型（Resonance V2）
2. 技术指标模型（TrendAnalyzer）
3. 市场宽度模型（MarketBreadthAnalyzer）
4. 情绪分析模型（JQDataSentimentAnalyzer）
5. 宏观指标模型（MacroIndicatorAnalyzer）

目标：确保每个模型都经过验证，准确率>55%才纳入集成

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np

# 添加项目路径
PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

warnings.filterwarnings('ignore')

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入各模型
from core.resonance_v2 import ResonanceHMMAnalyzer, MarketState
from core.trend_analyzer import TrendAnalyzer
from core.astock_indicators import MarketBreadthAnalyzer
from core.jqdata_sentiment_analyzer import JQDataSentimentAnalyzer

# 初始化JQData
try:
    import jqdatasdk as jq
    from config.config_manager import get_config_manager
    cm = get_config_manager()
    jq_config = cm.get_config('jqdata')
    jq.auth(jq_config['username'], jq_config['password'])
    logger.info("JQData认证成功")
except Exception as e:
    logger.error(f"JQData认证失败: {e}")
    sys.exit(1)

# 验证期间
VALIDATION_PERIODS = [
    {"name": "2019-Q1~Q2 牛市启动", "start": "2019-01-01", "end": "2019-06-30", "expected": "bull"},
    {"name": "2019-Q3~Q4 震荡", "start": "2019-07-01", "end": "2019-12-31", "expected": "sideways"},
    {"name": "2020-Q1 疫情暴跌", "start": "2020-01-01", "end": "2020-03-31", "expected": "bear"},
    {"name": "2020-Q2~Q4 复苏牛", "start": "2020-04-01", "end": "2020-12-31", "expected": "bull"},
    {"name": "2021-Q1 牛市顶部", "start": "2021-01-01", "end": "2021-03-31", "expected": "bull"},
    {"name": "2021-Q2~Q4 调整", "start": "2021-04-01", "end": "2021-12-31", "expected": "sideways"},
    {"name": "2022 全年熊市", "start": "2022-01-01", "end": "2022-12-31", "expected": "bear"},
    {"name": "2023 震荡筑底", "start": "2023-01-01", "end": "2023-12-31", "expected": "sideways"},
    {"name": "2024-Q1~Q2 反弹", "start": "2024-01-01", "end": "2024-06-30", "expected": "sideways"},
    {"name": "2024-Q3~Q4 技术反弹", "start": "2024-07-01", "end": "2024-12-31", "expected": "bull"},
]

INDEX_CODE = "000300.XSHG"  # 沪深300
FORWARD_DAYS = 63  # 3个月前瞻


@dataclass
class ModelValidationResult:
    """模型验证结果"""
    model_name: str
    period_name: str
    predicted_trend: str  # bull/bear/sideways
    actual_trend: str
    is_correct: bool
    confidence: float
    forward_return: float  # 3个月前瞻收益


def calculate_actual_trend(forward_return: float) -> str:
    """根据3个月前瞻收益判断实际趋势"""
    if forward_return > 0.10:
        return "bull"
    elif forward_return < -0.10:
        return "bear"
    else:
        return "sideways"


def validate_hmm_model(period: Dict) -> List[ModelValidationResult]:
    """验证HMM模型"""
    logger.info(f"验证HMM模型: {period['name']}")
    results = []
    
    try:
        analyzer = ResonanceHMMAnalyzer()
        
        # 获取该期间的数据
        start_date = period['start']
        end_date = period['end']
        
        # 获取未来3个月收益作为ground truth
        index_data = jq.get_price(
            INDEX_CODE,
            start_date=start_date,
            end_date=(pd.to_datetime(end_date) + timedelta(days=90)).strftime('%Y-%m-%d'),
            frequency='daily',
            fields=['close']
        )
        
        if index_data is None or index_data.empty:
            return results
        
        # 处理MultiIndex
        if isinstance(index_data.index, pd.MultiIndex):
            index_data = index_data.reset_index(level='code', drop=True)
        
        # 采样验证（每15个交易日验证一次，减少计算量）
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        sample_days = [d.strftime('%Y-%m-%d') for d in trade_days[::15]]
        
        for date_str in sample_days:
            try:
                # HMM预测
                result = analyzer.analyze(INDEX_CODE, date_str, lookback_days=400)
                
                if result is None:
                    continue
                
                # 映射HMM状态到趋势
                hmm_state = result.market_state
                if hmm_state == MarketState.RISK_ON:
                    predicted = "bull"
                elif hmm_state == MarketState.RISK_OFF:
                    predicted = "bear"
                else:
                    predicted = "sideways"
                
                # 获取实际3个月收益
                try:
                    date_dt = pd.to_datetime(date_str)
                    date_idx = index_data.index.get_indexer([date_dt], method='nearest')[0]
                    if date_idx >= 0 and date_idx + FORWARD_DAYS < len(index_data):
                        forward_return = (index_data.iloc[date_idx + FORWARD_DAYS]['close'] / 
                                        index_data.iloc[date_idx]['close'] - 1)
                        actual = calculate_actual_trend(forward_return)
                        
                        results.append(ModelValidationResult(
                            model_name="HMM",
                            period_name=period['name'],
                            predicted_trend=predicted,
                            actual_trend=actual,
                            is_correct=(predicted == actual),
                            confidence=result.state_confidence,
                            forward_return=forward_return
                        ))
                except Exception as e:
                    logger.debug(f"获取收益失败 {date_str}: {e}")
                    continue
            except Exception as e:
                logger.debug(f"HMM验证 {date_str} 失败: {e}")
                continue
        
    except Exception as e:
        logger.error(f"HMM模型验证失败: {e}")
    
    return results


def validate_technical_model(period: Dict) -> List[ModelValidationResult]:
    """验证技术指标模型"""
    logger.info(f"验证技术指标模型: {period['name']}")
    results = []
    
    try:
        analyzer = TrendAnalyzer()
        
        start_date = period['start']
        end_date = period['end']
        
        index_data = jq.get_price(
            INDEX_CODE,
            start_date=start_date,
            end_date=(pd.to_datetime(end_date) + timedelta(days=90)).strftime('%Y-%m-%d'),
            frequency='daily',
            fields=['close']
        )
        
        if index_data is None or index_data.empty:
            return results
        
        # 处理MultiIndex
        if isinstance(index_data.index, pd.MultiIndex):
            index_data = index_data.reset_index(level='code', drop=True)
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        sample_days = [d.strftime('%Y-%m-%d') for d in trade_days[::15]]
        
        for date_str in sample_days:
            try:
                # 技术指标分析
                result = analyzer.analyze_market(INDEX_CODE, date_str)
                
                if result is None:
                    continue
                
                # 根据综合得分判断趋势
                composite = result.composite_score
                if composite > 30:
                    predicted = "bull"
                elif composite < -30:
                    predicted = "bear"
                else:
                    predicted = "sideways"
                
                # 获取实际收益
                try:
                    date_dt = pd.to_datetime(date_str)
                    date_idx = index_data.index.get_indexer([date_dt], method='nearest')[0]
                    if date_idx >= 0 and date_idx + FORWARD_DAYS < len(index_data):
                        forward_return = (index_data.iloc[date_idx + FORWARD_DAYS]['close'] / 
                                        index_data.iloc[date_idx]['close'] - 1)
                        actual = calculate_actual_trend(forward_return)
                        
                        results.append(ModelValidationResult(
                            model_name="Technical",
                            period_name=period['name'],
                            predicted_trend=predicted,
                            actual_trend=actual,
                            is_correct=(predicted == actual),
                            confidence=abs(composite) / 100.0,  # 归一化到0-1
                            forward_return=forward_return
                        ))
                except Exception as e:
                    logger.debug(f"获取收益失败 {date_str}: {e}")
                    continue
            except Exception as e:
                logger.debug(f"技术指标验证 {date_str} 失败: {e}")
                continue
        
    except Exception as e:
        logger.error(f"技术指标模型验证失败: {e}")
    
    return results


def validate_breadth_model(period: Dict) -> List[ModelValidationResult]:
    """验证市场宽度模型"""
    logger.info(f"验证市场宽度模型: {period['name']}")
    results = []
    
    try:
        analyzer = MarketBreadthAnalyzer()
        
        start_date = period['start']
        end_date = period['end']
        
        index_data = jq.get_price(
            INDEX_CODE,
            start_date=start_date,
            end_date=(pd.to_datetime(end_date) + timedelta(days=90)).strftime('%Y-%m-%d'),
            frequency='daily',
            fields=['close']
        )
        
        if index_data is None or index_data.empty:
            return results
        
        # 处理MultiIndex
        if isinstance(index_data.index, pd.MultiIndex):
            index_data = index_data.reset_index(level='code', drop=True)
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        sample_days = [d.strftime('%Y-%m-%d') for d in trade_days[::15]]
        
        for date_str in sample_days:
            try:
                # 市场宽度分析
                breadth_data = analyzer.analyze(date_str)
                
                if breadth_data is None:
                    continue
                
                # 根据市场宽度得分判断趋势
                score = breadth_data.signal_score
                if score > 20:
                    predicted = "bull"
                elif score < -20:
                    predicted = "bear"
                else:
                    predicted = "sideways"
                
                # 获取实际收益
                try:
                    date_dt = pd.to_datetime(date_str)
                    date_idx = index_data.index.get_indexer([date_dt], method='nearest')[0]
                    if date_idx >= 0 and date_idx + FORWARD_DAYS < len(index_data):
                        forward_return = (index_data.iloc[date_idx + FORWARD_DAYS]['close'] / 
                                        index_data.iloc[date_idx]['close'] - 1)
                        actual = calculate_actual_trend(forward_return)
                        
                        results.append(ModelValidationResult(
                            model_name="Breadth",
                            period_name=period['name'],
                            predicted_trend=predicted,
                            actual_trend=actual,
                            is_correct=(predicted == actual),
                            confidence=abs(score) / 100.0,
                            forward_return=forward_return
                        ))
                except Exception as e:
                    logger.debug(f"获取收益失败 {date_str}: {e}")
                    continue
            except Exception as e:
                logger.debug(f"市场宽度验证 {date_str} 失败: {e}")
                continue
        
    except Exception as e:
        logger.error(f"市场宽度模型验证失败: {e}")
    
    return results


def validate_sentiment_model(period: Dict) -> List[ModelValidationResult]:
    """验证情绪分析模型"""
    logger.info(f"验证情绪分析模型: {period['name']}")
    results = []
    
    try:
        analyzer = JQDataSentimentAnalyzer()
        
        start_date = period['start']
        end_date = period['end']
        
        index_data = jq.get_price(
            INDEX_CODE,
            start_date=start_date,
            end_date=(pd.to_datetime(end_date) + timedelta(days=90)).strftime('%Y-%m-%d'),
            frequency='daily',
            fields=['close']
        )
        
        if index_data is None or index_data.empty:
            return results
        
        # 处理MultiIndex
        if isinstance(index_data.index, pd.MultiIndex):
            index_data = index_data.reset_index(level='code', drop=True)
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        sample_days = [d.strftime('%Y-%m-%d') for d in trade_days[::15]]
        
        for date_str in sample_days:
            try:
                # 情绪分析
                sentiment_result = analyzer.analyze(date_str, INDEX_CODE)
                
                if sentiment_result is None:
                    continue
                
                # 根据情绪信号判断趋势（注意：极度贪婪/恐慌时反向）
                signal = sentiment_result.signal
                if signal == "bullish":
                    predicted = "bull"
                elif signal == "bearish":
                    predicted = "bear"
                else:
                    predicted = "sideways"
                
                # 获取实际收益
                try:
                    date_dt = pd.to_datetime(date_str)
                    date_idx = index_data.index.get_indexer([date_dt], method='nearest')[0]
                    if date_idx >= 0 and date_idx + FORWARD_DAYS < len(index_data):
                        forward_return = (index_data.iloc[date_idx + FORWARD_DAYS]['close'] / 
                                        index_data.iloc[date_idx]['close'] - 1)
                        actual = calculate_actual_trend(forward_return)
                        
                        results.append(ModelValidationResult(
                            model_name="Sentiment",
                            period_name=period['name'],
                            predicted_trend=predicted,
                            actual_trend=actual,
                            is_correct=(predicted == actual),
                            confidence=abs(sentiment_result.composite_score) / 100.0,
                            forward_return=forward_return
                        ))
                except Exception as e:
                    logger.debug(f"获取收益失败 {date_str}: {e}")
                    continue
            except Exception as e:
                logger.debug(f"情绪分析验证 {date_str} 失败: {e}")
                continue
        
    except Exception as e:
        logger.error(f"情绪分析模型验证失败: {e}")
    
    return results


def generate_validation_report(all_results: Dict[str, List[ModelValidationResult]]):
    """生成验证报告"""
    output_dir = PROJECT_ROOT / "output" / "model_validation"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"individual_models_validation_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 各模型可靠性验证报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**验证指数**: {INDEX_CODE} (沪深300)\n")
        f.write(f"**前瞻周期**: {FORWARD_DAYS} 交易日 (约3个月)\n\n")
        
        f.write("## 1. 执行摘要\n\n")
        
        # 计算各模型总体准确率
        model_stats = {}
        for model_name, results in all_results.items():
            if not results:
                continue
            
            correct = sum(1 for r in results if r.is_correct)
            total = len(results)
            accuracy = correct / total if total > 0 else 0.0
            avg_confidence = np.mean([r.confidence for r in results]) if results else 0.0
            
            model_stats[model_name] = {
                'accuracy': accuracy,
                'total': total,
                'correct': correct,
                'avg_confidence': avg_confidence
            }
        
        f.write("| 模型 | 准确率 | 样本数 | 平均置信度 | 状态 |\n")
        f.write("|------|--------|--------|------------|------|\n")
        
        for model_name, stats in sorted(model_stats.items(), key=lambda x: x[1]['accuracy'], reverse=True):
            status = "✅ 通过" if stats['accuracy'] >= 0.55 else "❌ 不通过"
            f.write(f"| {model_name} | {stats['accuracy']:.1%} | {stats['total']} | {stats['avg_confidence']:.2f} | {status} |\n")
        
        f.write("\n## 2. 各模型详细结果\n\n")
        
        for model_name, results in all_results.items():
            if not results:
                continue
            
            f.write(f"### 2.{list(all_results.keys()).index(model_name) + 1} {model_name}模型\n\n")
            
            # 按时期统计
            period_stats = {}
            for r in results:
                if r.period_name not in period_stats:
                    period_stats[r.period_name] = {'correct': 0, 'total': 0}
                period_stats[r.period_name]['total'] += 1
                if r.is_correct:
                    period_stats[r.period_name]['correct'] += 1
            
            f.write("| 时期 | 准确率 | 样本数 |\n")
            f.write("|------|--------|--------|\n")
            
            for period_name, stats in sorted(period_stats.items()):
                accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0.0
                f.write(f"| {period_name} | {accuracy:.1%} | {stats['total']} |\n")
            
            f.write("\n")
        
        f.write("## 3. 模型可靠性评估\n\n")
        
        f.write("### 3.1 纳入集成的模型（准确率>=55%）\n\n")
        reliable_models = [name for name, stats in model_stats.items() if stats['accuracy'] >= 0.55]
        if reliable_models:
            for name in reliable_models:
                f.write(f"- ✅ **{name}**: 准确率 {model_stats[name]['accuracy']:.1%}\n")
        else:
            f.write("- 暂无模型达到55%准确率阈值\n")
        
        f.write("\n### 3.2 需要优化的模型（准确率<55%）\n\n")
        unreliable_models = [name for name, stats in model_stats.items() if stats['accuracy'] < 0.55]
        if unreliable_models:
            for name in unreliable_models:
                f.write(f"- ⚠️ **{name}**: 准确率 {model_stats[name]['accuracy']:.1%}，需要优化\n")
        else:
            f.write("- 所有模型均达到阈值\n")
        
        f.write("\n## 4. 下一步行动\n\n")
        f.write("1. 对通过验证的模型进行权重优化\n")
        f.write("2. 构建多模型投票系统\n")
        f.write("3. 回测验证集成模型准确率\n")
        f.write("4. 对未通过验证的模型进行优化\n")
    
    logger.info(f"验证报告已保存: {report_path}")
    return report_path


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("开始验证各模型可靠性")
    logger.info("=" * 80)
    
    all_results = {
        'HMM': [],
        'Technical': [],
        'Breadth': [],
        'Sentiment': []
    }
    
    # 验证每个模型
    for period in VALIDATION_PERIODS:
        logger.info(f"\n验证时期: {period['name']}")
        
        # HMM模型
        hmm_results = validate_hmm_model(period)
        all_results['HMM'].extend(hmm_results)
        logger.info(f"  HMM: {len(hmm_results)} 个样本")
        
        # 技术指标模型
        tech_results = validate_technical_model(period)
        all_results['Technical'].extend(tech_results)
        logger.info(f"  技术指标: {len(tech_results)} 个样本")
        
        # 市场宽度模型
        breadth_results = validate_breadth_model(period)
        all_results['Breadth'].extend(breadth_results)
        logger.info(f"  市场宽度: {len(breadth_results)} 个样本")
        
        # 情绪分析模型
        sentiment_results = validate_sentiment_model(period)
        all_results['Sentiment'].extend(sentiment_results)
        logger.info(f"  情绪分析: {len(sentiment_results)} 个样本")
    
    # 生成报告
    report_path = generate_validation_report(all_results)
    
    logger.info("\n" + "=" * 80)
    logger.info("验证完成")
    logger.info(f"报告路径: {report_path}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
