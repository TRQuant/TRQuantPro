#!/usr/bin/env python3
"""
测试炸板率历史数据获取工具

测试内容：
1. 单日数据获取
2. 批量数据获取
3. 数据格式验证
4. 错误处理
5. 缓存功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.market_data.zhaban_rate_fetcher import (
    get_zhaban_rate,
    get_historical_zhaban_rates,
    ZhabanRateFetcher
)
from datetime import datetime, timedelta

def test_single_date():
    """测试单日数据获取"""
    print("=" * 80)
    print("📊 测试1: 单日数据获取")
    print("=" * 80)
    
    # 测试今日数据
    today = datetime.now().strftime('%Y%m%d')
    print(f"\n测试日期: {today}")
    
    try:
        result = get_zhaban_rate(today, limit_up_count=100)
        
        print(f"\n✅ 获取成功！")
        print(f"   日期: {result['date']}")
        print(f"   炸板数量: {result['zhaban_count']}只")
        print(f"   涨停成功: {result['limit_up_count']}只")
        print(f"   总尝试数: {result['total_attempts']}只")
        print(f"   炸板率: {result['zhaban_rate']:.2f}%")
        print(f"   数据来源: {result['source']}")
        print(f"   成功标志: {result['success']}")
        
        # 验证数据格式
        assert 'date' in result
        assert 'zhaban_count' in result
        assert 'zhaban_rate' in result
        assert 'source' in result
        assert 'success' in result
        print(f"\n✅ 数据格式验证通过")
        
        return True
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_historical_date():
    """测试历史日期数据获取"""
    print("\n" + "=" * 80)
    print("📊 测试2: 历史日期数据获取")
    print("=" * 80)
    
    # 测试一周前的数据
    test_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    print(f"\n测试日期: {test_date} (7天前)")
    
    try:
        result = get_zhaban_rate(test_date, limit_up_count=80)
        
        print(f"\n✅ 获取成功！")
        print(f"   日期: {result['date']}")
        print(f"   炸板数量: {result['zhaban_count']}只")
        print(f"   涨停成功: {result['limit_up_count']}只")
        print(f"   炸板率: {result['zhaban_rate']:.2f}%")
        print(f"   数据来源: {result['source']}")
        
        # 检查数据来源
        if result['source'] == 'estimated':
            print(f"\n⚠️  注意: 使用了估算值（历史数据可能不可用）")
        elif result['source'] == 'akshare':
            print(f"\n✅ 成功获取真实历史数据")
        
        return True
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_fetch():
    """测试批量数据获取"""
    print("\n" + "=" * 80)
    print("📊 测试3: 批量数据获取（最近5个交易日）")
    print("=" * 80)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # 最近7天（包含周末）
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    print(f"\n日期范围: {start_str} ~ {end_str}")
    print("正在获取数据（可能需要几秒钟）...")
    
    try:
        df = get_historical_zhaban_rates(
            start_date=start_str,
            end_date=end_str,
            delay_between_requests=0.3  # 请求间隔0.3秒
        )
        
        if df.empty:
            print(f"\n⚠️  未获取到数据")
            return False
        
        print(f"\n✅ 批量获取成功！")
        print(f"   总记录数: {len(df)}")
        print(f"\n数据预览:")
        print(df.head(10).to_string(index=False))
        
        # 统计信息
        print(f"\n📊 数据统计:")
        print(f"   成功获取: {df['success'].sum()}/{len(df)}")
        print(f"   数据来源分布:")
        source_counts = df['source'].value_counts()
        for source, count in source_counts.items():
            print(f"     {source}: {count}条")
        
        # 炸板率统计
        if 'zhaban_rate' in df.columns:
            valid_rates = df[df['zhaban_rate'] > 0]['zhaban_rate']
            if len(valid_rates) > 0:
                print(f"\n   炸板率统计:")
                print(f"     平均: {valid_rates.mean():.2f}%")
                print(f"     最高: {valid_rates.max():.2f}%")
                print(f"     最低: {valid_rates.min():.2f}%")
        
        return True
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cache():
    """测试缓存功能"""
    print("\n" + "=" * 80)
    print("📊 测试4: 缓存功能")
    print("=" * 80)
    
    fetcher = ZhabanRateFetcher(cache_enabled=True)
    test_date = datetime.now().strftime('%Y%m%d')
    
    print(f"\n测试日期: {test_date}")
    
    try:
        # 第一次获取（应该从API获取）
        import time
        start1 = time.time()
        result1 = fetcher.get_zhaban_rate(test_date, limit_up_count=100)
        time1 = time.time() - start1
        
        print(f"\n第一次获取:")
        print(f"   耗时: {time1:.3f}秒")
        print(f"   数据来源: {result1['source']}")
        
        # 第二次获取（应该从缓存读取）
        start2 = time.time()
        result2 = fetcher.get_zhaban_rate(test_date, limit_up_count=100)
        time2 = time.time() - start2
        
        print(f"\n第二次获取（缓存）:")
        print(f"   耗时: {time2:.3f}秒")
        print(f"   数据来源: {result2['source']}")
        
        # 验证缓存效果
        if time2 < time1:
            print(f"\n✅ 缓存生效！第二次获取更快 ({time2:.3f}s < {time1:.3f}s)")
        else:
            print(f"\n⚠️  缓存可能未生效")
        
        # 验证数据一致性
        if result1['zhaban_rate'] == result2['zhaban_rate']:
            print(f"✅ 缓存数据一致性验证通过")
        else:
            print(f"⚠️  缓存数据不一致")
        
        # 清空缓存测试
        fetcher.clear_cache()
        print(f"\n✅ 缓存已清空")
        
        return True
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 80)
    print("📊 测试5: 错误处理")
    print("=" * 80)
    
    # 测试无效日期
    print(f"\n测试1: 无效日期格式")
    try:
        result = get_zhaban_rate('invalid_date', limit_up_count=100)
        if result['success']:
            print(f"⚠️  意外成功: {result}")
        else:
            print(f"✅ 正确处理无效日期")
    except Exception as e:
        print(f"✅ 正确抛出异常: {type(e).__name__}")
    
    # 测试未来日期
    print(f"\n测试2: 未来日期")
    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
    try:
        result = get_zhaban_rate(future_date, limit_up_count=100)
        print(f"   结果: {result['source']}")
        if result['source'] in ['estimated', 'failed']:
            print(f"✅ 正确处理未来日期")
    except Exception as e:
        print(f"✅ 正确处理异常: {type(e).__name__}")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("🧪 炸板率历史数据获取工具 - 完整测试")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 运行所有测试
    results.append(("单日数据获取", test_single_date()))
    results.append(("历史日期获取", test_historical_date()))
    results.append(("批量数据获取", test_batch_fetch()))
    results.append(("缓存功能", test_cache()))
    results.append(("错误处理", test_error_handling()))
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！工具工作正常。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查。")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
