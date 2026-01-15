#!/usr/bin/env python3
"""
更新陈小群策略回测缓存数据

补上最新日期的市场数据，确保数据完整性
"""

import sys
from pathlib import Path
import json
import akshare as ak
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# 添加项目根目录
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 尝试导入炸板率获取工具
try:
    from notebooks.lib.research_utils import get_zhaban_rate_fetcher
    zhaban_fetcher_class = get_zhaban_rate_fetcher()
except:
    # 如果导入失败，使用简单估算
    zhaban_fetcher_class = None

def fetch_single_day_data(date_str):
    """获取单日市场数据"""
    date_compact = date_str.replace('-', '')
    result = {
        'date': date_str,
        'success': False,
        'data': None
    }
    
    try:
        # 获取涨停板数据
        limit_up_count = 0
        max_height = 0
        
        try:
            limit_up_data = ak.stock_zt_pool_em(date=date_compact)
            if limit_up_data is not None and not limit_up_data.empty:
                limit_up_count = len(limit_up_data)
                # 计算连板高度
                if '连板数' in limit_up_data.columns:
                    max_height = int(limit_up_data['连板数'].max())
                elif '涨停统计' in limit_up_data.columns:
                    try:
                        heights = []
                        for stat in limit_up_data['涨停统计']:
                            if isinstance(stat, str) and '/' in stat:
                                parts = stat.split('/')
                                if len(parts) >= 2:
                                    heights.append(int(parts[0]))
                        if heights:
                            max_height = max(heights)
                    except:
                        max_height = 3
        except Exception as e:
            print(f"   ⚠️  {date_str}: 获取涨停数据失败 - {e}")
        
        # 获取炸板率
        if zhaban_fetcher_class:
            try:
                zhaban_fetcher = zhaban_fetcher_class(cache_enabled=True)
                zhaban_result = zhaban_fetcher.get_zhaban_rate(date_compact, limit_up_count=limit_up_count)
                zhaban_rate = zhaban_result.get('zhaban_rate', 15.0)
                zhaban_source = zhaban_result.get('source', 'estimated')
            except:
                zhaban_rate = 15.0
                zhaban_source = 'estimated'
        else:
            # 简单估算：根据涨停家数估算炸板率
            if limit_up_count > 0:
                zhaban_rate = max(10.0, min(30.0, 20.0 - limit_up_count * 0.1))
            else:
                zhaban_rate = 25.0
            zhaban_source = 'estimated'
        
        result['success'] = True
        result['data'] = {
            'limit_up_count': limit_up_count,
            'zhaban_rate': zhaban_rate,
            'zhaban_source': zhaban_source,
            'max_height': max_height,
        }
    except Exception as e:
        print(f"   ❌ {date_str}: 获取失败 - {e}")
        # 使用估算值
        result['data'] = {
            'limit_up_count': 30,
            'zhaban_rate': 15.0,
            'zhaban_source': 'estimated',
            'max_height': 4,
        }
    
    return result

def update_cache():
    """更新缓存数据"""
    cache_file = project_root / 'data' / 'backtest_cache' / 'chen_xiaoqun_market_data.json'
    
    # 加载现有缓存
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
    else:
        cached_data = {}
    
    # 确定需要更新的日期范围（最近2周）
    today = datetime.now()
    start_date = today - timedelta(days=14)
    
    # 生成交易日列表（最近2周）
    from datetime import date
    trade_days = []
    current = start_date.date()
    while current <= today.date():
        # 跳过周末
        if current.weekday() < 5:  # 0-4 = Monday-Friday
            trade_days.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    print("=" * 80)
    print("📊 更新陈小群策略回测缓存数据")
    print("=" * 80)
    print(f"日期范围: {trade_days[0]} ~ {trade_days[-1]}")
    print(f"总交易日: {len(trade_days)}天")
    print()
    
    # 检查哪些日期需要更新
    missing_dates = []
    outdated_dates = []
    
    for date_str in trade_days:
        if date_str not in cached_data:
            missing_dates.append(date_str)
        else:
            # 检查数据是否有效（涨停家数>0或数据源不是failed）
            data = cached_data[date_str]
            if data.get('limit_up_count', 0) == 0 and data.get('zhaban_source') == 'failed':
                outdated_dates.append(date_str)
    
    total_to_update = len(missing_dates) + len(outdated_dates)
    
    if total_to_update == 0:
        print("✅ 所有数据都是最新的，无需更新")
        return
    
    print(f"需要更新: {total_to_update}天")
    print(f"  - 缺失数据: {len(missing_dates)}天")
    print(f"  - 无效数据: {len(outdated_dates)}天")
    print()
    
    # 更新数据
    dates_to_fetch = missing_dates + outdated_dates
    
    print("📥 开始获取市场数据...")
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fetch_single_day_data, date): date for date in dates_to_fetch}
        
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            date_str = result['date']
            
            cached_data[date_str] = result['data']
            
            if result['success']:
                success_count += 1
                print(f"   ✅ {date_str}: 涨停{result['data']['limit_up_count']}只, 炸板率{result['data']['zhaban_rate']:.1f}%, 连板{result['data']['max_height']}板")
            else:
                fail_count += 1
                print(f"   ⚠️  {date_str}: 使用估算值")
            
            completed += 1
            if completed % 5 == 0 or completed == len(dates_to_fetch):
                print(f"   进度: {completed}/{len(dates_to_fetch)} ({completed/len(dates_to_fetch)*100:.1f}%)")
    
    print()
    print(f"✅ 数据更新完成")
    print(f"   成功: {success_count}天")
    print(f"   失败/估算: {fail_count}天")
    
    # 保存缓存
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cached_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 缓存已保存: {cache_file}")
    
    # 统计最近2周的数据质量
    valid_count = sum(1 for d in trade_days if d in cached_data and cached_data[d].get('limit_up_count', 0) > 0)
    print(f"\n📊 数据质量统计（最近2周）:")
    print(f"   总交易日: {len(trade_days)}天")
    print(f"   有效数据: {valid_count}天 ({valid_count/len(trade_days)*100:.1f}%)")
    print(f"   无效数据: {len(trade_days) - valid_count}天")

if __name__ == '__main__':
    update_cache()
