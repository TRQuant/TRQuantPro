---
title: 10.9 MCP × Cursor × 工具链联用规范
lang: zh
layout: /src/layouts/Layout.astro
---

# 10.9 MCP × Cursor × 工具链联用规范

## 概述

本章节详细说明如何在开发过程中使用MCP服务器、Cursor IDE和工具链进行高效协作。

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-10

## 统一工作模式（三条铁律）

### 铁律A：所有信息入口先MCP

- 查文档：`docs_server`
- 查代码：`code_server`
- 查知识：`kb.query`
- 查策略：`strategy_kb.query`
- 查规范：`spec_server`
- 查历史：`evidence_server`
- 查任务：`task_server`

### 铁律B：所有写操作走"安全写入协议"

标准流程：`dry_run` → `confirm_token` → `execute` → `evidence.record` → `git commit/tag` → `report.compare`

### 铁律C：所有大输出artifact化

- 输出超过阈值直接生成artifact pointer
- 手册中也必须引用pointer（避免终端/聊天粘贴大段）

## 模块开发流程模板

### 因子库开发流程

**目标**：新增/修改因子 → 验证 → 回测对比 → 产出报告 → 版本化

**步骤（MCP + Cursor 联用）**:

1. Cursor 打开 TRQuant repo，使用 `code.search` 定位入口类/接口（例如 FactorManager）
2. `docs.search/read` 查模块设计文档（接口约定、命名规范、边界条件）
3. `spec.validate` 校验你要写的章节文档结构（frontmatter、导航、字段）
4. 新增因子：`factor.create (dry_run)` → 拿到 confirm_token
5. `factor.create (execute + confirm_token + evidence)` → 生成因子版本
6. 回测：调用 backtest/workflow（workflow.run）产出结果 artifact
7. `report.generate` + `report.compare`：与基准策略/旧版本对比
8. `evidence.record`：记录本次变更目的、影响、回滚方案、对比报告链接
9. git：提交策略/文档/配置变更（用 git MCP 或本地 git），打 tag

**验收**:
- ✅ 能复现（固定数据集/seed）
- ✅ 有对比报告（report.compare）
- ✅ 有证据链（evidence）
- ✅ 有版本标识（tag）
- ✅ 有 trace_id（可观测性）

### 策略开发流程

**目标**：生成策略 → 回测验证 → 优化对比 → 产出定版策略

**步骤**:

1. `strategy_kb.query` - 检索相关研究卡
2. `workflow.strategy.generate_candidate` - 生成候选策略（含Python代码）
3. `workflow.run(backtest)` - 回测验证
4. `optimizer.run` - 策略优化
5. `report.compare` - 对比报告
6. `evidence.record` - 记录证据
7. `git tag` - 版本化

### 回测与优化流程

**步骤**:

1. `workflow.run` - 批量回测（walk-forward）
2. `optimizer.run` - 参数/权重/组合优化
3. `quality.validate` - 输入数据质量门禁
4. `report.compare` - 输出"为何升级"的证据
5. `task_server` - 记录"回测批次/优化批次"的任务与进度

### 平台集成/实盘反馈流程

**步骤**:

1. 数据回流（行情/订单/成交/滑点）进入 data pipeline（并被 quality.monitor）
2. 触发器命中 → `task.create` → `workflow.run(dry_run)` → `optimizer.run` → `report.compare`
3. 若要升级策略：必须 `confirm_token + evidence + 可回滚`

## Cursor侧标准化配置

### 统一venv路径

\`\`\`bash
TRQuant/extension/venv
\`\`\`

### 统一Cursor workspace settings

- 固定解释器路径
- 终端自动激活策略

### 统一MCP配置

\`\`\`json
{
  "mcpServers": {
    "trquant-engineering": {...},
    "trquant-kb": {...},
    "trquant-strategy-kb": {...},
    "trquant-docs": {...},
    "trquant-code": {...}
  }
}
\`\`\`

## 新成员入门流程

1. 打开 repo → 选择 interpreter → 启动 MCP servers
2. 跑一个 workflow dry_run → 生成一个 report
3. 查看 `docs/开发手册开发流程_工具使用指南.md`

## 最佳实践

### 稳定、高效、易维护

- **稳定**：每个模块都按同一套"工具链协议"走，不靠个人经验
- **高效**：充分利用MCP工具链，避免重复工作
- **易维护**：所有操作可追溯、可复现、可审计

### 关键原则

1. **信息入口先MCP**：优先使用MCP服务器查询信息
2. **写操作走安全协议**：dry_run → confirm_token → execute → evidence
3. **大输出artifact化**：避免终端/聊天粘贴大段内容
4. **引用强制**：所有章节必须包含引用（来自kb.query或strategy_kb.query）
5. **版本绑定**：所有代码示例带版本指纹

---

*最后更新: 2025-12-10*
