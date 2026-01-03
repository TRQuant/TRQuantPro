# -*- coding: utf-8 -*-
"""
招聘数据爬虫

数据源（需要登录，这里使用模拟数据）：
- 猎聘
- BOSS直聘
- 智联招聘
- 拉勾网

采集内容：
- 公司招聘岗位数量
- 薪资范围
- 岗位类型分布
"""

import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .base_crawler import BaseCrawler, CrawlResult, register_crawler

logger = logging.getLogger(__name__)


@dataclass
class JobRecord:
    """招聘记录"""
    job_id: str
    company_name: str
    stock_code: str
    position_title: str
    salary_min: int  # 最低月薪（K）
    salary_max: int  # 最高月薪（K）
    location: str
    job_type: str  # tech/sales/operations/finance
    experience: str  # 经验要求
    education: str  # 学历要求
    publish_date: datetime
    source: str  # liepin/boss/zhilian
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "company_name": self.company_name,
            "stock_code": self.stock_code,
            "position_title": self.position_title,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_avg": (self.salary_min + self.salary_max) / 2,
            "location": self.location,
            "job_type": self.job_type,
            "experience": self.experience,
            "education": self.education,
            "publish_date": self.publish_date.strftime("%Y-%m-%d") if self.publish_date else None,
            "source": self.source,
            "metadata": {
                "crawl_time": datetime.now().isoformat()
            }
        }


class JobCrawler(BaseCrawler):
    """招聘数据爬虫"""
    
    # 上市公司招聘数据（示例）
    TRACKED_COMPANIES = {
        "宁德时代": {"stock": "300750.SZ", "industry": "新能源"},
        "比亚迪": {"stock": "002594.SZ", "industry": "新能源汽车"},
        "隆基绿能": {"stock": "601012.SH", "industry": "光伏"},
        "中兴通讯": {"stock": "000063.SZ", "industry": "通信"},
        "海康威视": {"stock": "002415.SZ", "industry": "安防"},
        "立讯精密": {"stock": "002475.SZ", "industry": "消费电子"},
        "药明康德": {"stock": "603259.SH", "industry": "医药"},
        "迈瑞医疗": {"stock": "300760.SZ", "industry": "医疗器械"},
    }
    
    JOB_TYPES = {
        "tech": ["软件工程师", "算法工程师", "数据分析师", "测试工程师", "前端开发", "后端开发"],
        "sales": ["销售经理", "大客户经理", "商务拓展", "市场专员"],
        "operations": ["运营经理", "供应链专员", "采购经理", "生产主管"],
        "finance": ["财务经理", "会计", "审计", "投资分析师"],
    }
    
    def __init__(self, delay_range: tuple = (1.5, 3.0)):
        super().__init__(
            name="job",
            base_url="https://www.liepin.com",
            delay_range=delay_range
        )
    
    def build_url(self, **kwargs) -> str:
        return self.base_url
    
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        """解析招聘数据"""
        # 由于需要登录，返回空列表
        return []
    
    def generate_mock_data(self, company_name: str = None, count: int = 30) -> List[Dict[str, Any]]:
        """生成模拟招聘数据"""
        records = []
        base_date = datetime.now()
        
        # 如果指定了公司
        if company_name and company_name in self.TRACKED_COMPANIES:
            companies = {company_name: self.TRACKED_COMPANIES[company_name]}
        else:
            companies = self.TRACKED_COMPANIES
        
        for company, info in companies.items():
            # 每个公司生成多个岗位
            job_count = count // len(companies) if len(companies) > 0 else count
            
            for i in range(job_count):
                job_type = random.choice(list(self.JOB_TYPES.keys()))
                position = random.choice(self.JOB_TYPES[job_type])
                
                # 根据岗位类型设置薪资范围
                if job_type == "tech":
                    salary_min = random.randint(15, 30)
                    salary_max = salary_min + random.randint(5, 20)
                elif job_type == "sales":
                    salary_min = random.randint(10, 20)
                    salary_max = salary_min + random.randint(5, 15)
                else:
                    salary_min = random.randint(8, 15)
                    salary_max = salary_min + random.randint(3, 10)
                
                days_ago = random.randint(0, 14)
                
                record = JobRecord(
                    job_id=f"JOB{base_date.strftime('%Y%m%d')}{len(records):04d}",
                    company_name=company,
                    stock_code=info["stock"],
                    position_title=position,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    location=random.choice(["深圳", "上海", "北京", "杭州", "广州"]),
                    job_type=job_type,
                    experience=random.choice(["1-3年", "3-5年", "5-10年", "不限"]),
                    education=random.choice(["本科", "硕士", "不限"]),
                    publish_date=base_date - timedelta(days=days_ago),
                    source=random.choice(["liepin", "boss", "zhilian"])
                )
                records.append(record.to_dict())
        
        return records
    
    def fetch_jobs(self, company_name: str = None, job_type: str = None,
                   page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        """获取招聘数据"""
        logger.info("使用模拟数据（真实API需要登录）")
        jobs = self.generate_mock_data(company_name, page_size * 2)
        
        # 筛选岗位类型
        if job_type:
            jobs = [j for j in jobs if j.get("job_type") == job_type]
        
        return jobs[:page_size]
    
    def get_company_hiring_trend(self, stock_code: str, days: int = 30) -> Dict[str, Any]:
        """获取公司招聘趋势"""
        # 找到公司名称
        company_name = None
        for name, info in self.TRACKED_COMPANIES.items():
            if info["stock"] == stock_code:
                company_name = name
                break
        
        if not company_name:
            return {"error": f"未找到股票代码 {stock_code} 对应的公司"}
        
        jobs = self.generate_mock_data(company_name, 50)
        
        # 统计
        job_type_counts = {}
        total_salary = 0
        
        for job in jobs:
            jt = job.get("job_type", "other")
            job_type_counts[jt] = job_type_counts.get(jt, 0) + 1
            total_salary += job.get("salary_avg", 0)
        
        return {
            "stock_code": stock_code,
            "company_name": company_name,
            "total_positions": len(jobs),
            "job_type_distribution": job_type_counts,
            "avg_salary": round(total_salary / len(jobs), 1) if jobs else 0,
            "period_days": days,
            "trend": "expanding" if len(jobs) > 20 else "stable"
        }


_job_crawler = None

def get_job_crawler() -> JobCrawler:
    """获取招聘爬虫实例"""
    global _job_crawler
    if _job_crawler is None:
        _job_crawler = JobCrawler()
        register_crawler("job", _job_crawler)
    return _job_crawler
