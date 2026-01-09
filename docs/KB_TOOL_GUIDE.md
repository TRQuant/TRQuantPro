# TRQuant 知识库工具使用指南

> **版本**: 1.0  
> **更新时间**: 2026-01-09

---

## 1. 快速开始

### 1.1 命令行工具

```bash
# 进入项目目录
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 搜索知识库
./venv/bin/python3 scripts/kb_tool.py search "BulletTrade"

# 按分类搜索
./venv/bin/python3 scripts/kb_tool.py search "" --category bulletrade_debug

# 列出所有知识
./venv/bin/python3 scripts/kb_tool.py list

# 添加知识
./venv/bin/python3 scripts/kb_tool.py add "标题" "内容" --category bulletrade_debug
```

### 1.2 Python API

```python
import sys
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope')
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope/mcp_servers')

from unified_dev_server import kb_search, kb_add, kb_best_practices

# 搜索
result = kb_search("BulletTrade")
print(result)

# 添加
result = kb_add("标题", "内容", category="bulletrade_debug")
print(result)
```

---

## 2. 当前知识库内容

### 2.1 BulletTrade调试经验 (bulletrade_debug)

| 标题 | 关键问题 | 解决方案 |
|------|----------|----------|
| get_price返回MultiIndex列名 | `'code' in df.columns` 返回False | 展平MultiIndex列名 |
| get_fundamentals未定义 | BulletTrade不含此函数 | 从jqdatasdk导入并认证 |
| Position属性不同 | 没有total_value属性 | 使用hasattr检查属性 |
| jqdata模块替换机制 | 策略加载时模块被替换 | 了解替换机制，正确导入 |

### 2.2 JQData API (jqdata_api)

| 标题 | 关键问题 | 解决方案 |
|------|----------|----------|
| market_cap单位 | 误以为是元单位 | 直接使用（已是亿元） |

---

## 3. 标准开发流程

### 开发前
```
1. kb_search("相关问题")  // 先查知识库
2. kb_best_practices()    // 查看最佳实践
```

### 开发中
```
1. 遇到问题先搜索知识库
2. 重要发现立即记录
```

### 开发后
```
1. kb_add(title, content, category)  // 存入经验
2. evidence_add(decision, reason, data)  // 记录决策
```

---

## 4. 知识条目模板

```python
kb_add(
    title="问题标题（简洁明确）",
    content="""
问题描述：
简要描述遇到的问题

错误表现：
- 具体的错误信息
- 现象描述

根因分析：
问题的根本原因

解决方案：
```python
# 代码示例
```

验证方法：
如何验证问题已解决

适用场景：
- 场景1
- 场景2
""",
    category="bulletrade_debug"  # 或其他分类
)
```

---

## 5. 文件位置

| 文件 | 说明 |
|------|------|
| `scripts/kb_tool.py` | 命令行工具 |
| `mcp_servers/unified_dev_server.py` | KB API实现 |
| `.trquant/dev/kb/custom_kb.json` | 知识库数据文件 |
| `docs/STANDARD_DEV_WORKFLOW.md` | 标准开发流程文档 |

---

## 6. 分类说明

| 分类 | 说明 | 使用场景 |
|------|------|----------|
| `bulletrade_debug` | BulletTrade回测调试 | 回测相关问题 |
| `jqdata_api` | JQData API使用 | 数据获取问题 |
| `strategy` | 策略开发 | 策略逻辑问题 |
| `backtest` | 回测配置 | 回测参数问题 |
| `risk` | 风控相关 | 风险管理问题 |
| `code` | 代码规范 | 编码标准问题 |
| `general` | 通用知识 | 其他问题 |

---

*TRQuant开发团队*
