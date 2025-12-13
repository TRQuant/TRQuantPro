"""
数据收集工具包
整合开源工具，实现知识库数据自动收集
"""

from .web_crawler import WebCrawler
from .pdf_downloader import PDFDownloader
from .academic_scraper import AcademicScraper
from .source_recommender import SourceRecommender

__all__ = [
    'WebCrawler',
    'PDFDownloader',
    'AcademicScraper',
    'SourceRecommender',
]

