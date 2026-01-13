# TRQuant 知识库管理工具完整总结

> **更新时间**: 2026-01-09  
> **版本**: 1.0

---

## 📋 概述

TRQuant项目使用**统一开发工具服务器**（`unified_dev_server`）管理知识库，提供多种访问方式：MCP工具、Python API、命令行工具。

---

## 🔧 工具分类

### 1. MCP工具（推荐使用）

**位置**: `mcp_servers/unified_dev_server.py`

通过 `MCPClient` 调用，支持在Cursor Chat中直接使用：

| 工具 | 功能 | 参数 |
|------|------|------|
| `kb.add` | 添加知识条目 | `title`, `content`, `category` |
| `kb.search` | 搜索知识库 | `query`, `category`, `limit` |
| `kb.get_strategy` | 获取策略详情 | `strategy_name` |
| `kb.get_api` | 获取API文档 | `api_name` |
| `kb.best_practices` | 获取最佳实践 | `category` |

**使用示例**:
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='kb.add',
    arguments={
        'title': 'PTrade API文档',
        'content': '...',
        'category': 'PTrade_API'
    }
)
```

---

### 2. Python API

**位置**: `mcp_servers/unified_dev_server.py`

直接导入函数使用：

| 函数 | 功能 | 返回值 |
|------|------|--------|
| `knowledge_add(title, content, type, tags, source)` | 添加知识 | `{"success": True, "knowledge_id": "..."}` |
| `knowledge_search(query, type, limit)` | 搜索知识 | `{"success": True, "results": [...], "total": N}` |
| `knowledge_get(knowledge_id)` | 获取知识详情 | `{"success": True, "item": {...}}` |
| `knowledge_update(knowledge_id, content, tags)` | 更新知识 | `{"success": True, "item": {...}}` |
| `knowledge_mark_useful(knowledge_id)` | 标记有用 | `{"success": True, "useful_count": N}` |
| `knowledge_stats()` | 统计信息 | `{"total": N, "by_type": {...}}` |

**使用示例**:
```python
from mcp_servers.unified_dev_server import knowledge_add, knowledge_search

# 添加知识
result = knowledge_add(
    title="问题标题",
    content="问题描述和解决方案",
    type="lesson",
    tags=["BulletTrade", "回测"],
    source="调试经验"
)

# 搜索知识
result = knowledge_search("BulletTrade", limit=10)
```

---

### 3. 命令行工具

**位置**: `scripts/kb_tool.py`

**命令**:
```bash
# 搜索知识库
./venv/bin/python3 scripts/kb_tool.py search "关键词"
./venv/bin/python3 scripts/kb_tool.py search "关键词" --category bulletrade_debug

# 添加知识
./venv/bin/python3 scripts/kb_tool.py add "标题" "内容" --category bulletrade_debug

# 列出所有知识
./venv/bin/python3 scripts/kb_tool.py list
./venv/bin/python3 scripts/kb_tool.py list --category bulletrade_debug

# 查看最佳实践
./venv/bin/python3 scripts/kb_tool.py best-practices
./venv/bin/python3 scripts/kb_tool.py best-practices --category backtest
```

---

## 📁 存储位置

### 主要知识库文件

1. **统一开发工具知识库**
   - 路径: `.trquant/dev/knowledge/knowledge_base.json`
   - 用途: 开发经验、调试经验、最佳实践
   - 格式: JSON，包含 `items` 和 `stats`

2. **策略知识库**
   - 路径: `.trquant/dev/kb/custom_kb.json`
   - 用途: 策略相关知识和API文档
   - 格式: JSON

3. **文档知识库**
   - 路径: `docs/knowledge_base/`
   - 用途: 分类存储的文档知识库
   - 文件:
     - `bullettrade_kb.json` - BulletTrade相关
     - `joinquant_backtest_kb.json` - 聚宽回测相关
     - `jqfactor_analyzer_kb.json` - 因子分析相关

4. **向量索引**（如果启用）
   - 路径: `.trquant/dev/knowledge/vector_index/`
   - 用途: 向量搜索索引

---

## 🔍 搜索功能

### 混合检索（Hybrid Search）

`knowledge_search()` 支持**混合检索**模式：

1. **向量语义搜索**: 使用嵌入向量进行语义相似度搜索
2. **关键词精确匹配**: 精确匹配API函数名、因子名等
3. **标签优先匹配**: 标签匹配优先级更高
4. **RRF结果融合**: 使用Reciprocal Rank Fusion融合结果

**搜索模式**:
- `auto`: 自动选择最佳模式
- `hybrid`: 混合检索（向量+关键词）
- `keyword`: 仅关键词搜索
- `basic`: 基础文本搜索（回退模式）

---

## 📊 知识类型（Type）

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| `lesson` | 经验教训 | 调试经验、问题解决 |
| `practice` | 最佳实践 | 开发规范、代码模式 |
| `reference` | 参考文档 | API文档、使用指南 |
| `pattern` | 设计模式 | 代码模式、架构模式 |
| `error` | 错误模式 | 常见错误和解决方案 |
| `tip` | 开发技巧 | 实用技巧、优化建议 |
| `rule` | 开发规则 | 编码规范、流程规则 |
| `api_reference` | API参考 | API函数说明 |
| `guide` | 使用指南 | 教程、操作指南 |
| `tutorial` | 安装配置 | 环境配置、安装说明 |

---

## 🏷️ 知识分类（Category）

| 分类 | 说明 | 使用场景 |
|------|------|----------|
| `bulletrade_debug` | BulletTrade调试 | 回测相关问题 |
| `jqdata_api` | JQData API | 数据获取问题 |
| `strategy` | 策略开发 | 策略逻辑问题 |
| `backtest` | 回测配置 | 回测参数问题 |
| `risk` | 风控相关 | 风险管理问题 |
| `code` | 代码规范 | 编码标准问题 |
| `PTrade_API` | PTrade API | PTrade平台相关 |
| `general` | 通用知识 | 其他问题 |

---

## 💡 使用建议

### 开发前
1. 使用 `kb.search` 查找是否有类似问题的解决方案
2. 使用 `kb.best_practices` 查看最佳实践
3. 使用 `kb.get_api` 查看API文档

### 开发中
1. 遇到问题时先搜索知识库
2. 重要发现立即记录（使用 `kb.add`）
3. 记录调试日志

### 开发后
1. 使用 `kb.add` 存入经验
2. 使用 `evidence.add` 记录决策证据
3. 更新相关文档

---

## 🔗 相关文档

- **工具使用指南**: `docs/KB_TOOL_GUIDE.md`
- **标准开发流程**: `docs/STANDARD_DEV_WORKFLOW.md`
- **知识库架构**: `docs/KB_ARCHITECTURE_DESIGN.md`
- **知识库总结**: `docs/knowledge_base/KB_COMPREHENSIVE_SUMMARY.md`

---

## 📝 示例代码

### 完整示例：添加PTrade API知识

```python
from core.mcp.client import MCPClient

client = MCPClient()

result = client.call(
    tool_name='kb.add',
    arguments={
        'title': 'PTrade API: get_history - 获取历史行情',
        'content': '''
# get_history - 获取历史行情

## 函数签名
```python
get_history(security, count, unit='1d', fields=['open', 'high', 'low', 'close', 'volume'], 
            end_date=None, fq='pre', skip_paused=False, df=True)
```

## 参数说明
- security: 股票代码
- count: 获取数量
- unit: 周期（'1d', '1m', '5m'等）
- fields: 字段列表
- end_date: 结束日期
- fq: 复权类型
- skip_paused: 是否跳过停牌
- df: 是否返回DataFrame

## 使用示例
```python
# 获取日线数据
df = get_history('000001.XSHE', 30, unit='1d')

# 获取分钟数据
df = get_history('000001.XSHE', 100, unit='5m')
```
''',
        'category': 'PTrade_API'
    },
    timeout=30.0
)

if result.success:
    print(f"✅ 已添加知识 (ID: {result.data.get('knowledge_id')})")
```

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
