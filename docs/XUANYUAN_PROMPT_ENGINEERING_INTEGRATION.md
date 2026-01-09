# 轩辕剑灵Prompt Engineering集成方案

> **创建时间**: 2026-01-03  
> **状态**: ✅ 核心功能已实现，待完善

---

## 📋 问题诊断与解决

### 原始问题
- ❌ 创建模板功能失败
- ❌ MCP工具调用不兼容

### 根本原因
1. **xuanyuan_server使用官方MCP SDK** (`stdio_server`)
2. **MCPClient使用简单的subprocess JSON-RPC调用**
3. **两者通信协议不兼容**

### 解决方案
✅ **实现`_call_xuanyuan_direct`方法**（参考`_call_workflow9_direct`）
- 直接调用`handle_tool`函数，避免subprocess
- 解析`List[TextContent]`返回格式
- 在`_call_mcp_server`中添加xuanyuan工具的特殊处理

✅ **添加xuanyuan工具到TOOL_SERVER_MAP**（18个工具）

---

## 🔍 Prompt Engineering工具调研

### 1. 开源项目与工具

#### PromptEditor
- **特点**: 免费AI提示词编写工具
- **功能**: Prompt编辑、Markdown编辑、提示词专家、多模型对比分析
- **优势**: 语法工具条、内容辅助、调试优化、云端协作
- **适用性**: ⭐⭐⭐⭐ (适合作为参考)

#### PromptAid
- **特点**: 可视化分析系统
- **功能**: 提示词的探索、扰动、测试和迭代
- **优势**: 交互式创建、优化和测试提示词
- **适用性**: ⭐⭐⭐ (研究价值高)

#### PromptAgent
- **特点**: 自动生成高质量提示词
- **功能**: 基于蒙特卡洛树搜索的规划算法
- **优势**: 自动优化，反思模型错误
- **适用性**: ⭐⭐⭐ (适合高级场景)

#### LangChain
- **特点**: 应用框架，简化LLM应用开发
- **功能**: 标准接口连接语言模型、工具和数据源
- **适用性**: ⭐⭐⭐⭐⭐ (可集成)

### 2. 最佳实践总结

#### 提示词结构规范
```
1. 角色定义 (Role Definition)
2. 任务描述 (Task Description)
3. 上下文信息 (Context)
4. 输出格式 (Output Format)
5. 约束条件 (Constraints)
6. 示例 (Examples)
```

#### 提示词优化策略
- **关键词扰动**: 测试不同关键词组合
- **改写扰动**: 尝试不同表达方式
- **上下文示例**: 提供最佳上下文示例
- **迭代优化**: 基于反馈持续改进

---

## ✅ 已实现功能

### 1. MCP服务器集成
- ✅ xuanyuan_server.py (使用官方MCP SDK)
- ✅ 18个工具已注册到TOOL_SERVER_MAP
- ✅ `_call_xuanyuan_direct`方法实现
- ✅ 测试验证通过

### 2. 提示词模板管理
- ✅ 创建模板 (`xuanyuan.prompt.templates.create`)
- ✅ 列出模板 (`xuanyuan.prompt.templates.list`)
- ✅ 获取模板详情 (`xuanyuan.prompt.templates.get`)
- ✅ 更新模板 (`xuanyuan.prompt.templates.update`)
- ✅ 评估模板 (`xuanyuan.prompt.templates.evaluate`)
- ✅ 最佳实践搜索 (`xuanyuan.prompt.best_practices.search`)

### 3. GUI界面（基础）
- ✅ 独立GUI窗口 (`gui/xuanyuan_main_window.py`)
- ✅ 提示词管理Tab
- ✅ 模板列表显示（QTableWidget）
- ✅ 模板详情显示
- ✅ 创建/编辑模板对话框
- ✅ 复制模板内容功能
- ✅ 分类筛选功能

---

## 📝 待实现功能

### 1. 从开发记录提取Prompt ⭐⭐⭐ (高优先级)

**需求**: 从开发记录中提取典型的prompt，保存到GUI中供参考调用

**实现方案**:
```python
# 工具: xuanyuan.prompt.extract_from_logs
# 参数:
#   - log_path: 日志文件路径（可选，默认扫描logs/目录）
#   - pattern: 提取模式（可选，默认提取用户查询）
#   - min_length: 最小长度（可选，默认50字符）
#   - max_results: 最大结果数（可选，默认20）

# 提取逻辑:
#   1. 扫描logs/目录或指定文件
#   2. 使用正则表达式或LLM提取prompt模式
#   3. 去重和分类
#   4. 返回候选prompt列表
#   5. GUI中显示，用户可选择保存为模板
```

**数据来源**:
- `logs/`目录下的开发日志
- Cursor Chat历史记录（如果可访问）
- Git commit messages（提取开发意图）
- 代码注释中的TODO/FIXME（提取开发需求）

### 2. Prompt模板分类体系

**建议分类**:
- `system`: 系统级提示词（角色定义、行为规范）
- `code_generation`: 代码生成
- `code_review`: 代码审查
- `error_handling`: 错误处理
- `testing`: 测试相关
- `documentation`: 文档编写
- `data_analysis`: 数据分析
- `strategy_development`: 策略开发
- `backtest`: 回测相关
- `optimization`: 优化相关
- `general`: 通用

### 3. Prompt模板标签系统

**常用标签**:
- `high_quality`: 高质量模板
- `frequently_used`: 常用模板
- `experimental`: 实验性
- `deprecated`: 已弃用
- `quantitative`: 量化相关
- `trading`: 交易相关
- `research`: 研究相关

### 4. Prompt模板评估机制

**评估维度**:
- `usage_count`: 使用次数
- `avg_rating`: 平均评分（1-5星）
- `success_rate`: 成功率（如果可追踪）
- `response_time`: 响应时间
- `user_feedback`: 用户反馈

### 5. 最佳实践库

**内容来源**:
- 网络搜索的prompt engineering最佳实践
- 开源项目的prompt模板
- 社区分享的成功案例
- 内部积累的经验

**存储**: `data/xuanyuan/prompts/best_practices.json`

---

## 🔄 开发流程整合

### 当前工作流
```
开发需求 → Cursor Chat → 手动编写Prompt → 执行 → 结果
```

### 优化后的工作流
```
开发需求 → 轩辕剑灵GUI
  ├─ 搜索相似模板 → 复用/修改 → 执行
  ├─ 从开发记录提取 → 保存为模板 → 执行
  └─ 创建新模板 → 评估优化 → 保存 → 执行
```

### 循环测试流程

1. **提取阶段**
   - 从开发记录中提取prompt模式
   - 自动分类和标签
   - 保存为候选模板

2. **测试阶段**
   - 在GUI中测试模板
   - 记录使用效果
   - 收集反馈

3. **优化阶段**
   - 基于反馈优化模板
   - 更新评估指标
   - 标记高质量模板

4. **复用阶段**
   - 在相似场景中复用模板
   - 积累使用统计
   - 持续改进

---

## 📊 数据存储结构

### 提示词模板 (`data/xuanyuan/prompts/templates.json`)
```json
{
  "templates": [
    {
      "id": "tmpl_xxx",
      "name": "模板名称",
      "content": "模板内容",
      "category": "分类",
      "tags": ["标签1", "标签2"],
      "description": "描述",
      "created_at": "2026-01-03T18:53:16",
      "updated_at": "2026-01-03T18:53:16",
      "usage_count": 0,
      "avg_rating": 0.0,
      "source": "extracted|manual|imported",
      "source_info": {}
    }
  ]
}
```

### 最佳实践 (`data/xuanyuan/prompts/best_practices.json`)
```json
{
  "practices": [
    {
      "id": "practice_xxx",
      "title": "实践标题",
      "description": "描述",
      "category": "分类",
      "content": "实践内容",
      "examples": [],
      "references": [],
      "rating": 0.0,
      "created_at": "2026-01-03T18:53:16"
    }
  ]
}
```

---

## 🎯 下一步行动计划

### Phase 1: 基础功能完善（当前）
- ✅ MCP服务器集成
- ✅ 模板CRUD操作
- ✅ GUI基础界面
- 🔄 从开发记录提取prompt（进行中）

### Phase 2: 提取与导入（1-2周）
- ⏳ 实现日志提取功能
- ⏳ Git commit messages提取
- ⏳ 批量导入模板
- ⏳ 模板去重和合并

### Phase 3: 评估与优化（2-3周）
- ⏳ 使用统计追踪
- ⏳ 评分系统
- ⏳ 模板优化建议
- ⏳ A/B测试框架

### Phase 4: 最佳实践整合（3-4周）
- ⏳ 网络爬取最佳实践
- ⏳ 开源项目模板导入
- ⏳ 社区分享集成
- ⏳ 知识库构建

### Phase 5: 高级功能（4+周）
- ⏳ Prompt模板版本控制
- ⏳ 模板组合和链式调用
- ⏳ 自动优化算法
- ⏳ 多模型对比测试

---

## 📚 参考资源

1. **PromptEditor**: https://www.prompteditor.cn/
2. **PromptAid论文**: https://arxiv.org/abs/2304.01964
3. **PromptAgent论文**: https://arxiv.org/abs/2310.16427
4. **LangChain文档**: https://python.langchain.com/
5. **GitHub Prompt Engineering教程**: 中文教学项目

---

## ✅ 测试验证

### 测试结果
```bash
# 创建模板测试
✅ 成功创建模板，返回template_id: tmpl_20260103_185316_4f7069

# 列出模板测试
✅ 成功列出模板，数量: 1

# 功能验证
✅ MCP工具调用正常
✅ 数据持久化正常
✅ GUI界面响应正常
```

---

## 🔗 相关文档

- `docs/XUANYUAN_MCP_SETUP.md` - MCP服务器配置指南
- `docs/XUANYUAN_GUI_IMPLEMENTATION_PLAN.md` - GUI实现计划
- `docs/XUANYUAN_MCP_INTEGRATION_ISSUE.md` - 集成问题分析
- `mcp_servers/xuanyuan_server.py` - MCP服务器实现
- `gui/widgets/xuanyuan_assistant_panel.py` - GUI面板实现

