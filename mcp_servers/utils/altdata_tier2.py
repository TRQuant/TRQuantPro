"""
M3.4: 第二档数据源 (Tier2 AltData)

招投标数据 + 招聘数据趋势分析
用于识别公司业务扩张信号

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import logging
import re

logger = logging.getLogger(__name__)


class BidType(Enum):
    """招投标类型"""
    GOVERNMENT = "government"       # 政府采购
    ENTERPRISE = "enterprise"       # 企业招标
    CONSTRUCTION = "construction"   # 工程建设
    SERVICE = "service"             # 服务采购
    EQUIPMENT = "equipment"         # 设备采购


class JobType(Enum):
    """招聘类型"""
    TECH = "tech"                   # 技术研发
    SALES = "sales"                 # 销售市场
    PRODUCTION = "production"       # 生产制造
    MANAGEMENT = "management"       # 管理层
    SUPPORT = "support"             # 支持职能


@dataclass
class BidRecord:
    """招投标记录"""
    bid_id: str                     # 招标ID
    company: str                    # 公司名称
    symbol: Optional[str] = None    # 股票代码
    title: str = ""                 # 招标标题
    bid_type: BidType = BidType.GOVERNMENT
    amount: float = 0.0             # 金额(万元)
    publish_date: datetime = field(default_factory=datetime.now)
    region: str = ""                # 地区
    industry: str = ""              # 行业
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bid_id": self.bid_id,
            "company": self.company,
            "symbol": self.symbol,
            "title": self.title,
            "bid_type": self.bid_type.value,
            "amount": self.amount,
            "publish_date": self.publish_date.isoformat(),
            "region": self.region,
            "industry": self.industry,
            "keywords": self.keywords
        }


@dataclass
class JobRecord:
    """招聘记录"""
    job_id: str                     # 招聘ID
    company: str                    # 公司名称
    symbol: Optional[str] = None    # 股票代码
    title: str = ""                 # 职位名称
    job_type: JobType = JobType.TECH
    salary_min: float = 0.0         # 最低薪资(K)
    salary_max: float = 0.0         # 最高薪资(K)
    publish_date: datetime = field(default_factory=datetime.now)
    location: str = ""              # 工作地点
    experience: str = ""            # 经验要求
    education: str = ""             # 学历要求
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "company": self.company,
            "symbol": self.symbol,
            "title": self.title,
            "job_type": self.job_type.value,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "publish_date": self.publish_date.isoformat(),
            "location": self.location,
            "experience": self.experience,
            "education": self.education,
            "keywords": self.keywords
        }


@dataclass
class TrendSignal:
    """趋势信号"""
    symbol: str                     # 股票代码
    company: str                    # 公司名称
    signal_type: str                # 信号类型
    strength: float                 # 信号强度 (0-1)
    description: str                # 描述
    evidence: List[str] = field(default_factory=list)  # 证据
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "company": self.company,
            "signal_type": self.signal_type,
            "strength": self.strength,
            "description": self.description,
            "evidence": self.evidence,
            "generated_at": self.generated_at.isoformat()
        }


class BidDataStore:
    """招投标数据存储"""
    
    def __init__(self, mongo_uri: Optional[str] = None):
        self._db = None
        self._collection = None
        self._records: Dict[str, BidRecord] = {}
        self._company_index: Dict[str, List[str]] = {}  # company -> [bid_ids]
        self._symbol_index: Dict[str, List[str]] = {}   # symbol -> [bid_ids]
        
        if mongo_uri:
            self._init_mongodb(mongo_uri)
    
    def _init_mongodb(self, mongo_uri: str):
        try:
            from pymongo import MongoClient
            client = MongoClient(mongo_uri)
            self._db = client.trquant
            self._collection = self._db.bid_data
            logger.info("招投标数据MongoDB连接成功")
        except Exception as e:
            logger.warning(f"招投标数据MongoDB连接失败: {e}")
    
    def add_record(self, record: BidRecord) -> bool:
        """添加招投标记录"""
        self._records[record.bid_id] = record
        
        # 更新索引
        if record.company not in self._company_index:
            self._company_index[record.company] = []
        self._company_index[record.company].append(record.bid_id)
        
        if record.symbol:
            if record.symbol not in self._symbol_index:
                self._symbol_index[record.symbol] = []
            self._symbol_index[record.symbol].append(record.bid_id)
        
        return True
    
    def get_by_company(self, company: str, days: int = 90) -> List[BidRecord]:
        """获取公司招投标记录"""
        cutoff = datetime.now() - timedelta(days=days)
        bid_ids = self._company_index.get(company, [])
        records = [self._records[bid_id] for bid_id in bid_ids 
                   if bid_id in self._records and self._records[bid_id].publish_date >= cutoff]
        return sorted(records, key=lambda x: x.publish_date, reverse=True)
    
    def get_by_symbol(self, symbol: str, days: int = 90) -> List[BidRecord]:
        """获取股票招投标记录"""
        cutoff = datetime.now() - timedelta(days=days)
        bid_ids = self._symbol_index.get(symbol, [])
        records = [self._records[bid_id] for bid_id in bid_ids 
                   if bid_id in self._records and self._records[bid_id].publish_date >= cutoff]
        return sorted(records, key=lambda x: x.publish_date, reverse=True)
    
    def analyze_trend(self, symbol: str, days: int = 180) -> Dict[str, Any]:
        """分析招投标趋势"""
        records = self.get_by_symbol(symbol, days)
        if not records:
            return {"symbol": symbol, "trend": "no_data", "count": 0}
        
        # 按月统计
        monthly = {}
        for r in records:
            month = r.publish_date.strftime("%Y-%m")
            if month not in monthly:
                monthly[month] = {"count": 0, "amount": 0}
            monthly[month]["count"] += 1
            monthly[month]["amount"] += r.amount
        
        # 计算趋势
        months = sorted(monthly.keys())
        if len(months) >= 2:
            recent = monthly[months[-1]]["count"]
            previous = monthly[months[-2]]["count"]
            growth = (recent - previous) / max(previous, 1)
            trend = "growing" if growth > 0.2 else ("declining" if growth < -0.2 else "stable")
        else:
            trend = "insufficient_data"
            growth = 0
        
        return {
            "symbol": symbol,
            "trend": trend,
            "growth_rate": growth,
            "total_count": len(records),
            "total_amount": sum(r.amount for r in records),
            "monthly": monthly
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_records": len(self._records),
            "companies": len(self._company_index),
            "symbols": len(self._symbol_index)
        }


class JobDataStore:
    """招聘数据存储"""
    
    def __init__(self, mongo_uri: Optional[str] = None):
        self._db = None
        self._collection = None
        self._records: Dict[str, JobRecord] = {}
        self._company_index: Dict[str, List[str]] = {}
        self._symbol_index: Dict[str, List[str]] = {}
        
        if mongo_uri:
            self._init_mongodb(mongo_uri)
    
    def _init_mongodb(self, mongo_uri: str):
        try:
            from pymongo import MongoClient
            client = MongoClient(mongo_uri)
            self._db = client.trquant
            self._collection = self._db.job_data
            logger.info("招聘数据MongoDB连接成功")
        except Exception as e:
            logger.warning(f"招聘数据MongoDB连接失败: {e}")
    
    def add_record(self, record: JobRecord) -> bool:
        """添加招聘记录"""
        self._records[record.job_id] = record
        
        if record.company not in self._company_index:
            self._company_index[record.company] = []
        self._company_index[record.company].append(record.job_id)
        
        if record.symbol:
            if record.symbol not in self._symbol_index:
                self._symbol_index[record.symbol] = []
            self._symbol_index[record.symbol].append(record.job_id)
        
        return True
    
    def get_by_symbol(self, symbol: str, days: int = 90) -> List[JobRecord]:
        """获取股票招聘记录"""
        cutoff = datetime.now() - timedelta(days=days)
        job_ids = self._symbol_index.get(symbol, [])
        records = [self._records[job_id] for job_id in job_ids 
                   if job_id in self._records and self._records[job_id].publish_date >= cutoff]
        return sorted(records, key=lambda x: x.publish_date, reverse=True)
    
    def analyze_trend(self, symbol: str, days: int = 180) -> Dict[str, Any]:
        """分析招聘趋势"""
        records = self.get_by_symbol(symbol, days)
        if not records:
            return {"symbol": symbol, "trend": "no_data", "count": 0}
        
        # 按类型统计
        by_type = {}
        for r in records:
            t = r.job_type.value
            if t not in by_type:
                by_type[t] = 0
            by_type[t] += 1
        
        # 按月统计
        monthly = {}
        for r in records:
            month = r.publish_date.strftime("%Y-%m")
            if month not in monthly:
                monthly[month] = 0
            monthly[month] += 1
        
        # 计算趋势
        months = sorted(monthly.keys())
        if len(months) >= 2:
            recent = monthly[months[-1]]
            previous = monthly[months[-2]]
            growth = (recent - previous) / max(previous, 1)
            trend = "expanding" if growth > 0.3 else ("contracting" if growth < -0.3 else "stable")
        else:
            trend = "insufficient_data"
            growth = 0
        
        # 识别扩张信号
        tech_ratio = by_type.get("tech", 0) / max(len(records), 1)
        expansion_signal = tech_ratio > 0.4 and growth > 0.2
        
        return {
            "symbol": symbol,
            "trend": trend,
            "growth_rate": growth,
            "total_count": len(records),
            "by_type": by_type,
            "tech_ratio": tech_ratio,
            "expansion_signal": expansion_signal,
            "monthly": monthly
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_records": len(self._records),
            "companies": len(self._company_index),
            "symbols": len(self._symbol_index)
        }


class Tier2SignalGenerator:
    """Tier2信号生成器"""
    
    def __init__(self, bid_store: BidDataStore, job_store: JobDataStore):
        self.bid_store = bid_store
        self.job_store = job_store
    
    def generate_signals(self, symbol: str) -> List[TrendSignal]:
        """生成综合信号"""
        signals = []
        
        # 招投标信号
        bid_trend = self.bid_store.analyze_trend(symbol)
        if bid_trend["trend"] == "growing":
            signals.append(TrendSignal(
                symbol=symbol,
                company="",
                signal_type="bid_growth",
                strength=min(bid_trend["growth_rate"], 1.0),
                description=f"招投标活动增长 {bid_trend['growth_rate']*100:.0f}%",
                evidence=[f"总数: {bid_trend['total_count']}", f"总金额: {bid_trend['total_amount']:.0f}万"]
            ))
        
        # 招聘信号
        job_trend = self.job_store.analyze_trend(symbol)
        if job_trend.get("expansion_signal"):
            signals.append(TrendSignal(
                symbol=symbol,
                company="",
                signal_type="hiring_expansion",
                strength=min(job_trend["growth_rate"], 1.0),
                description=f"招聘扩张信号，技术岗占比 {job_trend['tech_ratio']*100:.0f}%",
                evidence=[f"总招聘: {job_trend['total_count']}", f"增长率: {job_trend['growth_rate']*100:.0f}%"]
            ))
        
        # 综合信号
        if bid_trend["trend"] == "growing" and job_trend.get("expansion_signal"):
            signals.append(TrendSignal(
                symbol=symbol,
                company="",
                signal_type="business_expansion",
                strength=0.8,
                description="业务扩张综合信号：招投标+招聘双增长",
                evidence=["招投标活动增长", "技术岗位扩招"]
            ))
        
        return signals
    
    def batch_analyze(self, symbols: List[str]) -> Dict[str, List[TrendSignal]]:
        """批量分析"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.generate_signals(symbol)
        return results


# 全局实例
_bid_store: Optional[BidDataStore] = None
_job_store: Optional[JobDataStore] = None
_signal_generator: Optional[Tier2SignalGenerator] = None


def get_bid_store(mongo_uri: Optional[str] = None) -> BidDataStore:
    global _bid_store
    if _bid_store is None:
        _bid_store = BidDataStore(mongo_uri)
    return _bid_store


def get_job_store(mongo_uri: Optional[str] = None) -> JobDataStore:
    global _job_store
    if _job_store is None:
        _job_store = JobDataStore(mongo_uri)
    return _job_store


def get_signal_generator() -> Tier2SignalGenerator:
    global _signal_generator
    if _signal_generator is None:
        _signal_generator = Tier2SignalGenerator(get_bid_store(), get_job_store())
    return _signal_generator
