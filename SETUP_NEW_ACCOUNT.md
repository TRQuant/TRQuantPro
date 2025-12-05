# 新账户开发环境准备工作清单

## 📋 当前状态检查

✅ **已检查项：**
- Node.js: v22.18.0 ✅
- npm: 11.5.2 ✅
- Python: 3.12.3 ✅
- 项目文件: 已恢复 ✅
- node_modules: 已存在 ✅
- dist/: 已编译 ✅

## 🔧 需要执行的准备工作

### 1. 更新 Git 用户信息（新账户）

```bash
# 设置新的 Git 用户信息
git config user.name "你的新用户名"
git config user.email "你的新邮箱"

# 验证配置
git config --get user.name
git config --get user.email
```

### 2. 更新 Git Remote（如果需要）

```bash
# 查看当前 remote
git remote -v

# 如果需要更新到新账户的仓库
git remote set-url origin https://github.com/新用户名/TRQuant.git

# 或者添加新的 remote
git remote add new-origin https://github.com/新用户名/TRQuant.git
```

### 3. 重新安装 Node.js 依赖（确保依赖最新）

```bash
cd extension
npm install
```

### 4. 重新编译 TypeScript

```bash
cd extension
npm run compile
```

### 5. 安装 Python 依赖

```bash
# 进入 Python 目录
cd extension/python

# 安装核心依赖（最小安装）
pip install numpy pandas scikit-learn

# 或者安装推荐依赖（含免费数据源）
pip install numpy pandas scikit-learn akshare

# 或者完整安装
pip install -r requirements.txt
```

### 6. 检查配置文件

```bash
# 检查扩展配置
cat extension/package.json | grep -A 5 "publisher\|repository"

# 检查 Python 配置（如果需要）
ls -la extension/python/bridge.py
```

### 7. 验证编译结果

```bash
cd extension
ls -la dist/
# 应该看到 extension.js 和 extension.js.map
```

### 8. 测试扩展（可选）

```bash
# 在 VS Code/Cursor 中
# 1. 按 F5 启动调试
# 2. 或使用命令面板: "Developer: Reload Window"
```

## 📝 注意事项

1. **Git 历史**: 当前在 `67dccf3` 提交，这是今天最早的状态
2. **未跟踪文件**: `workbenchPanel.ts` 等未跟踪文件可以保留或删除
3. **缺失文件**: `extension.ts` 中引用了不存在的文件（`projectConfig.ts` 等），这些需要后续创建或移除引用
4. **Python 环境**: 建议使用虚拟环境（venv）隔离依赖

## 🚀 快速启动命令（一键执行）

```bash
# 1. 更新 Git 配置（请替换为你的信息）
git config user.name "你的新用户名"
git config user.email "你的新邮箱"

# 2. 安装依赖并编译
cd extension
npm install
npm run compile

# 3. 安装 Python 依赖（最小安装）
cd python
pip install numpy pandas scikit-learn akshare
cd ../..

# 4. 验证
ls -la extension/dist/
```

## ✅ 完成检查清单

- [ ] Git 用户信息已更新
- [ ] Git remote 已更新（如需要）
- [ ] Node.js 依赖已安装
- [ ] TypeScript 已编译
- [ ] Python 依赖已安装
- [ ] 编译结果验证通过
- [ ] 扩展可以正常加载

---

**准备完成后，就可以开始新的开发工作了！** 🎉

