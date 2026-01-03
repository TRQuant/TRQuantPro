# -*- coding: utf-8 -*-
"""
招标数据爬虫

数据源：
- 全国公共资源交易平台
- 中国政府采购网
- 各省市招投标平台

采集内容：
- 中标公告
- 招标公告
- 中标金额、项目名称、中标单位
"""

import re
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .base_crawler import BaseCrawler, CrawlResult, register_crawler

logger = logging.getLogger(__name__)


@dataclass
class BidRecord:
    """招标/中标记录"""
    bid_id: str
    title: str
    project_name: str
    bid_type: str  # bid_announce/win_announce
    publish_date: datetime
    bid_amount: float  # 金额（万元）
    winner: str  # 中标单位
    buyer: str  # 采购单位
    region: str  # 地区
    industry: str  # 行业
    related_stock: str = ""  # 关联股票代码
    url: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bid_id": self.bid_id,
            "title": self.title,
            "project_name": self.project_name,
            "bid_type": self.bid_type,
            "publish_date": self.publish_date.strftime("%Y-%m-%d") if self.publish_date else None,
            "bid_amount": self.bid_amount,
            "winner": self.winner,
            "buyer": self.buyer,
            "region": self.region,
            "industry": self.industry,
            "related_stock": self.related_stock,
            "url": self.url,
            "metadata": {
                "source": "bid_crawler",
                "crawl_time": datetime.now().isoformat()
            }
        }


class BidCrawler(BaseCrawler):
    """招标数据爬虫"""
    
    # 全国公共资源交易平台API（示例）
    GGZY_API = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
    
    # 上市公司名称到股票代码映射（部分示例）
    COMPANY_STOCK_MAP = {
        "中国移动": "600941.SH",
        "中国电信": "601728.SH",
        "中国联通": "600050.SH",
        "华为": "",  # 非上市
        "中兴通讯": "000063.SZ",
        "比亚迪": "002594.SZ",
        "宁德时代": "300750.SZ",
        "隆基绿能": "601012.SH",
        "阳光电源": "300274.SZ",
        "三一重工": "600031.SH",
        "中联重科": "000157.SZ",
        "徐工机械": "000425.SZ",
    }
    
    def __init__(self, delay_range: tuple = (2.0, 4.0)):
        super().__init__(
            name="bid",
            base_url="http://deal.ggzy.gov.cn",
            delay_range=delay_range
        )
    
    def build_url(self, **kwargs) -> str:
        return self.GGZY_API
    
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        """解析招标数据"""
        records = []
        try:
            data = json.loads(content)
            items = data.get("data", [])
            
            for item in items:
                try:
                    record = BidRecord(
                        bid_id=item.get("id", ""),
                        title=item.get("title", ""),
                        project_name=item.get("projectName", ""),
                        bid_type="win_announce" if "中标" in item.get("title", "") else "bid_announce",
                        publish_date=self._parse_date(item.get("publishDate")),
                        bid_amount=self._parse_amount(item.get("bidAmount", 0)),
                        winner=item.get("winner", ""),
                        buyer=item.get("buyer", ""),
                        region=item.get("region", ""),
                        industry=item.get("industry", ""),
                        related_stock=self._match_stock(item.get("winner", "")),
                        url=item.get("url", "")
                    )
                    records.append(record.to_dict())
                except Exception as e:
                    continue
        except Exception as e:
            logger.error(f"解析招标数据失败: {e}")
        
        return records
    
    def _parse_date(self, date_str: Any) -> Optional[datetime]:
        """解析日期"""
        if not date_str:
            return None
        try:
            if isinstance(date_str, str):
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日"]:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        continue
        except:
            pass
        return None
    
    def _parse_amount(self, amount: Any) -> float:
        """解析金额（转换为万元）"""
        if not amount:
            return 0.0
        try:
            if isinstance(amount, str):
                # 去除单位
                amount = re.sub(r'[万元亿]', '', amount)
                amount = float(amount)
            return float(amount)
        except:
            return 0.0
    
    def _match_stock(self, company_name: str) -> str:
        """匹配上市公司股票代码"""
        if not company_name:
            return ""
        for name, code in self.COMPANY_STOCK_MAP.items():
            if name in company_name:
                return code
        return ""
    
    def generate_mock_data(self, count: int = 20) -> List[Dict[str, Any]]:
        """生成模拟招标数据（用于测试）"""
        import random
        
        companies = [
            ("中兴通讯", "000063.SZ"),
            ("比亚迪", "002594.SZ"),
            ("宁德时代", "300750.SZ"),
            ("隆基绿能", "601012.SH"),
            ("阳光电源", "300274.SZ"),
            ("三一重工", "600031.SH"),
            ("中联重科", "000157.SZ"),
        ]
        
        industries = ["新能源", "通信", "工程机械", "电力设备", "储能"]
        regions = ["北京", "上海", "广东", "江苏", "浙江", "四川"]
        
        records = []
        base_date = datetime.now()
        
        for i in range(count):
            company, stock = random.choice(companies)
            days_ago = random.randint(0, 30)
            amount = random.uniform(100, 5000)  # 100-5000万
            
            record = BidRecord(
                bid_id=f"BID{base_date.strftime('%Y%m%d')}{i:04d}",
                title=f"{company}中标{random.choice(industries)}项目",
                project_name=f"2024年{random.choice(industries)}设备采购项目",
                bid_type="win_announce",
                publish_date=base_date - timedelta(days=days_ago),
                bid_amount=round(amount, 2),
                winner=company,
                buyer=f"{random.choice(regions)}市政府采购中心",
                region=random.choice(regions),
                industry=random.choice(industries),
                related_stock=stock,
                url=f"http://example.com/bid/{i}"
            )
            records.append(record.to_dict())
        
        return records
    
    def fetch_bids(self, keyword: str = None, region: str = None,
                   start_date: str = None, end_date: str = None,
                   page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        """获取招标数据"""
        # 由于真实API需要认证，这里返回模拟数据
        logger.info("使用模拟数据（真实API需要认证）")
        return self.generate_mock_data(page_size)
    
    def get_company_bids(self, company_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """获取指定公司的中标数据"""
        all_bids = self.generate_mock_data(50)
        # 筛选指定公司
        return [b for b in all_bids if company_name in b.get("winner", "")]


_bid_crawler = None

def get_bid_crawler() -> BidCrawler:
    """获取招标爬虫实例"""
    global _bid_crawler
    if _bid_crawler is None:
        _bid_crawler = BidCrawler()
        register_crawler("bid", _bid_crawler)
    return _bid_crawler
