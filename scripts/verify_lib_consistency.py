"""
验证库函数输出与notebook输出的一致性

对比：
1. judge_emotion_cycle的输出格式
2. select_first_board_stocks的输出格式
3. select_dragon_stocks的输出格式
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
from core.strategies.chen_xiaoqun import (
    judge_emotion_cycle,
    select_first_board_stocks,
    select_dragon_stocks
)

print("=" * 80)
print("库函数输出格式一致性验证")
print("=" * 80)

# ========== 1. 验证judge_emotion_cycle输出格式 ==========
print("\n1. judge_emotion_cycle输出格式验证")
print("-" * 80)

# 使用与01_notebook相同的测试数据
test_cases = [
    {
        'name': '过热期场景（与01_notebook一致）',
        'limit_up_count': 102,
        'max_height': 5,
        'zhaban_rate': 36.65,
        'avg_inflow': -2.26,
        'fund_sentiment_score': -2.0,
        'expected_cycle': '过热期',
        'expected_position': '30-50%',
        'expected_strategy': '逐步减仓'
    },
    {
        'name': '启动期场景',
        'limit_up_count': 15,
        'max_height': 3,
        'zhaban_rate': 15.0,
        'avg_inflow': 0.5,
        'fund_sentiment_score': 0.5,
        'expected_cycle': '启动期',
        'expected_position': '10%',
        'expected_strategy': '首板卡位术（10%试错仓）'
    }
]

for case in test_cases:
    result = judge_emotion_cycle(
        case['limit_up_count'],
        case['max_height'],
        case['zhaban_rate'],
        case['avg_inflow'],
        case['fund_sentiment_score']
    )
    
    # 验证输出格式
    required_keys = ['cycle', 'position', 'strategy', 'limit_up_count', 'max_height', 
                     'zhaban_rate', 'avg_inflow', 'confidence_score', 'confidence_level', 
                     'confidence_icon', 'factors']
    has_all_keys = all(key in result for key in required_keys)
    
    # 验证输出值
    cycle_match = result['cycle'] == case['expected_cycle']
    position_match = result['position'] == case['expected_position']
    strategy_match = case['expected_strategy'] in result['strategy']  # 策略名称可能包含额外描述
    
    passed = has_all_keys and cycle_match and position_match and strategy_match
    
    status = "✅" if passed else "❌"
    print(f"{status} {case['name']}")
    print(f"   周期: {result['cycle']} (期望: {case['expected_cycle']}) {'✅' if cycle_match else '❌'}")
    print(f"   仓位: {result['position']} (期望: {case['expected_position']}) {'✅' if position_match else '❌'}")
    print(f"   策略: {result['strategy']} (期望包含: {case['expected_strategy']}) {'✅' if strategy_match else '❌'}")
    print(f"   包含所有键: {'✅' if has_all_keys else '❌'}")
    if not passed:
        print(f"   ⚠️  输出不一致！")

# ========== 2. 验证select_first_board_stocks输出格式 ==========
print("\n2. select_first_board_stocks输出格式验证")
print("-" * 80)

# 创建与02_notebook相同格式的测试数据
test_data = pd.DataFrame([
    {
        '代码': '000001',
        '名称': '测试股票1',
        '连板数': 1,
        '流通市值': 20 * 1e8,  # 20亿，符合条件
        '封板资金': 0.5 * 1e8,  # 0.5亿，占比2.5%，符合条件
        '所属行业': '测试行业'
    },
    {
        '代码': '000002',
        '名称': '测试股票2',
        '连板数': 1,
        '流通市值': 40 * 1e8,  # 40亿，不符合条件
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
    }
])

candidates = select_first_board_stocks(test_data)

# 验证输出格式
expected_keys = ['code', 'jq_code', 'name', 'market_cap', 'limit_ratio', 'sector']
if candidates:
    actual_keys = list(candidates[0].keys())
    keys_match = set(expected_keys) == set(actual_keys)
    
    # 验证逻辑正确性（应该只返回1只符合条件的股票）
    count_match = len(candidates) == 1
    code_match = candidates[0]['code'] == '000001'
    
    passed = keys_match and count_match and code_match
    
    status = "✅" if passed else "❌"
    print(f"{status} 输出格式验证")
    print(f"   返回数量: {len(candidates)}只 (期望: 1只) {'✅' if count_match else '❌'}")
    print(f"   包含的键: {actual_keys}")
    print(f"   键匹配: {'✅' if keys_match else '❌'}")
    print(f"   选中的股票: {candidates[0]['code']} (期望: 000001) {'✅' if code_match else '❌'}")
    print(f"   示例: {candidates[0]}")
else:
    print("❌ 未返回任何候选股票")

# ========== 3. 验证select_dragon_stocks输出格式 ==========
print("\n3. select_dragon_stocks输出格式验证")
print("-" * 80)

test_data2 = pd.DataFrame([
    {
        '代码': '000001',
        '名称': '测试龙头1',
        '连板数': 5,  # 最高连板
        '所属行业': '测试行业'
    },
    {
        '代码': '000002',
        '名称': '测试龙头2',
        '连板数': 3,
        '所属行业': '测试行业'
    },
    {
        '代码': '000003',
        '名称': '测试龙头3',
        '连板数': 5,  # 也是最高连板
        '所属行业': '测试行业'
    }
])

dragons = select_dragon_stocks(test_data2)

# 验证输出格式
expected_keys = ['code', 'jq_code', 'name', 'board_count', 'sector']
if dragons:
    actual_keys = list(dragons[0].keys())
    keys_match = set(expected_keys) == set(actual_keys)
    
    # 验证逻辑正确性（应该返回2只5板的股票）
    count_match = len(dragons) == 2
    board_match = all(d['board_count'] == 5 for d in dragons)
    codes_match = set(d['code'] for d in dragons) == {'000001', '000003'}
    
    passed = keys_match and count_match and board_match and codes_match
    
    status = "✅" if passed else "❌"
    print(f"{status} 输出格式验证")
    print(f"   返回数量: {len(dragons)}只 (期望: 2只) {'✅' if count_match else '❌'}")
    print(f"   包含的键: {actual_keys}")
    print(f"   键匹配: {'✅' if keys_match else '❌'}")
    print(f"   连板数: {[d['board_count'] for d in dragons]} (期望: 都是5) {'✅' if board_match else '❌'}")
    print(f"   选中的股票: {[d['code'] for d in dragons]} (期望: ['000001', '000003']) {'✅' if codes_match else '❌'}")
    print(f"   示例: {dragons[0]}")
else:
    print("❌ 未返回任何龙头股票")

# ========== 4. 验证04_backtest_validation.ipynb是否已修改 ==========
print("\n4. 验证04_backtest_validation.ipynb是否已修改")
print("-" * 80)

import json
notebook_path = project_root / 'notebooks' / 'research' / 'chen_xiaoqun_strategy' / '04_backtest_validation.ipynb'

if notebook_path.exists():
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # 检查Cell 2中是否导入了策略库
    cell2_imported = False
    cell12_uses_lib = False
    cell15_uses_lib = False
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Cell 2: 检查导入
            if 'from core.strategies.chen_xiaoqun import' in source:
                cell2_imported = True
                print(f"   ✅ Cell {i}: 已导入策略库")
            
            # Cell 12: 检查是否使用库函数
            if '使用策略库中的judge_emotion_cycle函数' in source:
                cell12_uses_lib = True
                print(f"   ✅ Cell {i}: 已使用库函数judge_emotion_cycle")
            
            # Cell 15: 检查是否使用库函数
            if '使用策略库中的选股函数' in source and '已从core.strategies.chen_xiaoqun导入' in source:
                cell15_uses_lib = True
                print(f"   ✅ Cell {i}: 已使用库函数选股")
            
            # 检查是否还有内联函数定义
            if 'def select_first_board_stocks(limit_up_data, date_str):' in source and '首板卡位术选股（启动期）' in source:
                print(f"   ⚠️  Cell {i}: 仍包含内联函数定义 select_first_board_stocks")
            if 'def select_dragon_stocks(limit_up_data, date_str):' in source and '龙头战法选股（加速期）' in source:
                print(f"   ⚠️  Cell {i}: 仍包含内联函数定义 select_dragon_stocks")
            if 'def identify_exchange_and_convert(code):' in source and '识别股票交易所类型并转换为JQData格式' in source:
                print(f"   ⚠️  Cell {i}: 仍包含内联函数定义 identify_exchange_and_convert")
    
    print(f"\n   修改状态:")
    print(f"   - Cell 2导入库: {'✅' if cell2_imported else '❌'}")
    print(f"   - Cell 12使用库: {'✅' if cell12_uses_lib else '❌'}")
    print(f"   - Cell 15使用库: {'✅' if cell15_uses_lib else '❌'}")
    
    all_modified = cell2_imported and cell12_uses_lib and cell15_uses_lib
    print(f"\n   总体状态: {'✅ 已修改' if all_modified else '❌ 未完全修改'}")
else:
    print("   ❌ 未找到notebook文件")

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
