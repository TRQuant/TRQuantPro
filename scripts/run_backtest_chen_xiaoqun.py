#!/usr/bin/env python3
"""
运行陈小群战法回测（使用缓存，不重复抓取数据）

直接从notebook中提取关键代码并执行
"""

import sys
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# 添加项目根目录
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("=" * 80)
print("陈小群战法回测执行")
print("=" * 80)
print(f"项目根目录: {project_root}")
print(f"缓存目录: {project_root / 'data' / 'backtest_cache'}")

# 检查缓存
cache_file = project_root / 'data' / 'backtest_cache' / 'chen_xiaoqun_market_data.json'
if cache_file.exists():
    with open(cache_file, 'r') as f:
        cache_data = json.load(f)
    print(f"\n✅ 缓存文件存在: {len(cache_data)}天数据")
    print(f"   日期范围: {sorted(cache_data.keys())[0]} ~ {sorted(cache_data.keys())[-1]}")
else:
    print(f"\n⚠️  缓存文件不存在，将创建新缓存")

print("\n" + "=" * 80)
print("开始执行回测...")
print("=" * 80)
print("\n💡 提示: 回测将使用缓存数据，不会重复抓取")
print("   如果需要重新抓取数据，请删除缓存文件后重新运行")
print("\n执行notebook中的回测代码...\n")

# 执行notebook的关键部分
exec(open(project_root / 'notebooks' / 'research' / 'chen_xiaoqun_strategy' / '04_backtest_validation.ipynb').read())
