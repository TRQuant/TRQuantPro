# TRQuant MCP服务器 - Windows配置完整指南

> **版本**: v1.0  
> **更新**: 2026-01-16  
> **目的**: Windows系统上配置TRQuant所有MCP服务器的完整指南  
> **Windows路径**: `C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope`

---

## 📋 目录

1. [前置条件](#前置条件)
2. [MCP配置文件位置](#mcp配置文件位置)
3. [核心MCP服务器配置](#核心mcp服务器配置)
4. [完整配置示例](#完整配置示例)
5. [验证配置](#验证配置)
6. [常见问题](#常见问题)
7. [服务器列表](#服务器列表)

---

## ✅ 前置条件

### 1. 确保MCP服务器文件已同步

通过Git同步后，MCP服务器文件应该位于：
```
C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\mcp_servers\
```

验证文件是否存在：
```powershell
# 检查MCP服务器目录
Test-Path "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\mcp_servers"

# 列出主要服务器文件
Get-ChildItem "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\mcp_servers\*.py" | Select-Object Name
```

### 2. 确保Python环境已配置

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 验证Python版本（应该是3.12）
python --version

# 验证MCP SDK已安装
python -c "import mcp; print('✅ MCP SDK已安装')"
```

如果MCP SDK未安装：
```powershell
pip install mcp
```

### 3. 确保依赖已安装

```powershell
# 安装所有依赖
pip install -r requirements.txt
```

---

## 📁 MCP配置文件位置

### Windows配置文件路径

MCP配置文件位于：
```
%APPDATA%\Cursor\mcp.json
```

完整路径通常是：
```
C:\Users\Administrator\AppData\Roaming\Cursor\mcp.json
```

### 创建配置文件

如果配置文件不存在，需要手动创建：

```powershell
# 方法1: 使用PowerShell创建
$mcpConfigPath = "$env:APPDATA\Cursor\mcp.json"
$mcpConfigDir = Split-Path $mcpConfigPath -Parent

# 确保目录存在
if (-not (Test-Path $mcpConfigDir)) {
    New-Item -ItemType Directory -Path $mcpConfigDir -Force
}

# 创建空配置文件
if (-not (Test-Path $mcpConfigPath)) {
    @{
        mcpServers = @{}
    } | ConvertTo-Json -Depth 10 | Set-Content $mcpConfigPath -Encoding UTF8
    Write-Host "✅ MCP配置文件已创建: $mcpConfigPath"
}
```

### 验证配置文件

```powershell
# 检查配置文件是否存在
Test-Path "$env:APPDATA\Cursor\mcp.json"

# 查看配置文件内容
Get-Content "$env:APPDATA\Cursor\mcp.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 🔧 核心MCP服务器配置

### 1. TRQuant核心业务服务器 (trquant_core_server.py)

**功能**: 整合所有核心业务功能（数据源、市场分析、因子、策略、回测、优化）

**配置**:
```json
{
  "mcpServers": {
    "trquant-core": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\trquant_core_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "📊 TRQuant核心业务服务器（数据源、市场、因子、策略、回测、优化）"
    }
  }
}
```

**工具前缀**: `trquant-core.*` (如 `trquant-core.data.*`, `trquant-core.market.*`)

### 2. 统一开发工具服务器 (unified_dev_server.py)

**功能**: 开发流程管理（任务、日志、里程碑、问题追踪、经验管理、进度报告）

**配置**:
```json
{
  "mcpServers": {
    "trquant-dev": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\unified_dev_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🛠️ TRQuant统一开发工具服务器（任务管理、开发日志、进度跟踪）"
    }
  }
}
```

**工具前缀**: `trquant-dev.*` (如 `trquant-dev.task.*`, `trquant-dev.devlog.*`)

### 3. 工作流服务器 (workflow_9steps_server.py)

**功能**: 9步骤投资工作流执行

**配置**:
```json
{
  "mcpServers": {
    "trquant-workflow": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\workflow_9steps_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🔄 TRQuant 9步骤投资工作流服务器"
    }
  }
}
```

**工具前缀**: `workflow9.*`

### 4. 知识库服务器 (kb_server.py / knowledge_vector_index.py)

**功能**: 知识库搜索和向量索引管理

**配置**:
```json
{
  "mcpServers": {
    "trquant-kb": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\kb_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "📚 TRQuant知识库服务器（RAG搜索、向量索引）"
    }
  }
}
```

**工具前缀**: `kb.*`

### 5. 轩辕剑灵服务器 (xuanyuan_server.py)

**功能**: 提示词管理、错误处理、命令助手、记忆功能

**配置**:
```json
{
  "mcpServers": {
    "xuanyuan": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\xuanyuan_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🐉 轩辕剑灵开发助手（提示词管理、错误处理、命令助手）"
    }
  }
}
```

**工具前缀**: `xuanyuan.*`

### 6. 回测服务器 (backtest_server_v2.py)

**功能**: 策略回测执行和分析

**配置**:
```json
{
  "mcpServers": {
    "trquant-backtest": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\backtest_server_v2.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "⚡ TRQuant回测服务器"
    }
  }
}
```

**工具前缀**: `backtest.*`

---

## 📝 完整配置示例

### 完整mcp.json配置

将以下内容保存到 `%APPDATA%\Cursor\mcp.json`:

```json
{
  "mcpServers": {
    "trquant-core": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\trquant_core_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "📊 TRQuant核心业务服务器"
    },
    "trquant-dev": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\unified_dev_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🛠️ TRQuant统一开发工具服务器"
    },
    "trquant-workflow": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\workflow_9steps_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🔄 TRQuant 9步骤投资工作流服务器"
    },
    "trquant-kb": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\kb_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "📚 TRQuant知识库服务器"
    },
    "xuanyuan": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\xuanyuan_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "🐉 轩辕剑灵开发助手"
    },
    "trquant-backtest": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\backtest_server_v2.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      },
      "description": "⚡ TRQuant回测服务器"
    }
  }
}
```

### 使用PowerShell脚本创建配置

创建脚本 `scripts/setup_mcp_config.ps1`:

```powershell
# TRQuant MCP服务器配置脚本 (Windows)
# 用途: 自动创建或更新MCP配置文件

$projectRoot = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
$pythonPath = "$projectRoot\venv\Scripts\python.exe"
$mcpConfigPath = "$env:APPDATA\Cursor\mcp.json"
$mcpConfigDir = Split-Path $mcpConfigPath -Parent

# 确保目录存在
if (-not (Test-Path $mcpConfigDir)) {
    New-Item -ItemType Directory -Path $mcpConfigDir -Force | Out-Null
    Write-Host "✅ 创建MCP配置目录: $mcpConfigDir"
}

# 读取现有配置（如果存在）
$existingConfig = @{}
if (Test-Path $mcpConfigPath) {
    try {
        $existingConfig = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
        if ($existingConfig.mcpServers) {
            $existingConfig = $existingConfig.mcpServers
        }
    } catch {
        Write-Host "⚠️ 现有配置文件格式错误，将创建新配置"
    }
}

# TRQuant MCP服务器配置
$trquantServers = @{
    "trquant-core" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\trquant_core_server.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "📊 TRQuant核心业务服务器"
    }
    "trquant-dev" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\unified_dev_server.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "🛠️ TRQuant统一开发工具服务器"
    }
    "trquant-workflow" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\workflow_9steps_server.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "🔄 TRQuant 9步骤投资工作流服务器"
    }
    "trquant-kb" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\kb_server.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "📚 TRQuant知识库服务器"
    }
    "xuanyuan" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\xuanyuan_server.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "🐉 轩辕剑灵开发助手"
    }
    "trquant-backtest" = @{
        command = $pythonPath
        args = @(
            "$projectRoot\mcp_servers\backtest_server_v2.py"
        )
        env = @{
            PYTHONIOENCODING = "utf-8"
            TRQUANT_ROOT = $projectRoot
        }
        description = "⚡ TRQuant回测服务器"
    }
}

# 合并配置（保留现有非TRQuant服务器）
$mergedConfig = @{}
foreach ($key in $existingConfig.PSObject.Properties.Name) {
    if (-not $key.StartsWith("trquant-") -and $key -ne "xuanyuan") {
        $mergedConfig[$key] = $existingConfig.$key
    }
}

# 添加TRQuant服务器
foreach ($key in $trquantServers.Keys) {
    $mergedConfig[$key] = $trquantServers[$key]
}

# 保存配置
$finalConfig = @{
    mcpServers = $mergedConfig
}

$finalConfig | ConvertTo-Json -Depth 10 | Set-Content $mcpConfigPath -Encoding UTF8

Write-Host "✅ MCP配置文件已更新: $mcpConfigPath"
Write-Host "📋 已配置的TRQuant服务器:"
foreach ($key in $trquantServers.Keys) {
    Write-Host "   - $key"
}
Write-Host ""
Write-Host "⚠️ 请重启Cursor以使配置生效"
```

运行脚本：
```powershell
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
.\scripts\setup_mcp_config.ps1
```

---

## ✅ 验证配置

### 1. 验证配置文件格式

```powershell
# 检查JSON格式
$config = Get-Content "$env:APPDATA\Cursor\mcp.json" -Raw | ConvertFrom-Json
$config | ConvertTo-Json -Depth 10
```

### 2. 测试服务器启动

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 测试核心服务器（应该等待stdio输入，不报错）
python mcp_servers\trquant_core_server.py

# 按Ctrl+C退出
```

### 3. 重启Cursor并验证

1. **完全关闭Cursor**
   - 确保所有Cursor窗口都已关闭
   - 检查任务管理器，确保没有Cursor进程

2. **重新打开Cursor**
   - 打开Cursor
   - 打开项目目录

3. **检查MCP服务器状态**
   - 按 `Ctrl+,` 打开设置
   - 搜索 "MCP" 或 "Model Context Protocol"
   - 查看 "MCP Servers" 配置项
   - 应该看到所有配置的服务器

4. **在Cursor Chat中测试**
   ```
   请列出所有可用的MCP工具
   ```

---

## 🔍 常见问题

### 问题1: 配置文件路径错误

**错误**: `找不到文件或路径`

**解决方案**:
```powershell
# 检查Python路径
Test-Path "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\venv\Scripts\python.exe"

# 检查MCP服务器文件路径
Test-Path "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope\mcp_servers\trquant_core_server.py"

# 如果路径不同，请修改配置文件中的路径
```

### 问题2: Python路径使用反斜杠

**错误**: JSON配置中路径格式错误

**解决方案**:
- 在JSON中，Windows路径需要使用双反斜杠 `\\` 或正斜杠 `/`
- 推荐使用双反斜杠：`C:\\Users\\Administrator\\...`

### 问题3: 服务器无法启动

**错误**: `ModuleNotFoundError` 或 `ImportError`

**解决方案**:
```powershell
# 确保虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 检查MCP SDK是否安装
pip list | findstr mcp

# 如果未安装，安装MCP SDK
pip install mcp

# 检查其他依赖
pip install -r requirements.txt
```

### 问题4: 编码问题

**错误**: `UnicodeDecodeError` 或中文乱码

**解决方案**:
- 确保配置文件中包含 `"PYTHONIOENCODING": "utf-8"`
- 确保配置文件保存为UTF-8编码

### 问题5: Cursor无法识别服务器

**错误**: 重启Cursor后仍看不到MCP服务器

**解决方案**:
1. 检查配置文件路径是否正确：`%APPDATA%\Cursor\mcp.json`
2. 验证JSON格式是否正确（使用 `ConvertFrom-Json` 测试）
3. 查看Cursor日志：
   - 按 `Ctrl+Shift+P`
   - 输入 "Developer: Show Logs"
   - 查看MCP相关错误

### 问题6: 工具调用失败

**错误**: 工具调用时出现错误

**解决方案**:
```powershell
# 测试服务器是否能正常启动
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
.\venv\Scripts\Activate.ps1
python mcp_servers\trquant_core_server.py

# 检查环境变量
$env:TRQUANT_ROOT
$env:PYTHONIOENCODING
```

---

## 📋 服务器列表

### 核心业务服务器

| 服务器 | 文件 | 工具前缀 | 功能 |
|--------|------|----------|------|
| **trquant-core** | `trquant_core_server.py` | `trquant-core.*` | 数据源、市场分析、因子、策略、回测、优化 |
| **trquant-backtest** | `backtest_server_v2.py` | `backtest.*` | 策略回测执行和分析 |

### 开发工具服务器

| 服务器 | 文件 | 工具前缀 | 功能 |
|--------|------|----------|------|
| **trquant-dev** | `unified_dev_server.py` | `trquant-dev.*` | 任务管理、开发日志、进度跟踪 |
| **xuanyuan** | `xuanyuan_server.py` | `xuanyuan.*` | 提示词管理、错误处理、命令助手 |

### 工作流服务器

| 服务器 | 文件 | 工具前缀 | 功能 |
|--------|------|----------|------|
| **trquant-workflow** | `workflow_9steps_server.py` | `workflow9.*` | 9步骤投资工作流执行 |

### 知识库服务器

| 服务器 | 文件 | 工具前缀 | 功能 |
|--------|------|----------|------|
| **trquant-kb** | `kb_server.py` | `kb.*` | 知识库搜索、向量索引管理 |

### 其他可选服务器

| 服务器 | 文件 | 工具前缀 | 功能 |
|--------|------|----------|------|
| **trquant-factor** | `factor_server.py` | `factor.*` | 因子推荐和计算 |
| **trquant-strategy** | `strategy_server.py` | `strategy.*` | 策略开发和管理 |
| **trquant-market** | `market_server_v2.py` | `market.*` | 市场趋势分析 |
| **trquant-data** | `data_source_server_v2.py` | `data.*` | 数据源管理 |

---

## 🚀 快速开始

### 最小配置（推荐）

只配置最核心的3个服务器：

```json
{
  "mcpServers": {
    "trquant-core": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\trquant_core_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      }
    },
    "trquant-dev": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\unified_dev_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      }
    },
    "trquant-kb": {
      "command": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope\\mcp_servers\\kb_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "C:\\Users\\Administrator\\.cursor\\worktrees\\TRQuantPro\\ope"
      }
    }
  }
}
```

---

## 📝 相关文档

- `docs/WINDOWS_INSTALLATION_GUIDE.md` - Windows安装配置指南
- `docs/07_workflow/MCP配置指南.md` - 通用MCP配置指南
- `docs/XUANYUAN_MCP_SETUP.md` - 轩辕剑灵服务器配置

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
