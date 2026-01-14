"""
对比库函数输出与notebook实际运行结果（使用1月14日数据）

读取notebook保存的结果文件，与库函数输出进行详细对比
"""

import sys
from pathlib import Path
import json
import pandas as pd

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import akshare as ak
from core.strategies.chen_xiaoqun import (
    judge_emotion_cycle,
    select_first_board_stocks,
    select_dragon_stocks
)

print("=" * 80)
print("对比库函数输出与notebook实际运行结果（1月14日数据）")
print("=" * 80)

# ========== 1. 读取notebook结果文件 ==========
print("\n1. 读取notebook结果文件")
print("-" * 80)

# 读取01_notebook的最新结果
nb01_result_path = project_root / 'notebooks' / 'research' / 'results' / 'chen_xiaoqun_strategy' / '01_market_environment_judgment' / '20260114_222537' / 'result.json'
nb02_result_path = project_root / 'notebooks' / 'research' / 'results' / 'chen_xiaoqun_strategy' / '02_stock_selection' / '20260114_212145' / 'result.json'

nb01_result = None
nb02_result = None

if nb01_result_path.exists():
    with open(nb01_result_path, 'r', encoding='utf-8') as f:
        nb01_result = json.load(f)
    print(f"   ✅ 读取01_notebook结果: {nb01_result_path.name}")
else:
    print(f"   ❌ 未找到01_notebook结果文件")

if nb02_result_path.exists():
    with open(nb02_result_path, 'r', encoding='utf-8') as f:
        nb02_result = json.load(f)
    print(f"   ✅ 读取02_notebook结果: {nb02_result_path.name}")
else:
    print(f"   ❌ 未找到02_notebook结果文件")

# ========== 2. 提取notebook中的关键数据 ==========
print("\n2. 提取notebook中的关键数据")
print("-" * 80)

if nb01_result:
    # 提取情绪周期判断结果
    nb_cycle = nb01_result.get('cycle', 'N/A')
    nb_position = nb01_result.get('position', 'N/A')
    nb_strategy = nb01_result.get('strategy', 'N/A')
    nb_limit_up_count = nb01_result.get('limit_up_count', 0)
    nb_max_height = nb01_result.get('max_height', 0)
    nb_zhaban_rate = nb01_result.get('zhaban_rate', 0.0)
    
    print(f"   Notebook 01输出:")
    print(f"   - 情绪周期: {nb_cycle}")
    print(f"   - 建议仓位: {nb_position}")
    print(f"   - 推荐策略: {nb_strategy}")
    print(f"   - 涨停家数: {nb_limit_up_count}只")
    print(f"   - 最高连板: {nb_max_height}板")
    print(f"   - 炸板率: {nb_zhaban_rate:.2f}%")

if nb02_result:
    # 提取选股结果
    nb_first_board = nb02_result.get('first_board_candidates', [])
    nb_dragon = nb02_result.get('dragon_stocks', [])
    
    print(f"\n   Notebook 02输出:")
    print(f"   - 首板候选: {len(nb_first_board)}只")
    print(f"   - 龙头股票: {len(nb_dragon)}只")
    
    if nb_first_board:
        print(f"   - 首板候选前3只:")
        for i, stock in enumerate(nb_first_board[:3], 1):
            code = stock.get('代码', stock.get('code', 'N/A'))
            name = stock.get('名称', stock.get('name', 'N/A'))
            print(f"     {i}. {code} {name}")
    
    if nb_dragon:
        print(f"   - 龙头股票:")
        for i, stock in enumerate(nb_dragon[:3], 1):
            code = stock.get('代码', stock.get('code', 'N/A'))
            name = stock.get('名称', stock.get('name', 'N/A'))
            board_count = stock.get('连板数', stock.get('board_count', 'N/A'))
            print(f"     {i}. {code} {name} ({board_count}板)")

# ========== 3. 使用相同数据调用库函数 ==========
print("\n3. 使用相同数据调用库函数")
print("-" * 80)

target_date = "2026-01-14"
target_date_compact = "20260114"

# 获取涨停板数据
print(f"   正在获取 {target_date} 的涨停板数据...")
try:
    limit_up_data = ak.stock_zt_pool_em(date=target_date_compact)
    if limit_up_data is not None and not limit_up_data.empty:
        limit_up_count = len(limit_up_data)
        if '连板数' in limit_up_data.columns:
            max_height = int(limit_up_data['连板数'].max())
        else:
            max_height = 0
        print(f"   ✅ 涨停家数: {limit_up_count}只, 最高连板: {max_height}板")
    else:
        limit_up_data = None
        limit_up_count = 0
        max_height = 0
        print(f"   ⚠️  涨停板数据为空")
except Exception as e:
    limit_up_data = None
    limit_up_count = 0
    max_height = 0
    print(f"   ❌ 获取失败: {str(e)[:100]}")

# 获取炸板率
print(f"   正在获取炸板率...")
try:
    from core.market_data.zhaban_rate_fetcher import get_zhaban_rate
    zhaban_result = get_zhaban_rate(target_date_compact, limit_up_count)
    zhaban_rate = zhaban_result.get('zhaban_rate', 0.0)
    print(f"   ✅ 炸板率: {zhaban_rate:.2f}%")
except Exception as e:
    zhaban_rate = 0.0
    print(f"   ⚠️  获取失败，使用默认值: {str(e)[:100]}")

# 调用库函数
avg_inflow = 0.0
fund_sentiment_score = 0.0

lib_result = judge_emotion_cycle(
    limit_up_count,
    max_height,
    zhaban_rate,
    avg_inflow,
    fund_sentiment_score
)

print(f"\n   库函数输出:")
print(f"   - 情绪周期: {lib_result['cycle']}")
print(f"   - 建议仓位: {lib_result['position']}")
print(f"   - 推荐策略: {lib_result['strategy']}")
print(f"   - 涨停家数: {lib_result['limit_up_count']}只")
print(f"   - 最高连板: {lib_result['max_height']}板")
print(f"   - 炸板率: {lib_result['zhaban_rate']:.2f}%")

# 调用选股函数
if limit_up_data is not None and not limit_up_data.empty:
    lib_first_board = select_first_board_stocks(limit_up_data, target_date)
    lib_dragon = select_dragon_stocks(limit_up_data, target_date)
    
    print(f"\n   库函数选股输出:")
    print(f"   - 首板候选: {len(lib_first_board)}只")
    print(f"   - 龙头股票: {len(lib_dragon)}只")
    
    if lib_first_board:
        print(f"   - 首板候选前3只:")
        for i, stock in enumerate(lib_first_board[:3], 1):
            print(f"     {i}. {stock['code']} {stock['name']}")
    
    if lib_dragon:
        print(f"   - 龙头股票:")
        for i, stock in enumerate(lib_dragon[:3], 1):
            print(f"     {i}. {stock['code']} {stock['name']} ({stock['board_count']}板)")
else:
    lib_first_board = []
    lib_dragon = []

# ========== 4. 详细对比 ==========
print("\n4. 详细对比结果")
print("=" * 80)

# 对比情绪周期判断
if nb01_result:
    print("\n【情绪周期判断对比】")
    print("-" * 80)
    
    cycle_match = lib_result['cycle'] == nb_cycle
    position_match = lib_result['position'] == nb_position
    strategy_match = lib_result['strategy'] == nb_strategy or nb_strategy in lib_result['strategy']
    count_match = lib_result['limit_up_count'] == nb_limit_up_count
    height_match = lib_result['max_height'] == nb_max_height
    zhaban_match = abs(lib_result['zhaban_rate'] - nb_zhaban_rate) < 0.01  # 允许0.01%的误差
    
    print(f"情绪周期: {'✅ 一致' if cycle_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['cycle']}")
    print(f"  Notebook: {nb_cycle}")
    
    print(f"\n建议仓位: {'✅ 一致' if position_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['position']}")
    print(f"  Notebook: {nb_position}")
    
    print(f"\n推荐策略: {'✅ 一致' if strategy_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['strategy']}")
    print(f"  Notebook: {nb_strategy}")
    
    print(f"\n涨停家数: {'✅ 一致' if count_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['limit_up_count']}只")
    print(f"  Notebook: {nb_limit_up_count}只")
    
    print(f"\n最高连板: {'✅ 一致' if height_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['max_height']}板")
    print(f"  Notebook: {nb_max_height}板")
    
    print(f"\n炸板率: {'✅ 一致' if zhaban_match else '❌ 不一致'}")
    print(f"  库函数: {lib_result['zhaban_rate']:.2f}%")
    print(f"  Notebook: {nb_zhaban_rate:.2f}%")
    
    all_match = cycle_match and position_match and strategy_match and count_match and height_match and zhaban_match
    print(f"\n总体结果: {'✅ 完全一致' if all_match else '❌ 存在差异'}")

# 对比选股结果
if nb02_result:
    print("\n【选股结果对比】")
    print("-" * 80)
    
    # 对比首板候选
    print(f"\n首板候选股票:")
    print(f"  库函数: {len(lib_first_board)}只")
    print(f"  Notebook: {len(nb_first_board)}只")
    
    if lib_first_board and nb_first_board:
        # 提取股票代码
        lib_first_codes = [s['code'] for s in lib_first_board]
        nb_first_codes = [s.get('代码', s.get('code', '')) for s in nb_first_board]
        
        # 对比前5只
        print(f"\n  前5只股票代码对比:")
        for i in range(min(5, len(lib_first_codes), len(nb_first_codes))):
            lib_code = lib_first_codes[i] if i < len(lib_first_codes) else 'N/A'
            nb_code = nb_first_codes[i] if i < len(nb_first_codes) else 'N/A'
            match = lib_code == nb_code
            status = "✅" if match else "❌"
            print(f"    {status} 位置{i+1}: 库函数={lib_code}, Notebook={nb_code}")
        
        # 集合对比
        lib_set = set(lib_first_codes[:10])  # 对比前10只
        nb_set = set(nb_first_codes[:10])
        set_match = lib_set == nb_set
        print(f"\n  前10只股票集合对比: {'✅ 完全一致' if set_match else '❌ 存在差异'}")
        if not set_match:
            only_lib = lib_set - nb_set
            only_nb = nb_set - lib_set
            if only_lib:
                print(f"    仅在库函数中: {only_lib}")
            if only_nb:
                print(f"    仅在Notebook中: {only_nb}")
    elif len(lib_first_board) == 0 and len(nb_first_board) == 0:
        print(f"  ✅ 两者都为空，一致")
    else:
        print(f"  ❌ 数量不一致")
    
    # 对比龙头股票
    print(f"\n龙头股票:")
    print(f"  库函数: {len(lib_dragon)}只")
    print(f"  Notebook: {len(nb_dragon)}只")
    
    if lib_dragon and nb_dragon:
        lib_dragon_codes = [s['code'] for s in lib_dragon]
        nb_dragon_codes = [s.get('代码', s.get('code', '')) for s in nb_dragon]
        
        print(f"\n  股票代码对比:")
        for i in range(min(5, len(lib_dragon_codes), len(nb_dragon_codes))):
            lib_code = lib_dragon_codes[i] if i < len(lib_dragon_codes) else 'N/A'
            nb_code = nb_dragon_codes[i] if i < len(nb_dragon_codes) else 'N/A'
            match = lib_code == nb_code
            status = "✅" if match else "❌"
            print(f"    {status} 位置{i+1}: 库函数={lib_code}, Notebook={nb_code}")
        
        lib_set = set(lib_dragon_codes)
        nb_set = set(nb_dragon_codes)
        set_match = lib_set == nb_set
        print(f"\n  股票集合对比: {'✅ 完全一致' if set_match else '❌ 存在差异'}")
        if not set_match:
            only_lib = lib_set - nb_set
            only_nb = nb_set - lib_set
            if only_lib:
                print(f"    仅在库函数中: {only_lib}")
            if only_nb:
                print(f"    仅在Notebook中: {only_nb}")
    elif len(lib_dragon) == 0 and len(nb_dragon) == 0:
        print(f"  ✅ 两者都为空，一致")
    else:
        print(f"  ❌ 数量不一致")

print("\n" + "=" * 80)
print("对比完成")
print("=" * 80)
