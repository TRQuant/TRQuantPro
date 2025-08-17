# GitHub 仓库设置指南

本指南将帮助您将本地 QuantConnect Research 项目连接到 GitHub 进行版本控制和协作。

## 1. 在 GitHub 上创建仓库

### 步骤 1: 登录 GitHub
访问 [GitHub.com](https://github.com) 并登录您的账户。

### 步骤 2: 创建新仓库
1. 点击右上角的 "+" 按钮，选择 "New repository"
2. 填写仓库信息：
   - **Repository name**: `QuantConnect-Research` (或您喜欢的名称)
   - **Description**: `QuantConnect Research environment with automation tools`
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Add a README file" (我们已经有本地文件)
   - **不要**勾选 "Add .gitignore" (我们已经有自定义的 .gitignore)
   - **不要**勾选 "Choose a license" (可选)

3. 点击 "Create repository"

### 步骤 3: 复制仓库URL
创建完成后，复制仓库的 HTTPS URL，例如：
```
https://github.com/yourusername/QuantConnect-Research.git
```

## 2. 连接本地仓库到 GitHub

### 步骤 1: 设置远程仓库
```bash
# 在项目根目录执行
python3 Scripts/git_manager.py setup-remote --remote-url https://github.com/yourusername/QuantConnect-Research.git
```

### 步骤 2: 推送初始代码
```bash
# 推送所有代码到 GitHub
python3 Scripts/git_manager.py push
```

### 步骤 3: 验证连接
访问您的 GitHub 仓库页面，确认文件已成功上传。

## 3. 配置 Git 用户信息

如果还没有配置 Git 用户信息，请执行：

```bash
# 设置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 验证设置
git config --global user.name
git config --global user.email
```

## 4. 设置 SSH 密钥（推荐）

### 步骤 1: 生成 SSH 密钥
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your.email@example.com"

# 启动 ssh-agent
eval "$(ssh-agent -s)"

# 添加密钥到 ssh-agent
ssh-add ~/.ssh/id_ed25519
```

### 步骤 2: 添加公钥到 GitHub
```bash
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub
```

1. 在 GitHub 上，点击右上角头像 → Settings
2. 左侧菜单选择 "SSH and GPG keys"
3. 点击 "New SSH key"
4. 粘贴公钥内容，给密钥起个名字
5. 点击 "Add SSH key"

### 步骤 3: 更新远程仓库URL
```bash
# 将 HTTPS URL 更改为 SSH URL
python3 Scripts/git_manager.py setup-remote --remote-url git@github.com:yourusername/QuantConnect-Research.git
```

## 5. 日常使用流程

### 每日工作流程
```bash
# 1. 开始工作前，拉取最新更改
python3 Scripts/git_manager.py pull

# 2. 工作过程中，定期提交
python3 Scripts/git_manager.py auto-commit

# 3. 工作结束时，推送更改
python3 Scripts/git_manager.py push
```

### 定期备份
```bash
# 创建完整备份
./Scripts/auto_backup.sh

# 或创建 Git 备份分支
python3 Scripts/git_manager.py backup-branch --message "weekly_backup"
```

## 6. 协作开发

### 邀请协作者
1. 在 GitHub 仓库页面，点击 "Settings"
2. 左侧菜单选择 "Collaborators"
3. 点击 "Add people"
4. 输入用户名或邮箱，选择权限级别

### 分支管理
```bash
# 创建功能分支
git checkout -b feature/new-strategy

# 开发完成后合并到主分支
git checkout main
git merge feature/new-strategy

# 删除功能分支
git branch -d feature/new-strategy
```

## 7. 安全注意事项

### 敏感信息保护
- **不要**提交包含 API 密钥的文件
- **不要**提交个人配置文件
- 使用环境变量或 `.env` 文件存储敏感信息

### 数据文件管理
- 大型数据文件（如 `.zip`, `.csv`）已配置在 `.gitignore` 中
- 使用 `Scripts/data_downloader.py` 重新下载数据
- 考虑使用 Git LFS 管理大型文件

## 8. 故障排除

### 常见问题

1. **推送失败**
   ```bash
   # 检查远程仓库设置
   git remote -v
   
   # 重新设置远程仓库
   python3 Scripts/git_manager.py setup-remote --remote-url <your-repo-url>
   ```

2. **拉取冲突**
   ```bash
   # 查看冲突文件
   git status
   
   # 解决冲突后提交
   git add .
   git commit -m "Resolve merge conflicts"
   ```

3. **SSH 连接问题**
   ```bash
   # 测试 SSH 连接
   ssh -T git@github.com
   
   # 如果失败，检查 SSH 密钥
   ssh-add -l
   ```

### 获取帮助
- GitHub 文档: https://docs.github.com/
- Git 文档: https://git-scm.com/doc
- 项目文档: `QuantConnect_Research_Start.md`

## 9. 最佳实践

1. **频繁提交**: 每完成一个小功能就提交一次
2. **清晰的提交消息**: 使用描述性的提交消息
3. **定期推送**: 至少每天推送一次
4. **使用分支**: 为重要功能创建独立分支
5. **代码审查**: 在合并前进行代码审查
6. **备份策略**: 定期创建完整备份

---

**注意**: 确保您的 GitHub 账户启用了双因素认证，以提高安全性。 