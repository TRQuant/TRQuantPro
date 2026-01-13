# TRQuant Windows迁移打包脚本 (PowerShell版本)
# 用途: 在Windows上打包TRQuant系统用于迁移
# 作者: TRQuant Team
# 日期: 2026-01-11

Write-Host "🚀 TRQuant Windows迁移打包工具" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# 获取脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# 进入项目根目录
Set-Location $ProjectRoot

# 生成包名
$DateStr = Get-Date -Format "yyyyMMdd_HHmmss"
$PackageName = "TRQuant_Windows_$DateStr.zip"
$PackageDir = "TRQuant_Windows_Package_$DateStr"

Write-Host "📦 项目根目录: $ProjectRoot" -ForegroundColor Yellow
Write-Host "📦 打包目录: $PackageDir" -ForegroundColor Yellow
Write-Host ""

# 创建临时打包目录
New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null
Set-Location $PackageDir

# 创建目录结构
Write-Host "📁 创建目录结构..." -ForegroundColor Yellow
$Dirs = @("core", "mcp_servers", "notebooks", "config", "scripts", "strategies", "data_sources", "gui", "extension", "docs")
foreach ($dir in $Dirs) {
    New-Item -ItemType Directory -Path "TRQuant\$dir" -Force | Out-Null
}

# 复制核心代码
Write-Host "📋 复制核心代码..." -ForegroundColor Yellow
$CopyItems = @(
    @{Source="core"; Dest="TRQuant\core"},
    @{Source="mcp_servers"; Dest="TRQuant\mcp_servers"},
    @{Source="notebooks"; Dest="TRQuant\notebooks"},
    @{Source="scripts"; Dest="TRQuant\scripts"},
    @{Source="strategies"; Dest="TRQuant\strategies"},
    @{Source="data_sources"; Dest="TRQuant\data_sources"},
    @{Source="gui"; Dest="TRQuant\gui"},
    @{Source="extension"; Dest="TRQuant\extension"},
    @{Source="docs"; Dest="TRQuant\docs"},
    @{Source="config"; Dest="TRQuant\config"}
)

foreach ($item in $CopyItems) {
    $src = Join-Path $ProjectRoot $item.Source
    $dst = $item.Dest
    if (Test-Path $src) {
        Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# 复制根目录文件
Write-Host "📄 复制根目录文件..." -ForegroundColor Yellow
$RootFiles = @("requirements.txt", "requirements-dev.txt", "README.md", "CLAUDE.md", "VERSION")
foreach ($file in $RootFiles) {
    $src = Join-Path $ProjectRoot $file
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination "TRQuant\" -Force
    }
}

# 复制Python入口文件
Get-ChildItem -Path $ProjectRoot -Filter "*.py" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination "TRQuant\" -Force
}

# 创建配置模板
Write-Host "⚙️  创建配置模板..." -ForegroundColor Yellow
if (Test-Path "TRQuant\config\jqdata_config.json") {
    $ConfigTemplate = @{
        username = "请填写你的JQData账号"
        password = "请填写你的JQData密码"
        data_range = @{
            start_date = "2022-01-01"
            end_date = "2024-12-31"
        }
    }
    $ConfigTemplate | ConvertTo-Json -Depth 3 | Out-File -FilePath "TRQuant\config\jqdata_config.json.example" -Encoding UTF8
}

# 创建Windows安装脚本
Write-Host "🔧 创建Windows安装脚本..." -ForegroundColor Yellow
$InstallScript = @'
# TRQuant Windows安装脚本
Write-Host "🚀 TRQuant Windows安装程序" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 检查Python
Write-Host "📋 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或未添加到PATH" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
Write-Host "📦 创建Python虚拟环境..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 虚拟环境创建失败" -ForegroundColor Red
    exit 1
}

# 激活虚拟环境
& .\venv\Scripts\Activate.ps1

# 升级pip
Write-Host "⬆️  升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# 安装依赖
Write-Host "📦 安装Python依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "✅ 安装完成！" -ForegroundColor Green
'@
$InstallScript | Out-File -FilePath "TRQuant\install_windows.ps1" -Encoding UTF8

# 创建启动脚本
$StartJupyter = @'
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
jupyter notebook notebooks\research\
pause
'@
$StartJupyter | Out-File -FilePath "TRQuant\start_jupyter.bat" -Encoding ASCII

# 清理不需要的文件
Write-Host "🧹 清理不需要的文件..." -ForegroundColor Yellow
Get-ChildItem -Path "TRQuant" -Recurse -Include "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "TRQuant" -Recurse -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "TRQuant" -Recurse -Include ".git" -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 计算大小
$PackageSize = (Get-ChildItem -Path $PackageDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ""
Write-Host "✅ 打包完成！" -ForegroundColor Green
Write-Host "📦 打包目录: $PackageDir" -ForegroundColor Green
Write-Host "📊 目录大小: $([math]::Round($PackageSize, 2)) MB" -ForegroundColor Green

# 创建压缩包
Write-Host ""
Write-Host "🗜️  创建压缩包..." -ForegroundColor Yellow
Set-Location $ProjectRoot
Compress-Archive -Path $PackageDir -DestinationPath $PackageName -Force

$CompressedSize = (Get-Item $PackageName).Length / 1MB
Write-Host ""
Write-Host "✅ 压缩完成！" -ForegroundColor Green
Write-Host "📦 压缩包: $PackageName" -ForegroundColor Green
Write-Host "📊 压缩包大小: $([math]::Round($CompressedSize, 2)) MB" -ForegroundColor Green
Write-Host ""
Write-Host "📋 下一步:" -ForegroundColor Yellow
Write-Host "  1. 将 $PackageName 传输到目标Windows电脑" -ForegroundColor Yellow
Write-Host "  2. 解压到 C:\TRQuant" -ForegroundColor Yellow
Write-Host "  3. 运行 install_windows.ps1" -ForegroundColor Yellow
