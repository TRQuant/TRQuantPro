#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 知识库批量爬取工具
========================

根据PDF方案，批量爬取多个平台的文档：
- 聚宽 (JoinQuant)
- BulletTrade
- PTrade
- QMT

运行: python scripts/kb/kb_batch_crawl.py --platform <平台名>
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
import time

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('KBBatchCrawler')

# 导入知识库爬虫
from scripts.kb.kb_crawler import KnowledgeCrawler

# 平台URL配置
PLATFORM_URLS = {
    "JoinQuant": [
        "https://www.joinquant.com/help/api",
        "https://www.joinquant.com/help/document/",
        "https://www.joinquant.com/help/faq",
    ],
    "BulletTrade": [
        "https://github.com/bullettrade/bullettrade",
        "https://www.cnblogs.com/bullettrade/p/19308512",
    ],
    "PTrade": [
        "https://ptradeapi.com/",
    ],
    "QMT": [
        "http://qmt.ptradeapi.com/",  # QMT文档
        "https://dict.thinktrader.net/",  # QMT官方文档
        "https://dict.thinktrader.net/nativeApi/",  # xtquant API文档
        "https://www.cnblogs.com/bigleft/p/18286458",  # QMT量化交易系统介绍
    ]
}


def crawl_platform(platform: str, urls: List[str], method: str = "playwright") -> Dict[str, Any]:
    """
    爬取指定平台的所有URL
    
    Args:
        platform: 平台名称
        urls: URL列表
        method: 爬取方法
        
    Returns:
        爬取结果统计
    """
    crawler = KnowledgeCrawler()
    
    stats = {
        "platform": platform,
        "total_urls": len(urls),
        "success": 0,
        "failed": 0,
        "kb_ids": []
    }
    
    print(f"\n{'='*70}")
    print(f"🕷️ 开始爬取 {platform} 平台文档")
    print(f"{'='*70}")
    print(f"共 {len(urls)} 个URL")
    print()
    
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] 爬取: {url}")
        
        try:
            kb_ids = crawler.crawl_and_save(
                url=url,
                platform=platform,
                method=method
            )
            
            if kb_ids:
                stats["success"] += 1
                stats["kb_ids"].extend(kb_ids)
                print(f"   ✅ 成功添加 {len(kb_ids)} 条知识条目")
            else:
                stats["failed"] += 1
                print(f"   ❌ 失败")
            
            # 延迟，避免请求过快
            if idx < len(urls):
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"爬取失败: {url}, 错误: {e}")
            stats["failed"] += 1
    
    return stats


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="TRQuant 知识库批量爬取工具")
    parser.add_argument(
        "--platform",
        type=str,
        choices=list(PLATFORM_URLS.keys()) + ["all"],
        default="all",
        help="平台名称（JoinQuant/BulletTrade/PTrade/QMT/all）"
    )
    parser.add_argument(
        "--method",
        type=str,
        default="playwright",
        choices=["playwright", "mcp"],
        help="爬取方法"
    )
    parser.add_argument(
        "--build-index",
        action="store_true",
        help="爬取后构建向量索引"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("TRQuant 知识库批量爬取工具")
    print("=" * 70)
    print()
    
    crawler = KnowledgeCrawler()
    all_stats = []
    
    # 确定要爬取的平台
    if args.platform == "all":
        platforms_to_crawl = list(PLATFORM_URLS.keys())
    else:
        platforms_to_crawl = [args.platform]
    
    # 爬取每个平台
    for platform in platforms_to_crawl:
        urls = PLATFORM_URLS.get(platform, [])
        if not urls:
            logger.warning(f"平台 {platform} 没有配置URL")
            continue
        
        stats = crawl_platform(platform, urls, method=args.method)
        all_stats.append(stats)
    
    # 汇总统计
    print()
    print("=" * 70)
    print("📊 爬取统计")
    print("=" * 70)
    
    total_success = 0
    total_failed = 0
    total_kb_ids = []
    
    for stats in all_stats:
        print(f"\n{stats['platform']}:")
        print(f"  总URL数: {stats['total_urls']}")
        print(f"  成功: {stats['success']}")
        print(f"  失败: {stats['failed']}")
        print(f"  知识条目: {len(stats['kb_ids'])} 条")
        
        total_success += stats['success']
        total_failed += stats['failed']
        total_kb_ids.extend(stats['kb_ids'])
    
    print()
    print(f"总计:")
    print(f"  成功: {total_success} 个URL")
    print(f"  失败: {total_failed} 个URL")
    print(f"  知识条目: {len(total_kb_ids)} 条")
    
    # 构建向量索引
    if args.build_index and total_kb_ids:
        print()
        print("🔨 构建向量索引...")
        result = crawler.builder.build_vector_index(force_rebuild=False)
        if result.get("success"):
            print(f"✅ 向量索引构建成功")
            print(f"   - 条目数: {result.get('items_count', 0)}")
            print(f"   - 模型: {result.get('model', '')}")
        else:
            print(f"❌ 向量索引构建失败: {result.get('error', 'Unknown error')}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
