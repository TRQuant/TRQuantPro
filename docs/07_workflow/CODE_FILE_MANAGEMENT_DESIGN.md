# 代码文件独立管理系统设计

## 📋 概述

为了便于代码的修改、升级和维护，所有文档中的代码示例应该：
1. **独立存储**：每个代码示例存储在独立的文件中
2. **数据库管理**：使用数据库管理代码文件的元数据和版本
3. **引用机制**：文档中通过引用方式使用代码，而非直接嵌入
4. **版本控制**：支持代码版本管理和升级

## 🗄️ 数据库设计

### 代码文件表（code_files）

```sql
CREATE TABLE code_files (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(100) UNIQUE NOT NULL,  -- 代码唯一标识，如 "3.2.2.analyze_price_dimension"
    chapter VARCHAR(50) NOT NULL,          -- 章节，如 "003_Chapter3_Market_Analysis"
    section VARCHAR(100) NOT NULL,         -- 小节，如 "3.2.2"
    function_name VARCHAR(100),             -- 函数/类名
    file_path VARCHAR(255) NOT NULL,       -- 代码文件路径
    code_type VARCHAR(50) NOT NULL,        -- 代码类型：function, class, module, example
    language VARCHAR(20) DEFAULT 'python',  -- 编程语言
    description TEXT,                       -- 代码描述
    design_principles TEXT,                 -- 设计原理说明
    usage_scenarios TEXT,                   -- 使用场景
    version VARCHAR(20) DEFAULT '1.0.0',    -- 版本号
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    author VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active'     -- active, deprecated, archived
);

CREATE INDEX idx_code_files_chapter ON code_files(chapter, section);
CREATE INDEX idx_code_files_code_id ON code_files(code_id);
```

### 代码版本表（code_versions）

```sql
CREATE TABLE code_versions (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    code_content TEXT NOT NULL,            -- 代码内容
    change_log TEXT,                       -- 变更日志
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    FOREIGN KEY (code_id) REFERENCES code_files(code_id)
);

CREATE INDEX idx_code_versions_code_id ON code_versions(code_id, version);
```

### 代码引用表（code_references）

```sql
CREATE TABLE code_references (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(100) NOT NULL,
    document_path VARCHAR(255) NOT NULL,   -- 文档路径
    line_number INTEGER,                    -- 引用行号
    context TEXT,                           -- 引用上下文
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (code_id) REFERENCES code_files(code_id)
);

CREATE INDEX idx_code_references_code_id ON code_references(code_id);
CREATE INDEX idx_code_references_document ON code_references(document_path);
```

## 📁 文件系统结构

```
code_library/
├── 001_Chapter1_System_Overview/
│   ├── 1.1/
│   │   ├── code_1.1.1.example_function.py
│   │   └── code_1.1.2.another_function.py
│   └── 1.2/
│       └── code_1.2.1.system_architecture.py
├── 002_Chapter2_Data_Source/
│   └── 2.1/
│       └── code_2.1.1.data_source_manager.py
├── 003_Chapter3_Market_Analysis/
│   ├── 3.1/
│   │   └── code_3.1.1.trend_analyzer.py
│   └── 3.2/
│       ├── code_3.2.1.market_status.py
│       └── code_3.2.2.analyze_price_dimension.py
└── ...
```

## 🔧 代码管理工具

### 代码提取脚本

```python
# scripts/extract_code_from_docs.py
"""
从文档中提取代码并存储到代码库
"""
import re
import json
from pathlib import Path
from typing import List, Dict
import psycopg2
from psycopg2.extras import execute_values

class CodeExtractor:
    def __init__(self, db_config: Dict):
        self.conn = psycopg2.connect(**db_config)
        self.code_library_dir = Path("code_library")
        self.code_library_dir.mkdir(exist_ok=True)
    
    def extract_code_blocks(self, md_file: Path) -> List[Dict]:
        """从Markdown文件中提取代码块"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配代码块：```python ... ```
        pattern = r'```python\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        code_blocks = []
        for i, match in enumerate(matches, 1):
            code_content = match.group(1).strip()
            
            # 提取函数/类名
            func_match = re.search(r'def\s+(\w+)|class\s+(\w+)', code_content)
            func_name = func_match.group(1) if func_match else func_match.group(2) if func_match else None
            
            # 生成代码ID
            chapter = md_file.parent.name
            section = self._extract_section(md_file, match.start())
            code_id = f"{section}.{func_name or f'code_{i}'}"
            
            code_blocks.append({
                'code_id': code_id,
                'chapter': chapter,
                'section': section,
                'function_name': func_name,
                'code_content': code_content,
                'line_number': content[:match.start()].count('\n') + 1
            })
        
        return code_blocks
    
    def save_code_file(self, code_block: Dict) -> Path:
        """保存代码到文件"""
        chapter_dir = self.code_library_dir / code_block['chapter'] / code_block['section']
        chapter_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = chapter_dir / f"code_{code_block['code_id'].replace('.', '_')}.py"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_block['code_content'])
        
        return file_path
    
    def register_to_db(self, code_block: Dict, file_path: Path):
        """注册代码到数据库"""
        cur = self.conn.cursor()
        
        # 插入代码文件记录
        cur.execute("""
            INSERT INTO code_files (
                code_id, chapter, section, function_name, file_path,
                code_type, language, version
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (code_id) DO UPDATE SET
                file_path = EXCLUDED.file_path,
                updated_at = NOW()
        """, (
            code_block['code_id'],
            code_block['chapter'],
            code_block['section'],
            code_block['function_name'],
            str(file_path),
            'function' if code_block['function_name'] else 'example',
            'python',
            '1.0.0'
        ))
        
        # 插入代码版本
        cur.execute("""
            INSERT INTO code_versions (code_id, version, code_content)
            VALUES (%s, %s, %s)
        """, (
            code_block['code_id'],
            '1.0.0',
            code_block['code_content']
        ))
        
        self.conn.commit()
        cur.close()
```

### 代码引用生成器

```python
# scripts/generate_code_references.py
"""
生成文档中的代码引用
"""
import re
from pathlib import Path
import psycopg2

class CodeReferenceGenerator:
    def __init__(self, db_config: Dict):
        self.conn = psycopg2.connect(**db_config)
    
    def replace_code_in_doc(self, md_file: Path):
        """将文档中的代码块替换为引用"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配代码块
        pattern = r'```python\n(.*?)```'
        
        def replace_code(match):
            code_content = match.group(1).strip()
            
            # 查找对应的代码ID
            code_id = self._find_code_id(code_content)
            if code_id:
                # 生成引用标记
                return f"```python\n<!-- CODE_REF: {code_id} -->\n{code_content}\n```"
            return match.group(0)
        
        new_content = re.sub(pattern, replace_code, content, flags=re.DOTALL)
        
        # 保存更新后的文档
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    def _find_code_id(self, code_content: str) -> str:
        """根据代码内容查找代码ID"""
        cur = self.conn.cursor()
        
        # 提取函数/类名
        func_match = re.search(r'def\s+(\w+)|class\s+(\w+)', code_content)
        if func_match:
            func_name = func_match.group(1) or func_match.group(2)
            
            cur.execute("""
                SELECT code_id FROM code_files
                WHERE function_name = %s
                ORDER BY updated_at DESC
                LIMIT 1
            """, (func_name,))
            
            result = cur.fetchone()
            cur.close()
            return result[0] if result else None
        
        return None
```

## 📝 使用流程

### 1. 提取代码

```bash
# 从所有文档中提取代码
python scripts/extract_code_from_docs.py \
    --docs-dir extension/AShare-manual/src/pages/ashare-book6 \
    --db-config config/database.json
```

### 2. 更新代码

```python
# 更新代码文件
code_manager = CodeManager(db_config)
code_manager.update_code(
    code_id="3.2.2.analyze_price_dimension",
    new_code=updated_code,
    change_log="添加设计原理说明"
)
```

### 3. 同步到文档

```bash
# 将代码库中的代码同步到文档
python scripts/sync_code_to_docs.py \
    --docs-dir extension/AShare-manual/src/pages/ashare-book6 \
    --code-lib-dir code_library
```

## 🎯 优势

1. **集中管理**：所有代码集中存储，便于查找和修改
2. **版本控制**：支持代码版本管理，可以回滚到历史版本
3. **引用追踪**：可以追踪代码在哪些文档中被引用
4. **批量更新**：修改一处代码，可以批量更新所有引用
5. **代码复用**：相同功能的代码可以复用，避免重复

## 📚 实施计划

1. **阶段1**：设计数据库表结构，创建代码库目录
2. **阶段2**：开发代码提取脚本，从现有文档中提取代码
3. **阶段3**：开发代码管理工具，支持代码的增删改查
4. **阶段4**：开发文档同步工具，将代码库中的代码同步到文档
5. **阶段5**：迁移现有文档，将所有代码改为引用方式

