# 轩辕剑灵LLM优化功能实现计划

> **日期**: 2026-01-03  
> **状态**: 📋 规划中

---

## 问题描述

当前Prompt优化功能使用模板套用方式，用户希望改为使用真正的LLM（通过Cursor）进行智能优化。

---

## 实现方案

### 方案1: 通过Cursor MCP服务器（推荐）

Cursor提供了MCP（Model Context Protocol）服务器，可以通过MCP调用Cursor的LLM能力。

**优点**:
- 无需额外的API密钥
- 直接使用Cursor的LLM
- 与Cursor深度集成

**实现步骤**:
1. 研究Cursor的MCP服务器API
2. 在`xuanyuan_server.py`中添加LLM调用函数
3. 修改`handle_optimize_prompt`使用LLM而非模板

### 方案2: 直接调用OpenAI/Anthropic API

如果用户有API密钥，可以直接调用。

**优点**:
- 独立于Cursor
- 可以自定义模型和参数

**缺点**:
- 需要API密钥配置
- 增加成本

### 方案3: 使用Cursor的本地API（如果存在）

如果Cursor提供本地API接口，可以直接调用。

---

## 当前改进

在实现真正的LLM优化之前，我们已改进：

1. ✅ **布局优化**: 增加间距和边距，改善视觉效果
2. ✅ **可编辑结果**: 优化后的Prompt框改为可编辑
3. ✅ **发送到Cursor**: 改进"发送到Cursor"功能，复制到剪贴板
4. ✅ **中文输入**: 添加输入法支持（需要系统环境支持）

---

## 下一步计划

1. **研究Cursor MCP API**
   - 查看Cursor文档
   - 测试MCP服务器调用方式

2. **实现LLM优化函数**
   - 在`xuanyuan_server.py`中添加`_optimize_with_llm`函数
   - 使用Cursor的LLM进行智能优化
   - 保留结构化输出格式

3. **配置管理**
   - 添加LLM配置选项
   - 支持选择优化模式（模板/LLM）

4. **用户体验**
   - 显示优化进度
   - 提供优化建议和解释

---

## 技术细节

### LLM优化Prompt示例

```python
async def _optimize_with_llm(task_description: str, context: str, prompt_type: str):
    """使用LLM优化Prompt"""
    
    system_prompt = """你是一个Prompt优化专家，擅长根据Cursor方法论优化开发任务的Prompt。
    
要求：
1. 生成结构化的Prompt，包含：目标、约束、范围、验收标准
2. 根据任务类型（新功能/Bug修复/重构等）调整结构
3. 考虑项目上下文和技术栈
4. 提供清晰、可执行的指导"""
    
    user_prompt = f"""
任务描述：{task_description}
上下文：{context}
任务类型：{prompt_type}

请生成一个符合Cursor方法论的结构化Prompt。
"""
    
    # 调用LLM（通过Cursor MCP或直接API）
    # response = await call_llm(system_prompt, user_prompt)
    # return response
    
    # 当前占位符实现
    return _generate_structured_prompt(task_description, context, prompt_type)
```

---

**最后更新**: 2026-01-03

