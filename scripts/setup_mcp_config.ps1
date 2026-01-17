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
