#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
财经数据收集器实时演示脚本
==========================
实时演示FinancialCollector从多个数据源抓取财经新闻的过程

支持的数据源:
1. eastmoney (东方财富) - 已实现
2. sina (新浪财经) - 已配置，待实现
3. cls (财联社) - 已配置，待实现

作者: TRQuant Team
日期: 2026-01-11
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


async def demo_fetch_news_live(source: str = "eastmoney", limit: int = 10):
    """
    实时演示从指定数据源抓取财经新闻
    
    Args:
        source: 数据源名称 (eastmoney/sina/cls)
        limit: 抓取数量
    """
    print("\n" + "=" * 70)
    print(f"📰 实时演示：从 {source} 抓取财经新闻")
    print("=" * 70)
    
    try:
        from core.data_collection import FinancialCollector
        
        print(f"\n🔧 初始化FinancialCollector...")
        print(f"   数据源: {source}")
        print(f"   数量限制: {limit}条")
        print(f"   浏览器模式: headless=True")
        
        async with FinancialCollector(headless=True) as collector:
            print(f"\n⏳ 开始抓取新闻...")
            print(f"   正在连接 {source}...")
            
            # 实时显示抓取过程
            start_time = datetime.now()
            
            result = await collector.fetch_news(source, limit=limit)
            
            elapsed_time = (datetime.now() - start_time).total_seconds()
            
            if result.success:
                news_list = result.data
                print(f"\n✅ 抓取成功！")
                print(f"   耗时: {elapsed_time:.2f}秒")
                print(f"   数据源: {result.source}")
                print(f"   新闻数量: {result.count}/{len(news_list)}")
                
                print(f"\n📋 新闻列表:")
                print("-" * 70)
                for i, news in enumerate(news_list, 1):
                    title = news.get('title', 'N/A')
                    url = news.get('url', 'N/A')
                    date = news.get('publish_time', news.get('date', 'N/A'))
                    
                    print(f"\n[{i}] {title[:60]}...")
                    print(f"    链接: {url[:80]}...")
                    print(f"    时间: {date}")
                    if i >= 5:  # 只显示前5条
                        print(f"\n    ... 还有 {len(news_list) - 5} 条新闻")
                        break
                
                print("\n" + "-" * 70)
                print(f"✅ 共抓取 {len(news_list)} 条新闻")
                
                return result
            else:
                print(f"\n❌ 抓取失败: {result.error}")
                return result
                
    except Exception as e:
        print(f"\n❌ 抓取异常: {e}")
        import traceback
        traceback.print_exc()
        return None


async def demo_multi_source_live():
    """实时演示从多个数据源抓取财经新闻"""
    print("\n" + "=" * 70)
    print("📰 实时演示：从多个数据源抓取财经新闻")
    print("=" * 70)
    
    # 支持的数据源
    sources = ["eastmoney", "sina", "cls"]
    
    all_results = {}
    
    for source in sources:
        print(f"\n{'='*70}")
        print(f"📰 数据源: {source}")
        print(f"{'='*70}")
        
        try:
            result = await demo_fetch_news_live(source, limit=5)
            all_results[source] = result
        except Exception as e:
            print(f"❌ {source} 抓取失败: {e}")
            all_results[source] = None
        
        # 短暂延迟，避免请求过快
        await asyncio.sleep(1)
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 多数据源抓取汇总")
    print("=" * 70)
    
    for source, result in all_results.items():
        if result and result.success:
            print(f"\n✅ {source}: 成功抓取 {result.count} 条新闻")
        else:
            error_msg = result.error if result else "未实现"
            print(f"\n❌ {source}: 抓取失败 ({error_msg})")
    
    return all_results


async def demo_collector_status():
    """显示FinancialCollector支持的数据源"""
    print("\n" + "=" * 70)
    print("📋 FinancialCollector支持的数据源")
    print("=" * 70)
    
    try:
        from core.data_collection.financial_collector import FinancialCollector
        
        print("\n📰 新闻数据源:")
        for source_id, source_config in FinancialCollector.NEWS_SOURCES.items():
            name = source_config.get('name', source_id)
            url = source_config.get('url', 'N/A')
            status = "✅ 已实现" if source_id == "eastmoney" else "⚠️  待实现"
            print(f"  - {source_id} ({name})")
            print(f"    URL: {url}")
            print(f"    状态: {status}")
            print()
        
        print("\n📢 公告数据源:")
        for source_id, source_config in FinancialCollector.ANNOUNCEMENT_SOURCES.items():
            name = source_config.get('name', source_id)
            url = source_config.get('url', 'N/A')
            status = "✅ 已实现" if source_id == "eastmoney" else "⚠️  待实现"
            print(f"  - {source_id} ({name})")
            print(f"    URL: {url}")
            print(f"    状态: {status}")
            print()
        
    except Exception as e:
        print(f"❌ 获取数据源配置失败: {e}")


async def main():
    """主函数"""
    print("=" * 70)
    print("财经数据收集器实时演示")
    print("=" * 70)
    
    # 1. 显示支持的数据源
    await demo_collector_status()
    
    # 2. 实时演示从eastmoney抓取
    print("\n" + "=" * 70)
    print("实时演示：从eastmoney抓取财经新闻")
    print("=" * 70)
    
    result = await demo_fetch_news_live("eastmoney", limit=10)
    
    # 3. 多数据源演示（可选）
    print("\n" + "=" * 70)
    user_input = input("\n是否尝试从其他数据源抓取？(y/n): ")
    if user_input.lower() == 'y':
        await demo_multi_source_live()
    
    print("\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n💡 提示:")
    print("  - FinancialCollector目前只实现了eastmoney数据源")
    print("  - sina和cls数据源已配置，但抓取逻辑待实现")
    print("  - 可以根据需要添加更多数据源的实现")


if __name__ == "__main__":
    asyncio.run(main())
