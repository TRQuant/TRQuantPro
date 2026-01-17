"""
信息源推荐器
"""
from typing import List, Dict
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class InformationSource:
    """信息源"""
    name: str
    url: str
    type: str  # 'book', 'academic', 'blog', 'documentation', 'api'
    description: str
    access_method: str  # 'free', 'subscription', 'purchase', 'api'
    quality_score: float  # 1-10
    relevance_keywords: List[str]
    language: str = 'zh'  # 'zh', 'en', 'both'


class SourceRecommender:
    """信息源推荐器"""
    
    def __init__(self, sources_file: Path = None):
        """
        初始化推荐器
        
        Args:
            sources_file: 信息源配置文件路径（JSON格式）
        """
        if sources_file and Path(sources_file).exists():
            self.sources = self._load_from_file(sources_file)
        else:
            self.sources = self._load_default_sources()
    
    def _load_default_sources(self) -> List[InformationSource]:
        """加载默认信息源列表"""
        return [
            # 中文书籍
            InformationSource(
                name="量化投资：策略与技术",
                url="https://book.douban.com/subject/",
                type="book",
                description="量化投资经典教材，丁鹏著",
                access_method="purchase",
                quality_score=9.0,
                relevance_keywords=["量化投资", "策略", "技术", "Python"],
                language="zh"
            ),
            # 学术数据库
            InformationSource(
                name="arXiv",
                url="https://arxiv.org/",
                type="academic",
                description="免费学术论文库，包含大量量化金融和机器学习论文",
                access_method="free",
                quality_score=8.5,
                relevance_keywords=["机器学习", "量化金融", "算法交易", "策略研究"],
                language="en"
            ),
            InformationSource(
                name="SSRN",
                url="https://www.ssrn.com/",
                type="academic",
                description="社会科学研究网络，金融和经济学论文",
                access_method="free",
                quality_score=8.0,
                relevance_keywords=["金融", "经济学", "量化投资", "策略研究"],
                language="en"
            ),
            # 技术文档
            InformationSource(
                name="聚宽文档",
                url="https://www.joinquant.com/help",
                type="documentation",
                description="聚宽量化平台文档和API参考",
                access_method="free",
                quality_score=8.0,
                relevance_keywords=["量化平台", "API", "策略开发", "回测"],
                language="zh"
            ),
            InformationSource(
                name="米筐文档",
                url="https://www.ricequant.com/doc",
                type="documentation",
                description="米筐量化平台文档",
                access_method="free",
                quality_score=7.5,
                relevance_keywords=["量化平台", "API", "策略开发"],
                language="zh"
            ),
            # 技术博客
            InformationSource(
                name="QuantStart",
                url="https://www.quantstart.com/",
                type="blog",
                description="量化交易教程和策略研究博客",
                access_method="free",
                quality_score=8.5,
                relevance_keywords=["量化交易", "策略", "教程", "Python"],
                language="en"
            ),
            # GitHub项目
            InformationSource(
                name="GitHub量化项目",
                url="https://github.com/topics/quantitative-finance",
                type="documentation",
                description="GitHub上的量化投资开源项目",
                access_method="free",
                quality_score=8.0,
                relevance_keywords=["量化", "开源", "策略", "代码"],
                language="both"
            ),
        ]
    
    def _load_from_file(self, file_path: Path) -> List[InformationSource]:
        """从文件加载信息源"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sources = []
        for item in data:
            sources.append(InformationSource(**item))
        return sources
    
    def recommend(self, keywords: List[str],
                  source_type: str = None,
                  min_quality: float = 7.0,
                  language: str = None) -> List[InformationSource]:
        """
        推荐信息源
        
        Args:
            keywords: 关键词列表
            source_type: 信息源类型过滤
            min_quality: 最低质量分数
            language: 语言过滤（'zh', 'en', 'both'）
        
        Returns:
            推荐的信息源列表（按相关性排序）
        """
        recommendations = []
        
        for source in self.sources:
            # 类型过滤
            if source_type and source.type != source_type:
                continue
            
            # 质量过滤
            if source.quality_score < min_quality:
                continue
            
            # 语言过滤
            if language and language != 'both':
                if source.language != language and source.language != 'both':
                    continue
            
            # 计算相关性
            relevance = self._calculate_relevance(source, keywords)
            if relevance > 0.3:  # 相关性阈值
                recommendations.append((source, relevance))
        
        # 按相关性排序
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [src for src, _ in recommendations]
    
    def _calculate_relevance(self, source: InformationSource,
                            keywords: List[str]) -> float:
        """计算相关性分数"""
        if not keywords:
            return 0.0
        
        score = 0.0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # 检查关键词匹配
            if keyword_lower in [k.lower() for k in source.relevance_keywords]:
                score += 1.0
            if keyword_lower in source.description.lower():
                score += 0.5
            if keyword_lower in source.name.lower():
                score += 0.3
        
        return score / len(keywords) if keywords else 0.0
    
    def list_all_sources(self) -> List[InformationSource]:
        """列出所有信息源"""
        return self.sources
    
    def save_to_file(self, file_path: Path):
        """保存信息源到文件"""
        data = []
        for source in self.sources:
            data.append({
                'name': source.name,
                'url': source.url,
                'type': source.type,
                'description': source.description,
                'access_method': source.access_method,
                'quality_score': source.quality_score,
                'relevance_keywords': source.relevance_keywords,
                'language': source.language
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

