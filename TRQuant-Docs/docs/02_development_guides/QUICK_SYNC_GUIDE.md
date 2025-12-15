# 快速同步指南

## 🎯 核心问题

- **主项目目录**：`/home/taotao/dev/QuantTest/TRQuant`（Git仓库，Cursor可管理）
- **工作目录**：`~/.local/share/jqquant`（实际运行，最新代码）

## ⚡ 快速同步（3步）

### 1. 同步代码到主项目
```bash
cd ~/.local/share/jqquant
python scripts/sync_to_main_project.py
```

### 2. 在主项目中提交
```bash
cd /home/taotao/dev/QuantTest/TRQuant
git add .
git commit -m "同步最新代码"
git push  # 可选
```

### 3. 在Cursor中打开主项目
- File → Open Folder
- 选择 `/home/taotao/dev/QuantTest/TRQuant`

## 🔄 日常开发流程

### 选项A：在主项目开发（推荐）

1. 在Cursor中打开主项目
2. 编写代码
3. 测试运行（使用环境变量）
4. 提交Git

### 选项B：在安装目录开发（当前）

1. 在安装目录编写代码
2. 定期同步到主项目
3. 在主项目提交Git

## 🐳 Docker关系

Docker使用 `~/.local/share/jqquant` 作为数据目录：
- 配置：`~/.local/share/jqquant/config`
- 日志：`~/.local/share/jqquant/logs`
- 结果：`~/.local/share/jqquant/results`

**不影响代码开发**，代码可以在主项目中开发。

---

*快速参考 - 详细说明见 PROJECT_DIRECTORY_EXPLANATION.md*

