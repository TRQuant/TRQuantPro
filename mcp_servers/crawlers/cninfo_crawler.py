# -*- coding: utf-8 -*-
"""巨潮资讯网爬虫"""

import re
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .base_crawler import BaseCrawler, CrawlResult, register_crawler

logger = logging.getLogger(__name__)

@dataclass
class Announcement:
    ann_id: str
    security_code: str
    security_name: str
    title: str
    publish_date: datetime
    ann_type: str
    download_url: str
    content: str = ""
    
    def to_dict(self):
        return {
            "ann_id": self.ann_id,
            "security_id": f"{self.security_code}.SZ" if self.security_code.startswith(('0', '3')) else f"{self.security_code}.SH",
            "security_code": self.security_code,
            "security_name": self.security_name,
            "title": self.title,
            "publish_date": self.publish_date.strftime("%Y-%m-%d") if self.publish_date else None,
            "doc_type": self.ann_type,
            "download_url": self.download_url,
            "content": self.content,
            "metadata": {"source": "cninfo", "crawl_time": datetime.now().isoformat()}
        }

class CninfoCrawler(BaseCrawler):
    API_BASE = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    DOWNLOAD_BASE = "http://static.cninfo.com.cn/"
    
    def __init__(self, delay_range: tuple = (1.5, 3.0)):
        super().__init__(name="cninfo", base_url="http://www.cninfo.com.cn", delay_range=delay_range)
        self.type_mapping = {
            "annual": "category_ndbg_szsh",
            "semi": "category_bndbg_szsh",
            "quarterly": "category_jibg_szsh",
            "profit": "category_yjyg_szsh",
            "major": "category_zdsx_szsh",
        }

    def _normalize_code(self, stock_code: Optional[str]) -> str:
        if not stock_code:
            return ""
        return str(stock_code).replace(".SZ", "").replace(".SH", "").strip()

    def _infer_column(self, stock_code: Optional[str]) -> str:
        code = self._normalize_code(stock_code)
        if code.startswith("6"):
            return "sse"
        return "szse"

    def _resolve_org_id(self, stock_code: str) -> Optional[str]:
        """
        cninfo 的 hisAnnouncement/query 接口在按股票过滤时通常需要 "secCode,orgId" 的格式。
        我们用 searchkey 先查到 orgId。
        """
        code = self._normalize_code(stock_code)
        if not code:
            return None

        payload = {
            "pageNum": 1,
            "pageSize": 10,
            "column": self._infer_column(code),
            "tabName": "fulltext",
            "plate": "",
            "stock": "",
            "searchkey": code,
            "secid": "",
            "category": "",
            "trade": "",
            "seDate": "",
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }
        res = self.post_sync(self.API_BASE, data=payload)
        if not res.success or not res.content:
            return None
        try:
            data = json.loads(res.content)
            anns = data.get("announcements") or []
            for item in anns:
                if str(item.get("secCode", "")).strip() == code and item.get("orgId"):
                    return str(item.get("orgId")).strip()
        except Exception:
            return None
        return None
    
    def build_url(self, **kwargs) -> str:
        return self.API_BASE
    
    def fetch_announcements(self, stock_code: str = None, ann_type: str = None,
                           start_date: str = None, end_date: str = None,
                           page: int = 1, page_size: int = 30) -> List[Dict[str, Any]]:
        if ann_type and ann_type in self.type_mapping:
            ann_type = self.type_mapping[ann_type]
        
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        column = self._infer_column(stock_code)

        # cninfo 按股票过滤时通常需要 "secCode,orgId" 格式
        stock_param = stock_code or ""
        if stock_code:
            code = self._normalize_code(stock_code)
            if code.isdigit() and "," not in code:
                org_id = self._resolve_org_id(code)
                if org_id:
                    stock_param = f"{code},{org_id}"

        params = {
            "pageNum": page, "pageSize": page_size, "column": column,
            "tabName": "fulltext", "plate": "", "stock": stock_code or "",
            "searchkey": "", "secid": "", "category": ann_type or "",
            "trade": "", "seDate": f"{start_date}~{end_date}",
            "sortName": "", "sortType": "", "isHLtitle": "true"
        }

        params["stock"] = stock_param
        
        result = self.post_sync(self.API_BASE, data=params)
        if not result.success:
            return []
        return self.parse_content(result.content)
    
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        announcements = []
        try:
            data = json.loads(content)
            if not data.get("announcements"):
                return []
            for item in data["announcements"]:
                try:
                    ann = Announcement(
                        ann_id=item.get("announcementId", ""),
                        security_code=item.get("secCode", ""),
                        security_name=item.get("secName", ""),
                        title=re.sub(r'<em>|</em>', '', item.get("announcementTitle", "")),
                        publish_date=datetime.fromtimestamp(item.get("announcementTime", 0) / 1000) if item.get("announcementTime") else None,
                        ann_type=item.get("announcementTypeName", "other"),
                        download_url=f"{self.DOWNLOAD_BASE}{item.get('adjunctUrl', '')}"
                    )
                    announcements.append(ann.to_dict())
                except Exception as e:
                    continue
        except Exception as e:
            logger.error(f"解析失败: {e}")
        return announcements
    
    def get_stock_announcements(self, stock_code: str, days: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.fetch_announcements(stock_code=stock_code, start_date=start_date, end_date=end_date, page=page)

_cninfo_crawler = None

def get_cninfo_crawler() -> CninfoCrawler:
    global _cninfo_crawler
    if _cninfo_crawler is None:
        _cninfo_crawler = CninfoCrawler()
        register_crawler("cninfo", _cninfo_crawler)
    return _cninfo_crawler
