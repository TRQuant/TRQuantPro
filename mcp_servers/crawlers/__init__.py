# -*- coding: utf-8 -*-
"""TRQuant 爬虫模块"""

from .base_crawler import (
    BaseCrawler, CrawlResult, CrawlTask, CrawlerStatus,
    register_crawler, get_crawler, list_crawlers
)
from .cninfo_crawler import CninfoCrawler, get_cninfo_crawler
from .eastmoney_crawler import EastmoneyCrawler, get_eastmoney_crawler
from .bid_crawler import BidCrawler, get_bid_crawler
from .job_crawler import JobCrawler, get_job_crawler

__all__ = [
    "BaseCrawler", "CrawlResult", "CrawlTask", "CrawlerStatus",
    "register_crawler", "get_crawler", "list_crawlers",
    "CninfoCrawler", "get_cninfo_crawler",
    "EastmoneyCrawler", "get_eastmoney_crawler",
    "BidCrawler", "get_bid_crawler",
    "JobCrawler", "get_job_crawler",
]

# 集成模块
from .crawler_integration import (
    CrawlerIntegration,
    get_crawler_integration,
    crawl_and_store,
    get_integration_status,
    IntegrationResult
)

__all__.extend([
    "CrawlerIntegration",
    "get_crawler_integration", 
    "crawl_and_store",
    "get_integration_status",
    "IntegrationResult"
])

# Event处理模块
from .event_processor import (
    EventProcessor,
    get_event_processor,
    process_new_docs,
    get_processor_status,
    ProcessResult
)

__all__.extend([
    "EventProcessor",
    "get_event_processor",
    "process_new_docs",
    "get_processor_status",
    "ProcessResult"
])

# 端到端管道
from .pipeline import (
    DataPipeline,
    get_pipeline,
    run_pipeline,
    pipeline_status,
    PipelineResult
)

__all__.extend([
    "DataPipeline",
    "get_pipeline",
    "run_pipeline",
    "pipeline_status",
    "PipelineResult"
])
