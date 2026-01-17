#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
陈小群策略知识库增强工具

使用网络搜索和爬取工具获取更多信息，增强知识库
"""

import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入知识库工具
from scripts.import_chen_xiaoqun_knowledge import add_to_strategy_kb, load_strategy_kb, save_strategy_kb

# 关键词列表
SEARCH_KEYWORDS = [
    "陈小群 情绪周期 龙头战法",
    "陈小群 首板卡位术 选股技巧",
    "陈小群 仓位管理 止损止盈",
    "陈小群 游资席位 大连黄河路",
    "陈小群 情绪合力 市场共振",
    "陈小群 打板技巧 涨停板",
    "陈小群 题材轮动 主线识别",
    "陈小群 风险控制 纪律执行",
    "陈小群 复盘方法 交易计划",
    "陈小群 浙江建投 中交地产 案例"
]

# 需要爬取的网站列表
CRAWL_URLS = [
    "https://www.guminchaguan.com/youziwudao/2388.html",  # 股民茶馆
    "https://finance.sina.com.cn/jjxw/2025-12-26/doc-inheautr2809070.shtml",  # 新浪财经
    "https://news.hexun.com/2025-11-02/222108378.html",  # 和讯网
]


def add_web_search_result(title: str, content: str, source: str = None, tags: List[str] = None):
    """添加网络搜索结果到知识库"""
    kb_id = add_to_strategy_kb(
        title=title,
        content=content,
        source_file=source or "web_search",
        tags=tags or ["web_search", "chen_xiaoqun"],
        category="strategy"
    )
    return kb_id


def enhance_with_web_search():
    """使用网络搜索结果增强知识库"""
    print("=" * 80)
    print("开始网络搜索增强知识库")
    print("=" * 80)
    
    # 从之前的web_search结果中提取信息
    search_results = [
        {
            "title": "陈小群投资策略核心 - 情绪周期+龙头战法",
            "content": """
陈小群，95后知名游资，2018年以30万元本金起步，经过高频试错和持续的模式优化：
- 2019年达到百万级别
- 2020年触及千万级别
- 2021年跃上千万级别
- 2022年资金规模突破亿元
- 2023年资产达3亿
- 2025年跃升至近10亿级别

核心策略：情绪周期+龙头战法+极致纪律

投资风格特点：
1. 专注于捕捉市场总龙头
2. 青睐于已经被市场资金高度认可的热门题材股
3. 敢于高位重仓介入
4. 整体以短线波段操作为主
5. 在个股短线震荡调整过程中经常趁机做T
6. 对于部分此前曾重仓博弈的个股，待其股价充分调整之后经常会再度进场博弈

风格演变：
- 开始关注优质赛道的趋势行情
- 采取中长线持股策略
- 打破游资"快进快出"的刻板印象
- 意识到优质赛道的趋势行情持续时间更长，盈利空间更大
            """,
            "tags": ["investment_strategy", "emotion_cycle", "dragon_stock", "growth_timeline"]
        },
        {
            "title": "陈小群交易逻辑详解 - 题材驱动与情绪把控",
            "content": """
核心交易逻辑：

1. 题材驱动，狙击主升浪：
   - 聚焦最强题材：专注于政策利好、产业变革或突发事件催生的主流题材
   - 避免参与杂毛股
   - 龙头战法：重仓参与板块龙头，利用资金优势助推股价，打造市场标杆

2. 情绪周期精准把控：
   - 启动期介入：在题材发酵初期，通过分时弱转强、涨停突破等信号识别龙头启动点
   - 高潮期撤退：当市场情绪过热、跟风股普涨时，逐步兑现利润，避免退潮期风险

3. 盘口语言与资金博弈：
   - 分时承接力：观察盘中抛压与买盘强度，选择分歧转一致的介入时机
   - 席位溢价效应：利用自身影响力吸引跟风资金，形成"小群上车"的市场共识

实战案例：
- 浙江建投（2022年2-4月）：在基建政策利好的背景下，成为市场龙头，通过精准介入实现高额收益
- 中交地产（2023年）：第二波行情中，连续涨停后高位锁仓，待分歧日快速离场
            """,
            "tags": ["trading_logic", "theme_driven", "emotion_control", "case_study"]
        },
        {
            "title": "陈小群策略优化建议 - 提升回报率的关键",
            "content": """
可能导致回报率低的关键原因：

1. 题材选择不当：
   - 未能聚焦于市场最强的主流题材
   - 导致资金效应和市场关注度不足

2. 龙头股把握不足：
   - 未能准确识别并重仓参与板块龙头
   - 错失主升浪行情

3. 情绪周期把控不精准：
   - 未能在题材启动期及时介入
   - 或在高潮期未能及时撤退，导致收益缩水或亏损

改进建议：

1. 优化题材筛选机制：
   - 建立系统的题材筛选标准
   - 关注政策导向、产业趋势和市场热点
   - 确保选择的题材具备足够的市场关注度和资金效应

2. 加强龙头股识别能力：
   - 通过技术分析和基本面研究
   - 识别并重仓参与板块龙头
   - 利用资金优势助推股价上涨

3. 提升情绪周期研判能力：
   - 建立市场情绪监测指标
   - 及时捕捉题材启动信号
   - 在市场情绪高涨时逐步兑现利润
   - 避免退潮期风险
            """,
            "tags": ["strategy_optimization", "return_improvement", "risk_control"]
        }
    ]
    
    # 添加搜索结果
    added_count = 0
    for result in search_results:
        try:
            kb_id = add_web_search_result(
                title=result["title"],
                content=result["content"].strip(),
                source="web_search",
                tags=result["tags"]
            )
            added_count += 1
            print(f"✅ 已添加: {kb_id} - {result['title']}")
        except Exception as e:
            print(f"❌ 添加失败: {result['title']}, 错误: {e}")
    
    print(f"\n✅ 网络搜索增强完成，添加了 {added_count} 条知识")
    return added_count


def enhance_with_keywords():
    """使用关键词搜索增强知识库"""
    print("\n" + "=" * 80)
    print("关键词搜索增强（需要网络爬取工具）")
    print("=" * 80)
    print(f"准备搜索 {len(SEARCH_KEYWORDS)} 个关键词")
    print("\n关键词列表:")
    for i, keyword in enumerate(SEARCH_KEYWORDS, 1):
        print(f"  {i}. {keyword}")
    
    print("\n💡 提示: 可以使用MCP工具进行网络爬取，例如:")
    print("  - crawler_fetch: 基础网页爬取")
    print("  - crawler_selenium_fetch: Selenium爬取（支持JavaScript）")
    print("  - 或使用web_search进行关键词搜索")
    
    return 0


def create_knowledge_summary():
    """创建知识库摘要"""
    kb = load_strategy_kb()
    
    summary = {
        "total_items": kb["stats"]["total"],
        "by_type": kb["stats"]["by_type"],
        "top_tags": dict(sorted(kb["stats"]["by_tag"].items(), key=lambda x: x[1], reverse=True)[:15]),
        "recent_items": [
            {
                "id": item["id"],
                "title": item["title"],
                "type": item["type"],
                "tags": item["tags"][:5]  # 只显示前5个标签
            }
            for item in kb["items"][:10]  # 最近10条
        ]
    }
    
    summary_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "strategy_knowledge" / "summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("知识库摘要")
    print("=" * 80)
    print(f"总条目数: {summary['total_items']}")
    print(f"\n按类型分布:")
    for type_name, count in summary['by_type'].items():
        print(f"  - {type_name}: {count}")
    print(f"\n热门标签 (Top 15):")
    for tag, count in summary['top_tags'].items():
        print(f"  - {tag}: {count}")
    print(f"\n最近添加的条目 (Top 10):")
    for item in summary['recent_items']:
        print(f"  - [{item['type']}] {item['title']} (ID: {item['id']})")
        print(f"    标签: {', '.join(item['tags'])}")
    
    print(f"\n✅ 摘要已保存到: {summary_file}")


def main():
    """主函数"""
    print("=" * 80)
    print("陈小群策略知识库增强工具")
    print("=" * 80)
    
    # 1. 网络搜索增强
    enhance_with_web_search()
    
    # 2. 关键词搜索提示
    enhance_with_keywords()
    
    # 3. 创建知识库摘要
    create_knowledge_summary()
    
    print("\n" + "=" * 80)
    print("增强完成！")
    print("=" * 80)
    print("\n下一步建议:")
    print("1. 使用MCP工具进行网络爬取，获取更多详细信息")
    print("2. 使用knowledge_search搜索知识库内容")
    print("3. 根据搜索结果优化策略代码")


if __name__ == "__main__":
    main()
