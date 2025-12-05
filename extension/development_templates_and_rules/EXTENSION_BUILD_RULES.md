# TRQuant 扩展开发规则

## 🚨 重要：代码修改后的部署流程

### 问题背景
Cursor/VS Code 使用的是**已安装的扩展**（位于 `~/.cursor/extensions/` 或 `~/.vscode/extensions/`），而**不是**开发目录中的源代码。

因此，修改 `extension/src/` 中的代码后，**必须**重新打包并安装才能生效。

### ✅ 正确的部署流程

```bash
# 1. 编译 TypeScript
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run compile

# 2. 打包为 .vsix 文件
npx @vscode/vsce package --allow-missing-repository --no-dependencies

# 3. 安装到 Cursor
cursor --install-extension trquant-cursor-extension-0.1.0.vsix --force

# 4. 重新加载窗口
# 在 Cursor 中按 Ctrl+Shift+P → Developer: Reload Window
```

### ❌ 常见错误

1. **只编译不安装**：修改代码后只运行 `npm run compile`，期望扩展自动更新
   - 错误原因：编译只更新 `extension/dist/extension.js`，但 Cursor 使用的是 `~/.cursor/extensions/` 中的版本

2. **路径错误**：使用 `path.dirname(context.extensionPath)` 获取根目录
   - 错误原因：安装后 `context.extensionPath` 指向 `~/.cursor/extensions/xxx/`，`path.dirname()` 会返回 `~/.cursor/extensions/`
   - 正确做法：直接使用 `context.extensionPath` 作为扩展根目录

### 📁 路径说明

| 环境 | `context.extensionPath` | 说明 |
|------|------------------------|------|
| 开发调试 (F5) | `/home/taotao/dev/QuantTest/TRQuant/extension` | 开发目录 |
| 安装后使用 | `~/.cursor/extensions/trquant.trquant-cursor-extension-0.1.0` | 安装目录 |

### 🔧 验证修改是否生效

```bash
# 检查已安装版本是否包含你的修改
grep "你的修改内容" ~/.cursor/extensions/trquant.trquant-cursor-extension-0.1.0/dist/extension.js

# 如果没有找到，说明需要重新打包安装
```

### 📝 一键部署脚本

```bash
#!/bin/bash
# deploy_extension.sh
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run compile && \
npx @vscode/vsce package --allow-missing-repository --no-dependencies && \
cursor --install-extension trquant-cursor-extension-0.1.0.vsix --force && \
echo "✅ 部署完成！请重新加载 Cursor 窗口"
```

---

## 更新日志

- 2025-12-05: 创建此文档，记录扩展部署流程







