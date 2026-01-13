#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略测试集最终评估脚本

Phase 3: 最优策略确定
- 使用最优参数在测试集上进行最终回测
- 生成评估报告
- 对比训练集/验证集/测试集结果
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
import logging
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_best_params(params_file: Optional[Path] = None) -> Dict:
    """
    加载最优参数
    
    Args:
        params_file: 参数文件路径（如果为None，则从output目录查找最新的）
    
    Returns:
        Dict: 参数字典
    """
    if params_file is None:
        # 查找最新的参数文件
        params_dir = PROJECT_ROOT / 'output' / 'chase_rise_optimization'
        if not params_dir.exists():
            logger.warning("未找到参数目录，使用默认参数")
            return {}
        
        param_files = list(params_dir.glob('best_params_*.json'))
        if not param_files:
            logger.warning("未找到参数文件，使用默认参数")
            return {}
        
        params_file = max(param_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(params_file, 'r', encoding='utf-8') as f:
            params = json.load(f)
        logger.info(f"✅ 已加载参数文件: {params_file}")
        return params
    except Exception as e:
        logger.error(f"❌ 加载参数文件失败: {e}")
        return {}


def evaluate_strategy(
    jq_client,
    params: Dict,
    test_period: Tuple[str, str],
    universe: Optional[List[str]] = None,
    max_stocks: int = 300,
) -> Dict:
    """
    评估策略
    
    Args:
        jq_client: JQData客户端
        params: 策略参数
        test_period: 测试时间段
        universe: 股票池
        max_stocks: 最大股票数
    
    Returns:
        Dict: 评估结果
    """
    # 导入回测函数
    import importlib.util
    iterate_module_path = PROJECT_ROOT / 'scripts' / 'iterate_chase_rise_strategy.py'
    spec = importlib.util.spec_from_file_location("iterate_chase_rise_strategy", iterate_module_path)
    iterate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(iterate_module)
    
    from scripts.iterate_chase_rise_strategy import StrategyParams, run_backtest, calculate_composite_score
    
    # 创建参数对象
    strategy_params = StrategyParams(**params)
    
    # 运行回测
    result = run_backtest(
        jq_client,
        strategy_params,
        test_period[0],
        test_period[1],
        universe=universe,
        max_stocks=max_stocks,
    )
    
    # 计算综合评分
    score = calculate_composite_score(result)
    
    return {
        'total_return': result.total_return,
        'weekly_return': result.weekly_return,
        'sharpe_ratio': result.sharpe_ratio,
        'max_drawdown': result.max_drawdown,
        'win_rate': result.win_rate,
        'total_trades': result.total_trades,
        'total_signals': result.total_signals,
        'composite_score': score,
    }


def compare_results(
    train_result: Dict,
    validate_result: Dict,
    test_result: Dict,
) -> Dict:
    """
    对比训练集/验证集/测试集结果
    
    Returns:
        Dict: 对比结果
    """
    comparison = {
        'train': train_result,
        'validate': validate_result,
        'test': test_result,
        'analysis': {},
    }
    
    # 过拟合分析
    train_sharpe = train_result.get('sharpe_ratio', 0)
    validate_sharpe = validate_result.get('sharpe_ratio', 0)
    test_sharpe = test_result.get('sharpe_ratio', 0)
    
    if validate_sharpe > 0:
        overfit_ratio = train_sharpe / validate_sharpe
        comparison['analysis']['overfit_ratio_train_validate'] = overfit_ratio
        comparison['analysis']['is_overfitting'] = overfit_ratio > 1.5
    
    if test_sharpe > 0:
        overfit_ratio_test = validate_sharpe / test_sharpe
        comparison['analysis']['overfit_ratio_validate_test'] = overfit_ratio_test
    
    # 稳定性分析
    train_return = train_result.get('weekly_return', 0)
    validate_return = validate_result.get('weekly_return', 0)
    test_return = test_result.get('weekly_return', 0)
    
    returns_std = np.std([train_return, validate_return, test_return])
    comparison['analysis']['returns_std'] = returns_std
    comparison['analysis']['is_stable'] = returns_std < 5.0  # 标准差小于5%认为稳定
    
    return comparison


def generate_report(comparison: Dict, output_dir: Path, timestamp: str) -> str:
    """
    生成评估报告
    
    Args:
        comparison: 对比结果
        output_dir: 输出目录
        timestamp: 时间戳
    
    Returns:
        str: 报告文件路径
    """
    report_path = output_dir / f'evaluation_report_{timestamp}.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 追涨策略测试集最终评估报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # 数据集划分
        f.write("## 数据集划分\n\n")
        f.write("- **训练集**: 2019-01-01~2020-06-30 + 2024-09-01~2025-06-30\n")
        f.write("- **验证集**: 2020-07-01~2021-03-31\n")
        f.write("- **测试集**: 2025-07-01~2026-01-10\n\n")
        f.write("---\n\n")
        
        # 结果对比
        f.write("## 结果对比\n\n")
        f.write("| 指标 | 训练集 | 验证集 | 测试集 |\n")
        f.write("|------|--------|--------|--------|\n")
        
        metrics = ['weekly_return', 'sharpe_ratio', 'max_drawdown', 'win_rate', 'total_trades']
        for metric in metrics:
            train_val = comparison['train'].get(metric, 0)
            validate_val = comparison['validate'].get(metric, 0)
            test_val = comparison['test'].get(metric, 0)
            
            if isinstance(train_val, float):
                f.write(f"| {metric} | {train_val:.2f} | {validate_val:.2f} | {test_val:.2f} |\n")
            else:
                f.write(f"| {metric} | {train_val} | {validate_val} | {test_val} |\n")
        
        f.write("\n---\n\n")
        
        # 分析
        f.write("## 分析\n\n")
        analysis = comparison.get('analysis', {})
        
        if 'overfit_ratio_train_validate' in analysis:
            f.write(f"### 过拟合分析\n\n")
            f.write(f"- 训练集/验证集夏普比率比: {analysis['overfit_ratio_train_validate']:.2f}\n")
            f.write(f"- 是否过拟合: {'是' if analysis.get('is_overfitting', False) else '否'}\n\n")
        
        if 'returns_std' in analysis:
            f.write(f"### 稳定性分析\n\n")
            f.write(f"- 收益率标准差: {analysis['returns_std']:.2f}%\n")
            f.write(f"- 策略稳定性: {'稳定' if analysis.get('is_stable', False) else '不稳定'}\n\n")
        
        f.write("---\n\n")
        
        # 结论
        f.write("## 结论\n\n")
        if analysis.get('is_overfitting', False):
            f.write("⚠️ **策略存在过拟合风险**，建议调整参数或增加正则化。\n\n")
        elif analysis.get('is_stable', False):
            f.write("✅ **策略表现稳定**，可以在测试集上进一步验证。\n\n")
        else:
            f.write("⚠️ **策略稳定性需要进一步观察**。\n\n")
    
    logger.info(f"✅ 评估报告已保存: {report_path}")
    return str(report_path)


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("追涨策略测试集最终评估")
    logger.info("=" * 70)
    
    # 初始化JQData
    try:
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        logger.info("✅ JQData连接成功")
    except Exception as e:
        logger.error(f"❌ JQData连接失败: {e}")
        return
    
    # 加载最优参数
    best_params = load_best_params()
    if not best_params:
        logger.warning("使用默认参数")
        best_params = {
            'limit_up_threshold': 0.095,
            'vol_ratio_threshold_first': 3.0,
            'mom_5d_threshold_breakout': 15.0,
            'mom_5d_threshold_volume': 10.0,
            'max_positions': 2,
            'stop_loss_pct': -10.0,
            'take_profit_pct': 25.0,
            'rebalance_days': 5,
        }
    
    # 数据集划分
    train_periods = [
        ('2019-01-01', '2020-06-30'),
        ('2024-09-01', '2025-06-30'),
    ]
    validate_period = ('2020-07-01', '2021-03-31')
    test_period = ('2025-07-01', '2026-01-10')
    
    # 获取股票池
    try:
        securities = jq.get_all_securities(types=['stock'], date=test_period[1])
        stocks = securities.index.tolist()
        universe = [
            code for code in stocks[:200]
            if 'ST' not in str(securities.loc[code, 'display_name']).upper()
        ]
        logger.info(f"股票池: {len(universe)}只")
    except Exception as e:
        logger.error(f"获取股票池失败: {e}")
        return
    
    # 评估各个数据集
    logger.info("\n评估训练集...")
    train_results = []
    for train_start, train_end in train_periods:
        result = evaluate_strategy(jq, best_params, (train_start, train_end), universe=universe)
        train_results.append(result)
    
    # 平均训练结果
    avg_train_result = {
        key: np.mean([r.get(key, 0) for r in train_results])
        for key in train_results[0].keys()
    }
    
    logger.info("评估验证集...")
    validate_result = evaluate_strategy(jq, best_params, validate_period, universe=universe)
    
    logger.info("评估测试集...")
    test_result = evaluate_strategy(jq, best_params, test_period, universe=universe)
    
    # 对比结果
    comparison = compare_results(avg_train_result, validate_result, test_result)
    
    # 打印结果
    logger.info("\n" + "=" * 70)
    logger.info("评估结果")
    logger.info("=" * 70)
    
    print("\n📊 结果对比:")
    print("-" * 70)
    print(f"{'指标':<20} {'训练集':<15} {'验证集':<15} {'测试集':<15}")
    print("-" * 70)
    
    metrics = ['weekly_return', 'sharpe_ratio', 'max_drawdown', 'win_rate']
    for metric in metrics:
        train_val = avg_train_result.get(metric, 0)
        validate_val = validate_result.get(metric, 0)
        test_val = test_result.get(metric, 0)
        print(f"{metric:<20} {train_val:>14.2f} {validate_val:>14.2f} {test_val:>14.2f}")
    
    # 保存结果
    output_dir = PROJECT_ROOT / 'output' / 'chase_rise_evaluation'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存JSON结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = output_dir / f'evaluation_results_{timestamp}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"\n✅ 评估结果已保存: {json_path}")
    
    # 生成报告
    report_path = generate_report(comparison, output_dir, timestamp)
    
    logger.info("\n" + "=" * 70)
    logger.info("评估完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
