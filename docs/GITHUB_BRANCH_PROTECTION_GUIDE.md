# GitHub分支保护设置和调整完整指南

> **调研时间**: 2024-12-14  
> **调研人**: 轩辕剑灵  
> **仓库**: ZhuTechLLC/TRQuantExt

## 📍 访问路径

### 直接链接
- **分支设置页面**: https://github.com/ZhuTechLLC/TRQuantExt/settings/branches
- **仓库设置**: https://github.com/ZhuTechLLC/TRQuantExt/settings

### 手动导航步骤
1. 访问仓库主页: https://github.com/ZhuTechLLC/TRQuantExt
2. 点击 **Settings** 标签
3. 在左侧菜单找到 **Branches**（在 "Code and automation" 部分下）

## 🔍 查看当前分支保护规则

### 步骤
1. 进入分支设置页面
2. 查看 **"Branch protection rules"** 部分
3. 查看是否有针对以下分支的保护规则：
   - `main`
   - `main-clean`
   - 或其他分支

### 检查内容
- 规则名称/分支模式
- 启用的保护选项
- 规则创建/修改时间

## ✅ 临时禁用分支保护（允许推送）

### 方法1：编辑规则（推荐，保留规则配置）

**步骤**：
1. 找到保护 `main` 或目标分支的规则
2. 点击规则右侧的 **"Edit"** 按钮
3. **取消勾选以下限制选项**：
   - ❌ **Require a pull request before merging**
     - 取消勾选：允许直接推送
   - ❌ **Require approvals**
     - 取消勾选：不需要审批即可推送
   - ❌ **Restrict who can push to matching branches**
     - 取消勾选：允许所有有权限的用户推送
   - ❌ **Do not allow bypassing the above settings**
     - 取消勾选：允许管理员绕过规则
4. **保留以下选项**（如果需要）：
   - ✅ **Allow force pushes**（如果需要强制推送）
   - ✅ **Allow deletions**（如果需要删除分支）
5. 点击 **"Save changes"** 保存更改

**优点**：
- 保留规则配置，推送后容易恢复
- 不需要重新创建规则

### 方法2：删除规则（临时，完全移除）

**步骤**：
1. 找到要删除的保护规则
2. 点击规则右侧的 **"Delete"** 按钮
3. 在确认对话框中点击 **"Delete rule"**
4. **重要**：推送完成后，记得重新创建规则

**优点**：
- 完全移除限制，确保推送成功
- 适合紧急情况

**缺点**：
- 需要重新配置规则
- 可能忘记重新启用保护

## 🔒 重新启用分支保护（推送后）

### 步骤
1. 在分支设置页面，点击 **"Add rule"** 按钮
2. **配置规则**：
   - **Branch name pattern**: 输入分支名称（如 `main`）
   - **勾选需要的保护选项**：
     - ✅ Require a pull request before merging
     - ✅ Require approvals（设置审批数量）
     - ✅ Require status checks to pass before merging
     - ✅ Restrict who can push to matching branches
     - ✅ Do not allow bypassing the above settings
3. 点击 **"Create"** 创建规则

### 推荐配置（平衡安全性和便利性）

```yaml
分支名称: main
保护选项:
  - Require a pull request before merging: ✅
  - Require approvals: ✅ (1个审批)
  - Require status checks: ❌ (如果不需要CI)
  - Restrict who can push: ❌ (允许所有协作者)
  - Do not allow bypassing: ❌ (允许管理员绕过)
  - Allow force pushes: ❌ (禁止强制推送)
  - Allow deletions: ❌ (禁止删除分支)
```

## ⚠️ 关键设置说明

### 1. "Require a pull request before merging"
- **启用**：所有更改必须通过PR合并，不能直接推送
- **禁用**：允许直接推送到受保护分支
- **影响**：这是最常见的推送阻止原因

### 2. "Require approvals"
- **启用**：PR需要指定数量的审批才能合并
- **设置**：可以设置审批数量（通常1-2个）
- **影响**：即使允许PR，也需要审批才能合并

### 3. "Restrict who can push to matching branches"
- **启用**：只有指定用户/团队可以推送
- **禁用**：所有有写权限的用户都可以推送
- **影响**：如果启用且未包含你的账户，会被阻止

### 4. "Do not allow bypassing the above settings"
- **启用**：即使是管理员也无法绕过保护规则
- **禁用**：管理员可以绕过规则直接推送
- **影响**：如果启用，管理员也需要遵守规则

### 5. "Allow force pushes"
- **启用**：允许 `git push --force`
- **禁用**：禁止强制推送
- **影响**：强制推送会覆盖远程历史，通常应该禁用

### 6. "Allow deletions"
- **启用**：允许删除受保护分支
- **禁用**：禁止删除分支
- **影响**：防止误删除重要分支

## 🎯 针对当前推送问题的解决方案

### 方案A：临时禁用保护（最快）

**适用场景**：需要立即推送，且推送后可以重新启用保护

**步骤**：
1. 访问：https://github.com/ZhuTechLLC/TRQuantExt/settings/branches
2. 找到 `main` 分支的保护规则
3. 点击 **"Edit"**
4. **取消勾选所有限制选项**
5. 点击 **"Save changes"**
6. **执行推送**：
   ```bash
   git push origin main-clean
   ```
7. **推送完成后，重新启用保护**

### 方案B：推送到不受保护的分支（推荐）

**适用场景**：不想修改main分支保护规则

**步骤**：
1. **创建新分支**（如果还没有）：
   ```bash
   git checkout -b main-clean
   ```
2. **确认新分支不受保护**（在分支设置页面检查）
3. **推送到新分支**：
   ```bash
   git push origin main-clean
   ```
4. **通过PR合并到main**（如果需要）

### 方案C：使用管理员权限绕过（如果可用）

**适用场景**：你是仓库管理员，且规则允许绕过

**前提条件**：
- 你是仓库管理员
- "Do not allow bypassing" 选项未启用

**步骤**：
1. 确认管理员权限
2. 直接推送（管理员可以绕过某些规则）

## 📋 操作检查清单

### 推送前检查
- [ ] 已访问分支设置页面
- [ ] 已查看当前分支保护规则
- [ ] 已确认Token有完整repo权限
- [ ] 已确认是仓库管理员或有推送权限
- [ ] 已决定使用哪种方案（禁用保护/新分支/绕过）

### 推送操作
- [ ] 已调整分支保护规则（如需要）
- [ ] 已执行推送命令
- [ ] 已确认推送成功

### 推送后恢复
- [ ] 已重新启用分支保护规则（如果临时禁用了）
- [ ] 已验证代码已成功推送
- [ ] 已检查分支历史记录
- [ ] 已通知团队成员（如果修改了保护规则）

## 🔗 相关链接

- **GitHub官方文档**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- **管理分支保护规则**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule
- **仓库分支设置**: https://github.com/ZhuTechLLC/TRQuantExt/settings/branches
- **Token权限设置**: https://github.com/settings/tokens

## 💡 最佳实践建议

1. **不要永久禁用分支保护**
   - 保护规则有助于代码质量
   - 推送后立即恢复

2. **使用新分支进行实验性推送**
   - 创建临时分支进行推送
   - 通过PR合并到main

3. **定期审查保护规则**
   - 确保规则符合团队需求
   - 避免过度限制影响开发效率

4. **文档化保护规则**
   - 记录为什么设置某个规则
   - 帮助团队成员理解规则目的

## 🚨 常见错误和解决方案

### 错误1：找不到"Edit"按钮
**原因**：没有管理员权限  
**解决**：联系仓库管理员

### 错误2：保存后仍然无法推送
**原因**：可能有多个规则匹配，或缓存问题  
**解决**：
- 检查是否有其他规则匹配
- 等待几分钟让更改生效
- 刷新页面重试

### 错误3：忘记重新启用保护
**原因**：推送后忘记恢复  
**解决**：
- 设置提醒
- 在推送脚本中添加恢复步骤
- 使用GitHub Actions自动恢复

## 📝 操作记录模板

```markdown
## 分支保护规则调整记录

**日期**: 2024-12-14
**操作人**: [你的名字]
**原因**: 需要推送清理后的Git历史

**操作前状态**:
- 规则名称: main
- 保护选项: [列出启用的选项]

**操作**:
- [ ] 临时禁用保护
- [ ] 推送到新分支
- [ ] 其他: ___________

**操作后状态**:
- 规则名称: main
- 保护选项: [列出当前选项]

**恢复时间**: [推送完成后的时间]
**恢复人**: [你的名字]
```

