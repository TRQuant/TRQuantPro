# MCP批量执行工具使用指南

## 📋 概述

在Max模式下，多次调用MCP工具会消耗次数。为了优化这个问题，我们提供了批量执行工具，可以一次性执行多个工具调用，自动运行到需要用户输入时才停止。

## 🎯 功能特性

1. **workflow.batch**: 批量执行多个工具调用
2. **workflow.auto**: 自动执行工作流直到需要用户输入
3. **智能检测**: 自动检测何时需要用户输入
4. **上下文管理**: 自动管理步骤间的数据传递

## 🔧 工具说明

### 1. workflow.batch

批量执行多个工具调用，减少MCP调用次数。

**参数：**
- `tools`: 工具列表，每个元素格式: `{"name": "tool.name", "args": {...}}`
- `stop_on_input`: 遇到需要用户输入时是否停止，默认`true`
- `stop_on_error`: 遇到错误时是否停止，默认`false`
- `max_calls`: 最大调用次数，默认`50`

### 2. workflow.auto

自动执行工作流直到需要用户输入。

**参数：**
- `workflow_steps`: 工作流步骤定义
- `context`: 初始上下文（可选）

## 💡 使用场景

在Max模式下，优先使用`workflow.batch`或`workflow.auto`，减少MCP调用次数。
