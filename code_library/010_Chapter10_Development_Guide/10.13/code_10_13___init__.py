"""
文件名: code_10_13___init__.py
保存路径: code_library/010_Chapter10_Development_Guide/10.13/code_10_13___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.13_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# extension/python/tools/data_collector/web_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
from typing import List, Optional, Dict
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class WebCrawler:
    """网页爬虫 - 基于 requests + Beautiful Soup"""
    
    def __init__(self, output_dir: Path, 
                 delay_range: tuple = (1, 3),
                 respect_robots: bool = True,
                 proxy_config: Optional[Dict] = None,
                 max_retries: int = 3):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.delay_range = delay_range
        self.respect_robots = respect_robots
        self.max_retries = max_retries
        
        # 创建session
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置User-Agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def collect(self, url: str, max_depth: int = 2,
                allowed_domains: Optional[List[str]] = None,
                allowed_patterns: Optional[List[str]] = None) -> List[Path]:
        """爬取网页"""
        visited = set()
        to_visit = [(url, 0)]
        downloaded_files = []
        
        while to_visit:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited or depth > max_depth:
                continue
            
            visited.add(current_url)
            
            try:
                # 检查域名
                if allowed_domains:
                    domain = urlparse(current_url).netloc
                    if domain not in allowed_domains:
                        continue
                
                # 发送请求
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                
                # 解析HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 提取文本内容
                text_content = soup.get_text(separator='\n', strip=True)
                
                # 保存文件
                file_path = self._save_content(current_url, text_content)
                downloaded_files.append(file_path)
                
                # 发现新链接
                if depth < max_depth:
                    links = self._extract_links(soup, current_url, allowed_patterns)
                    for link in links:
                        if link not in visited:
                            to_visit.append((link, depth + 1))
                
                # 延迟
                time.sleep(random.uniform(*self.delay_range))
                
            except Exception as e:
                logger.error(f"爬取失败 {current_url}: {e}")
                continue
        
        return downloaded_files