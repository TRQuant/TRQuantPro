"""
学术数据库爬虫
支持 arXiv, SSRN, CrossRef 等
"""
import feedparser
import requests
from typing import List, Optional, Dict
from pathlib import Path
import logging
from .pdf_downloader import PDFDownloader

logger = logging.getLogger(__name__)


class AcademicScraper:
    """学术数据库爬虫"""
    
    SUPPORTED_DATABASES = {
        'arxiv': {
            'api_url': 'https://export.arxiv.org/api/query',
            'free': True,
            'description': 'arXiv - 免费学术论文库'
        },
        'ssrn': {
            'api_url': None,  # 需要爬取
            'free': True,
            'description': 'SSRN - 社会科学研究网络'
        },
        'crossref': {
            'api_url': 'https://api.crossref.org/works',
            'free': True,
            'description': 'CrossRef - 学术论文元数据'
        }
    }
    
    def __init__(self, output_dir: Path, proxy_config: Optional[Dict] = None):
        """
        初始化学术爬虫
        
        Args:
            output_dir: 输出目录
            proxy_config: 代理配置
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.proxy_config = proxy_config
        self.pdf_downloader = PDFDownloader(self.output_dir, proxy_config)
    
    def collect(self, database: str, query: str,
                max_results: int = 100, **kwargs) -> List[Path]:
        """
        从学术数据库收集论文
        
        Args:
            database: 数据库名称（arxiv, ssrn, crossref）
            query: 搜索查询
            max_results: 最大结果数
        
        Returns:
            下载的文件路径列表
        """
        if database not in self.SUPPORTED_DATABASES:
            logger.error(f"Unsupported database: {database}")
            logger.info(f"Supported databases: {list(self.SUPPORTED_DATABASES.keys())}")
            return []
        
        db_config = self.SUPPORTED_DATABASES[database]
        
        if database == 'arxiv':
            return self._collect_arxiv(query, max_results)
        elif database == 'crossref':
            return self._collect_crossref(query, max_results)
        else:
            logger.warning(f"Database {database} not yet implemented")
            return []
    
    def _collect_arxiv(self, query: str, max_results: int) -> List[Path]:
        """从arXiv收集论文"""
        try:
            url = f"https://export.arxiv.org/api/query?search_query={query}&max_results={max_results}&sortBy=relevance&sortOrder=descending"
            feed = feedparser.parse(url)
            
            if feed.bozo:
                logger.error(f"Error parsing arXiv feed: {feed.bozo_exception}")
                return []
            
            downloaded_files = []
            papers_dir = self.output_dir / "papers"
            papers_dir.mkdir(exist_ok=True)
            metadata_dir = self.output_dir / "metadata"
            metadata_dir.mkdir(exist_ok=True)
            
            for entry in feed.entries:
                try:
                    # 提取论文ID
                    paper_id = entry.id.split('/')[-1].split('v')[0]
                    
                    # 下载PDF
                    pdf_url = None
                    for link in entry.links:
                        if link.type == 'application/pdf':
                            pdf_url = link.href
                            break
                    
                    if pdf_url:
                        filename = f"arxiv_{paper_id}.pdf"
                        files = self.pdf_downloader.collect(pdf_url, filename=filename)
                        downloaded_files.extend(files)
                        
                        # 保存元数据
                        import json
                        metadata = {
                            'id': paper_id,
                            'title': entry.title,
                            'authors': ', '.join([a.name for a in entry.authors]),
                            'summary': entry.summary,
                            'published': entry.published,
                            'updated': entry.updated if hasattr(entry, 'updated') else None,
                            'categories': [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else [],
                            'pdf_url': pdf_url,
                            'source': 'arxiv'
                        }
                        metadata_path = metadata_dir / f"arxiv_{paper_id}_metadata.json"
                        metadata_path.write_text(
                            json.dumps(metadata, indent=2, ensure_ascii=False),
                            encoding='utf-8'
                        )
                        
                        logger.info(f"Downloaded arXiv paper: {entry.title[:50]}...")
                    
                except Exception as e:
                    logger.error(f"Error downloading paper {entry.id}: {e}")
            
            logger.info(f"Downloaded {len(downloaded_files)} papers from arXiv")
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Error collecting from arXiv: {e}")
            return []
    
    def _collect_crossref(self, query: str, max_results: int) -> List[Path]:
        """从CrossRef收集论文元数据（不直接下载PDF）"""
        try:
            url = "https://api.crossref.org/works"
            params = {
                'query': query,
                'rows': min(max_results, 1000),  # CrossRef限制
                'sort': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            metadata_dir = self.output_dir / "metadata"
            metadata_dir.mkdir(exist_ok=True)
            
            saved_files = []
            for item in data.get('message', {}).get('items', []):
                try:
                    import json
                    doi = item.get('DOI', 'unknown')
                    metadata = {
                        'doi': doi,
                        'title': ' '.join(item.get('title', [])),
                        'authors': [f"{a.get('given', '')} {a.get('family', '')}" 
                                   for a in item.get('author', [])],
                        'published': item.get('published-print', {}).get('date-parts', [None])[0],
                        'journal': item.get('container-title', [None])[0],
                        'url': item.get('URL'),
                        'source': 'crossref'
                    }
                    
                    metadata_path = metadata_dir / f"crossref_{doi.replace('/', '_')}_metadata.json"
                    metadata_path.write_text(
                        json.dumps(metadata, indent=2, ensure_ascii=False),
                        encoding='utf-8'
                    )
                    saved_files.append(metadata_path)
                    
                except Exception as e:
                    logger.error(f"Error processing CrossRef item: {e}")
            
            logger.info(f"Saved {len(saved_files)} metadata files from CrossRef")
            return saved_files
            
        except Exception as e:
            logger.error(f"Error collecting from CrossRef: {e}")
            return []
    
    def list_databases(self) -> Dict:
        """列出支持的数据库"""
        return self.SUPPORTED_DATABASES

