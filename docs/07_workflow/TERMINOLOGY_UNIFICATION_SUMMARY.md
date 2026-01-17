# 工作流程术语统一总结

> **创建时间**: 2026-01-06  
> **目的**: 统一工作流程术语，将"候选池构建"改为"投资标的筛选"

---

## ✅ 已完成的修改

### 1. MCP Server文件

#### `mcp_servers/workflow_9steps_server.py`
- ✅ 将步骤4的注释从"候选池 (candidate_pool)"改为"投资标的筛选 (investment_target_selection)"
- ✅ 将工作流定义中的 `"name": "候选池构建"` 改为 `"name": "投资标的筛选"`
- ✅ 将 `"description": "构建候选股票池"` 改为 `"description": "筛选投资标的股票"`
- ✅ 将函数名 `execute_step_candidate_pool` 改为 `execute_step_investment_target_selection`
- ✅ 将函数注释从"步骤4: 候选池构建"改为"步骤4: 投资标的筛选"
- ✅ 将上下文键从 `"candidate_pool"` 改为 `"investment_target_selection"`
- ✅ 将路由映射从 `"candidate_pool": execute_step_candidate_pool` 改为 `"investment_target_selection": execute_step_investment_target_selection`

#### `mcp_servers/data_source_server_v2.py`
- ✅ 将注释从"- 候选池构建"改为"- 投资标的筛选"
- ✅ 将工具描述从"基于投资主线构建候选股票池"改为"基于投资主线筛选投资标的股票"
- ✅ 将函数注释从"构建候选股票池"改为"筛选投资标的股票"
- ✅ 将日志消息从"候选池构建失败"改为"投资标的筛选失败"
- ✅ 将返回消息从"构建X只股票候选池"改为"筛选出X只投资标的股票"

#### `mcp_servers/trquant_core_server.py`
- ✅ 将工具描述从"根据主线构建候选股票池"改为"根据主线筛选投资标的股票"

---

## 📝 待完成的修改

### 2. Notebook文件

需要更新以下notebook文件中的术语：
- `notebooks/research/01_market_trend_comprehensive.ipynb`
  - 将"步骤3: 候选池构建"改为"步骤4: 投资标的筛选"
  - 将"候选池筛选策略"改为"投资标的筛选策略"
  - 将"候选池构建时调整筛选条件"改为"投资标的筛选时调整筛选条件"
  - 将表格中的"候选池构建"改为"投资标的筛选"

- `notebooks/research/01_市场趋势综合评估.ipynb` (类似修改)
- `notebooks/research/01_market_trend_comprehensive_backup_20260103.ipynb` (类似修改)
- `notebooks/research/01_market_trend_comprehensive-Copy1.ipynb` (类似修改)

### 3. 文档文件

需要更新以下文档文件中的术语（约20个文件）：
- `docs/07_workflow/INVESTMENT_TARGET_MCP_SERVER_SUMMARY.md`
- `docs/07_workflow/INVESTMENT_TARGET_MCP_SERVER_DESIGN.md`
- `docs/07_workflow/STOCK_ANALYSIS_MODULE_DESIGN.md`
- 以及其他工作流相关文档

### 4. 其他代码文件

需要检查以下文件：
- `gui/widgets/investment_workflow_panel.py`
- `extension/src/views/workflowPanel.ts`
- `extension/webview-ui/src/pages/Workflow.tsx`
- `extension/webview-ui/src/store/workflowStore.ts`
- 其他前端/UI相关文件

---

## 🎯 统一术语对照表

| 旧术语 | 新术语 | 说明 |
|--------|--------|------|
| 候选池构建 | 投资标的筛选 | 工作流步骤名称 |
| build_candidate_pool | investment_target_selection | 函数/变量名 |
| candidate_pool | investment_target_selection | 上下文键名 |
| 构建候选股票池 | 筛选投资标的股票 | 描述文本 |
| 候选池筛选策略 | 投资标的筛选策略 | 策略描述 |

---

## 📋 验证清单

- [x] MCP Server核心文件已更新
- [ ] Notebook文件已更新
- [ ] 文档文件已更新
- [ ] 前端/UI文件已更新
- [ ] 所有修改已测试验证

---

## 🔍 注意事项

1. **内部实现保持不变**: 虽然对外接口和描述已统一为"投资标的筛选"，但内部实现（如`CandidatePoolBuilder`类名、`candidate_pool`集合名）可以保持不变，避免破坏现有功能。

2. **向后兼容**: MCP工具名称（如`data_source.candidate_pool`）可以保持不变，只更新描述文本，确保向后兼容。

3. **逐步迁移**: 可以分阶段完成术语统一，先更新核心MCP Server，再更新文档和UI。

---

**最后更新**: 2026-01-06  
**状态**: MCP Server核心文件已完成，Notebook和文档待更新
