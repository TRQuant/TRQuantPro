# 自动提交和推送指南

TRQuant 支持自动提交和推送功能，并保持版本号管理。

## 版本管理

版本号存储在 `VERSION` 文件中，格式为 `MAJOR.MINOR.PATCH`（如 `2.0.0`）。

### 查看当前版本

```bash
cat VERSION
```

### 更新版本号

```python
from core.version import increment_version

# 递增补丁版本 (2.0.0 -> 2.0.1)
new_version = increment_version('patch')

# 递增次版本 (2.0.0 -> 2.1.0)
new_version = increment_version('minor')

# 递增主版本 (2.0.0 -> 3.0.0)
new_version = increment_version('major')
```

## 自动提交和推送

### 方法1: 使用Python脚本（推荐）

```bash
python3 scripts/auto_commit_push.py
```

### 方法2: 使用Shell脚本

```bash
./scripts/auto_commit_push.sh
```

### 方法3: 使用Git Alias

首先设置alias：
```bash
git config alias.acp '!f() { python3 scripts/auto_commit_push.py; }; f'
```

然后使用：
```bash
git acp
```

## 自动推送设置

### 启用自动推送（每次commit后自动push）

运行设置脚本：
```bash
./scripts/setup_auto_commit.sh
```

选择启用自动推送，这样每次 `git commit` 后会自动执行 `git push`。

### 手动控制

如果未启用自动推送，可以：
1. 手动执行 `python3 scripts/auto_commit_push.py`
2. 或先 `git commit`，再 `git push`

## Commit Message格式

自动提交的commit message格式：
```
chore: auto commit [v2.0.0] - 2025-11-30 12:34:56

自动提交更新
版本: v2.0.0
时间: 2025-11-30 12:34:56
```

## 注意事项

1. **敏感文件**: 确保 `.gitignore` 正确配置，敏感配置文件不会被提交
2. **版本号**: 版本号会自动包含在commit message中
3. **网络**: 推送需要网络连接，失败时会提示手动处理
4. **权限**: 确保有GitHub推送权限

## 故障排除

### 推送失败

如果推送失败，检查：
1. 网络连接
2. GitHub认证（token或SSH密钥）
3. 远程仓库地址：`git remote -v`

### 版本号未更新

确保 `VERSION` 文件存在且格式正确：
```bash
echo "2.0.0" > VERSION
```

