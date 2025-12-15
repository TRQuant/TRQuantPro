# TRQuant Cursor 工作流程规范

## 核心原则

**Composer ≠ 文件生成器**

Composer 只用于：
- ✅ 分析已有代码
- ✅ 小范围修改
- ✅ 重构已有函数

**生成型任务一律用 Chat + 手动落盘**

## 标准流程

### 生成型任务（文档/模块/示例）

1. 使用 **Chat 模式**
2. 让AI生成完整文件内容
3. **手动**新建/覆盖文件
4. 保存
5. ❌ **不要让Composer参与**

### 修改型任务（已有代码）

1. ✅ 使用 **Composer**
2. ✅ 小范围修改
3. ✅ 重构已有函数
4. ✅ 分析代码，不生成大量新内容

## 工作区隔离建议

### 工作区1: TRQuant-core
- 路径: `TRQuant/` (排除 `extension/AShare-manual`)
- 用途: 核心代码开发
- Composer: ✅ 可用（只做小改）

### 工作区2: AShare-manual
- 路径: `TRQuant/extension/AShare-manual/`
- 用途: 文档维护
- Composer: ❌ 禁用（只用Chat）

### 工作区3: tools/data_collector
- 路径: `TRQuant/tools/data_collector/`
- 用途: 生成型脚本
- Composer: ⚠️ 只小改，不生成

## 绝对禁止

❌ 让Composer"从0到1生成大量文件"
❌ 批量生成工程代码 + 文档
❌ 让Composer处理"原文件1行 → 新文件200+行"的变更
❌ 在Composer中一次性生成多个大文件

## 当前状态

✅ 9步工作流改造已完成
- 只修改已有代码文件
- 使用Python脚本做自动化小改动
- 未生成任何新的大文件
- 未处理任何Markdown文档

## 物理隔离实施（2025-12-15）

### 工作区划分

1. **TRQuant**（代码开发）
   - 路径: `/home/taotao/dev/QuantTest/TRQuant/`
   - 用途: 核心代码开发
   - Composer: ✅ 可用（只做小改 <50行）

2. **TRQuant-Docs**（文档维护）
   - 路径: `/home/taotao/dev/QuantTest/TRQuant-Docs/`
   - 用途: 文档创建和维护
   - Composer: ❌ 禁用（只用 Chat）

3. **TRQuant-Scripts**（脚本生成）
   - 路径: `/home/taotao/dev/QuantTest/TRQuant-Scripts/`
   - 用途: 生成型脚本
   - Composer: ⚠️ 仅小改（<20行）

### 已迁移内容

**到 TRQuant-Docs**:
- `docs/` 目录（所有文档）
- `extension/AShare-manual/` 目录（A股手册）

**到 TRQuant-Scripts**:
- `scripts/` 目录（所有脚本）
- `tools/data_collector/` 目录（数据收集脚本）

### 使用说明

- 代码开发：在 TRQuant 工作区使用 Composer 做小改
- 文档维护：在 TRQuant-Docs 工作区使用 Chat 生成文档
- 脚本生成：在 TRQuant-Scripts 工作区使用 Chat 生成脚本

详细说明见各工作区的 README.txt 文件。
