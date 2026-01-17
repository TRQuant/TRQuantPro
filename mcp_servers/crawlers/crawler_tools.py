# -*- coding: utf-8 -*-
"""爬虫MCP工具 - 完整版"""

from typing import Dict, Any, List

CRAWLER_TOOLS = [
    {"name": "crawler.list", "description": "列出所有可用的爬虫", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "crawler.cninfo.fetch", "description": "从巨潮资讯网爬取公告", "inputSchema": {
        "type": "object", "properties": {
            "stock_code": {"type": "string"}, "ann_type": {"type": "string"},
            "start_date": {"type": "string"}, "end_date": {"type": "string"}, "page": {"type": "integer"}
        }
    }},
    {"name": "crawler.eastmoney.fetch", "description": "从东方财富网爬取公告", "inputSchema": {
        "type": "object", "properties": {
            "stock_code": {"type": "string"}, "days": {"type": "integer"}, "page": {"type": "integer"}
        }
    }},
    {"name": "crawler.eastmoney.research", "description": "从东方财富网爬取研报", "inputSchema": {
        "type": "object", "properties": {"stock_code": {"type": "string"}, "page": {"type": "integer"}}
    }},
    {"name": "crawler.bid.fetch", "description": "获取招标中标数据", "inputSchema": {
        "type": "object", "properties": {
            "keyword": {"type": "string"}, "region": {"type": "string"},
            "page": {"type": "integer"}, "page_size": {"type": "integer"}
        }
    }},
    {"name": "crawler.job.fetch", "description": "获取招聘数据", "inputSchema": {
        "type": "object", "properties": {
            "company_name": {"type": "string"}, "job_type": {"type": "string"}, "page": {"type": "integer"}
        }
    }},
    {"name": "crawler.job.trend", "description": "获取公司招聘趋势", "inputSchema": {
        "type": "object", "properties": {"stock_code": {"type": "string"}, "days": {"type": "integer"}},
        "required": ["stock_code"]
    }},
    {"name": "crawler.stats", "description": "获取爬虫统计信息", "inputSchema": {
        "type": "object", "properties": {"crawler_name": {"type": "string"}}, "required": ["crawler_name"]
    }},
]

async def handle_crawler_list(args: Dict[str, Any]) -> Dict[str, Any]:
    from .base_crawler import list_crawlers
    return {"crawlers": [
        {"name": "cninfo", "description": "巨潮资讯网 - 上市公司公告"},
        {"name": "eastmoney", "description": "东方财富网 - 公告、研报"},
        {"name": "bid", "description": "招标数据 - 中标公告"},
        {"name": "job", "description": "招聘数据 - 岗位信息"},
    ], "registered": list_crawlers()}

async def handle_cninfo_fetch(args: Dict[str, Any]) -> Dict[str, Any]:
    from .cninfo_crawler import get_cninfo_crawler
    crawler = get_cninfo_crawler()
    announcements = crawler.fetch_announcements(
        stock_code=args.get("stock_code"), ann_type=args.get("ann_type"),
        start_date=args.get("start_date"), end_date=args.get("end_date"), page=args.get("page", 1)
    )
    return {"source": "cninfo", "count": len(announcements), "announcements": announcements[:20], "stats": crawler.get_stats()}

async def handle_eastmoney_fetch(args: Dict[str, Any]) -> Dict[str, Any]:
    from .eastmoney_crawler import get_eastmoney_crawler
    crawler = get_eastmoney_crawler()
    announcements = crawler.get_stock_announcements(
        stock_code=args.get("stock_code", ""), days=args.get("days", 30), page=args.get("page", 1)
    )
    return {"source": "eastmoney", "count": len(announcements), "announcements": announcements[:20], "stats": crawler.get_stats()}

async def handle_eastmoney_research(args: Dict[str, Any]) -> Dict[str, Any]:
    from .eastmoney_crawler import get_eastmoney_crawler
    crawler = get_eastmoney_crawler()
    reports = crawler.fetch_research_reports(stock_code=args.get("stock_code"), page=args.get("page", 1))
    return {"source": "eastmoney", "count": len(reports), "reports": reports[:20], "stats": crawler.get_stats()}

async def handle_bid_fetch(args: Dict[str, Any]) -> Dict[str, Any]:
    from .bid_crawler import get_bid_crawler
    crawler = get_bid_crawler()
    bids = crawler.fetch_bids(
        keyword=args.get("keyword"), region=args.get("region"),
        page=args.get("page", 1), page_size=args.get("page_size", 20)
    )
    return {"source": "bid", "count": len(bids), "bids": bids[:20], "stats": crawler.get_stats()}

async def handle_job_fetch(args: Dict[str, Any]) -> Dict[str, Any]:
    from .job_crawler import get_job_crawler
    crawler = get_job_crawler()
    jobs = crawler.fetch_jobs(
        company_name=args.get("company_name"), job_type=args.get("job_type"), page=args.get("page", 1)
    )
    return {"source": "job", "count": len(jobs), "jobs": jobs[:20], "stats": crawler.get_stats()}

async def handle_job_trend(args: Dict[str, Any]) -> Dict[str, Any]:
    from .job_crawler import get_job_crawler
    crawler = get_job_crawler()
    return crawler.get_company_hiring_trend(
        stock_code=args.get("stock_code"), days=args.get("days", 30)
    )

async def handle_crawler_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    crawler_name = args.get("crawler_name", "cninfo")
    if crawler_name == "cninfo":
        from .cninfo_crawler import get_cninfo_crawler
        return get_cninfo_crawler().get_stats()
    elif crawler_name == "eastmoney":
        from .eastmoney_crawler import get_eastmoney_crawler
        return get_eastmoney_crawler().get_stats()
    elif crawler_name == "bid":
        from .bid_crawler import get_bid_crawler
        return get_bid_crawler().get_stats()
    elif crawler_name == "job":
        from .job_crawler import get_job_crawler
        return get_job_crawler().get_stats()
    return {"error": f"未知爬虫: {crawler_name}"}

CRAWLER_HANDLERS = {
    "crawler.list": handle_crawler_list,
    "crawler.cninfo.fetch": handle_cninfo_fetch,
    "crawler.eastmoney.fetch": handle_eastmoney_fetch,
    "crawler.eastmoney.research": handle_eastmoney_research,
    "crawler.bid.fetch": handle_bid_fetch,
    "crawler.job.fetch": handle_job_fetch,
    "crawler.job.trend": handle_job_trend,
    "crawler.stats": handle_crawler_stats,
}
