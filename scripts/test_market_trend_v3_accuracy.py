#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phase 1: 验证MarketTrendAnalyzerV3在2024政策牛期间的输出准确性

目的:
1. 测试MarketTrendAnalyzerV3在牛市期间的识别能力
2. 分析ensemble_score与实际市场表现的对应关系
3. 找出识别不准确的原因

作者: TRQuant Team
版本: V6.0 开发测试
日期: 2026-01-12
"""

import sys
from pathlib import Path

# 设置路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def setup_jqdata():
    """初始化JQData"""
    try:
        import jqdatasdk as jq
        config_path = project_root / "config" / "jqdata_config.json"
        with open(config_path) as f:
            config = json.load(f)
        jq.auth(config['username'], config['password'])
        logger.info(f"JQData认证成功")
        return jq
    except Exception as e:
        logger.error(f"JQData认证失败: {e}")
        return None


def test_market_trend_analyzer_v3():
    """测试MarketTrendAnalyzerV3"""
    
    print("=" * 70)
    print("Phase 1: MarketTrendAnalyzerV3 准确性验证")
    print("=" * 70)
    
    # 1. 初始化JQData
    jq = setup_jqdata()
    if not jq:
        return None
    
    # 2. 初始化MarketTrendAnalyzerV3
    try:
        from core.advisor_v3.market_trend_v3 import MarketTrendAnalyzerV3
        analyzer = MarketTrendAnalyzerV3(use_composite=True)
        logger.info("MarketTrendAnalyzerV3 初始化成功")
    except Exception as e:
        logger.error(f"MarketTrendAnalyzerV3 初始化失败: {e}")
        return None
    
    # 3. 定义测试时段
    test_periods = {
        "2024_policy_bull": {
            "start": "2024-09-20",
            "end": "2024-10-15",
            "expected_type": "快牛",
            "description": "2024政策牛市（924大涨）"
        },
        "2024_year_end": {
            "start": "2024-11-15",
            "end": "2024-12-15",
            "expected_type": "震荡/慢牛",
            "description": "2024年末行情"
        },
        "2020_summer_bull": {
            "start": "2020-06-15",
            "end": "2020-07-31",
            "expected_type": "快牛",
            "description": "2020夏季牛市"
        },
        "2019_spring_slow": {
            "start": "2019-02-01",
            "end": "2019-04-15",
            "expected_type": "慢牛",
            "description": "2019春季慢牛"
        },
    }
    
    # 4. 获取沪深300指数数据作为基准
    print("\n获取沪深300指数数据...")
    index_code = "000300.XSHG"
    
    results = {}
    
    for period_name, period_info in test_periods.items():
        print(f"\n{'='*60}")
        print(f"测试时段: {period_name} - {period_info['description']}")
        print(f"{'='*60}")
        
        start_date = period_info['start']
        end_date = period_info['end']
        
        # 获取指数数据
        try:
            index_df = jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            if index_df is None or len(index_df) == 0:
                logger.warning(f"无法获取 {period_name} 的指数数据")
                continue
            
            # 计算实际涨幅
            actual_return = (index_df['close'].iloc[-1] / index_df['close'].iloc[0] - 1) * 100
            max_return = (index_df['close'].max() / index_df['close'].iloc[0] - 1) * 100
            volatility = index_df['close'].pct_change().std() * 100
            
            print(f"实际指数表现:")
            print(f"  - 区间涨幅: {actual_return:.2f}%")
            print(f"  - 最大涨幅: {max_return:.2f}%")
            print(f"  - 日波动率: {volatility:.2f}%")
            
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
            continue
        
        # 在时段内多个日期测试分析器
        test_dates = pd.date_range(start=start_date, end=end_date, freq='5D')
        
        period_results = []
        
        for test_date in test_dates:
            date_str = test_date.strftime('%Y-%m-%d')
            
            try:
                # 调用分析器
                result = analyzer.analyze(
                    as_of_date=date_str,
                    index_code=index_code,
                )
                
                if result:
                    period_results.append({
                        "date": date_str,
                        "ensemble_score": result.ensemble_score,
                        "direction": result.direction,
                        "hmm_state": result.hmm_state,
                        "hmm_confidence": result.hmm_confidence,
                        "resonance_phase": result.resonance_phase,
                        "position_cap": result.position_cap,
                        "strategy_mode": result.strategy_mode,
                        "period_scores": result.period_scores,
                    })
                    
                    print(f"\n日期: {date_str}")
                    print(f"  综合得分: {result.ensemble_score:.1f}")
                    print(f"  趋势方向: {result.direction}")
                    print(f"  HMM状态: {result.hmm_state} (置信度: {result.hmm_confidence:.2f})")
                    print(f"  共振阶段: {result.resonance_phase}")
                    print(f"  仓位上限: {result.position_cap:.0%}")
                    print(f"  策略模式: {result.strategy_mode}")
                    print(f"  周期得分: {result.period_scores}")
                    
            except Exception as e:
                logger.warning(f"分析 {date_str} 失败: {e}")
        
        # 汇总该时段结果
        if period_results:
            avg_score = np.mean([r['ensemble_score'] for r in period_results])
            avg_position_cap = np.mean([r['position_cap'] for r in period_results])
            
            # 统计各状态出现次数
            hmm_states = [r['hmm_state'] for r in period_results]
            directions = [r['direction'] for r in period_results]
            
            results[period_name] = {
                "period_info": period_info,
                "actual_return": actual_return,
                "max_return": max_return,
                "volatility": volatility,
                "avg_ensemble_score": avg_score,
                "avg_position_cap": avg_position_cap,
                "hmm_states": dict(pd.Series(hmm_states).value_counts()),
                "directions": dict(pd.Series(directions).value_counts()),
                "detailed_results": period_results,
            }
            
            print(f"\n--- 时段汇总 ---")
            print(f"平均综合得分: {avg_score:.1f}")
            print(f"平均仓位上限: {avg_position_cap:.0%}")
            print(f"HMM状态分布: {results[period_name]['hmm_states']}")
            print(f"趋势方向分布: {results[period_name]['directions']}")
            print(f"期望类型: {period_info['expected_type']}")
            
            # 判断是否准确
            if period_info['expected_type'] == "快牛":
                if avg_score > 40:
                    print(f"✓ 识别准确: 得分{avg_score:.1f} > 40，符合快牛预期")
                else:
                    print(f"✗ 识别偏差: 得分{avg_score:.1f} <= 40，未识别为快牛")
            elif period_info['expected_type'] == "慢牛":
                if 20 < avg_score <= 40:
                    print(f"✓ 识别准确: 得分{avg_score:.1f}，符合慢牛预期")
                else:
                    print(f"? 识别偏差: 得分{avg_score:.1f}")
    
    # 5. 保存结果
    output_dir = project_root / "output" / "bull_market_v6"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存JSON
    output_file = output_dir / f"market_trend_v3_accuracy_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # 转换numpy类型
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    results_serializable = json.loads(json.dumps(results, default=convert_numpy))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_serializable, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    
    return results


def analyze_accuracy_issues(results: dict):
    """分析准确性问题并给出改进建议"""
    
    print("\n" + "=" * 70)
    print("准确性问题分析与改进建议")
    print("=" * 70)
    
    issues = []
    recommendations = []
    
    for period_name, data in results.items():
        period_info = data['period_info']
        expected = period_info['expected_type']
        avg_score = data['avg_ensemble_score']
        actual_return = data['actual_return']
        
        # 分析问题
        if expected == "快牛" and avg_score <= 30:
            issues.append({
                "period": period_name,
                "issue": f"快牛时段({actual_return:.1f}%涨幅)未被识别，得分仅{avg_score:.1f}",
                "severity": "高"
            })
            
        if expected == "快牛" and avg_score <= 50 and actual_return > 15:
            issues.append({
                "period": period_name,
                "issue": f"指数涨幅{actual_return:.1f}%但得分仅{avg_score:.1f}，阈值偏高",
                "severity": "中"
            })
    
    # 改进建议
    print("\n【问题诊断】")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. [{issue['severity']}] {issue['period']}: {issue['issue']}")
    
    print("\n【改进建议】")
    recommendations = [
        "1. 降低牛市识别阈值: trend_score_bull 从 30 降至 20",
        "2. 增加短期动量权重: 当20日涨幅>10%时，额外加分",
        "3. 增加涨停数量监测: 实时统计每日涨停数量，作为辅助判断",
        "4. 增加政策事件驱动: 检测重大政策发布后的快速切换机制",
        "5. HMM状态滞后修正: 当连续3日大涨时，强制切换为牛市状态",
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    return issues, recommendations


def main():
    """主函数"""
    print("=" * 70)
    print("牛市高回报策略 V6.0 - Phase 1: 市场趋势分析验证")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行测试
    results = test_market_trend_analyzer_v3()
    
    if results:
        # 分析问题
        issues, recommendations = analyze_accuracy_issues(results)
        
        print("\n" + "=" * 70)
        print("Phase 1 完成: 下一步将根据分析结果改进MarketCharacterClassifier")
        print("=" * 70)
    else:
        print("\n测试失败，请检查错误日志")
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
