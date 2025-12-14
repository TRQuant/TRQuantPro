# GitHub认证问题调研报告

> **调研时间**: 2024-12-13  
> **调研人**: 轩辕剑灵

## 🔍 问题诊断

### 当前状态
- **错误信息**: `permission denied` 推送被拒绝
- **Token权限检查结果**:
  ```json
  {
    "admin": false,
    "maintain": false,
    "push": false,  // ❌ 没有推送权限
    "triage": false,
    "pull": true     // ✅ 只有读取权限
  }
  ```
- **仓库信息**:
  - 所有者: `ZhuTechLLC`
  - 仓库: `TRQuantExt`
  - 类型: 公开仓库

### 问题根源

根据GitHub官方文档和调研，问题可能由以下原因导致：

1. **Token权限不足**（最可能）
   - 当前token只有 `pull` 权限
   - 缺少 `push` 权限
   - 缺少 `admin` 权限（强制推送需要）

2. **分支保护规则**
   - main分支可能启用了保护规则
   - 阻止直接推送或强制推送
   - 需要管理员权限或PR审核

3. **Token权限范围设置错误**
   - 生成token时可能只选择了部分权限
   - `repo` 权限需要完整勾选（包括所有子权限）

## 💡 解决方案

### 方案1：重新生成Token（推荐）

**步骤**：

1. **访问Token设置页面**
   - https://github.com/settings/tokens
   - 或：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **生成新Token**
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 设置名称：`TRQuant Full Access`
   - **重要：勾选完整权限**
     - ✅ `repo` (完整仓库访问权限)
       - ✅ `repo:status`
       - ✅ `repo_deployment`
       - ✅ `public_repo`
       - ✅ `repo:invite`
       - ✅ `security_events`
     - ✅ `admin:repo_hook` (如果需要管理webhooks)
   - 设置过期时间（建议：90天或更长）
   - 点击 "Generate token"
   - **立即复制token**（只显示一次）

3. **使用新Token推送**
   ```bash
   git remote set-url origin https://<NEW_TOKEN>@github.com/ZhuTechLLC/TRQuantExt.git
   git push origin main-clean
   ```

### 方案2：检查并调整分支保护规则

**步骤**：

1. **访问仓库设置**
   - https://github.com/ZhuTechLLC/TRQuantExt/settings/branches

2. **检查main分支保护规则**
   - 查看是否有 "Require pull request reviews"
   - 查看是否有 "Restrict who can push to matching branches"
   - 查看是否有 "Do not allow bypassing the above settings"

3. **暂时禁用保护（推送后重新启用）**
   - 取消勾选保护规则
   - 执行推送
   - 推送完成后重新启用保护

### 方案3：使用SSH密钥（最安全，推荐长期使用）

**步骤**：

1. **生成SSH密钥**
   ```bash
   ssh-keygen -t ed25519 -C "zhutechllc@gmail.com"
   # 按Enter使用默认路径
   # 设置密码（可选，但推荐）
   ```

2. **复制公钥**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **添加到GitHub**
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - 标题：`TRQuant Development`
   - 粘贴公钥内容
   - 点击 "Add SSH key"

4. **测试SSH连接**
   ```bash
   ssh -T git@github.com
   ```

5. **使用SSH URL**
   ```bash
   git remote set-url origin git@github.com:ZhuTechLLC/TRQuantExt.git
   git push origin main-clean
   ```

### 方案4：使用GitHub CLI（gh）

**步骤**：

1. **安装GitHub CLI**
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # 或使用snap
   sudo snap install gh
   ```

2. **登录**
   ```bash
   gh auth login
   # 选择：GitHub.com
   # 选择：HTTPS
   # 选择：Login with a web browser
   ```

3. **推送**
   ```bash
   git push origin main-clean
   ```

## 🎯 推荐方案

### 短期解决（立即）
1. **重新生成Token**，确保勾选完整的 `repo` 权限
2. **检查分支保护规则**，必要时暂时禁用
3. **使用新Token推送**

### 长期方案（推荐）
1. **配置SSH密钥**（最安全，无需token）
2. **或使用GitHub CLI**（更便捷）

## ⚠️ 注意事项

1. **Token安全**
   - Token一旦泄露，立即撤销
   - 不要在代码中硬编码token
   - 使用环境变量或凭据管理器

2. **分支保护**
   - 推送完成后，记得重新启用分支保护
   - 保护规则有助于代码质量

3. **权限最小化**
   - 只授予必要的权限
   - 定期审查和更新token

## 📋 快速检查清单

- [ ] Token有完整的 `repo` 权限
- [ ] 分支保护规则已检查/调整
- [ ] 使用正确的用户名（ZhuTechLLC）
- [ ] Token未过期
- [ ] 仓库存在且可访问

## 🔗 相关链接

- [GitHub Token设置](https://github.com/settings/tokens)
- [分支保护规则](https://github.com/ZhuTechLLC/TRQuantExt/settings/branches)
- [SSH密钥管理](https://github.com/settings/keys)
- [GitHub CLI文档](https://cli.github.com/)

