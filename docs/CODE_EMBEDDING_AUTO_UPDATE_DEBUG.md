# 代码嵌入自动更新调试指南

## 🔍 问题诊断

### 问题：代码文件修改后没有自动更新

### 可能原因

1. **路径匹配问题** ✅ 已修复
   - Markdown文件中的路径：`code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py`
   - 代码提取的相对路径：`003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py`
   - **修复**：支持完整路径和相对路径两种格式

2. **服务器未启动**
   - 检查：`ps aux | grep "astro dev"`

3. **集成未加载**
   - 检查控制台是否有 `[watch-code-library] ✅ 开始监控` 日志

4. **文件监控未触发**
   - 检查控制台是否有 `[watch-code-library] 📝 检测到代码文件变化` 日志

## ✅ 修复方案

### 1. 路径匹配修复

支持三种路径格式：

```javascript
// 1. 完整路径（包含 code_library/ 前缀）
code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py

// 2. 相对路径（不包含 code_library/ 前缀）
003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py

// 3. 文件名（只匹配文件名）
code_3_2_2_analyze_price_dimension.py
```

### 2. 调试步骤

#### 步骤1：检查服务器是否启动

```bash
ps aux | grep "astro dev"
```

#### 步骤2：检查集成是否加载

查看控制台输出，应该看到：
```
[watch-code-library] ✅ 开始监控: /path/to/code_library
```

#### 步骤3：修改代码文件

```bash
cd /home/taotao/dev/QuantTest/TRQuant
echo "" >> code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
```

#### 步骤4：检查控制台日志

应该看到：
```
[watch-code-library] 📝 检测到代码文件变化: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[watch-code-library] 查找包含代码文件的Markdown: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[watch-code-library] 已更新: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.2_Market_Status_CN.md
[watch-code-library] 已更新 1 个Markdown文件
```

#### 步骤5：检查浏览器

- 页面应该自动刷新
- 代码内容应该已更新

## 🔧 手动测试

### 测试路径匹配

```javascript
const codeFileRelativePath = '003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py';
const markdownContent = '<CodeFromFile filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py" />';

// 应该匹配成功
const escapedPath = codeFileRelativePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const escapedFullPath = `code_library/${escapedPath}`;
const pattern = new RegExp(`<CodeFromFile[^>]*filePath=["']${escapedFullPath}["']`, 'i');
console.log(pattern.test(markdownContent)); // 应该输出 true
```

## 📋 检查清单

- [ ] 服务器已启动
- [ ] 集成已加载（看到开始监控日志）
- [ ] 代码文件路径正确
- [ ] Markdown文件包含 CodeFromFile 标签
- [ ] 路径匹配成功（看到已更新日志）
- [ ] 浏览器自动刷新
- [ ] 代码内容已更新

## 🐛 常见问题

### 问题1：没有看到开始监控日志

**原因**：集成未加载或代码库路径不正确

**解决**：
1. 检查 `astro.config.mjs` 中是否注册了集成
2. 检查代码库路径是否正确
3. 重启开发服务器

### 问题2：看到检测到变化，但没有更新Markdown文件

**原因**：路径匹配失败

**解决**：
1. 检查Markdown文件中的 `filePath` 属性
2. 确保路径格式正确
3. 查看控制台的警告日志

### 问题3：更新了Markdown文件，但页面没有刷新

**原因**：Astro没有检测到Markdown文件变化

**解决**：
1. 检查时间戳注释是否正确添加
2. 手动刷新浏览器
3. 检查Astro构建日志

---

**更新时间**: 2025-12-13  
**状态**: ✅ 路径匹配已修复

