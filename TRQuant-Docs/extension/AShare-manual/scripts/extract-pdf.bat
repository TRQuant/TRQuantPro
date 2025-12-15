@echo off
chcp 65001 >nul
title PDF内容提取工具

echo ========================================
echo           PDF内容提取工具
echo ========================================
echo.

if "%~1"=="" (
    echo 请将PDF文件拖拽到此批处理文件上，或者
    echo 在命令行中使用: extract-pdf.bat "PDF文件路径"
    echo.
    pause
    exit /b 1
)

set "PDF_FILE=%~1"
set "OUTPUT_DIR=pdf_extracted_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "OUTPUT_DIR=%OUTPUT_DIR: =0%"

echo 处理文件: %PDF_FILE%
echo 输出目录: %OUTPUT_DIR%
echo.

:: 检查PowerShell是否可用
powershell -Command "Write-Host 'PowerShell可用'" >nul 2>&1
if errorlevel 1 (
    echo 错误：系统中未找到PowerShell
    echo 请确保Windows PowerShell已安装
    pause
    exit /b 1
)

:: 调用PowerShell脚本
echo 正在启动提取过程...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0comprehensive-pdf-extractor.ps1" -PdfPath "%PDF_FILE%" -OutputDir "%OUTPUT_DIR%"

if errorlevel 1 (
    echo.
    echo 提取过程中出现错误，请检查：
    echo 1. PDF文件是否存在且可访问
    echo 2. Python环境是否正确安装
    echo 3. 必要的Python库是否已安装
    echo.
) else (
    echo.
    echo ========================================
    echo           提取完成！
    echo ========================================
    echo 输出目录: %OUTPUT_DIR%
    echo.
)

pause 