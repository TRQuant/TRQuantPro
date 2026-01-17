# 在 Worktrees 根目录开发工作流

## ✅ 可行性分析

**结论：可以在 worktrees 根目录直接工作！**

### 当前状态

- ✅ worktrees根目录已有完整项目文件（20GB，173,950个文件）
- ✅ 有 `.git` 文件/目录（Git支持）
- ✅ 包含所有最新代码和配置
- ✅ Cursor默认在此工作

## 🎯 推荐方案：在worktrees根目录工作

### 优势

1. ✅ **Cursor默认工作目录** - 无需配置
2. ✅ **文件完整** - 包含所有最新代码和数据
3. ✅ **避免路径混淆** - 直接在当前目录工作
4. ✅ **包含运行时环境** - venv, data, logs等都在

### 需要做的事情

#### 1. 检查Git状态

```bash
cd ~/.cursor/worktrees/TRQuant
git status
git remote -v
git branch
```

#### 2. 配置Git（如果需要）

如果Git未配置或需要重新初始化：

```bash
cd ~/.cursor/worktrees/TRQuant

# 选项A：连接到主目录的Git仓库（推荐）
# 如果是worktree，已经连接
git remote -v

# 选项B：独立Git仓库（如果需要）
git init
git remote add origin <主目录的remote URL>
git remote add upstream /home/taotao/dev/QuantTest/TRQuant/.git
```

#### 3. 清理不需要的目录

```bash
cd ~/.cursor/worktrees/TRQuant

# 删除ope目录（如果不再需要）
rm -rf ope/

# 或者保留作为备份
mv ope/ ope_backup_$(date +%Y%m%d)/
```

#### 4. 开发工作流

```bash
# 在worktrees根目录开发
cd ~/.cursor/worktrees/TRQuant

# 编写代码
# ...

# 提交Git
git add .
git commit -m "开发内容"

# 推送到远程（如果有remote）
git push

# 或同步到主目录（如果使用独立仓库）
# 方法1：通过remote同步
git push origin main

# 方法2：使用rsync同步代码文件到主目录
# （但建议使用Git方式）
```

## 🔄 与主目录的同步

### 方案A：Git同步（推荐）

如果worktrees根目录是Git worktree或连接了remote：

```bash
# 在worktrees根目录开发并提交
cd ~/.cursor/worktrees/TRQuant
git add .
git commit -m "开发内容"
git push

# 在主目录拉取
cd /home/taotao/dev/QuantTest/TRQuant
git pull
```

### 方案B：独立开发，定期同步

如果worktrees根目录是独立的Git仓库：

```bash
# 1. 在worktrees根目录开发
cd ~/.cursor/worktrees/TRQuant
# 开发代码...
git add .
git commit -m "开发内容"

# 2. 创建patch或导出更改
git format-patch -1 HEAD

# 3. 在主目录应用
cd /home/taotao/dev/QuantTest/TRQuant
git am <patch文件>

# 或者使用rsync同步代码文件（不推荐，会丢失Git历史）
```

### 方案C：主目录作为backup，worktrees作为主工作区

如果主目录只作为备份：

```bash
# 定期同步代码到主目录（使用rsync，排除运行时文件）
cd ~/.cursor/worktrees/TRQuant
rsync -av --exclude='venv' --exclude='data' --exclude='logs' \
  --exclude='.cache' --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='node_modules' --exclude='.git' \
  . /home/taotao/dev/QuantTest/TRQuant/
```

## ⚠️ 注意事项

### 1. Git配置

- 确保Git正常工作
- 配置user.name和user.email
- 设置remote（如果需要）

### 2. 路径引用

代码中如有硬编码路径，确保指向worktrees目录：
```python
PROJECT_ROOT = Path('/home/taotao/.cursor/worktrees/TRQuant')
```

或使用环境变量：
```bash
export TRQUANT_ROOT=/home/taotao/.cursor/worktrees/TRQuant
```

### 3. 备份策略

- 定期提交到Git
- 重要更改推送到remote
- 定期同步到主目录作为备份

### 4. 清理策略

- 定期清理缓存文件（`.cache`, `__pycache__`等）
- 清理旧的回测结果和日志
- 但保留运行时必要的文件（venv, data等）

## 📝 快速开始

```bash
# 1. 进入worktrees根目录
cd ~/.cursor/worktrees/TRQuant

# 2. 检查Git状态
git status

# 3. 如果Git未配置，初始化
# git init  # 仅在需要时

# 4. 配置Git用户（如果未配置）
# git config user.name "Your Name"
# git config user.email "your.email@example.com"

# 5. 开始开发
# 在Cursor中打开此目录
# File -> Open Folder -> ~/.cursor/worktrees/TRQuant

# 6. 开发完成后提交
git add .
git commit -m "描述"
git push  # 如果有remote
```

## 🎯 最终建议

**✅ 推荐：在worktrees根目录工作**

理由：
1. Cursor默认在此工作
2. 文件完整，包含所有最新代码
3. 包含运行时环境
4. 避免路径混淆
5. 减少同步需求

**同步策略**：
- 使用Git进行版本控制
- 定期推送到remote（如果有）
- 定期同步到主目录作为备份（可选）










