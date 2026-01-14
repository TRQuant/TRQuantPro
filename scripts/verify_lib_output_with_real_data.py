"""
使用1月14日的实际数据验证库函数输出与notebook输出是否一致

步骤：
1. 获取1月14日的实际市场数据（涨停家数、炸板率、连板高度等）
2. 调用库函数judge_emotion_cycle，获取输出
3. 获取1月14日的涨停板数据
4. 调用库函数select_first_board_stocks和select_dragon_stocks，获取输出
5. 对比与notebook中实际运行的结果是否一致
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

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
print("使用1月14日实际数据验证库函数输出与notebook输出一致性")
print("=" * 80)

# ========== 1. 获取1月14日的实际市场数据 ==========
print("\n1. 获取1月14日的实际市场数据")
print("-" * 80)

target_date = "2026-01-14"
target_date_compact = "20260114"

# 获取涨停板数据
print(f"   正在获取 {target_date} 的涨停板数据...")
try:
    limit_up_data = ak.stock_zt_pool_em(date=target_date_compact)
    if limit_up_data is not None and not limit_up_data.empty:
        limit_up_count = len(limit_up_data)
        print(f"   ✅ 涨停家数: {limit_up_count}只")
        
        # 计算最高连板高度
        if '连板数' in limit_up_data.columns:
            max_height = int(limit_up_data['连板数'].max())
            print(f"   ✅ 最高连板: {max_height}板")
        else:
            max_height = 0
            print(f"   ⚠️  未找到'连板数'列")
    else:
        limit_up_count = 0
        max_height = 0
        print(f"   ⚠️  涨停板数据为空")
except Exception as e:
    limit_up_count = 0
    max_height = 0
    print(f"   ❌ 获取涨停板数据失败: {str(e)[:100]}")

# 获取炸板率
print(f"   正在获取 {target_date} 的炸板率...")
try:
    from core.market_data.zhaban_rate_fetcher import get_zhaban_rate
    zhaban_result = get_zhaban_rate(target_date_compact, limit_up_count)
    zhaban_rate = zhaban_result.get('zhaban_rate', 0.0)
    print(f"   ✅ 炸板率: {zhaban_rate:.2f}%")
except Exception as e:
    zhaban_rate = 0.0
    print(f"   ⚠️  获取炸板率失败，使用默认值0%: {str(e)[:100]}")

# 获取资金流向（简化处理，使用默认值）
avg_inflow = 0.0
fund_sentiment_score = 0.0
print(f"   资金流向: 使用默认值（回测中通常为0）")

print(f"\n   汇总数据:")
print(f"   - 涨停家数: {limit_up_count}只")
print(f"   - 最高连板: {max_height}板")
print(f"   - 炸板率: {zhaban_rate:.2f}%")
print(f"   - 资金净流入: {avg_inflow:.2f}%")
print(f"   - 资金态度评分: {fund_sentiment_score:.2f}")

# ========== 2. 调用库函数judge_emotion_cycle ==========
print("\n2. 调用库函数judge_emotion_cycle")
print("-" * 80)

result = judge_emotion_cycle(
    limit_up_count,
    max_height,
    zhaban_rate,
    avg_inflow,
    fund_sentiment_score
)

print(f"   输出结果:")
print(f"   - 情绪周期: {result['cycle']}")
print(f"   - 建议仓位: {result['position']}")
print(f"   - 推荐策略: {result['strategy']}")
print(f"   - 置信度: {result['confidence_icon']} {result['confidence_level']} ({result['confidence_score']:.1f}/5.0)")
print(f"   - 判断依据:")
for factor in result['factors'][:3]:  # 只显示前3个
    print(f"     • {factor}")

# ========== 3. 调用库函数select_first_board_stocks ==========
print("\n3. 调用库函数select_first_board_stocks")
print("-" * 80)

if limit_up_data is not None and not limit_up_data.empty:
    first_board_candidates = select_first_board_stocks(limit_up_data, target_date)
    
    print(f"   输出结果:")
    print(f"   - 候选股票数量: {len(first_board_candidates)}只")
    
    if first_board_candidates:
        print(f"   - 前3只候选股票:")
        for i, stock in enumerate(first_board_candidates[:3], 1):
            print(f"     {i}. {stock['code']} {stock['name']}")
            print(f"        流通市值: {stock['market_cap']:.2f}亿元")
            print(f"        封板资金占比: {stock['limit_ratio']:.2f}%")
            print(f"        所属行业: {stock['sector']}")
    else:
        print(f"   - ⚠️  未找到符合条件的首板股票")
else:
    first_board_candidates = []
    print(f"   - ⚠️  无法获取涨停板数据，跳过选股")

# ========== 4. 调用库函数select_dragon_stocks ==========
print("\n4. 调用库函数select_dragon_stocks")
print("-" * 80)

if limit_up_data is not None and not limit_up_data.empty:
    dragon_stocks = select_dragon_stocks(limit_up_data, target_date)
    
    print(f"   输出结果:")
    print(f"   - 龙头股票数量: {len(dragon_stocks)}只")
    
    if dragon_stocks:
        print(f"   - 龙头股票列表:")
        for i, stock in enumerate(dragon_stocks[:5], 1):  # 显示前5只
            print(f"     {i}. {stock['code']} {stock['name']}")
            print(f"        连板数: {stock['board_count']}板")
            print(f"        所属行业: {stock['sector']}")
    else:
        print(f"   - ⚠️  未找到符合条件的龙头股票")
else:
    dragon_stocks = []
    print(f"   - ⚠️  无法获取涨停板数据，跳过选股")

# ========== 5. 从MongoDB读取notebook的实际输出（如果存在） ==========
print("\n5. 从MongoDB读取notebook的实际输出（对比）")
print("-" * 80)

try:
    from config.config_manager import get_config_manager
    from pymongo import MongoClient
    
    cm = get_config_manager()
    mongo_config = cm.get_config('mongodb')
    
    client = MongoClient(
        host=mongo_config.get('host', 'localhost'),
        port=mongo_config.get('port', 27017),
        username=mongo_config.get('username'),
        password=mongo_config.get('password')
    )
    db = client[mongo_config.get('database', 'jqquant')]
    collection = db['notebook_results']
    
    # 查找1月14日的01_notebook结果
    notebook01_result = collection.find_one({
        'notebook_name': '01_market_environment_judgment',
        'timestamp': {'$regex': '20260114'}
    }, sort=[('timestamp', -1)])
    
    if notebook01_result:
        print(f"   ✅ 找到01_notebook的结果（时间戳: {notebook01_result.get('timestamp', 'N/A')}）")
        
        # 提取情绪周期判断结果
        if 'result' in notebook01_result:
            nb_result = notebook01_result['result']
            if isinstance(nb_result, dict):
                nb_cycle = nb_result.get('cycle', 'N/A')
                nb_position = nb_result.get('position', 'N/A')
                nb_strategy = nb_result.get('strategy', 'N/A')
                
                print(f"   Notebook输出:")
                print(f"   - 情绪周期: {nb_cycle}")
                print(f"   - 建议仓位: {nb_position}")
                print(f"   - 推荐策略: {nb_strategy}")
                
                # 对比
                print(f"\n   对比结果:")
                cycle_match = result['cycle'] == nb_cycle
                position_match = result['position'] == nb_position
                strategy_match = result['strategy'] == nb_strategy or nb_strategy in result['strategy']
                
                print(f"   - 情绪周期: {'✅ 一致' if cycle_match else '❌ 不一致'} (库函数: {result['cycle']}, Notebook: {nb_cycle})")
                print(f"   - 建议仓位: {'✅ 一致' if position_match else '❌ 不一致'} (库函数: {result['position']}, Notebook: {nb_position})")
                print(f"   - 推荐策略: {'✅ 一致' if strategy_match else '❌ 不一致'} (库函数: {result['strategy']}, Notebook: {nb_strategy})")
        else:
            print(f"   ⚠️  Notebook结果中未找到'result'字段")
    else:
        print(f"   ⚠️  未找到01_notebook的结果（可能需要先运行notebook）")
    
    # 查找1月14日的02_notebook结果
    notebook02_result = collection.find_one({
        'notebook_name': '02_stock_selection',
        'timestamp': {'$regex': '20260114'}
    }, sort=[('timestamp', -1)])
    
    if notebook02_result:
        print(f"\n   ✅ 找到02_notebook的结果（时间戳: {notebook02_result.get('timestamp', 'N/A')}）")
        
        # 提取选股结果
        if 'result' in notebook02_result:
            nb_result = notebook02_result['result']
            if isinstance(nb_result, dict):
                nb_first_board = nb_result.get('first_board_candidates', [])
                nb_dragon = nb_result.get('dragon_stocks', [])
                
                print(f"   Notebook输出:")
                print(f"   - 首板候选: {len(nb_first_board)}只")
                print(f"   - 龙头股票: {len(nb_dragon)}只")
                
                # 对比首板候选
                if nb_first_board:
                    nb_first_codes = [s.get('代码', s.get('code', '')) for s in nb_first_board[:5]]
                    lib_first_codes = [s['code'] for s in first_board_candidates[:5]]
                    
                    print(f"\n   首板候选对比:")
                    print(f"   - Notebook: {nb_first_codes}")
                    print(f"   - 库函数: {lib_first_codes}")
                    codes_match = set(nb_first_codes) == set(lib_first_codes)
                    print(f"   - 结果: {'✅ 一致' if codes_match else '❌ 不一致'}")
                
                # 对比龙头股票
                if nb_dragon:
                    nb_dragon_codes = [s.get('代码', s.get('code', '')) for s in nb_dragon[:5]]
                    lib_dragon_codes = [s['code'] for s in dragon_stocks[:5]]
                    
                    print(f"\n   龙头股票对比:")
                    print(f"   - Notebook: {nb_dragon_codes}")
                    print(f"   - 库函数: {lib_dragon_codes}")
                    codes_match = set(nb_dragon_codes) == set(lib_dragon_codes)
                    print(f"   - 结果: {'✅ 一致' if codes_match else '❌ 不一致'}")
        else:
            print(f"   ⚠️  Notebook结果中未找到'result'字段")
    else:
        print(f"   ⚠️  未找到02_notebook的结果（可能需要先运行notebook）")
    
    client.close()
    
except Exception as e:
    print(f"   ⚠️  无法连接MongoDB或读取数据: {str(e)[:150]}")

# ========== 6. 输出详细对比报告 ==========
print("\n" + "=" * 80)
print("详细对比报告")
print("=" * 80)

print(f"\n【库函数输出】")
print(f"情绪周期判断:")
print(f"  - 周期: {result['cycle']}")
print(f"  - 仓位: {result['position']}")
print(f"  - 策略: {result['strategy']}")
print(f"  - 涨停家数: {result['limit_up_count']}只")
print(f"  - 最高连板: {result['max_height']}板")
print(f"  - 炸板率: {result['zhaban_rate']:.2f}%")

print(f"\n首板候选股票: {len(first_board_candidates)}只")
if first_board_candidates:
    for i, stock in enumerate(first_board_candidates[:5], 1):
        print(f"  {i}. {stock['code']} {stock['name']} (封板资金占比: {stock['limit_ratio']:.2f}%)")

print(f"\n龙头股票: {len(dragon_stocks)}只")
if dragon_stocks:
    for i, stock in enumerate(dragon_stocks[:5], 1):
        print(f"  {i}. {stock['code']} {stock['name']} (连板数: {stock['board_count']}板)")

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
print("\n💡 提示: 如果MongoDB中没有找到notebook结果，请先运行01和02 notebook，然后再运行此验证脚本")
