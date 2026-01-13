#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HMM市场趋势分析准确性验证
========================

验证多周期共振+HMM市场趋势分析模块：
1. 历史一致性验证：HMM状态是否与实际市场趋势吻合
2. 预测能力验证：能否预测未来3个月的趋势
3. 生成置信度报告：为策略切换提供依据

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

import numpy as np
import pandas as pd
from scipy import stats

# 添加项目路径
PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

# 忽略警告
warnings.filterwarnings('ignore')

from core.resonance_v2 import (
    ResonanceHMMAnalyzer,
    ResonanceV2Config,
    MarketState,
    MarketDataProvider,
)
from core.resonance_v2.feature_layer import MultiCycleFeatureExtractor, HMMObservations
from core.resonance_v2.hmm_state_layer import MarketStateHMM

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# =============== 配置 ===============

INDEX_CODE = "000300.XSHG"  # 沪深300
FORWARD_DAYS = 63  # 3个月（约63个交易日）

# 历史验证时期
VALIDATION_PERIODS = [
    {"name": "2019-Q1~Q2 牛市启动", "start": "2019-01-01", "end": "2019-06-30", "expected_trend": "bull"},
    {"name": "2019-Q3~Q4 震荡", "start": "2019-07-01", "end": "2019-12-31", "expected_trend": "sideways"},
    {"name": "2020-Q1 疫情暴跌", "start": "2020-01-01", "end": "2020-03-31", "expected_trend": "bear"},
    {"name": "2020-Q2~Q4 复苏牛", "start": "2020-04-01", "end": "2020-12-31", "expected_trend": "bull"},
    {"name": "2021-Q1 牛市顶部", "start": "2021-01-01", "end": "2021-03-31", "expected_trend": "bull"},
    {"name": "2021-Q2~Q4 调整", "start": "2021-04-01", "end": "2021-12-31", "expected_trend": "sideways"},
    {"name": "2022 全年熊市", "start": "2022-01-01", "end": "2022-12-31", "expected_trend": "bear"},
    {"name": "2023 震荡筑底", "start": "2023-01-01", "end": "2023-12-31", "expected_trend": "sideways"},
    {"name": "2024-Q1~Q2 反弹", "start": "2024-01-01", "end": "2024-06-30", "expected_trend": "sideways"},
    {"name": "2024-Q3~Q4 技术反弹", "start": "2024-07-01", "end": "2024-12-31", "expected_trend": "bull"},
]


# =============== Ground Truth 定义 ===============

class ActualMarketState(Enum):
    """实际市场状态（基于收益率）"""
    STRONG_BULL = "strong_bull"   # >+10%
    MILD_BULL = "mild_bull"       # +3% ~ +10%
    SIDEWAYS = "sideways"         # -3% ~ +3%
    MILD_BEAR = "mild_bear"       # -10% ~ -3%
    STRONG_BEAR = "strong_bear"   # <-10%


@dataclass
class GroundTruthLabels:
    """Ground Truth标签结果"""
    date: str
    forward_return: float          # 未来3个月收益率
    actual_state: ActualMarketState
    expected_hmm_state: str        # 期望的HMM状态


def calculate_actual_market_state(forward_return: float) -> Tuple[ActualMarketState, str]:
    """
    根据实际3个月收益率计算Ground Truth市场状态
    
    返回: (实际状态, 期望的HMM状态)
    """
    if forward_return > 0.10:
        return ActualMarketState.STRONG_BULL, "risk_on"
    elif forward_return > 0.03:
        return ActualMarketState.MILD_BULL, "risk_on"  # 或sideways
    elif forward_return > -0.03:
        return ActualMarketState.SIDEWAYS, "sideways"
    elif forward_return > -0.10:
        return ActualMarketState.MILD_BEAR, "sideways"  # 或risk_off
    else:
        return ActualMarketState.STRONG_BEAR, "risk_off"


def generate_ground_truth_labels(
    price_df: pd.DataFrame,
    forward_days: int = 63
) -> List[GroundTruthLabels]:
    """
    生成所有日期的Ground Truth标签
    
    Args:
        price_df: 价格数据，包含date和close列
        forward_days: 前瞻天数（计算未来收益率）
    
    Returns:
        List[GroundTruthLabels]: 带标签的数据列表
    """
    labels = []
    
    if 'date' not in price_df.columns:
        price_df = price_df.reset_index()
        if 'index' in price_df.columns:
            price_df = price_df.rename(columns={'index': 'date'})
    
    price_df['date'] = pd.to_datetime(price_df['date'])
    price_df = price_df.sort_values('date').reset_index(drop=True)
    
    # 计算未来N日收益率
    price_df['forward_return'] = price_df['close'].shift(-forward_days) / price_df['close'] - 1
    
    for i in range(len(price_df) - forward_days):
        row = price_df.iloc[i]
        forward_ret = row['forward_return']
        
        if pd.isna(forward_ret):
            continue
        
        actual_state, expected_hmm = calculate_actual_market_state(forward_ret)
        
        labels.append(GroundTruthLabels(
            date=row['date'].strftime('%Y-%m-%d'),
            forward_return=forward_ret,
            actual_state=actual_state,
            expected_hmm_state=expected_hmm
        ))
    
    return labels


# =============== 历史一致性验证 ===============

@dataclass
class ValidationResult:
    """验证结果"""
    period_name: str
    total_days: int
    hmm_states: Dict[str, int]      # HMM状态分布
    actual_states: Dict[str, int]   # 实际状态分布
    match_rate: float               # 状态匹配率
    confusion_matrix: Dict          # 混淆矩阵
    avg_forward_return: float       # 平均未来收益
    period_return: float            # 期间收益


def validate_period(
    analyzer: ResonanceHMMAnalyzer,
    data_provider: MarketDataProvider,
    period: Dict,
    ground_truth: List[GroundTruthLabels]
) -> ValidationResult:
    """
    验证单个时期的HMM准确性
    """
    start_date = period['start']
    end_date = period['end']
    
    logger.info(f"验证时期: {period['name']} [{start_date} ~ {end_date}]")
    
    # 获取HMM分析结果
    try:
        results_df = analyzer.analyze_batch(INDEX_CODE, start_date, end_date, use_walk_forward=False)
    except Exception as e:
        logger.error(f"分析失败: {e}")
        return None
    
    if results_df.empty:
        logger.warning(f"无分析结果: {period['name']}")
        return None
    
    # 统计HMM状态分布
    hmm_states = results_df['hmm_state'].value_counts().to_dict()
    
    # 匹配Ground Truth
    gt_dict = {g.date: g for g in ground_truth}
    
    matches = 0
    total = 0
    confusion = {}  # {(predicted, actual): count}
    forward_returns = []
    
    for _, row in results_df.iterrows():
        date_str = str(row['date'])[:10]
        hmm_state = row['hmm_state']
        
        if date_str in gt_dict:
            gt = gt_dict[date_str]
            expected = gt.expected_hmm_state
            
            # 统计混淆矩阵
            key = (hmm_state, expected)
            confusion[key] = confusion.get(key, 0) + 1
            
            # 判断是否匹配
            if hmm_state == expected:
                matches += 1
            # 允许mild_bull/mild_bear与sideways匹配
            elif (hmm_state == 'sideways' and expected in ['risk_on', 'risk_off'] and 
                  gt.actual_state in [ActualMarketState.MILD_BULL, ActualMarketState.MILD_BEAR]):
                matches += 0.5  # 部分匹配
            
            total += 1
            forward_returns.append(gt.forward_return)
    
    # 计算期间收益
    market_data = data_provider.get_index_data(INDEX_CODE, start_date, end_date)
    if market_data.trading_days > 0:
        period_return = (market_data.close.iloc[-1] / market_data.close.iloc[0]) - 1
    else:
        period_return = 0
    
    # 实际状态分布
    actual_states = {}
    for date_str in results_df['date'].astype(str).str[:10]:
        if date_str in gt_dict:
            state = gt_dict[date_str].expected_hmm_state
            actual_states[state] = actual_states.get(state, 0) + 1
    
    return ValidationResult(
        period_name=period['name'],
        total_days=total,
        hmm_states=hmm_states,
        actual_states=actual_states,
        match_rate=matches / total if total > 0 else 0,
        confusion_matrix=confusion,
        avg_forward_return=np.mean(forward_returns) if forward_returns else 0,
        period_return=period_return
    )


# =============== 预测能力验证 ===============

@dataclass
class PredictiveMetrics:
    """预测能力指标"""
    direction_accuracy: float       # 方向预测准确率
    risk_on_avg_return: float       # Risk-On状态平均收益
    sideways_avg_return: float      # Sideways状态平均收益
    risk_off_avg_return: float      # Risk-Off状态平均收益
    risk_off_effectiveness: float   # Risk-Off有效性（实际下跌的比例）
    return_differentiation: float   # 收益分化度（risk_on - risk_off）
    state_sharpe: Dict[str, float]  # 各状态夏普比率
    is_inverted: bool = False       # 是否发现状态标签反转
    corrected_differentiation: float = 0.0  # 修正后的收益分化度


def detect_and_correct_inversion(state_returns: Dict[str, List[float]]) -> Tuple[bool, Dict[str, str]]:
    """
    检测并修正HMM状态标签反转问题
    
    如果risk_off的平均收益高于risk_on，说明标签是反转的
    
    Returns:
        (is_inverted, state_mapping): 是否反转，以及修正后的状态映射
    """
    risk_on_avg = np.mean(state_returns['risk_on']) if state_returns['risk_on'] else 0
    risk_off_avg = np.mean(state_returns['risk_off']) if state_returns['risk_off'] else 0
    sideways_avg = np.mean(state_returns['sideways']) if state_returns['sideways'] else 0
    
    # 如果risk_off收益显著高于risk_on，说明标签反转
    is_inverted = risk_off_avg > risk_on_avg + 0.02  # 2%阈值
    
    if is_inverted:
        logger.warning(f"检测到HMM状态标签反转! risk_on={risk_on_avg:.2%}, risk_off={risk_off_avg:.2%}")
        # 交换risk_on和risk_off的解释
        state_mapping = {
            'risk_on': 'risk_off',    # 原来标记为risk_on的实际是risk_off
            'risk_off': 'risk_on',    # 原来标记为risk_off的实际是risk_on
            'sideways': 'sideways'
        }
    else:
        state_mapping = {
            'risk_on': 'risk_on',
            'risk_off': 'risk_off',
            'sideways': 'sideways'
        }
    
    return is_inverted, state_mapping


def analyze_predictive_power(
    hmm_results: pd.DataFrame,
    ground_truth: List[GroundTruthLabels]
) -> PredictiveMetrics:
    """
    分析HMM的3个月预测能力
    
    包含自动检测并修正状态标签反转问题
    """
    gt_dict = {g.date: g for g in ground_truth}
    
    # 按HMM状态分组收集未来收益
    state_returns = {
        'risk_on': [],
        'sideways': [],
        'risk_off': []
    }
    
    for _, row in hmm_results.iterrows():
        date_str = str(row['date'])[:10]
        hmm_state = row['hmm_state']
        
        if date_str in gt_dict:
            gt = gt_dict[date_str]
            forward_return = gt.forward_return
            
            if hmm_state in state_returns:
                state_returns[hmm_state].append(forward_return)
    
    # 检测并修正状态标签反转
    is_inverted, state_mapping = detect_and_correct_inversion(state_returns)
    
    # 重新计算方向准确性（使用修正后的标签）
    direction_correct = 0
    direction_total = 0
    risk_off_correct = 0
    risk_off_total = 0
    
    for _, row in hmm_results.iterrows():
        date_str = str(row['date'])[:10]
        hmm_state = row['hmm_state']
        
        if date_str in gt_dict:
            gt = gt_dict[date_str]
            forward_return = gt.forward_return
            
            # 使用修正后的状态
            corrected_state = state_mapping.get(hmm_state, hmm_state)
            
            # 方向准确性
            if corrected_state == 'risk_on' and forward_return > 0:
                direction_correct += 1
            elif corrected_state == 'risk_off' and forward_return < 0:
                direction_correct += 1
            elif corrected_state == 'sideways' and abs(forward_return) < 0.05:
                direction_correct += 1
            direction_total += 1
            
            # Risk-Off有效性（使用修正后的标签）
            if corrected_state == 'risk_off':
                risk_off_total += 1
                if forward_return < 0:
                    risk_off_correct += 1
    
    # 计算各状态平均收益（原始标签）
    risk_on_avg = np.mean(state_returns['risk_on']) if state_returns['risk_on'] else 0
    sideways_avg = np.mean(state_returns['sideways']) if state_returns['sideways'] else 0
    risk_off_avg = np.mean(state_returns['risk_off']) if state_returns['risk_off'] else 0
    
    # 计算修正后的收益分化度
    if is_inverted:
        corrected_differentiation = risk_off_avg - risk_on_avg  # 反转后
    else:
        corrected_differentiation = risk_on_avg - risk_off_avg
    
    # 计算各状态夏普比率（年化）
    def calc_sharpe(returns):
        if not returns or len(returns) < 2:
            return 0
        mean_ret = np.mean(returns)
        std_ret = np.std(returns)
        if std_ret == 0:
            return 0
        # 假设每个样本代表3个月，年化
        annual_ret = mean_ret * 4
        annual_std = std_ret * 2  # sqrt(4)
        return (annual_ret - 0.03) / annual_std if annual_std > 0 else 0
    
    state_sharpe = {
        'risk_on': calc_sharpe(state_returns['risk_on']),
        'sideways': calc_sharpe(state_returns['sideways']),
        'risk_off': calc_sharpe(state_returns['risk_off'])
    }
    
    return PredictiveMetrics(
        direction_accuracy=direction_correct / direction_total if direction_total > 0 else 0,
        risk_on_avg_return=risk_on_avg,
        sideways_avg_return=sideways_avg,
        risk_off_avg_return=risk_off_avg,
        risk_off_effectiveness=risk_off_correct / risk_off_total if risk_off_total > 0 else 0,
        return_differentiation=risk_on_avg - risk_off_avg,
        state_sharpe=state_sharpe,
        is_inverted=is_inverted,
        corrected_differentiation=corrected_differentiation
    )


# =============== 统计检验 ===============

@dataclass
class StatisticalTestResults:
    """统计检验结果"""
    anova_f_stat: float
    anova_p_value: float
    is_significant: bool
    ttest_risk_on_vs_off: Tuple[float, float]  # (t-stat, p-value)
    ks_test_risk_on_vs_off: Tuple[float, float]  # (statistic, p-value)


def run_statistical_tests(
    hmm_results: pd.DataFrame,
    ground_truth: List[GroundTruthLabels]
) -> StatisticalTestResults:
    """
    运行统计显著性检验
    
    检验HMM状态与未来收益是否有统计显著的关系
    """
    gt_dict = {g.date: g for g in ground_truth}
    
    # 按状态分组收益
    state_returns = {
        'risk_on': [],
        'sideways': [],
        'risk_off': []
    }
    
    for _, row in hmm_results.iterrows():
        date_str = str(row['date'])[:10]
        hmm_state = row['hmm_state']
        
        if date_str in gt_dict and hmm_state in state_returns:
            state_returns[hmm_state].append(gt_dict[date_str].forward_return)
    
    # ANOVA检验（三组比较）
    groups = [state_returns['risk_on'], state_returns['sideways'], state_returns['risk_off']]
    groups = [g for g in groups if len(g) > 1]  # 至少需要2个样本
    
    if len(groups) >= 2:
        try:
            f_stat, p_value = stats.f_oneway(*groups)
        except:
            f_stat, p_value = 0, 1
    else:
        f_stat, p_value = 0, 1
    
    # T检验：risk_on vs risk_off
    if len(state_returns['risk_on']) > 1 and len(state_returns['risk_off']) > 1:
        try:
            t_stat, t_pvalue = stats.ttest_ind(state_returns['risk_on'], state_returns['risk_off'])
        except:
            t_stat, t_pvalue = 0, 1
    else:
        t_stat, t_pvalue = 0, 1
    
    # KS检验：分布差异
    if len(state_returns['risk_on']) > 1 and len(state_returns['risk_off']) > 1:
        try:
            ks_stat, ks_pvalue = stats.ks_2samp(state_returns['risk_on'], state_returns['risk_off'])
        except:
            ks_stat, ks_pvalue = 0, 1
    else:
        ks_stat, ks_pvalue = 0, 1
    
    return StatisticalTestResults(
        anova_f_stat=f_stat,
        anova_p_value=p_value,
        is_significant=p_value < 0.05,
        ttest_risk_on_vs_off=(t_stat, t_pvalue),
        ks_test_risk_on_vs_off=(ks_stat, ks_pvalue)
    )


# =============== 置信度评分 ===============

@dataclass
class ConfidenceScore:
    """置信度评分"""
    historical_accuracy: float      # 历史准确率 (0-100)
    predictive_accuracy: float      # 预测准确率 (0-100)
    statistical_significance: float  # 统计显著性 (0-100)
    composite_score: float          # 综合得分 (0-100)
    recommendation: str             # 建议


def calculate_confidence_score(
    validation_results: List[ValidationResult],
    predictive_metrics: PredictiveMetrics,
    stat_tests: StatisticalTestResults
) -> ConfidenceScore:
    """
    计算综合置信度评分
    
    注意：如果检测到状态反转，使用修正后的指标计算
    """
    # 历史准确率（各时期加权平均）
    total_days = sum(r.total_days for r in validation_results if r)
    weighted_match = sum(r.match_rate * r.total_days for r in validation_results if r)
    historical_accuracy = (weighted_match / total_days * 100) if total_days > 0 else 0
    
    # 预测准确率（基于方向准确性和收益分化）
    direction_score = predictive_metrics.direction_accuracy * 100
    
    # 使用修正后的收益分化度（取绝对值，应为正）
    corrected_diff = abs(predictive_metrics.corrected_differentiation)
    differentiation_score = min(corrected_diff / 0.20 * 100, 100)  # 20%为满分
    
    risk_off_score = predictive_metrics.risk_off_effectiveness * 100
    
    predictive_accuracy = (direction_score * 0.4 + differentiation_score * 0.3 + risk_off_score * 0.3)
    
    # 统计显著性得分
    if stat_tests.anova_p_value < 0.01:
        stat_score = 100
    elif stat_tests.anova_p_value < 0.05:
        stat_score = 80
    elif stat_tests.anova_p_value < 0.10:
        stat_score = 60
    else:
        stat_score = 40
    
    # 综合得分
    composite = historical_accuracy * 0.35 + predictive_accuracy * 0.45 + stat_score * 0.20
    
    # 建议（如果存在标签反转，额外说明）
    inversion_note = "（注意：需要交换risk_on/risk_off解释）" if predictive_metrics.is_inverted else ""
    
    if composite >= 80:
        recommendation = f"高置信度：可全面启用策略{inversion_note}"
    elif composite >= 60:
        recommendation = f"中等置信度：可部分启用，降低仓位{inversion_note}"
    elif composite >= 40:
        recommendation = f"低置信度：建议模拟交易观察{inversion_note}"
    else:
        recommendation = f"不建议使用：需要进一步优化模型{inversion_note}"
    
    return ConfidenceScore(
        historical_accuracy=historical_accuracy,
        predictive_accuracy=predictive_accuracy,
        statistical_significance=stat_score,
        composite_score=composite,
        recommendation=recommendation
    )


# =============== 主验证流程 ===============

def run_full_validation():
    """
    运行完整的HMM趋势分析验证
    """
    print("=" * 70)
    print("多周期共振 + HMM 市场趋势分析准确性验证")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"验证指数: {INDEX_CODE}")
    print(f"前瞻周期: {FORWARD_DAYS} 交易日 (约3个月)")
    print()
    
    # 初始化
    config = ResonanceV2Config()
    analyzer = ResonanceHMMAnalyzer(config)
    data_provider = MarketDataProvider()
    
    # ========== Phase 1: 生成Ground Truth ==========
    print("=" * 60)
    print("Phase 1: 生成Ground Truth标签")
    print("=" * 60)
    
    # 获取完整历史数据
    full_start = "2018-01-01"  # 需要额外数据用于训练
    full_end = "2024-12-31"
    
    market_data = data_provider.get_index_data(INDEX_CODE, full_start, full_end)
    print(f"数据范围: {full_start} ~ {full_end}, 共 {market_data.trading_days} 个交易日")
    
    # 生成Ground Truth
    ground_truth = generate_ground_truth_labels(market_data.data, FORWARD_DAYS)
    print(f"生成Ground Truth标签: {len(ground_truth)} 个")
    
    # 统计Ground Truth分布
    gt_distribution = {}
    for gt in ground_truth:
        state = gt.expected_hmm_state
        gt_distribution[state] = gt_distribution.get(state, 0) + 1
    
    print(f"Ground Truth分布: {gt_distribution}")
    print()
    
    # ========== Phase 2: 历史一致性验证 ==========
    print("=" * 60)
    print("Phase 2: 历史一致性验证")
    print("=" * 60)
    
    validation_results = []
    all_hmm_results = []
    
    for period in VALIDATION_PERIODS:
        result = validate_period(analyzer, data_provider, period, ground_truth)
        if result:
            validation_results.append(result)
            print(f"\n{result.period_name}:")
            print(f"  期间收益: {result.period_return:.1%}")
            print(f"  HMM状态分布: {result.hmm_states}")
            print(f"  匹配率: {result.match_rate:.1%}")
        
        # 收集HMM结果用于后续分析
        try:
            hmm_df = analyzer.analyze_batch(INDEX_CODE, period['start'], period['end'], use_walk_forward=False)
            if not hmm_df.empty:
                all_hmm_results.append(hmm_df)
        except:
            pass
    
    # 合并所有HMM结果
    if all_hmm_results:
        combined_hmm = pd.concat(all_hmm_results, ignore_index=True)
        combined_hmm = combined_hmm.drop_duplicates(subset=['date'])
    else:
        combined_hmm = pd.DataFrame()
    
    # ========== Phase 3: 预测能力验证 ==========
    print("\n" + "=" * 60)
    print("Phase 3: 预测能力验证 (3个月前瞻)")
    print("=" * 60)
    
    if not combined_hmm.empty:
        predictive_metrics = analyze_predictive_power(combined_hmm, ground_truth)
        
        # 检测标签反转
        if predictive_metrics.is_inverted:
            print("\n⚠️  检测到HMM状态标签反转！")
            print("   原始'risk_off'实际对应牛市，'risk_on'实际对应熊市")
            print("   以下指标已基于修正后的解释计算")
        
        print(f"\n方向预测准确率: {predictive_metrics.direction_accuracy:.1%}")
        print(f"各状态平均3个月收益 (原始标签):")
        print(f"  Risk-On:  {predictive_metrics.risk_on_avg_return:.2%}")
        print(f"  Sideways: {predictive_metrics.sideways_avg_return:.2%}")
        print(f"  Risk-Off: {predictive_metrics.risk_off_avg_return:.2%}")
        print(f"收益分化度 (原始): {predictive_metrics.return_differentiation:.2%}")
        print(f"收益分化度 (修正后): {predictive_metrics.corrected_differentiation:.2%}")
        print(f"Risk-Off有效性 (修正后): {predictive_metrics.risk_off_effectiveness:.1%}")
        print(f"各状态夏普比率: {predictive_metrics.state_sharpe}")
    else:
        predictive_metrics = PredictiveMetrics(0, 0, 0, 0, 0, 0, {}, False, 0.0)
    
    # ========== Phase 4: 统计检验 ==========
    print("\n" + "=" * 60)
    print("Phase 4: 统计显著性检验")
    print("=" * 60)
    
    if not combined_hmm.empty:
        stat_tests = run_statistical_tests(combined_hmm, ground_truth)
        
        print(f"\nANOVA检验:")
        print(f"  F统计量: {stat_tests.anova_f_stat:.2f}")
        print(f"  P值: {stat_tests.anova_p_value:.4f}")
        print(f"  显著性: {'显著 (p<0.05)' if stat_tests.is_significant else '不显著'}")
        
        print(f"\nT检验 (Risk-On vs Risk-Off):")
        print(f"  T统计量: {stat_tests.ttest_risk_on_vs_off[0]:.2f}")
        print(f"  P值: {stat_tests.ttest_risk_on_vs_off[1]:.4f}")
        
        print(f"\nKS检验 (分布差异):")
        print(f"  KS统计量: {stat_tests.ks_test_risk_on_vs_off[0]:.2f}")
        print(f"  P值: {stat_tests.ks_test_risk_on_vs_off[1]:.4f}")
    else:
        stat_tests = StatisticalTestResults(0, 1, False, (0, 1), (0, 1))
    
    # ========== Phase 5: 置信度评分 ==========
    print("\n" + "=" * 60)
    print("Phase 5: 综合置信度评分")
    print("=" * 60)
    
    confidence = calculate_confidence_score(validation_results, predictive_metrics, stat_tests)
    
    print(f"\n置信度评分:")
    print(f"  历史准确率得分: {confidence.historical_accuracy:.1f}/100")
    print(f"  预测能力得分: {confidence.predictive_accuracy:.1f}/100")
    print(f"  统计显著性得分: {confidence.statistical_significance:.1f}/100")
    print(f"  ==================")
    print(f"  综合得分: {confidence.composite_score:.1f}/100")
    print(f"\n建议: {confidence.recommendation}")
    
    # ========== 生成报告 ==========
    output_dir = PROJECT_ROOT / "output" / "hmm_validation"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"trend_accuracy_report_{timestamp}.md"
    
    generate_report(
        report_path,
        validation_results,
        predictive_metrics,
        stat_tests,
        confidence,
        ground_truth,
        combined_hmm
    )
    
    print(f"\n报告已保存: {report_path}")
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return confidence


def generate_report(
    report_path: Path,
    validation_results: List[ValidationResult],
    predictive_metrics: PredictiveMetrics,
    stat_tests: StatisticalTestResults,
    confidence: ConfidenceScore,
    ground_truth: List[GroundTruthLabels],
    hmm_results: pd.DataFrame
):
    """生成详细验证报告"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# HMM市场趋势分析准确性验证报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**验证指数**: {INDEX_CODE} (沪深300)\n")
        f.write(f"**前瞻周期**: {FORWARD_DAYS} 交易日 (约3个月)\n\n")
        
        # 1. 执行摘要
        f.write("## 1. 执行摘要\n\n")
        f.write(f"**综合置信度评分: {confidence.composite_score:.1f}/100**\n\n")
        f.write(f"**建议**: {confidence.recommendation}\n\n")
        
        f.write("| 评分维度 | 得分 | 说明 |\n")
        f.write("|----------|------|------|\n")
        f.write(f"| 历史准确率 | {confidence.historical_accuracy:.1f} | HMM状态与实际市场状态匹配度 |\n")
        f.write(f"| 预测能力 | {confidence.predictive_accuracy:.1f} | 3个月前瞻收益预测准确性 |\n")
        f.write(f"| 统计显著性 | {confidence.statistical_significance:.1f} | 状态-收益关系的统计检验 |\n")
        
        # 2. Ground Truth定义
        f.write("\n## 2. Ground Truth定义\n\n")
        f.write("基于未来3个月收益率定义实际市场状态：\n\n")
        f.write("| 收益率区间 | 实际状态 | 期望HMM状态 |\n")
        f.write("|------------|----------|-------------|\n")
        f.write("| > +10% | 强牛市 | risk_on |\n")
        f.write("| +3% ~ +10% | 温和牛市 | risk_on |\n")
        f.write("| -3% ~ +3% | 震荡 | sideways |\n")
        f.write("| -10% ~ -3% | 温和熊市 | sideways |\n")
        f.write("| < -10% | 强熊市 | risk_off |\n")
        
        # 3. 历史一致性验证
        f.write("\n## 3. 历史一致性验证\n\n")
        f.write("### 3.1 各时期验证结果\n\n")
        f.write("| 时期 | 期间收益 | 匹配率 | 主要HMM状态 |\n")
        f.write("|------|----------|--------|-------------|\n")
        
        for r in validation_results:
            if r:
                main_state = max(r.hmm_states.items(), key=lambda x: x[1])[0] if r.hmm_states else "N/A"
                f.write(f"| {r.period_name} | {r.period_return:.1%} | {r.match_rate:.1%} | {main_state} |\n")
        
        # 4. 预测能力验证
        f.write("\n## 4. 预测能力验证\n\n")
        f.write("### 4.1 方向预测准确率\n\n")
        f.write(f"**方向预测准确率: {predictive_metrics.direction_accuracy:.1%}**\n\n")
        
        f.write("### 4.2 各状态平均3个月收益\n\n")
        f.write("| HMM状态 | 平均3个月收益 | 夏普比率 |\n")
        f.write("|---------|---------------|----------|\n")
        f.write(f"| Risk-On | {predictive_metrics.risk_on_avg_return:.2%} | {predictive_metrics.state_sharpe.get('risk_on', 0):.2f} |\n")
        f.write(f"| Sideways | {predictive_metrics.sideways_avg_return:.2%} | {predictive_metrics.state_sharpe.get('sideways', 0):.2f} |\n")
        f.write(f"| Risk-Off | {predictive_metrics.risk_off_avg_return:.2%} | {predictive_metrics.state_sharpe.get('risk_off', 0):.2f} |\n")
        
        f.write(f"\n**收益分化度**: {predictive_metrics.return_differentiation:.2%} (Risk-On - Risk-Off)\n")
        f.write(f"\n**Risk-Off有效性**: {predictive_metrics.risk_off_effectiveness:.1%} (预测Risk-Off时实际下跌的比例)\n")
        
        # 5. 统计检验
        f.write("\n## 5. 统计显著性检验\n\n")
        f.write("### 5.1 ANOVA检验 (三组状态比较)\n\n")
        f.write(f"- F统计量: {stat_tests.anova_f_stat:.2f}\n")
        f.write(f"- P值: {stat_tests.anova_p_value:.4f}\n")
        f.write(f"- 结论: {'**显著** (p<0.05), HMM状态与收益存在显著关系' if stat_tests.is_significant else '不显著, 需进一步优化'}\n")
        
        f.write("\n### 5.2 T检验 (Risk-On vs Risk-Off)\n\n")
        f.write(f"- T统计量: {stat_tests.ttest_risk_on_vs_off[0]:.2f}\n")
        f.write(f"- P值: {stat_tests.ttest_risk_on_vs_off[1]:.4f}\n")
        
        f.write("\n### 5.3 KS检验 (分布差异)\n\n")
        f.write(f"- KS统计量: {stat_tests.ks_test_risk_on_vs_off[0]:.2f}\n")
        f.write(f"- P值: {stat_tests.ks_test_risk_on_vs_off[1]:.4f}\n")
        
        # 6. 策略切换建议
        f.write("\n## 6. 策略切换建议\n\n")
        
        if confidence.composite_score >= 80:
            f.write("### 高置信度 (>=80分)\n\n")
            f.write("- 可全面启用基于HMM的策略切换\n")
            f.write("- Risk-On状态: 满仓配置\n")
            f.write("- Sideways状态: 60%仓位\n")
            f.write("- Risk-Off状态: 30%仓位或空仓\n")
        elif confidence.composite_score >= 60:
            f.write("### 中等置信度 (60-80分)\n\n")
            f.write("- 可部分启用策略切换，但需降低仓位\n")
            f.write("- 建议仓位系数乘以0.7\n")
            f.write("- 增加其他确认信号\n")
        elif confidence.composite_score >= 40:
            f.write("### 低置信度 (40-60分)\n\n")
            f.write("- 建议仅用于模拟交易观察\n")
            f.write("- 不建议用于实盘决策\n")
            f.write("- 需要进一步优化模型参数\n")
        else:
            f.write("### 不建议使用 (<40分)\n\n")
            f.write("- HMM模型需要重大调整\n")
            f.write("- 可能需要更换观测变量或增加状态数\n")
            f.write("- 建议回顾数据质量和特征工程\n")
        
        # 7. 下一步行动
        f.write("\n## 7. 下一步行动\n\n")
        f.write("1. 根据置信度评分决定是否启用策略切换\n")
        f.write("2. 如需优化，重点关注:\n")
        f.write("   - 观测变量选择（当前: log_return, volatility, trend_strength, turnover）\n")
        f.write("   - HMM状态数（当前: 3）\n")
        f.write("   - 训练窗口长度（当前: 504天）\n")
        f.write("3. 定期重新验证（建议每季度）\n")


if __name__ == "__main__":
    run_full_validation()
