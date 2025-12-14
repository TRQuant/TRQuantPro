# 轩辕剑灵自动备份功能指南

## 概述

轩辕剑灵（AI助手）现在具备自动备份功能，可以在执行可能丢失数据的操作前自动创建备份，保护你的工作成果。

## 自动备份触发条件

### 1. 危险操作前自动备份

以下操作会自动触发备份：

- **Git操作**：
  - `git restore` - 恢复文件
  - `git reset` - 重置提交
  - `git clean` - 清理未跟踪文件
  - `git checkout` - 切换分支（可能丢失未提交更改）

- **文件操作**：
  - 批量删除文件
  - 清空目录
  - 移动或重命名大量文件

- **代码重构**：
  - 大规模代码重构
  - 修改多个文件的架构
  - 删除重要模块或功能

### 2. 定期备份提醒

- 每天工作结束时，AI会提醒创建备份
- 重要功能开发完成后，建议创建备份
- 重大版本发布前，建议创建完整备份

### 3. 用户请求时

当你说：
- "备份"
- "创建备份"
- "保存当前状态"
- "备份一下"

AI会自动执行备份。

## 备份策略

### Essential Files备份（默认）

**使用场景**：
- 日常开发中的自动备份
- 快速备份当前工作状态
- 代码和配置的轻量级备份

**包含内容**：
- 所有源代码文件（`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.mjs`, `.astro`等）
- 配置文件（`package.json`, `requirements.txt`, `*.yml`, `*.yaml`, `*.toml`等）
- 文档文件（`*.md`, `*.txt`）
- 脚本文件（`*.sh`, `*.ps1`, `*.bat`）

**排除内容**：
- `node_modules/` - Node.js依赖
- `venv/`, `.venv/` - Python虚拟环境
- `.taorui/` - 知识库索引
- `*.vsix` - VS Code扩展包
- `*.sqlite3` - 数据库文件
- `dist/`, `build/` - 构建产物
- `logs/`, `*.log` - 日志文件
- `data/`, `*.csv`, `*.xlsx` - 数据文件

### 完整备份

**使用场景**：
- 重大版本发布前
- 系统架构重大变更前
- 用户明确要求完整备份时

**包含内容**：
- 所有文件（排除`.git`、`__pycache__`等明显不需要的）

## 备份执行流程

### 自动备份流程

1. **检测危险操作**
   ```
   AI识别：用户要执行 git restore
   → 检测到可能丢失数据的操作
   ```

2. **自动创建备份**
   ```
   AI执行：调用 backup_essential 工具
   → 显示：正在创建 Essential Files 备份...
   → 显示：备份进度和统计信息
   ```

3. **确认备份完成**
   ```
   AI显示：备份完成
   → 备份文件：/mnt/data/backups/TRQuant/TRQuant_essential_20251213_170000.tar.gz
   → 文件数：1234 复制, 567 跳过
   → 归档大小：11.78 MB
   ```

4. **执行用户请求**
   ```
   AI执行：确认备份完成后，执行 git restore
   → 安全执行用户请求的操作
   ```

### 手动备份流程

1. **用户请求备份**
   ```
   用户：请创建备份
   ```

2. **AI询问备份类型**
   ```
   AI：要创建哪种备份？
   - Essential Files备份（推荐，快速）
   - 完整备份（包含所有文件）
   ```

3. **执行备份**
   ```
   AI执行：调用相应的备份工具
   → 显示备份结果
   ```

## 备份位置

所有备份存储在：
```
/mnt/data/backups/TRQuant/
```

备份文件命名：
- Essential备份：`TRQuant_essential_YYYYMMDD_HHMMSS.tar.gz`
- 完整备份：`TRQuant_full_YYYYMMDD_HHMMSS.tar.gz`

## 备份管理

### 查看所有备份

```
用户：列出所有备份
AI执行：调用 list_backups 工具
AI显示：
  - 备份名称
  - 创建时间
  - 文件大小
  - 备份类型
```

### 删除旧备份

```
用户：删除7天前的备份
AI执行：
  1. 调用 list_backups 获取所有备份
  2. 筛选7天前的备份
  3. 调用 delete_backup 删除
  4. 显示删除结果
```

### 恢复备份

```
用户：从备份恢复文件
AI指导：
  1. 列出可用备份
  2. 选择要恢复的备份
  3. 提供恢复命令：
     cd /path/to/restore
     tar -xzf /mnt/data/backups/TRQuant/TRQuant_essential_YYYYMMDD_HHMMSS.tar.gz
```

## 使用示例

### 示例1：Git操作前自动备份

```
用户：git restore extension/AShare-manual/src/pages/index.astro

AI响应：
⚠️ 检测到 git restore 操作，可能丢失未提交的更改。
正在创建 Essential Files 备份以保护你的工作...

✅ 备份完成：
   - 备份文件：TRQuant_essential_20251213_170000.tar.gz
   - 文件数：1234 复制
   - 大小：11.78 MB
   - 位置：/mnt/data/backups/TRQuant/

现在安全执行 git restore...
```

### 示例2：用户主动请求备份

```
用户：备份一下

AI响应：
正在创建 Essential Files 备份...

✅ 备份完成：
   - 备份名称：TRQuant_essential_20251213_170000
   - 备份路径：/mnt/data/backups/TRQuant/TRQuant_essential_20251213_170000.tar.gz
   - 文件统计：1234 复制, 567 跳过
   - 归档大小：11.78 MB
   - 时间戳：20251213_170000
```

### 示例3：查看备份列表

```
用户：有哪些备份？

AI响应：
📦 备份列表（共 5 个）：

1. TRQuant_essential_20251213_170000.tar.gz
   - 类型：Essential Files
   - 大小：11.78 MB
   - 创建时间：2025-12-13 17:00:00

2. TRQuant_essential_20251212_180000.tar.gz
   - 类型：Essential Files
   - 大小：11.65 MB
   - 创建时间：2025-12-12 18:00:00

...
```

## 最佳实践

1. **信任自动备份**：
   - AI会在危险操作前自动备份
   - 无需手动干预，专注于开发

2. **定期检查备份**：
   - 每周查看一次备份列表
   - 确保备份正常创建

3. **清理旧备份**：
   - 保留最近30天的备份
   - 定期清理更早的备份以节省空间

4. **重要节点手动完整备份**：
   - 重大版本发布前
   - 系统架构变更前
   - 明确要求AI创建完整备份

## 故障排除

### 备份失败

如果自动备份失败，AI会：
1. 显示错误信息
2. 询问是否继续执行用户请求的操作
3. 提供手动备份的选项

### 备份空间不足

如果data盘空间不足：
1. AI会提醒清理旧备份
2. 提供删除旧备份的命令
3. 建议使用Essential备份而不是完整备份

## 技术细节

- **备份工具**：`trquant-backup` MCP服务器
- **备份格式**：tar.gz（gzip压缩）
- **备份方式**：文件系统复制 + tar归档
- **并发安全**：支持多个备份同时进行

## 相关文档

- [备份服务器使用指南](./BACKUP_SERVER_GUIDE.md)
- [MCP服务器配置](../.cursor/mcp.json)

