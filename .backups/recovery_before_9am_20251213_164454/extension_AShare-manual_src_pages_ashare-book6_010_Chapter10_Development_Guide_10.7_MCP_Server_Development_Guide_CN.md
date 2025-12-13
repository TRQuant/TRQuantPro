---
title: 10.7 MCP Server开发指南
lang: zh
layout: /src/layouts/Layout.astro
---

# 10.7 MCP Server开发指南

## 概述

MCP Server开发指南，包括协议理解、服务器实现、工具开发等。

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-10

## 详细内容

刚才Phase 2生成的内容，**主要是Cursor（我）根据模板硬编码生成的**，而不是真正从MCP Server检索来的。

### 内容来源分析

1. **章节框架和模板** → 由Python脚本硬编码生成（Cursor生成）
   - 例如：`section_content = f'''---\ntitle: ...\n---\n# ...\n'''`
   - 这是我在Python脚本中直接写的模板

2. **KB引用信息** → 尝试调用了`kb.query`/`strategy_kb.query`，但：
   - ❌ **KB索引不存在**（检查发现Manual KB和Engineering KB索引都不存在）
   - ❌ **Strategy KB索引也不存在**
   - 所以即使调用了，返回的也是空引用或错误信息
   - 即使有引用，也只是引用列表，**内容还是模板**

3. **详细内容** → 目前都是占位符（"本节内容正在开发中"）

## MCP Server的实际作用

### ✅ MCP Server负责什么？

1. **提供检索能力**：从知识库中检索相关内容
   - `kb.query` - 从Manual KB和Engineering KB检索
   - `strategy_kb.query` - 从Strategy KB检索研究卡

2. **提供验证能力**：验证内容是否符合规范
   - `spec.validate` - 验证文档结构
   - `strategy_kb.rule.validate` - 验证策略是否符合规则

3. **提供规则能力**：Strategy KB提供策略规则约束
   - `strategy_kb.rule.get` - 获取规则
   - 规则是硬约束，不能由LLM随意生成

4. **提供工作流能力**：Engineering Server编排整个流程
   - `engineering.plan` - 规划任务
   - `engineering.work` - 执行任务
   - `engineering.verify` - 验证质量
   - `enginee

# MCP Phase 0 执行记录

> 开始时间: 2025-12-09  
> 阶段: Phase 0 - 官方服务器整合

---

## 📋 执行状态

### Day 1: Filesystem Server

#### 环境检查 ✅

...

*完整内容请参考源文档*


## 相关文档

- 源文档位置：`docs/02_development_guides/` 或相关目录
- 相关代码：`extension/` 或 `mcp_servers/` 目录

## 关键要点

### 开发流程

1. **环境搭建**
   - 安装依赖
   - 配置开发环境
   - 验证环境

2. **开发实现**
   - 编写代码
   - 测试功能
   - 调试问题

3. **集成测试**
   - 单元测试
   - 集成测试
   - 端到端测试

4. **文档更新**
   - 更新文档
   - 更新示例
   - 更新指南

## 下一步

- [ ] 整理和格式化内容
- [ ] 添加代码示例
- [ ] 添加截图和图表
- [ ] 验证内容准确性

---

*最后更新: 2025-12-10*
