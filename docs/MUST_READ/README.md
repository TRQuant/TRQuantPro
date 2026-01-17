# DevMustRead - 开发必读文档

> **创建时间**: 2024-12-19  
> **目的**: 存放开发过程中必须参考的核心文档

---

## 📚 文档清单

### 1. MCP工具完整清单 (`MCP_TOOLS_COMPLETE_LIST.md`)

**用途**: 快速查找所有可用的MCP工具及其使用方法

**内容**:
- 9步投资工作流服务器工具 (9个)
- 十倍股早期识别系统工具 (7个)
- 轩辕剑灵/统一开发服务器工具 (103个)
- 核心量化服务器工具 (25个)
- 数据源服务器工具 (9个)
- 市场分析服务器工具 (11个)
- 回测服务器工具 (9个)
- 策略服务器工具 (14个)
- 因子服务器工具 (8个)
- 报告服务器工具 (7个)
- 优化服务器工具 (6个)
- Utils工具模块 (多个)

**统计**: 约292个MCP工具

**知识库ID**: `kb_20251219_195854`

---

### 2. MCP标准开发流程完全指南 (`MCP_STANDARD_DEV_WORKFLOW.md`)

**用途**: 规范开发流程，确保开发质量和一致性

**版本**: 4.0

**核心内容**:
- 标准开发流程 (6步法)
  - 步骤0: 会话初始化
  - 步骤0.5: 知识库构建 (新增)
  - 步骤1: 规划阶段
  - 步骤2: 开发阶段
  - 步骤3: 测试阶段
  - 步骤4: 完成阶段
- MCP工具清单 (103个)
- 工作目录规范
- 知识库使用规范
- 自动学习触发器
- 检查清单
- 常见问题

**知识库ID**: `kb_20251219_200101`

---

## 🔍 如何使用

### 方式1: 直接阅读文件
```bash
cd /home/taotao/dev/QuantTest/TRQuant/DevMustRead
cat MCP_TOOLS_COMPLETE_LIST.md
cat MCP_STANDARD_DEV_WORKFLOW.md
```

### 方式2: 通过知识库搜索 (推荐)
```python
# 搜索MCP工具
knowledge.search("MCP工具清单")

# 搜索开发流程
knowledge.search("标准开发流程")
```

### 方式3: 通过知识ID直接获取
```python
# 获取MCP工具清单
knowledge.get("kb_20251219_195854")

# 获取标准开发流程
knowledge.get("kb_20251219_200101")
```

---

## 📝 更新说明

### 何时更新
- 新增MCP工具时，更新 `MCP_TOOLS_COMPLETE_LIST.md`
- 开发流程变更时，更新 `MCP_STANDARD_DEV_WORKFLOW.md`
- 重要规范变更时，同步更新两个文档

### 如何更新
1. 修改文档文件
2. 使用 `knowledge.update` 更新知识库
3. 确保文档路径和知识库内容一致

---

## 🔗 相关文档

- **原始文档位置**: `/home/taotao/dev/QuantTest/TRQuant/docs/`
- **知识库**: 通过 `knowledge.search` 或 `knowledge.get` 访问
- **MCP服务器**: `mcp_servers/` 目录

---

*最后更新: 2024-12-19*

## 4. TENBAGGER_MCP_WORKFLOW.md
**十倍股MCP工作流程** - 独立于9步工作流的十倍股识别系统专有流程

⚠️ **重要区分**:
- 9步工作流: `workflow_9steps_server` → 完整投资决策
- 十倍股识别: `trquant_core_server` → 高成长股筛选


## 5. TENBAGGER_RUN_HISTORY.md
**十倍股运行历史记录** - 记录早上(2025-12-19)运行十倍股筛选系统的详细流程和结果

📝 **关键信息**:
- 运行脚本: `scripts/run_tenbagger_screening.py`
- 运行方式: Python直接调用（非MCP工具）
- 评估结果: 15只股票，推荐14只（S级1只，A级13只）

