#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API文档爬取启动脚本
用于后台运行完整爬取
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import scripts.crawl_jqdata_final_optimized as crawler

# 完整爬取配置
crawler.CONFIG["max_pages"] = 200  # 爬取200页（覆盖所有JQData文档）
crawler.CONFIG["rate_limit_delay"] = 2  # 2秒间隔
crawler.CONFIG["progress_save_interval"] = 10  # 每10页保存
crawler.CONFIG["retry_times"] = 3  # 重试3次

def main():
    print("=" * 70)
    print(f"🚀 聚宽API文档完整爬取")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print(f"配置:")
    print(f"  - 最大页面数: {crawler.CONFIG['max_pages']}")
    print(f"  - 请求间隔: {crawler.CONFIG['rate_limit_delay']}秒")
    print(f"  - 进度保存间隔: {crawler.CONFIG['progress_save_interval']}页")
    print("=" * 70)
    print()
    
    asyncio.run(crawler.main())
    
    print()
    print("=" * 70)
    print(f"✅ 爬取完成")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()

