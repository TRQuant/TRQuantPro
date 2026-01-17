# TRQuant 知识库完整指南

> **版本**: v1.0  
> **更新**: 2026-01-16  
> **目的**: 知识库内容、功能、跨平台同步和补充机制完整说明

---

## 📚 知识库概览

### 核心定位

TRQuant知识库是一个**RAG（检索增强生成）知识库系统**，为AI助手提供结构化的量化交易知识支持。

### 功能特性

1. **语义搜索** - 使用向量嵌入实现语义相似度搜索
2. **混合检索** - 向量搜索 + 关键词搜索 + RRF融合
3. **知识管理** - 知识条目的增删改查、分类、标签
4. **跨平台同步** - Git同步JSON文件，Windows重新构建向量索引

---

## 📊 知识库内容

### 目录结构

```
.trquant/dev/knowledge/
├── knowledge_base.json              # 主知识库（2.5GB，包含大量文档）
├── joinquant_backtest_kb.json       # 聚宽回测知识库（20KB）
├── strategy_knowledge/              # 策略知识库目录
│   ├── chen_xiaoqun_kb.json        # 陈小群策略知识库
│   ├── summary.json                # 策略知识库摘要
│   ├── crawl_instructions.json     # 爬取指令
│   └── README.md                   # 使用指南
├── vector_index/                    # 向量索引（ChromaDB，69MB）
│   ├── chroma.sqlite3              # ChromaDB数据库
│   ├── index_meta.json             # 索引元数据
│   ├── strategy_kb_meta.json       # 策略知识库索引元数据
│   └── [多个UUID目录]               # ChromaDB集合数据
├── raw_data/                        # 原始数据（爬取的HTML等）
└── processed_data/                  # 处理后的数据
```

### 知识库内容分类

#### 1. 主知识库 (`knowledge_base.json`)

**大小**: 2.5GB  
**格式**: JSON（包含大量知识条目）

**内容来源**:
- BulletTrade文档（GitHub + 网站，14个页面）
- vibe-coding-cn开发指南
- TRQuant系统开发文档（36+个相关文档）
- 聚宽平台文档
- 策略知识库
- 开发最佳实践

**知识条目结构**:
```json
{
  "items": [
    {
      "id": "kb_xxx",
      "title": "知识条目标题",
      "content": "知识内容（Markdown格式）",
      "type": "reference|strategy|api|best_practice",
      "tags": ["标签1", "标签2"],
      "source": "来源URL",
      "platform": "平台名称（如JoinQuant、BulletTrade）",
      "created_at": "2026-01-09 12:00:00",
      "useful_count": 0,
      "_score": 0
    }
  ],
  "updated_at": "2026-01-09 12:00:00"
}
```

**知识类型**:
- `reference` - 参考文档（API文档、使用指南等）
- `strategy` - 策略知识（策略案例、策略模板）
- `api` - API文档（函数说明、参数、示例）
- `best_practice` - 最佳实践（开发经验、问题解决）

#### 2. 聚宽回测知识库 (`joinquant_backtest_kb.json`)

**大小**: 20KB  
**内容**: 聚宽回测引擎相关文档和最佳实践

#### 3. 策略知识库 (`strategy_knowledge/`)

**陈小群策略知识库** (`chen_xiaoqun_kb.json`):
- **条目数**: 9条
- **知识类型**:
  - 策略类 (strategy): 6条 (66.7%)
  - 案例分析 (case_study): 2条 (22.2%)
  - 仓位管理 (position_management): 1条 (11.1%)

**内容来源**:
- 本地文件导入（6个）
- 网络搜索增强（3条）

---

## 🔧 技术架构

### 存储层

1. **JSON文件** - 知识库元数据存储
   - 位置: `.trquant/dev/knowledge/knowledge_base.json`
   - 格式: JSON（包含所有知识条目）
   - 大小: 2.5GB（包含大量文本内容）

2. **ChromaDB** - 向量索引存储
   - 位置: `.trquant/dev/knowledge/vector_index/`
   - 格式: ChromaDB本地持久化存储
   - 大小: 69MB
   - 集合: `knowledge_base`（主知识库）, `strategy_knowledge_base`（策略知识库）

### Embedding模型

- **模型**: `paraphrase-multilingual-MiniLM-L12-v2`
- **提供商**: sentence-transformers
- **向量维度**: 384
- **特点**:
  - ✅ 支持中英文
  - ✅ 轻量级（约80MB）
  - ✅ 本地部署，无需API密钥
  - ✅ 适合语义相似度搜索

### 检索方式

#### 1. 向量语义搜索

使用sentence-transformers生成查询向量，在ChromaDB中搜索相似知识条目。

**优点**:
- 支持语义理解（"获取价格" = "get_price"）
- 支持多语言（中英文混合）
- 支持模糊匹配

#### 2. 关键词精确搜索

基于JSON文件内容进行关键词匹配。

**优点**:
- 精确匹配（函数名、API名称）
- 快速检索
- 支持标签过滤

#### 3. 混合检索（推荐）

结合向量搜索和关键词搜索，使用RRF（Reciprocal Rank Fusion）融合结果。

**优点**:
- 兼顾语义理解和精确匹配
- 结果更准确
- 自动选择最佳模式

---

## 🌐 跨平台同步机制

### 核心原则

1. **JSON文件** - 通过Git同步（包含所有知识内容）
2. **向量索引** - 不同步，Windows上重新构建（ChromaDB本地存储，平台相关）
3. **自动同步** - 每日自动同步JSON文件到Git

### Ubuntu端操作

#### 1. 日常使用（无需同步）

```bash
# 知识库搜索（MCP工具）
# 在Cursor Chat中: "请搜索知识库中的get_price函数"

# 或直接使用Python脚本
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python -m mcp_servers.knowledge_search_api search --query "get_price函数"
```

#### 2. 更新知识库后同步到Git

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 1. 添加知识库JSON文件
git add .trquant/dev/knowledge/knowledge_base.json
git add .trquant/dev/knowledge/joinquant_backtest_kb.json
git add .trquant/dev/knowledge/strategy_knowledge/

# 2. 提交
git commit -m "sync: 知识库更新 [描述具体更新内容]"

# 3. 推送到远程
git push origin ope
```

#### 3. 从Git拉取最新知识库

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 1. 拉取最新代码
git pull origin ope

# 2. 重新构建向量索引（可选，如果JSON文件更新）
python -c "from mcp_servers.knowledge_vector_index import build_vector_index; from pathlib import Path; build_vector_index(Path('.trquant/dev/knowledge/knowledge_base.json'), force_rebuild=True)"
```

**注意**: 向量索引会自动检测JSON文件是否更新，通常不需要手动重建。

### Windows端操作

#### 1. 首次安装（从Git克隆后）

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 1. 确保Python虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 2. 安装知识库依赖
pip install sentence-transformers chromadb

# 3. 检查知识库JSON文件是否存在
Test-Path .trquant\dev\knowledge\knowledge_base.json
# 应该返回 True（从Git同步过来的）

# 4. 构建向量索引（首次必需）
python -c "from mcp_servers.knowledge_vector_index import build_vector_index; from pathlib import Path; kb_file = Path('.trquant/dev/knowledge/knowledge_base.json'); result = build_vector_index(kb_file, force_rebuild=True); print(result)"

# 5. 构建策略知识库向量索引（可选）
python -c "from scripts.build_strategy_kb_vector_index import build_strategy_kb_vector_index; result = build_strategy_kb_vector_index(force_rebuild=True); print(result)"
```

#### 2. 日常使用（从Git拉取最新知识库）

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 1. 拉取最新代码
git pull origin windows

# 2. 检查知识库JSON文件是否有更新
$kbFile = ".trquant\dev\knowledge\knowledge_base.json"
$lastModified = (Get-Item $kbFile).LastWriteTime
Write-Host "知识库最后修改时间: $lastModified"

# 3. 重新构建向量索引（如果JSON文件更新）
python -c "from mcp_servers.knowledge_vector_index import build_vector_index; from pathlib import Path; kb_file = Path('.trquant/dev/knowledge/knowledge_base.json'); result = build_vector_index(kb_file, force_rebuild=False); print(result)"
```

**注意**: 向量索引构建会根据JSON文件的修改时间自动判断是否需要重建。

#### 3. 更新知识库后同步到Git

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 1. 添加知识库JSON文件
git add .trquant\dev\knowledge\knowledge_base.json
git add .trquant\dev\knowledge\joinquant_backtest_kb.json
git add .trquant\dev\knowledge\strategy_knowledge\

# 2. 提交
git commit -m "sync: 知识库更新 [描述具体更新内容]"

# 3. 推送到远程
git push origin windows

# ⚠️ 注意：不要提交 vector_index 目录！
# vector_index 目录应在 .gitignore 中，或手动排除
```

---

## 🔄 自动同步机制

### Ubuntu端（Crontab）

```bash
# 编辑crontab
crontab -e

# 添加每日同步任务（每天9点）
0 9 * * * /home/taotao/.cursor/worktrees/TRQuant/ope/scripts/sync/sync_kb_daily.sh
```

**同步脚本**: `scripts/sync/sync_kb_daily.sh`
- 检查知识库JSON文件是否有更改
- 如果有更改，自动提交并推送到Git

### Windows端（任务计划程序）

**同步脚本**: `scripts/sync/sync_kb_daily.ps1`

**添加到任务计划程序**:
1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器: 每天9:00
4. 操作: 启动程序
   - 程序: `powershell.exe`
   - 参数: `-File "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\scripts\sync\sync_kb_daily.ps1"`
5. 保存任务

**脚本功能**:
- 检查知识库JSON文件是否有更改
- 如果有更改，自动提交并推送到Git
- 记录日志到 `.sync_kb_daily.log`

---

## 🆕 知识库补充机制

### 1. 从文档添加知识

#### 方式1: 使用MCP工具（推荐）

```python
# 在Cursor Chat中
"请将docs/MUST_READ/01_QUICK_START.md添加到知识库"
```

#### 方式2: 使用Python脚本

```bash
# Ubuntu
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python scripts/kb/add_doc_to_kb.py --file docs/MUST_READ/01_QUICK_START.md --type reference

# Windows
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
python scripts\kb\add_doc_to_kb.py --file docs\MUST_READ\01_QUICK_START.md --type reference
```

### 2. 从网页爬取添加知识

#### 方式1: 使用MCP工具（推荐）

```python
# 在Cursor Chat中
"请爬取 https://www.joinquant.com/help/api/help?name=JQData 并添加到知识库"
```

#### 方式2: 使用Python脚本

```bash
# Ubuntu
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python scripts/kb/kb_batch_crawl.py --platform JoinQuant --build-index

# Windows
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
python scripts\kb\kb_batch_crawl.py --platform JoinQuant --build-index
```

### 3. 手动添加知识条目

#### 方式1: 直接编辑JSON文件（不推荐）

⚠️ **警告**: `knowledge_base.json` 文件过大（2.5GB），直接编辑可能导致文件损坏。

#### 方式2: 使用Python脚本（推荐）

```python
# 创建脚本 scripts/kb/add_kb_item.py
from pathlib import Path
import json
from datetime import datetime

def add_kb_item(title: str, content: str, type: str = "reference", tags: list = None, source: str = None):
    """添加知识条目到知识库"""
    kb_file = Path(".trquant/dev/knowledge/knowledge_base.json")
    
    # 加载知识库
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # 创建新条目
    new_item = {
        "id": f"kb_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "title": title,
        "content": content,
        "type": type,
        "tags": tags or [],
        "source": source or "",
        "platform": "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "useful_count": 0,
        "_score": 0
    }
    
    # 添加到知识库
    kb["items"].append(new_item)
    kb["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加知识条目: {new_item['id']}")
    return new_item["id"]

# 使用示例
if __name__ == "__main__":
    add_kb_item(
        title="新的策略知识",
        content="这是策略的详细说明...",
        type="strategy",
        tags=["策略", "量化"],
        source="https://example.com"
    )
```

### 4. 从其他知识库合并

#### 策略知识库合并

```bash
# Ubuntu
python scripts/kb/merge_strategy_kb.py --source .trquant/dev/knowledge/strategy_knowledge/chen_xiaoqun_kb.json --target .trquant/dev/knowledge/knowledge_base.json

# Windows
python scripts\kb\merge_strategy_kb.py --source .trquant\dev\knowledge\strategy_knowledge\chen_xiaoqun_kb.json --target .trquant\dev\knowledge\knowledge_base.json
```

---

## 🔍 知识库搜索

### 方式1: 使用MCP工具（推荐）

在Cursor Chat中：
```
"请搜索知识库中的get_price函数"
"请搜索策略相关的知识"
"请搜索BulletTrade回测配置"
```

### 方式2: 使用Python脚本

```bash
# Ubuntu
python -m mcp_servers.knowledge_search_api search --query "get_price函数" --limit 10

# Windows
python -m mcp_servers.knowledge_search_api search --query "get_price函数" --limit 10
```

### 方式3: 使用kb_manager.py

```bash
# Ubuntu
python scripts/kb/kb_manager.py search --query "策略开发" --limit 10

# Windows
python scripts\kb\kb_manager.py search --query "策略开发" --limit 10
```

---

## ⚠️ 重要注意事项

### 1. 文件大小

- **知识库JSON文件**: 2.5GB（非常大）
- **向量索引**: 69MB（相对较小）
- **注意**: JSON文件过大，直接编辑可能导致文件损坏，建议使用脚本操作

### 2. Git同步策略

- ✅ **同步**: `knowledge_base.json`, `joinquant_backtest_kb.json`, `strategy_knowledge/` 目录
- ❌ **不同步**: `vector_index/` 目录（Windows上重新构建）
- ❌ **不同步**: `raw_data/`, `processed_data/` 目录（临时文件）

### 3. 向量索引重建

- **何时重建**: 
  - 首次安装（Windows端）
  - JSON文件更新后（自动检测）
  - 手动强制重建（`force_rebuild=True`）
- **重建时间**: 
  - 2.5GB JSON文件: 约10-30分钟（取决于硬件）
  - 20KB JSON文件: 约1-2秒

### 4. 平台差异

- **Ubuntu端**: 向量索引已构建，直接使用
- **Windows端**: 需要从Git拉取JSON文件后重新构建向量索引
- **原因**: ChromaDB本地存储格式可能因平台而异，重新构建确保兼容性

---

## 🔧 故障排除

### 问题1: 向量索引构建失败

**症状**: 
```
ImportError: No module named 'sentence_transformers'
```

**解决方案**:
```bash
# Ubuntu
pip install sentence-transformers chromadb

# Windows
.\venv\Scripts\Activate.ps1
pip install sentence-transformers chromadb
```

### 问题2: 知识库JSON文件过大

**症状**: 文件读取超时或内存不足

**解决方案**:
- 使用流式读取（分批处理）
- 考虑拆分知识库为多个小文件
- 使用数据库存储替代JSON文件（未来优化）

### 问题3: Git同步冲突

**症状**: 
```
error: Your local changes to 'knowledge_base.json' would be overwritten by merge
```

**解决方案**:
```bash
# 1. 备份本地更改
cp .trquant/dev/knowledge/knowledge_base.json .trquant/dev/knowledge/knowledge_base.json.bak

# 2. 暂存本地更改
git stash

# 3. 拉取远程更改
git pull origin ope  # 或 windows

# 4. 恢复本地更改并手动合并
git stash pop
# 手动合并冲突后，重新提交
```

### 问题4: 向量索引不更新

**症状**: 搜索结果显示旧数据

**解决方案**:
```bash
# 强制重建向量索引
python -c "from mcp_servers.knowledge_vector_index import build_vector_index; from pathlib import Path; build_vector_index(Path('.trquant/dev/knowledge/knowledge_base.json'), force_rebuild=True)"
```

---

## 📝 最佳实践

### 1. 知识库更新流程

1. **Ubuntu端更新知识库**
   ```bash
   # 添加新知识条目
   python scripts/kb/add_kb_item.py ...
   
   # 提交并推送
   git add .trquant/dev/knowledge/knowledge_base.json
   git commit -m "sync: 知识库更新"
   git push origin ope
   ```

2. **Windows端同步**
   ```powershell
   # 拉取最新知识库
   git pull origin windows
   
   # 重新构建向量索引（自动检测，通常不需要手动）
   ```

### 2. 知识库维护

- **定期清理**: 删除重复或过时的知识条目
- **定期验证**: 验证知识条目的准确性和相关性
- **定期备份**: 备份知识库JSON文件到其他位置

### 3. 性能优化

- **向量索引缓存**: 向量索引已缓存，搜索速度快
- **JSON文件优化**: 考虑拆分大文件为多个小文件（未来优化）
- **检索优化**: 使用混合检索（向量+关键词）获得最佳结果

---

## 📚 相关文档

- `docs/KB_ARCHITECTURE_DESIGN.md` - 知识库架构设计
- `docs/KB_FRAMEWORK_DETAILS.md` - 知识库框架详解
- `docs/CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南
- `scripts/kb/README.md` - 知识库管理工具文档
- `.trquant/dev/knowledge/strategy_knowledge/README.md` - 策略知识库使用指南

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
