# TRQuant 标准开发流程

> **版本**: 1.0  
> **更新时间**: 2026-01-09

---

## 1. 概述

本文档定义了TRQuant项目的标准开发流程，确保开发过程中的知识积累和经验复用。

### 核心原则

1. **知识沉淀**: 每次调试经验都应存入知识库
2. **可追溯**: 所有决策都要有证据支持
3. **可复用**: 解决方案应该结构化，便于后续查阅

---

## 2. 工具链

### 2.1 KB工具（知识库）

| 工具 | 功能 | 示例 |
|------|------|------|
| `kb.search` | 搜索知识库 | `kb_search("BulletTrade")` |
| `kb.add` | 添加知识条目 | `kb_add(title, content, category)` |
| `kb.get_api` | 获取API文档 | `kb_get_api("get_price")` |
| `kb.get_strategy` | 获取策略详情 | `kb_get_strategy("momentum")` |
| `kb.best_practices` | 获取最佳实践 | `kb_best_practices("backtest")` |

### 2.2 Evidence工具（证据追踪）

| 工具 | 功能 |
|------|------|
| `evidence.add` | 添加决策证据 |
| `evidence.list` | 列出证据 |
| `evidence.search` | 搜索证据 |

### 2.3 Research工具（研究笔记）

| 工具 | 功能 |
|------|------|
| `research.note` | 添加研究笔记 |
| `research.list` | 列出笔记 |
| `research.search` | 搜索笔记 |

---

## 3. 标准开发流程

### 3.1 开始开发前

```
1. kb.search("相关问题")  // 查找是否有类似问题的解决方案
2. kb.best_practices("相关分类")  // 查看最佳实践
3. kb.get_api("相关API")  // 查看API文档
```

### 3.2 开发过程中

```
1. 遇到问题时先搜索知识库
2. 记录调试日志（使用devlog.add）
3. 重要发现立即存入知识库
```

### 3.3 问题解决后

```
1. kb.add(title, content, category)  // 存入知识库
2. evidence.add(decision, reason, data)  // 记录决策证据
3. 更新文档
```

---

## 4. 知识库分类

### 4.1 预定义分类

| 分类 | 说明 |
|------|------|
| `bulletrade_debug` | BulletTrade回测相关调试经验 |
| `jqdata_api` | JQData API使用经验 |
| `strategy` | 策略开发经验 |
| `backtest` | 回测相关经验 |
| `risk` | 风控相关经验 |
| `code` | 代码规范和最佳实践 |
| `general` | 通用知识 |

### 4.2 知识条目结构

```python
{
    "id": "kb_20260109_105614",
    "title": "问题标题",
    "content": """
问题描述：
...

错误表现：
...

根因分析：
...

解决方案：
...

验证方法：
...
""",
    "category": "bulletrade_debug",
    "created": "2026-01-09T10:56:14"
}
```

---

## 5. 使用示例

### 5.1 遇到BulletTrade问题时

```python
# 1. 先搜索知识库
from unified_dev_server import kb_search
result = kb_search("BulletTrade get_price")
if result['total'] > 0:
    print("找到相关知识：")
    for r in result['results']:
        print(f"- {r['title']}")
        print(f"  {r['content'][:200]}...")
```

### 5.2 解决问题后存入知识库

```python
from unified_dev_server import kb_add

kb_add(
    title="问题标题",
    content="""
问题描述：
...

解决方案：
```python
# 代码示例
```
""",
    category="bulletrade_debug"
)
```

### 5.3 记录决策证据

```python
from unified_dev_server import evidence_add

evidence_add(
    decision="选择使用jqdatasdk获取基本面数据",
    reason="BulletTrade的jqdata兼容层不包含get_fundamentals",
    data={"tested_alternatives": ["from jqdata import *", "jqdatasdk.get_fundamentals"]}
)
```

---

## 6. 当前知识库内容

### 6.1 BulletTrade调试经验

1. **BulletTrade get_price返回MultiIndex列名问题**
   - 分类: `bulletrade_debug`
   - 解决方案: 展平MultiIndex列名

2. **BulletTrade get_fundamentals未定义错误**
   - 分类: `bulletrade_debug`
   - 解决方案: 从jqdatasdk导入并认证

3. **BulletTrade Position对象属性与聚宽不同**
   - 分类: `bulletrade_debug`
   - 解决方案: 使用hasattr检查属性

4. **BulletTrade jqdata模块替换机制**
   - 分类: `bulletrade_debug`
   - 内容: 模块替换原理说明

### 6.2 JQData API经验

1. **JQData market_cap单位是亿元不需要转换**
   - 分类: `jqdata_api`
   - 解决方案: 直接使用返回值，不除以1亿

---

## 7. 工具调用方式

### 7.1 Python直接调用

```python
import sys
sys.path.insert(0, '/path/to/TRQuant/ope')
sys.path.insert(0, '/path/to/TRQuant/ope/mcp_servers')

from unified_dev_server import kb_search, kb_add, kb_best_practices
```

### 7.2 MCP工具调用

通过Cursor IDE的MCP工具调用：
- `mcp_unified-dev_kb.search`
- `mcp_unified-dev_kb.add`
- `mcp_unified-dev_kb.best_practices`

---

## 8. 维护指南

### 8.1 定期任务

1. **每周**: 审核新添加的知识条目
2. **每月**: 清理过时的知识
3. **每季度**: 优化知识分类体系

### 8.2 质量标准

- 每个知识条目必须包含: 问题描述、解决方案、验证方法
- 代码示例必须可运行
- 分类必须准确

---

*文档维护: TRQuant开发团队*
