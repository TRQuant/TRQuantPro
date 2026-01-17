@echo off
REM QMT策略文件编码修复脚本
REM 使用方法: fix_encoding.bat "策略文件.py"

if "%~1"=="" (
    echo 使用方法: fix_encoding.bat "策略文件.py"
    exit /b 1
)

set "FILE=%~1"

echo 正在修复文件编码: %FILE%

REM 使用Python修复编码
python -c "with open(r'%FILE%', 'rb') as f: content = f.read(); text = content.decode('gbk') if b'\xbc' in content[:100] else content.decode('utf-8'); open(r'%FILE%', 'w', encoding='utf-8').write(text)"

if %ERRORLEVEL% EQU 0 (
    echo ✅ 文件编码修复成功
) else (
    echo ❌ 文件编码修复失败
    echo 建议: 使用Notepad++手动转换为UTF-8编码
)

pause
