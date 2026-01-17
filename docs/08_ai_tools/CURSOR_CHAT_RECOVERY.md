# Cursor 聊天记录恢复指南

> **创建时间**: 2026-01-13  
> **目的**: 帮助恢复 Cursor 宕机后丢失的聊天记录

---

## 📋 重要说明

### Cursor 聊天记录的存储机制

**Cursor 的聊天记录存储在云端（Anysphere 服务器）**，而不是本地数据库：

- ✅ **云端存储**: 聊天记录会同步到 Cursor 服务器
- ❌ **本地缓存**: 本地只有临时缓存，宕机可能丢失
- 🔄 **自动同步**: Cursor 启动时会自动同步云端记录

---

## 🔍 恢复方法

### 方法1: 等待自动同步（推荐）

**步骤**:

1. **重新启动 Cursor**
   - 完全关闭 Cursor
   - 重新打开 Cursor
   - 等待自动同步（可能需要几分钟）

2. **检查聊天记录**
   - 打开 Cursor Chat 面板
   - 查看是否有历史对话记录
   - 如果有，说明已自动同步

3. **注意事项**
   - 确保网络连接正常
   - 等待几分钟让同步完成
   - 可能需要登录 Cursor 账号

### 方法2: 检查本地缓存（高级）

**位置**: Cursor 可能在本地的临时位置存储缓存

**Linux**:
```bash
# 检查 Cursor 配置目录
ls -la ~/.config/Cursor/
ls -la ~/.cursor/

# 检查项目相关的配置
find ~/.cursor/projects/ -name "*.json" | grep -i chat
```

**Windows**:
```powershell
# 检查 Cursor 配置目录
dir %APPDATA%\Cursor
dir %USERPROFILE%\.cursor
```

**macOS**:
```bash
# 检查 Cursor 配置目录
ls -la ~/Library/Application\ Support/Cursor
ls -la ~/.cursor
```

**注意**: 这些位置通常只存储配置，不存储完整的聊天记录。

### 方法3: 联系 Cursor 支持

如果自动同步没有恢复记录，可以联系 Cursor 支持：

1. **提交问题报告**
   - 访问: https://cursor.com/support
   - 或发送邮件到: support@cursor.com

2. **提供信息**
   - 问题描述: "Cursor 宕机后聊天记录丢失"
   - 时间范围: 丢失记录的日期和时间
   - 账号信息: Cursor 账号（如果需要）

---

## 🛡️ 预防措施

### 1. 定期备份重要对话

**创建聊天记录备份文档**:

```markdown
# 重要对话备份 - YYYY-MM-DD

## 对话主题
[简要描述对话内容]

## 关键信息
- 讨论了什么功能
- 达成了什么决策
- 需要记住的要点

## 相关文件
- [文件路径1]
- [文件路径2]
```

**建议位置**: `docs/07_workflow/chat_history_backup.md`

### 2. 使用知识库存储重要信息

**对于重要的技术决策和方案**:

1. 使用 `knowledge.add` 工具添加到知识库
2. 或创建文档保存在 `docs/` 目录
3. 或更新 `.cursor/rules/` 规则文件

### 3. 使用 Git 提交记录工作进展

**重要的工作成果**:

1. 及时提交代码到 Git
2. 使用清晰的提交信息
3. 定期推送 to 远程仓库

### 4. 使用 `.cursor/plans/` 记录计划

**长期任务和计划**:

1. 使用 Cursor Plan 功能创建计划文件
2. 计划文件会自动保存在 `.cursor/plans/`
3. 已完成计划会自动归档到 `.cursor/archived_plans/`

---

## 📝 当前项目的聊天记录备份

### 现有备份文档

- **`docs/07_workflow/chat_history_backup.md`**: 项目开发聊天记录备份
- **`docs/08_ai_tools/chat_history_backup.md`**: AI工具使用记录

### 建议的备份策略

1. **重要对话立即备份**: 讨论重要功能或决策后，立即创建备份文档
2. **定期汇总**: 每周汇总一次重要对话记录
3. **版本控制**: 备份文档纳入 Git 版本控制

---

## 🔧 技术细节

### Cursor 聊天记录的存储位置

**云端存储**:
- 服务器: Anysphere 服务器
- 账号关联: 与 Cursor 账号绑定
- 同步机制: 自动同步，启动时拉取

**本地缓存** (临时):
- Linux: `~/.config/Cursor/` 或 `~/.cursor/`
- Windows: `%APPDATA%\Cursor` 或 `%USERPROFILE%\.cursor`
- macOS: `~/Library/Application Support/Cursor` 或 `~/.cursor`

**项目相关配置**:
- `.cursor/projects/`: 项目级别的配置（不包含聊天记录）
- `.cursor/plans/`: 计划文件（不包含聊天记录）

### 为什么本地找不到聊天记录？

1. **云端存储**: Cursor 采用云端存储，本地只有临时缓存
2. **安全性**: 云端存储更安全，防止本地文件丢失
3. **同步机制**: 需要网络连接才能访问完整记录
4. **隐私保护**: 聊天记录存储在加密的云端服务器

---

## ❓ 常见问题

### Q1: 聊天记录完全丢失了，还能恢复吗？

**A**: 如果能重新登录 Cursor 账号，通常可以恢复云端记录。如果本地缓存丢失但云端记录还在，重启 Cursor 后会自动同步。

### Q2: 如何确认聊天记录是否在云端？

**A**: 
1. 在其他设备登录同一 Cursor 账号
2. 检查是否有相同的聊天记录
3. 如果有，说明记录在云端

### Q3: 聊天记录会永久保存吗？

**A**: Cursor 通常会在云端保存聊天记录，但具体保留时间取决于 Cursor 的政策。建议对重要对话进行备份。

### Q4: 如何避免聊天记录丢失？

**A**: 
1. 定期备份重要对话
2. 使用知识库存储重要信息
3. 使用 Git 提交记录工作进展
4. 使用 `.cursor/plans/` 记录计划

---

## 📚 相关文档

- **Cursor 故障排除指南**: https://cursor.com/docs/troubleshooting
- **聊天记录备份**: `docs/07_workflow/chat_history_backup.md`
- **知识库使用**: `docs/MUST_READ/05_KNOWLEDGE.md`
- **开发流程**: `docs/MUST_READ/02_DEV_WORKFLOW.md`

---

**最后更新**: 2026-01-13  
**维护**: TRQuant Team
