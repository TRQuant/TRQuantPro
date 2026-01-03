# -*- coding: utf-8 -*-
"""
调研报告管理器
==============

统一管理所有类型的调研报告：
- 行业调研报告
- 公司实地调研
- 专家会议纪要
- 券商研报
- 社交信息/校友圈信息

功能：
1. 报告上传和分类存储
2. 报告索引和搜索
3. 关键信息提取
4. 与策略开发集成
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# 默认调研报告存储路径
DEFAULT_RESEARCH_PATH = Path(__file__).parent.parent / "data" / "research_reports"

# 报告分类
REPORT_CATEGORIES = {
    "industry": {
        "name": "行业调研",
        "icon": "🏭",
        "description": "产业链分析、行业格局、发展趋势",
        "path": "industry",
    },
    "company": {
        "name": "公司调研",
        "icon": "🏢",
        "description": "实地考察、管理层访谈、经营分析",
        "path": "company",
    },
    "expert": {
        "name": "专家会议",
        "icon": "🎤",
        "description": "行业专家、分析师观点、电话会议",
        "path": "expert",
    },
    "broker": {
        "name": "券商研报",
        "icon": "📊",
        "description": "买方/卖方研究报告、深度报告",
        "path": "broker",
    },
    "social": {
        "name": "社交信息",
        "icon": "💬",
        "description": "校友圈、行业交流、投资人脉、市场传闻",
        "path": "social",
    },
}


class ResearchReport:
    """调研报告对象"""
    
    def __init__(self, 
                 title: str,
                 category: str,
                 file_path: str = None,
                 content: str = None,
                 tags: List[str] = None,
                 related_stocks: List[str] = None,
                 source: str = None,
                 author: str = None,
                 date: str = None,
                 summary: str = None,
                 key_points: List[str] = None,
                 investment_logic: str = None,
                 risk_notes: str = None):
        
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.title = title
        self.category = category
        self.file_path = file_path
        self.content = content
        self.tags = tags or []
        self.related_stocks = related_stocks or []
        self.source = source or "未知"
        self.author = author or "未知"
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.summary = summary or ""
        self.key_points = key_points or []
        self.investment_logic = investment_logic or ""
        self.risk_notes = risk_notes or ""
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "file_path": self.file_path,
            "tags": self.tags,
            "related_stocks": self.related_stocks,
            "source": self.source,
            "author": self.author,
            "date": self.date,
            "summary": self.summary,
            "key_points": self.key_points,
            "investment_logic": self.investment_logic,
            "risk_notes": self.risk_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ResearchReport':
        report = cls(
            title=data.get("title", ""),
            category=data.get("category", ""),
            file_path=data.get("file_path"),
            tags=data.get("tags", []),
            related_stocks=data.get("related_stocks", []),
            source=data.get("source"),
            author=data.get("author"),
            date=data.get("date"),
            summary=data.get("summary"),
            key_points=data.get("key_points", []),
            investment_logic=data.get("investment_logic"),
            risk_notes=data.get("risk_notes"),
        )
        report.id = data.get("id", report.id)
        report.created_at = data.get("created_at", report.created_at)
        report.updated_at = data.get("updated_at", report.updated_at)
        return report


class ResearchManager:
    """调研报告管理器"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or DEFAULT_RESEARCH_PATH
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 确保所有分类目录存在
        for cat_key, cat_info in REPORT_CATEGORIES.items():
            (self.base_path / cat_info["path"]).mkdir(exist_ok=True)
        
        # 索引文件路径
        self.index_file = self.base_path / "index.json"
        
        # 加载索引
        self.reports: Dict[str, ResearchReport] = {}
        self._load_index()
    
    def _load_index(self):
        """加载报告索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for report_data in data.get("reports", []):
                        report = ResearchReport.from_dict(report_data)
                        self.reports[report.id] = report
                logger.info(f"加载了 {len(self.reports)} 份调研报告索引")
            except Exception as e:
                logger.error(f"加载索引失败: {e}")
    
    def _save_index(self):
        """保存报告索引"""
        try:
            data = {
                "updated_at": datetime.now().isoformat(),
                "total_count": len(self.reports),
                "reports": [r.to_dict() for r in self.reports.values()]
            }
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"保存了 {len(self.reports)} 份调研报告索引")
        except Exception as e:
            logger.error(f"保存索引失败: {e}")
    
    def add_report(self, 
                   title: str,
                   category: str,
                   file_path: str = None,
                   content: str = None,
                   **kwargs) -> ResearchReport:
        """
        添加调研报告
        
        参数:
            title: 报告标题
            category: 分类 (industry/company/expert/broker/social)
            file_path: 源文件路径（将被复制到管理目录）
            content: 文本内容（如果没有文件）
            **kwargs: 其他属性
        
        返回:
            ResearchReport 对象
        """
        if category not in REPORT_CATEGORIES:
            raise ValueError(f"无效的分类: {category}")
        
        # 创建报告对象
        report = ResearchReport(
            title=title,
            category=category,
            content=content,
            **kwargs
        )
        
        # 如果有文件，复制到管理目录
        if file_path and os.path.exists(file_path):
            src_path = Path(file_path)
            dest_dir = self.base_path / REPORT_CATEGORIES[category]["path"]
            
            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{src_path.name}"
            dest_path = dest_dir / new_filename
            
            # 复制文件
            shutil.copy2(src_path, dest_path)
            report.file_path = str(dest_path)
            logger.info(f"文件已复制到: {dest_path}")
        
        # 如果只有内容，保存为文本文件
        elif content:
            dest_dir = self.base_path / REPORT_CATEGORIES[category]["path"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:50]
            new_filename = f"{timestamp}_{safe_title}.md"
            dest_path = dest_dir / new_filename
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"日期: {report.date}\n")
                f.write(f"来源: {report.source}\n")
                f.write(f"作者: {report.author}\n\n")
                f.write("---\n\n")
                f.write(content)
            
            report.file_path = str(dest_path)
            logger.info(f"内容已保存到: {dest_path}")
        
        # 添加到索引
        self.reports[report.id] = report
        self._save_index()
        
        return report
    
    def get_report(self, report_id: str) -> Optional[ResearchReport]:
        """获取报告"""
        return self.reports.get(report_id)
    
    def list_reports(self, 
                     category: str = None,
                     tags: List[str] = None,
                     stocks: List[str] = None,
                     keyword: str = None,
                     limit: int = 100) -> List[ResearchReport]:
        """
        列出报告
        
        参数:
            category: 按分类筛选
            tags: 按标签筛选
            stocks: 按关联股票筛选
            keyword: 关键词搜索（标题、摘要）
            limit: 返回数量限制
        """
        results = list(self.reports.values())
        
        # 按分类筛选
        if category:
            results = [r for r in results if r.category == category]
        
        # 按标签筛选
        if tags:
            results = [r for r in results if any(t in r.tags for t in tags)]
        
        # 按股票筛选
        if stocks:
            results = [r for r in results if any(s in r.related_stocks for s in stocks)]
        
        # 关键词搜索
        if keyword:
            keyword = keyword.lower()
            results = [r for r in results 
                      if keyword in r.title.lower() 
                      or keyword in r.summary.lower()
                      or keyword in r.investment_logic.lower()]
        
        # 按日期排序（最新在前）
        results.sort(key=lambda r: r.date, reverse=True)
        
        return results[:limit]
    
    def delete_report(self, report_id: str) -> bool:
        """删除报告"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        # 删除文件
        if report.file_path and os.path.exists(report.file_path):
            os.remove(report.file_path)
            logger.info(f"已删除文件: {report.file_path}")
        
        # 从索引中移除
        del self.reports[report_id]
        self._save_index()
        
        return True
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = {
            "total": len(self.reports),
            "by_category": {},
            "recent_7_days": 0,
            "stocks_covered": set(),
            "tags_used": set(),
        }
        
        from datetime import timedelta
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        for report in self.reports.values():
            # 按分类统计
            cat = report.category
            if cat not in stats["by_category"]:
                stats["by_category"][cat] = 0
            stats["by_category"][cat] += 1
            
            # 最近7天
            if report.date >= seven_days_ago:
                stats["recent_7_days"] += 1
            
            # 覆盖股票
            stats["stocks_covered"].update(report.related_stocks)
            
            # 使用标签
            stats["tags_used"].update(report.tags)
        
        stats["stocks_covered"] = list(stats["stocks_covered"])
        stats["tags_used"] = list(stats["tags_used"])
        
        return stats
    
    def get_reports_for_strategy(self, stocks: List[str] = None, 
                                  tags: List[str] = None) -> Dict:
        """
        获取策略开发相关的调研报告
        
        返回整理好的信息，供策略开发参考
        """
        reports = self.list_reports(stocks=stocks, tags=tags)
        
        result = {
            "total_reports": len(reports),
            "investment_logics": [],
            "risk_notes": [],
            "key_points": [],
            "related_reports": [],
        }
        
        for report in reports:
            if report.investment_logic:
                result["investment_logics"].append({
                    "title": report.title,
                    "logic": report.investment_logic,
                    "date": report.date,
                })
            
            if report.risk_notes:
                result["risk_notes"].append({
                    "title": report.title,
                    "risk": report.risk_notes,
                    "date": report.date,
                })
            
            result["key_points"].extend(report.key_points)
            
            result["related_reports"].append({
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "date": report.date,
                "summary": report.summary[:200] if report.summary else "",
            })
        
        return result
    
    def scan_folder(self) -> List[str]:
        """扫描文件夹，发现未索引的文件"""
        unindexed = []
        indexed_paths = {r.file_path for r in self.reports.values() if r.file_path}
        
        for cat_key, cat_info in REPORT_CATEGORIES.items():
            cat_path = self.base_path / cat_info["path"]
            if cat_path.exists():
                for file_path in cat_path.iterdir():
                    if file_path.is_file() and str(file_path) not in indexed_paths:
                        unindexed.append(str(file_path))
        
        return unindexed


# 全局实例
_research_manager = None

def get_research_manager() -> ResearchManager:
    """获取调研报告管理器单例"""
    global _research_manager
    if _research_manager is None:
        _research_manager = ResearchManager()
    return _research_manager





