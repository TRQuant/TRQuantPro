#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多数据源财经新闻实时抓取演示
==========================
实时演示从多个数据源（eastmoney, sina, cls）抓取财经新闻的过程

功能:
1. 实时显示抓取进度
2. 从多个数据源抓取新闻
3. 显示每个数据源的结果
4. 汇总所有数据源的结果

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


async def fetch_news_from_source(collector, source: str, limit: int = 10):
    """
    从指定数据源抓取新闻（实时显示进度）
    
    Args:
        collector: FinancialCollector实例
        source: 数据源名称
        limit: 抓取数量
    
    Returns:
        CollectorResult: 抓取结果
    """
    print(f"\n{'='*70}")
    print(f"📡 数据源: {source}")
    print(f"{'='*70}")
    
    start_time = datetime.now()
    
    try:
        from core.data_collection.financial_collector import FinancialCollector
        
        source_config = FinancialCollector.NEWS_SOURCES.get(source)
        if not source_config:
            print(f"  ❌ 未知的数据源: {source}")
            return None
        
        print(f"  📋 数据源信息:")
        print(f"     名称: {source_config.get('name', source)}")
        print(f"     URL: {source_config.get('url', 'N/A')}")
        print(f"     数量限制: {limit}条")
        
        print(f"\n  ⏳ 开始抓取...")
        print(f"     正在连接 {source_config.get('name', source)}...")
        
        result = await collector.fetch_news(source, limit=limit)
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        if result and result.success:
            news_list = result.data
            print(f"\n  ✅ 抓取成功！")
            print(f"     耗时: {elapsed_time:.2f}秒")
            print(f"     数据源: {result.source}")
            print(f"     新闻数量: {result.count}/{len(news_list)}")
            
            if news_list:
                print(f"\n  📋 新闻列表（前{min(5, len(news_list))}条）:")
                for i, news in enumerate(news_list[:5], 1):
                    title = news.get('title', 'N/A')
                    url = news.get('url', 'N/A')
                    date = news.get('publish_time', news.get('date', 'N/A'))
                    
                    print(f"\n     [{i}] {title[:55]}...")
                    print(f"         链接: {url[:70]}...")
                    if date:
                        print(f"         时间: {date}")
                
                if len(news_list) > 5:
                    print(f"\n     ... 还有 {len(news_list) - 5} 条新闻")
            else:
                print(f"\n  ⚠️  抓取成功但无新闻数据")
            
            return result
        else:
            error_msg = result.error if result else "未知错误"
            print(f"\n  ❌ 抓取失败")
            print(f"     错误: {error_msg}")
            print(f"     耗时: {elapsed_time:.2f}秒")
            return result
            
    except Exception as e:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        print(f"\n  ❌ 抓取异常")
        print(f"     错误: {str(e)[:100]}")
        print(f"     耗时: {elapsed_time:.2f}秒")
        import traceback
        traceback.print_exc()
        return None


async def demo_multi_source_news_live():
    """实时演示从多个数据源抓取财经新闻"""
    print("=" * 70)
    print("📰 多数据源财经新闻实时抓取演示")
    print("=" * 70)
    
    # 支持的数据源
    sources = ["eastmoney", "sina", "cls"]
    
    # 显示支持的数据源信息
    print("\n📋 支持的数据源:")
    try:
        from core.data_collection.financial_collector import FinancialCollector
        
        for source_id in sources:
            source_config = FinancialCollector.NEWS_SOURCES.get(source_id)
            if source_config:
                name = source_config.get('name', source_id)
                url = source_config.get('url', 'N/A')
                status = "✅ 已实现" if source_id == "eastmoney" else "⚠️  通用解析（可能不够精确）"
                print(f"  - {source_id} ({name}): {status}")
                print(f"    URL: {url}")
    except Exception as e:
        print(f"  ❌ 获取数据源配置失败: {e}")
    
    all_results = {}
    all_news = []
    
    try:
        from core.data_collection import FinancialCollector
        
        print(f"\n🔧 初始化FinancialCollector...")
        print(f"   浏览器模式: headless=True")
        
        async with FinancialCollector(headless=True) as collector:
            # 从每个数据源抓取
            for source in sources:
                result = await fetch_news_from_source(collector, source, limit=10)
                all_results[source] = result
                
                if result and result.success and result.data:
                    all_news.extend(result.data)
                
                # 短暂延迟，避免请求过快
                if source != sources[-1]:  # 最后一个不需要延迟
                    await asyncio.sleep(1)
        
        # 汇总结果
        print("\n" + "=" * 70)
        print("📊 多数据源抓取汇总")
        print("=" * 70)
        
        total_news = 0
        successful_sources = 0
        
        for source, result in all_results.items():
            if result and result.success:
                count = result.count if result.count > 0 else len(result.data) if result.data else 0
                total_news += count
                successful_sources += 1
                print(f"\n✅ {source}: 成功抓取 {count} 条新闻")
            else:
                error_msg = result.error if result else "未实现或异常"
                print(f"\n❌ {source}: 抓取失败 ({error_msg[:50]})")
        
        # 去重汇总
        if all_news:
            seen_titles = set()
            unique_news = []
            for news in all_news:
                title = news.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    unique_news.append(news)
            
            print(f"\n📊 汇总统计:")
            print(f"   成功数据源: {successful_sources}/{len(sources)}")
            print(f"   总新闻数（未去重）: {total_news}")
            print(f"   去重后新闻数: {len(unique_news)}")
            
            # 按数据源统计
            source_counts = {}
            for news in unique_news:
                source = news.get('source', 'unknown')
                source_counts[source] = source_counts.get(source, 0) + 1
            
            print(f"\n📋 数据源分布:")
            for source, count in source_counts.items():
                print(f"   - {source}: {count} 条")
        else:
            print(f"\n⚠️  未抓取到任何新闻")
        
        return {
            "results": all_results,
            "all_news": all_news,
            "unique_news": unique_news if all_news else []
        }
        
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """主函数"""
    summary = await demo_multi_source_news_live()
    
    print("\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    
    if summary:
        unique_news = summary.get("unique_news", [])
        if unique_news:
            print(f"\n💡 提示:")
            print(f"  - 共从 {len(summary['results'])} 个数据源抓取新闻")
            print(f"  - 去重后共 {len(unique_news)} 条新闻")
            print(f"  - 可以使用这些数据生成投资热点报告")
        else:
            print(f"\n⚠️  未抓取到新闻数据")
            print(f"  - 可能是因为某些数据源的解析逻辑需要优化")
            print(f"  - 目前eastmoney数据源最稳定")
    else:
        print(f"\n❌ 演示失败")


if __name__ == "__main__":
    asyncio.run(main())
