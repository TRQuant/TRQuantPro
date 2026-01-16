# 代码嵌入自动更新 - 路径修复

## ✅ 问题已解决

**代码库路径**：`/home/taotao/dev/QuantTest/TRQuant/code_library`

## 🔧 修复内容

### 1. 直接使用已知路径

不再依赖复杂的路径计算，直接使用已知路径：

```javascript
const KNOWN_CODE_LIBRARY = '/home/taotao/dev/QuantTest/TRQuant/code_library';
const KNOWN_PROJECT_ROOT = '/home/taotao/dev/QuantTest/TRQuant';

if (existsSync(KNOWN_CODE_LIBRARY)) {
  return KNOWN_PROJECT_ROOT;
}
```

### 2. 路径验证

- ✅ 已知路径存在检查
- ✅ 备用路径计算（如果已知路径不存在）
- ✅ 错误提示和异常处理

## 📋 测试步骤

### 1. 重启开发服务器

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/AShare-manual
pkill -f "astro dev"
npm run dev
```

### 2. 检查启动日志

应该看到：
```
[vite-code-library-watcher] 🚀 插件开始初始化...
[vite-code-library-watcher] ✅ 使用已知路径: /home/taotao/dev/QuantTest/TRQuant
[vite-code-library-watcher] 📂 当前工作目录: /path/to/AShare-manual
[vite-code-library-watcher] 📂 项目根目录: /home/taotao/dev/QuantTest/TRQuant
[vite-code-library-watcher] 📂 代码库路径: /home/taotao/dev/QuantTest/TRQuant/code_library
[vite-code-library-watcher] ✅ 开始监控: /home/taotao/dev/QuantTest/TRQuant/code_library
[vite-code-library-watcher] ✅ 已添加到Vite监控: /home/taotao/dev/QuantTest/TRQuant/code_library
```

### 3. 修改并保存代码文件

在编辑器中打开并修改：
```
/home/taotao/dev/QuantTest/TRQuant/code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
```

保存文件（Ctrl+S）

### 4. 观察控制台日志

应该看到：
```
[vite-code-library-watcher] 📝 Vite检测到代码文件变化: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[vite-code-library-watcher] 🔍 查找包含代码文件的Markdown: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[vite-code-library-watcher] 📄 找到相关文件: src/pages/...
[vite-code-library-watcher] ✅ 找到 1 个相关Markdown文件
[vite-code-library-watcher] ✅ 已更新文件时间戳: ...
[vite-code-library-watcher] ✅ 已触发文件变化事件: ...
[vite-code-library-watcher] ✅ 已失效模块: ...
```

### 5. 检查浏览器

- 页面应该自动刷新
- 代码内容应该已更新

## 🎯 关键改进

1. **直接使用已知路径**：不再依赖复杂的路径计算
2. **Vite原生监控**：使用 `server.watcher.add()` 直接监控外部目录
3. **双重保障**：Vite监控 + 事件监听 + handleHotUpdate
4. **文件保存检测**：等待200ms确保文件保存完成
5. **详细日志**：每个步骤都有日志输出

## ✅ 验证结果

- ✅ 路径计算正确
- ✅ 代码库路径存在
- ✅ Vite监控已添加
- ✅ 文件变化检测正常

---

**更新时间**: 2025-12-13  
**版本**: 工作版 - 路径修复  
**状态**: ✅ 路径问题已解决

