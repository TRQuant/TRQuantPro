#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库网页爬虫

抓取相关网页补充知识库：
1. 量化交易策略文档
2. A股牛市历史分析
3. 因子投资研究
4. 技术指标解析
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime
import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


class KnowledgeWebCrawler:
    """知识库网页爬虫"""
    
    # 预定义的知识源
    KNOWLEDGE_SOURCES = {
        'quantconnect': {
            'name': 'QuantConnect文档',
            'urls': [
                'https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/order-types',
                'https://www.quantconnect.com/docs/v2/writing-algorithms/indicators',
            ],
            'tags': ['量化', 'QuantConnect', '策略']
        },
        'jqdata': {
            'name': '聚宽数据文档',
            'urls': [
                'https://www.joinquant.com/help/api/help',
            ],
            'tags': ['聚宽', 'JQData', '数据']
        },
        'bull_market': {
            'name': 'A股牛市分析',
            'urls': [
                # 可以添加牛市分析相关URL
            ],
            'tags': ['牛市', 'A股', '历史分析']
        }
    }
    
    def __init__(self, output_dir: Optional[Path] = None, verbose: bool = True):
        """
        初始化爬虫
        
        Args:
            output_dir: 输出目录
            verbose: 是否输出详细信息
        """
        self.output_dir = output_dir or Path('output/kb_crawler')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        
        self.crawled_urls: List[str] = []
        self.knowledge_entries: List[Dict] = []
        
        # 尝试导入requests
        try:
            import requests
            from bs4 import BeautifulSoup
            self.requests = requests
            self.BeautifulSoup = BeautifulSoup
            self._can_crawl = True
        except ImportError:
            self._can_crawl = False
            if verbose:
                print("⚠️ 未安装 requests 或 beautifulsoup4，使用预定义知识")
    
    def crawl_all_sources(self, max_urls_per_source: int = 5) -> List[Dict]:
        """
        爬取所有预定义知识源
        
        Args:
            max_urls_per_source: 每个源最大爬取URL数
        
        Returns:
            知识条目列表
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print("🕷️ 知识库网页爬虫")
            print(f"{'='*60}")
        
        for source_id, source_info in self.KNOWLEDGE_SOURCES.items():
            if self.verbose:
                print(f"\n[{source_info['name']}]")
            
            urls = source_info['urls'][:max_urls_per_source]
            
            for url in urls:
                if self._can_crawl:
                    entry = self._crawl_url(url, source_info['tags'])
                    if entry:
                        self.knowledge_entries.append(entry)
                        self.crawled_urls.append(url)
        
        # 添加预定义知识（确保有内容）
        self._add_predefined_knowledge()
        
        if self.verbose:
            print(f"\n✅ 爬取完成: {len(self.knowledge_entries)} 条知识")
        
        # 保存到文件
        self._save_entries()
        
        return self.knowledge_entries
    
    def crawl_url(self, url: str, tags: Optional[List[str]] = None) -> Optional[Dict]:
        """
        爬取单个URL
        
        Args:
            url: 要爬取的URL
            tags: 标签列表
        
        Returns:
            知识条目或None
        """
        return self._crawl_url(url, tags or [])
    
    def _crawl_url(self, url: str, tags: List[str]) -> Optional[Dict]:
        """内部爬取方法"""
        if not self._can_crawl:
            return None
        
        try:
            if self.verbose:
                print(f"  爬取: {url[:60]}...")
            
            response = self.requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                if self.verbose:
                    print(f"    ❌ 状态码: {response.status_code}")
                return None
            
            soup = self.BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title = soup.find('title')
            title_text = title.get_text().strip() if title else urlparse(url).path
            
            # 提取正文
            content_parts = []
            
            # 尝试多种选择器
            for selector in ['article', 'main', '.content', '.post-content', '#content']:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_parts.append(content_elem.get_text(separator='\n', strip=True))
                    break
            
            if not content_parts:
                # 提取所有段落
                paragraphs = soup.find_all('p')
                content_parts = [p.get_text(strip=True) for p in paragraphs[:20]]
            
            content = '\n\n'.join(content_parts)
            
            # 限制内容长度
            if len(content) > 10000:
                content = content[:10000] + '...(内容已截断)'
            
            if len(content) < 100:
                if self.verbose:
                    print(f"    ⚠️ 内容过短，跳过")
                return None
            
            entry = {
                'title': title_text[:200],
                'content': content,
                'url': url,
                'tags': tags,
                'crawled_at': datetime.now().isoformat(),
                'type': 'web_crawl'
            }
            
            if self.verbose:
                print(f"    ✅ 提取 {len(content)} 字符")
            
            return entry
        
        except Exception as e:
            if self.verbose:
                print(f"    ❌ 爬取失败: {e}")
            return None
    
    def _add_predefined_knowledge(self):
        """添加预定义知识（确保知识库有内容）"""
        predefined = [
            {
                'title': 'A股历史牛市特征总结',
                'content': '''
# A股历史牛市特征总结

## 第三次牛市（股权分置改革牛，2005-2007）
- **时间**: 2005年7月 - 2007年10月
- **涨幅**: 上证指数从998点涨至6124点（+514%）
- **特征**:
  - 股权分置改革释放制度红利
  - 流动性充裕，居民储蓄入市
  - 全面普涨，小盘股弹性更大
- **因子表现**:
  - 动量因子有效性极高
  - 小市值因子显著
  - 换手率与涨幅正相关

## 第四次牛市（杠杆牛，2014-2015）
- **时间**: 2014年7月 - 2015年6月
- **涨幅**: 上证指数从2000点涨至5178点（+159%）
- **特征**:
  - 融资融券推动杠杆入市
  - 创业板领涨，成长股占优
  - 快牛快熊，波动剧烈
- **因子表现**:
  - 成长因子（营收增长、利润增速）表现优异
  - 动量因子中后期失效
  - 杠杆水平与个股涨幅正相关

## 第五次牛市（结构性牛，2019-2021）
- **时间**: 2019年1月 - 2021年3月
- **涨幅**: 指数涨幅有限，但结构分化明显
- **特征**:
  - 核心资产、新能源赛道领涨
  - 机构化程度提高，抱团现象明显
  - 注册制改革，科创板表现突出
- **因子表现**:
  - ROE因子（盈利质量）最有效
  - 行业动量因子显著
  - 市值因子分化，大票更抗跌

## 牛市操作策略建议
1. **牛市初期**: 重仓小盘股，提高动量因子权重
2. **牛市中期**: 关注板块轮动，缩短调仓周期
3. **牛市末期**: 转向大盘蓝筹，增加防御仓位
4. **风控**: 设置移动止损，避免回撤吞噬利润
''',
                'tags': ['牛市', 'A股', '历史分析', '因子'],
                'type': 'predefined'
            },
            {
                'title': '量化因子投资指南',
                'content': '''
# 量化因子投资指南

## 核心因子分类

### 1. 动量因子
- **定义**: 过去一段时间的价格涨跌幅
- **常用周期**: 5日、20日、60日
- **应用**: 追涨策略、趋势跟踪
- **注意**: 牛市有效，熊市可能失效

### 2. 价值因子
- **定义**: 股票估值水平
- **指标**: PE、PB、PS、PCF
- **应用**: 低估值选股
- **注意**: 价值陷阱风险

### 3. 质量因子
- **定义**: 公司盈利能力和稳定性
- **指标**: ROE、ROA、毛利率、净利率
- **应用**: 选择优质公司
- **特点**: 长期有效，回撤较小

### 4. 规模因子
- **定义**: 公司市值大小
- **应用**: 小盘股策略
- **注意**: A股小市值效应显著

### 5. 波动率因子
- **定义**: 价格波动程度
- **应用**: 低波动策略
- **特点**: 防御性强

## 因子组合方法

### 等权加权
- 各因子权重相等
- 简单稳定

### IC加权
- 根据因子IC值分配权重
- 动态调整

### 最大化IR
- 信息比率最大化
- 考虑因子相关性

## 风险控制

### 止损策略
- 固定止损: -8%到-10%
- 移动止损: 跟踪最高点回撤

### 仓位管理
- 根据市场状态调整仓位
- 牛市80%-100%，熊市30%-50%

### 分散化
- 行业分散
- 个股分散
- 因子分散
''',
                'tags': ['因子投资', '量化策略', '风控'],
                'type': 'predefined'
            },
            {
                'title': 'TRQuant策略开发最佳实践',
                'content': '''
# TRQuant策略开发最佳实践

## 策略开发流程

### 1. 研究阶段
- 使用Jupyter Notebook进行因子研究
- 验证因子有效性（IC、ICIR）
- 回测验证策略逻辑

### 2. 开发阶段
- 在Core模块中实现策略逻辑
- 遵循PEP8编码规范
- 添加完整的错误处理

### 3. 回测阶段
- 使用BulletTrade进行历史回测
- 多时间段验证稳定性
- 分析各项风险指标

### 4. 优化阶段
- 遗传算法参数优化
- 避免过拟合
- 样本外验证

## 代码规范

### 命名规范
- 函数: snake_case
- 类: PascalCase
- 常量: UPPER_CASE

### 文档规范
- 所有公共函数必须有docstring
- 使用类型提示

### 错误处理
- 使用try-except包装关键操作
- 记录详细错误日志
- 提供降级方案

## 性能优化

### 数据缓存
- 使用MongoDB存储历史数据
- 内存缓存热点数据
- 增量更新机制

### 并行计算
- CPU多线程计算因子
- GPU加速技术指标
- 批量处理股票数据

### 代码优化
- 使用numpy/pandas向量化操作
- 避免循环内重复计算
- 减少I/O操作
''',
                'tags': ['TRQuant', '最佳实践', '开发指南'],
                'type': 'predefined'
            },
            {
                'title': '月收益30%策略关键要素',
                'content': '''
# 月收益30%策略关键要素

## 目标分析
- 月收益30% = 年化收益约3000%（复利）
- 这是极高的收益目标
- 只在特定市场环境（强牛市）可能实现

## 实现条件

### 1. 市场环境
- 必须处于牛市中期或后期
- 市场流动性充裕
- 板块轮动活跃

### 2. 策略特征
- 高换手率（周频或更高）
- 集中持仓（3-10只）
- 追涨杀跌（动量策略）
- 杠杆使用（可选但危险）

### 3. 选股条件
- 20日动量 > 15%
- 5日动量 > 5%
- 相对位置 < 70%（还有上涨空间）
- 成交量放大（流动性好）

### 4. 调仓频率
- 至少周频调仓
- 牛市中期可日频

### 5. 风控措施
- 严格止损（-8%）
- 移动止盈
- 仓位动态调整

## 风险警示
⚠️ 高收益必然伴随高风险
⚠️ 可能在一周内亏损30%或更多
⚠️ 不适合作为长期策略
⚠️ 只在确认牛市时使用

## 建议方案
1. 将30%目标分解为：
   - 选股收益：20%
   - 择时收益：10%
2. 控制最大回撤在15%以内
3. 保持良好的夏普比率（>2.0）
''',
                'tags': ['高收益', '牛市策略', '风险'],
                'type': 'predefined'
            }
        ]
        
        for entry in predefined:
            entry['crawled_at'] = datetime.now().isoformat()
            self.knowledge_entries.append(entry)
        
        if self.verbose:
            print(f"\n  添加 {len(predefined)} 条预定义知识")
    
    def _save_entries(self):
        """保存知识条目到文件"""
        filepath = self.output_dir / f"kb_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'count': len(self.knowledge_entries),
                'crawled_urls': self.crawled_urls,
                'entries': self.knowledge_entries
            }, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"  保存到: {filepath}")
    
    def get_entries_for_kb(self) -> List[Dict]:
        """获取可导入知识库的条目格式"""
        return [
            {
                'title': e['title'],
                'content': e['content'],
                'type': 'reference',
                'tags': e.get('tags', []),
                'source': e.get('url', 'predefined')
            }
            for e in self.knowledge_entries
        ]


def main():
    """测试爬虫"""
    crawler = KnowledgeWebCrawler(verbose=True)
    entries = crawler.crawl_all_sources()
    
    print(f"\n总计 {len(entries)} 条知识条目")
    for entry in entries[:3]:
        print(f"\n标题: {entry['title']}")
        print(f"标签: {entry.get('tags', [])}")
        print(f"内容: {entry['content'][:200]}...")


if __name__ == '__main__':
    main()
