# TRQuant 前端设计与架构审计报告

**日期**: 2025-12-21
**审计者**: 轩辕剑灵 (Gemini 3 Pro Powered)

## 1. 架构概述

TRQuant 前端采用 **React + Zustand + Ant Design** 技术栈，运行在 VS Code Webview 环境中。

### 核心组件
- **UI 框架**: React 18, Ant Design 5 (VS Code 主题适配)
- **构建工具**: Vite (配置了相对路径输出)
- **状态管理**: Zustand (模块化 Store + 统一入口)
- **通信层**: MCP Protocol (Webview <-> Extension Host <-> Python Server)

## 2. 关键发现与修复

### 2.1 路径解析问题 (已修复)
- **问题**: Vite 默认使用绝对路径 (`/assets/...`)，导致 Webview 无法加载资源。
- **修复**: 在 `vite.config.ts` 中设置 `base: './'`，并在 `ReactPanel.ts` 中使用 `webview.asWebviewUri()` 动态替换路径。

### 2.2 通信可靠性 (已优化)
- **问题**: 原 `useAppStore` 使用简陋的 `postMessage` 实现，缺乏重试和队列机制。
- **修复**: 重构 `store/index.ts`，使其底层调用统一的 `WebviewMCPClient`。该客户端实现了：
  - 消息队列 (Message Queue) 确保顺序执行
  - 指数退避重试 (Exponential Backoff Retry) 处理临时故障
  - 请求/响应 ID 匹配 (Request/Response Matching) 防止乱序

### 2.3 安全策略 (已增强)
- **配置**: `ReactPanel.ts` 中配置了严格的 CSP (Content Security Policy)，但放宽了 `unsafe-inline` 和 `unsafe-eval` 以兼容 React 和 Ant Design 的动态特性。

## 3. 设计建议

### 3.1 模块化 Store 迁移
虽然目前通过 `store/index.ts` 保持了向后兼容，但建议未来将各个页面 (`WorkflowPage`, `TenbaggerPage`) 的状态管理完全迁移到独立的 `workflowStore.ts` 和 `tenbaggerStore.ts`，减少全局 Store 的臃肿。

### 3.2 组件解耦
目前 `App.tsx` 承担了过多的布局职责。建议拆分为 `MainLayout` 组件，使路由（Tab切换）逻辑更清晰。

### 3.3 错误边界
建议在 `App.tsx` 顶层添加 `ErrorBoundary` 组件，防止某个 Tab 的渲染错误导致整个面板白屏。

## 4. 结论

前端架构现已"理顺"。核心通信链路（React -> MCP）已加固，构建配置已修正。系统已准备好进行功能测试。

---
**生成的扩展包**: `extension/trquant-cursor-extension-0.2.9-202512211953.vsix`
