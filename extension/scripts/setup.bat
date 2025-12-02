@echo off
REM TRQuant Cursor Extension - Windows 安装脚本
REM 用法: scripts\setup.bat

echo ==========================================
echo   TRQuant Cursor Extension 安装脚本
echo   平台: Windows
echo ==========================================

setlocal enabledelayedexpansion

REM 获取脚本目录
set "SCRIPT_DIR=%~dp0"
set "EXTENSION_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%EXTENSION_DIR%\.."

echo.
echo 项目路径: %PROJECT_ROOT%
echo Extension路径: %EXTENSION_DIR%
echo.

REM 1. 检查依赖
echo 🔍 检查系统依赖...
echo -------------------

set DEPS_OK=1

where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Node.js 未安装
    echo    请访问 https://nodejs.org/ 下载安装
    set DEPS_OK=0
) else (
    for /f "tokens=*" %%i in ('node --version') do echo ✓ Node.js 已安装: %%i
)

where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ npm 未安装
    set DEPS_OK=0
) else (
    for /f "tokens=*" %%i in ('npm --version') do echo ✓ npm 已安装: %%i
)

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python 未安装
    echo    请访问 https://www.python.org/ 下载安装
    set DEPS_OK=0
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✓ Python 已安装: %%i
)

if %DEPS_OK% equ 0 (
    echo.
    echo 请先安装缺失的依赖后重新运行此脚本
    pause
    exit /b 1
)

echo.

REM 2. 安装Node依赖
echo 📦 安装Node依赖...
echo -------------------
cd /d "%EXTENSION_DIR%"
call npm install
if %ERRORLEVEL% neq 0 (
    echo ❌ npm install 失败
    pause
    exit /b 1
)
echo ✓ Node依赖安装完成
echo.

REM 3. 创建Python虚拟环境
echo 🐍 配置Python环境...
echo -------------------
cd /d "%PROJECT_ROOT%"

if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate.bat

if exist "requirements.txt" (
    pip install -r requirements.txt
)

echo ✓ Python环境配置完成
echo.

REM 4. 构建Extension
echo 🔨 构建Extension...
echo -------------------
cd /d "%EXTENSION_DIR%"
call npm run compile
if %ERRORLEVEL% neq 0 (
    echo ❌ 构建失败
    pause
    exit /b 1
)
echo ✓ Extension构建完成
echo.

REM 5. 创建配置文件
echo ⚙️ 创建配置文件...
echo -------------------

set "PYTHON_PATH=%PROJECT_ROOT%\venv\Scripts\python.exe"

if not exist "%EXTENSION_DIR%\.vscode" mkdir "%EXTENSION_DIR%\.vscode"

(
echo {
echo   "trquant.pythonPath": "%PYTHON_PATH:\=\\%",
echo   "trquant.serverHost": "127.0.0.1",
echo   "trquant.serverPort": 5000,
echo   "trquant.mcpEnabled": true
echo }
) > "%EXTENSION_DIR%\.vscode\settings.json"

echo ✓ 配置文件已创建
echo.

REM 6. 验证安装
echo 🧪 验证安装...
echo -------------------

echo {"action": "get_market_status", "params": {}} | "%PYTHON_PATH%" "%EXTENSION_DIR%\python\bridge.py"

echo.
echo ==========================================
echo ✅ 安装完成！
echo ==========================================
echo.
echo 下一步：
echo 1. 在Cursor中按F5启动调试模式
echo 2. 或运行 'npm run package' 打包VSIX
echo 3. 在新窗口中测试 'TRQuant: 获取市场状态' 命令
echo.
echo 配置文件位置：
echo   %EXTENSION_DIR%\.vscode\settings.json
echo.

pause

