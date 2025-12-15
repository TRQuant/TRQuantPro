@echo off
chcp 65001 >nul
echo 🔄 投资手册更新工具
echo ====================
echo.
echo 请选择操作：
echo 1. 完整更新（推荐）
echo 2. 仅同步内容
echo 3. 仅优化格式
echo 4. 检查更新
echo 5. 创建备份
echo 6. 退出
echo.
set /p choice=请输入选择 (1-6): 

if "%choice%"=="1" (
    echo.
    echo 🚀 开始完整更新流程...
    python update_workflow.py --mode full
) else if "%choice%"=="2" (
    echo.
    echo 📄 开始内容同步...
    python update_workflow.py --mode sync
) else if "%choice%"=="3" (
    echo.
    echo 🎨 开始格式优化...
    python update_workflow.py --mode format
) else if "%choice%"=="4" (
    echo.
    echo 🔍 检查更新...
    python update_workflow.py --mode check
) else if "%choice%"=="5" (
    echo.
    echo 📦 创建备份...
    python update_workflow.py --mode backup
) else if "%choice%"=="6" (
    echo.
    echo 👋 再见！
    exit
) else (
    echo.
    echo ❌ 无效选择，请重新运行脚本
    pause
    exit
)

echo.
echo ✅ 操作完成！
pause 
chcp 65001 >nul
echo 🔄 投资手册更新工具
echo ====================
echo.
echo 请选择操作：
echo 1. 完整更新（推荐）
echo 2. 仅同步内容
echo 3. 仅优化格式
echo 4. 检查更新
echo 5. 创建备份
echo 6. 退出
echo.
set /p choice=请输入选择 (1-6): 

if "%choice%"=="1" (
    echo.
    echo 🚀 开始完整更新流程...
    python update_workflow.py --mode full
) else if "%choice%"=="2" (
    echo.
    echo 📄 开始内容同步...
    python update_workflow.py --mode sync
) else if "%choice%"=="3" (
    echo.
    echo 🎨 开始格式优化...
    python update_workflow.py --mode format
) else if "%choice%"=="4" (
    echo.
    echo 🔍 检查更新...
    python update_workflow.py --mode check
) else if "%choice%"=="5" (
    echo.
    echo 📦 创建备份...
    python update_workflow.py --mode backup
) else if "%choice%"=="6" (
    echo.
    echo 👋 再见！
    exit
) else (
    echo.
    echo ❌ 无效选择，请重新运行脚本
    pause
    exit
)

echo.
echo ✅ 操作完成！
pause 
 
 
 