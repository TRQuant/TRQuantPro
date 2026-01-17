# Git Token 配置说明

> **版本**: v1.2  
> **更新**: 2026-01-15  
> **用途**: US-China 工作站同步专用Token  
> **状态**: ✅ 已配置并测试通过

---

## 🔐 Token 信息

### Token 用途
- **专用用途**: US-China 工作站跨平台同步
- **仓库**: `TRQuant/TRQuantPro`
- **分支**: `ope` (Ubuntu) 和 `windows` (Windows)
- **Git用户**: `TRQuant` / `zhutechllc@gmail.com`
- **创建时间**: 2026-01-15

### Token 配置

**Token**: `[请使用Personal Access Token，不要提交到仓库]`

**远程仓库URL格式**:
```bash
https://[TOKEN]@github.com/TRQuant/TRQuantPro.git
```

**注意**: Token不应提交到仓库，请使用环境变量或安全存储。

---

## 📋 配置步骤

### Ubuntu端（美国Linux系统）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 配置Git用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"

# 更新远程仓库URL（请替换[TOKEN]为实际Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 验证配置
git remote -v
```

### Windows端（中国Windows系统）

```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 配置Git用户信息
git config user.name "TRQuant"
git config user.email "zhutechllc@gmail.com"

# 更新远程仓库URL（请替换[TOKEN]为实际Token）
git remote set-url origin https://[TOKEN]@github.com/TRQuant/TRQuantPro.git

# 验证配置
git remote -v
```

---

## ⚠️ 重要提示

1. **Token权限**: 确保Token具有以下权限：
   - `repo` - 完整仓库访问权限
   - `workflow` - 工作流访问权限（如需要）

2. **Token安全**:
   - **不要将Token提交到Git仓库**
   - 不要在公开场合分享Token
   - 如果Token泄露，立即在GitHub上撤销并重新生成
   - 使用环境变量或安全存储方式管理Token

3. **Token验证**:
   - 配置后使用 `git push --dry-run` 测试连接
   - 如果出现403错误，检查Token权限和仓库访问权限

---

## 🔧 故障排除

### 问题1: 403 Permission Denied

**原因**: Token没有权限或仓库访问权限不足

**解决方案**:
1. 检查Token是否具有 `repo` 权限
2. 确认Token对应的GitHub账号有仓库访问权限
3. 检查仓库是否为私有仓库，需要相应权限

### 问题2: Token过期

**原因**: Token已过期或被撤销

**解决方案**:
1. 在GitHub Settings → Developer settings → Personal access tokens 检查Token状态
2. 如果过期，生成新Token并更新配置

### 问题3: Push Protection阻止

**原因**: GitHub检测到提交中包含敏感信息（如Token）

**解决方案**:
1. 从提交历史中移除包含Token的文件
2. 使用 `git commit --amend` 或 `git rebase` 修改提交
3. 确保文档中不包含实际Token，只使用占位符

---

## 📝 相关文档

- `docs/GIT_SYNC_COMPLETE_GUIDE.md` - Git同步完整指南
- `docs/CROSS_PLATFORM_SYNC_GUIDE.md` - 跨平台同步指南
- `docs/SYNC_SOLUTION_SUMMARY.md` - 同步方案总结

---

**最后更新**: 2026-01-15  
**维护者**: TRQuant Team
