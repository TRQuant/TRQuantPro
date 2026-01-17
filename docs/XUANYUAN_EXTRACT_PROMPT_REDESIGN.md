# 轩辕剑灵Prompt提取功能重新设计

> **日期**: 2026-01-03  
> **状态**: 重新设计

---

## 📋 问题分析

### 原始设计的问题
- ❌ 从Git commits提取是我自己想的，不是用户真实需求
- ❌ 没有从实际开发记录中提取
- ❌ 不符合Cursor Prompt Engineering最佳实践

### 用户需求
根据用户提供的方法论，应该从**实际开发记录**中提取prompt，包括：
1. **Cursor Rules文件** (`.cursor/rules/*.mdc`) - 项目级系统提示词
2. **已保存的prompt模板** (`prompts/*.md`) - 团队Prompt模板库
3. **开发日志** (`devlog`) - 开发过程中使用的prompt记录
4. **代码注释** - 代码中的prompt模式

---

## 🎯 新的设计原则

### 遵循Cursor Prompt Engineering最佳实践

根据用户提供的方法论，提取的prompt应该：

1. **结构化提取**
   - 目标（要实现什么）
   - 约束（技术栈、规范、安全、性能）
   - 范围（要改哪些文件/模块）
   - 验收标准（测试、lint、行为）
   - 输出格式（diff/文件清单/步骤）

2. **识别Prompt模式**
   - 计划式Prompt（先计划后执行）
   - 闭环式Prompt（任务拆成最小闭环）
   - 约束式Prompt（明确技术约束）
   - 验收式Prompt（包含验收标准）

3. **分类提取**
   - 新功能开发Prompt
   - 重构Prompt
   - Bug修复Prompt
   - 代码Review Prompt
   - 测试编写Prompt

---

## 📂 数据源设计

### 1. Cursor Rules文件 (`.cursor/rules/*.mdc`)
- **位置**: `.cursor/rules/*.mdc`, `.cursor/index.mdc`
- **格式**: Markdown格式的规则文件
- **提取方法**: 
  - 提取文件内容作为系统级prompt规则
  - 识别规则的结构（全局规则、模块规则）

### 2. Prompt模板文件 (`prompts/*.md`)
- **位置**: `prompts/*.md`
- **格式**: Markdown，包含代码块中的prompt模板
- **提取方法**: 
  - 提取代码块（```标记的内容）
  - 提取标题下的段落（可能是prompt描述）

### 3. 开发日志 (`devlog`)
- **位置**: `.trquant/project_data/trquant/devlog.json`
- **格式**: JSON格式的开发日志
- **提取方法**:
  - 从日志内容中提取可能包含prompt的条目
  - 识别包含"目标"、"约束"、"要求"等关键词的日志

### 4. 代码注释
- **位置**: 代码文件中的注释
- **格式**: Python/TypeScript等代码注释
- **提取方法**:
  - 提取包含prompt模式的注释（如"TODO: 需要..."）
  - 提取docstring中的prompt描述

---

## 🔧 实现方案

### 重新设计`_extract_from_logs`函数

```python
async def _extract_from_logs(limit: int, min_length: int) -> List[Dict[str, Any]]:
    """从实际开发记录中提取prompt"""
    prompts = []
    
    # 1. 从prompts目录提取Markdown模板（保留）
    prompts_dir = TRQUANT_ROOT / "prompts"
    if prompts_dir.exists():
        # ... 已有逻辑
    
    # 2. 从.cursor/rules提取Cursor Rules
    cursor_rules_dir = TRQUANT_ROOT / ".cursor" / "rules"
    if cursor_rules_dir.exists():
        for mdc_file in cursor_rules_dir.rglob("*.mdc"):
            # 提取规则内容作为系统级prompt
    
    # 3. 从devlog提取开发日志中的prompt
    devlog_file = TRQUANT_ROOT / ".trquant" / "project_data" / "trquant" / "devlog.json"
    if devlog_file.exists():
        # 读取devlog，提取包含prompt模式的条目
    
    return prompts
```

---

## 📝 下一步行动

1. ✅ 修复工具路由问题（已完成）
2. ⏳ 重新实现提取逻辑，移除git commits提取
3. ⏳ 添加从.cursor/rules提取功能
4. ⏳ 添加从devlog提取功能
5. ⏳ 优化提取算法，识别结构化prompt模式
6. ⏳ 测试新的提取功能

---

## 📚 参考

- Cursor Prompt Engineering方法论（用户提供）
- Cursor Rules官方文档
- 开发日志格式规范

