"""
网页爬虫工具
基于 Scrapy 和 Beautiful Soup
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
        初始化爬虫
        
        Args:
            output_dir: 输出目录
            delay_range: 请求延迟范围（秒）
            respect_robots: 是否遵守robots.txt
            proxy_config: 代理配置
            max_retries: 最大重试次数
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
                    if not self._check_robots_txt(current_url):
                        logger.warning(f"Skipping {current_url} (robots.txt)")
                        continue
                
                # 下载页面
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                
                # 保存HTML
                file_path = self._save_html(current_url, response.text)
                downloaded_files.append(file_path)
                
                logger.info(f"Downloaded: {current_url} -> {file_path}")
                
                # 解析链接
                if depth < max_depth:
                    links = self._extract_links(response.text, current_url)
                    for link in links:
                        # 检查URL模式
                        if allowed_patterns:
                            import re
                            if not any(re.match(pattern, link) for pattern in allowed_patterns):
                                continue
                        to_visit.append((link, depth + 1))
                
                # 延迟
                time.sleep(random.uniform(*self.delay_range))
                
            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")
        
        return downloaded_files
    
    def _check_robots_txt(self, url: str) -> bool:
        """检查robots.txt（简化版）"""
        # TODO: 实现完整的robots.txt检查
        # 可以使用 urllib.robotparser
        return True
    
    def _save_html(self, url: str, html: str) -> Path:
        """保存HTML文件"""
        parsed = urlparse(url)
        # 生成安全的文件名
        filename = f"{parsed.netloc}_{parsed.path.replace('/', '_').replace('?', '_')}.html"
        filename = filename[:200]  # 限制文件名长度
        file_path = self.output_dir / filename
        file_path.write_text(html, encoding='utf-8')
        return file_path
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """提取链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            link = urljoin(base_url, a['href'])
            if link.startswith('http'):
                links.append(link)
        return links

