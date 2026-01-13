#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略信号参数敏感性测试脚本

Phase 1.2: 信号参数敏感性测试
- 测试关键参数的敏感性
- 找出最优参数范围

测试参数:
- LIMIT_UP_THRESHOLD: 涨停阈值
- VOLUME_RATIO_THRESHOLD: 量比阈值
- MOM_5D_THRESHOLD: 5日动量阈值
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import logging
import json
from itertools import product

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


def test_parameter_sensitivity(
    jq_client,
    test_date_range: Tuple[str, str],
    test_stocks: List[str],
    param_grid: Dict[str, List[float]]
) -> pd.DataFrame:
    """
    测试参数敏感性
    
    Args:
        jq_client: JQData客户端
        test_date_range: 测试日期范围
        test_stocks: 测试股票列表
        param_grid: 参数网格
    
    Returns:
        pd.DataFrame: 测试结果
    """
    logger.info(f"开始参数敏感性测试: {test_date_range[0]} ~ {test_date_range[1]}")
    logger.info(f"测试股票数: {len(test_stocks)}")
    
    # 导入信号分析函数（直接导入模块）
    import importlib.util
    signal_analysis_path = PROJECT_ROOT / 'scripts' / 'analyze_chase_rise_signals.py'
    spec = importlib.util.spec_from_file_location("analyze_chase_rise_signals", signal_analysis_path)
    signal_analysis_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(signal_analysis_module)
    analyze_signals_for_period = signal_analysis_module.analyze_signals_for_period
    analyze_signal_statistics = signal_analysis_module.analyze_signal_statistics
    
    results = []
    
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    
    total_combinations = 1
    for vals in param_values:
        total_combinations *= len(vals)
    
    logger.info(f"参数组合总数: {total_combinations}")
    
    combination_idx = 0
    for param_combo in product(*param_values):
        combination_idx += 1
        params = dict(zip(param_names, param_combo))
        
        if combination_idx % 10 == 0:
            logger.info(f"  进度: {combination_idx}/{total_combinations}")
        
        try:
            # 分析信号
            df = analyze_signals_for_period(
                jq_client,
                test_date_range[0],
                test_date_range[1],
                universe=test_stocks,
                max_stocks=0,  # 使用全部测试股票
                rebalance_days=5,
                **params
            )
            
            if df.empty:
                continue
            
            # 统计结果
            stats = analyze_signal_statistics(df)
            
            if 'overall' not in stats:
                continue
            
            # 记录结果
            result = params.copy()
            result.update({
                'total_signals': stats['overall']['total_signals'],
                'avg_return': stats['overall']['avg_return'],
                'win_rate': stats['overall']['win_rate'],
                'avg_score': stats['overall']['avg_score'],
            })
            
            results.append(result)
        
        except Exception as e:
            logger.debug(f"参数组合 {params} 测试失败: {e}")
            continue
    
    if not results:
        logger.warning("未找到任何测试结果")
        return pd.DataFrame()
    
    result_df = pd.DataFrame(results)
    logger.info(f"✅ 测试完成，共 {len(result_df)} 个有效结果")
    
    return result_df


def analyze_sensitivity_results(df: pd.DataFrame) -> Dict:
    """
    分析敏感性测试结果
    
    Returns:
        Dict: 分析结果
    """
    if df.empty:
        return {}
    
    analysis = {}
    
    # 找出最优参数组合
    # 综合评分 = 平均收益 * 0.4 + 胜率 * 0.3 + 信号数归一化 * 0.3
    df['composite_score'] = (
        df['avg_return'] * 0.4 +
        df['win_rate'] * 0.3 +
        (df['total_signals'] / df['total_signals'].max()) * 100 * 0.3
    )
    
    # 找出Top 10
    top_10 = df.nlargest(10, 'composite_score')
    
    analysis['top_10'] = top_10.to_dict('records')
    
    # 参数影响分析（单变量分析）
    param_cols = [col for col in df.columns if col not in ['total_signals', 'avg_return', 'win_rate', 'avg_score', 'composite_score']]
    
    for param in param_cols:
        if param not in df.columns:
            continue
        
        # 按参数值分组统计
        grouped = df.groupby(param).agg({
            'avg_return': 'mean',
            'win_rate': 'mean',
            'total_signals': 'mean',
        }).reset_index()
        
        analysis[f'{param}_impact'] = grouped.to_dict('records')
    
    # 最优参数
    best_idx = df['composite_score'].idxmax()
    analysis['best_params'] = df.loc[best_idx].to_dict()
    
    return analysis


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("追涨策略信号参数敏感性测试")
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
    
    # 测试日期范围（使用较小的数据集以加速）
    test_date_range = ('2024-09-01', '2024-12-31')
    
    # 测试股票池（限制数量以加速）
    try:
        securities = jq.get_all_securities(types=['stock'], date=test_date_range[1])
        stocks = securities.index.tolist()
        test_stocks = [
            code for code in stocks[:200]  # 限制200只股票
            if 'ST' not in str(securities.loc[code, 'display_name']).upper()
        ]
        logger.info(f"测试股票池: {len(test_stocks)}只")
    except Exception as e:
        logger.error(f"获取测试股票池失败: {e}")
        return
    
    # 参数网格（简化版本，减少组合数以加速）
    param_grid = {
        'limit_up_threshold': [0.090, 0.095, 0.098],  # 涨停阈值
        'vol_ratio_threshold_first': [2.0, 3.0, 4.0],  # 首板放量阈值
        'mom_5d_threshold_breakout': [12.0, 15.0, 18.0],  # 强势突破动量
        'mom_5d_threshold_volume': [8.0, 10.0, 12.0],  # 量价齐升动量
        'vol_ratio_threshold_breakout': [1.2, 1.5, 2.0],  # 强势突破量比
        'vol_ratio_threshold_volume': [1.5, 2.0, 2.5],  # 量价齐升量比
    }
    
    logger.info(f"\n参数网格:")
    for param, values in param_grid.items():
        logger.info(f"  {param}: {values}")
    
    # 执行敏感性测试
    result_df = test_parameter_sensitivity(
        jq,
        test_date_range,
        test_stocks,
        param_grid
    )
    
    if result_df.empty:
        logger.error("测试未产生任何结果")
        return
    
    # 分析结果
    logger.info("\n" + "=" * 70)
    logger.info("敏感性分析结果")
    logger.info("=" * 70)
    
    analysis = analyze_sensitivity_results(result_df)
    
    # 打印Top 10
    if 'top_10' in analysis:
        print("\n📊 Top 10 参数组合:")
        print("-" * 70)
        for i, combo in enumerate(analysis['top_10'][:5], 1):
            print(f"\n{i}. 综合评分: {combo.get('composite_score', 0):.2f}")
            print(f"   平均收益: {combo.get('avg_return', 0):.2f}%")
            print(f"   胜率: {combo.get('win_rate', 0):.2f}%")
            print(f"   信号数: {combo.get('total_signals', 0)}")
            print(f"   参数:")
            for key, value in combo.items():
                if key not in ['total_signals', 'avg_return', 'win_rate', 'avg_score', 'composite_score']:
                    print(f"     {key}: {value}")
    
    # 打印最优参数
    if 'best_params' in analysis:
        print(f"\n🏆 最优参数组合:")
        print("-" * 70)
        best = analysis['best_params']
        print(f"综合评分: {best.get('composite_score', 0):.2f}")
        print(f"平均收益: {best.get('avg_return', 0):.2f}%")
        print(f"胜率: {best.get('win_rate', 0):.2f}%")
        print(f"信号数: {best.get('total_signals', 0)}")
        print(f"参数:")
        for key, value in best.items():
            if key not in ['total_signals', 'avg_return', 'win_rate', 'avg_score', 'composite_score']:
                print(f"  {key}: {value}")
    
    # 保存结果
    output_dir = PROJECT_ROOT / 'output' / 'chase_rise_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存DataFrame
    csv_path = output_dir / f'sensitivity_results_{timestamp}.csv'
    result_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n✅ 测试结果已保存: {csv_path}")
    
    # 保存分析结果
    json_path = output_dir / f'sensitivity_analysis_{timestamp}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"✅ 分析结果已保存: {json_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("敏感性测试完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
