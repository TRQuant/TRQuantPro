"""
陈小群战法策略库测试脚本

测试所有库函数的功能和一致性。
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from core.strategies.chen_xiaoqun import (
    judge_emotion_cycle,
    select_first_board_stocks,
    select_dragon_stocks,
    identify_exchange_and_convert,
    analyze_third_board,
    monitor_position,
    judge_stop_loss,
    convert_code_to_jq
)


def test_judge_emotion_cycle():
    """测试情绪周期判断函数"""
    print("=" * 80)
    print("测试1: judge_emotion_cycle - 情绪周期判断")
    print("=" * 80)
    
    test_cases = [
        # (limit_up_count, max_height, zhaban_rate, avg_inflow, fund_sentiment_score, expected_cycle)
        (5, 2, 45.0, -1.5, -1.0, "退潮期"),
        (15, 3, 15.0, 0.5, 0.5, "启动期"),
        (45, 5, 20.0, 1.5, 1.0, "加速期"),
        (80, 8, 35.0, 2.0, 1.5, "过热期"),
    ]
    
    all_passed = True
    for i, (limit_up, height, zhaban, inflow, fund_score, expected) in enumerate(test_cases, 1):
        result = judge_emotion_cycle(limit_up, height, zhaban, inflow, fund_score)
        cycle = result['cycle']
        passed = cycle == expected
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"{status} 测试用例{i}: 涨停{limit_up}只, 连板{height}板, 炸板率{zhaban}%")
        print(f"   预期: {expected}, 实际: {cycle}, 置信度: {result['confidence_score']:.2f}")
        if not passed:
            print(f"   ⚠️  判断不一致！")
    
    print(f"\n{'✅ 所有测试通过' if all_passed else '❌ 部分测试失败'}")
    return all_passed


def test_identify_exchange_and_convert():
    """测试股票代码转换函数"""
    print("\n" + "=" * 80)
    print("测试2: identify_exchange_and_convert - 股票代码转换")
    print("=" * 80)
    
    test_cases = [
        # (code, expected_jq_code, expected_exchange, expected_valid)
        ("000001", "000001.XSHE", "XSHE", True),
        ("300001", "300001.XSHE", "XSHE", True),
        ("600000", "600000.XSHG", "XSHG", True),
        ("688001", "688001.XSHG", "XSHG", True),
        ("920001", None, "BSE", False),  # 北交所
        ("123456", None, "OTHER", False),  # 无效代码
    ]
    
    all_passed = True
    for i, (code, exp_jq, exp_exchange, exp_valid) in enumerate(test_cases, 1):
        jq_code, exchange, is_valid = identify_exchange_and_convert(code)
        passed = (jq_code == exp_jq and exchange == exp_exchange and is_valid == exp_valid)
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"{status} 测试用例{i}: {code}")
        print(f"   预期: {exp_jq}, {exp_exchange}, {exp_valid}")
        print(f"   实际: {jq_code}, {exchange}, {is_valid}")
        if not passed:
            print(f"   ⚠️  转换不一致！")
    
    print(f"\n{'✅ 所有测试通过' if all_passed else '❌ 部分测试失败'}")
    return all_passed


def test_select_first_board_stocks():
    """测试首板卡位术选股函数"""
    print("\n" + "=" * 80)
    print("测试3: select_first_board_stocks - 首板卡位术选股")
    print("=" * 80)
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            '代码': '000001',
            '名称': '测试股票1',
            '连板数': 1,
            '流通市值': 20 * 1e8,  # 20亿
            '封板资金': 0.5 * 1e8,  # 0.5亿，占比2.5%
            '所属行业': '测试行业'
        },
        {
            '代码': '000002',
            '名称': '测试股票2',
            '连板数': 1,
            '流通市值': 40 * 1e8,  # 40亿，不符合
            '封板资金': 1 * 1e8,
            '所属行业': '测试行业'
        },
        {
            '代码': '000003',
            '名称': '测试股票3',
            '连板数': 2,  # 不是首板
            '流通市值': 20 * 1e8,
            '封板资金': 0.5 * 1e8,
            '所属行业': '测试行业'
        },
        {
            '代码': '000004',
            '名称': '测试股票4',
            '连板数': 1,
            '流通市值': 20 * 1e8,
            '封板资金': 0.3 * 1e8,  # 占比1.5%，不符合
            '所属行业': '测试行业'
        },
    ])
    
    candidates = select_first_board_stocks(test_data)
    
    # 验证结果
    expected_count = 1  # 只有000001符合条件
    passed = len(candidates) == expected_count
    
    if passed and len(candidates) > 0:
        passed = passed and candidates[0]['code'] == '000001'
    
    status = "✅" if passed else "❌"
    print(f"{status} 测试结果: 找到 {len(candidates)} 只候选股票（预期: {expected_count}只）")
    
    if len(candidates) > 0:
        print(f"   候选股票: {candidates[0]['code']} {candidates[0]['name']}")
        print(f"   封板资金占比: {candidates[0]['limit_ratio']:.2f}%")
    
    print(f"\n{'✅ 测试通过' if passed else '❌ 测试失败'}")
    return passed


def test_select_dragon_stocks():
    """测试龙头战法选股函数"""
    print("\n" + "=" * 80)
    print("测试4: select_dragon_stocks - 龙头战法选股")
    print("=" * 80)
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            '代码': '000001',
            '名称': '测试股票1',
            '连板数': 5,  # 最高连板
            '所属行业': '测试行业'
        },
        {
            '代码': '000002',
            '名称': '测试股票2',
            '连板数': 3,
            '所属行业': '测试行业'
        },
        {
            '代码': '000003',
            '名称': '测试股票3',
            '连板数': 5,  # 也是最高连板
            '所属行业': '测试行业'
        },
        {
            '代码': '000004',
            '名称': '测试股票4',
            '连板数': 1,  # 不是连板
            '所属行业': '测试行业'
        },
    ])
    
    dragons = select_dragon_stocks(test_data)
    
    # 验证结果：应该找到2只5板的股票
    expected_count = 2
    passed = len(dragons) == expected_count
    
    if passed and len(dragons) > 0:
        passed = passed and all(d['board_count'] == 5 for d in dragons)
        passed = passed and set(d['code'] for d in dragons) == {'000001', '000003'}
    
    status = "✅" if passed else "❌"
    print(f"{status} 测试结果: 找到 {len(dragons)} 只龙头股票（预期: {expected_count}只）")
    
    if len(dragons) > 0:
        for dragon in dragons:
            print(f"   龙头股票: {dragon['code']} {dragon['name']} - {dragon['board_count']}板")
    
    print(f"\n{'✅ 测试通过' if passed else '❌ 测试失败'}")
    return passed


def test_analyze_third_board():
    """测试三板加速术分析函数"""
    print("\n" + "=" * 80)
    print("测试5: analyze_third_board - 三板加速术分析")
    print("=" * 80)
    
    # 创建测试数据（需要至少3只同板块股票才能产生板块效应）
    test_data = pd.DataFrame([
        {
            '代码': '000001',
            '名称': '测试股票1',
            '连板数': 2,
            '换手率': 5.0,  # 缩量
            '所属行业': '测试行业',
            '封板资金': 6 * 1e8  # 6亿（>=5亿，资金共识强）
        },
        {
            '代码': '000002',
            '名称': '测试股票2',
            '连板数': 3,
            '换手率': 8.0,  # 缩量
            '所属行业': '测试行业',
            '封板资金': 5 * 1e8  # 5亿
        },
        {
            '代码': '000003',
            '名称': '测试股票3',
            '连板数': 1,  # 首板，用于增加板块效应
            '换手率': 10.0,
            '所属行业': '测试行业',
            '封板资金': 2 * 1e8
        },
        {
            '代码': '000004',
            '名称': '测试股票4',
            '连板数': 1,  # 首板，用于增加板块效应
            '换手率': 12.0,
            '所属行业': '测试行业',
            '封板资金': 1.5 * 1e8
        },
    ])
    
    # 分析三板潜力
    result_df = analyze_third_board(test_data)
    
    passed = not result_df.empty
    if passed:
        # 验证高潜力股票
        high_potential = result_df[result_df['三板潜力'] == '高']
        passed = len(high_potential) > 0
    
    status = "✅" if passed else "❌"
    print(f"{status} 测试结果: 分析 {len(result_df)} 只股票")
    
    if not result_df.empty:
        print(f"   高潜力: {len(result_df[result_df['三板潜力'] == '高'])}只")
        print(f"   中潜力: {len(result_df[result_df['三板潜力'] == '中'])}只")
        print(f"   低潜力: {len(result_df[result_df['三板潜力'] == '低'])}只")
    
    print(f"\n{'✅ 测试通过' if passed else '❌ 测试失败'}")
    return passed


def test_monitor_position():
    """测试持仓监控函数"""
    print("\n" + "=" * 80)
    print("测试6: monitor_position - 持仓监控")
    print("=" * 80)
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            '代码': '000001',
            '名称': '测试股票1',
            '连板数': 3,
            '封板资金': 2 * 1e8,  # 2亿
            '所属行业': '测试行业'
        },
    ])
    
    # 添加板块内其他股票（模拟板块效应）
    test_data = pd.concat([
        test_data,
        pd.DataFrame([
            {'代码': '000002', '名称': '测试股票2', '连板数': 2, '封板资金': 1e8, '所属行业': '测试行业'},
            {'代码': '000003', '名称': '测试股票3', '连板数': 1, '封板资金': 0.5e8, '所属行业': '测试行业'},
        ])
    ], ignore_index=True)
    
    status, risk, signals = monitor_position('000001', '测试股票1', test_data)
    
    passed = status == 'holding' and risk < 30
    
    status_icon = "✅" if passed else "❌"
    print(f"{status_icon} 测试结果: 状态={status}, 风险={risk}/100")
    print(f"   信号: {len(signals)}条")
    for signal in signals:
        print(f"      - {signal}")
    
    print(f"\n{'✅ 测试通过' if passed else '❌ 测试失败'}")
    return passed


def test_judge_stop_loss():
    """测试止盈止损判断函数"""
    print("\n" + "=" * 80)
    print("测试7: judge_stop_loss - 止盈止损判断")
    print("=" * 80)
    
    # 测试高风险情况
    result1 = judge_stop_loss(
        zhaban_rate=35.0,
        limit_up_count=100,
        max_height=8,
        emotion_cycle="过热期",
        limit_up_count_today=70,
        max_height_today=6
    )
    
    passed1 = result1['market_risk'] >= 50
    
    status1 = "✅" if passed1 else "❌"
    print(f"{status1} 测试用例1（高风险）: 风险等级={result1['market_risk']}/100")
    print(f"   操作建议: {result1['operation_advice']}")
    
    # 测试低风险情况
    result2 = judge_stop_loss(
        zhaban_rate=15.0,
        limit_up_count=30,
        max_height=4,
        emotion_cycle="加速期",
        limit_up_count_today=35,
        max_height_today=5
    )
    
    passed2 = result2['market_risk'] < 30
    
    status2 = "✅" if passed2 else "❌"
    print(f"{status2} 测试用例2（低风险）: 风险等级={result2['market_risk']}/100")
    print(f"   操作建议: {result2['operation_advice']}")
    
    all_passed = passed1 and passed2
    print(f"\n{'✅ 所有测试通过' if all_passed else '❌ 部分测试失败'}")
    return all_passed


def test_consistency_with_notebook():
    """测试与notebook输出的一致性"""
    print("\n" + "=" * 80)
    print("测试8: 一致性测试 - 与notebook输出对比")
    print("=" * 80)
    
    # 使用真实场景的数据进行测试
    # 场景1: 过热期（102只涨停，5板，36.65%炸板率）
    result1 = judge_emotion_cycle(
        limit_up_count=102,
        max_height=5,
        zhaban_rate=36.65,
        avg_inflow=-2.26,
        fund_sentiment_score=-2.0
    )
    
    passed1 = result1['cycle'] == '过热期'
    status1 = "✅" if passed1 else "❌"
    print(f"{status1} 场景1（过热期）: {result1['cycle']}, 置信度={result1['confidence_score']:.2f}")
    
    # 场景2: 启动期（15只涨停，3板，15%炸板率）
    result2 = judge_emotion_cycle(
        limit_up_count=15,
        max_height=3,
        zhaban_rate=15.0,
        avg_inflow=0.5,
        fund_sentiment_score=0.5
    )
    
    passed2 = result2['cycle'] == '启动期'
    status2 = "✅" if passed2 else "❌"
    print(f"{status2} 场景2（启动期）: {result2['cycle']}, 置信度={result2['confidence_score']:.2f}")
    
    all_passed = passed1 and passed2
    print(f"\n{'✅ 一致性测试通过' if all_passed else '❌ 一致性测试失败'}")
    return all_passed


def main():
    """运行所有测试"""
    print("=" * 80)
    print("陈小群战法策略库 - 完整测试套件")
    print("=" * 80)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("情绪周期判断", test_judge_emotion_cycle()))
    test_results.append(("股票代码转换", test_identify_exchange_and_convert()))
    test_results.append(("首板卡位术选股", test_select_first_board_stocks()))
    test_results.append(("龙头战法选股", test_select_dragon_stocks()))
    test_results.append(("三板加速术分析", test_analyze_third_board()))
    test_results.append(("持仓监控", test_monitor_position()))
    test_results.append(("止盈止损判断", test_judge_stop_loss()))
    test_results.append(("一致性测试", test_consistency_with_notebook()))
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    passed_count = sum(1 for _, result in test_results if result)
    total_count = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print(f"\n总计: {passed_count}/{total_count} 测试通过")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！库函数功能正常，可以用于回测。")
        return True
    else:
        print(f"\n⚠️  有 {total_count - passed_count} 个测试失败，请检查代码。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
