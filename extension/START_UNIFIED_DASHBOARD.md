# 🐉 TRQuant 统一仪表板启动指南

## ⚠️ 重要提示

如果命令面板或侧栏中没有看到"打开统一仪表板"选项，**必须重新加载Cursor窗口**！

## 🔄 第一步：重新加载窗口（必须）

1. 按 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. 输入: `Developer: Reload Window`
3. 回车执行

**这是最关键的步骤！** VS Code扩展在修改后必须重新加载才能识别新的命令和视图。

## 🚀 第二步：启动统一仪表板

### 方法1: 命令面板（最可靠）

1. 按 `Ctrl+Shift+P`
2. 输入: `TRQuant: 打开统一仪表板`
3. 回车执行

### 方法2: 侧栏快捷按钮

1. 点击左侧 **Activity Bar** 的 **TRQuant** 图标（🐉）
2. 在侧栏中找到 **🐉 统一仪表板** 视图
3. 点击 **"打开统一仪表板"** 按钮

### 方法3: 侧栏树视图

1. 点击左侧 **Activity Bar** 的 **TRQuant** 图标
2. 展开 **📊 9步工作流** 视图
3. 点击 **🏠 打开统一仪表板**

## 🔍 验证命令是否可用

在命令面板中（`Ctrl+Shift+P`），输入 `TRQuant`，应该能看到：

- ✅ `TRQuant: 打开统一仪表板`
- ✅ `TRQuant: 打开工作流面板`
- ✅ `TRQuant: 打开十倍股仪表盘`
- ✅ `TRQuant: 打开策略生成器`

**如果看不到这些命令，说明扩展未正确加载！**

## 🛠️ 故障排查

### 问题1: 重新加载后仍然看不到命令

**解决方案：使用F5调试模式（最可靠）**

1. 在Cursor中打开 `/home/taotao/dev/QuantTest/TRQuant/extension` 文件夹
2. 按 `F5` 键
3. 选择 "Run Extension"
4. 在新窗口中测试

### 问题2: 侧栏没有TRQuant图标

**解决方案：检查扩展是否启用**

1. 按 `Ctrl+Shift+X` 打开扩展面板
2. 搜索 `TRQuant`
3. 确认扩展已启用（不是禁用状态）

### 问题3: 命令执行后没有反应

**解决方案：检查编译输出**

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm run compile
```

查看是否有编译错误。

### 问题4: 仍然无法启动

**解决方案：查看扩展日志**

1. 按 `Ctrl+Shift+U` 打开输出面板
2. 下拉选择 `TRQuant` 通道
3. 查看错误信息

## 📋 技术细节

### 命令注册位置
- **package.json**: `contributes.commands` 中定义命令
- **registerPanels.ts**: 注册命令处理器
- **extension.ts**: 调用 `registerPanels()` 和 `registerSidebarProviders()`

### 视图注册位置
- **package.json**: `contributes.viewsContainers` 和 `contributes.views` 中定义视图
- **sidebarProvider.ts**: 实现视图提供者
- **extension.ts**: 调用 `registerSidebarProviders()`

### 为什么需要重新加载？

VS Code扩展在启动时读取 `package.json` 配置。如果配置已更改但窗口未重新加载，VS Code仍然使用旧的配置，导致新命令和视图不可见。

## ✅ 成功标志

当统一仪表板成功启动时，你应该看到：

1. 一个新的Webview面板打开
2. 标题显示 "🐉 韬睿量化 - 统一仪表板"
3. 面板中有三个标签页：
   - 📊 9步工作流
   - 🎯 十倍股识别
   - 📈 趋势策略

---

**最后更新**: 2025-12-19
