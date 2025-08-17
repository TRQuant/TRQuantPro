# QuantConnect Research 本地环境设置指南

**更新时间**: 2025-08-17 13:46:55 EDT  
**版本**: 1.0  
**状态**: ✅ 已验证

## 概述

本指南提供在本地环境中设置 QuantConnect Research 的完整流程，使用 Docker 容器和 VS Code/Cursor 进行量化研究。

## A. 一次性准备

### 1. 安装 Lean CLI

```bash
# 安装 pipx（推荐）
python3 -m pip install --user pipx && pipx ensurepath

# 安装 lean CLI
pipx install lean

# 验证安装
lean --version
```

### 2. 登录 QuantConnect

```bash
# 全局一次性登录
lean login
```

## B. 创建工作区 & 初始化

```bash
# 创建工作目录
mkdir -p ~/dev/QuantTest && cd ~/dev/QuantTest

# 初始化 Lean 环境
lean init   # 生成 lean.json、data/ 等文件
```

**验证**: 检查 `lean.json` 文件是否存在，确认 `data-folder` 设置为 `"data"`

## C. 启动本地 Research 环境

```bash
# 清理可能存在的旧容器
docker ps --filter "ancestor=quantconnect/research" -q | xargs -r docker rm -f

# 启动 Research 容器
lean research . --port 8888
```

**重要**: 记下 Jupyter 服务器地址 `http://127.0.0.1:8888`（无需 token）

## D. 配置 VS Code/Cursor 连接

1. **打开命令面板**: `Ctrl/Cmd + Shift + P`
2. **选择 Jupyter 服务器**: 
   - 输入 `Jupyter: Specify Jupyter Server for connections`
   - 选择 `Existing`
   - 粘贴 `http://127.0.0.1:8888`
3. **选择内核**: 在可用内核列表中选择 `Python 3 (ipykernel)`

**验证**: 运行 `import sys; print(sys.executable)` 应显示 `/opt/miniconda3/bin/python`

## E. 笔记本标准配置

每个新的 Jupyter 笔记本都应在第一个单元格包含以下配置：

```python
# 标准配置 - 每个笔记本首格必备
from QuantConnect.Configuration import Config
Config.Set("data-folder", "/Lean/Data")   # 指向容器挂载点
Config.Set("log-level", "ERROR")          # 可选：安静日志
```

## F. 最小验证测试

```python
# 验证 QuantConnect Research 功能
from QuantConnect.Research import QuantBook
from QuantConnect import Resolution

qb = QuantBook()
s = qb.AddEquity("SPY").Symbol
hist = qb.History([s], 5, Resolution.Daily)
print(hist.head())
```

## G. 数据管理

### 数据挂载机制

- **主机目录**: `~/dev/QuantTest/data`
- **容器内路径**: `/Lean/Data`
- **自动挂载**: Lean CLI 启动容器时自动将主机 `data/` 挂载到容器内 `/Lean/Data`

### 复制最小数据集

如果主机 `data/` 为空，可以从容器复制基础数据：

```bash
# 获取容器ID
CID=$(docker ps --filter "ancestor=quantconnect/research" -q | head -n1)

# 创建目录结构
mkdir -p ./data/equity/usa/{daily,map_files,factor_files}

# 复制基础文件
docker cp "$CID":/Lean/Data/market-hours              ./data/
docker cp "$CID":/Lean/Data/symbol-properties         ./data/
docker cp "$CID":/Lean/Data/equity/usa/daily/spy.zip  ./data/equity/usa/daily/
docker cp "$CID":/Lean/Data/equity/usa/map_files/spy.csv ./data/equity/usa/map_files/
docker cp "$CID":/Lean/Data/equity/usa/factor_files/spy.csv ./data/equity/usa/factor_files/
```

## H. 常见问题与解决方案

### 1. 笔记本未连接容器内核
**症状**: 运行代码时使用本地 Python 而非容器环境  
**解决**: 重新执行步骤 D，确保选择正确的 Jupyter 服务器

### 2. 数据路径错误
**症状**: 出现 `/Lean/Launcher/bin/Data/...` 路径错误  
**解决**: 
- 确认首格已设置 `Config.Set("data-folder","/Lean/Data")`
- 如有历史笔记本残留，在容器中创建兼容链接：

```bash
CID=$(docker ps --filter "ancestor=quantconnect/research" -q | head -n1)
docker exec -it "$CID" bash -lc 'mkdir -p /Lean/Launcher/bin && ln -sfn /Lean/Data /Lean/Launcher/bin/Data'
```

### 3. 端口占用
**症状**: 启动时提示端口 8888 被占用  
**解决**: 使用其他端口
```bash
lean research . --port 8890
```
然后使用新 URL `http://127.0.0.1:8890` 连接

### 4. 内核连接问题
**症状**: 内核 404 错误或旧会话残留  
**解决**: 
1. VS Code 中运行 `Jupyter: Shut Down All Kernels`
2. 运行 `Jupyter: Clear Jupyter Remote Server List`
3. 重新加载窗口 (`Ctrl/Cmd + Shift + P` → `Developer: Reload Window`)
4. 重新绑定 Jupyter 服务器 URL

### 5. Mono 运行时问题
**症状**: `RuntimeError: Could not find libmono`  
**状态**: 当前版本存在此问题，但不影响 Jupyter 环境使用  
**解决**: 在 Jupyter 环境中直接使用 QuantConnect 模块，避免命令行直接调用

## I. 回测环境使用

```bash
# 在工作区根目录（非 backtests/ 目录）
lean create-project "MyAlgo"   # 首次需要
lean backtest "MyAlgo"         # 不要使用编辑器右上角 ▶️
```

## J. 日常使用流程

**每日启动**:
1. 启动 Docker
2. `cd ~/dev/QuantTest`
3. `lean research . --port 8888`
4. VS Code/Cursor 连接现有 Jupyter 服务器
5. 笔记本首格添加两行配置（data-folder + log-level）
6. 开始研究

## K. 自动化工具集

### Scripts 工具集

工作区包含了一套完整的自动化工具脚本，位于 `Scripts/` 目录：

#### 1. 笔记本生成器 (`create_research_notebook.py`)
```bash
# 创建基础笔记本
python3 Scripts/create_research_notebook.py my_analysis

# 使用特定模板
python3 Scripts/create_research_notebook.py strategy_dev --template strategy
python3 Scripts/create_research_notebook.py backtest_analysis --template backtest
python3 Scripts/create_research_notebook.py data_study --template data_analysis
```

#### 2. 数据下载器 (`data_downloader.py`)
```bash
# 下载单个股票
python3 Scripts/data_downloader.py SPY

# 批量下载
python3 Scripts/data_downloader.py --indices      # 主要指数
python3 Scripts/data_downloader.py --sectors      # 行业ETF
python3 Scripts/data_downloader.py --commodities  # 商品
python3 Scripts/data_downloader.py --crypto       # 加密货币
```

#### 3. 回测分析器 (`backtest_analyzer.py`)
```bash
# 分析回测结果
python3 Scripts/backtest_analyzer.py <backtest_id>
```

#### 4. 笔记本管理器 (`notebook_manager.py`)
```bash
# 批量添加标准配置
python3 Scripts/notebook_manager.py batch-add-config

# 清理笔记本输出
python3 Scripts/notebook_manager.py batch-clean

# 生成笔记本索引
python3 Scripts/notebook_manager.py index
```

#### 5. 自动化设置脚本 (`setup_workspace.sh`)
```bash
# 一键设置新工作区
./Scripts/setup_workspace.sh [workspace_name]
```

详细使用说明请参考：`Scripts/README.md`

## O. Git 版本控制与备份

### 初始化Git仓库

```bash
# 初始化Git仓库（已完成）
git init

# 查看状态
git status

# 查看修改的文件
python3 Scripts/git_manager.py status
```

### 日常Git工作流程

```bash
# 1. 检查修改的文件
python3 Scripts/git_manager.py status

# 2. 自动提交更改
python3 Scripts/git_manager.py auto-commit

# 3. 推送到远程仓库（首次需要设置）
python3 Scripts/git_manager.py setup-remote --remote-url <your-github-repo-url>
python3 Scripts/git_manager.py push

# 4. 从远程仓库拉取更新
python3 Scripts/git_manager.py pull
```

### 备份策略

#### 自动备份
```bash
# 创建完整备份（包括Git分支）
./Scripts/auto_backup.sh [backup_name]

# 备份重要文件
python3 Scripts/git_manager.py backup-files

# 创建Git备份分支
python3 Scripts/git_manager.py backup-branch --message "backup_name"
```

#### 手动备份
```bash
# 查看提交历史
python3 Scripts/git_manager.py show-log --count 20

# 列出所有分支
python3 Scripts/git_manager.py list-branches
```

### 推荐的Git工作流程

1. **每日开始工作前**:
   ```bash
   python3 Scripts/git_manager.py pull  # 拉取最新更改
   ```

2. **工作过程中**:
   ```bash
   python3 Scripts/git_manager.py status  # 检查状态
   python3 Scripts/git_manager.py auto-commit  # 定期提交
   ```

3. **工作结束时**:
   ```bash
   python3 Scripts/git_manager.py auto-commit  # 提交更改
   python3 Scripts/git_manager.py push  # 推送到远程
   ```

4. **定期备份**:
   ```bash
   ./Scripts/auto_backup.sh  # 每周或重要更改后
   ```

### 设置GitHub远程仓库

1. **在GitHub上创建新仓库**
2. **设置远程仓库**:
   ```bash
   python3 Scripts/git_manager.py setup-remote --remote-url https://github.com/yourusername/your-repo.git
   ```
3. **推送初始代码**:
   ```bash
   python3 Scripts/git_manager.py push
   ```

### 恢复策略

#### 从Git恢复
```bash
# 查看提交历史
git log --oneline

# 恢复到特定提交
git checkout <commit-hash>

# 恢复到特定分支
git checkout <branch-name>
```

#### 从备份恢复
```bash
# 解压备份文件
tar -xzf backups/backup_name.tar.gz

# 按照备份报告中的说明恢复文件
```

### 最佳实践

1. **频繁提交**: 每完成一个功能就提交一次
2. **清晰的提交消息**: 使用描述性的提交消息
3. **定期推送**: 至少每天推送一次到远程仓库
4. **定期备份**: 每周或重要更改后创建完整备份
5. **分支管理**: 为重要功能创建独立分支
6. **忽略大文件**: 确保 `.gitignore` 正确配置，避免提交数据文件

## L. 环境验证清单

- [ ] Lean CLI 已安装 (`lean --version`)
- [ ] 已登录 QuantConnect (`lean login`)
- [ ] 工作区已初始化 (`lean init`)
- [ ] Research 容器正在运行 (`docker ps`)
- [ ] Jupyter 服务器可访问 (`http://127.0.0.1:8888`)
- [ ] VS Code 已连接容器内核
- [ ] 数据文件夹存在且包含 SPY 数据
- [ ] 笔记本首格配置正确
- [ ] 最小验证测试通过

## M. 技术规格

- **Lean CLI 版本**: 1.0.220
- **Docker 镜像**: quantconnect/research
- **Python 版本**: 3.11.13 (容器内)
- **Jupyter 版本**: 4.4.3
- **数据格式**: ZIP 压缩的 CSV 文件
- **支持资产类型**: 股票、期货、期权、加密货币、外汇等

## N. 故障排除

如遇到未列出的问题：

1. 检查 Docker 容器日志: `docker logs <container_id>`
2. 重启 Research 环境: `lean research . --port 8888`
3. 清理并重新初始化: `rm -rf data/ && lean init`
4. 查看 QuantConnect 官方文档: https://www.quantconnect.com/docs/v2/lean-cli

---

**注意**: 本环境仅用于研究和回测，不适用于实盘交易。实盘交易请使用 QuantConnect 云端环境。 