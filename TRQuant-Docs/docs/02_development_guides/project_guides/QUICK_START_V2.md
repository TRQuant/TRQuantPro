# TRQuant 快速开始指南

## 🚀 一键安装（复制粘贴到终端）

### 步骤1：编译

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run compile
```

### 步骤2：打包

```bash
npx @vscode/vsce package --allow-missing-repository --no-dependencies
```

### 步骤3：安装到Cursor

```bash
cursor --install-extension trquant-cursor-extension-0.1.0.vsix
```

### 步骤4：重启Cursor

关闭并重新打开Cursor。

---

## 🔧 调试模式

### 方式A：F5调试

1. 在Cursor中打开 `/home/taotao/dev/QuantTest/TRQuant/extension` 文件夹
2. 按 `F5` 键
3. 选择 "Run Extension"
4. 新窗口中测试

### 方式B：命令行调试

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run watch &
cursor --extensionDevelopmentPath=$(pwd)
```

---

## ✅ 验证安装

1. 按 `Ctrl+Shift+P`
2. 输入 `TRQuant`
3. 应该看到所有TRQuant命令

---

## 📋 完整命令列表

| 命令 | 功能 |
|------|------|
| `TRQuant: 打开主界面` | Dashboard |
| `TRQuant: 显示欢迎页面` | 欢迎引导 |
| `TRQuant: 新建量化项目` | 创建项目 |
| `TRQuant: 获取市场状态` | 市场分析 |
| `TRQuant: 获取投资主线` | 热门板块 |
| `TRQuant: 推荐因子` | 因子推荐 |
| `TRQuant: 生成策略代码` | AI生成 |
| `TRQuant: 运行回测` | 执行回测 |

---

## 🐛 问题排查

### 编译错误

```bash
# 清理重新编译
rm -rf node_modules dist
npm install
npm run compile
```

### Python后端测试

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/python
echo '{"action": "health_check", "params": {}}' | python bridge.py
```

### 查看日志

在Cursor中：`Ctrl+Shift+U` → 选择 `TRQuant`







