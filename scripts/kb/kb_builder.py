#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 知识库系统构建工具
==========================

根据PDF方案实现完整的知识库系统：
1. 知识采集（多源数据抓取）
2. 数据清洗与解析
3. 向量知识库构建
4. 检索响应系统

运行: python scripts/kb/kb_builder.py
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('KBBuilder')

# 数据目录
KB_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge"
KB_DIR.mkdir(parents=True, exist_ok=True)
KB_JSON_FILE = KB_DIR / "knowledge_base.json"
VECTOR_INDEX_DIR = KB_DIR / "vector_index"
RAW_DATA_DIR = KB_DIR / "raw_data"
PROCESSED_DATA_DIR = KB_DIR / "processed_data"

for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VECTOR_INDEX_DIR]:
    d.mkdir(parents=True, exist_ok=True)


class KnowledgeBaseBuilder:
    """知识库构建器"""
    
    def __init__(self):
        self.kb_file = KB_JSON_FILE
        self.raw_dir = RAW_DATA_DIR
        self.processed_dir = PROCESSED_DATA_DIR
        self.vector_dir = VECTOR_INDEX_DIR
        
    def load_kb(self) -> Dict:
        """加载知识库"""
        if self.kb_file.exists():
            try:
                return json.loads(self.kb_file.read_text(encoding='utf-8'))
            except Exception as e:
                logger.error(f"加载知识库失败: {e}")
                return {"items": []}
        return {"items": []}
    
    def save_kb(self, kb: Dict) -> bool:
        """保存知识库"""
        try:
            self.kb_file.write_text(
                json.dumps(kb, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            logger.info(f"✅ 知识库已保存: {len(kb.get('items', []))} 条")
            return True
        except Exception as e:
            logger.error(f"保存知识库失败: {e}")
            return False
    
    def add_knowledge(
        self,
        title: str,
        content: str,
        type: str = "reference",
        tags: List[str] = None,
        source: str = "",
        platform: str = ""
    ) -> str:
        """添加知识条目"""
        kb = self.load_kb()
        items = kb.get("items", [])
        
        # 生成ID
        content_hash = hashlib.md5(f"{title}{content}".encode()).hexdigest()[:12]
        kb_id = f"kb_{content_hash}"
        
        # 检查是否已存在
        for item in items:
            if item.get("id") == kb_id:
                logger.info(f"知识条目已存在: {title}")
                return kb_id
        
        # 创建新条目
        new_item = {
            "id": kb_id,
            "title": title,
            "content": content,
            "type": type,
            "tags": tags or [],
            "source": source,
            "platform": platform,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "useful_count": 0,
            "_score": 0
        }
        
        items.append(new_item)
        kb["items"] = items
        kb["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_kb(kb)
        logger.info(f"✅ 已添加知识条目: {title} (ID: {kb_id})")
        
        return kb_id
    
    def build_vector_index(self, force_rebuild: bool = False) -> Dict:
        """构建向量索引"""
        try:
            from mcp_servers.knowledge_vector_index import build_vector_index
            result = build_vector_index(self.kb_file, force_rebuild=force_rebuild)
            # 如果返回成功但items_count为0，尝试从元数据文件读取
            if result.get('success') and result.get('items_count', 0) == 0:
                index_meta_file = self.vector_dir / "index_meta.json"
                if index_meta_file.exists():
                    import json
                    meta = json.loads(index_meta_file.read_text(encoding='utf-8'))
                    result['items_count'] = meta.get('items_count', 0)
                    result['vector_dim'] = meta.get('embedding_dim', 0)
            return result
        except Exception as e:
            logger.error(f"构建向量索引失败: {e}")
            return {"success": False, "error": str(e)}
    
    def clean_and_parse_content(self, raw_content: str, source_type: str = "web") -> Dict:
        """
        清洗和解析内容
        
        Args:
            raw_content: 原始内容
            source_type: 来源类型 (web/pdf/markdown)
            
        Returns:
            解析后的结构化内容
        """
        try:
            from bs4 import BeautifulSoup
            
            if source_type == "web":
                # HTML解析
                soup = BeautifulSoup(raw_content, 'html.parser')
                
                # 移除无用标签
                for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                    tag.decompose()
                
                # 提取标题
                title = ""
                if soup.find('h1'):
                    title = soup.find('h1').get_text(strip=True)
                elif soup.find('title'):
                    title = soup.find('title').get_text(strip=True)
                
                # 提取正文
                content = soup.get_text(separator='\n', strip=True)
                
                # 提取代码块
                code_blocks = []
                for pre in soup.find_all(['pre', 'code']):
                    code_text = pre.get_text(strip=True)
                    if len(code_text) > 20:  # 过滤太短的代码
                        code_blocks.append(code_text)
                
                return {
                    "title": title,
                    "content": content,
                    "code_blocks": code_blocks,
                    "structure": "html"
                }
            
            elif source_type == "markdown":
                # Markdown解析（简单处理）
                lines = raw_content.split('\n')
                title = ""
                content_lines = []
                
                for line in lines:
                    if line.startswith('# '):
                        if not title:
                            title = line[2:].strip()
                    elif line.startswith('## '):
                        content_lines.append(f"\n## {line[3:].strip()}\n")
                    else:
                        content_lines.append(line)
                
                content = '\n'.join(content_lines)
                
                return {
                    "title": title or "Untitled",
                    "content": content,
                    "code_blocks": [],
                    "structure": "markdown"
                }
            
            else:
                # 纯文本
                return {
                    "title": "Untitled",
                    "content": raw_content,
                    "code_blocks": [],
                    "structure": "text"
                }
                
        except Exception as e:
            logger.error(f"内容解析失败: {e}")
            return {
                "title": "Untitled",
                "content": raw_content[:1000],  # 截取前1000字符
                "code_blocks": [],
                "structure": "text"
            }
    
    def chunk_content(self, content: str, max_chunk_size: int = 500) -> List[str]:
        """
        将长文本分块
        
        Args:
            content: 原始内容
            max_chunk_size: 每块最大字符数
            
        Returns:
            文本块列表
        """
        if len(content) <= max_chunk_size:
            return [content]
        
        chunks = []
        paragraphs = content.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_crawled_data(
        self,
        url: str,
        raw_content: str,
        source_type: str = "web",
        platform: str = ""
    ) -> List[str]:
        """
        处理爬取的数据
        
        Args:
            url: 来源URL
            raw_content: 原始内容
            source_type: 来源类型
            platform: 平台名称
            
        Returns:
            添加的知识条目ID列表
        """
        # 清洗和解析
        parsed = self.clean_and_parse_content(raw_content, source_type)
        
        # 分块
        chunks = self.chunk_content(parsed["content"], max_chunk_size=500)
        
        kb_ids = []
        
        # 添加主条目
        main_id = self.add_knowledge(
            title=parsed["title"],
            content=parsed["content"][:2000],  # 限制长度
            type="reference",
            tags=[platform] if platform else [],
            source=url,
            platform=platform
        )
        kb_ids.append(main_id)
        
        # 添加代码块
        for idx, code_block in enumerate(parsed["code_blocks"][:5]):  # 最多5个代码块
            code_id = self.add_knowledge(
                title=f"{parsed['title']} - 代码示例 {idx+1}",
                content=code_block,
                type="code",
                tags=[platform, "code"] if platform else ["code"],
                source=url,
                platform=platform
            )
            kb_ids.append(code_id)
        
        # 如果内容很长，添加分块条目
        if len(chunks) > 1:
            for idx, chunk in enumerate(chunks[1:], 1):  # 跳过第一个（已在主条目中）
                chunk_id = self.add_knowledge(
                    title=f"{parsed['title']} - 片段 {idx+1}",
                    content=chunk,
                    type="reference",
                    tags=[platform, "chunk"] if platform else ["chunk"],
                    source=url,
                    platform=platform
                )
                kb_ids.append(chunk_id)
        
        return kb_ids


def main():
    """主函数"""
    print("=" * 70)
    print("TRQuant 知识库系统构建工具")
    print("=" * 70)
    print()
    
    builder = KnowledgeBaseBuilder()
    
    # 加载知识库
    kb = builder.load_kb()
    print(f"📚 当前知识库: {len(kb.get('items', []))} 条")
    print()
    
    # 构建向量索引
    print("🔨 构建向量索引...")
    result = builder.build_vector_index(force_rebuild=False)
    
    if result.get("success"):
        print(f"✅ 向量索引构建成功")
        print(f"   - 条目数: {result.get('items_count', 0)}")
        print(f"   - 模型: {result.get('model', '')}")
        print(f"   - 向量维度: {result.get('embedding_dim', 0)}")
        print(f"   - 索引路径: {result.get('index_path', '')}")
    else:
        print(f"❌ 向量索引构建失败: {result.get('error', 'Unknown error')}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
