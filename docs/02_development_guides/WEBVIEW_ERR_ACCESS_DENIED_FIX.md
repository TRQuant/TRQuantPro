# Webview ERR_ACCESS_DENIED 错误修复指南

## 问题描述

当打开 React Panel 时，可能出现以下错误：
```
GET vscode-webview://.../assets/index.js net::ERR_ACCESS_DENIED
```

## 根本原因

VS Code Webview 对资源加载有严格的安全限制：
1. **localResourceRoots 配置不足**：没有正确包含资源文件所在目录
2. **URI 生成问题**：`asWebviewUri` 生成的 URI 路径不正确
3. **文件权限问题**：文件系统权限不足
4. **CSP 限制**：Content Security Policy 过于严格

## 已实施的修复

### 1. 扩展 localResourceRoots

```typescript
localResourceRoots: [
    distPath,           // dist 目录
    assetsPath,          // assets 子目录
    resourcesPath,       // resources 目录
    webviewUiPath,       // webview-ui 目录
    extensionUri         // 整个扩展目录（最宽泛的权限）
]
```

### 2. 增强路径替换逻辑

支持多种路径格式：
- `./assets/index.js`
- `/assets/index.js`
- `assets/index.js`
- 单引号和双引号

### 3. 详细的调试日志

在 `ReactPanel.ts` 中添加了：
- 文件存在性检查
- URI 生成日志
- 资源路径验证

### 4. 错误处理

如果资源加载失败，显示详细的错误信息页面。

## 如果错误仍然出现

### 步骤 1: 检查输出日志

1. 打开 VS Code 输出面板：`View > Output`
2. 选择 "Log (Extension Host)"
3. 查找 `[ReactPanel]` 开头的日志
4. 确认：
   - ✓ Dist 目录是否存在
   - ✓ Assets 文件列表
   - ✓ Script URI 和 Style URI

### 步骤 2: 检查文件系统

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/webview-ui/dist
ls -la assets/
```

确认以下文件存在：
- `assets/index.js`
- `assets/index.css`

### 步骤 3: 检查文件权限

```bash
ls -la /home/taotao/dev/QuantTest/TRQuant/extension/webview-ui/dist/assets/
```

确保文件有读取权限（`-r--r--r--` 或 `-rw-rw-r--`）。

### 步骤 4: 检查 Webview 开发者工具

1. 打开 Webview 开发者工具：`Ctrl+Shift+P` > "Developer: Open Webview Developer Tools"
2. 查看 Console 中的错误
3. 查看 Network 标签，检查资源请求状态

### 步骤 5: 验证 URI 格式

在 Webview 开发者工具的 Console 中运行：
```javascript
console.log('Script URI:', document.querySelector('script[src]')?.src);
console.log('Style URI:', document.querySelector('link[rel="stylesheet"]')?.href);
```

URI 应该是 `vscode-webview://` 格式，例如：
```
vscode-webview://13ohu5vsktsud090kggjm746pnaj21v7flf2unhfnd9ol0ad4sn8/assets/index.js
```

### 步骤 6: 尝试备用方案

如果上述步骤都失败，可以尝试：

#### 方案 A: 使用 data URI（仅适用于小文件）

将 JavaScript 和 CSS 内联到 HTML 中（不推荐，但可以作为临时方案）。

#### 方案 B: 使用 HTTP 服务器

在本地启动一个 HTTP 服务器，然后修改 `connect-src` CSP 允许 `http://localhost:*`。

#### 方案 C: 检查 VS Code 版本

某些旧版本的 VS Code 可能有 Webview 资源加载的 bug。尝试更新到最新版本。

### 步骤 7: 重新构建

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/webview-ui
rm -rf dist node_modules
npm install
npm run build
```

然后重新编译和打包扩展。

## 调试检查清单

- [ ] Dist 目录存在
- [ ] Assets 目录存在
- [ ] index.js 和 index.css 文件存在
- [ ] 文件有读取权限
- [ ] localResourceRoots 包含所有必要路径
- [ ] URI 格式正确（vscode-webview://）
- [ ] CSP 允许必要的资源
- [ ] 没有 Service Worker 干扰
- [ ] VS Code 版本是最新的

## 联系支持

如果所有步骤都失败，请提供：
1. VS Code 版本
2. 完整的输出日志（`[ReactPanel]` 相关）
3. Webview 开发者工具的 Console 输出
4. Network 标签的截图
5. 文件系统权限信息

