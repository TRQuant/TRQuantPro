# Python依赖安装脚本
Write-Host "=== PDF提取工具依赖安装 ===" -ForegroundColor Cyan
Write-Host "正在安装必要的Python库..." -ForegroundColor Yellow
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python未安装或不在PATH中，请先安装Python 3.7+"
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

# 升级pip
Write-Host "升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 安装基础库
$basicLibraries = @(
    "PyPDF2",
    "pdfplumber", 
    "pdf2image",
    "Pillow",
    "pandas",
    "openpyxl",
    "pdfminer.six",
    "matplotlib",
    "numpy"
)

Write-Host "`n安装基础库..." -ForegroundColor Yellow
foreach ($lib in $basicLibraries) {
    Write-Host "安装 $lib..." -ForegroundColor Cyan
    pip install $lib
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "安装 $lib 失败，但继续安装其他库"
    }
}

# 安装表格提取库
Write-Host "`n安装表格提取库..." -ForegroundColor Yellow

# 安装Java依赖的tabula-py
Write-Host "安装 tabula-py..." -ForegroundColor Cyan
pip install tabula-py
if ($LASTEXITCODE -ne 0) {
    Write-Warning "tabula-py安装失败，可能需要Java环境"
    Write-Host "如需使用tabula功能，请安装Java: https://www.java.com/download/" -ForegroundColor Yellow
}

# 安装系统依赖的camelot
Write-Host "安装 camelot-py..." -ForegroundColor Cyan
pip install "camelot-py[cv]"
if ($LASTEXITCODE -ne 0) {
    Write-Warning "camelot-py安装失败，尝试安装简化版本"
    pip install camelot-py
}

# 安装OpenCV
Write-Host "安装 opencv-python..." -ForegroundColor Cyan
pip install opencv-python
if ($LASTEXITCODE -ne 0) {
    Write-Warning "opencv-python安装失败，图表检测功能可能受限"
}

# 安装poppler-utils (Windows)
Write-Host "`n检查poppler-utils..." -ForegroundColor Yellow
Write-Host "pdf2image需要poppler-utils支持" -ForegroundColor Gray

# 创建依赖检查脚本
$checkScript = @"
import sys
import importlib

libraries = [
    'PyPDF2', 'pdfplumber', 'pdf2image', 'PIL', 'pandas', 
    'tabula', 'camelot', 'pdfminer', 'matplotlib', 'cv2', 'numpy'
]

print("=== 依赖库检查结果 ===")
missing = []
for lib in libraries:
    try:
        if lib == 'PIL':
            importlib.import_module('PIL')
        elif lib == 'cv2':
            importlib.import_module('cv2')
        else:
            importlib.import_module(lib)
        print(f"✓ {lib}")
    except ImportError:
        print(f"✗ {lib} - 未安装或导入失败")
        missing.append(lib)

if missing:
    print(f"\n缺少的库: {', '.join(missing)}")
    print("请手动安装缺少的库")
else:
    print("\n✅ 所有依赖库检查通过！")
"@

$checkFile = "check_dependencies.py"
Set-Content -Path $checkFile -Value $checkScript -Encoding UTF8

Write-Host "`n检查安装结果..." -ForegroundColor Yellow
python $checkFile

Remove-Item $checkFile -Force

Write-Host "`n=== 安装完成 ===" -ForegroundColor Green
Write-Host "如果某些库安装失败，可以尝试：" -ForegroundColor Yellow
Write-Host "1. 手动安装: pip install 库名" -ForegroundColor Gray
Write-Host "2. 使用conda: conda install 库名" -ForegroundColor Gray
Write-Host "3. 对于poppler-utils，Windows用户可以：" -ForegroundColor Gray
Write-Host "   - 下载: https://github.com/oschwartz10612/poppler-windows/releases" -ForegroundColor Gray
Write-Host "   - 解压并添加到PATH环境变量" -ForegroundColor Gray
Write-Host ""

Write-Host "现在可以使用PDF提取工具了！" -ForegroundColor Green
pause 