#!/usr/bin/env python3
"""
代码文件管理系统

功能：
1. 从文档中提取代码并存储到代码库
2. 管理代码文件的版本
3. 将代码库中的代码同步到文档
"""

import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeManager:
    """代码管理器"""
    
    def __init__(self, db_config: Dict, code_library_dir: str = "code_library"):
        """
        初始化代码管理器
        
        Args:
            db_config: 数据库配置
            code_library_dir: 代码库目录
        """
        self.db_config = db_config
        self.code_library_dir = Path(code_library_dir)
        self.code_library_dir.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表"""
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        # 创建代码文件表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_files (
                id SERIAL PRIMARY KEY,
                code_id VARCHAR(100) UNIQUE NOT NULL,
                chapter VARCHAR(50) NOT NULL,
                section VARCHAR(100) NOT NULL,
                function_name VARCHAR(100),
                file_path VARCHAR(255) NOT NULL,
                code_type VARCHAR(50) NOT NULL,
                language VARCHAR(20) DEFAULT 'python',
                description TEXT,
                design_principles TEXT,
                usage_scenarios TEXT,
                version VARCHAR(20) DEFAULT '1.0.0',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                author VARCHAR(100),
                status VARCHAR(20) DEFAULT 'active'
            )
        """)
        
        # 创建代码版本表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_versions (
                id SERIAL PRIMARY KEY,
                code_id VARCHAR(100) NOT NULL,
                version VARCHAR(20) NOT NULL,
                code_content TEXT NOT NULL,
                change_log TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                created_by VARCHAR(100),
                FOREIGN KEY (code_id) REFERENCES code_files(code_id)
            )
        """)
        
        # 创建代码引用表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_references (
                id SERIAL PRIMARY KEY,
                code_id VARCHAR(100) NOT NULL,
                document_path VARCHAR(255) NOT NULL,
                line_number INTEGER,
                context TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                FOREIGN KEY (code_id) REFERENCES code_files(code_id)
            )
        """)
        
        # 创建索引
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code_files_chapter 
            ON code_files(chapter, section)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code_files_code_id 
            ON code_files(code_id)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code_versions_code_id 
            ON code_versions(code_id, version)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code_references_code_id 
            ON code_references(code_id)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_code_references_document 
            ON code_references(document_path)
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("数据库表初始化完成")
    
    def extract_code_from_doc(self, md_file: Path) -> List[Dict]:
        """
        从Markdown文件中提取代码块
        
        Args:
            md_file: Markdown文件路径
        
        Returns:
            代码块列表
        """
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配代码块：```python ... ```
        pattern = r'```python\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        code_blocks = []
        for i, match in enumerate(matches, 1):
            code_content = match.group(1).strip()
            
            # 跳过空代码块
            if not code_content or len(code_content) < 10:
                continue
            
            # 提取函数/类名
            func_match = re.search(r'def\s+(\w+)|class\s+(\w+)', code_content)
            func_name = func_match.group(1) if func_match and func_match.group(1) else \
                       (func_match.group(2) if func_match and func_match.group(2) else None)
            
            # 提取设计原理说明
            design_principles = self._extract_design_principles(code_content)
            
            # 生成代码ID
            chapter = md_file.parent.name
            section = self._extract_section(md_file, match.start())
            code_id = f"{section}.{func_name or f'code_{i}'}"
            
            # 计算代码哈希
            code_hash = hashlib.md5(code_content.encode()).hexdigest()[:8]
            
            code_blocks.append({
                'code_id': code_id,
                'chapter': chapter,
                'section': section,
                'function_name': func_name,
                'code_content': code_content,
                'design_principles': design_principles,
                'code_hash': code_hash,
                'line_number': content[:match.start()].count('\n') + 1,
                'document_path': str(md_file)
            })
        
        return code_blocks
    
    def _extract_section(self, md_file: Path, position: int) -> str:
        """从文档中提取章节号"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找位置之前的最后一个章节标题
        before_content = content[:position]
        section_match = re.search(r'<h2[^>]*id="section-([^"]+)"', before_content)
        if section_match:
            return section_match.group(1)
        
        # 如果没有找到，尝试从文件名提取
        filename = md_file.stem
        section_match = re.search(r'(\d+\.\d+)', filename)
        return section_match.group(1) if section_match else "unknown"
    
    def _extract_design_principles(self, code_content: str) -> Optional[str]:
        """从代码注释中提取设计原理"""
        # 查找设计原理说明块
        pattern = r'\*\*设计原理\*\*[：:]\s*\n(.*?)(?=\*\*|$)'
        match = re.search(pattern, code_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def save_code_file(self, code_block: Dict) -> Path:
        """
        保存代码到文件
        
        Args:
            code_block: 代码块字典
        
        Returns:
            保存的文件路径
        """
        chapter_dir = self.code_library_dir / code_block['chapter'] / code_block['section']
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        safe_code_id = code_block['code_id'].replace('.', '_').replace('-', '_')
        file_path = chapter_dir / f"{safe_code_id}.py"
        
        # 保存代码
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_block['code_content'])
        
        logger.info(f"保存代码文件: {file_path}")
        return file_path
    
    def register_code(self, code_block: Dict, file_path: Path, author: str = "system"):
        """
        注册代码到数据库
        
        Args:
            code_block: 代码块字典
            file_path: 代码文件路径
            author: 作者
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        try:
            # 检查代码是否已存在
            cur.execute("SELECT code_id, version FROM code_files WHERE code_id = %s", (code_block['code_id'],))
            existing = cur.fetchone()
            
            if existing:
                # 更新现有代码
                code_id, current_version = existing
                
                # 检查代码内容是否变化
                cur.execute("""
                    SELECT code_content FROM code_versions
                    WHERE code_id = %s AND version = %s
                """, (code_id, current_version))
                old_code = cur.fetchone()
                
                if old_code and old_code[0] != code_block['code_content']:
                    # 代码有变化，创建新版本
                    new_version = self._increment_version(current_version)
                    
                    # 插入新版本
                    cur.execute("""
                        INSERT INTO code_versions (code_id, version, code_content, change_log, created_by)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        code_id,
                        new_version,
                        code_block['code_content'],
                        "自动更新",
                        author
                    ))
                    
                    # 更新代码文件记录
                    cur.execute("""
                        UPDATE code_files SET
                            file_path = %s,
                            design_principles = %s,
                            version = %s,
                            updated_at = NOW()
                        WHERE code_id = %s
                    """, (
                        str(file_path),
                        code_block.get('design_principles'),
                        new_version,
                        code_id
                    ))
                    
                    logger.info(f"更新代码: {code_id} v{current_version} -> v{new_version}")
                else:
                    # 代码无变化，只更新元数据
                    cur.execute("""
                        UPDATE code_files SET
                            file_path = %s,
                            design_principles = %s,
                            updated_at = NOW()
                        WHERE code_id = %s
                    """, (
                        str(file_path),
                        code_block.get('design_principles'),
                        code_id
                    ))
            else:
                # 插入新代码
                cur.execute("""
                    INSERT INTO code_files (
                        code_id, chapter, section, function_name, file_path,
                        code_type, language, design_principles, version, author
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    code_block['code_id'],
                    code_block['chapter'],
                    code_block['section'],
                    code_block.get('function_name'),
                    str(file_path),
                    'function' if code_block.get('function_name') else 'example',
                    'python',
                    code_block.get('design_principles'),
                    '1.0.0',
                    author
                ))
                
                # 插入初始版本
                cur.execute("""
                    INSERT INTO code_versions (code_id, version, code_content, created_by)
                    VALUES (%s, %s, %s, %s)
                """, (
                    code_block['code_id'],
                    '1.0.0',
                    code_block['code_content'],
                    author
                ))
                
                logger.info(f"注册新代码: {code_block['code_id']}")
            
            # 记录代码引用
            cur.execute("""
                INSERT INTO code_references (code_id, document_path, line_number, context)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                code_block['code_id'],
                code_block['document_path'],
                code_block.get('line_number'),
                code_block.get('function_name', '')
            ))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"注册代码失败: {e}")
            raise
        finally:
            cur.close()
            conn.close()
    
    def _increment_version(self, version: str, level: str = 'patch') -> str:
        """递增版本号"""
        parts = version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if level == 'major':
            major += 1
            minor = 0
            patch = 0
        elif level == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def get_code(self, code_id: str, version: str = None) -> Optional[Dict]:
        """
        获取代码
        
        Args:
            code_id: 代码ID
            version: 版本号（可选，默认最新版本）
        
        Returns:
            代码字典
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        if version:
            cur.execute("""
                SELECT cf.*, cv.code_content
                FROM code_files cf
                JOIN code_versions cv ON cf.code_id = cv.code_id
                WHERE cf.code_id = %s AND cv.version = %s
            """, (code_id, version))
        else:
            cur.execute("""
                SELECT cf.*, cv.code_content
                FROM code_files cf
                JOIN code_versions cv ON cf.code_id = cv.code_id
                WHERE cf.code_id = %s AND cv.version = cf.version
            """, (code_id,))
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return {
                'code_id': result[0],
                'chapter': result[2],
                'section': result[3],
                'function_name': result[4],
                'file_path': result[5],
                'code_type': result[6],
                'language': result[7],
                'description': result[8],
                'design_principles': result[9],
                'version': result[11],
                'code_content': result[16]
            }
        return None
    
    def update_code(self, code_id: str, new_code: str, change_log: str = "", author: str = "system"):
        """
        更新代码
        
        Args:
            code_id: 代码ID
            new_code: 新代码内容
            change_log: 变更日志
            author: 作者
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        try:
            # 获取当前版本
            cur.execute("SELECT version FROM code_files WHERE code_id = %s", (code_id,))
            result = cur.fetchone()
            if not result:
                raise ValueError(f"代码不存在: {code_id}")
            
            current_version = result[0]
            new_version = self._increment_version(current_version)
            
            # 插入新版本
            cur.execute("""
                INSERT INTO code_versions (code_id, version, code_content, change_log, created_by)
                VALUES (%s, %s, %s, %s, %s)
            """, (code_id, new_version, new_code, change_log, author))
            
            # 更新代码文件记录
            cur.execute("""
                UPDATE code_files SET
                    version = %s,
                    updated_at = NOW()
                WHERE code_id = %s
            """, (new_version, code_id))
            
            # 更新代码文件
            cur.execute("SELECT file_path FROM code_files WHERE code_id = %s", (code_id,))
            file_path = Path(cur.fetchone()[0])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            conn.commit()
            logger.info(f"更新代码: {code_id} v{current_version} -> v{new_version}")
        except Exception as e:
            conn.rollback()
            logger.error(f"更新代码失败: {e}")
            raise
        finally:
            cur.close()
            conn.close()
    
    def sync_code_to_docs(self, docs_dir: Path, dry_run: bool = False):
        """
        将代码库中的代码同步到文档
        
        Args:
            docs_dir: 文档目录
            dry_run: 是否只预览不实际修改
        """
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        # 获取所有代码引用
        cur.execute("""
            SELECT DISTINCT document_path FROM code_references
        """)
        doc_paths = [row[0] for row in cur.fetchall()]
        
        for doc_path in doc_paths:
            doc_file = Path(doc_path)
            if not doc_file.exists():
                continue
            
            # 获取该文档的所有代码引用
            cur.execute("""
                SELECT cr.code_id, cr.line_number, cf.version
                FROM code_references cr
                JOIN code_files cf ON cr.code_id = cf.code_id
                WHERE cr.document_path = %s
            """, (doc_path,))
            
            references = cur.fetchall()
            
            if references:
                self._update_doc_with_code(doc_file, references, dry_run)
        
        cur.close()
        conn.close()
    
    def _update_doc_with_code(self, doc_file: Path, references: List, dry_run: bool):
        """更新文档中的代码"""
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 为每个引用更新代码
        for code_id, line_number, version in references:
            code_info = self.get_code(code_id, version)
            if not code_info:
                continue
            
            # 查找并替换代码块
            pattern = rf'```python\n(.*?<!-- CODE_REF: {code_id} -->.*?)\n```'
            replacement = f"```python\n<!-- CODE_REF: {code_id} v{version} -->\n{code_info['code_content']}\n```"
            
            if re.search(pattern, content, re.DOTALL):
                if not dry_run:
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                    logger.info(f"更新文档代码: {doc_file} - {code_id}")
                else:
                    logger.info(f"[预览] 将更新文档代码: {doc_file} - {code_id}")
        
        if not dry_run:
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(content)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='代码文件管理系统')
    parser.add_argument('--action', choices=['extract', 'sync', 'update'], required=True,
                       help='操作类型：extract=提取代码，sync=同步到文档，update=更新代码')
    parser.add_argument('--docs-dir', type=str, required=True,
                       help='文档目录')
    parser.add_argument('--code-lib-dir', type=str, default='code_library',
                       help='代码库目录')
    parser.add_argument('--db-config', type=str, required=True,
                       help='数据库配置文件路径')
    parser.add_argument('--code-id', type=str,
                       help='代码ID（update操作时必需）')
    parser.add_argument('--new-code-file', type=str,
                       help='新代码文件路径（update操作时必需）')
    parser.add_argument('--change-log', type=str, default='',
                       help='变更日志')
    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，不实际修改文件')
    
    args = parser.parse_args()
    
    # 加载数据库配置
    with open(args.db_config, 'r') as f:
        db_config = json.load(f)
    
    manager = CodeManager(db_config, args.code_lib_dir)
    
    if args.action == 'extract':
        # 提取代码
        docs_dir = Path(args.docs_dir)
        for md_file in docs_dir.rglob('*.md'):
            if md_file.name.startswith('00') or md_file.name.endswith('_CN.md'):
                code_blocks = manager.extract_code_from_doc(md_file)
                for code_block in code_blocks:
                    file_path = manager.save_code_file(code_block)
                    manager.register_code(code_block, file_path)
                logger.info(f"处理文档: {md_file}，提取 {len(code_blocks)} 个代码块")
    
    elif args.action == 'sync':
        # 同步到文档
        manager.sync_code_to_docs(Path(args.docs_dir), args.dry_run)
    
    elif args.action == 'update':
        # 更新代码
        if not args.code_id or not args.new_code_file:
            parser.error("update操作需要--code-id和--new-code-file参数")
        
        with open(args.new_code_file, 'r', encoding='utf-8') as f:
            new_code = f.read()
        
        manager.update_code(args.code_id, new_code, args.change_log)


if __name__ == '__main__':
    main()

