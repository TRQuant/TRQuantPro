# Lavague 安装问题修复指南

> **问题**: `ModuleNotFoundError: No module named 'lavague'`  
> **原因**: pip安装到了错误的虚拟环境  
> **修复时间**: 2026-01-17

---

## 🔍 问题诊断

### 问题现象

```bash
$ python -c "import lavague"
ModuleNotFoundError: No module named 'lavague'

$ pip show lavague
Location: /home/taotao/dev/QuantTest/TRQuant/venv/lib/python3.12/site-packages
```

### 根本原因

**pip安装位置和Python使用位置不一致**：

| 项目 | 路径 | 说明 |
|------|------|------|
| **pip安装位置** | `/home/taotao/dev/QuantTest/TRQuant/venv/` | ❌ 旧虚拟环境 |
| **Python使用位置** | `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/` | ✅ 当前虚拟环境 |

---

## ✅ 正确安装方法（已验证）

### 方法1：使用 `python -m pip`（推荐）✅

```bash
# 进入项目目录
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 使用python -m pip确保使用正确的Python环境
./venv/bin/python -m pip install lavague

# 验证安装位置
./venv/bin/python -m pip show lavague | grep Location
# 应该显示: Location: /home/taotao/.cursor/worktrees/TRQuant/ope/venv/lib/python3.12/site-packages

# 验证导入
./venv/bin/python -c "import lavague; print('✅ 安装成功')"
```

### 方法2：使用完整路径的pip

```bash
# 使用完整路径的pip
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/pip install lavague

# 验证安装位置
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/pip show lavague | grep Location
```

### 方法3：激活虚拟环境后安装

```bash
# 激活虚拟环境
source /home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/activate

# 安装
pip install lavague

# 验证
python -c "import lavague; print('✅ 安装成功')"

# 退出虚拟环境
deactivate
```

---

## 🔧 验证安装

### 1. 检查安装位置

```bash
# 检查pip安装位置
./venv/bin/pip show lavague | grep Location

# 应该显示：
# Location: /home/taotao/.cursor/worktrees/TRQuant/ope/venv/lib/python3.12/site-packages
```

### 2. 测试导入

```bash
# 基础导入
./venv/bin/python -c "import lavague; print('✅ lavague导入成功')"

# 核心模块导入
./venv/bin/python -c "from lavague import ActionEngine, WorldModel, get_selenium_driver; print('✅ 核心模块导入成功')"
```

### 3. 检查Python路径

```bash
./venv/bin/python -c "import sys; print('Python路径:', sys.executable); print('site-packages:', [p for p in sys.path if 'site-packages' in p])"
```

---

## 📋 统一安装和使用规范

### TRQuant项目标准

**所有Python包安装必须使用**：

```bash
# 标准命令格式
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python -m pip install <package_name>
```

**或者使用完整路径**：

```bash
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/pip install <package_name>
```

### 在脚本中使用

**测试脚本** (`scripts/test_crawlers.py`):

```python
#!/usr/bin/env python
# 使用项目venv中的Python
# 确保脚本使用正确的Python解释器
```

**运行脚本**:

```bash
# 使用完整路径运行
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python scripts/test_crawlers.py
```

---

## 🚨 常见错误

### 错误1：使用系统pip

```bash
# ❌ 错误
pip install lavague  # 可能安装到系统Python

# ✅ 正确
./venv/bin/python -m pip install lavague
```

### 错误2：虚拟环境未激活

```bash
# ❌ 错误（未激活虚拟环境）
pip install lavague

# ✅ 正确
source venv/bin/activate
pip install lavague
```

### 错误3：使用错误的Python解释器

```bash
# ❌ 错误（使用系统Python）
python -c "import lavague"

# ✅ 正确（使用项目venv中的Python）
./venv/bin/python -c "import lavague"
```

---

## 📝 安装检查清单

安装lavague后，执行以下检查：

- [ ] `pip show lavague` 显示Location在正确的venv中
- [ ] `python -c "import lavague"` 成功导入
- [ ] `python -c "from lavague import ActionEngine"` 成功导入
- [ ] 测试脚本可以正常运行

---

## 🔗 相关文档

- `docs/CRAWLER_TEST_OPTIMIZATION.md` - 测试性能优化
- `docs/CRAWLER_TOOLS_COMPLETE_GUIDE.md` - 爬虫工具完整指南

---

**最后更新**: 2026-01-17
