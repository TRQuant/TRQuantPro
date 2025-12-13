"""
PDF下载器
"""
import requests
from pathlib import Path
from typing import List, Optional, Dict
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class PDFDownloader:
    """PDF下载器"""
    
    def __init__(self, output_dir: Path, proxy_config: Optional[Dict] = None):
        """
        初始化PDF下载器
        
        Args:
            output_dir: 输出目录
            proxy_config: 代理配置
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建session
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 配置代理
        if proxy_config:
            self.session.proxies.update(proxy_config)
    
    def collect(self, url: str, filename: Optional[str] = None) -> List[Path]:
        """
        下载PDF
        
        Args:
            url: PDF URL
            filename: 保存的文件名（可选）
        
        Returns:
            下载的文件路径列表
        """
        if not self.validate_source(url):
            return []
        
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 检查Content-Type
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' not in content_type.lower() and not url.lower().endswith('.pdf'):
                logger.warning(f"URL may not be a PDF: {url}")
            
            if filename is None:
                # 从URL提取文件名
                filename = url.split('/')[-1] or 'document.pdf'
                # 清理文件名
                filename = filename.split('?')[0]  # 移除查询参数
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
            
            file_path = self.output_dir / filename
            
            # 下载文件
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded PDF: {file_path}")
            return [file_path]
            
        except Exception as e:
            logger.error(f"Error downloading PDF from {url}: {e}")
            return []
    
    def validate_source(self, source: str) -> bool:
        """验证PDF URL"""
        return source.lower().endswith('.pdf') or 'pdf' in source.lower() or source.startswith('http')

