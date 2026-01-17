# -*- coding: utf-8 -*-
"""东方财富网爬虫"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .base_crawler import BaseCrawler, register_crawler

logger = logging.getLogger(__name__)

@dataclass
class EastmoneyNews:
    news_id: str
    security_code: str
    security_name: str
    title: str
    publish_date: datetime
    news_type: str
    source: str
    url: str
    content: str = ""
    
    def to_dict(self):
        code = self.security_code.replace("SZ", "").replace("SH", "").strip()
        if code.startswith(('0', '3')):
            security_id = f"{code}.SZ"
        elif code.startswith('6'):
            security_id = f"{code}.SH"
        else:
            security_id = code
        
        return {
            "news_id": self.news_id, "security_id": security_id,
            "security_code": self.security_code, "security_name": self.security_name,
            "title": self.title,
            "publish_date": self.publish_date.strftime("%Y-%m-%d %H:%M:%S") if self.publish_date else None,
            "doc_type": self.news_type, "source": self.source, "url": self.url,
            "content": self.content,
            "metadata": {"source": "eastmoney", "crawl_time": datetime.now().isoformat()}
        }

class EastmoneyCrawler(BaseCrawler):
    ANNOUNCEMENT_API = "https://np-anotice-stock.eastmoney.com/api/security/ann"
    RESEARCH_API = "https://reportapi.eastmoney.com/report/list"
    
    def __init__(self, delay_range: tuple = (1.0, 2.5)):
        super().__init__(name="eastmoney", base_url="https://www.eastmoney.com", delay_range=delay_range)
    
    def build_url(self, **kwargs) -> str:
        return self.ANNOUNCEMENT_API
    
    def _convert_stock_code(self, code: str) -> str:
        code = code.replace(".SZ", "").replace(".SH", "").strip()
        if code.startswith(('0', '3')):
            return f"SZ{code}"
        elif code.startswith('6'):
            return f"SH{code}"
        return code
    
    def fetch_announcements(self, stock_code: str = None, start_date: str = None,
                           end_date: str = None, page: int = 1, page_size: int = 50) -> List[Dict[str, Any]]:
        params = {
            "sr": -1, "page_size": page_size, "page_index": page,
            "ann_type": "A", "client_source": "web", "f_node": 0, "s_node": 0
        }
        if stock_code:
            params["stock_list"] = self._convert_stock_code(stock_code)
        if start_date:
            params["begin_time"] = start_date
        if end_date:
            params["end_time"] = end_date
        
        result = self.fetch_sync(self.ANNOUNCEMENT_API, params=params)
        if not result.success:
            return []
        return self.parse_content(result.content)
    
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        announcements = []
        try:
            data = json.loads(content)
            if not data.get("data", {}).get("list"):
                return []
            for item in data["data"]["list"]:
                try:
                    codes = item.get("codes", [{}])
                    news = EastmoneyNews(
                        news_id=str(item.get("art_code", "")),
                        security_code=codes[0].get("stock_code", "") if codes else "",
                        security_name=codes[0].get("short_name", "") if codes else "",
                        title=item.get("title", ""),
                        publish_date=self._parse_date(item.get("notice_date")),
                        news_type="announcement", source="eastmoney",
                        url=item.get("pdf_url", "")
                    )
                    announcements.append(news.to_dict())
                except Exception as e:
                    continue
        except Exception as e:
            logger.error(f"解析失败: {e}")
        return announcements
    
    def _parse_date(self, date_str) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            if isinstance(date_str, str):
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        continue
            elif isinstance(date_str, (int, float)):
                return datetime.fromtimestamp(date_str / 1000)
        except:
            pass
        return None
    
    def fetch_research_reports(self, stock_code: str = None, page: int = 1, page_size: int = 30) -> List[Dict[str, Any]]:
        params = {
            "industryCode": "*", "pageNo": page, "pageSize": page_size,
            "fields": "", "qType": 0, "_": int(datetime.now().timestamp() * 1000)
        }
        if stock_code:
            params["code"] = stock_code.replace(".SZ", "").replace(".SH", "")
        
        result = self.fetch_sync(self.RESEARCH_API, params=params)
        if not result.success:
            return []
        
        reports = []
        try:
            data = json.loads(result.content)
            for item in data.get("data", []):
                news = EastmoneyNews(
                    news_id=str(item.get("infoCode", "")),
                    security_code=item.get("stockCode", ""),
                    security_name=item.get("stockName", ""),
                    title=item.get("title", ""),
                    publish_date=self._parse_date(item.get("publishDate")),
                    news_type="research", source=item.get("orgSName", "eastmoney"),
                    url=f"https://data.eastmoney.com/report/zw_industry.jshtml?infocode={item.get('infoCode', '')}"
                )
                reports.append(news.to_dict())
        except Exception as e:
            logger.error(f"解析研报失败: {e}")
        return reports
    
    def get_stock_announcements(self, stock_code: str, days: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.fetch_announcements(stock_code=stock_code, start_date=start_date, end_date=end_date, page=page)

_eastmoney_crawler = None

def get_eastmoney_crawler() -> EastmoneyCrawler:
    global _eastmoney_crawler
    if _eastmoney_crawler is None:
        _eastmoney_crawler = EastmoneyCrawler()
        register_crawler("eastmoney", _eastmoney_crawler)
    return _eastmoney_crawler
