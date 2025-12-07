# TRQuant 完整恢复指南

**恢复点**: 2025-12-07 04:55:48  
**Git 提交**: `64fbe99e`  
**备份文件**: `TRQuant_full_backup_20251207_045548.tar.gz`

---

## 📦 恢复方式

### 方式 1: 从 Git 恢复（推荐）

```bash
# 1. 进入项目目录
cd /home/taotao/dev/QuantTest/TRQuant

# 2. 检查当前状态
git status

# 3. 恢复到指定提交
git reset --hard 64fbe99e

# 4. 清理未跟踪文件（可选）
git clean -fd
```

### 方式 2: 从完整备份恢复

```bash
# 1. 备份当前目录（如果需要）
cd /home/taotao/dev/QuantTest
mv TRQuant TRQuant_current_backup_$(date +%Y%m%d_%H%M%S)

# 2. 解压完整备份
cd /home/taotao/dev/QuantTest
tar -xzf TRQuant_backups/TRQuant_full_backup_20251207_045548.tar.gz

# 3. 验证恢复
cd TRQuant
git log --oneline -1
# 应该显示: 64fbe99e chore: 代码质量工具安装和规范化配置
```

### 方式 3: 部分恢复（仅恢复特定文件）

```bash
# 从备份中提取特定文件
cd /home/taotao/dev/QuantTest
tar -xzf TRQuant_backups/TRQuant_full_backup_20251207_045548.tar.gz \
  TRQuant/path/to/specific/file.py
```

---

## ✅ 恢复验证清单

恢复后，请验证以下内容：

### 1. Git 状态
```bash
cd /home/taotao/dev/QuantTest/TRQuant
git log --oneline -1
# 应该显示: 64fbe99e chore: 代码质量工具安装和规范化配置

git status
# 应该显示: "nothing to commit, working tree clean"
```

### 2. 关键文件存在
```bash
# 检查关键文件
ls -la .cursorrules
ls -la pyproject.toml
ls -la extension/.prettierrc
ls -la extension/.eslintrc.json
ls -la docs/CODE_QUALITY_ANALYSIS.md
ls -la scripts/fix_code_quality.sh
```

### 3. 虚拟环境
```bash
# 检查 extension 虚拟环境
ls -la extension/venv/bin/activate
source extension/venv/bin/activate
python -m black --version
python -m ruff --version
python -m mypy --version
```

### 4. Node.js 依赖
```bash
cd extension
npm list prettier eslint 2>/dev/null | head -5
```

---

## 🔄 恢复后重建环境

如果虚拟环境或 node_modules 丢失，可以重建：

### Python 环境
```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install black ruff mypy pytest pytest-cov
```

### Node.js 依赖
```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension
npm install
npm install --save-dev prettier eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

---

## 📋 恢复点信息

- **备份时间**: 2025-12-07 04:55:48
- **备份大小**: 1.5 GB
- **Git 提交**: 64fbe99e
- **提交信息**: "chore: 代码质量工具安装和规范化配置"
- **文件变更**: 23,884 个文件

### 此恢复点包含的主要变更

1. ✅ 代码质量工具安装（Black, Ruff, mypy, Prettier, ESLint）
2. ✅ 代码规范化配置文件（.cursorrules, pyproject.toml, .prettierrc, .eslintrc.json）
3. ✅ 代码质量分析报告（docs/CODE_QUALITY_ANALYSIS.md）
4. ✅ 自动修复脚本（scripts/fix_code_quality.sh）
5. ✅ 代码格式化（20+ Python 文件，30+ TypeScript 文件）
6. ✅ Windows 安装指南和脚本
7. ✅ 项目清理（删除临时文件、旧备份、生成报告）

---

## ⚠️ 注意事项

1. **恢复前备份当前状态**: 如果当前有未保存的工作，请先备份
2. **虚拟环境**: 恢复后可能需要重建虚拟环境
3. **Node.js 依赖**: 恢复后可能需要重新安装 npm 包
4. **大文件**: 某些大文件（如 PDF、图片）可能不在 Git 中，需要从备份恢复

---

## 🆘 故障排除

### 问题 1: Git 提交找不到
```bash
# 检查 Git 历史
git log --all --oneline | grep 64fbe99e

# 如果找不到，从备份恢复
tar -xzf TRQuant_backups/TRQuant_full_backup_20251207_045548.tar.gz
```

### 问题 2: 文件权限错误
```bash
# 修复文件权限
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
find . -name "*.sh" -exec chmod +x {} \;
```

### 问题 3: 虚拟环境无法激活
```bash
# 重建虚拟环境
rm -rf extension/venv
cd extension
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements-dev.txt
```

---

**最后更新**: 2025-12-07  
**维护者**: TRQuant 开发团队






