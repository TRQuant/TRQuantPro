"""
文件名: code_10_12___init__.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

"""
网页爬虫工具
基于 requests + Beautiful Soup
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
from typing import List, Optional, Dict
from pathlib import Path
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


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
        
        # 配置代理
        if proxy_config:
            self.session.proxies.update(proxy_config)
    
    def collect(self, url: str, max_depth: int = 2,
                allowed_domains: Optional[List[str]] = None,
                allowed_patterns: Optional[List[str]] = None) -> List[Path]:
        """
        爬取网页
        
        Args:
            url: 起始URL
            max_depth: 最大爬取深度
            allowed_domains: 允许的域名列表
            allowed_patterns: 允许的URL模式（正则表达式）
        
        Returns:
            下载的文件路径列表
        """
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
                
                # 检查robots.txt
                if self.respect_robots:
                    if not self._check_robots(current_url):
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
    
    def _check_robots(self, url: str) -> bool:
        """检查robots.txt"""
        # 简化实现，实际应该解析robots.txt
        return True
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str, 
                      allowed_patterns: Optional[List[str]] = None) -> List[str]:
        """提取链接"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(base_url, href)
            
            if allowed_patterns:
                import re
                if not any(re.match(pattern, absolute_url) for pattern in allowed_patterns):
                    continue
            
            links.append(absolute_url)
        
        return links
    
    def _save_content(self, url: str, content: str) -> Path:
        """保存内容"""
        # 生成文件名
        parsed = urlparse(url)
        filename = parsed.path.strip('/').replace('/', '_') or 'index'
        filename = filename[:100]  # 限制长度
        
        file_path = self.output_dir / f"{filename}.txt"
        file_path.write_text(content, encoding='utf-8')
        
        return file_path