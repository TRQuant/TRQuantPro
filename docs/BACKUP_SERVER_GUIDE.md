# TRQuant 备份服务器使用指南

## 概述

TRQuant备份服务器是一个MCP (Model Context Protocol) 服务器，用于将项目文件备份到data盘（`/mnt/data/backups/TRQuant`）。

## 功能特性

### 1. 全部备份 (`backup_full`)
- 备份所有文件（排除 `.git`、`__pycache__` 等明显不需要的）
- 适合完整项目备份
- 包含所有依赖和构建产物

### 2. Essential Files备份 (`backup_essential`)
- 只备份源代码和配置文件
- 排除可重新构建的文件：
  - `node_modules/` - Node.js依赖
  - `venv/`, `.venv/` - Python虚拟环境
  - `.taorui/` - 知识库索引
  - `*.vsix` - VS Code扩展包
  - `*.sqlite3` - 数据库文件
  - `dist/`, `build/` - 构建产物
  - `logs/`, `*.log` - 日志文件
  - `data/`, `*.csv`, `*.xlsx` - 数据文件
  - `backtest_results/` - 回测结果
- 适合代码和配置的轻量级备份

## 使用方法

### 通过MCP客户端调用

备份服务器已注册到MCP配置中，可以通过Cursor或其他MCP客户端调用。

#### 1. 创建全部备份

```json
{
  "tool": "backup_full",
  "arguments": {
    "source_dir": "/home/taotao/dev/QuantTest/TRQuant"
  }
}
```

#### 2. 创建Essential Files备份

```json
{
  "tool": "backup_essential",
  "arguments": {
    "source_dir": "/home/taotao/dev/QuantTest/TRQuant"
  }
}
```

#### 3. 列出所有备份

```json
{
  "tool": "list_backups",
  "arguments": {}
}
```

#### 4. 删除备份

```json
{
  "tool": "delete_backup",
  "arguments": {
    "backup_name": "TRQuant_essential_20251213_170000"
  }
}
```

### 直接运行服务器

```bash
# 使用项目venv
extension/venv/bin/python mcp_servers/backup_server.py

# 或使用系统Python（需要安装mcp包）
python3 mcp_servers/backup_server.py
```

## 备份位置

所有备份存储在：
```
/mnt/data/backups/TRQuant/
```

备份文件命名格式：
- 全部备份：`TRQuant_full_YYYYMMDD_HHMMSS.tar.gz`
- Essential备份：`TRQuant_essential_YYYYMMDD_HHMMSS.tar.gz`

## 备份内容说明

### Essential Files备份包含

- **源代码文件**：
  - `*.py`, `*.js`, `*.ts`, `*.tsx`, `*.jsx`
  - `*.mjs`, `*.astro`, `*.css`, `*.html`
  
- **配置文件**：
  - `package.json`, `package-lock.json`
  - `requirements.txt`, `pyproject.toml`
  - `tsconfig.json`, `astro.config.mjs`
  - `*.yml`, `*.yaml`, `*.toml`, `*.ini`, `*.cfg`
  
- **文档文件**：
  - `*.md`, `*.txt`
  - `README*`, `LICENSE*`, `CHANGELOG*`
  
- **脚本文件**：
  - `*.sh`, `*.ps1`, `*.bat`

### Essential Files备份排除

- **依赖目录**：`node_modules/`, `venv/`, `.venv/`, `env/`
- **构建产物**：`dist/`, `build/`, `.next/`, `.nuxt/`, `.cache/`
- **大文件**：`.taorui/`, `*.vsix`, `*.sqlite3`, `*.db`
- **日志和临时文件**：`logs/`, `*.log`, `*.tmp`, `*.temp`
- **数据文件**：`data/`, `*.csv`, `*.xlsx`, `*.pkl`
- **回测结果**：`backtest_results/`, `results/`
- **Git相关**：`.git/`, `.gitignore`

## 备份统计信息

每次备份完成后会返回统计信息：

```json
{
  "success": true,
  "result": {
    "backup_name": "TRQuant_essential_20251213_170000",
    "backup_type": "essential",
    "backup_path": "/mnt/data/backups/TRQuant/TRQuant_essential_20251213_170000.tar.gz",
    "files_copied": 1234,
    "files_skipped": 567,
    "total_size_bytes": 45678901,
    "archive_size_bytes": 12345678,
    "archive_size_mb": 11.78,
    "timestamp": "20251213_170000",
    "source_dir": "/home/taotao/dev/QuantTest/TRQuant"
  }
}
```

## 恢复备份

### 解压备份文件

```bash
# 解压到指定目录
cd /path/to/restore
tar -xzf /mnt/data/backups/TRQuant/TRQuant_essential_20251213_170000.tar.gz

# 解压后的目录结构
TRQuant_essential_20251213_170000/
  ├── mcp_servers/
  ├── extension/
  ├── core/
  └── ...
```

## 最佳实践

1. **定期备份**：建议每天或每次重要更改后创建essential备份
2. **版本管理**：保留最近7-30天的备份，定期清理旧备份
3. **空间管理**：data盘有3.6TB空间，但建议定期清理旧备份
4. **备份验证**：定期验证备份文件的完整性

## 故障排除

### 备份失败

- 检查data盘是否挂载：`df -h | grep /mnt/data`
- 检查备份目录权限：`ls -ld /mnt/data/backups/TRQuant`
- 查看日志输出获取详细错误信息

### 备份文件过大

- 使用essential备份而不是full备份
- 检查是否有意外包含的大文件
- 清理不必要的备份文件

## 技术细节

- **压缩格式**：tar.gz (gzip压缩)
- **备份方式**：文件系统复制 + tar归档
- **并发安全**：支持多个备份同时进行（使用时间戳区分）
- **错误处理**：单个文件失败不影响整体备份

## 相关文件

- 服务器脚本：`mcp_servers/backup_server.py`
- MCP配置：`.cursor/mcp.json`
- 备份目录：`/mnt/data/backups/TRQuant/`

