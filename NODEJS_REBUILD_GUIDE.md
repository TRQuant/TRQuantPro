# Node.js 依赖重建指南

## 📦 概述

本项目包含两个需要 Node.js 依赖的部分：
1. **VS Code 扩展** (`extension/`)
2. **AShare Manual 文档系统** (`extension/AShare-manual/`)

## 🔧 重建步骤

### 1. 前置要求

确保已安装：
- **Node.js** 18.x 或更高版本
- **npm** 9.x 或更高版本

检查版本：
```bash
node --version
npm --version
```

### 2. 重建 VS Code 扩展依赖

```bash
cd extension
npm install
```

这将安装扩展所需的依赖，包括：
- TypeScript 编译工具
- Webpack 打包工具
- VS Code API 类型定义
- 其他开发依赖

### 3. 编译扩展

```bash
cd extension
npm run compile
```

或使用开发模式（自动监听文件变化）：
```bash
npm run watch
```

### 4. 打包扩展（可选）

如果需要生成 `.vsix` 文件：

```bash
cd extension
npm install -g @vscode/vsce  # 如果未安装
vsce package
```

或使用 npx（无需全局安装）：
```bash
cd extension
npx vsce package
```

### 5. 重建 AShare Manual 文档系统

```bash
cd extension/AShare-manual
npm install
```

这将安装 Astro 框架及其依赖，包括：
- Astro 构建工具
- Markdown 处理库
- 图片处理库（sharp）
- 其他文档系统依赖

### 6. 构建文档系统（可选）

如果需要构建静态站点：

```bash
cd extension/AShare-manual
npm run build
```

开发模式（热重载）：
```bash
npm run dev
```

## 📋 依赖清单

### extension/package.json 主要依赖

- **开发依赖**:
  - `@types/node`: Node.js 类型定义
  - `@types/vscode`: VS Code API 类型
  - `typescript`: TypeScript 编译器
  - `webpack`: 模块打包工具
  - `ts-loader`: TypeScript 加载器
  - `eslint`: 代码检查工具

- **运行时依赖**:
  - `axios`: HTTP 客户端

### extension/AShare-manual/package.json 主要依赖

- **Astro 框架**: 静态站点生成器
- **Markdown 处理**: 支持 Markdown 渲染
- **图片处理**: sharp 库用于图片优化
- **其他工具**: 各种 Astro 插件和工具

## ⚠️ 注意事项

1. **网络要求**: 首次安装需要稳定的网络连接，npm 会从 registry 下载包
2. **磁盘空间**: node_modules 目录可能占用 200-500MB 空间
3. **平台差异**: 某些依赖（如 sharp）会根据平台下载不同的二进制文件
4. **版本锁定**: 项目使用 `package-lock.json` 锁定版本，确保一致性

## 🔍 故障排除

### npm install 失败

1. 清除 npm 缓存：
   ```bash
   npm cache clean --force
   ```

2. 删除 node_modules 和 package-lock.json，重新安装：
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. 使用国内镜像（如淘宝镜像）：
   ```bash
   npm config set registry https://registry.npmmirror.com
   npm install
   ```

### 编译错误

1. 确保 TypeScript 版本兼容：
   ```bash
   npm list typescript
   ```

2. 检查 Node.js 版本是否符合要求

3. 查看详细错误信息：
   ```bash
   npm run compile -- --verbose
   ```

## 📝 验证安装

### 验证扩展依赖

```bash
cd extension
npm list --depth=0
```

### 验证文档系统依赖

```bash
cd extension/AShare-manual
npm list --depth=0
```

## 🚀 快速重建脚本

创建 `rebuild_nodejs.sh`（Linux/macOS）或 `rebuild_nodejs.ps1`（Windows）：

```bash
#!/bin/bash
# rebuild_nodejs.sh

echo "重建 VS Code 扩展依赖..."
cd extension
npm install
echo "✓ 扩展依赖安装完成"

echo "重建 AShare Manual 依赖..."
cd AShare-manual
npm install
echo "✓ 文档系统依赖安装完成"

echo "所有 Node.js 依赖重建完成！"
```

---

**最后更新**: 2025-12-06


